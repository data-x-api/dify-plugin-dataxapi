from typing import Any

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base, routes


class PostCommentsTool(base.DataXAPITool):
    def route(self, tool_parameters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        return routes.comments(
            tool_parameters.get("platform", ""),
            tool_parameters.get("post", ""),
            tool_parameters.get("cursor"),
        )
