"""The worlds of checking's general lines on rules and their catalogue (b370), rows design_model_check_worlds' TABLE
takes first: a capability that violates a rule whose severity is `error` (v15a) or only one whose severity is
`warning` (a line of example data, w_example), and the rule catalogue a context keeps (`CATALOGUE`, one entry of
v15a with its purpose and the item it came by): a requirement that names a rule it has no entry of; that entry with
no purpose, with no item, or with the item b1 of the context's backlog, whose status is `ready`."""
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
ENTRY = "grammar/rules.md#v15a"
ITEM = "item/%s/b1" % H.PATH


def catalogue(purpose=True, since=True):
    """The rule catalogue of one entry, v15a."""
    return ("# Rule catalogue\n\nSince: and Changed: name items of `%s`.\n\n## v15a\n\na requirement has no id\n\n%s%s"
            % (H.PATH, "- Purpose: every line can be cited by its id.\n" if purpose else "",
               "- Since: b1\n" if since else ""))


CATALOGUE = catalogue()
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
    clean(step, EXEMPLIFIED)



def clean(step, line):
    """The smallest codified-2 world, its r1 `line` with its scenario: nothing else violates a rule."""
    C2.context(step.repo, H.PATH, [line])
    H.write(step.repo, "features/thing.feature", H.feature("thing", "@r1"))


def uncatalogued(step):
    """r1 a line that names `v_zz9` (the spec pack imported), in a context whose rule catalogue has no entry of it."""
    clean(step, NAMING)
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [cli, spec]", 1))
    H.write(step.repo, "grammar/rules.md", CATALOGUE)



def entry(**kwargs):
    """A builder: the context's rule catalogue, its entry v15a with no purpose or with no item."""
    def build(step):
        clean(step, C2.LINES["plural"][0])
        H.write(step.repo, "grammar/rules.md", catalogue(**kwargs))
    return build


def undelivered(step):
    """The entry v15a came by the item b1, whose status in the context's backlog is `ready`."""
    entry()(step)
    H.write(step.repo, ".shop/backlog/b1.md", "---\nid: %s\nkind: item\nstatus: ready\nprovenance: own\n---\n\n# One"
            " item\n" % ITEM)


ROWS = [
    (("rule is `error`", "capability violate rule"), erring, {"r1": "v15a"}),
    (("rule has no catalogue entry", "requirement use rule"), uncatalogued, {"r2": UNCATALOGUED}),
    (("catalogue entry has no purpose",), entry(purpose=False), {"c1": ENTRY}),
    (("catalogue entry mention no item",), entry(since=False), {"c1": ENTRY}),
    (("item is not `delivered`", "catalogue entry mention item"), undelivered, {"c1": ENTRY, "i1": ITEM}),
    (("rule is `warning`", "capability violate rule", "no rule is `error`"), warned, {"r1": "w_example"}),
]
