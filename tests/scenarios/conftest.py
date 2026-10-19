"""Fixtures every scenario step module shares."""
import json
import pathlib
import subprocess
import sys
import textwrap

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


@pytest.fixture
def repo(tmp_path):
    """A fresh temporary directory, the root of the repository a scenario builds."""
    return tmp_path


@pytest.fixture
def context():
    """What a When step leaves for the Then steps."""
    return {}


@pytest.fixture
def run(repo):
    """Run one of the scripts (model, features, tools) with this Python; return the completed process.

    `run("model", "check", "--root", ...)`: the arguments go to the script as given; `cwd` defaults to the repository root.
    """
    def _run(script, *args, cwd=None, **kwargs):
        cmd = [sys.executable, str(SCRIPTS / script), *map(str, args)]
        return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or repo, **kwargs)
    return _run


def pytest_configure(config):
    """The feature files' requirement tags (@r1 ...) are marks; register them."""
    for number in range(1, 200):
        config.addinivalue_line("markers", "r%d: scenario of requirement r%d" % (number, number))


# --- the repositories design-model-check's scenarios build ---------------------------------------------------
# Paths are the ones `model` reads today (spec/, features/, decisions/, work/, records/); final-layout-read moves
# the decision, work and record paths, and the builders below are where they change.

PATH = "ex.com/prod/ctx"
CONTEXT = "bounded-context/" + PATH
INDEX = "---\nid: %s\n---\n# ctx\n" % CONTEXT


def full(kind, name):
    """A node's id in full: <kind>/<context path>/<name>."""
    return "%s/%s/%s" % (kind, PATH, name)


THING = full("capability", "thing")
P1 = full("capability-proposal", "p1")
I1 = full("initiative", "i1")
W1 = full("work-item", "w1")
OBS1 = full("observation", "obs-1")


def cap(name, reqs, group="service", retired="[]", rests_on="[]"):
    """The text of a capability file: its Behaviour holds `reqs`, one line each."""
    lines = "\n".join(reqs)
    return textwrap.dedent("""\
        ---
        id: capability/%s/%s
        title: %s
        narrator: a client
        group: %s
        rests_on: %s
        formulated_as: features/%s.feature
        retired: %s
        ---

        # %s

        ## Purpose
        Something.

        ## Behaviour
        """ % (PATH, name, name, group, rests_on, name, retired, name)) + lines + "\n\n## Not yet\n- None.\n"


def feature(name, *scenarios):
    """The text of a feature file: `scenarios` are (tag line, title) pairs."""
    out = ["# formulated from spec/capabilities/%s.md" % name, "Feature: " + name, "  Narrator: a client", ""]
    for tag, title in scenarios:
        out += ["  " + tag, "  Scenario: " + title, "    Given a thing", "    Then it holds", ""]
    return "\n".join(out)


class World:
    """The repository a scenario builds in `repo`, and the way to run `model` on it."""

    def __init__(self, root):
        self.root = root
        self.write("spec/index.md", INDEX)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def model(self, *args, python=None, **kwargs):
        """Run `model --root <repo> <args>`; `python` is the interpreter's command line."""
        cmd = (python or [sys.executable]) + [str(SCRIPTS / "model"), "--root", str(self.root), *args]
        return subprocess.run(cmd, capture_output=True, text=True, **kwargs)

    def check_json(self, *args):
        """`model check --json`: the parsed object, and the process."""
        r = self.model("check", "--json", *args)
        return json.loads(r.stdout), r

    def work_item(self, ident="w1", **fields):
        fm = {"id": full("work-item", ident), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted",
              "under": "thing", "check": "true"}
        fm.update(fields)
        body = "".join("%s: %s\n" % (k, v) for k, v in fm.items() if v is not None)
        self.write("work/i1/%s.md" % ident, "---\n%s---\n" % body)

    def good(self):
        """One capability whose one requirement has its scenario."""
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it answers."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it answers")))

    def initiative(self, ident="i1", source="[observation/obs-1]", status="started", kind="capability-change"):
        self.write("work/%s/initiative.md" % ident, textwrap.dedent("""\
            ---
            id: %s
            title: t
            summary: s
            kind: %s
            owner-level: ctx
            status: %s
            priority: 1
            source: %s
            date: 2026-10-15
            ---
            """ % (full("initiative", ident), kind, status, source)))

    def proposal(self, ident="p1", status="drafted", adds="[]", changes="[]", initiative="i1", argues="[thing]",
                 removes="[]", date="2026-10-15"):
        self.write("work/%s/%s.md" % (initiative, ident), textwrap.dedent("""\
            ---
            id: %s
            kind: capability-proposal
            part_of: initiative/%s
            status: %s
            argues: %s
            adds: %s
            changes: %s
            removes: %s
            date: %s
            ---
            """ % (full("capability-proposal", ident), initiative, status, argues, adds, changes, removes, date)))

    def observation(self, ident="obs-1"):
        self.write("records/observations.md", "# Observations\n\n## %s\nabout: %s\nby: someone\ndate: 2026-10-15\n\nSeen.\n"
                   % (full("observation", ident), CONTEXT))


@pytest.fixture
def world(repo):
    """The builder and runner for the repository in `repo`."""
    return World(repo)
