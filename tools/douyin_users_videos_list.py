"""Douyin user videos (douyin.users.videos.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinUsersVideosListTool(base.EndpointTool):
    endpoint = "douyin.users.videos.list"
    list_params = frozenset([])
    integer_params = frozenset([])
