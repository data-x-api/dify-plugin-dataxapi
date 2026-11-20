"""Shared invoke logic for every DataXAPI tool."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any, ClassVar

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.client import DataXAPIClient, DataXAPIError, summarize


class InputError(ValueError):
    """The tool's input cannot become a request; nothing was sent or charged."""


class DataXAPITool(Tool):
    # Tests swap this for an httpx.MockTransport.
    transport = None

    def client(self) -> DataXAPIClient:
        return DataXAPIClient(
            self.runtime.credentials.get("api_key", ""), transport=self.transport
        )

    def route(self, tool_parameters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        raise NotImplementedError

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            endpoint, params = self.route(tool_parameters)
            envelope = self.client().call(endpoint, params)
        except InputError as exc:
            yield self.create_text_message(f"Invalid input: {exc} Nothing was charged. 输入不对：没有发出请求，不收费。")
            return
        except DataXAPIError as exc:
            yield self.create_text_message(exc.describe())
            return
        yield self.create_json_message(summarize(envelope))


class EndpointTool(DataXAPITool):
    """One DataXAPI endpoint. The generated tool files set these three."""

    endpoint: ClassVar[str] = ""
    # Parameters the endpoint takes as a list; the form gives them comma-separated.
    list_params: ClassVar[frozenset[str]] = frozenset()
    integer_params: ClassVar[frozenset[str]] = frozenset()

    def route(self, tool_parameters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        params: dict[str, Any] = {}
        for name, value in tool_parameters.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                continue
            if name in self.list_params:
                items = value if isinstance(value, list) else [v.strip() for v in str(value).replace("，", ",").split(",")]
                items = [str(v).strip() for v in items if str(v).strip()]
                if items:
                    params[name] = items
            elif name in self.integer_params:
                try:
                    params[name] = int(float(value))
                except (TypeError, ValueError):
                    raise InputError(f"'{name}' must be a whole number.") from None
            elif isinstance(value, str):
                params[name] = value.strip()
            else:
                params[name] = value
        return self.endpoint, params
