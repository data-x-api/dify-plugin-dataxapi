"""Douyin Xingtu creator search (douyin.xingtu.creators.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class DouyinXingtuCreatorsSearchTool(base.EndpointTool):
    endpoint = "douyin.xingtu.creators.search"
    list_params = frozenset([])
    integer_params = frozenset(['cpm_max', 'cpm_min', 'followers_max', 'followers_min'])
