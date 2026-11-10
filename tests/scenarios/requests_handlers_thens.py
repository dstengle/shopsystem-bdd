"""The Thens of features/requests.feature (codified-2, read in the step grammar 4): what `work` refused and named,
the status and side it set or kept, the line outcome it assigned, the lines, comments, items and requests it wrote,
and what it printed, read back from the requests' files, the backlog and the run's output. A request, a line or an
item the command wrote anew is bound to the scenario's name at the first Then that names it. Each is a local of
work_queue_world's table, taken only in a scenario of features/requests.feature."""
import importlib.util
import re
import sys
from pathlib import Path

import request_text


def shared(name, file):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
Q = shared("shop_requests_world", "requests_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
HANDLERS = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("requests_handlers.py"))
ISSUES = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith(
    "requests_handlers_issues.py"))
local = W.local
FIELDS = {"status": "status", "side": "turn"}


def ours(step):
    return Q.feature(step) == "requests"


def bound(step, name):
    """The file of the request `name`; one the scenario has not written is the request the last run wrote."""
    if not W.node_rel(step.context, name):
        written = [rel for rel in W.runs(step)[-1]["changed"] if re.fullmatch(r"\.shop/requests/q\d+\.md", rel)]
        assert written, ("no request was written", step.text)
        step.context.setdefault("nodes", {})[name] = ("request", written[-1])
    return step.repo / W.node_rel(step.context, name)


def owner(np):
    """(attribute, request name) of "the status of the request r1"."""
    found = re.fullmatch(r"the (status|side) of the request (\S+)", np)
    return found.group(1), found.group(2)


def words(step):
    """What output must hold for each noun phrase of the step."""
    out, says = [], step.context.get("says", {})
    for np in step.nps:
        if re.fullmatch(r"the (status|side) of the request \S+", np):
            attribute, name = owner(np)
            out.append(W.field(bound(step, name), FIELDS[attribute]))
        elif np == "this repository":
            out.append(str(Path(step.repo).resolve()))       # its path, as git's refusal names it
        elif "`" in np:                                  # `--source`, the `--thread` option
            out += re.findall(r"`([^`]+)`", np)
        elif np.startswith("the origin"):
            out.append("origin")
        elif np.startswith("the request ") and not np.startswith("the request line"):
            out.append(bound(step, np.split()[-1]).stem)
        else:
            out += [says.get(n, n) for n in np.split() if n in step.names]
    return out


def line(step, name):
    """(request file, number) of the request line `name`."""
    request, k = step.context["line_of"][name]
    return bound(step, request), k


def does(step):
    term, np, done = step.event, step.nps[-1], step.context.get("result")
    if term == "refuse":
        assert done.returncode == 1, (step.text, done.returncode, done.stderr)
    elif term == "name":
        assert words(step), ("no words to look for", step.text)
        for word in words(step):
            assert word in done.stdout + done.stderr, (step.text, word, done.stderr)
    elif term == "set" and step.nps[0].startswith("the line outcome of "):
        outcome(step)
    elif term in ("set", "keep"):
        attribute, name = owner(step.nps[0])
        got = W.field(bound(step, name), FIELDS[attribute])
        want = step.values[0].strip("`") if term == "set" else step.context["before_of"][name][attribute]
        assert got == want, (step.text, got, want)
    elif term == "has":                                  # the request r1 has the issue i1
        url = W.field(bound(step, step.names[0]), "issue")
        assert url, step.text
        step.context.setdefault("issues", {})[step.names[1]] = url
    elif term in ("proposed in", "raised for"):
        return proposed(step) if term == "proposed in" else raised(step)
    elif term == "write" and np.startswith("the request line"):
        written_line(step)
    elif term == "write" and np.startswith("the comment"):
        assert ISSUES.held(step, step.names[0]) == 1, step.text
    elif term == "write" and np.startswith("the item"):
        B.bind_written(step, step.names[0])
    else:
        return False


def outcome(step):
    """`work` sets the line outcome of the request line r2 to `v`: the request's `## Outcomes` entry for the line."""
    path, k = line(step, step.names[0])
    got = request_text.entries(path.read_text(), "Outcomes")
    assert "%d. %s" % (k, step.values[0].strip("`")) in got, (step.text, got)


def proposed(step):
    """The request line is a line of the request; a line no Given placed is its first."""
    step.context.setdefault("line_of", {}).setdefault(step.names[0], (step.names[1], 1))
    path, k = line(step, step.names[0])
    got = request_text.entries(path.read_text(), "Lines")
    assert any(e.startswith("%d. " % k) for e in got), (step.text, got)


def raised(step):
    request, other = step.names
    got = W.field(bound(step, request), "raised_for") or ""
    assert got.endswith("/%s" % bound(step, other).stem), (step.text, got)


def written_line(step):
    """The request's `## Lines` gained an entry in the last run; the name is bound to its number."""
    name = next(n for n, (kind, _) in step.context["nodes"].items() if kind == "request")
    path = bound(step, name)
    rel = path.relative_to(step.repo).as_posix()
    had = request_text.entries(W.git(step.repo, "show", "%s:%s" % (step.context["head"], rel)), "Lines")
    now = request_text.entries(path.read_text(), "Lines")
    assert len(now) == len(had) + 1, (step.text, had, now)
    step.context.setdefault("line_of", {})[step.names[0]] = (name, int(now[-1].split(".", 1)[0]))


@local("ThenDoes")
def then_does(step):
    if not ours(step):
        return False
    return does(step)


@local("ThenPrints")
def then_prints(step):
    if not ours(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    for word in words(step):
        assert word in done.stdout, (step.text, word, done.stdout)


@local("ThenPrintsNot")
def then_prints_not(step):
    """`work` does not print a request: no `q<n>` in its output."""
    if not ours(step) or step.nps != ["a request"]:
        return False
    done = step.context["result"]
    assert not re.search(r"\bq\d+\b", done.stdout), (step.text, done.stdout)


@local("ThenK_A", "request")
def then_request_is(step):
    if not ours(step):
        return False
    bound(step, step.names[0])
    return False


@local("ThenK_A", "item")
def then_item_is(step):
    if not ours(step):
        return False
    B.bind_written(step, step.names[0])
    return False
