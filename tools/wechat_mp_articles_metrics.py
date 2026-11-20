"""WeChat Official Account article stats (wechat_mp.articles.metrics). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatMpArticlesMetricsTool(base.EndpointTool):
    endpoint = "wechat_mp.articles.metrics"
    list_params = frozenset([])
    integer_params = frozenset([])
