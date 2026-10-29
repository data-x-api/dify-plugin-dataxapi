import json
import uuid

import httpx
import pytest

from tests.conftest import API_KEY, Recorder, error_body, ok_envelope
from tools.client import DataXAPIClient, DataXAPIError, summarize


def test_get_builds_path_query_and_headers():
    rec = Recorder()
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    client.call("douyin.videos.comments.list", {"id": "123", "cursor": "", "fields": ["id", "text"], "x": None})
    req = rec.last
    assert req.method == "GET"
    assert req.url.host == "api.dataxapi.com"
    assert req.url.path == "/v1/douyin/videos/comments/list"
    assert dict(req.url.params) == {"id": "123", "fields": "id,text"}
    assert req.headers["Authorization"] == f"Bearer {API_KEY}"
    assert req.headers["X-Source"] == "dify"
    uuid.UUID(req.headers["Idempotency-Key"])


def test_each_call_gets_a_new_idempotency_key():
    rec = Recorder()
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    client.call("douyin.videos.search", {"query": "a"})
    client.call("douyin.videos.search", {"query": "a"})
    assert rec.requests[0].headers["Idempotency-Key"] != rec.requests[1].headers["Idempotency-Key"]


def test_ids_or_keywords_go_as_post_json():
    rec = Recorder()
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    client.call("x.users.get", {"ids": ["1", "2"], "view": "compact"})
    req = rec.last
    assert req.method == "POST"
    assert req.url.path == "/v1/x/users/get"
    assert json.loads(req.content) == {"ids": ["1", "2"], "view": "compact"}


def test_error_answer_is_raised_with_its_fields():
    rec = Recorder((400, error_body()))
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    with pytest.raises(DataXAPIError) as err:
        client.call("douyin.videos.comments.list", {"id": "x"})
    e = err.value
    assert e.code == "invalid_params" and e.status == 400 and e.charged is False
    assert "Nothing was charged" in e.describe()


def test_unknown_settlement_points_to_lookup():
    rec = Recorder((500, error_body("settlement_unknown", charged=None, retry="same_key")))
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    with pytest.raises(DataXAPIError) as err:
        client.call("douyin.videos.search", {"query": "a"})
    assert "/v1/calls/22222222-2222-4222-8222-222222222222" in err.value.describe()


def test_non_json_answer():
    rec = Recorder((502, "Bad gateway"))
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    with pytest.raises(DataXAPIError) as err:
        client.call("douyin.videos.search", {"query": "a"})
    assert err.value.code == "http_error"


def test_connection_error_does_not_leak_key():
    def boom(request):
        raise httpx.ConnectError(f"failed with {request.headers['Authorization']}")

    client = DataXAPIClient(API_KEY, transport=httpx.MockTransport(boom))
    with pytest.raises(DataXAPIError) as err:
        client.call("douyin.videos.search", {"query": "a"})
    assert API_KEY not in str(err.value) and API_KEY not in err.value.describe()


@pytest.mark.parametrize("bad", ["", "douyin", "Douyin.videos", "../etc/passwd", "douyin/videos/search", "a..b"])
def test_invalid_endpoint_ids_are_refused_before_any_request(bad):
    rec = Recorder()
    client = DataXAPIClient(API_KEY, transport=rec.transport)
    with pytest.raises(DataXAPIError):
        client.call(bad, {})
    assert rec.requests == []


def test_missing_key():
    with pytest.raises(DataXAPIError):
        DataXAPIClient("")


def test_summarize_keeps_data_page_and_billing():
    out = summarize(ok_envelope(cursor="c2"))
    assert out["page"]["next_cursor"] == "c2"
    assert out["billing"]["amount"] == "0.02"
    assert out["data"]["items"][0]["id"] == "1"
