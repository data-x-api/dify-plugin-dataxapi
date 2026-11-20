"""WeChat Official Account articles (wechat_mp.accounts.articles.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatMpAccountsArticlesListTool(base.EndpointTool):
    endpoint = "wechat_mp.accounts.articles.list"
    list_params = frozenset([])
    integer_params = frozenset([])
