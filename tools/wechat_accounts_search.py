"""WeChat Official Account live search (wechat.accounts.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatAccountsSearchTool(base.EndpointTool):
    endpoint = "wechat.accounts.search"
    list_params = frozenset([])
    integer_params = frozenset([])
