"""WeChat Channels video detail (wechat_channels.videos.get). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatChannelsVideosGetTool(base.EndpointTool):
    endpoint = "wechat_channels.videos.get"
    list_params = frozenset([])
    integer_params = frozenset([])
