"""supervision r131, r132: a researcher's file set is its output; an empty one says no file is to change and is given,
while a result with no file set at all gives none. The GF conversion's design §13: an integrate round's output is
codified drafts, which `work run` parses and checks (`uncodified`); a formulate round has no session and no
formulation question."""
import pathlib
import shutil
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import supervise_outputs
import toolchain

FIXTURE = pathlib.Path(__file__).resolve().parent / "fixtures" / "generate" / "repo"
ABANDON = ("- [r5] When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status "
           "to `abandoned`.\n")
FROBNICATE = ("- [r5] When the person runs `work start` on an initiative that is `proposed`, `work` shall frobnicate "
              "the initiative.\n")
DONE = ("- [r5] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to "
        "`done`.\n")
TERM = "- **frobnicate** (event): Forms: frobnicates, frobnicated.\n"


def test_an_empty_researcher_file_set_is_given():
    assert supervise_outputs.missing("researcher", {"fileset": []}) is None


def test_a_researcher_result_with_no_file_set_misses_it():
    assert supervise_outputs.missing("researcher", {"summary": "done"}) == "the researcher's file set"


def test_a_planner_file_set_must_name_a_file():
    assert supervise_outputs.missing("planner", {"plan": "p", "fileset": []}) == "the planner's file set"


def test_a_formulate_round_sends_nothing_back_and_has_no_nothing_formulated():
    assert not hasattr(supervise_outputs, "formulated_nothing")
    assert supervise_outputs.sent_back("formulate", {"nothing_formulated": "the answers change lines not in spec/"}) is False


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    root = tmp_path / "repo"
    shutil.copytree(FIXTURE, root)
    return root


def behaviour(*groups):
    """A drafted `## Behaviour` section of work-queue.md: its three groups and the ones given."""
    live = (FIXTURE / "spec" / "capabilities" / "work-queue.md").read_text()
    section = live.split("## Behaviour\n", 1)[1].split("## Not yet", 1)[0].rstrip("\n") + "\n"
    return "## Behaviour\n" + section + "".join("\n### [g%d] %s\n%s" % (4 + n, "a drafted group", g)
                                                for n, g in enumerate(groups))


def draft(stage, rnd, text, rel="spec/capabilities/work-queue.md"):
    path = stage / "drafts" / ("round-%d" % rnd) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return stage / "drafts"


def test_drafted_requirements_that_parse_and_check_give_no_refusal(repo, tmp_path):
    drafts = draft(tmp_path / "stage", 1, behaviour(ABANDON))
    assert supervise_outputs.uncodified(repo, drafts) == []


def test_a_drafted_requirement_that_does_not_parse_is_refused_naming_it_the_token_and_the_nearest_words(repo, tmp_path):
    drafts = draft(tmp_path / "stage", 1, behaviour(FROBNICATE))
    refused = supervise_outputs.uncodified(repo, drafts)
    assert len(refused) == 1, refused
    assert refused[0].startswith("work-queue#r5: ") and "frobnicate" in refused[0] and "parsed up to:" in refused[0]


def test_a_word_the_drafts_terms_give_is_in_the_lexicon(repo, tmp_path):
    drafts = draft(tmp_path / "stage", 1, "## Terms\n" + TERM + "\n" + behaviour(FROBNICATE))
    assert supervise_outputs.uncodified(repo, drafts) == []


def test_a_word_a_drafted_glossary_gives_is_in_the_lexicon(repo, tmp_path):
    index = (repo / "spec" / "index.md").read_text()
    glossary = "## Glossary\n" + index.split("## Glossary\n", 1)[1] + "\n" + TERM
    stage = tmp_path / "stage"
    draft(stage, 1, glossary, rel="spec/index.md")
    drafts = draft(stage, 1, behaviour(FROBNICATE))
    assert supervise_outputs.uncodified(repo, drafts) == []


def test_a_drafted_status_change_no_transition_allows_is_refused_by_the_logic_check(repo, tmp_path):
    drafts = draft(tmp_path / "stage", 1, behaviour(DONE))
    refused = supervise_outputs.uncodified(repo, drafts)
    assert any(r.startswith("L3 work-queue#r5 ") for r in refused), refused
    assert all(r.startswith(("L1 ", "L3 ")) for r in refused), refused


def test_a_later_round_replaces_an_earlier_rounds_section(repo, tmp_path):
    stage = tmp_path / "stage"
    draft(stage, 1, behaviour(FROBNICATE))
    drafts = draft(stage, 2, behaviour(ABANDON))
    assert supervise_outputs.uncodified(repo, drafts) == []


def test_a_malformed_group_is_refused_naming_the_file(repo, tmp_path):
    drafts = draft(tmp_path / "stage", 1, behaviour("- [r9] `work` shall exit successfully.\n- r10 no id\n"))
    refused = supervise_outputs.uncodified(repo, drafts)
    assert refused and refused[0].startswith("work-queue.md: "), refused


def test_a_draft_of_an_uncodified_capability_is_not_checked(repo, tmp_path):
    drafts = draft(tmp_path / "stage", 1, "## Behaviour\n- [r2] **When** asked twice, frobnicate it.\n",
                   rel="spec/capabilities/legacy.md")
    assert supervise_outputs.uncodified(repo, drafts) == []


def test_no_drafts_give_no_refusal(tmp_path):
    assert supervise_outputs.uncodified(tmp_path, tmp_path / "none") == []


def test_a_frontmatter_draft_replaces_the_frontmatter_and_keeps_the_sections():
    live = "---\nid: a\nretired: []\n---\n\n# A\n\n## Purpose\nOld.\n\n## Behaviour\nB.\n"
    out = supervise_outputs.overlay(live, "---\nid: a\nretired: [r1]\n---\n\n## Purpose\nNew.\n")
    assert out.startswith("---\nid: a\nretired: [r1]\n---\n") and "New." in out and "Old." not in out and "B." in out


def test_a_section_the_live_file_lacks_is_added_after_its_last():
    out = supervise_outputs.overlay("---\nid: a\n---\n\n# A\n\n## Purpose\nP.\n", "## Terms\nT.\n")
    assert out.index("## Purpose") < out.index("## Terms")


def test_drafts_still_refused_are_asked_with_their_refusals_and_readings():
    asked = supervise_outputs.uncodified_question(["work-queue#r5: does not parse at frobnicate"], 2)
    assert asked.startswith(supervise_outputs.UNCODIFIED) and "after 2 send-backs" in asked
    assert "work-queue#r5: does not parse at frobnicate" in asked and "Readings:" in asked
    assert supervise_outputs.uncodified_question([], 2) is None


def test_the_question_goes_on_the_proposals_a_refusal_names_else_on_all(tmp_path):
    paths = []
    for name in ("work-queue", "review"):
        paths.append(tmp_path / ("%s.md" % name))
        paths[-1].write_text("---\nkind: capability-proposal\nstatus: drafted\n---\n")
    (tmp_path / "terms.md").write_text("---\nkind: glossary-proposal\n---\n")
    paths.append(tmp_path / "terms.md")
    assert supervise_outputs.refused_proposals(paths, ["L1 review#g2 (r4) cannot happen"]) == ["review"]
    assert supervise_outputs.refused_proposals(paths, ["work-queue.md: 12: a group heading is not"]) == ["work-queue"]
    assert supervise_outputs.refused_proposals(paths, ["index.md: something"]) == ["work-queue", "review"]
