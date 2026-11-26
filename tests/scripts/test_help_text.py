"""The plugin's help texts and the docs' pack list say nothing a new user cannot read (b816): every parser's help of
shop and of the tools it runs holds no item id nor decision number, and docs/index.md's `grammar/packs/` line names
every pack the plugin keeps."""
import importlib.machinery
import importlib.util
import re

from docs_testing import DOCS, REPO, TOOLS, parser, subcommands

INTERNAL = re.compile(r"\bb\d{2,}\b|\bdecisions? \d{4}\b")


def _shop():
    loader = importlib.machinery.SourceFileLoader("help_text_shop", str(REPO / "scripts" / "shop"))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    return module.parser()


def _helps(p, words):
    yield " ".join(words), p.format_help()
    for name, child in subcommands(p).items():
        yield from _helps(child, words + [name])


def _internal(p, words):
    return [(path, found) for path, text in _helps(p, words) for found in INTERNAL.findall(text)]


def test_shop_help_names_no_internal_id():
    assert _internal(_shop(), ["shop"]) == []


def test_every_tool_help_names_no_internal_id():
    found = [hit for tool in TOOLS for hit in _internal(parser(tool), ["shop", tool])]
    assert found == []


def test_internal_ids_are_caught():
    assert INTERNAL.findall("the notice (b631), by decision 0132") == ["b631", "decision 0132"]


def test_docs_pack_list_names_every_pack():
    line = next(line for line in (DOCS / "index.md").read_text().splitlines() if "grammar/packs/" in line)
    packs = sorted(path.stem for path in (REPO / "grammar" / "packs").glob("*.md"))
    assert packs and [pack for pack in packs if "`%s`" % pack not in line] == []
