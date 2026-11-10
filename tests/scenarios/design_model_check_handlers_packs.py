"""Handlers of the packs of design-model-check (b132): `model lexicon` run on the repository, and the conditions of a
bounded context and of a term that the packs give. A bounded context that is importing imports the plugin's CLI pack
and its own pack p1, which alone defines t1; one that is misimporting imports p1, which no pack is. A term that is
unmarked is defined by p1 too, which the context imports; one that is redefining says so with `Redefines: p1.`.
requests_handlers' bounded context condition and design_model_check_handlers_conditions' term condition hand these
words to `bounded_context` and `term`."""
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


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
CONTEXT = ("importing", "misimporting")
TERM = ("unmarked", "redefining")


def imports(repo, *names):
    """`imports:` written into the frontmatter of spec/index.md."""
    path = repo / "spec" / "index.md"
    path.write_text(path.read_text().replace("\n---\n", "\nimports: [%s]\n---\n" % ", ".join(names), 1))


def pack(repo, name, *terms):
    H.write(repo, "spec/packs/%s.md" % name, "---\nsource: ex.com/prod/up\n---\n# %s\n\n## Glossary\n\n%s" % (
        name, "".join("- **%s** (noun): a thing the pack gives.\n" % t for t in terms)))


@handler("WhenRuns", "`model lexicon`")
def model_lexicon(step):
    H.run_model(step, "lexicon")


def bounded_context(step, word):
    H.base(step.repo, step.context)
    if word == "importing":
        pack(step.repo, "p1", "t1")
        imports(step.repo, "cli", "p1")
    else:
        imports(step.repo, "p1")


def term(step, word):
    name, repo = step.names[0], step.repo
    H.base(repo, step.context)
    pack(repo, "p1", name)
    imports(repo, "p1")
    if word == "redefining":
        path = repo / "spec" / "index.md"
        path.write_text(path.read_text().replace("- **%s** (noun): a thing.\n" % name,
                                                 "- **%s** (noun): a thing. Redefines: p1.\n" % name))
