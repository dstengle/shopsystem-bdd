"""The worlds of the language service's general lines (parsing, b369), rows design_model_check_worlds' TABLE takes last:
a requirement that conforms to the language reference (the base world's r1), one that violates a reading rule (R2's
"the" with no antecedent, the rule named as the language reference names it) and one that uses a construct the
context's construct catalogue has no entry of (the plugin's catalogue written into the context with the entry of
`rc-object` left out). Each world but the base one is codified2_world's, its r1 the line here."""
import importlib.util
import re
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C2 = _sibling("codified2_world.py", "shop_codified2_world")
CATALOGUE = Path(__file__).resolve().parents[2] / "grammar" / "constructs.md"
UNCATALOGUED = "rc-object"


def line(text):
    return lambda step: C2.context(step.repo, H.PATH, [text])


def uncatalogued(step):
    """r1 a line of a relative clause on a verb's frame (`rc-object`), and a construct catalogue with no entry of it."""
    C2.context(step.repo, H.PATH, [C2.LINES["relative"][0]])
    text = re.sub(r"^## %s\n.*?(?=^## )" % re.escape(UNCATALOGUED), "", CATALOGUE.read_text(),
                  flags=re.MULTILINE | re.DOTALL)
    assert "## %s\n" % UNCATALOGUED not in text
    H.write(step.repo, "grammar/constructs.md", text)


ROWS = [
    (("requirement conform language reference",), lambda step: None, {}),
    (("requirement violate reading rule",), line(C2.LINES["antecedentless"][0]), {"r2": "R2"}),
    (("construct has no catalogue entry", "requirement use construct"), uncatalogued, {"c1": UNCATALOGUED}),
]
