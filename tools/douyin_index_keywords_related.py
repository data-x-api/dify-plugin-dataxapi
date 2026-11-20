"""Douyin trend-index related keywords (douyin.index.keywords.related). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinIndexKeywordsRelatedTool(base.EndpointTool):
    endpoint = "douyin.index.keywords.related"
    list_params = frozenset([])
    integer_params = frozenset([])
