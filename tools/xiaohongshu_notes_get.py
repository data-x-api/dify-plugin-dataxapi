"""Xiaohongshu note detail (xiaohongshu.notes.get). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class XiaohongshuNotesGetTool(base.EndpointTool):
    endpoint = "xiaohongshu.notes.get"
    list_params = frozenset([])
    integer_params = frozenset([])
