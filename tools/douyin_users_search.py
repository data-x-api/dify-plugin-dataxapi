"""Douyin user search (douyin.users.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinUsersSearchTool(base.EndpointTool):
    endpoint = "douyin.users.search"
    list_params = frozenset([])
    integer_params = frozenset([])
