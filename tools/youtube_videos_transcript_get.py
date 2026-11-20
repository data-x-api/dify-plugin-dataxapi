"""YouTube video transcript (youtube.videos.transcript.get). Written by scripts/generate_tools.py."""

# Import the module, not the class: Dify loads the one Tool subclass found in this file.
from tools import base


class YoutubeVideosTranscriptGetTool(base.EndpointTool):
    endpoint = "youtube.videos.transcript.get"
    list_params = frozenset([])
    integer_params = frozenset([])
