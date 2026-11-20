"""Douyin video search (douyin.videos.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinVideosSearchTool(base.EndpointTool):
    endpoint = "douyin.videos.search"
    list_params = frozenset([])
    integer_params = frozenset([])
