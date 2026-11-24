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
    found = json.loads(script("spec", "--root", str(ROOT), "check", "--json").stdout)["content"]
    rows = [row for row in found["violations"] + found["warnings"] if row[0] in ("w_untiered", "v_d6", "v_d7", "v_d8")]
    assert rows == [], rows
    named = [p for p in found["problems"] + found["unresolved"] if "spec/decisions/" in p]
    assert named == [], named


def test_the_sort_holds_its_totals():
    found = model_decisions.decisions(ROOT)
    assert len(found) == 126, len(found)       # the domain contract's twelve (0098-0109), three superseding; 0110-0114; 0115-0127
    assert collections.Counter(d.status for d in found) == {"accepted": 65, "superseded": 59, "rejected": 2}
    tiers = collections.Counter(d.tier for d in found if d.status == "accepted")
    assert tiers == {"check": 11, "requirement": 13, "judgement": 41}, tiers     # 0110-0112 judgements (b418, b420, b430); 0115-0125 (the contracts design); 0126, 0127
    # 0113 (check) superseded a check decision and was itself superseded by 0114 (check), so the check tier holds 11
    # `work decision --supersedes` (b179) sets only the status of the decision it replaces, so a decision out of force
    # keeps its tier only when it was superseded so; `model decisions --check` runs none of them.
    kept = [d.rel for d in found if d.status != "accepted" and d.tier]
    assert kept and all(d.status == "superseded" for d in found if d.rel in kept), kept


def test_the_judgement_decisions_reach_the_brief():
    found = [rel for rel, _ in batch_brief.judgement(ROOT)]
    assert "spec/decisions/0074-the-workflow-simplified.md" in found, found
    assert "spec/decisions/0079-a-knob-is-changed-by-a-decision.md" in found, found
    assert "spec/decisions/0080-the-old-workflow-retired.md" in found, found
    assert "spec/decisions/0065-workflow-capabilities-are-guarantees.md" not in found, found
    assert "spec/decisions/0036-one-requirement-form.md" in found, found
    assert "spec/decisions/0081-the-2-0-layout.md" in found, found
    assert "spec/decisions/0084-requests-only-propose.md" in found, found
    assert "spec/decisions/0085-requirements-retired-never-edited.md" in found, found
    assert "spec/decisions/0089-u5-is-a-judgement.md" in found, found
    assert "spec/decisions/0090-u7-is-a-judgement.md" in found, found
    assert "spec/decisions/0092-versions-are-0-y-z-until-1-0.md" in found, found
    assert "spec/decisions/0097-while-alpha-a-change-breaks-consumers-cleanly-with-no-compatibility-path.md" in found, found
    assert "spec/decisions/0107-the-specification-has-four-parts.md" in found, found
    assert "spec/decisions/0111-a-request-acts-on-one-thing.md" in found, found
    assert len(found) == 41, found     # 0110, 0111 and 0112 (b418, b420, b430); 0115-0125 (the contracts design); 0126, 0127


def test_0060_is_superseded_by_measure_a_batch():
    """Plan 7, D15."""
    by = {d.rel: d for d in model_decisions.decisions(ROOT)}
    old = by["spec/decisions/0060-measure-an-initiative.md"]
    assert old.status == "superseded" and not old.tier
    new = by["spec/decisions/0078-measure-a-batch.md"]
    assert new.status == "accepted" and new.tier == "requirement"
    assert list(new.requirements) == ["telemetry#r5", "telemetry#r6", "telemetry#r7", "telemetry#r8"]
    head = (ROOT / "spec/capabilities/telemetry.md").read_text().split("\n---", 1)[0]
    assert "design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-a-batch" in head


def test_the_review_runs_the_check_decisions():
    """Plan 6, D14: every pull request brief gives `model decisions --check`'s exit at the head and at the base."""
    assert "python3 {scripts}/model decisions --check" in batch_brief.CHECKS
