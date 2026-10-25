"""Probes of work add (r32) and work withdraw (r31) through scripts/work, each in its own repository under the scratch dir."""
import json
import pathlib
import shutil
import subprocess

SCRATCH = pathlib.Path("/tmp/work-run-i33-9vstbbh_/w192-1-research/.shop/scratch/1-research")
WORK = "/tmp/work-run-i33-9vstbbh_/w192-1-research/scripts/work"
CTX = "missingmass.io/shopsystem/shopsystem-bdd"


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def make(name, initiative_status, items, log=None):
    root = SCRATCH / name
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "probe@example.com")
    git(root, "config", "user.name", "probe")
    (root / "spec").mkdir()
    (root / "spec/index.md").write_text("---\nid: bounded-context/%s\n---\n# ctx\n" % CTX)
    d = root / ".shop/work/i1"
    d.mkdir(parents=True)
    if initiative_status is not None:
        (d / "initiative.md").write_text("---\nid: initiative/%s/i1\nkind: initiative\nstatus: %s\n---\n"
                                         % (CTX, initiative_status))
    for item, status in items:
        (d / (item + ".md")).write_text("---\nid: work-item/%s/%s\nkind: work-item\npart_of: initiative/i1\n"
                                        "status: %s\nunder: thing\naccepts: [thing#r1]\n---\n\n# %s\n"
                                        % (CTX, item, status, item))
    if log is not None:
        (d / "log.jsonl").write_text("".join(json.dumps(line) + "\n" for line in log))
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "probe repository")
    return root


def work(root, *args):
    done = subprocess.run(["python3", WORK, "--root", str(root), *args], capture_output=True, text=True)
    return done.returncode, done.stdout.strip(), done.stderr.strip()


def status_of(root, item="initiative"):
    text = (root / f".shop/work/i1/{item}.md").read_text()
    return [l for l in text.splitlines() if l.startswith("status:")]


def items_of(root):
    return sorted(p.name for p in (root / ".shop/work/i1").glob("w*.md"))


def show(label, result):
    print("%s: rc=%s stdout=%r stderr=%r" % (label, *result))


ADD = ("add", "i1", "Show the queue", "--part-of", "capability-proposal/p1", "--under", "thing", "--accepts", "thing#r1")


def test_add_into_done_initiative():
    root = make("add_done", "done", [("w1", "green")])
    show("add into done (r32 says refused)", work(root, *ADD))
    print("  initiative status now:", status_of(root), " items:", items_of(root))


def test_add_into_abandoned_initiative():
    root = make("add_abandoned", "abandoned", [("w1", "withdrawn")])
    show("add into abandoned (r32 says refused)", work(root, *ADD))
    print("  items:", items_of(root))


def test_add_into_started_control():
    root = make("add_started", "started", [("w1", "green")])
    show("add into started (control)", work(root, *ADD))


def test_add_into_initiative_without_initiative_md():
    root = make("add_no_initiative_md", None, [("w1", "green")])
    show("add into initiative with no initiative.md", work(root, *ADD))


def test_withdraw_scenario_shape():
    log = [{"time": "2026-10-19T10:00:00+00:00", "work-item": "w2", "before": "researched", "after": "ready", "by": "someone"}]
    root = make("withdraw_scenario", "started", [("w1", "withdrawn"), ("w2", "ready")], log)
    show("withdraw w2 (scenario shape; r31 says initiative stays started)", work(root, "withdraw", "w2"))
    print("  initiative status now:", status_of(root), " w2:", status_of(root, "w2"))


def test_withdraw_sole_item():
    root = make("withdraw_sole", "started", [("w1", "ready")])
    show("withdraw the only work-item w1 (ready)", work(root, "withdraw", "w1"))
    print("  initiative status now:", status_of(root))


def test_withdraw_last_with_green_control():
    root = make("withdraw_with_green", "started", [("w1", "green"), ("w2", "ready")])
    show("withdraw w2 with w1 green (r23 says done)", work(root, "withdraw", "w2"))
    print("  initiative status now:", status_of(root))


def test_withdraw_last_drafted_no_green():
    root = make("withdraw_drafted", "started", [("w1", "withdrawn"), ("w2", "drafted")])
    show("withdraw w2 drafted, w1 withdrawn, no green", work(root, "withdraw", "w2"))
    print("  initiative status now:", status_of(root))
