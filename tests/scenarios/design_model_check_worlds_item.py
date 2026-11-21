"""The worlds of a requirement previewed for an item (parsing r19, r20, r22, b452), rows design_model_check_worlds'
TABLE takes first: the smallest codified-2 world (codified2_world) whose r1 uses the noun `shelf`, which only the item
b1 holds (a term bullet of its block of `thing`), so that `spec parse --item b1` reads r1 and `spec parse` alone
refuses it; and `args`, the item the When names as `spec parse --item` takes it, its file written when no world wrote
one (an item that holds no line)."""
import importlib.util
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C2 = _sibling("codified2_world.py", "shop_codified2_world")
ITEM = ".shop/backlog/b1.md"
TERM = "- **shelf** (noun): a place a stage's files are kept until it is ended. Plural: shelves."
LINE = "When a session ends a stage, `work` shall print a shelf."


def item(repo, block=""):
    """The item b1, `ready`, with `block` as its requirements."""
    H.write(repo, ITEM, "---\nid: item/%s/b1\nkind: item\nstatus: ready\nprovenance: own\nvalue: high-value\n"
            "urgency: medium-urgency\nsize: small\ndepends_on: []\n---\n\n# Shelves\n\n## Notes\n\nShelves.\n\n"
            "## Requirements\n\n%s" % (H.PATH, block))


def shelved(step):
    """r1 says `a shelf`; only the item b1 holds the term."""
    C2.context(step.repo, H.PATH, [LINE])
    item(step.repo, "### thing\n\n%s\n" % TERM)


def args(step):
    """`--item b1`, the item the When names; written when the world has none."""
    if not (step.repo / ITEM).is_file():
        item(step.repo)
    H.says(step, "i1", "b1")
    return ["--item", "b1"]


ROWS = [
    (("item holds term", "requirement use term"), shelved, {}),
]
