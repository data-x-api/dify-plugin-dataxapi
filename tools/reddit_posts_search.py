"""Reddit post search (reddit.posts.search). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class RedditPostsSearchTool(base.EndpointTool):
    endpoint = "reddit.posts.search"
    list_params = frozenset([])
    integer_params = frozenset([])
