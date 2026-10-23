"""batch-measurement r57: a run whose session.json is empty is named as such, and no other run of its stage is."""
import json
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import measure_build

FIGURES = {"session_id": "s-3", "num_turns": 14, "total_cost_usd": 0.42,
           "usage": {"input_tokens": 10, "output_tokens": 20}}


def event(kind, at, session, stage="research"):
    return {"time": at, "event": kind, "work-item": "cart-1", "stage": stage, "agent": "a", "session": session}


def build(tmp_path, monkeypatch, directories):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "store"))
    work = tmp_path / ".shop/work/i1"
    rows = [event("start", "2026-10-22T10:00:00Z", "s-1"), event("end", "2026-10-22T10:10:00Z", "s-1"),
            event("start", "2026-10-22T11:00:00Z", "s-3"), event("end", "2026-10-22T11:10:00Z", "s-3")]
    work.mkdir(parents=True)
    (work / "log.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    for name, text in directories.items():
        (work / "runs/cart-1" / name).mkdir(parents=True)
        (work / "runs/cart-1" / name / "session.json").write_text(text)
    return measure_build.figures_of("i1", tmp_path)


def test_only_the_run_with_the_empty_session_json_is_named_empty(tmp_path, monkeypatch):
    figures = build(tmp_path, monkeypatch, {"1-research": "", "2-research": json.dumps(FIGURES)})
    first, second = figures["stages"]
    assert first.get("session_json") == "empty" and "turns" not in first
    assert "session_json" not in second and second["turns"] == 14 and second["cost"] == 0.42
    assert figures["totals"]["sessions"] == 1


def test_the_later_run_with_the_empty_session_json_is_the_one_named(tmp_path, monkeypatch):
    other = dict(FIGURES, session_id="s-1")
    figures = build(tmp_path, monkeypatch, {"2-research": "", "10-research": json.dumps(other)})
    first, second = figures["stages"]
    assert first.get("session_json") == "empty" and "session_json" not in second
