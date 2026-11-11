"""The 0.32.0 upgrade step "verb frames" (migration-tools g25): each term's category written as its part of speech in
the glossary and a capability's `## Terms`, nothing else changed, and each verb with no frame, each relational
condition named by file; no line is reworded."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import migrate_upgrade_frames as step
import toolchain

INDEX = ("---\nid: bounded-context/example.org/acme/shop\ntitle: shop\nlanguage: codified-1\n---\n# shop\n## Glossary\n"
         "- **cart** (kind): the goods a shopper picks.\n- **shopper** (kind): a person who buys.\n"
         "- **full** (condition of cart): a cart that the shopper fills.\n"
         "- **pick** (event): a shopper puts goods in a cart. Forms: picks, picked.\n")
OTHER = "\n## Other\n- **x** (kind): y.\n"
SPOKEN = (INDEX.replace("(kind)", "(noun)").replace("(condition of cart)", "(adjective of cart)")
          .replace("(event)", "(verb)"))
LINE = "When a shopper picks a cart, the shopper shall be full."
BUY = ("---\nid: capability/example.org/acme/shop/buy\ntitle: buy\nlanguage: codified-1\nretired: []\nunbuilt: []\n"
       "---\n# buy\n## Terms\n- **till** (resource, exclusive): where a shopper pays.\n## Behaviour\n"
       "### [g1] picking\n- [r1] %s\n" % LINE)


def spec(tmp_path):
    (tmp_path / "spec/capabilities").mkdir(parents=True)
    (tmp_path / "spec/index.md").write_text(INDEX + OTHER)
    (tmp_path / "spec/capabilities/buy.md").write_text(BUY)
    return tmp_path


def test_each_category_is_written_as_its_part_of_speech_and_nothing_else(tmp_path):
    toolchain.require()
    changes = step.plan(spec(tmp_path))
    assert changes.texts["spec/index.md"] == SPOKEN + OTHER       # `x` is no glossary entry
    assert changes.texts["spec/capabilities/buy.md"] == BUY.replace("(resource, exclusive)", "(noun, exclusive)")
    assert (tmp_path / "spec/index.md").read_text() == INDEX + OTHER            # plan writes nothing


def test_each_frameless_verb_and_relational_condition_is_named(tmp_path):
    toolchain.require()
    notes = step.plan(spec(tmp_path)).notes
    assert any(n.startswith("verb frames: v_t11 pick, spec/index.md:") for n in notes), notes
    assert any(n.startswith("verb frames: v_t12 full, spec/index.md:") for n in notes), notes
    assert not any("no longer parses" in n for n in notes), notes       # the lines are the next step's to report
    assert LINE in step.plan(tmp_path).texts["spec/capabilities/buy.md"]   # no line reworded


def test_a_spec_in_its_parts_of_speech_is_left_alone(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(SPOKEN)
    assert step.plan(tmp_path).texts == {}
