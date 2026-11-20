"""Douyin trend-index keyword trends (douyin.index.keywords.history). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinIndexKeywordsHistoryTool(base.EndpointTool):
    endpoint = "douyin.index.keywords.history"
    list_params = frozenset(['keywords'])
    integer_params = frozenset([])
