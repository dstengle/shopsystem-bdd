"""`work status`: where an initiative stands, for a session to start from (capability work-queue, r16-r18).

Read-only: it prints each work-item's status as its file gives it and moves nothing.
"""
import contextlib
import io
import json
import re
import subprocess
from pathlib import Path

import workqueue
from workqueue import Refused

ENDED = ("done", "abandoned")
DATED = re.compile(r"^- \d{4}-\d{2}-\d{2}: (.*)$")


def natural(name):
    return [int(w) if w.isdigit() else w for w in re.split(r"(\d+)", name)]


def git(root, *args):
    """git's stdout, or None when git cannot answer (no repository, no such ref, no remote)."""
    try:
        done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout if done.returncode == 0 else None


def section(text, heading):
    """The bullets under `## heading` of `text`."""
    found = re.search(r"(?ms)^## %s\n(.*?)(?=^## |\Z)" % heading, text)
    return [l[2:].strip() for l in found.group(1).splitlines() if l.startswith("- ")] if found else []


def parts(root, directory):
    """Each part of an initiative but its initiative.md and its ledger: (kind, name, status, open questions)."""
    for path in sorted(directory.glob("*.md"), key=lambda p: natural(p.stem)):
        if path.name in ("initiative.md", "ledger.md"):
            continue
        text = workqueue.read(path, root)
        data, _ = workqueue.frontmatter(text)
        if data.get("kind") in ("capability-proposal", "work-item"):
            # the n-th answer answers the n-th question (work run's rule); the open ones are those past the answers
            questions = section(text, "Questions")[len(section(text, "Answers")):]
            yield data["kind"], path.stem, data.get("status"), questions


def branch(root):
    """The checkout's branch and whether its remote has every commit of it (True, False, or None when unknown)."""
    name = (git(root, "symbolic-ref", "--short", "-q", "HEAD") or "").strip() or None
    if name is None:
        return {"name": None, "pushed": None}
    remote = (git(root, "config", "branch.%s.remote" % name) or "origin").strip()
    listed = (git(root, "ls-remote", remote, "refs/heads/" + name) or "").split()
    pushed = None
    if listed and git(root, "rev-parse", "-q", "--verify", "HEAD") is not None:
        pushed = git(root, "merge-base", "--is-ancestor", "HEAD", listed[0]) is not None
    return {"name": name, "pushed": pushed}


def changes(root):
    """(tracked files with changes, untracked files git does not ignore), by git status of the whole checkout."""
    out = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all") or ""
    changed, untracked, entries = [], [], iter(out.split("\0"))
    for entry in entries:
        if len(entry) < 4:
            continue
        (untracked if entry[:2] == "??" else changed).append(entry[3:])
        if entry[0] in "RC":
            next(entries, None)     # a rename or copy is followed by the path it came from
    return changed, untracked


def ledger(directory):
    path = directory / "ledger.md"
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    nexts = [l for l in lines if (DATED.match(l) or [None, ""])[1].startswith("next:")]
    return lines[-10:], (nexts[-1] if nexts else None)


def read(root, name, shared):
    directory = Path(root) / workqueue.WORK / name
    data, _ = workqueue.frontmatter(workqueue.read(directory / "initiative.md", root))
    found = list(parts(root, directory))
    last, newest = ledger(directory)
    return {"initiative": name, "status": data.get("status"),
            "proposals": [{"capability-proposal": n, "status": s} for k, n, s, _ in found if k == "capability-proposal"],
            "work-items": [{"work-item": n, "status": s, "questions": q} for k, n, s, q in found if k == "work-item"],
            "branch": shared["branch"], "uncommitted": shared["uncommitted"], "untracked": shared["untracked"],
            "ledger": last, "next": newest}


def render(found):
    pushed = {True: "the remote has every commit of it", False: "the remote does not have every commit of it",
              None: "the remote cannot be compared with it"}[found["branch"]["pushed"]]
    lines = ["initiative %s %s" % (found["initiative"], found["status"])]
    lines += ["capability-proposal %s %s" % (p["capability-proposal"], p["status"]) for p in found["proposals"]]
    for item in found["work-items"]:
        lines.append("work-item %s %s" % (item["work-item"], item["status"]))
        lines += ["  question: %s" % q for q in item["questions"]]
    lines.append("branch %s: %s" % (found["branch"]["name"], pushed))
    for title, files in (("uncommitted", found["uncommitted"]), ("untracked", found["untracked"])):
        lines += [title + ":"] + ["  " + f for f in files] if files else [title + ": none"]
    lines += ["ledger:"] + ["  " + l for l in found["ledger"]]
    lines.append("last next: %s" % (found["next"] or "none"))
    return "\n".join(lines)


def open_names(root):
    """The names of the initiatives under .shop/work/ whose initiative.md gives a status other than done or abandoned."""
    work = Path(root) / workqueue.WORK
    names = sorted((p.parent.name for p in work.glob("*/initiative.md")), key=natural)
    return [n for n in names
            if workqueue.frontmatter(workqueue.read(work / n / "initiative.md", root))[0].get("status") not in ENDED]


def open_text(root):
    """What `work status` prints at `root` for each initiative neither done nor abandoned ('' when there is none)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        status(root, None, False)
    return out.getvalue()


def status(root, initiative, as_json):
    """Print where `initiative` stands, or each initiative neither done nor abandoned; return the exit status."""
    work = Path(root) / workqueue.WORK
    if initiative is not None:
        workqueue.entry(initiative, "initiative")
        if not (work / initiative / "initiative.md").is_file():
            raise Refused("the initiative %s does not exist (no %s)" % (initiative, (work / initiative).relative_to(root)))
        names = [initiative]
    else:
        names = sorted((p.parent.name for p in work.glob("*/initiative.md")), key=natural)
    changed, untracked = changes(root)
    shared = {"branch": branch(root), "uncommitted": changed, "untracked": untracked}
    found = [read(root, n, shared) for n in names]
    if initiative is None:
        found = [f for f in found if f["status"] not in ENDED]
    if as_json:
        print(json.dumps({"initiatives": found}))
    elif found:
        print("\n\n".join(render(f) for f in found))
    return 0
