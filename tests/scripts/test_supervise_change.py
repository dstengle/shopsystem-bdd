"""supervise_change: the proposals an integrate round's change list is written as (capability supervision r92)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from supervise_change import Changes, entries  # noqa: E402


def write(tmp_path, changes):
    initiative = tmp_path / "i1"
    initiative.mkdir()
    (initiative / "initiative.md").write_text("---\nid: initiative/a.io/b/c/i1\nkind: initiative\n---\n")
    holder = Changes()
    holder.dir = initiative
    return [p.read_text() for p in holder.write_proposals(entries({"changes": changes}), "drafts/")]


def proposal(path, name, capability, adds, removes):
    path.joinpath(name + ".md").write_text(
        "---\nid: capability-proposal/a.io/b/c/%s\nkind: capability-proposal\nstatus: applied\nargues: [%s]\n"
        "adds: [%s]\nchanges: []\nremoves: [%s]\n---\n\n# %s\n\nThe drafts of this proposal are in old/.\n" % (
            name, capability, ", ".join(adds), ", ".join(removes), name))


def test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal(tmp_path):
    initiative = tmp_path / "i1"
    initiative.mkdir()
    (initiative / "initiative.md").write_text("---\nid: initiative/a.io/b/c/i1\nkind: initiative\n---\n")
    proposal(initiative, "p1", "thing", ["thing#r1"], [])
    proposal(initiative, "p2", "other", ["other#r1"], ["other#r9"])
    holder = Changes()
    holder.dir = initiative
    found = entries({"changes": [{"capability": "thing", "adds": ["thing#r5"]},
                                 {"capability": "other", "adds": ["other#r1", "other#r2"], "removes": ["other#r8"]}]})
    holder.write_proposals(found, "drafts/", "p1")
    assert "adds: [thing#r5]\n" in (initiative / "p1.md").read_text()
    other = (initiative / "p2.md").read_text()
    assert "adds: [other#r1, other#r2]\n" in other
    assert "removes: [other#r9, other#r8]\n" in other
    assert "status: applied" in other


def test_a_round_started_for_one_proposal_leaves_another_held_proposals_drafts_path_as_it_was(tmp_path):
    initiative = tmp_path / "i1"
    initiative.mkdir()
    (initiative / "initiative.md").write_text("---\nid: initiative/a.io/b/c/i1\nkind: initiative\n---\n")
    proposal(initiative, "p1", "thing", ["thing#r1"], [])
    proposal(initiative, "p2", "other", ["other#r1"], [])
    holder = Changes()
    holder.dir = initiative
    holder.write_proposals(entries({"changes": [{"capability": "other", "adds": ["other#r2"]}]}), "drafts/", "p1")
    assert "The drafts of this proposal are in old/." in (initiative / "p2.md").read_text()


def test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids(tmp_path):
    written = write(tmp_path, [{"capability": "thing", "adds": ["thing#r3"]},
                               {"capability": "thing", "adds": ["thing#r4"], "removes": ["thing#r1"]},
                               {"capability": "other", "changes": ["other#r2"]}])
    assert len(written) == 2
    assert "adds: [thing#r3, thing#r4]\n" in written[0]
    assert "removes: [thing#r1]\n" in written[0]
    assert "argues: [other]" in written[1]
