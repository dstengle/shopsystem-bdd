"""work-queue r59: `work show <request>` lists every line of the request, a line with no line outcome yet as unsettled."""
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import workqueue_list

REQUEST = ("---\nid: request/o/p/c/q1\nkind: request\nasker: bounded-context/o/p/c\nstatus: accepted\nturn: upstream\n---\n\n"
           "# q1\n\n## Lines\n1. The first line.\n2. The second line.\n\n## Questions\n\n## Answers\n\n"
           "## Outcomes\n1. accepted\n\n## Resolution\n")


def test_a_line_with_no_line_outcome_is_listed_as_unsettled(tmp_path, capsys):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text("---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n")
    (tmp_path / ".shop/work/requests").mkdir(parents=True)
    (tmp_path / ".shop/work/requests/q1.md").write_text(REQUEST)
    assert workqueue_list.show(tmp_path, "q1", False) == 0
    shown = capsys.readouterr().out.splitlines()
    assert "  line 1: accepted - The first line." in shown, shown
    assert "  line 2: unsettled - The second line." in shown, shown
