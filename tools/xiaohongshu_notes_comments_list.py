"""Xiaohongshu note comments (xiaohongshu.notes.comments.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class XiaohongshuNotesCommentsListTool(base.EndpointTool):
    endpoint = "xiaohongshu.notes.comments.list"
    list_params = frozenset([])
    integer_params = frozenset([])
