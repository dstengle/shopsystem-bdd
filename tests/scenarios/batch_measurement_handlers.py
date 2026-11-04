"""batch-measurement's handlers (design §14.3): the Givens record on a World (batch_measurement_world.py) what the
repository is to hold: an initiative log's or a measurement's example rows, or the condition or value a trace gives a
thing; every `measure ...` command of the generated feature makes the rest of the repository (`made`: the standard
log when no Given wrote one) and runs `measure`'s main in-process on the World's day; the Thens read what it printed
and the measurement it wrote.

`include "x"` holds when x is in the measurement's text; `not include "x"` when x is in none of its entries (its
stages, work-items, sessions and request; its totals are left out, since they always name every figure). `include
"x" for the logged stage l1` holds when x is a figure of that stage's entry, `not include` when it is not."""
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
    """The log a scenario's initiative has when no Given writes one: one research stage, 10:00 to 10:12."""
    w.stage("cart-1", "research", "10:00", "10:12", session="s-1")
    w.session("s-1", "cart-1", "research", 14, 3000, 2000, 50000, 0.42)


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


# --- Givens ---

@handler("GivenCodeText", "initiative log")
def given_log_rows(step):
    """The initiative log's rows, one JSON object a line, read in a zone east of UTC; a stage's session is the canned
    one with a reply, and the work-item branch has one commit for each transition."""
    w = world(step)
    in_utc_plus_five(step)
    for line in step.docstring.splitlines():
        row = json.loads(line)
        w.log(**row)
        if "before" in row:
            w.moves.append((row["work-item"], row["before"], row["after"]))
        elif row.get("event") == "start":
            w.session(row["session"], row["work-item"], row["stage"], 14, 3000, 2000, 50000, 0.42,
                      reply="a secret reply")
    if w.moves:
        w.git_steps.append(lambda: git_moves(w))


@handler("GivenK", "initiative log")
@handler("GivenK", "measurement")
def given_thing(step):
    """A thing a condition is about: the condition's Given says what it is."""


@handler("GivenK", "logged stage")
def given_logged_stage(step):
    """The stage of the standard log, whose session file and transcript the scenario's other Givens describe."""
    world(step).called[step.names[0]] = "cart-1"


@handler("GivenR", "has")
def given_has(step):
    """A logged stage's session file or transcript: the one stage has the one session, so the Given only records."""


@handler("GivenK_C", "initiative log")
def given_log_condition(step):
    w, word = world(step), step.text.rsplit(" is ", 1)[1]
    if word == "unwritten":
        w.unwritten = True
    elif word == "overfulfilling":
        w.requests += [["q1", True, ASKERS["external"][1]], ["q2", True, ASKERS["external"][1]]]
    else:
        assert word == "requestless", step.text


@handler("GivenK_C", "measurement")
def given_existing(step):
    w = world(step)
    assert step.text.endswith(" is present"), step.text
    w.existing = w.record()
    w.existing.parent.mkdir(parents=True, exist_ok=True)
    w.existing.write_text("an earlier measurement\n")
    w.before = w.existing.read_text()
    w.called[step.names[0]] = w.existing.stem


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


@handler("GivenK_A", "session file")
def given_session_file(step):
    w = world(step)
    w.content = bare(step.values[0])
    w.called[step.names[0]] = "session.json"


@handler("GivenK_A", "transcript")
def given_transcript(step):
    w = world(step)
    w.availability = bare(step.values[0])
    w.called[step.names[0]] = "s-9.jsonl" if w.availability == "unreadable" else "s-1"


@handler("GivenCodeText", "measurement")
def given_measurement(step):
    path = step.repo / ("%s.md" % bare(step.names[0]))
    path.write_text("# Measurement\n\n```json\n%s\n```\n" % step.docstring)


# --- the world a When runs in ---

def line_break_inside(session):
    rows = [json.loads(line) for line in tr.store_session(session, 3, 3).splitlines()]
    rows[0]["message"]["content"] = [{"type": "text", "text": "before after"}]
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


