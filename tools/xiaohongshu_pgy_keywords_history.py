"""Xiaohongshu PGY keyword search index (xiaohongshu.pgy.keywords.history). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class XiaohongshuPgyKeywordsHistoryTool(base.EndpointTool):
    endpoint = "xiaohongshu.pgy.keywords.history"
    list_params = frozenset([])
    integer_params = frozenset([])
