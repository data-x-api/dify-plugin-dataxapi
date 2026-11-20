"""WeChat Channels video comments (wechat_channels.videos.comments.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatChannelsVideosCommentsListTool(base.EndpointTool):
    endpoint = "wechat_channels.videos.comments.list"
    list_params = frozenset([])
    integer_params = frozenset([])
