"""Minimal DataXAPI HTTP client shared by the provider and the tools."""

from __future__ import annotations

import re
import uuid
from typing import Any

import httpx

BASE_URL = "https://api.dataxapi.com"
SOURCE = "dify"
USER_AGENT = "dataxapi-dify-plugin/0.1.0"
TIMEOUT_SECONDS = 90.0

# Endpoint IDs look like "douyin.videos.comments.list".
ENDPOINT_ID_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")
# A request carrying one of these goes as POST with a JSON body.
BODY_PARAMS = frozenset({"ids", "keywords"})


class DataXAPIError(Exception):
    """An error answer from DataXAPI, or a failure to reach it."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        status: int | None = None,
        request_id: str | None = None,
        charged: bool | None = False,
        retry: str | None = None,
    ) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.status = status
        self.request_id = request_id
        self.charged = charged
        self.retry = retry

    def describe(self) -> str:
        parts = [f"DataXAPI error {self.code}: {self.message}"]
        if self.charged is False:
            parts.append("Nothing was charged.")
        elif self.charged is None and self.request_id:
            parts.append(
                "Whether it was charged is not known; "
                f"look up the call at /v1/calls/{self.request_id}."
            )
        if self.retry:
            parts.append(f"Retry: {self.retry}.")
        if self.request_id:
            parts.append(f"Request ID: {self.request_id}.")
        return " ".join(parts)


def endpoint_path(endpoint_id: str) -> str:
    if not ENDPOINT_ID_RE.match(endpoint_id or ""):
        raise DataXAPIError(
            "invalid_endpoint",
            "The endpoint ID must look like 'douyin.videos.comments.list'.",
        )
    return "/v1/" + endpoint_id.replace(".", "/")


def clean_params(params: dict[str, Any]) -> dict[str, Any]:
    """Drop empty values so optional fields left blank are not sent."""
    return {k: v for k, v in params.items() if v is not None and v != "" and v != []}


def to_query(params: dict[str, Any]) -> dict[str, str]:
    query: dict[str, str] = {}
    for key, value in params.items():
        if isinstance(value, bool):
            query[key] = "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            query[key] = ",".join(str(v) for v in value)
        else:
            query[key] = str(value)
    return query


class DataXAPIClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        transport: httpx.BaseTransport | None = None,
        timeout: float = TIMEOUT_SECONDS,
    ) -> None:
        if not api_key:
            raise DataXAPIError("unauthorized", "No DataXAPI API key was given.")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._transport = transport
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            "X-Source": SOURCE,
            # A fresh key per call: a run started again is a new call.
            "Idempotency-Key": str(uuid.uuid4()),
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            with httpx.Client(transport=self._transport, timeout=self._timeout) as http:
                response = http.request(
                    method,
                    self._base_url + path,
                    params=query,
                    json=body,
                    headers=self._headers(),
                )
        except httpx.HTTPError as exc:
            # The exception text never includes request headers, so the key stays out.
            raise DataXAPIError(
                "connection_error",
                f"Could not reach DataXAPI ({type(exc).__name__}).",
                charged=None,
            ) from None

        try:
            payload = response.json()
        except ValueError:
            payload = None

        if response.is_success and isinstance(payload, dict):
            return payload

        if isinstance(payload, dict) and isinstance(payload.get("code"), str):
            raise DataXAPIError(
                payload["code"],
                str(payload.get("message") or "The request failed."),
                status=response.status_code,
                request_id=payload.get("request_id"),
                charged=payload.get("charged", False),
                retry=payload.get("retry"),
            )
        raise DataXAPIError(
            "http_error",
            f"HTTP {response.status_code} without a DataXAPI answer.",
            status=response.status_code,
            charged=None,
        )

    def call(self, endpoint_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Fetch one page from one endpoint. Each call is charged on its own."""
        path = endpoint_path(endpoint_id)
        given = clean_params(params or {})
        if BODY_PARAMS.intersection(given):
            return self._request("POST", path, body=given)
        return self._request("GET", path, query=to_query(given))

    def account(self) -> dict[str, Any]:
        """Balance and key details. Free; needs the key."""
        return self._request("GET", "/v1/account")


def summarize(envelope: dict[str, Any]) -> dict[str, Any]:
    """Keep what a workflow needs: data, paging, the charge and warnings."""
    meta = envelope.get("meta") or {}
    return {
        "request_id": envelope.get("request_id"),
        "endpoint": meta.get("capability"),
        "data": envelope.get("data"),
        "page": envelope.get("page"),
        "warnings": envelope.get("warnings") or [],
        "billing": meta.get("billing"),
        "fetched_at": meta.get("fetched_at"),
    }
