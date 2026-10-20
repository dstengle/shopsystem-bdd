"""The work-queue of a bounded context in .shop/work/: the library behind scripts/work (capability work-queue).

Standard library only. Frontmatter is read with scripts/model's own reader, so the two never disagree on a file.
"""
import importlib.machinery
import importlib.util
from pathlib import Path

WORK = Path(".shop") / "work"


def _load_model():
    path = Path(__file__).resolve().with_name("model")
    loader = importlib.machinery.SourceFileLoader("shopsystem_model", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


frontmatter = _load_model().frontmatter


class Refused(Exception):
    """What work was asked cannot be done; the message says why, and nothing was changed."""


def context_path(root):
    """The <owner>/<product>/<context name> of spec/index.md's bounded-context id."""
    data, _ = frontmatter((Path(root) / "spec" / "index.md").read_text())
    return data["id"].split("/", 1)[1]


def add(root, initiative, name, part_of, under, accepts):
    """Write .shop/work/<initiative>/<name>.md as a drafted work-item (r1)."""
    path = Path(root) / WORK / initiative / (name + ".md")
    text = ("---\nid: work-item/%s/%s\nkind: work-item\npart_of: %s\nstatus: drafted\nunder: %s\naccepts: [%s]\n---\n\n# %s\n"
            % (context_path(root), name, part_of, under, ", ".join(accepts), name))
    path.write_text(text)
    return path
