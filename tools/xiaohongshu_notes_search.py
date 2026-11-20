"""Xiaohongshu note search (xiaohongshu.notes.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class XiaohongshuNotesSearchTool(base.EndpointTool):
    endpoint = "xiaohongshu.notes.search"
    list_params = frozenset([])
    integer_params = frozenset([])
