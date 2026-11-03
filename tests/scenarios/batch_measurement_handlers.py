"""batch-measurement's handlers (design §14.3): the Givens record on a World (batch_measurement_world.py) what the
repository is to hold, a canned setup for an initiative log, a transcript or a measurement named with no text; every
`measure ...` command of the generated feature runs `measure`'s main in-process on the World's day; the Thens read
what it printed and the measurement it wrote.

`include "x"` holds when x is in the measurement's text; `not include "x"` when x is in none of its entries (its
stages, work-items, sessions and request; its totals are left out, since they always name every figure)."""
import json
import pathlib
import re
import shlex
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

from scenarios import batch_measurement_transcripts as tr
from scenarios import batch_measurement_world as bw

FEATURE = HERE.parents[1] / "features" / "batch-measurement.feature"
ASKERS = {"internal": (True, "internal"), "external": (True, "bounded-context/ex.com/prod/other"),
          "unheld": (False, "internal"), "askerless": (True, "")}


def bare(word):
    return word.strip("`")


def world(step):
    if "world" not in step.context:
        step.context["world"] = bw.World(step.repo)
    return step.context["world"]


def standard(w):
    w.stage("cart-1", "research", "10:00", "10:12", session="s-1")
    w.session("s-1", "cart-1", "research", 14, 3000, 2000, 50000, 0.42)


def transitions(w, first, last):
    w.log(**{"time": bw.stamp(first), "work-item": "cart-1", "before": "drafted", "after": "researched"})
    w.log(**{"time": bw.stamp(last), "work-item": "cart-1", "before": "researched", "after": "planned"})


def git_moves(w):
    bw.git(w.repo, "init", "-q", "-b", "main")
    bw.git(w.repo, "config", "user.email", "t@example.com")
    bw.git(w.repo, "config", "user.name", "t")
    bw.git(w.repo, "commit", "-q", "--allow-empty", "-m", "start")
    for item, before, after in w.moves:
        bw.git(w.repo, "commit", "-q", "--allow-empty", "-m", "work: %s %s -> %s" % (item, before, after))


def in_utc_plus_five(step):
    step.fixtures("monkeypatch").setenv("TZ", "UTC-5")      # POSIX spells the sign the other way round
    time.tzset()
    step.request.addfinalizer(time.tzset)


def log_named(step, name):
    w = world(step)
    if name == "i7-cart":
        standard(w)
    elif name == "zulu":
        in_utc_plus_five(step)
        transitions(w, "2026-10-22T07:55:00Z", "2026-10-22T11:40:00+02:00")
    elif name == "transitions":
        standard(w)
        moves = [("drafted", "researched"), ("researched", "awaiting-answer"), ("awaiting-answer", "researched")]
        for number, (before, after) in enumerate(moves):
            w.log(**{"time": bw.stamp("10:%02d" % number), "work-item": "cart-1", "before": before, "after": after})
        w.moves = [("cart-1", *move) for move in moves]
        w.git_steps.append(lambda: git_moves(w))
    elif name == "window":
        transitions(w, "09:55", "11:40")
    elif name == "secret":
        w.stage("cart-1", "research", "10:00", "10:12", session="s-1")
        w.session("s-1", "cart-1", "research", 3, 10, 10, 10, 0.01, reply="a secret reply")
        transitions(w, "09:00", "23:00")
        w.transcripts["sessions/s-9.jsonl"] = tr.raw_session("s-9", "11:00", "11:30", "a secret prompt", "a secret tool")
    else:
        raise AssertionError("no canned initiative log %s" % name)


@handler("GivenK", "initiative log")
def given_log(step):
    log_named(step, bare(step.names[0]))


@handler("GivenK_A", "logged stage")
def given_stage(step):
    w = world(step)
    ended = step.values[0] == "`ended`"
    w.stage(bare(step.names[0]), "research", "10:00" if ended else "10:20", "10:12" if ended else None, session="s-1")
    w.session("s-1", bare(step.names[0]), "research", 14, 3000, 2000, 50000, 0.42)


@handler("GivenK_A", "fulfilled request")
def given_request(step):
    held, asker = ASKERS[bare(step.values[0])]
    world(step).requests.append([step.names[0], held, asker])


@handler("GivenCode", "session file")
@handler("GivenK_A", "session file")
def given_session_file(step):
    w, session = world(step), bare(step.names[0])
    item, stage, _ = w.sessions[session]
    w.sessions[session] = (item, stage, step.quoted[0].strip('"') if step.quoted else "")
    assert not step.values or step.values[0] == "`empty`"


@handler("GivenCode", "transcript")
def given_transcript_text(step):
    world(step).transcripts[bare(step.names[0])] = step.quoted[0].strip('"') + "\n"


