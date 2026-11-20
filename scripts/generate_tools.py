"""Writes one Dify tool per chosen DataXAPI endpoint from the live catalog.

    .venv/bin/python scripts/generate_tools.py [catalog.json]

Reads https://api.dataxapi.com/v1/catalog (free, no key) unless a saved copy is given. For each endpoint in
CHOSEN it writes tools/<name>.yaml (names, descriptions and parameters in Chinese and English, from the catalog)
and tools/<name>.py (the endpoint's ID), then the provider's tool list and the tool tables in both READMEs.
Run it again when the catalog or the prices change; it overwrites what it wrote and nothing else.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# The endpoints the most accounts called in the 30 days to 2026-11-20 (DataXAPI's own call records, internal
# accounts left out), in that order, then four for the platforms abroad. Everything else: find_endpoint and
# call_endpoint.
CHOSEN = [
    "xiaohongshu.notes.search",
    "douyin.videos.search",
    "wechat_mp.accounts.articles.list",
    "douyin.videos.comments.list",
    "douyin.videos.metrics",
    "douyin.videos.get",
    "douyin.users.videos.list",
    "wechat_mp.articles.get",
    "douyin.users.get",
    "xiaohongshu.notes.get",
    "douyin.users.search",
    "douyin.index.keywords.history",
    "douyin.trends.list",
    "wechat.posts.search",
    "wechat_channels.videos.search",
    "wechat.accounts.search",
    "wechat_channels.videos.get",
    "xiaohongshu.notes.comments.list",
    "wechat_channels.users.videos.list",
    "xiaohongshu.users.notes.list",
    "weibo.posts.search",
    "bilibili.videos.search",
    "xiaohongshu.users.get",
    "xiaohongshu.pgy.keywords.history",
    "wechat_mp.articles.metrics",
    "wechat_channels.videos.comments.list",
    "douyin.index.keywords.related",
    "zhihu.posts.search",
    "kuaishou.videos.search",
    "douyin.xingtu.creators.search",
    "tiktok.videos.search",
    "youtube.videos.transcript.get",
    "x.posts.search",
    "reddit.posts.search",
]
HAND_WRITTEN = ["tools/find_endpoint.yaml", "tools/call_endpoint.yaml"]
SKIP_PARAMS = {"view", "fields", "include"}  # the plugin always returns the standard view


def tool_name(endpoint: str) -> str:
    return endpoint.replace(".", "_")


def class_name(endpoint: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[._]", endpoint)) + "Tool"


def money(value: str) -> str:
    return "$" + value


def price_words(pricing: dict) -> tuple[str, str]:
    if pricing["per"] == "item":
        return (
            f"每条 {money(pricing['price'])}，一次最多 {money(pricing['max_charge'])}",
            f"{money(pricing['price'])} an item, at most {money(pricing['max_charge'])} a call",
        )
    return f"{money(pricing['price'])} 一次", f"{money(pricing['price'])} a call"


# Chinese names for the option values the chosen tools use; any other value shows as it is.
VALUE_ZH = {
    "relevance": "综合", "latest": "最新", "popular": "最热", "most_comments": "评论最多", "most_favorites": "收藏最多",
    "day": "一天内", "week": "一周内", "half_year": "半年内", "month": "一个月内", "year": "一年内",
    "video": "视频", "image": "图文", "articles": "文章", "videos": "视频", "images": "贴图",
    "hot": "最热", "new": "最新", "top": "最热", "all": "全部",
    "article": "公众号文章", "answer": "回答", "female": "女", "male": "男", "lowest_cpm": "千次播放成本最低",
    "under_1_min": "1 分钟以内", "1_to_5_min": "1 到 5 分钟", "over_5_min": "5 分钟以上",
    "hot_search": "热搜榜", "rising": "上升热点", "topics": "话题热榜", "searches": "热门搜索词", "music": "音乐榜",
}


def value_en(value: str) -> str:
    words = value.replace("_", " ")
    return words[:1].upper() + words[1:]


# Short field names for the form; id, url and anything not here take the first words of the endpoint's own doc.
LABELS = {
    "query": ("Search terms", "搜索词"), "sort": ("Sort", "排序"), "published_within": ("Published within", "发布时间"),
    "type": ("Type", "类型"), "keyword": ("Keyword", "关键词"), "keywords": ("Keywords (several)", "多个关键词"),
    "since": ("From (date)", "开始日期"), "until": ("To (date)", "结束日期"), "followers_min": ("Followers at least", "粉丝数不少于"),
    "followers_max": ("Followers at most", "粉丝数不多于"), "cpm_min": ("CPM at least", "千次播放成本下限"),
    "cpm_max": ("CPM at most", "千次播放成本上限"), "gender": ("Gender", "性别"), "duration": ("Duration", "视频时长"),
    "lang": ("Language", "语言"), "board": ("Board", "榜单"), "tab": ("Tab", "栏目"),
    "export_id": ("Search result video ID", "搜索结果里的作品编号"), "cursor": ("Next page cursor", "翻页游标"),
}


def short(text: str, seps: str) -> str:
    head = re.split(f"[{seps}]", text, maxsplit=1)[0].strip()
    head = re.sub(r"^The ", "", head)
    return head[:1].upper() + head[1:] if 0 < len(head) <= 40 else head[:40].rsplit(" ", 1)[0]


def param_decl(name: str, spec: dict, common: dict) -> dict:
    kind = (common.get(name) or {}).get("type", "string")
    doc = spec.get("doc") or {"zh": (common.get(name) or {}).get("zh", name), "en": (common.get(name) or {}).get("en", name)}
    example = spec.get("example")
    if isinstance(example, list):
        example = ",".join(map(str, example))
    zh, en = doc["zh"], doc["en"]
    if kind == "string[]":
        zh, en = zh + "。多个用英文逗号隔开", en + ". Several separated by commas"
    if example not in (None, ""):
        zh, en = f"{zh}。例：{example}", f"{en}. Example: {example}"
        zh = "翻页：填上一次返回里的 page.next_cursor。每一页单独计费"
        en = "Next page: the page.next_cursor of the last answer. Each page is charged on its own"
    decl: dict = {
        "name": name,
        "type": "number" if kind == "integer" else "string",
        "required": bool(spec.get("required")),
        "form": "llm",
        "label": {"en_US": LABELS[name][0], "zh_Hans": LABELS[name][1]}
        if name in LABELS
        else {"en_US": short(doc["en"], ",;:("), "zh_Hans": short(doc["zh"], "，；：（,(")},
        "human_description": {"en_US": en, "zh_Hans": zh},
        "llm_description": en,
    }
    if spec.get("values"):
        decl["type"] = "select"
        decl["options"] = [{"value": v, "label": {"en_US": value_en(v), "zh_Hans": VALUE_ZH.get(v, v)}} for v in spec["values"]]
        if spec.get("default"):
            decl["default"] = spec["default"]
    return decl


def tool_decl(cap: dict, common: dict) -> dict:
    zh_price, en_price = price_words(cap["pricing"])
    params = [param_decl(n, s, common) for n, s in cap["params"].items() if n not in SKIP_PARAMS]
    if "cursor" in cap.get("request_params", []):
        params.append(param_decl("cursor", {}, common))
    params.sort(key=lambda p: not p["required"])
    page = "One call returns one page; for more, call again with page.next_cursor as cursor (each page is its own charged call)." if "cursor" in cap.get("request_params", []) else "One call, one answer."
    return {
        "identity": {
            "name": tool_name(cap["id"]),
            "author": "dataxapi",
            "label": {"en_US": cap["name"]["en"], "zh_Hans": cap["name"]["zh"]},
        },
        "description": {
            "human": {
                "en_US": f"{cap['summary']['en']} {en_price}; errors are not charged. No sign-in to your own platform account.",
                "zh_Hans": f"{cap['summary']['zh']}{zh_price}，出错不收费。不用登录你自己的平台账号。",
            },
            "llm": f"DataXAPI endpoint {cap['id']}. {cap['summary']['en']} {page} {en_price}; errors are not charged.",
        },
        "parameters": params,
        "extra": {"python": {"source": f"tools/{tool_name(cap['id'])}.py"}},
    }


def tool_source(cap: dict, common: dict) -> str:
    names = [n for n in cap["params"] if n not in SKIP_PARAMS]
    lists = sorted(n for n in names if (common.get(n) or {}).get("type") == "string[]")
    ints = sorted(n for n in names if (common.get(n) or {}).get("type") == "integer")
    return (
        f'"""{cap["name"]["en"]} ({cap["id"]}). Written by scripts/generate_tools.py."""\n\n'
        "# Import the module, not the class: Dify loads the one Tool subclass found in this file.\n"
        "from tools import base\n\n\n"
        f"class {class_name(cap['id'])}(base.EndpointTool):\n"
        f'    endpoint = "{cap["id"]}"\n'
        f"    list_params = frozenset({lists!r})\n"
        f"    integer_params = frozenset({ints!r})\n"
    )


def table(caps: list[dict], lang: str) -> str:
    rows = []
    if lang == "zh":
        rows.append("| 工具 | 拿到什么 | 价格 |\n|---|---|---|")
        for c in caps:
            rows.append(f"| {c['name']['zh']} | {c['summary']['zh']} | {price_words(c['pricing'])[0]} |")
        rows.append("| 找接口 | 用一句话描述要的数据，列出能用的接口、价格和参数 | 免费 |")
        rows.append("| 调用任意接口 | 用接口编号加参数调用全部 237 个接口里的任何一个 | 按该接口的价格 |")
    else:
        rows.append("| Tool | What it returns | Price |\n|---|---|---|")
        for c in caps:
            rows.append(f"| {c['name']['en']} | {c['summary']['en']} | {price_words(c['pricing'])[1]} |")
        rows.append("| Find an endpoint | Endpoints for a need described in plain words, with price and parameters | free |")
        rows.append("| Call any endpoint | Any of the 237 endpoints by its ID | that endpoint's price |")
    return "\n".join(rows)


def replace_between(path: Path, text: str) -> None:
    body = path.read_text()
    start, end = "<!-- tools:start -->", "<!-- tools:end -->"
    if start not in body:
        raise SystemExit(f"{path} has no {start} marker")
    before, rest = body.split(start, 1)
    _, after = rest.split(end, 1)
    path.write_text(f"{before}{start}\n{text}\n{end}{after}")


def main() -> None:
    if len(sys.argv) > 1:
        catalog = json.loads(Path(sys.argv[1]).read_text())
    else:
        with urllib.request.urlopen("https://api.dataxapi.com/v1/catalog", timeout=60) as r:
            catalog = json.load(r)
    data = catalog["data"]
    caps = {c["id"]: c for c in data["capabilities"]}
    missing = [e for e in CHOSEN if e not in caps]
    if missing:
        raise SystemExit(f"not in the catalog: {missing}")
    common = data["params"]
    chosen = [caps[e] for e in CHOSEN]
    dumper = dict(allow_unicode=True, sort_keys=False, width=1000)
    for cap in chosen:
        name = tool_name(cap["id"])
        (ROOT / "tools" / f"{name}.yaml").write_text(yaml.safe_dump(tool_decl(cap, common), **dumper))
        (ROOT / "tools" / f"{name}.py").write_text(tool_source(cap, common))
    provider_path = ROOT / "provider" / "dataxapi.yaml"
    provider = yaml.safe_load(provider_path.read_text())
    provider["tools"] = [f"tools/{tool_name(e)}.yaml" for e in CHOSEN] + HAND_WRITTEN
    provider_path.write_text(yaml.safe_dump(provider, **dumper))
    replace_between(ROOT / "README.md", table(chosen, "en"))
    replace_between(ROOT / "readme" / "README_zh_Hans.md", table(chosen, "zh"))
    print(f"{len(chosen)} endpoint tools from catalog {data['revision']}, price book {data['prices']['version']}")


if __name__ == "__main__":
    main()
