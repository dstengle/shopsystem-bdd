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


def test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids(tmp_path):
    written = write(tmp_path, [{"capability": "thing", "adds": ["thing#r3"]},
                               {"capability": "thing", "adds": ["thing#r4"], "removes": ["thing#r1"]},
                               {"capability": "other", "changes": ["other#r2"]}])
    assert len(written) == 2
    assert "adds: [thing#r3, thing#r4]\n" in written[0]
    assert "removes: [thing#r1]\n" in written[0]
    assert "argues: [other]" in written[1]
