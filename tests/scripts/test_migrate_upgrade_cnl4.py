"""The 0.33.0 upgrade step "the controlled language 4" (migration-tools g61): each file's marker, `imports: [cli]` and
each verb's aspect rewritten where that is mechanical, and what it cannot reword named by file and id; no line is
reworded."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import migrate_upgrade_cnl4 as step
import toolchain

# b161's given block, with what each report needs
INDEX = """---
id: bounded-context/example.org/acme/shop
title: shop
language: codified-1
---
# shop
## Glossary
- **the person** (proper noun): the human who shops. Kind of: agent.
- **`shop`** (proper noun): the shop's tool. Kind of: tool.
- **cart** (noun): the goods a shopper picks.
- **shopper** (noun): a person who buys.
- **till** (noun): where a shopper pays.
- **command** (noun): what a shopper types.
- **pick** (verb): a shopper puts goods in a cart. Forms: picks, picked. Frame: shopper picks cart.
- **own** (verb): a shopper has a cart. Forms: owns, owned. Frame: shopper owns cart.
- **watch** (verb): a shopper looks at a till. Forms: watches, watched. Frame: shopper watches till.
- **guard** (verb): a shopper keeps a cart. Forms: guards, guarded. Frame: shopper guards cart.
- **full** (adjective of cart): a cart that holds ten goods.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| till | for | shopper |  |
| cart | of | shopper | one |
"""
LINES = {
    "r1": "When a shopper picks a cart, the shopper shall watch a till.",
    "r2": 'If the person runs `shop pay`, then `shop` shall exit with an error naming `apples`.',
    "r3": "When a shopper picks a cart, the shopper shall watch the till.",
    "r4": "While a shopper does not own a cart, when the shopper picks a cart, the shopper shall watch a till.",
    "r5": "When a shopper picks a cart quickly, the shopper shall watch a till.",
    "r6": "While a cart is full, when a shopper picks the cart, the shopper shall watch a till.",
    "r7": "While a shopper guards a cart, when the shopper picks a cart, the shopper shall watch a till.",
    "r8": "When a shopper guards a cart, the shopper shall watch a till.",
}
BUY = ("---\nid: capability/example.org/acme/shop/buy\ntitle: buy\nlanguage: codified-1\nretired: []\nunbuilt: []\n"
       "---\n# buy\n## Terms\n## Behaviour\n### [g1] picking\n"
       + "".join("- [%s] %s\n" % kv for kv in LINES.items()))


def spec(tmp_path):
    (tmp_path / "spec/capabilities").mkdir(parents=True)
    (tmp_path / "spec/index.md").write_text(INDEX)
    (tmp_path / "spec/capabilities/buy.md").write_text(BUY)
    return tmp_path


def test_each_marker_is_codified_2_and_the_cli_pack_imported(tmp_path):
    toolchain.require()
    texts = step.plan(spec(tmp_path)).texts
    assert "language: codified-2\nimports: [cli]\n---\n" in texts["spec/index.md"]
    assert texts["spec/capabilities/buy.md"] == BUY.replace("codified-1", "codified-2")      # no line reworded
    assert (tmp_path / "spec/index.md").read_text() == INDEX                                # plan writes nothing


def test_a_verb_is_given_the_aspect_its_lines_use_it_in(tmp_path):
    toolchain.require()
    index = step.plan(spec(tmp_path)).texts["spec/index.md"]
    assert "**pick** (verb, action)" in index           # a trigger only
    assert "**own** (verb, state)" in index             # a While clause only
    assert "**watch** (verb, action)" in index          # a response
    assert "**guard** (verb):" in index                 # a trigger and a While clause: a session decides


def test_what_it_cannot_reword_is_named_by_file_and_id(tmp_path):
    toolchain.require()
    notes = step.plan(spec(tmp_path)).notes
    cap = "the controlled language 4: spec/capabilities/buy.md "

    def has(start):
        assert any(n.startswith(start) for n in notes), (start, notes)
    has("the controlled language 4: v_t14 guard, spec/index.md: a state in r7 and an action in r8")
    has(cap + 'r3 says "the" with no antecedent')
    has(cap + "r4 says a negated indefinite in a While clause")
    has(cap + "r5 no longer parses: does not parse at quickly")
    has("the controlled language 4: spec/index.md full is a condition (adjective) grammar 4 reads no definition "
        "of; say it with a structure in each line using it: spec/capabilities/buy.md r6")
    has(cap + "r2 holds example data: `apples`")
    has(cap + 'r2 says "exit with an error naming"')
    has("the controlled language 4: spec/index.md the row till | for | shopper has no cardinality")
    assert not any("cart | of | shopper" in n for n in notes), notes
    has("the controlled language 4: v_t16 command, spec/index.md: the pack cli defines it too")
    assert not any(cap + "r1 " in n for n in notes), notes


def test_a_spec_in_the_controlled_language_4_is_left_alone(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(INDEX.replace("codified-1", "codified-2"))
    changes = step.plan(tmp_path)
    assert changes.texts == {} and changes.notes == []


def test_an_index_with_no_marker_is_given_one(tmp_path):
    assert step.remarked("---\nid: x\n---\n# x\n", index=True) == "---\nid: x\nlanguage: codified-2\n---\n# x\n"
    assert step.remarked("---\nid: x\n---\n# x\n") == "---\nid: x\n---\n# x\n"
    assert step.imported("---\nimports: [time]\n---\n") == "---\nimports: [time, cli]\n---\n"
