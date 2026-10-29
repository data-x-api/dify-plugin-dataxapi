from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.client import DataXAPIClient, DataXAPIError


class DataXAPIProvider(ToolProvider):
    # Tests swap this for an httpx.MockTransport.
    transport = None

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # GET /v1/account is free and needs the key, so checking costs nothing.
        try:
            DataXAPIClient(credentials.get("api_key", ""), transport=self.transport).account()
        except DataXAPIError as exc:
            raise ToolProviderCredentialValidationError(exc.describe()) from None
