"""Xiaohongshu user notes (xiaohongshu.users.notes.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class XiaohongshuUsersNotesListTool(base.EndpointTool):
    endpoint = "xiaohongshu.users.notes.list"
    list_params = frozenset([])
    integer_params = frozenset([])
