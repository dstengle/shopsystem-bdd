"""Handlers of features/requests.feature (design §14.3): the request commands of `work` run on the requests the Givens
wrote (requests_handlers_givens), each `q<k>.md` on its issue, in a git repository, with the lines, outcomes and
origins the Givens keep in the context; and the request lines, conditions and `change` of features/intake.feature.

A request's `turn` follows its status before a command runs (the asker's for `awaiting-asker`, `delivered` and
`refused`), since a request is written in the upstream's turn. `ThenDoes` with `change` (intake) compares a
request's status or side with what it was before the command ran."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def shared(name="shop_work_queue_world", file="work_queue_world.py"):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared()
Q = shared("shop_requests_world", "requests_world.py")
OWN = "bounded-context/ex.com/prod/ctx"
FIXTURE = (Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "glossary" / "spec" / "index.md").read_text()
# The context's index is codified, with the typed glossary of tests/scripts/fixtures/glossary/, so GOOD parses.
HEAD = "---\nid: %s\nlanguage: codified-2\nimports: [cli]\n---\n" % OWN
INDEX = HEAD + "# ctx\n\n%s" % FIXTURE[FIXTURE.index("## Glossary"):]
GOOD = "While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to `started`."
BAD = "the queue is nice and quick"
THING = ("---\nid: capability/ex.com/prod/ctx/thing\ntitle: Thing\nnarrator: a client\ngroup: service\n"
         "language: codified-2\nrests_on: []\nretired: []\n---\n\n# Thing\n\n## Purpose\nSomething.\n\n## Behaviour\n")
SIDE = {"awaiting-asker": "asker", "delivered": "asker", "refused": "asker"}
FIELDS = {"status": "status", "side": "turn"}


def says(step, key, word):
    step.context.setdefault("says", {})[key] = word


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


@handler("GivenK_C", "bounded context")
def given_context(step):
    """The packs a bounded context imports, unmigrated (a `records/` directory at the root), and any other word (sound):
    an index that lists an upstream (design-model-check)."""
    word = step.text.rsplit(" is ", 1)[1]
    packs = shared("shop_design_model_check_handlers_packs", "design_model_check_handlers_packs.py")
    if word in packs.CONTEXT:       # the packs it imports (design-model-check)
        return packs.bounded_context(step, word)
    if step.text.endswith(" unmigrated"):
        (step.repo / "records").mkdir(parents=True, exist_ok=True)
        (step.repo / "records" / "old.md").write_text("# old\n")
        says(step, step.names[0], "scripts/migrate")
        return
    index = step.repo / "spec" / "index.md"         # any other word (sound): the index, which lists an upstream
    if not index.is_file():
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(INDEX)
    index.write_text(index.read_text() + "\n## Upstreams\n- bounded-context/ex.com/prod/up: the upstream, github: ex/up.\n")


@handler("GivenK", "observation")
def given_observation(step):
    step.context.setdefault("observations", set()).add(step.names[0])
    path = step.repo / ".shop" / "records" / "observations.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    head = path.read_text() if path.is_file() else "# Observations\n"
    path.write_text(head + "\n## observation/ex.com/prod/ctx/%s\nabout: %s\nby: someone\ndate: 2026-10-15\n\nSeen.\n"
                    % (step.names[0], OWN))


@handler("GivenK_C", "observation")
def given_uncited(step):
    """uncited (design-model-check, codified-1): the observation as its Given wrote it, which no node's `source`
    names."""
    step.context.setdefault("observations", set()).add(step.names[0])


def path_of(step, name):
    """The file of the request `name`, written by requests_handlers_givens where no Given wrote it."""
    return givens().request(step, name)


def givens():
    return next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith(
        "requests_handlers_givens.py"))


def prepare(step, name):
    """The request `name` as the command will find it: its side from its status (a request is written in the
    upstream's turn), the line outcomes the Givens gave its lines; and its status and side before the command, for
    `keep` and `change`. Returns its `q<n>`."""
    path = path_of(step, name)
    text = path.read_text()
    status = W.field(path, "status")
    text = text.replace("turn: upstream", "turn: %s" % SIDE.get(status, "upstream"))
    lines, outcomes = step.context.get("lines", {}), []
    for line, (request, k) in sorted(step.context.get("line_of", {}).items(), key=lambda kv: kv[1][1]):
        if request == name and lines.get(line):
            outcomes.append("%d. %s\n" % (k, lines[line]))
    text = text.replace("## Outcomes\n", "## Outcomes\n" + "".join(outcomes), 1)
    path.write_text(text)
    step.context["before"] = {k: W.field(path, f) for k, f in FIELDS.items()}
    step.context.setdefault("before_of", {})[name] = step.context["before"]
    return path.stem


def prepare_all(step):
    """Every request the Givens wrote prepared, and the comments put on their issues (a sync or a watch)."""
    for name, (kind, _) in list(step.context.get("nodes", {}).items()):
        if kind == "request":
            prepare(step, name)
    Q.put_comments(step, path_of)


def run_work(step, *args):
    index = step.repo / "spec" / "index.md"
    if not index.is_file():
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(INDEX)
    elif not index.read_text().startswith(HEAD):      # world_nodes' index: the fixture glossary instead
        index.write_text(INDEX + index.read_text().partition("## Glossary\n")[2])
    step.context["head"] = W.init(step.repo)
    Q.hosted(step.repo)
    for before in step.context.get("before_run", []):
        before(step)
    step.context["result"] = step.run("work", *args, env=Q.env(step))


def options(step):
    """({option: its argument's words or None} the When gives, {option the When says it does not give}), each option
    without its backticks."""
    given = {code.strip("`"): arg for code, arg in getattr(step, "options", [])}
    return given, {code.strip("`") for code in getattr(step, "without", [])}


@handler("WhenRuns", "`work request`")
def work_request(step):
    """`work request` with the options the When gives (codified-2): `--from` the asker a Given made (a text that does
    not identify this bounded context), `--raised-for` set to a request, `--to` set to the upstream a Given gave no
    GitHub repository, `--source` with `--thread` or `--raised-for`; none of `--source`, `--thread` and `--raised-for`
    where the When says so; else a job-thread to an upstream (where this bounded context has one), or an observation."""
    given, without = options(step)
    asker = step.context.get("from") or (OWN if step.context.get("downstream") else "internal")
    args = ["request", "a request", "--from", asker, "--ask", "I need to do something like this"]
    if given.get("--raised-for"):
        args += ["--raised-for", path_of(step, step.names[0]).stem]
    elif "--source" in given:
        args += ["--source", "observation/ex.com/prod/ctx/obs-1"]
        args += ["--thread", "job-thread/ex.com/prod/t1"] if "--thread" in given else ["--raised-for", "q9"]
    elif {"--source", "--thread", "--raised-for"} <= without:
        pass
    elif step.context.get("downstream"):
        args += ["--thread", "job-thread/ex.com/prod/t1"] + (["--to", Q.UP] if "--to" in given else [])
    else:
        args += ["--source", "observation/ex.com/prod/ctx/obs-1"]
    run_work(step, *args)


@handler("WhenRuns", "`work outcome`")
@handler("WhenRuns", "`work ask`")
@handler("WhenRuns", "`work reply`")
@handler("WhenRuns", "`work turn`")
@handler("WhenRuns", "`work resolve`")
def work_request_command(step):
    name = step.names[-1]
    q = prepare(step, name)
    word = step.term.strip("`").split()[1]
    if word == "outcome":     # an accepted line parses here and names the capability it goes into
        path = path_of(step, name)
        path.write_text(path.read_text().replace("1. line 1\n", "1. %s\n" % GOOD, 1))
        cap = step.repo / "spec" / "capabilities" / "thing.md"
        cap.parent.mkdir(parents=True, exist_ok=True)
        cap.write_text(THING)
    rest = {"outcome": ["1", "accepted", "--into", "thing"], "ask": ["1", "Which queue?"], "reply": ["1", "The work queue"],
            "turn": [], "resolve": ["--line", "1", "thing#r1", "1.0.0"]}[word]
    run_work(step, word, q, *rest)


@handler("WhenRuns", "`work list`")
@handler("WhenRuns", "`work show`")
def work_read(step):
    """`work list` and `work show` on a request, on the requests the Givens wrote."""
    for name in step.names:
        path_of(step, name)
    prepare_all(step)
    words = step.term.strip("`").split()[1:]
    run_work(step, *words, *[path_of(step, n).stem for n in step.names])


@W.local("WhenRuns")
def work_outcome_accepted(step):
    """`work outcome accepted` on a request line of features/requests.feature (codified-2), line k of the request a Given
    proposed it in (a request of its own where none did): in this context's grammar, the line GOOD, which goes into the
    capability `thing`, or the words a Given said a line that does not conform has. Any other run goes on to its
    handler (intake's `work outcome accepted` among them)."""
    if step.term != "`work outcome accepted`" or not givens().ours(step):
        return False
    line = step.names[-1]
    if line not in step.context.get("line_of", {}):
        givens().propose(step, line, "the request of %s" % line)
    name, k = step.context["line_of"][line]
    path = path_of(step, name)
    words = BAD if step.context.get("unparsed") else GOOD
    path.write_text(path.read_text().replace("%d. line %d\n" % (k, k), "%d. %s\n" % (k, words), 1))
    step.context.setdefault("says", {})[line] = "line %d" % k
    cap = step.repo / "spec" / "capabilities" / "thing.md"
    cap.parent.mkdir(parents=True, exist_ok=True)
    cap.write_text(THING)
    run_work(step, "outcome", prepare(step, name), str(k), "accepted", "--into", "thing")


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
    """A request's status or side; a file of another feature's Givens (analysis-tools' dependency file) world_cli's."""
    if step.nps[-1].split()[1] not in FIELDS:
        return shared("shop_world_cli", "world_cli.py").files_unchanged(step)
    assert not changed(step), step.text
