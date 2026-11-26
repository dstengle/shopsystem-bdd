"""scenarios' requests with their parameters in a generated feature (b418), feature_file_tools_capability's world and
Thens of them: a requirement that uses `param-of` is the construct catalogue's example of it, and one that governs an
operation that makes a referent the example of `request-params` (the decisions service's enter, whose design-decision
is its `done →` outcome's and named by no parameter), each the one requirement of the capability c1 in the
catalogue's request context (grammar/corpus/constructs/request/: a domain model, its vocabulary and the request
pack) (`prepare`). The Thens read the feature `features generate` wrote: a given step and the when step that mention
one code (the value in use, made up, given to the other thing and to the request), and the thing the operation makes
brought in by the when step ("When the person enters a design-decision d1 ...") and by no given step (`then`); and a
requirement that uses `reply-trigger` the example of it, every instance its steps mention brought in by a given or a
when step (b724: `unbrought`), in g1 beside g2, the line whose response makes the request (`response-request`) and
whose doer is the requester (b728); with a requester, r1 that trigger with a response by another agent (`REPLIED`), a
given step naming the requester (`REQUESTER`)."""
import re
import shutil
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
CONTEXT = PLUGIN / "grammar" / "corpus" / "constructs" / "request" / "spec"
KINDS = ("operation", "when step", "requester")
GIVEN = re.compile(r"^    (?:Given|And) (.*)$")
REPLIED = ("When the registry completes the request to publish a design-decision, the registry shall notify the person "
           "of the design-decision.")
REQUESTER = "the decisions service"     # the doer of the response-request example's response


def example(code):
    text = (PLUGIN / "grammar" / "constructs.md").read_text()
    return re.search(r"^## %s\n.*?```construct\n(.*?)\n" % re.escape(code), text, re.DOTALL | re.MULTILINE).group(1)


def construct(w, kind):
    """The construct whose example r1 is: `param-of` when a Given says r1 uses it, `request-params` when r1 governs an
    operation that makes a referent, else None."""
    used = {o for v, a, o, pos in w["facts"] if v == "use" and pos and kind(w, a) == "requirement"}
    if "`param-of`" in used:
        return "param-of"
    if "`reply-trigger`" in used:     # b724: the thing the replied request is on brought in
        return "reply-trigger"
    makes = {a for v, a, o, pos in w["facts"] if v == "make" and pos and kind(w, a) == "operation"}
    governs = any(v == "govern" and pos and o in makes for v, _, o, pos in w["facts"])
    return "request-params" if governs else None


def prepare(step, w, kind, name, path):
    """The capability `name` whose r1 is the example of the construct the Givens say; True when one was written."""
    code = construct(w, kind)
    if code is None:
        return False
    lines = "### [g1] %s\n- [r1] %s\n" % (code, example(code))
    if code == "reply-trigger":     # the line that makes the request the reply is on, which gives its requester (b728)
        if any(v == "has" and pos and kind(w, o) == "requester" for v, _, o, pos in w["facts"]):
            lines, w["requester"] = "### [g1] %s\n- [r1] %s\n" % (code, REPLIED), REQUESTER
        lines += "\n### [g2] requesting\n- [r2] %s\n" % example("response-request")
    shutil.copytree(CONTEXT, step.repo / "spec", dirs_exist_ok=True)
    cap = ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: the person\ngroup: service\narea: decisions\n"
           "specifies: service decisions\nlanguage: codified-2\nretired: []\n---\n\n# %s\n\n## Purpose\n\nSomething."
           "\n\n## Behaviour\n\n%s" % (path, name, name, name, lines))
    (step.repo / "spec" / "capabilities").mkdir(parents=True, exist_ok=True)
    (step.repo / "spec" / "capabilities" / ("%s.md" % name)).write_text(cap)
    w["request"], w["code"] = name, code
    return True


def mine(w):
    return "request" in w


def steps(step, w):
    """(the given steps, the when steps) of the feature's first scenario, g1's."""
    text = (step.repo / "features" / ("%s.feature" % w["request"])).read_text()
    givens, whens, now = [], [], None
    for line in text.split("\n  Scenario")[1].splitlines():
        found = re.match(r"^    (Given|When|Then|And|But) (.*)$", line)
        if found:
            now = found.group(1) if found.group(1) in ("Given", "When", "Then") else now
            (givens if now == "Given" else whens if now == "When" else []).append(found.group(2))
    return givens, whens


def made(whens):
    """(kind, name) of the thing the when step brings in ("a design-decision d1"), or None."""
    found = re.search(r"\ban? ([a-z][a-z -]*?) ([a-z]\d+)\b", " ".join(whens))
    return found.groups() if found else None


def unbrought(givens, whens):
    """Each instance a step mentions ("the design-decision d1") that no given step and no when step brings in ("a
    design-decision d1"), a code's words left out."""
    brought = {m for line in givens + whens for m in re.findall(r"\ban? [a-z][a-z -]*? ([a-z]\d+)\b", line)}
    named = {m for line in givens + whens for m in re.findall(r"(?<![\w@-])([a-z]\d+)\b", re.sub(r"`[^`]*`", "", line))}
    return named - brought


def codes(lines):
    return {c for line in lines for c in re.findall(r"`[^`]+`", line)}


def then(step, w, pos=True):
    """The Thens of the request's feature: kept (or not) a given step or the when step, what each mentions or
    introduces, and the instance of the referent the operation makes."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    givens, whens = steps(step, w)
    np = step.nps[0] if step.nps else ""
    introduced = made(whens)
    if not pos and w.get("code") == "reply-trigger":     # every instance a step mentions brought in (b724)
        assert givens and whens and not unbrought(givens, whens), (unbrought(givens, whens), givens, whens)
    elif not pos:     # the given step that would bring in what the operation makes
        assert introduced, ("the when step brings in nothing", whens)
        kind, name = introduced
        assert "a %s %s" % (kind, name) not in givens and "an %s %s" % (kind, name) not in givens, givens
    elif np.startswith("the requester") and step.term == "mention":     # the doer of r2's response (b728)
        assert "%s publishes the design-decision" % w["requester"] in " ".join(givens), (givens, whens)
    elif step.subject.startswith("the given step") and step.term == "mention":
        assert codes(givens) & codes(whens), (givens, whens)
    elif step.subject.startswith("the when step") and step.term == "mention":
        assert codes(whens) & codes(givens), (givens, whens)
    elif step.term in ("introduce", "has"):
        assert introduced, ("the when step brings in nothing", whens)
    elif np.startswith("the given step"):
        assert givens, "no given step"
    elif np.startswith("the when step"):
        assert whens, "no when step"
    else:
        return False
    return None
