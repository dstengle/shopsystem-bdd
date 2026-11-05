"""`measure batch <batch>` (capability telemetry; workflow simplification plan 7, D2-D10): a batch's window from the
git history of its plan, its sessions' requests inside the window from the transcripts on disk, each with its role
and session time, the cost by role, the pull request's review findings by grade, the defects traced to their items
and the knobs it ran with, as one dict of figures (D9). It reads no network and writes no prompt, reply, tool content
or description text. Standard library only."""
import datetime
import subprocess
from pathlib import Path

import backlog_items
import batch_brief
import batch_findings
import batch_git
import batch_pick
import batch_plan
import measure_batch_read
import measure_batch_sessions
import measure_build
import measure_cost
import measure_defect
import workqueue
from measure_read import Refused, moment


def now():
    return datetime.datetime.now(datetime.UTC)


def _git(root, *args):
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        raise Refused("git %s failed: %s" % (args[0], (done.stderr.strip() or "exit %d" % done.returncode)))
    return done.stdout


def window_of(root, batch):
    """D3: `started` (the plan's first commit), `first_review` (the first `-> in-review`), `built` (the last
    `-> awaiting-merge`) and `closed` (`-> merged` or `-> abandoned`, else the last commit of a closed batch), each an
    ISO time or None."""
    rows = [line.split("\t", 2) for line in _git(root, "log", "--reverse", "--format=%H%x09%cI%x09%s", "--",
                                                  batch_plan.rel_of(batch.name)).splitlines() if line.strip()]
    first = lambda word: next((at for _, at, s in rows if word in s), None)
    last = lambda word: next((at for _, at, s in reversed(rows) if word in s), None)
    closed = last("-> merged") or last("-> abandoned")
    if closed is None and batch.status in ("merged", "abandoned") and rows:
        closed = rows[-1][1]
    return {"started": rows[0][1] if rows else None, "first_review": first("-> in-review"),
            "built": last("-> awaiting-merge"), "closed": closed}


def findings_of(root, batch):
    """D7: the reviews, each with the lines its own range changed, each finding, and the findings by grade and by
    triage (every one, 0 included)."""
    reviews = batch_findings.reviews(root, batch.name)
    found = [{"finding": f.fid, "review": r.number, "grade": f.grade, "triage": f.triage, "item": f.item}
             for r in reviews for f in r.findings]
    return {"reviews": [{"review": r.number, "result": r.result, "findings": len(r.findings),
                         "lines": changed_lines(root, r.range)} for r in reviews],
            "findings": found,
            "findings_by_grade": {g: sum(f["grade"] == g for f in found) for g in batch_findings.GRADES},
            "findings_by_triage": {t: sum(f["triage"] == t for f in found) for t in batch_findings.TRIAGES}}


def changed_lines(root, rng):
    """The lines added and removed over `rng`, `.shop/` left out; a binary file counts 0."""
    out = _git(root, "diff", "--numstat", rng, "--", ".", ":(exclude).shop")
    return sum(int(a) + int(b) for a, b, _ in (line.split("\t", 2) for line in out.splitlines() if line.strip())
               if a.isdigit() and b.isdigit())


def knobs_of(root, batch, reviews):
    """D10: the knobs as the batch ran with them; nothing here sets one. The changed lines are the whole batch as last
    reviewed, its fork to the last review's head (plan 7 review S1, Q3)."""
    return {"batch_size": batch_pick.batch_size(root), "items": len(batch.tasks),
            "changed_lines": changed_lines(root, "%s..%s" % (batch.forked_from, reviews[-1].head)) if reviews else None,
            "size_limit": batch_git.delivery(root).get("review", {}).get("size", batch_brief.SIZE),
            "reviews": len(reviews), "readiness_bar": "mechanical"}


def _after_merge(root, name):
    counts = {}
    for defect in measure_defect.defects(root, name):
        counts[defect.item] = counts.get(defect.item, 0) + 1
    return counts


def _seconds(a, b):
    return round((b - a).total_seconds()) if a and b else None


def figures_of(root, name, sessions_dir=None):
    """D9's figures of the batch `name`; a batch file refused by `work` is refused here."""
    try:
        return _figures(root, name, sessions_dir)
    except workqueue.Refused as why:
        raise Refused(str(why)) from None


def _figures(root, name, sessions_dir):
    batch = batch_plan.find(root, name)
    items = [backlog_items.find(root, t.item) for t in batch.tasks]
    window = window_of(root, batch)
    at = {k: moment(v, batch_plan.rel_of(name)) if v else None for k, v in window.items()}
    stop = now()
    directory = Path(sessions_dir) if sessions_dir else measure_batch_read.project_dir(root)
    table = measure_cost.prices(root)
    span = (at["started"] or stop, at["built"] or at["closed"] or stop)
    sessions = measure_batch_sessions.sessions_of(measure_batch_read.requests_of(directory),
                                                  measure_batch_read.agent_types(directory), span,
                                                  at["first_review"], table, batch=name,
                                                  parents=measure_batch_read.parents(directory))
    unpriced = {}
    for one in sessions:
        for model, count in one.pop("unpriced").items():
            unpriced[model] = unpriced.get(model, 0) + count
    review = findings_of(root, batch)
    reviews = batch_findings.reviews(root, name)
    defects = {"review": {}, "after_merge": _after_merge(root, name)}
    for f in review["findings"]:
        if f["triage"] == "fix now" and f["item"]:
            defects["review"][f["item"]] = defects["review"].get(f["item"], 0) + 1
    total = sum(defects["review"].values()) + sum(defects["after_merge"].values())
    defects["per_item"] = round(total / len(items), 6) if items else None
    wall = _seconds(at["started"], at["closed"] or stop)
    seconds = sum(s["session_time_seconds"] for s in sessions)
    cost = round(sum(s["cost"] or 0 for s in sessions), 6)
    return {"batch": name, "status": batch.status, "pull_request": batch.pull_request,
            "items": [{"item": i.name, "title": i.title, "status": i.status} for i in items],
            "window": window, "wall_time_seconds": wall,
            "wall_time": measure_build.duration(wall) if wall is not None else None,
            "waiting_for_merge_seconds": _seconds(at["built"], at["closed"]),
            "session_time_seconds": seconds, "session_time": measure_build.duration(seconds),
            "tokens": {k: sum(s[k] for s in sessions) for k in measure_build.KINDS},
            "cost": cost, "unpriced": unpriced, "prices_as_of": measure_cost.AS_OF,
            "cost_by_role": measure_batch_sessions.roles_of(sessions),
            "sessions": sessions, "sessions_from": str(directory),
            "sessions_found": len(list(directory.rglob("*.jsonl"))) if directory.is_dir() else 0,
            **review, "defects": defects, "knobs": knobs_of(root, batch, reviews),
            "goals": {"wall_time_seconds": wall, "cost": cost, "defects_per_item": defects["per_item"]}}
