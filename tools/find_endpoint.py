from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base
from tools.client import DataXAPIError


class FindEndpointTool(base.DataXAPITool):
    """Searches the catalog. Free: it calls no data endpoint."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        query = (tool_parameters.get("query") or "").strip()
        if not query:
            yield self.create_text_message("Describe the data you need, for example 'xiaohongshu note comments' or '公众号文章阅读数'.")
            return
        try:
            answer = self.client().find(query, (tool_parameters.get("platform") or "").strip() or None)
        except DataXAPIError as exc:
            yield self.create_text_message(exc.describe())
            return
        matches = []
        for m in (answer.get("data") or {}).get("matches") or []:
            if m.get("type") != "capability":
                continue
            matches.append(
                {
                    "endpoint": m.get("id"),
                    "name": m.get("name"),
                    "summary": m.get("summary"),
                    "required": m.get("required"),
                    "price": (m.get("pricing") or {}).get("price"),
                    "per": (m.get("pricing") or {}).get("per"),
                    "example_params": (m.get("example") or {}).get("params"),
                    "docs": "https://dataxapi.com" + (m.get("url") or "/apis/"),
                }
            )
        yield self.create_json_message({"matches": matches, "next": "Call one with the Call any endpoint tool: endpoint = matches[i].endpoint, params = a JSON object like example_params."})
