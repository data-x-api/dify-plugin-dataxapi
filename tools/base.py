"""Shared invoke logic for every DataXAPI tool."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.client import DataXAPIClient, DataXAPIError, summarize
from tools.routes import RouteError


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
        except RouteError as exc:
            yield self.create_text_message(f"Invalid input: {exc} Nothing was charged.")
            return
        except DataXAPIError as exc:
            yield self.create_text_message(exc.describe())
            return
        yield self.create_json_message(summarize(envelope))
