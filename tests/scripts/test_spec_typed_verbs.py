"""spec_typed_verbs and spec_frames (b84, design call 5): a verb's subject, object and recipient typed by its frame's
kinds, a noun of a kind under the frame's kind filling the role, the refusal naming the verb, and the normal form the
other tools read. Parsed in the typed glossary fixture (`tests/scripts/fixtures/glossary`) and, for a recipient, in
the live glossary."""
import pathlib
import shutil
import sys

import pytest
import spec_frames
import spec_grammar
import spec_lexicon
import spec_typed_verbs

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "glossary"
RUN = "When the person runs `work start`, "


@pytest.fixture(scope="module")
def root():
    toolchain.require()
    return FIXTURE


def refusal(root, line):
    parsed = spec_grammar.parse(root, line)
    assert parsed.tree is None, parsed.tree
    return parsed.refusal


def test_a_noun_of_a_kind_under_the_frames_kind_fills_its_role(root):
    lex = spec_lexicon.read(root)
    assert "file" in spec_frames.below(lex)["text"] and "`work`" in spec_frames.below(lex)["agent"]
    tree = spec_grammar.parse(root, RUN + "`work` shall write a file and commit the file.").tree
    assert tree and spec_grammar.linearise(root, tree) == RUN + "`work` shall write a file and commit the file."


def test_a_role_of_the_wrong_kind_is_refused_naming_the_verb(root):
    assert refusal(root, RUN + "`work` shall write a stage.") == (
        "refused: the verb write takes as its object text or a kind of it: agent writes text")
    assert refusal(root, "When a request writes a file, `work` shall exit successfully.") == (
        "refused: the verb write takes as its subject agent or a kind of it: agent writes text")


def test_a_shalls_subject_is_checked_against_its_verbs(root):
    assert refusal(root, RUN + "a request shall write a file.") == (
        "refused: the verb write takes as its subject agent or a kind of it: agent writes text")


def test_a_recipient_of_the_wrong_kind_is_refused_naming_the_verb():
    toolchain.require()
    assert refusal(REPO, RUN + "`pr-reviewer` shall give a grade to a stage.") == (
        "refused: the verb give takes as its recipient text or a kind of it: agent gives thing to text")


def test_a_noun_phrase_with_no_kind_fills_any_object(root):
    for obj in ("`spec/index.md`", '"wall time"', "the status of the initiative", "only a file"):
        line = RUN + "`work` shall write %s." % obj
        tree = spec_grammar.parse(root, line).tree
        assert tree and spec_grammar.linearise(root, tree) == line, obj


def test_a_tree_is_read_in_its_normal_form_and_written_back_typed(root):
    lex = spec_lexicon.read(root)
    line = "When a session ends a stage, `work run` shall give only a brief to the stage."
    tree = spec_grammar.parse(root, line).tree
    trig, vp = tree[1], tree[2][1][2][1]
    assert trig[0] == "Happens" and trig[2] == ("e_end",) and trig[1][0] == "NPSubj"
    assert vp[0] == "DoTo" and vp[2] == ("Only", ("k_brief_toNP", ("k_brief_An", ("k_brief",))))
    typed = spec_typed_verbs.typed(tree, spec_typed_verbs.frames(lex))
    assert typed[1][0] == "e_end__Happens" and typed[1][1][0] == "k_agent_Sb__k_session"
    assert spec_typed_verbs.normal(typed) == tree


def test_no_generic_verb_fun_is_left_in_the_grammar():
    gf = "".join((spec_grammar.GRAMMARS / name).read_text() for name in ("Core.gf", "Req.gf"))
    for fun in ("Happens :", "HappensI :", "Do :", "DoI :", "DoTo :", "SDoes :", "SDoesTo :", "Event ;"):
        assert fun not in gf, fun


def test_a_verbs_later_sense_is_typed_by_its_own_frame(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text().replace("- **name** (verb, action)", "- **name** (verb, state): a text names "
                                               "a thing. Frame: text names thing.\n- **name** (verb, action)", 1))
    for line in ("When a session names a stage, `work` shall name a file.",
                 "When a file names a stage, `work` shall exit successfully."):
        tree = spec_grammar.parse(tmp_path, line).tree
        assert tree and spec_grammar.linearise(tmp_path, tree) == line, line
    assert refusal(tmp_path, "When a requirement group names a file, `work` shall exit successfully.")


def test_a_recipient_behind_another_preposition_is_typed(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    index = tmp_path / "spec" / "index.md"
    index.write_text(index.read_text() + "- **record** (verb, action): Frame: agent records thing in text.\n")
    line = RUN + "`work` shall record a stage in a file."
    tree = spec_grammar.parse(tmp_path, line).tree
    assert tree and spec_grammar.linearise(tmp_path, tree) == line
    assert refusal(tmp_path, RUN + "`work` shall record a stage to a file.")
