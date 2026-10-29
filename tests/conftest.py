import json
import sys
from pathlib import Path

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

API_KEY = "dx_test_not_a_real_key"


def ok_envelope(items=None, cursor=None, amount="0.02"):
    return {
        "code": "ok",
        "request_id": "11111111-1111-4111-8111-111111111111",
        "data": {"items": items if items is not None else [{"id": "1", "text": "hello"}]},
        "page": {"next_cursor": cursor, "has_more": cursor is not None, "returned": 1},
        "warnings": [],
        "meta": {
            "capability": "test.endpoint",
            "fetched_at": "2026-10-29T00:00:00Z",
            "billing": {"amount": amount, "currency": "USD", "balance_after": "9.98"},
        },
    }


def error_body(code="invalid_params", charged=False, retry="after_fix"):
    return {
        "code": code,
        "request_id": "22222222-2222-4222-8222-222222222222",
        "message": "A parameter is invalid",
        "message_zh": "参数不对",
        "charged": charged,
        "retry": retry,
        "retry_after_seconds": None,
        "param": "id",
        "docs_url": "https://dataxapi.com/docs/errors/",
    }


class Recorder:
    """An httpx transport that records requests and answers from a queue."""

    def __init__(self, *responses):
        self.requests: list[httpx.Request] = []
        self._responses = list(responses) or [(200, ok_envelope())]

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        status, body = self._responses.pop(0) if len(self._responses) > 1 else self._responses[0]
        if isinstance(body, (dict, list)):
            return httpx.Response(status, content=json.dumps(body).encode(), headers={"content-type": "application/json"})
        return httpx.Response(status, content=str(body).encode())

    @property
    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]


@pytest.fixture
def recorder_factory():
    return Recorder
