"""What the work-queue and requests handlers share (not a handler module itself, so the glob does not load it): the
scenario's repository as a git repository, the frontmatter of its nodes, the runs a scenario made, and a noun phrase
of a step matched against the files a run wrote or committed.

A handler module loads it by path (`shared()` in work_queue_handlers.py), as `vocab.load_handlers` loads the handler
modules themselves."""
import json
import re
import subprocess
from pathlib import Path

WORK = ".shop/work"
LINE_BREAK = "first line\nsecond line"


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def init(repo):
    """The repository as a git repository on main with an identity, everything in it committed, once a run."""
    repo = Path(repo)
    if not (repo / ".git").exists():
        git(repo, "init", "-q", "-b", "main")
        for key, value in (("user.name", "someone"), ("user.email", "someone@example.com"),
                           ("commit.gpgsign", "false")):
            git(repo, "config", key, value)
    git(repo, "add", "-A")
    if git(repo, "status", "--porcelain").strip():
        git(repo, "commit", "-q", "-m", "the scenario's repository")
    return git(repo, "rev-parse", "HEAD").strip()


def head(repo):
    try:
        return git(repo, "rev-parse", "HEAD").strip()
    except subprocess.CalledProcessError:
        return None


def committed(repo):
    """The files of the last commit."""
    return [p for p in git(repo, "show", "--name-only", "--format=", "HEAD").splitlines() if p]


def field(path, name):
    """A frontmatter field of a node's file, as written."""
    found = re.search(r"^%s: (.*)$" % re.escape(name), Path(path).read_text(), re.MULTILINE)
    return found.group(1).strip() if found else None


def node_rel(context, name):
    """Where the scenario wrote a node it named."""
    found = context.get("nodes", {}).get(name)
    return found[1] if found else None


def initiative_of(context, name):
    rel = node_rel(context, name)
    return rel.split("/")[2] if rel and rel.startswith(WORK + "/") else context.get("initiative", "i1")


def log(repo, initiative, item, before, after, by="supervision"):
    """Append a transition of `item` to its initiative's log.jsonl."""
    path = Path(repo) / WORK / initiative / "log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    line = {"time": "2026-10-15T00:00:00", "work-item": item, "before": before, "after": after, "by": by}
    with path.open("a") as out:
        out.write(json.dumps(line) + "\n")


def runs(step):
    return step.request.node.__dict__.get("_shop_runs", [])


def thing(step, name):
    """(kind, {attribute: value}) of an instance a Given named that is no node: a note, an answer, a question."""
    return step.context.get("things", {}).get(name, (None, {}))


PATHS = {"work-item": r"\.shop/work/[^/]+/w\d+\.md", "initiative": r"\.shop/work/[^/]+/initiative\.md",
         "request": r"\.shop/work/requests/q\d+\.md", "capability-proposal": r"\.shop/work/[^/]+/[^/]+\.md",
         "glossary-proposal": r"\.shop/work/[^/]+/[^/]+\.md", "transition": r"\.shop/work/[^/]+/log\.jsonl",
         "ledger": r"\.shop/work/[^/]+/ledger\.md"}


def matches(repo, context, np, rel):
    """Whether the file `rel` is what the noun phrase `np` names: an instance (`the work-item w1`), a ledger of an
    instance, or any node of a kind with an optional value (`a work-item that is `drafted``), an answer, a delegation
    or a transition."""
    path = Path(repo) / rel
    words = np.split()
    if np == "a decisions index":
        return rel == "spec/decisions/index.md"
    ledger = re.match(r"the ledger of the initiative (\S+)$", np)
    if ledger:
        return rel == "%s/%s/ledger.md" % (WORK, ledger.group(1))
    if words[0] == "the" and len(words) == 3:
        return rel == node_rel(context, words[2])
    kind = next((k for k in sorted(PATHS, key=len, reverse=True) if " %s" % k in " " + np), None)
    if np in ("an answer", "a question", "a delegation", "a resolution", "a line outcome"):
        section = {"an answer": "## Answers", "a question": "## Questions", "a resolution": "## Resolution",
                   "a line outcome": "## Outcomes"}
        if not path.is_file():
            return False
        text = path.read_text()
        return field(path, "delegation") is not None if np == "a delegation" else (
            section[np] in text and bool(text.split(section[np], 1)[1].split("\n## ", 1)[0].strip()))
    if kind is None or not re.fullmatch(PATHS[kind], rel) or not path.is_file():
        return False
    if kind in ("capability-proposal", "glossary-proposal") and field(path, "kind") != kind:
        return False
    value = re.search(r"that is `([^`]+)`", np)
    return value is None or field(path, "status") == value.group(1)


class Reads:
    """A step parser that matches any step the Steps grammar reads under its keyword (vocab.read)."""

    def __init__(self, vocab, root, keyword):
        self.vocab, self.root, self.keyword, self.name = vocab, root, keyword, "reads %s" % keyword

    def is_matching(self, name):
        return self.vocab.read(self.root, self.keyword, name) is not None

    def parse_arguments(self, name):
        return {"text": name}


def bind_all(namespace, root):
    """One step definition for each keyword, for any step the Steps grammar reads, dispatching to its handler as the
    vocabulary does. pytest-bdd prefers a test module's definitions to the conftest's, so these take over there: the
    vocabulary's own (template, kind) definition misses a step whose noun phrase names its kind with no instance
    (`` `work` writes a work-item that is `drafted` ``), by the words of its pattern."""
    import sys

    import pytest
    from pytest_bdd.steps import StepFunctionContext
    vocab = sys.modules["vocab"]
    for keyword in ("given", "when", "then"):
        context = StepFunctionContext(type=keyword, step_func=vocab._step_function(root, keyword),
                                      parser=Reads(vocab, root, keyword))
        name = "pytestbdd_stepdef_%s_reads_any" % keyword
        namespace[name] = pytest.fixture(name=name)(vocab._marker(context))
