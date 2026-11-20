"""Douyin video play count (douyin.videos.metrics). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinVideosMetricsTool(base.EndpointTool):
    endpoint = "douyin.videos.metrics"
    list_params = frozenset([])
    integer_params = frozenset([])
