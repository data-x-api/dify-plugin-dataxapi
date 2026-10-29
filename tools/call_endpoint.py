import json
from typing import Any

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base, routes
from tools.client import ENDPOINT_ID_RE


class CallEndpointTool(base.DataXAPITool):
    def route(self, tool_parameters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        endpoint = (tool_parameters.get("endpoint") or "").strip()
        if not ENDPOINT_ID_RE.match(endpoint):
            raise routes.RouteError(
                "The endpoint ID must look like 'douyin.videos.comments.list'; "
                "find IDs at https://dataxapi.com/apis/."
            )
        raw = tool_parameters.get("params")
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            params: Any = {}
        elif isinstance(raw, dict):
            params = raw
        else:
            try:
                params = json.loads(raw)
            except ValueError:
                raise routes.RouteError("Parameters must be a JSON object.") from None
        if not isinstance(params, dict):
            raise routes.RouteError("Parameters must be a JSON object.")
        return endpoint, params
