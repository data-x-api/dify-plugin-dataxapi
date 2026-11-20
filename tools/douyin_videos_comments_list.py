"""Douyin video comments (douyin.videos.comments.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinVideosCommentsListTool(base.EndpointTool):
    endpoint = "douyin.videos.comments.list"
    list_params = frozenset([])
    integer_params = frozenset([])
