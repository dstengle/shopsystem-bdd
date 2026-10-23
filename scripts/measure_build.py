"""measure's figures of one initiative: its stages, its work-items and their commits, its totals and, with a
directory of transcripts, its sessions. Standard library only."""
import re
import subprocess
from pathlib import Path

from measure_read import (
    Refused,
    read_log,
    read_session_jsons,
    read_transcripts,
    round_trips,
)

KINDS = ("output_tokens", "new_input_tokens", "cache_read_tokens")


def duration(seconds):
    """'1 hour 45 minutes', '12 minutes', '30 seconds'."""
    hours, rest = divmod(round(seconds), 3600)
    minutes, secs = divmod(rest, 60)
    parts = []
    if hours:
        parts.append("%d hour%s" % (hours, "" if hours == 1 else "s"))
    if minutes:
        parts.append("%d minute%s" % (minutes, "" if minutes == 1 else "s"))
    if secs or not parts:
        parts.append("%d second%s" % (secs, "" if secs == 1 else "s"))
    return " ".join(parts)


def stages_of(rows, sessions):
    """One entry per stage the log gives a start for, in the order started; its end where the log gives one."""
    stages, open_ = [], {}
    for row in rows:
        if row.get("event") == "start":
            one = {"work-item": row.get("work-item"), "stage": row.get("stage"), "agent": row.get("agent"),
                   "session": row.get("session"), "started": row["time"]}
            figures = sessions.get(row.get("session"))
            if figures:
                one.update({k: figures[k] for k in ("turns", *KINDS, "cost")})
            trips = round_trips(row.get("session"))
            if trips is not None:
                one["round_trips"] = trips
            stages.append(one)
            open_[(one["work-item"], one["stage"], one["session"])] = (one, row["at"])
        elif row.get("event") == "end":
            found = open_.pop((row.get("work-item"), row.get("stage"), row.get("session")), None)
            if found:
                one, began = found
                seconds = (row["at"] - began).total_seconds()
                one.update(ended=row["time"], took_seconds=seconds, took=duration(seconds))
    return stages


def merged_commits(root, name):
    """The commits `work run` merged for work-item <name>. It merges fast-forward, so they are the commits between
    the work-item's last transition commit before its merge (the one before its `-> done`) and its `-> done`
    transition commit, `work: ` transition commits excluded. None of a repository with no git."""
    if not (Path(root) / ".git").exists():
        return []
    done = subprocess.run(["git", "log", "--first-parent", "--reverse", "--format=%h%x09%s"], cwd=root,
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise Refused("git failed: " + done.stderr.strip())
    log = [line.split("\t", 1) for line in done.stdout.splitlines()]
    mine = re.compile(r"work: %s .*-> .*" % re.escape(name))
    moves = [i for i, (_, subject) in enumerate(log) if mine.fullmatch(subject)]
    ends = [i for i in moves if log[i][1].endswith("-> done")]
    if not ends:
        return []
    end = ends[-1]
    start = max([i for i in moves if i < end], default=-1)
    return [{"hash": h, "subject": sub} for h, sub in log[start + 1:end] if not sub.startswith("work: ")]


def work_items_of(rows, root):
    items = {}
    for row in rows:
        if "before" in row and "after" in row:
            one = items.setdefault(row["work-item"], {"work-item": row["work-item"], "transitions": []})
            one["transitions"].append({"time": row["time"], "from": row["before"], "to": row["after"]})
    for one in items.values():
        steps = one["transitions"]
        one["awaiting_answer"] = sum(1 for s in steps if s["to"] == "awaiting-answer")
        one["failed"] = sum(1 for s in steps if s["to"] == "failed")
        one["commits"] = merged_commits(root, one["work-item"])
    return list(items.values())


def sessions_found(directory, window):
    """The sessions that start inside the window, and every session those dispatched."""
    first, last = window
    found = read_transcripts(directory)
    inside = {s["session"] for s in found.values() if first and first <= s["start"] <= last}
    chosen = [s for s in found.values() if s["session"] in inside or s["dispatched_by"] in inside]
    return [{"session": s["session"], "started": s["start"].isoformat(), "dispatched_by": s["dispatched_by"],
             **{k: s[k] for k in KINDS}} for s in sorted(chosen, key=lambda s: s["start"])]


def figures_of(initiative, root, sessions_dir=None):
    """The measurement of `initiative`: its stages, work-items, totals and, with `sessions_dir`, its sessions."""
    work = Path(root) / ".shop" / "work" / initiative
    log = work / "log.jsonl"
    if not log.is_file():
        raise Refused("the initiative %s has no log.jsonl" % initiative)
    rows = read_log(log)
    stages = stages_of(rows, read_session_jsons(work / "runs"))
    moves = [r["at"] for r in rows if "before" in r and "after" in r]
    window = (min(moves), max(moves)) if moves else (None, None)
    totals = {"stages": len(stages), "sessions": len({s["session"] for s in stages if "turns" in s})}
    totals["turns"] = sum(s.get("turns", 0) for s in stages)
    totals["round_trips"] = sum(s.get("round_trips", 0) for s in stages)
    for kind in KINDS:
        totals[kind] = sum(s.get(kind, 0) for s in stages)
    totals["cost"] = round(sum(s.get("cost", 0) for s in stages), 6)
    seconds = (window[1] - window[0]).total_seconds() if moves else 0
    totals.update(time_seconds=seconds, time=duration(seconds))
    figures = {"initiative": initiative, "window": [m and m.isoformat() for m in window], "stages": stages,
               "work_items": work_items_of(rows, root), "totals": totals}
    if sessions_dir is not None:
        figures["sessions"] = sessions_found(sessions_dir, window)
    return figures
