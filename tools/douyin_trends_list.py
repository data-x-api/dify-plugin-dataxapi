"""Douyin hot search board (douyin.trends.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinTrendsListTool(base.EndpointTool):
    endpoint = "douyin.trends.list"
    list_params = frozenset([])
    integer_params = frozenset([])
