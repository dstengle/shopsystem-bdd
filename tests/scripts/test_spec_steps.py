"""spec_steps.read: one group's facts read into Givens, a When and Thens by the fixed rules of design-r3 §5, no
solver. The ids are the generation fixture's (`tests/scripts/fixtures/generate/repo`), copied and grown per test."""
import pathlib
import shutil
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "generate" / "repo"


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    shutil.copytree(FIXTURE, tmp_path / "repo")
    return tmp_path / "repo"


def add_group(root, cap, text):
    """`text` added as the last group of the capability's Behaviour."""
    path = root / "spec" / "capabilities" / ("%s.md" % cap)
    body = path.read_text()
    at = body.index("\n## ", body.index("## Behaviour"))
    path.write_text(body[:at] + "\n" + text + "\n" + body[at:])


def add_term(root, line):
    path = root / "spec" / "index.md"
    path.write_text(path.read_text().rstrip("\n") + "\n" + line + "\n")


def steps(root, gid):
    """[(keyword, text)] of one group, as `features generate` words them."""
    import features_vocab
    import spec_context
    import spec_steps
    ctx = spec_context.load(root)
    assert not ctx.refused, ctx.refused
    v = features_vocab.load(root)
    facts = [ctx.facts[s.id] for s in ctx.statements if s.group == gid]
    return [(k, v.text(t)) for k, t in spec_steps.read(facts, ctx.vocab, v)]


def test_a_while_condition_is_a_given_that_introduces_its_role(repo):
    add_group(repo, "work-queue", "### [g9] a drafted work-item is listed\n"
              "- [r9] While a work-item is `drafted`, when the person runs `work list`, `work` shall print the "
              "work-item.")
    got = steps(repo, "work-queue#g9")
    assert got[0] == ("given", "a work-item w1 that is `drafted`")
    assert got[-1] == ("then", "`work` prints the work-item w1")


def test_a_negated_restriction_is_a_kind_given_and_an_is_not(repo):
    assert steps(repo, "work-queue#g2")[:2] == [("given", "an initiative i1"),
                                                ("given", "the initiative i1 is not `proposed`")]


def test_the_trigger_is_the_when(repo):
    got = steps(repo, "work-queue#g2")
    assert [s for s in got if s[0] == "when"] == [("when", "the person runs `work start` on the initiative i1")]
    assert got.index(("when", "the person runs `work start` on the initiative i1")) == 2


def test_each_response_is_a_then_with_its_restrictions_then_its_sets(repo):
    assert [s for s in steps(repo, "work-queue#g1") if s[0] == "then"] == [
        ("then", "the initiative i1 is `started`"), ("then", "`work` exits successfully")]
    add_group(repo, "supervision", "### [g9] a stage for a ready work-item\n"
              "- [r9] When the person runs `work run`, `work run` shall start a stage for a work-item that is "
              "`ready`.")
    assert steps(repo, "supervision#g9") == [
        ("when", "the person runs `work run`"), ("then", "`work run` starts the stage s1"),
        ("then", "the work-item w1 is `ready`"), ("then", "the stage s1 is for the work-item w1")]


def test_a_negative_response_states_no_restriction_of_its_object(repo):
    add_group(repo, "supervision", "### [g9] no stage for a ready work-item\n"
              "- [r9] When the person runs `work run`, `work run` shall not start a stage for a work-item that is "
              "`ready`.")
    assert steps(repo, "supervision#g9") == [("when", "the person runs `work run`"),
                                             ("then", "`work run` does not start the stage s1")]


def test_an_every_role_gets_one_contrast_failing_its_restriction(repo):
    got = steps(repo, "supervision#g1")
    assert ("given", "an initiative i2 that is `done`") in got
    assert ("then", "`work run` does not take the initiative i2") in got
    assert not any("i3" in t for _, t in got)


def test_no_failing_value_gives_no_contrast(repo):
    add_term(repo, "- **state** (attribute of session): Values: `idle`.")
    add_group(repo, "supervision", "### [g9] idle sessions end\n"
              "- [r9] When the person runs `work run`, `work run` shall end every session that is `idle`.")
    got = steps(repo, "supervision#g9")
    assert got == [("given", "a session s1 that is `idle`"), ("when", "the person runs `work run`"),
                   ("then", "`work run` ends the session s1")]