def line_break_inside(session):
    rows = [json.loads(line) for line in tr.store_session(session, 3, 3).splitlines()]
    rows[0]["message"]["content"] = [{"type": "text", "text": "before after"}]
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


@handler("GivenK_A", "transcript")
def given_transcript(step):
    w, name = world(step), bare(step.names[0])
    if step.values[0] == "`found`":
        w.store["s-1"] = line_break_inside("s-1") if name == "u2028" else tr.store_session("s-1", 4, 2)
    else:
        assert "s-1" not in w.store


SESSIONS = (("s-7", "09:00", "09:00, 09:20, 12:00", None), ("s-8", "09:30", "09:30, 09:50, 10:05", None),
            ("s-9", "11:00", "11:00, 12:30", None), ("s-11", "12:00", "12:00, 12:20", "s-9"),
            ("s-10", "11:50", "11:50, 12:10", None), ("s-12", "12:05", "12:05, 12:08", "s-10"))


@handler("GivenK", "transcript")
def given_directory(step):
    """The directory `sessions` of r43's example: s-8, s-9 and s-11 inside the window, s-7, s-10 and s-12 not."""
    assert bare(step.names[0]) == "sessions"
    w = world(step)
    for session, starts, times, parent in SESSIONS:
        where = "sessions/%s/subagents/%s.jsonl" % (parent, session) if parent else "sessions/%s.jsonl" % session
        w.directory[session] = (parent, starts, where)
        w.transcripts[where] = tr.timed_session(session, parent, times.split(", "), 100, 10, 1000)
    w.transcripts["sessions/s-9.jsonl"] += tr.tool_use_rows("s-9", None, "11:00", {"Bash": 2, "Read": 1})
    w.transcripts["sessions/s-9.jsonl"] += tr.compaction_rows("s-9", None, "11:00", 1)


@handler("GivenCode", "measurement")
def given_existing(step):
    w = world(step)
    w.existing = w.repo / bw.MEASUREMENTS / ("%s.md" % bare(step.names[0]))
    w.existing.parent.mkdir(parents=True, exist_ok=True)
    w.existing.write_text(step.quoted[0].strip('"') + "\n")
    w.before = w.existing.read_text()


STAGE = {"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}
SESSION = {"session": "s-9", "started": None, "dispatched_by": None, "output_tokens": 9000, "new_input_tokens": 4000,
           "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"],
           "compactions": 1}
MEASUREMENTS = {"m1": {"stages": [dict(STAGE, round_trips=7)], "work_items": [],
                       "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}},
                "m2": {"stages": [STAGE], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}},
                "m3": {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [SESSION]}}


@handler("GivenK", "measurement")
def given_measurement(step):
    name = bare(step.names[0])
    path = step.repo / ("%s.md" % name)
    path.write_text("# Measurement\n\n```json\n%s\n```\n" % json.dumps(MEASUREMENTS[name]))


def runs_measure(step):
    w = world(step)
    argv = shlex.split(bare(step.command))[1:] + step.context.get("flags", [])
    w.run(step.fixtures("monkeypatch"), step.fixtures("capsys"), *argv)


for _command in sorted(set(re.findall(r"When the person runs (`measure[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_measure)


def mentioned(np):
    """What a noun phrase of an error names in measure's refusal."""
    if np.startswith('"'):
        return np.strip('"')
    if np.startswith("the session file"):
        return "session.json"
    found = re.search(r"(`[^`]+`|\b[a-z][a-z0-9-]*\d)$", np)
    return bare(found.group(1)).split("/")[-1] if found else bare(np)


@handler("ThenExitsOk", "`measure`")
def exits_ok(step):
    assert world(step).code == 0, world(step).err


@handler("ThenExitsErr", "`measure`")
def exits_err(step):
    w = world(step)
    assert w.code not in (0, None), w.out
    for np in step.nps:
        assert mentioned(np) in w.err, (np, w.err)


@handler("ThenChangesNothing", "`measure`")
def changes_nothing(step):
    w = world(step)
    if w.existing:
        assert w.existing.read_text() == w.before
    else:
        assert w.written() == [], w.written()


@handler("ThenPrints", "`measure`")
def prints(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        assert bare(np.strip('"')) in w.out, (np, w.out)


@handler("ThenPrintsNot", "`measure`")
def prints_not(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        assert np.strip('"') not in w.out, (np, w.out)


@handler("ThenDoes", "include")
def includes(step):
    w = world(step)
    assert w.code == 0, w.err
    for np in step.nps:
        assert np.strip('"') in w.record().read_text(), (np, w.record().read_text())


@handler("ThenDoesNot", "include")
def includes_not(step):
    w = world(step)
    assert w.code == 0, w.err
    entries = {k: v for k, v in w.figures().items() if k != "totals"}
    for np in step.nps:
        assert np.strip('"') not in json.dumps(entries), (np, entries)