SESSIONS = (("s-7", "09:00", "09:00, 09:20, 12:00", None), ("s-8", "09:30", "09:30, 09:50, 10:05", None),
            ("s-9", "11:00", "11:00, 12:30", None), ("s-11", "12:00", "12:00, 12:20", "s-9"),
            ("s-10", "11:50", "11:50, 12:10", None), ("s-12", "12:05", "12:05, 12:08", "s-10"))


def directory(w):
    """The directory `sessions` of r17's example: s-8, s-9, s-11 and s-13 inside the window, s-7, s-10 and s-12 not;
    s-13 has a prompt and a tool call whose content is not to be measured."""
    for session, starts, times, parent in SESSIONS:
        where = "sessions/%s/subagents/%s.jsonl" % (parent, session) if parent else "sessions/%s.jsonl" % session
        w.directory[session] = (parent, starts, where)
        w.transcripts[where] = tr.timed_session(session, parent, times.split(", "), 100, 10, 1000)
    w.transcripts["sessions/s-9.jsonl"] += tr.tool_use_rows("s-9", None, "11:00", {"Bash": 2, "Read": 1})
    w.transcripts["sessions/s-9.jsonl"] += tr.compaction_rows("s-9", None, "11:00", 1)
    w.transcripts["sessions/s-13.jsonl"] = tr.raw_session("s-13", "11:00", "11:30", "a secret prompt", "a secret tool")


def made(w, sessions):
    """The repository the Givens describe: the standard log when no Given wrote one, the session.json and transcript
    as a Given said, and the sessions directory for `--sessions`."""
    if not w.has_log and not w.unwritten:
        standard(w)
    if w.content:
        item, stage, _ = w.sessions["s-1"]
        if w.content != "filled":
            w.sessions["s-1"] = (item, stage, "" if w.content == "empty" else "not a session")
    if w.availability == "found":
        w.store["s-1"] = line_break_inside("s-1")
    if sessions:
        directory(w)
    if w.availability == "unreadable":
        w.transcripts["sessions/s-9.jsonl"] = "this is not a transcript\n"


def runs_measure(step):
    w = world(step)
    argv = shlex.split(bare(step.command))[1:] + step.context.get("flags", [])
    if argv[0] == "initiative":
        made(w, "--sessions" in argv)
    w.run(step.fixtures("monkeypatch"), step.fixtures("capsys"), *argv)


for _command in sorted(set(re.findall(r"When the person runs (`measure[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_measure)


# --- Thens ---

def mentioned(w, np):
    """What a noun phrase of an error names in measure's refusal."""
    if np.startswith('"'):
        return np.strip('"')
    found = re.search(r"(`[^`]+`|\b[a-z][a-z0-9-]*\d)$", np)
    name = bare(found.group(1)) if found else bare(np)
    return w.called.get(name, name.split("/")[-1])


@handler("ThenExitsOk", "`measure`")
def exits_ok(step):
    assert world(step).code == 0, world(step).err


@handler("ThenExitsErr", "`measure`")
def exits_err(step):
    w = world(step)
    assert w.code not in (0, None), w.out
    for np in step.nps:
        assert mentioned(w, np) in w.err, (np, w.err)


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


def stage_figures(w, name):
    """The figures of the stage a scenario names (`l1`): the keys of its entry."""
    item = w.called.get(name, name)
    found = [s for s in w.figures()["stages"] if s["work-item"] == item]
    assert len(found) == 1, (name, w.figures()["stages"])
    return found[0]


@handler("ThenDoes", "include")
def includes(step):
    w = world(step)
    assert w.code == 0, w.err
    if step.names:
        for q in step.quoted:
            assert q.strip('"') in stage_figures(w, step.names[0]), (q, step.text)
        return
    for np in step.nps:
        assert np.strip('"') in w.record().read_text(), (np, w.record().read_text())


@handler("ThenDoesNot", "include")
def includes_not(step):
    w = world(step)
    assert w.code == 0, w.err
    if step.names:
        for q in step.quoted:
            assert q.strip('"') not in stage_figures(w, step.names[0]), (q, step.text)
        return
    entries = {k: v for k, v in w.figures().items() if k != "totals"}
    for np in step.nps:
        assert np.strip('"') not in json.dumps(entries), (np, entries)
