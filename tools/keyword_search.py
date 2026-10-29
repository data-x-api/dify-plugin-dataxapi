from typing import Any

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base, routes


class KeywordSearchTool(base.DataXAPITool):
    def route(self, tool_parameters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        return routes.search(
            tool_parameters.get("platform", ""),
            tool_parameters.get("query", ""),
            tool_parameters.get("sort"),
            tool_parameters.get("published_within"),
            tool_parameters.get("cursor"),
        )
