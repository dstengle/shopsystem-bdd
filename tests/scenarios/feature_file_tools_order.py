"""feature-file-tools' Thens of the order of a scenario's Thens (r111, b268), read off the feature `features generate`
wrote of the example data's capability: the act a requirement's response brings a referent in by (the first Then said
by a tool, "`shelf` writes the book b1"), the referent (the instance it names last), and the descriptions of the
referent (each other Then that names it, "the status of the book b1 is `shelved`"), each by its place."""
import re

THEN = re.compile(r"^\s*(?:Then|And|But) (.*)$")
NAME = re.compile(r"\b[a-z]+\d+\b")


def thens(step):
    """The Then lines of the one scenario of the example data's feature, in order."""
    text = (step.repo / "features" / "shelf.feature").read_text()
    lines = text.split("\n")
    when = next(n for n, line in enumerate(lines) if line.strip().startswith("When "))
    return [m.group(1) for line in lines[when + 1:] if (m := THEN.match(line))]


def read(step, w):
    """{"act": its place, "referent": its name, "descriptions": [their places]}, kept for the scenario."""
    if "order" not in w:
        lines = thens(step)
        act = next(n for n, line in enumerate(lines) if line.startswith("`") and NAME.search(line))
        referent = NAME.findall(lines[act])[-1]
        descriptions = [n for n, line in enumerate(lines) if n != act and referent in NAME.findall(line)]
        w["order"] = {"act": act, "referent": referent, "descriptions": descriptions, "lines": lines}
    return w["order"]


def mine(w, step):
    """True for a step of r111's world: one that names a description, an act or a referent."""
    return any(w["kinds"].get(n) in ("description", "act", "referent") for n in step.names)


def has(step, w):
    """`the referent r2 has the description d1`: the referent's descriptions, of which there is one at least."""
    order = read(step, w)
    assert order["descriptions"], "no Then of the feature names %s: %s" % (order["referent"], order["lines"])


def follows(step, w):
    """`the description d1 follows the act a1`: every description of the referent after the act."""
    order = read(step, w)
    early = [order["lines"][n] for n in order["descriptions"] if n < order["act"]]
    assert not early, "before %r: %s" % (order["lines"][order["act"]], early)


def writes(step, w):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    has(step, w)


def writes_not(step, w):
    """`features does not write the description d2`: no description of the referent precedes the act."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    follows(step, w)
