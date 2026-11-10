"""The Givens of features/requests.feature (codified-2, read in the step grammar 4): a request kept as `q<k>.md` on
an issue of its own, its status, side and lines; the comments on its issue, read by requests_world.put_comments
before the run; this bounded context's upstream entries, its own asker, and a repository that rejects every commit.
Each is a local of work_queue_world's table (test_requests.py binds with `bind_all`), taken only in a scenario of
features/requests.feature; any other scenario's step goes on to its own handler."""
import importlib.util
import re
import sys
from pathlib import Path


def shared(name, file):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
Q = shared("shop_requests_world", "requests_world.py")
NODES = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("world_nodes.py"))
local = W.local
OTHER = "bounded-context/ex.com/prod/other"
FOREIGN = "ctx-elsewhere"
BAD = "the queue is nice and quick"


def says(step, key, word):
    step.context.setdefault("says", {})[key] = word


def ours(step):
    return Q.feature(step) == "requests"


def request(step, name, status="open"):
    """The request `name`, written as the next `q<k>.md` on the issue `ex/ctx#<k>` where no Given wrote it yet."""
    nodes = step.context.setdefault("nodes", {})
    if name not in nodes:
        k = 1 + sum(1 for kind, _ in nodes.values() if kind == "request")
        rel = ".shop/requests/q%d.md" % k
        NODES.index(step.repo)
        NODES.write(step.repo, rel, NODES.node_text("request", "q%d" % k, status, None))
        nodes[name] = ("request", rel)
        Q.with_issue(step, step.repo / rel, "https://github.com/%s/issues/%d" % (Q.OWN_REPO, k))
        says(step, name, "q%d" % k)
    return step.repo / nodes[name][1]


def set_field(path, key, value):
    """The request's frontmatter field `key` set to `value`, added after its `kind` where it has none."""
    text = path.read_text()
    if re.search(r"^%s: " % key, text, re.MULTILINE):
        text = re.sub(r"^%s: .*$" % key, "%s: %s" % (key, value), text, count=1, flags=re.MULTILINE)
    else:
        text = text.replace("\nkind: request\n", "\nkind: request\n%s: %s\n" % (key, value), 1)
    path.write_text(text)


def upstream(step, hosted=True):
    """This bounded context lists the upstream `ex.com/prod/up` under `## Upstreams`, with its GitHub repository or
    none."""
    index = step.repo / "spec" / "index.md"
    index.parent.mkdir(parents=True, exist_ok=True)
    handlers = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith(
        "requests_handlers.py"))
    index.write_text(handlers.INDEX + "\n## Upstreams\n- %s: the upstream%s.\n" % (Q.UP, ", github: ex/up" if hosted else ""))
    step.context["downstream"] = True


def propose(step, line, name):
    """The request line `line` is the next line of the request `name`."""
    path = request(step, name)
    line_of = step.context.setdefault("line_of", {})
    k = 1 + sum(1 for r, _ in line_of.values() if r == name)
    line_of[line] = (name, k)
    step.context.setdefault("lines", {}).setdefault(line, None)
    if k > 1:
        path.write_text(path.read_text().replace("\n\n## Outcomes", "\n%d. line %d\n\n## Outcomes" % (k, k), 1))
    says(step, line, "line %d" % k)


@local("GivenK", "request")
def given_request(step):
    if not ours(step):
        return False
    request(step, step.names[0])


@local("GivenK", "comment")
def given_comment(step):
    if not ours(step):
        return False
    Q.comment(step, step.names[0])


@local("GivenK", "commit")
@local("GivenK", "upstream entry")
def given_bare(step):
    """A commit or an upstream entry: what the condition that names it says is all the scenario keeps of it."""
    return None if ours(step) else False


@local("GivenK_A", "request")
def given_request_is(step):
    """`the request r1 is v` sets its status; `is not v` keeps another; `no request is v` writes none."""
    if not ours(step):
        return False
    if not step.names:
        return None
    path, value = request(step, step.names[0]), step.values[0].strip("`")
    if " is not " not in step.text:
        set_field(path, "status", value)
    elif W.field(path, "status") == value:
        set_field(path, "status", "open" if value != "open" else "awaiting-asker")


@local("GivenK_A", "request line")
def given_line_is(step):
    if not ours(step):
        return False
    step.context.setdefault("lines", {})[step.names[0]] = None if " is not " in step.text else step.values[0].strip("`")


def has(step):
    subject, np = step.subject, step.nps[-1]
    if subject == "this command":                       # no origin
        step.context["no_origin"] = True
    elif subject.startswith("the bounded context"):    # no host
        upstream(step, hosted=False)
        step.context["unhosted"] = True
        says(step, step.names[0], Q.UP)
    elif subject.startswith("the comment"):
        Q.comment(step, step.names[0])["body"] = "unreadable" if np == "no field block" else \
            step.context.get("blocks", {}).get(step.names[1], "readable")
    elif subject.startswith("the request line"):       # no logical form
        step.context["unparsed"] = True
        says(step, step.names[0], BAD)


def holds(step):
    if step.subject == "this bounded context":         # an upstream entry
        upstream(step)
    elif step.subject.startswith("the field block"):   # a foreign entry
        step.context.setdefault("blocks", {})[step.names[0]] = step.names[1]


@local("GivenDoes")
def given_does(step):
    """The conditions of a request, a comment, a line, this bounded context and this repository (requests)."""
    if not ours(step):
        return False
    term = step.event
    if term in ("proposed in", "block") and not step.subject.startswith("no "):
        propose(step, *step.names)
    elif term == "on":
        Q.comment(step, step.names[0])["request"] = step.names[1]
        request(step, step.names[1])
    elif term == "has":
        has(step)
    elif term == "holds":
        holds(step)
    elif term in ("address", "originate"):
        set_field(request(step, step.names[0]), "upstream" if term == "address" else "asker", Q.OWN)
    elif term == "reject":
        step.context.setdefault("before_run", []).append(next(m for m in list(sys.modules.values()) if getattr(
            m, "__file__", "").endswith("requests_handlers_commit.py")).uncommittable)
    elif term not in ("block", "lack", "has"):
        return False


@local("GivenDoesNot")
def given_does_not(step):
    if not ours(step):
        return False
    term = step.event
    if term == "address":
        set_field(request(step, step.names[0]), "upstream", Q.UP)
    elif term == "originate":
        set_field(request(step, step.names[0]), "asker", OTHER)
    elif term == "identify":
        step.context["from"] = FOREIGN
        says(step, step.names[0], FOREIGN)
    elif term != "holds":                               # a request that does not hold a comment: as written
        return False
