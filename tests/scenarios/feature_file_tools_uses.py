"""feature-file-tools' capability of one construct (b274): a requirement r1 that uses a construct a Given names
(`the requirement r1 uses `holds-exactly``, `the precondition p1 uses `nothing``) is the construct catalogue's example
of it, the one requirement of the capability c1 in the catalogue's context `grammar/corpus/constructs/` (`prepare`);
"the step s2 uses `not-condition`" holds when a step of the feature `features generate` wrote reads, in the step
grammar 4, as a tree that uses the construct as `model constructs` tells it (`uses`)."""
import re
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
CODES = ("holds-exactly", "nothing")


def construct(w):
    """The code of the construct a Given says the requirement or its precondition uses, or None."""
    used = [o.strip("`") for v, _, o, pos in w["facts"] if v == "use" and pos and isinstance(o, str)]
    return next((c for c in used if c in CODES), None)


def example(code):
    text = (PLUGIN / "grammar" / "constructs.md").read_text()
    return re.search(r"^## %s\n.*?```construct\n(.*?)\n" % re.escape(code), text, re.DOTALL | re.MULTILINE).group(1)


def prepare(step, w, write, name, path):
    """The capability `name` whose r1 is the catalogue's example of the construct; True when one was written."""
    code = construct(w)
    if code is None:
        return False
    cap = ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-2\n"
           "rests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n### [g1] %s\n"
           "- [r1] %s\n\n## Not yet\n" % (path, name, name, name, code, example(code)))
    write(step.repo / "spec" / "index.md", (PLUGIN / "grammar" / "corpus" / "constructs" / "spec" / "index.md")
          .read_text())
    write(step.repo / "spec" / "capabilities" / ("%s.md" % name), cap)
    return True


def uses(step, name):
    """Assert that a step of the feature of `name` uses the construct the Then names."""
    if str(PLUGIN / "scripts") not in sys.path:
        sys.path.insert(0, str(PLUGIN / "scripts"))
    import model_constructs
    import spec_gf
    import spec_rgl_steps
    from model_constructs_table import CONSTRUCTS
    code = step.nps[0].strip("`")
    entry = next(e for e in CONSTRUCTS if e["code"] == code)
    text = (step.repo / "features" / ("%s.feature" % name)).read_text()
    lines = re.findall(r"^\s*(?:Given|When|Then|And) (.*)$", text, re.MULTILINE)
    frames = model_constructs.roles(spec_rgl_steps.load(step.repo)[0])
    found = [line for line in lines for t in spec_rgl_steps.trees(step.repo, line)
             if model_constructs.uses(entry, str(spec_gf.expr(t)), frames)]
    assert found, "no step uses %s:\n%s" % (code, text)
