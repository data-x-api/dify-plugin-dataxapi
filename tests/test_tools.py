import json

import pytest
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from provider.dataxapi import DataXAPIProvider
from tests.conftest import API_KEY, Recorder, error_body, ok_envelope
from tools import base
from tools.account_posts import AccountPostsTool
from tools.call_endpoint import CallEndpointTool
from tools.keyword_search import KeywordSearchTool
from tools.post_comments import PostCommentsTool
from tools.wechat_mp_articles import WechatMpArticlesTool

JSON = ToolInvokeMessage.MessageType.JSON
TEXT = ToolInvokeMessage.MessageType.TEXT


def run(tool_cls, params, rec, monkeypatch):
    monkeypatch.setattr(base.DataXAPITool, "transport", rec.transport)
    tool = tool_cls.from_credentials({"api_key": API_KEY})
    return list(tool.invoke(params))


def test_wechat_mp_articles(monkeypatch):
    rec = Recorder((200, ok_envelope(cursor="next")))
    msgs = run(WechatMpArticlesTool, {"account_id": " gh_13c97ab93ce8 ", "cursor": ""}, rec, monkeypatch)
    assert rec.last.url.path == "/v1/wechat_mp/accounts/articles/list"
    assert dict(rec.last.url.params) == {"id": "gh_13c97ab93ce8"}
    assert len(msgs) == 1 and msgs[0].type == JSON
    assert msgs[0].message.json_object["page"]["next_cursor"] == "next"


@pytest.mark.parametrize(
    "platform,account,path,params",
    [
        ("douyin", "MS4wABC", "/v1/douyin/users/videos/list", {"id": "MS4wABC"}),
        ("xiaohongshu", "5a0b1c2d3e4f5a6b7c8d9e0f", "/v1/xiaohongshu/users/notes/list", {"id": "5a0b1c2d3e4f5a6b7c8d9e0f"}),
        (
            "xiaohongshu",
            "https://www.xiaohongshu.com/user/profile/abc?xsec_token=1",
            "/v1/xiaohongshu/users/notes/list",
            {"url": "https://www.xiaohongshu.com/user/profile/abc?xsec_token=1"},
        ),
        ("wechat_channels", "v2_abc@finder", "/v1/wechat_channels/users/videos/list", {"id": "v2_abc@finder"}),
        ("kuaishou", "123", "/v1/kuaishou/users/videos/list", {"id": "123"}),
        ("tiktok", "@nasa", "/v1/tiktok/users/videos/list", {"username": "nasa"}),
        ("bilibili", "8047632", "/v1/bilibili/users/videos/list", {"id": "8047632"}),
    ],
)
def test_account_posts_routes(monkeypatch, platform, account, path, params):
    rec = Recorder()
    run(AccountPostsTool, {"platform": platform, "account": account}, rec, monkeypatch)
    assert rec.last.url.path == path
    assert dict(rec.last.url.params) == params


@pytest.mark.parametrize(
    "platform,post,path,params",
    [
        ("douyin", "7694940173372575014", "/v1/douyin/videos/comments/list", {"id": "7694940173372575014"}),
        ("wechat_mp", "https://mp.weixin.qq.com/s/abc", "/v1/wechat_mp/articles/comments/list", {"url": "https://mp.weixin.qq.com/s/abc"}),
        ("wechat_channels", "1234", "/v1/wechat_channels/videos/comments/list", {"id": "1234"}),
        ("tiktok", "https://www.tiktok.com/@a/video/1", "/v1/tiktok/videos/comments/list", {"url": "https://www.tiktok.com/@a/video/1"}),
        ("bilibili", "BV1ECeJ65EZS", "/v1/bilibili/videos/comments/list", {"id": "BV1ECeJ65EZS"}),
    ],
)
def test_comments_routes(monkeypatch, platform, post, path, params):
    rec = Recorder()
    run(PostCommentsTool, {"platform": platform, "post": post, "cursor": "c1"}, rec, monkeypatch)
    assert rec.last.url.path == path
    assert dict(rec.last.url.params) == {**params, "cursor": "c1"}


