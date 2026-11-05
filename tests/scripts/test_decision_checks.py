"""The tests the `check` decisions of spec/decisions/ name, and the guard of the sort (workflow simplification plan 6,
D10, D17): the 300-line limit (0076), the features what `features generate` writes (0006), the live decisions kept
to their tiers by `model check`, the sort's totals, and the judgement decisions the pull request brief lists."""

import collections
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "scripts"))
import batch_brief
import model_decisions
import toolchain

SCRIPTS = ROOT / "scripts"


def script(name, *args):
    return subprocess.run([sys.executable, "-B", str(SCRIPTS / name), *args], cwd=ROOT, capture_output=True, text=True)


def test_every_tracked_python_file_is_300_lines_or_fewer():
    r = script("tools", "size", "--limit", "300")
    assert (r.returncode, r.stdout) == (0, ""), r.stdout + r.stderr


def test_the_features_are_what_features_generate_writes():
    toolchain.require()
    r = script("features", "generate", "--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_the_live_decisions_keep_their_tiers():
    toolchain.require()
    found = json.loads(script("model", "--root", str(ROOT), "check", "--json").stdout)
    rows = [row for row in found["violations"] + found["warnings"] if row[0] in ("w_untiered", "v_d6", "v_d7", "v_d8")]
    assert rows == [], rows
    named = [p for p in found["problems"] + found["unresolved"] if "spec/decisions/" in p]
    assert named == [], named


def test_the_sort_holds_its_totals():
    found = model_decisions.decisions(ROOT)
    assert len(found) == 75, len(found)
    assert collections.Counter(d.status for d in found) == {"accepted": 27, "superseded": 46, "rejected": 2}
    tiers = collections.Counter(d.tier for d in found if d.status == "accepted")
    assert tiers == {"check": 4, "requirement": 15, "judgement": 8}, tiers
    assert [d.rel for d in found if d.status != "accepted" and d.tier] == []


def test_the_judgement_decisions_reach_the_brief():
    found = [rel for rel, _ in batch_brief.judgement(ROOT)]
    assert "spec/decisions/0074-the-workflow-simplified.md" in found, found
    assert len(found) == 8, found
