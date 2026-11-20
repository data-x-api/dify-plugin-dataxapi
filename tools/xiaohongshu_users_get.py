"""Xiaohongshu user profile (xiaohongshu.users.get). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class XiaohongshuUsersGetTool(base.EndpointTool):
    endpoint = "xiaohongshu.users.get"
    list_params = frozenset([])
    integer_params = frozenset([])