def test_search_keeps_filters_the_platform_accepts(monkeypatch):
    rec = Recorder()
    run(KeywordSearchTool, {"platform": "douyin", "query": "咖啡", "sort": "latest", "published_within": "week"}, rec, monkeypatch)
    assert rec.last.url.path == "/v1/douyin/videos/search"
    assert dict(rec.last.url.params) == {"query": "咖啡", "sort": "latest", "published_within": "week"}


def test_search_drops_filters_the_platform_does_not_accept(monkeypatch):
    rec = Recorder()
    run(KeywordSearchTool, {"platform": "kuaishou", "query": "coffee", "sort": "latest", "published_within": "week"}, rec, monkeypatch)
    assert rec.last.url.path == "/v1/kuaishou/videos/search"
    assert dict(rec.last.url.params) == {"query": "coffee"}
    rec = Recorder()
    run(KeywordSearchTool, {"platform": "xiaohongshu", "query": "coffee", "sort": "popular", "published_within": "week"}, rec, monkeypatch)
    assert dict(rec.last.url.params) == {"query": "coffee", "sort": "popular"}


def test_wechat_search(monkeypatch):
    rec = Recorder()
    run(KeywordSearchTool, {"platform": "wechat", "query": "AI"}, rec, monkeypatch)
    assert rec.last.url.path == "/v1/wechat/posts/search"


def test_call_endpoint_get_and_post(monkeypatch):
    rec = Recorder()
    run(CallEndpointTool, {"endpoint": "douyin.users.get", "params": '{"id": "MS4w1"}'}, rec, monkeypatch)
    assert rec.last.method == "GET" and rec.last.url.path == "/v1/douyin/users/get"
    run(CallEndpointTool, {"endpoint": "x.users.get", "params": '{"ids": ["1"]}'}, rec, monkeypatch)
    assert rec.last.method == "POST" and json.loads(rec.last.content) == {"ids": ["1"]}


@pytest.mark.parametrize(
    "params",
    [
        {"endpoint": "douyin/users/get", "params": "{}"},
        {"endpoint": "douyin.users.get", "params": "not json"},
        {"endpoint": "douyin.users.get", "params": "[1, 2]"},
    ],
)
def test_call_endpoint_bad_input_sends_nothing(monkeypatch, params):
    rec = Recorder()
    msgs = run(CallEndpointTool, params, rec, monkeypatch)
    assert rec.requests == []
    assert msgs[0].type == TEXT and "Nothing was charged" in msgs[0].message.text


def test_unknown_platform_sends_nothing(monkeypatch):
    rec = Recorder()
    msgs = run(AccountPostsTool, {"platform": "myspace", "account": "a"}, rec, monkeypatch)
    assert rec.requests == [] and msgs[0].type == TEXT


def test_api_error_becomes_text(monkeypatch):
    rec = Recorder((404, error_body("not_found", retry="no")))
    msgs = run(PostCommentsTool, {"platform": "douyin", "post": "1"}, rec, monkeypatch)
    assert msgs[0].type == TEXT
    assert "not_found" in msgs[0].message.text and "Nothing was charged" in msgs[0].message.text


def test_provider_validates_with_free_account_endpoint(monkeypatch):
    rec = Recorder((200, {"code": "ok", "request_id": "r", "data": {"balance": "1.00", "currency": "USD"}}))
    monkeypatch.setattr(DataXAPIProvider, "transport", rec.transport)
    DataXAPIProvider().validate_credentials({"api_key": API_KEY})
    assert rec.last.method == "GET" and rec.last.url.path == "/v1/account"
    assert rec.last.headers["X-Source"] == "dify"


def test_provider_rejects_bad_key(monkeypatch):
    rec = Recorder((401, error_body("unauthorized", retry="no")))
    monkeypatch.setattr(DataXAPIProvider, "transport", rec.transport)
    with pytest.raises(ToolProviderCredentialValidationError):
        DataXAPIProvider().validate_credentials({"api_key": "dx_wrong"})
