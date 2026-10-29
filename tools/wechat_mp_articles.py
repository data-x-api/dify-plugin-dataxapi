from typing import Any

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base, routes


class WechatMpArticlesTool(base.DataXAPITool):
    def route(self, tool_parameters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        account_id = (tool_parameters.get("account_id") or "").strip()
        if not account_id:
            raise routes.RouteError("The account's original ID (gh_...) is required.")
        return routes.WECHAT_MP_ARTICLES, {
            "id": account_id,
            "cursor": tool_parameters.get("cursor"),
        }
