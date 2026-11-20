"""WeChat Channels account videos (wechat_channels.users.videos.list). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class WechatChannelsUsersVideosListTool(base.EndpointTool):
    endpoint = "wechat_channels.users.videos.list"
    list_params = frozenset([])
    integer_params = frozenset([])
