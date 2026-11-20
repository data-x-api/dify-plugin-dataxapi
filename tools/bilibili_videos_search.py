"""Bilibili video search (bilibili.videos.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class BilibiliVideosSearchTool(base.EndpointTool):
    endpoint = "bilibili.videos.search"
    list_params = frozenset([])
    integer_params = frozenset([])
