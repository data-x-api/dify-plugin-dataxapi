import importlib
import json

import pytest
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from provider.dataxapi import DataXAPIProvider
from tests.conftest import API_KEY, Recorder, error_body, ok_envelope
from tools import base
from tools.call_endpoint import CallEndpointTool
from tools.find_endpoint import FindEndpointTool

JSON = ToolInvokeMessage.MessageType.JSON
TEXT = ToolInvokeMessage.MessageType.TEXT


def tool(name):
    module = importlib.import_module(f"tools.{name}")
    return next(v for v in vars(module).values() if isinstance(v, type) and issubclass(v, base.DataXAPITool) and v.__module__ == module.__name__)


def run(tool_cls, params, rec, monkeypatch):
    monkeypatch.setattr(base.DataXAPITool, "transport", rec.transport)
    return list(tool_cls.from_credentials({"api_key": API_KEY}).invoke(params))


def test_endpoint_tool_sends_what_was_given_and_drops_blanks(monkeypatch):
    rec = Recorder((200, ok_envelope(cursor="next")))
    msgs = run(tool("wechat_mp_accounts_articles_list"), {"id": " gh_13c97ab93ce8 ", "tab": "", "cursor": None}, rec, monkeypatch)
    assert rec.last.method == "GET" and rec.last.url.path == "/v1/wechat_mp/accounts/articles/list"
    assert dict(rec.last.url.params) == {"id": "gh_13c97ab93ce8"}
    assert rec.last.headers["X-Source"] == "dify"
    assert msgs[0].type == JSON and msgs[0].message.json_object["page"]["next_cursor"] == "next"
    assert msgs[0].message.json_object["billing"]["amount"] == "0.02"


def test_select_and_cursor_pass_through(monkeypatch):
    rec = Recorder()
    run(tool("xiaohongshu_notes_search"), {"query": "咖啡", "sort": "latest", "published_within": "week", "cursor": "c1"}, rec, monkeypatch)
    assert rec.last.url.path == "/v1/xiaohongshu/notes/search"
    assert dict(rec.last.url.params) == {"query": "咖啡", "sort": "latest", "published_within": "week", "cursor": "c1"}


def test_list_parameter_goes_as_a_json_body(monkeypatch):
    rec = Recorder()
    run(tool("douyin_index_keywords_history"), {"keywords": "咖啡，CityWalk, 露营", "since": "2026-09-01", "until": "2026-09-30"}, rec, monkeypatch)
    assert rec.last.method == "POST" and rec.last.url.path == "/v1/douyin/index/keywords/history"
    assert json.loads(rec.last.content) == {"keywords": ["咖啡", "CityWalk", "露营"], "since": "2026-09-01", "until": "2026-09-30"}


def test_whole_numbers_are_sent_as_numbers_and_bad_ones_send_nothing(monkeypatch):
    rec = Recorder()
    run(tool("douyin_xingtu_creators_search"), {"query": "美妆", "followers_min": 10000.0}, rec, monkeypatch)
    assert dict(rec.last.url.params) == {"query": "美妆", "followers_min": "10000"}
    rec = Recorder()
    msgs = run(tool("douyin_xingtu_creators_search"), {"query": "美妆", "followers_min": "many"}, rec, monkeypatch)
    assert rec.requests == [] and msgs[0].type == TEXT and "Nothing was charged" in msgs[0].message.text


def test_api_error_becomes_text(monkeypatch):
    rec = Recorder((404, error_body("not_found", retry="no")))
    msgs = run(tool("douyin_videos_comments_list"), {"id": "1"}, rec, monkeypatch)
    assert msgs[0].type == TEXT
    assert "not_found" in msgs[0].message.text and "Nothing was charged" in msgs[0].message.text


def test_find_endpoint_is_the_free_catalog_search(monkeypatch):
    answer = {
        "code": "ok",
        "data": {
            "matches": [
                {
                    "type": "capability",
                    "id": "wechat_mp.articles.metrics",
                    "url": "/apis/wechat_mp/articles/metrics/",
                    "name": {"zh": "微信公众号文章互动数据", "en": "WeChat Official Account article stats"},
                    "summary": {"zh": "阅读、点赞", "en": "reads, likes"},
                    "required": ["url"],
                    "pricing": {"per": "call", "price": "0.02"},
                    "example": {"params": {"url": "https://mp.weixin.qq.com/s?__biz=1"}},
                },
                {"type": "board", "id": "x"},
            ]
        },
    }
    rec = Recorder((200, answer))
    msgs = run(FindEndpointTool, {"query": "公众号文章阅读数", "platform": ""}, rec, monkeypatch)
    assert rec.last.method == "GET" and rec.last.url.path == "/v1/catalog/search"
    assert dict(rec.last.url.params) == {"query": "公众号文章阅读数"}
    matches = msgs[0].message.json_object["matches"]
    assert [m["endpoint"] for m in matches] == ["wechat_mp.articles.metrics"]
    assert matches[0]["price"] == "0.02" and matches[0]["docs"].endswith("/apis/wechat_mp/articles/metrics/")


def test_find_endpoint_without_a_need_sends_nothing(monkeypatch):
    rec = Recorder()
    msgs = run(FindEndpointTool, {"query": "  "}, rec, monkeypatch)
    assert rec.requests == [] and msgs[0].type == TEXT


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
