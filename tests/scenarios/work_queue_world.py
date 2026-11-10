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
    if git(repo, "status", "--porcelain").strip() or head(repo) is None:
        git(repo, "commit", "-q", "--allow-empty", "-m", "the scenario's repository")
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
         "request": r"\.shop/requests/q\d+\.md", "capability-proposal": r"\.shop/work/[^/]+/[^/]+\.md",
         "glossary-proposal": r"\.shop/work/[^/]+/[^/]+\.md", "transition": r"\.shop/work/[^/]+/log\.jsonl",
         "ledger": r"\.shop/work/[^/]+/ledger\.md", "design-decision": r"spec/decisions/\d{4}-[^/]+\.md",
         "record": r"\.shop/records/\d{4}-\d\d-\d\d-[^/]+\.md",
         "batch brief": r"\.shop/worktrees/batch-\d+-driver/brief\.md", "rule catalogue": r"grammar/rules\.md",
         "feature": r"features/.+\.feature"}


SECTIONS = {"answer": "## Answers", "question": "## Questions", "resolution": "## Resolution",
            "line outcome": "## Outcomes", "delegation": None}
KINDS = sorted(set(PATHS) | set(SECTIONS), key=len, reverse=True)


def named(np):
    """(kind, name) of a noun phrase that names an instance of a kind the world keeps (`the work-item w1`)."""
    found = re.fullmatch(r"the (.+) (\S+)", np)
    return (found.group(1), found.group(2)) if found and found.group(1) in KINDS else None


def matches(repo, context, np, rel):
    """Whether the file `rel` is what the noun phrase `np` names: an instance the scenario wrote (`the work-item
    w1`), a ledger of an instance, or any node of a kind with an optional value (`a work-item that is `drafted``),
    an answer, a delegation or a transition. An instance the scenario has not written yet (the trace's name for what
    the command writes) is matched as any of its kind."""
    path = Path(repo) / rel
    if re.fullmatch(r"`[^`]+`", np):      # a file named by its path (migration-tools' `.shop/work/FROZEN.md`)
        return rel == np.strip("`")
    if re.fullmatch(r"(a|the) decisions index( \S+)?", np):
        return rel == "spec/decisions/index.md"
    ledger = re.match(r"the ledger of the initiative (\S+)$", np)
    if ledger:
        return rel == "%s/%s/ledger.md" % (WORK, ledger.group(1))
    instance = named(np)
    written = re.fullmatch(r"the .+ (\S+)", np)     # any kind another world wrote into the nodes (supervision's)
    if written and node_rel(context, written.group(1)):
        return rel == node_rel(context, written.group(1))
    kind = instance[0] if instance else next((k for k in KINDS if " %s" % k in " " + np), None)
    if kind in SECTIONS:
        if not path.is_file():
            return False
        text = path.read_text()
        if SECTIONS[kind] is None:
            return field(path, "delegation") is not None
        return SECTIONS[kind] in text and bool(text.split(SECTIONS[kind], 1)[1].split("\n## ", 1)[0].strip())
    if kind is None or not re.fullmatch(PATHS[kind], rel) or not path.is_file():
        return False
    if kind in ("capability-proposal", "glossary-proposal") and field(path, "kind") != kind:
        return False
    value = re.search(r"that is `([^`]+)`", np)
    return value is None or field(path, "status") == value.group(1)


def scenario_texts(step):
    """The texts of every step of the scenario that is running."""
    found = getattr(getattr(step.request.node, "function", None), "__scenario__", None)
    return [s.name for s in found.steps] if found is not None else []


DEFAULT = {"initiative": "started", "request": "open", "work-item": "drafted", "capability-proposal": "drafted"}
ELSEWHERE = "i9"


def ensure_named(step, write_node):
    """Write every node the scenario names that no Given wrote, before its command runs: the trace names an instance
    with no fluent at its first mention in a When or a Then (`work` prints the work-item w2). A work-item no Given
    keeps in an initiative is kept in an initiative of its own, so that it is in no initiative the scenario shows."""
    nodes = step.context.setdefault("nodes", {})
    for text in scenario_texts(step):
        for kind, name in re.findall(r"\bthe (%s) ([a-z]+\d+)\b" % "|".join(map(re.escape, DEFAULT)), text):
            if name in nodes or name in step.context.get("things", {}):
                continue
            if kind != "initiative" and kind != "request":
                step.context.setdefault("part_of", {}).setdefault(name, ELSEWHERE)
                if ELSEWHERE not in nodes:
                    write_node(step, "initiative", ELSEWHERE, "started")
            write_node(step, kind, name, DEFAULT[kind])
        for name in re.findall(r"\bthe observation ([a-z]+\d+)\b", text):
            if name not in step.context.setdefault("observations", set()):
                cite(step, name, write_node)


def observation(repo, name):
    """Add the observation `name` to .shop/records/observations.md; return its id."""
    path = Path(repo) / ".shop" / "records" / "observations.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    head = path.read_text() if path.is_file() else "# Observations\n"
    ident = "observation/ex.com/prod/ctx/%s" % name
    path.write_text(head + "\n## %s\nabout: bounded-context/ex.com/prod/ctx\nby: someone\ndate: 2026-10-15\n\n"
                    "Seen.\n" % ident)
    return ident


def cite(step, name, write_node):
    """An observation the scenario names that no Given wrote, cited by the `source` of an initiative of its own."""
    step.context["observations"].add(name)
    ident = observation(step.repo, name)
    rel = write_node(step, "initiative", ELSEWHERE, "started")
    rel.write_text(rel.read_text().replace("source: [", "source: [%s, " % ident, 1))


# Handlers of these features only, tried before the registry's (template, term) handler: a (template, kind) whose
# registry handler is another capability's (design-model-check's condition Givens of an initiative) or a shared one
# that does not read a negated Given (world_nodes' `the request q1 is not `accepted``). Each returns False to pass
# the step on to the registry's handler.
LOCAL = {}


def local(template, kind=None):
    """A second registration of one key chains (plan 4, D23): the new handler is tried first, the earlier one when it
    returns False."""
    def mark(fn):
        earlier = LOCAL.get((template, kind))
        LOCAL[(template, kind)] = fn if earlier is None else (lambda step: earlier(step) if fn(step) is False else None)
        return fn
    return mark


def _local_first(vocab, root, keyword):
    import sys

    import features_vocab
    registry = vocab._step_function(root, keyword)

    def step_function(text, request, docstring=None, datatable=None):
        call = features_vocab.step(features_vocab.load(root), keyword, text)
        call.docstring, call.datatable, call.fixtures = docstring, datatable, request.getfixturevalue
        table = getattr(sys.modules.get("shop_work_queue_world"), "LOCAL", LOCAL)   # the handlers' copy of this module
        found = table.get((call.template, call.kind)) or table.get((call.template, None))
        if found is not None and found(call) is not False:
            return None
        return registry(text, request, docstring, datatable)
    return step_function


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
        context = StepFunctionContext(type=keyword, step_func=_local_first(vocab, root, keyword),
                                      parser=Reads(vocab, root, keyword))
        name = "pytestbdd_stepdef_%s_reads_any" % keyword
        namespace[name] = pytest.fixture(name=name)(vocab._marker(context))
