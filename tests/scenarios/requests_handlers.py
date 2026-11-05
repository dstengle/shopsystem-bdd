"""Handlers of features/requests.feature (design §14.3): the request commands of `work` run on the requests
world_nodes.py writes, in a git repository, with the lines, delegations and origins the Givens keep in the context.

A request's `turn` follows its status before a command runs (the asker's for `awaiting-asker`, `delivered` and
`refused`), since world_nodes writes every request in the upstream's turn. Where the bounded context is downstream,
the request is the context's own request to its upstream (its asker is the context, it names no origin). `ThenDoes`
and `ThenDoesNot` with `change` compare a request's status or side with what it was before the command ran."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def shared():
    name = "shop_work_queue_world"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("work_queue_world.py"))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared()
OWN = "bounded-context/ex.com/prod/ctx"
FIXTURE = (Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "glossary" / "spec" / "index.md").read_text()
# The context's index is codified, with the typed glossary of tests/scripts/fixtures/glossary/, so GOOD parses.
INDEX = "---\nid: %s\nlanguage: codified-1\n---\n# ctx\n\n%s" % (OWN, FIXTURE[FIXTURE.index("## Glossary"):])
GOOD = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`."
BAD = "the queue is nice and quick"
FOREIGN = "ctx-elsewhere"
SIDE = {"awaiting-asker": "asker", "delivered": "asker", "refused": "asker"}
FIELDS = {"status": "status", "side": "turn"}


def says(step, key, word):
    step.context.setdefault("says", {})[key] = word


@handler("GivenK_A", "delegation")
def given_delegation(step):
    step.context["delegation"] = step.values[0].strip("`")
    says(step, step.names[0], "empty")


@handler("GivenK", "request line")
def given_line(step):
    step.context.setdefault("lines", {})[step.names[0]] = None
    says(step, step.names[0], "line 1")


@handler("GivenK_A", "request line")
def given_line_outcome(step):
    step.context.setdefault("lines", {})[step.names[0]] = step.values[0].strip("`")


@handler("GivenK_C", "request line")
def given_unparsed(step):
    step.context["unparsed"] = True
    says(step, step.names[0], BAD)


@handler("GivenR", "proposed in")
def given_proposed_in(step):
    says(step, step.names[0], "line 1")


@handler("GivenK", "command")
@handler("GivenK", "bounded context")
def given_bare(step):
    pass


@handler("GivenK_C", "command")
def given_command(step):
    step.context["command"] = step.text.split(" is ", 1)[1]
    says(step, "an origin", "(--")
    says(step, "a bounded context", FOREIGN)


@handler("GivenK_C", "bounded context")
def given_context(step):
    """downstream: the index lists an upstream; unmigrated: a `records/` directory at the root (design-model-check)."""
    if step.text.endswith(" unmigrated"):
        (step.repo / "records").mkdir(parents=True, exist_ok=True)
        (step.repo / "records" / "old.md").write_text("# old\n")
        says(step, step.names[0], "scripts/migrate")
        return
    index = step.repo / "spec" / "index.md"
    if not index.is_file():
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(INDEX)
    index.write_text(index.read_text() + "\n## Upstreams\n- bounded-context/ex.com/prod/up: the upstream.\n")
    step.context["downstream"] = True


@handler("GivenK", "observation")
def given_observation(step):
    step.context.setdefault("observations", set()).add(step.names[0])
    path = step.repo / ".shop" / "records" / "observations.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    head = path.read_text() if path.is_file() else "# Observations\n"
    path.write_text(head + "\n## observation/ex.com/prod/ctx/%s\nabout: %s\nby: someone\ndate: 2026-10-15\n\nSeen.\n"
                    % (step.names[0], OWN))


def prepare(step, name):
    """The request `name` as the command will find it: its side from its status, the context's own request where the
    context is downstream, its line outcomes from the Givens; and its fields before the command, for `change`."""
    path = step.repo / W.node_rel(step.context, name)
    text = path.read_text()
    status = W.field(path, "status")
    text = text.replace("turn: upstream", "turn: %s" % SIDE.get(status, "upstream"))
    if step.context.get("downstream"):
        text = text.replace("asker: other", "asker: %s" % OWN)
    outcomes = [o for o in step.context.get("lines", {}).values() if o]
    if outcomes:
        text = text.replace("## Outcomes\n", "## Outcomes\n1. %s\n" % outcomes[0])
    path.write_text(text)
    step.context["before"] = {k: W.field(path, f) for k, f in FIELDS.items()}


def run_work(step, *args):
    index = step.repo / "spec" / "index.md"
    if not index.is_file():
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(INDEX)
    elif "language: codified-1" not in index.read_text():      # world_nodes' index: the fixture glossary instead
        index.write_text(INDEX + index.read_text().partition("## Glossary\n")[2])
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("work", *args)


@handler("WhenRuns", "`work request`")
def work_request(step):
    lines = step.repo / "lines.md"
    lines.write_text((BAD if step.context.get("unparsed") else GOOD) + "\n")
    flags = step.context.get("flags", [])
    command = step.context.get("command")
    asker = FOREIGN if command == "foreign" else OWN if step.context.get("downstream") else "internal"
    args = ["request", "a request", "--from", asker, "--lines", "lines.md"]
    if command == "sourced":
        args += ["--source", "observation/ex.com/prod/ctx/obs-1", "--thread", "job-thread/ex.com/prod/t1"]
    elif command != "originless" and "--raised-for" not in flags:
        args += ["--source", "observation/ex.com/prod/ctx/obs-1"]
    if "--raised-for" in flags:
        args += ["--raised-for", step.names[0]]
    if "--delegation" in flags or step.context.get("delegation") == "empty":
        args += ["--delegation", "" if step.context.get("delegation") == "empty" else "answer any question"]
    run_work(step, *args)


@handler("WhenRuns", "`work delegate`")
def work_delegate(step):
    prepare(step, step.names[0])
    text = "" if step.context.get("delegation") == "empty" else 'The person, 2026-10-29: "answer any question"'
    run_work(step, "delegate", step.names[0], text)


@handler("WhenRuns", "`work outcome`")
@handler("WhenRuns", "`work ask`")
@handler("WhenRuns", "`work reply`")
@handler("WhenRuns", "`work turn`")
@handler("WhenRuns", "`work resolve`")
def work_request_command(step):
    name = step.names[0]
    prepare(step, name)
    word = step.term.strip("`").split()[1]
    rest = {"outcome": ["1", "accepted"], "ask": ["1", "Which queue?"], "reply": ["1", "The work queue"],
            "turn": [], "resolve": ["--line", "1", "thing#r1", "1.0.0"]}[word]
    run_work(step, word, name, *rest)


def changed(step):
    """Whether the request's status or side (the noun phrase's attribute) differs from before the command."""
    np = step.nps[-1]
    attribute, name = np.split()[1], np.split()[-1]
    now = W.field(step.repo / W.node_rel(step.context, name), FIELDS[attribute])
    return now != step.context["before"][attribute]


@handler("ThenDoes", "change")
def then_changes(step):
    assert changed(step), step.text


@handler("ThenDoesNot", "change")
def then_changes_not(step):
    assert not changed(step), step.text


@handler("GivenR", "raised for")
def given_raised_for(step):
    """A request raised for another: its `raised_for`; a request the trace says is raised for itself, nothing."""
    request, other = step.names
    if request != other:
        path = step.repo / W.node_rel(step.context, request)
        path.write_text(path.read_text().replace("\n---\n", "\nraised_for: request/ex.com/prod/ctx/%s\n---\n" % other, 1))


@handler("ThenR", "raised for")
def then_raised_for(step):
    """The request's file (the one the command wrote, where it wrote one) names the other in its `raised_for`."""
    request, other = step.names
    raised = W.field(step.repo / W.node_rel(step.context, request), "raised_for") or ""
    assert raised.endswith("/%s" % other), (step.text, raised)


@handler("GivenK_C", "observation")
def given_uncited(step):
    """uncited: the observation as its Given wrote it, which no node's `source` names."""
    step.context.setdefault("observations", set()).add(step.names[0])
