"""design-model-check's worlds of a value in use (b418, `param-of`), rows design_model_check_worlds' TABLE takes before
the language service's: a request whose parameter's value is another thing's value of the attribute the parameter
names, in the construct catalogue's request context (grammar/corpus/constructs/request/: a domain model, its
vocabulary and the request pack), r1 the line here; beside it r2, a line of the same request with a code of the value
that forbids what r1 obliges (an L1: the code and the value in use are one value of one request)."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTEXT = ROOT / "grammar" / "corpus" / "constructs" / "request" / "spec"
PATH = "ex.com/prod/ctx"
IN_USE = ("If the person enters a design-decision with the title of another design-decision, then the decisions "
          "service shall refuse the request.")
CODED = ("If the person enters a design-decision with the title `t1`, then the decisions service shall not refuse the "
         "request.")


def capability(lines):
    body = "\n".join("### [g%d] line %d\n- [r%d] %s" % (k, k, k, line) for k, line in enumerate(lines, 1))
    return ("---\nid: capability/%s/thing\ntitle: thing\nnarrator: the person\ngroup: service\narea: decisions\n"
            "specifies: service decisions\nlanguage: codified-2\nretired: []\n---\n\n# thing\n\n## Purpose\n\n"
            "Something.\n\n## Behaviour\n\n%s\n" % (PATH, body))


def line(*texts):
    """A builder: the request context with the capability `thing` of `texts` as r1 (r2)."""
    def build(step):
        spec = step.repo / "spec"
        shutil.copytree(CONTEXT, spec, dirs_exist_ok=True)
        (spec / "capabilities").mkdir(exist_ok=True)
        (spec / "capabilities" / "thing.md").write_text(capability(list(texts)))
    return build


ROWS = [
    (("requirement use `param-of`", "requirement oblige act", "requirement forbid act"), line(IN_USE, CODED), {}),
    (("requirement use `param-of`",), line(IN_USE), {}),
]
