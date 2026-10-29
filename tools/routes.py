"""Which DataXAPI endpoint serves each task on each platform.

Checked against https://dataxapi.com/openapi.json (catalog revision c48ce454ae6c4c65).
"""

from __future__ import annotations

from typing import Any

WECHAT_MP_ARTICLES = "wechat_mp.accounts.articles.list"

# platform -> (endpoint, how the account is identified)
ACCOUNT_POSTS: dict[str, tuple[str, str]] = {
    "douyin": ("douyin.users.videos.list", "id"),
    "xiaohongshu": ("xiaohongshu.users.notes.list", "id_or_url"),
    "wechat_channels": ("wechat_channels.users.videos.list", "id"),
    "kuaishou": ("kuaishou.users.videos.list", "id"),
    "tiktok": ("tiktok.users.videos.list", "username"),
    "bilibili": ("bilibili.users.videos.list", "id"),
}

# platform -> (endpoint, how the post is identified)
COMMENTS: dict[str, tuple[str, str]] = {
    "douyin": ("douyin.videos.comments.list", "id"),
    "xiaohongshu": ("xiaohongshu.notes.comments.list", "id_or_url"),
    "wechat_channels": ("wechat_channels.videos.comments.list", "id"),
    "wechat_mp": ("wechat_mp.articles.comments.list", "url"),
    "kuaishou": ("kuaishou.videos.comments.list", "id"),
    "tiktok": ("tiktok.videos.comments.list", "id_or_url"),
    "bilibili": ("bilibili.videos.comments.list", "id"),
}

# platform -> (endpoint, optional filters it accepts)
SEARCH: dict[str, tuple[str, frozenset[str]]] = {
    "douyin": ("douyin.videos.search", frozenset({"sort", "published_within"})),
    "xiaohongshu": ("xiaohongshu.notes.search", frozenset({"sort"})),
    "wechat_channels": ("wechat_channels.videos.search", frozenset({"sort", "published_within"})),
    "wechat": ("wechat.posts.search", frozenset({"sort", "published_within"})),
    "kuaishou": ("kuaishou.videos.search", frozenset()),
    "tiktok": ("tiktok.videos.search", frozenset({"sort", "published_within"})),
}


class RouteError(ValueError):
    pass


def _identify(kind: str, value: str) -> dict[str, str]:
    value = (value or "").strip()
    if not value:
        raise RouteError("An account or post identifier is required.")
    if kind == "username":
        return {"username": value.lstrip("@")}
    if kind == "url":
        return {"url": value}
    if kind == "id_or_url":
        # A link or a whole share text with a link in it goes as url.
        return {"url": value} if "http" in value or "xhslink" in value else {"id": value}
    return {"id": value}


def _platform(table: dict[str, Any], platform: str) -> Any:
    if platform not in table:
        raise RouteError(f"Unsupported platform '{platform}'. Choose one of: {', '.join(table)}.")
    return table[platform]


def account_posts(platform: str, account: str, cursor: str | None = None) -> tuple[str, dict]:
    endpoint, kind = _platform(ACCOUNT_POSTS, platform)
    return endpoint, {**_identify(kind, account), "cursor": cursor}


def comments(platform: str, post: str, cursor: str | None = None) -> tuple[str, dict]:
    endpoint, kind = _platform(COMMENTS, platform)
    return endpoint, {**_identify(kind, post), "cursor": cursor}


def search(
    platform: str,
    query: str,
    sort: str | None = None,
    published_within: str | None = None,
    cursor: str | None = None,
) -> tuple[str, dict]:
    endpoint, accepts = _platform(SEARCH, platform)
    if not (query or "").strip():
        raise RouteError("Search terms are required.")
    params: dict[str, Any] = {"query": query.strip(), "cursor": cursor}
    # Filters a platform does not accept are left out rather than refused.
    if "sort" in accepts:
        params["sort"] = sort
    if "published_within" in accepts:
        params["published_within"] = published_within
    return endpoint, params
