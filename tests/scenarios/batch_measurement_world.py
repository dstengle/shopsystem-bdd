"""batch-measurement's world: the repository a scenario builds for `measure initiative`, and the run of it.

The Given steps only record what the repository is to hold (a log's rows, a stage's session.json, transcripts); the
When step writes it out with `World.flush` and calls `measure`'s `main` in-process, in the repository, on the date
the scenario names.
"""
import importlib.machinery
import importlib.util
import json
import subprocess
import sys

import pytest

from .conftest import SCRIPTS

DAY = "2026-10-22"
INITIATIVE = "i7-cart"
MEASUREMENTS = ".shop/records/measurements"


def load_measure():
    sys.path.insert(0, str(SCRIPTS))
    loader = importlib.machinery.SourceFileLoader("measure_script", str(SCRIPTS / "measure"))
    spec = importlib.util.spec_from_loader("measure_script", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def stamp(clock):
    """'10:00' as the day's ISO time, in UTC; a full ISO time is given as it is."""
    if "T" in clock:
        return clock
    return "%sT%s:00+00:00" % (DAY, clock)


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


class World:
    """What the repository is to hold, and what running `measure` in it left."""

    def __init__(self, repo):
        self.repo = repo
        self.today = DAY
        self.has_log = False
        self.rows = []
        self.sessions = {}          # session id -> (work-item, stage, session.json text)
        self.transcripts = {}       # path under the repository -> text
        self.directory = {}         # session id -> (dispatched by, start, path) of a session --sessions's directory holds
        self.store = {}           # session id -> its transcript in Claude Code's store (the test's own)
        self.git_steps = []       # callables run in order, in the repository, after the log is written
        self.last = None            # the stage the latest Given gave: (work-item, stage, indexes of its log rows)
        self.stage_of = {}          # session id -> (work-item, stage)
        self.existing = None        # a measurement a Given wrote, and its text then
        self.before = None
        self.expected = []          # the transitions a Given gave, as (from, to)
        self.moves = []             # (work-item, from, to) of the transitions a Given gave
        self.shown = None           # the measurement `measure show` is run on
        self.named = {}             # measurement name -> its path, for `measure compare`
        self.merged = ()            # the commits a work-item's merge brought in
        self.requests = []          # [id, held by the queue, asker] of each request the initiative fulfils
        self.code = None
        self.err = ""
        self.out = ""

    def work(self):
        return self.repo / ".shop" / "work" / INITIATIVE

    def log(self, **row):
        self.has_log = True
        self.rows.append(row)

    def stage(self, item, stage, start, end=None, agent="researcher", session="s-1"):
        base = {"work-item": item, "stage": stage, "agent": agent, "session": session}
        self.log(time=stamp(start), event="start", **base)
        if end:
            self.log(time=stamp(end), event="end", **base)

    def session(self, session, item, stage, turns, out, new, read, cost, reply="done"):
        usage = {"input_tokens": new, "cache_creation_input_tokens": 0, "cache_read_input_tokens": read,
                 "output_tokens": out}
        self.sessions[session] = (item, stage, json.dumps({
            "session_id": session, "num_turns": turns, "duration_ms": 1000, "total_cost_usd": cost,
            "usage": usage, "result": reply}))

    def flush(self):
        (self.repo / "spec").mkdir(exist_ok=True)
        (self.repo / "spec" / "index.md").write_text("---\nid: bounded-context/ex.com/prod/ctx\n---\n")
        self.work().mkdir(parents=True, exist_ok=True)
        if self.requests:
            links = "".join("fulfils: request/%s\n" % ident for ident, _, _ in self.requests)
            (self.work() / "initiative.md").write_text(
                "---\nid: initiative/ex.com/prod/ctx/%s\nkind: initiative\n%s---\n" % (INITIATIVE, links))
            requests = self.repo / ".shop" / "work" / "requests"
            requests.mkdir(parents=True, exist_ok=True)
            for ident, held, asker in self.requests:
                if held:
                    (requests / (ident + ".md")).write_text(
                        "---\nid: request/ex.com/prod/ctx/%s\nkind: request\nasker: %s\nsource: [%s]\n"
                        "status: accepted\nturn: asker\n---\n\n# a request\n" % (ident, asker, INITIATIVE))
        if self.has_log:
            (self.work() / "log.jsonl").write_text("".join(json.dumps(r) + "\n" for r in self.rows))
        for number, (session, (item, stage, text)) in enumerate(self.sessions.items(), 1):
            where = self.work() / "runs" / item / ("%d-%s" % (number, stage))
            where.mkdir(parents=True, exist_ok=True)
            (where / "session.json").write_text(text)
        for path, text in self.transcripts.items():
            (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / path).write_text(text)
        for session, text in self.store.items():
            where = self.repo / "claude-store" / "projects" / "-work-tree" / ("%s.jsonl" % session)
            where.parent.mkdir(parents=True, exist_ok=True)
            where.write_text(text)
        for step in self.git_steps:
            step()

    def run(self, monkeypatch, capsys, *args):
        """measure's main, in the repository, on the scenario's day; leaves its exit code and what it printed."""
        script = load_measure()
        import measure_write
        monkeypatch.setattr(measure_write, "today", lambda: self.today)
        monkeypatch.chdir(self.repo)
        monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(self.repo / "claude-store"))
        self.flush()
        self.code = script.main(list(args))
        seen = capsys.readouterr()
        self.out, self.err = seen.out, seen.err

    def record(self, date=None):
        return self.repo / MEASUREMENTS / ("%s-%s.md" % (date or self.today, INITIATIVE))

    def figures(self):
        """The measurement's figures: the JSON block of the record."""
        text = self.record().read_text()
        return json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])

    def written(self):
        directory = self.repo / MEASUREMENTS
        return sorted(p.name for p in directory.glob("*")) if directory.is_dir() else []


@pytest.fixture
def world(repo):
    return World(repo)


@pytest.fixture
def measure_run(world, monkeypatch, capsys):
    """Run `measure` with the arguments given; the exit code, stdout and stderr stay in the world."""
    return lambda *args: world.run(monkeypatch, capsys, *args)
