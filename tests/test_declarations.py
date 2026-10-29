"""The YAML declarations, the Python sources and the routing tables agree."""

from pathlib import Path

import pytest
import yaml
from dify_plugin import Tool, ToolProvider
from dify_plugin.core.utils.class_loader import load_single_subclass_from_source

from tools import routes

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = yaml.safe_load((ROOT / "manifest.yaml").read_text())
PROVIDER = yaml.safe_load((ROOT / "provider/dataxapi.yaml").read_text())
TOOLS = {p: yaml.safe_load((ROOT / p).read_text()) for p in PROVIDER["tools"]}


def test_manifest_has_marketplace_fields():
    for key in ("author", "name", "version", "type", "icon", "privacy", "repo", "contact", "created_at"):
        assert MANIFEST.get(key), key
    assert "dify" not in MANIFEST["author"] and "langgenius" not in MANIFEST["author"]
    assert MANIFEST["contact"] == "support@dataxapi.com"
    assert (ROOT / "_assets" / MANIFEST["icon"]).is_file()
    assert (ROOT / MANIFEST["privacy"]).is_file()
    assert MANIFEST["meta"]["runner"]["version"] == "3.12"
    for path in MANIFEST["plugins"]["tools"]:
        assert (ROOT / path).is_file()


def test_provider_source_loads():
    cls = load_single_subclass_from_source(
        module_name="provider.dataxapi", script_path=str(ROOT / PROVIDER["extra"]["python"]["source"]), parent_type=ToolProvider
    )
    assert cls.__name__ == "DataXAPIProvider"


@pytest.mark.parametrize("path", list(TOOLS))
def test_each_tool_source_has_exactly_one_tool_class(path):
    decl = TOOLS[path]
    source = ROOT / decl["extra"]["python"]["source"]
    cls = load_single_subclass_from_source(
        module_name=f"tools.{source.stem}", script_path=str(source), parent_type=Tool
    )
    assert cls.__module__.startswith("tools.")


@pytest.mark.parametrize("path", list(TOOLS))
def test_descriptions_open_with_login_and_billing(path):
    human = TOOLS[path]["description"]["human"]
    first_en = human["en_US"].split(". ")[0]
    assert "No sign-in to your own platform account" in first_en
    assert "charged per call" in first_en and "errors are not charged" in first_en
    first_zh = human["zh_Hans"].split("。")[0]
    assert "不用登录你自己的平台账号" in first_zh and "按次计费" in first_zh and "出错不收费" in first_zh


def _options(tool, name):
    for p in TOOLS[tool]["parameters"]:
        if p["name"] == name:
            return [o["value"] for o in p["options"]]
    raise KeyError(name)


def test_dropdowns_match_routing_tables():
    assert _options("tools/account_posts.yaml", "platform") == list(routes.ACCOUNT_POSTS)
    assert _options("tools/post_comments.yaml", "platform") == list(routes.COMMENTS)
    assert _options("tools/keyword_search.yaml", "platform") == list(routes.SEARCH)


def test_credential_link_carries_source():
    assert PROVIDER["credentials_for_provider"]["api_key"]["url"] == "https://dataxapi.com/console/keys/?ref=dify"
