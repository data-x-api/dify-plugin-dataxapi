"""The YAML declarations, the Python sources and the routing tables agree."""

import re
from pathlib import Path

import pytest
import yaml
from dify_plugin import Tool, ToolProvider
from dify_plugin.core.utils.class_loader import load_single_subclass_from_source


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
def test_descriptions_say_login_and_billing(path):
    human = TOOLS[path]["description"]["human"]
    if path.endswith(("find_endpoint.yaml", "call_endpoint.yaml")):
        return
    assert "No sign-in to your own platform account" in human["en_US"] and "errors are not charged" in human["en_US"]
    assert "不用登录你自己的平台账号" in human["zh_Hans"] and "出错不收费" in human["zh_Hans"]


@pytest.mark.parametrize("path", [p for p in TOOLS if not p.endswith(("find_endpoint.yaml", "call_endpoint.yaml"))])
def test_endpoint_tool_class_matches_its_declaration(path):
    decl = TOOLS[path]
    source = ROOT / decl["extra"]["python"]["source"]
    cls = load_single_subclass_from_source(module_name=f"tools.{source.stem}", script_path=str(source), parent_type=Tool)
    assert cls.endpoint.replace(".", "_") == decl["identity"]["name"] == source.stem
    names = {p["name"] for p in decl["parameters"]}
    assert cls.list_params <= names and cls.integer_params <= names


def test_tool_names_are_unique_and_every_label_is_bilingual():
    names = [d["identity"]["name"] for d in TOOLS.values()]
    assert len(names) == len(set(names))
    for d in TOOLS.values():
        for p in d.get("parameters", []):
            assert p["label"]["en_US"] and p["label"]["zh_Hans"]
            for o in p.get("options", []):
                assert o["label"]["zh_Hans"]


FORBIDDEN = re.compile(r"tikhub|scrapecreators|rnote\.dev|twitterapi\.io|justoneapi|just one api|极致了|上游|供应商|转售|退款|refund", re.I)


def test_public_text_keeps_to_the_wording_rules():
    files = [ROOT / "README.md", ROOT / "readme" / "README_zh_Hans.md", ROOT / "PRIVACY.md", ROOT / "manifest.yaml", ROOT / "provider" / "dataxapi.yaml"]
    files += [ROOT / p for p in TOOLS]
    for f in files:
        assert not FORBIDDEN.search(f.read_text()), f


def test_readme_tables_list_every_tool():
    zh = (ROOT / "readme" / "README_zh_Hans.md").read_text()
    for d in TOOLS.values():
        assert d["identity"]["label"]["zh_Hans"] in zh, d["identity"]["name"]


def test_credential_link_carries_source():
    assert PROVIDER["credentials_for_provider"]["api_key"]["url"] == "https://dataxapi.com/console/keys/?ref=dify"