def test_no_k_is_v_gives_no_given(repo):
    add_group(repo, "supervision", "### [g9] a run with no started initiative\n"
              "- [r9] While no initiative is `started`, when the person runs `work run`, `work run` shall end "
              "a session.")
    got = steps(repo, "supervision#g9")
    assert not [s for s in got if s[0] == "given"]
    assert got[0] == ("when", "the person runs `work run`")


def test_a_scenario_does_not_change_when_an_unrelated_requirement_is_added(repo):
    before = steps(repo, "work-queue#g2")
    add_group(repo, "supervision", "### [g9] started initiatives\n"
              "- [r9] While an initiative is `started`, when the person runs `work start` on the initiative, "
              "`work` shall exit successfully.")
    assert steps(repo, "work-queue#g2") == before


def test_roles_are_named_by_kind_letter_in_order_of_first_mention(repo):
    add_group(repo, "supervision", "### [g9] a stage for a ready work-item\n"
              "- [r9] When the person runs `work start` on an initiative, `work run` shall start a stage for a "
              "work-item that is `ready`.")
    texts = " ".join(t for _, t in steps(repo, "supervision#g9"))
    assert texts.index("initiative i1") < texts.index("stage s1") < texts.index("work-item w1")
    assert steps(repo, "supervision#g3") == [("when", "`work run` starts the stage s1")]


def test_two_requirements_of_one_group_share_their_roles(repo):
    got = steps(repo, "work-queue#g1")
    assert not any("i2" in t for _, t in got)
    assert got == [("given", "an initiative i1 that is `proposed`"),
                   ("when", "the person runs `work start` on the initiative i1"),
                   ("then", "the initiative i1 is `started`"), ("then", "`work` exits successfully")]


def test_a_defined_condition_is_one_given_not_its_definition(repo):
    add_group(repo, "supervision", "### [g9] an open initiative\n"
              "- [r9] When the person runs `work run` on an initiative that is open, `work run` shall take the "
              "initiative.")
    got = steps(repo, "supervision#g9")
    assert [s for s in got if s[0] == "given"] == [("given", "an initiative i1"),
                                                   ("given", "the initiative i1 is open")]


def test_a_split_requirement_gives_its_first_way_through(repo):
    add_group(repo, "supervision", "### [g9] started or done\n"
              "- [r9] When the person runs `work run` on an initiative whose status is `started` or `done`, "
              "`work run` shall take the initiative.")
    got = steps(repo, "supervision#g9")
    assert got[0] == ("given", "an initiative i1 that is `started`")
    assert not any("`done`" in t for _, t in got)


def test_an_instance_name_is_lower_case_for_a_capitalised_kind(repo):
    add_term(repo, "- **Python interpreter** (kind): the Python a command runs with.")
    add_group(repo, "work-queue", "### [g9] the interpreter is listed\n"
              "- [r9] When the person runs `work list`, `work` shall print every Python interpreter.")
    assert steps(repo, "work-queue#g9")[-1] == ("then", "`work` prints the Python interpreter p1")


def test_a_quoted_figure_for_a_thing_is_a_then_naming_the_thing(repo):
    add_group(repo, "work-queue", "### [g9] a figure for a drafted work-item\n"
              "- [r9] While a work-item is `drafted`, when the person runs `work list`, `work` shall take "
              "\"turns\" for the work-item, and `work` shall not take \"took\" for the work-item.")
    assert [s for s in steps(repo, "work-queue#g9") if s[0] == "then"] == [
        ("then", "`work` takes \"turns\" for the work-item w1"),
        ("then", "`work` does not take \"took\" for the work-item w1")]


def test_a_verb_in_a_condition_is_a_given_of_the_verb_read_back_as_one_step(repo):
    import features_vocab
    add_group(repo, "work-queue", "### [g9] an initiative not taken\n"
              "- [r9] While `work run` does not take an initiative, when the person runs `work list`, `work` shall "
              "print the initiative.")
    got = steps(repo, "work-queue#g9")
    assert got[:2] == [("given", "an initiative i1"), ("given", "`work run` does not take the initiative i1")]
    call = features_vocab.step(features_vocab.load(repo), "given", got[1][1])
    assert (call.template, call.term, call.nps) == ("GivenDoesNot", "take", ["the initiative i1"])
    assert features_vocab.step(features_vocab.load(repo), "then", "`work run` takes the initiative i1").template == (
        "ThenDoes")
