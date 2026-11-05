"""`work list` and `work show <request>` (requests r25, r26; workflow simplification plan 9, D6, D9): every line of a
request, a line with no line outcome yet as unsettled; the requests and the uncited observations, and no initiative or
work-item of the frozen queue; an observation a frozen initiative cites is not uncited."""
import json
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import request_view

REQUEST = ("---\nid: request/o/p/c/q1\nkind: request\nasker: bounded-context/o/p/c\nstatus: accepted\nturn: upstream\n---\n\n"
           "# q1\n\n## Lines\n1. The first line.\n2. The second line.\n\n## Questions\n\n## Answers\n\n"
           "## Outcomes\n1. accepted\n\n## Resolution\n")


def test_a_line_with_no_line_outcome_is_listed_as_unsettled(tmp_path, capsys):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text("---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n")
    (tmp_path / ".shop/work/requests").mkdir(parents=True)
    (tmp_path / ".shop/work/requests/q1.md").write_text(REQUEST)
    assert request_view.show(tmp_path, "q1", False) == 0
    shown = capsys.readouterr().out.splitlines()
    assert "  line 1: accepted - The first line." in shown, shown
    assert "  line 2: unsettled - The second line." in shown, shown


OBSERVATIONS = ("# Observations\n\n## observation/o/p/c/o1\nabout: bounded-context/o/p/c\nby: someone\ndate: 2026-10-15\n\n"
                "Seen.\n\n## observation/o/p/c/o2\nabout: bounded-context/o/p/c\nby: someone\ndate: 2026-10-16\n\nSeen.\n")


def frozen(tmp_path):
    for rel, text in {"spec/index.md": "---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n",
                      ".shop/work/requests/q1.md": REQUEST,
                      ".shop/work/i1/initiative.md": "---\nkind: initiative\nstatus: started\n"
                                                     "source: [observation/o/p/c/o1]\n---\n",
                      ".shop/work/i1/w1.md": "---\nkind: work-item\nstatus: drafted\n---\n",
                      ".shop/records/observations.md": OBSERVATIONS}.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    return tmp_path


def test_work_list_gives_requests_and_uncited_observations_only(tmp_path, capsys):
    assert request_view.listing(frozen(tmp_path), False) == 0
    shown = capsys.readouterr().out
    assert "request q1 accepted" in shown, shown
    assert "i1" not in shown and "w1" not in shown, shown


def test_an_observation_a_frozen_initiative_cites_is_not_uncited(tmp_path, capsys):
    assert request_view.listing(frozen(tmp_path), True) == 0
    found = json.loads(capsys.readouterr().out)
    assert [o["observation"] for o in found["observations"]] == ["observation/o/p/c/o2"], found
    assert sorted(found) == ["observations", "requests"], found
