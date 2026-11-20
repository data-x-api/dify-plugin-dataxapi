"""Douyin user profile (douyin.users.get). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinUsersGetTool(base.EndpointTool):
    endpoint = "douyin.users.get"
    list_params = frozenset([])
    integer_params = frozenset([])
