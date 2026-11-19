"""The worlds of checking's general lines on rules and their catalogue (b370), rows design_model_check_worlds' TABLE
takes first: a capability that violates a rule whose severity is `error` (v15a) or only one whose severity is
`warning` (a line of example data, w_example), and the rule catalogue a context keeps (`CATALOGUE`, one entry of
v15a with its purpose and the item it came by): a requirement that names a rule it has no entry of."""
import importlib.util
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C = _sibling("design_model_check_handlers_conditions.py", "shop_design_model_check_handlers_conditions")
C2 = _sibling("codified2_world.py", "shop_codified2_world")
UNCATALOGUED = "v_zz9"
NAMING = ("While a file violates `%s`, when a session writes the file, `work` shall print the file." % UNCATALOGUED)
CATALOGUE = ("# Rule catalogue\n\nSince: and Changed: name items of `%s`.\n\n## v15a\n\na requirement has no id\n\n"
             "- Purpose: every line can be cited by its id.\n- Since: b1\n" % H.PATH)
EXEMPLIFIED = "When a session writes the `notes.txt` file, `work` shall print the file."


class As:
    """The step as a codified-1 condition's Given saw it: `the thing <name> is <word>`."""

    def __init__(self, step, name, word):
        self._step, self.names, self.text = step, [name], "the thing %s is %s" % (name, word)

    def __getattr__(self, attr):
        return getattr(self._step, attr)


def erring(step):
    """The capability c1 numbers no line: v15a, an error."""
    C.capability(As(step, step.context.get("kinds", {}).get("capability", ["c1"])[0], "unnumbered"))


def warned(step):
    """A line of example data (`notes.txt`, a parameter) and nothing else wrong: w_example, a warning, and no
    error."""
    C2.context(step.repo, H.PATH, [EXEMPLIFIED])
    H.write(step.repo, "features/thing.feature", H.feature("thing", "@r1"))



def uncatalogued(step):
    """r1 a line that names `v_zz9` (the spec pack imported), in a context whose rule catalogue has no entry of it."""
    C2.context(step.repo, H.PATH, [NAMING])
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [cli, spec]", 1))
    H.write(step.repo, "features/thing.feature", H.feature("thing", "@r1"))
    H.write(step.repo, "grammar/rules.md", CATALOGUE)


ROWS = [
    (("rule is `error`", "capability violate rule"), erring, {"r1": "v15a"}),
    (("rule has no catalogue entry", "requirement use rule"), uncatalogued, {"r2": UNCATALOGUED}),
    (("rule is `warning`", "capability violate rule", "no rule is `error`"), warned, {"r1": "w_example"}),
]
