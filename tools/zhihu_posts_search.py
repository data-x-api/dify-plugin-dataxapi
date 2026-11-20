"""Zhihu content search (zhihu.posts.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class ZhihuPostsSearchTool(base.EndpointTool):
    endpoint = "zhihu.posts.search"
    list_params = frozenset([])
    integer_params = frozenset([])
