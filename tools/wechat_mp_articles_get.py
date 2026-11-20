"""WeChat Official Account article detail (wechat_mp.articles.get). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatMpArticlesGetTool(base.EndpointTool):
    endpoint = "wechat_mp.articles.get"
    list_params = frozenset([])
    integer_params = frozenset([])
