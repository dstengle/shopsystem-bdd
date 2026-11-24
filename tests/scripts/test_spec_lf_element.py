"""Two terms of one element (b544, consistency r35): a proper noun of the actor the person in the notes layer, "the
owner", beside the shared layer's "the person", is one referent of a line's logical form (spec_lf_core's `constant`)
and one thing of the check's facts (spec_lf_ids' `actors`), so lines on either clash as lines on one thing."""
import pathlib
import re
import shutil

import pytest
import spec_context
import spec_grammar4
import spec_lf
import toolchain

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"
OWNER = "- **the owner** (proper noun) → actor the person. The one whose notes they are.\n"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


@pytest.fixture(scope="module")
def root(tmp_path_factory):
    out = tmp_path_factory.mktemp("element")
    for part in ("model", "vocabulary"):
        shutil.copytree(FIXTURE / "spec" / part, out / "spec" / part)
    shutil.copyfile(FIXTURE / "spec" / "index.md", out / "spec" / "index.md")
    vocabulary = out / "spec" / "vocabulary" / "notes.md"
    vocabulary.write_text(vocabulary.read_text() + OWNER)
    return out


def test_two_terms_of_one_actor_are_one_referent_of_a_line(root):
    vocab = spec_grammar4.load(root)[0]
    parsed = spec_grammar4.parse(root, "When the owner adds a note, the notes service shall notify the person of "
                                       "the note.")
    assert parsed.tree, parsed.refusal
    said = spec_lf.show(spec_lf.form(vocab, parsed.tree))
    assert "x1: agent the owner (constant)" in said and "the person" not in said
    assert "request(e1, notes.add, subject: x1, object: x2)" in said and "object: x1, of: x2" in said


def test_two_terms_of_one_actor_are_one_thing_of_the_facts(root):
    four = spec_context.Four(root)
    (_, owner), _ = four.facts("thing#r1", "When the owner adds a note, the notes service shall file the note.")
    (_, person), _ = four.facts("thing#r2", "When the person adds a note, the notes service shall file the note.")
    doer = re.compile(r"^trig\(.*,(a_\w+),x\d+\)\.$")
    said = [next(m.group(1) for m in map(doer.match, facts) if m) for facts in (owner, person)]
    assert said == ["a_notes__the_person"] * 2
