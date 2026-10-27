"""`work list` (capability work-queue r35, r39, r7): its JSON carries a request's status only, and a record it cannot read is refused."""
import json
import subprocess
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[2] / "scripts" / "work"


def repo(tmp_path, record=None):
    base = tmp_path / ".shop" / "work"
    (base / "i1").mkdir(parents=True)
    (base / "i1" / "initiative.md").write_text("---\nid: initiative/a/b/c/i1\nkind: initiative\nstatus: started\n---\n")
    (base / "requests").mkdir()
    (base / "requests" / "q1.md").write_text("---\nid: request/a/b/c/q1\nkind: request\nstatus: accepted\nturn: asker\n---\n")
    if record is not None:
        (base / "i1" / "raised.jsonl").write_text(record)
    return subprocess.run([sys.executable, str(WORK), "--root", str(tmp_path), "list"] + (["--json"] if record is None else []),
                          capture_output=True, text=True)


def test_list_json_gives_each_request_and_its_status_and_nothing_besides(tmp_path):
    done = repo(tmp_path)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["requests"] == [{"request": "q1", "status": "accepted"}]


def test_a_raised_record_line_that_cannot_be_read_is_refused_naming_the_file_and_line(tmp_path):
    for n, record in enumerate(["not json\n", '{"upstream": "u", "request": "q9"}\n']):
        done = repo(tmp_path / str(n), record)
        assert done.returncode != 0
        assert "Traceback" not in done.stderr
        assert "raised.jsonl" in done.stderr and "line 1" in done.stderr
