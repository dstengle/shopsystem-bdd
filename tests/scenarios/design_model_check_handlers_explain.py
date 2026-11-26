"""Handlers of design-model-check's `spec explain` (the CNL 4 design, I13b): the command run on the requirement the
When names, by the id a Given gave it (thing#r1 of a codified-2 world when no Given wrote a spec), with the id kept in `says` so that
a Then naming the requirement looks for the id in the output; a consequence it prints under "which also means:" with
its premise (b742)."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


W = _sibling("work_queue_world.py", "shop_work_queue_world")
H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C2 = _sibling("codified2_world.py", "shop_codified2_world")
# thing#r1 of the world when no Given wrote a spec: a codified-2 one, which `spec explain` reads
ASKED = "When the person runs `work start`, `work` shall exit successfully."


@handler("WhenRuns", "`spec explain`")
def model_explain(step):
    H.built(step)
    if not (step.repo / "spec" / "index.md").exists():
        C2.context(step.repo, H.PATH, [ASKED])
    name = step.names[0]
    ident = step.context.get("ids", {}).get(name, "thing#r1")
    H.says(step, name, ident)
    H.run_model(step, "explain", ident)


@handler("ThenK_C", "requirement")
def printed_refusing(step):
    """`the requirement r2 is refusing`: the line `spec explain` printed under the requirement's id says that the tool
    shall refuse a command."""
    word, ident = step.text.rsplit(" is ", 1)[1], step.context["says"][step.names[0]]
    assert word == "refusing", "no requirement condition %r as a Then" % word
    lines = [line for line in step.context["result"].stdout.splitlines() if line.strip().startswith(ident + "  ")]
    assert lines and any(" shall refuse " in line for line in lines), (ident, step.context["result"].stdout)


@W.local("ThenPrints")
def printed_consequence(step):
    """`the language service returns the consequence c1` (b742): `spec explain` exits 0 and a line under "which also
    means:" holds the words the world said the consequence by, with the premise the requirement r1."""
    if not step.nps or not step.nps[0].startswith("the consequence ") or "r1" not in step.context.get("says", {}):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    means = done.stdout.partition("which also means:\n")[2].split("\n")
    wanted = (step.context["says"][step.names[0]], "(by %s)" % step.context["says"]["r1"])
    assert any(line.startswith("  ") and all(w in line for w in wanted) for line in means), (wanted, done.stdout)
