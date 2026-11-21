"""An item's or a batch's id resolved to the file that holds it (b49): `item/<context path>/b<n>` the item
`.shop/backlog/b<n>.md`, `batch/<context path>/batch-<n>` the plan `.shop/batches/<n>/plan.md`, or `<kind>/<name>` in
this context, held when that file is there and its frontmatter `id` is the full id. Standard library and model_parse
only, so `spec`'s facts and `work record` read it alike."""
from pathlib import Path

from model_parse import frontmatter

FILES = {"item": lambda name: Path(".shop") / "backlog" / ("%s.md" % name),
         "batch": lambda name: Path(".shop") / "batches" / name.removeprefix("batch-") / "plan.md"}
KINDS = tuple(FILES)


def held(root, ident, path):
    """True when `ident` is the id of an item or a batch whose file the root holds; `path` the context's
    <owner>/<product>/<context name>."""
    kind, _, rest = str(ident).strip().partition("/")
    name = rest.removeprefix("%s/" % path)
    if kind not in FILES or not name or "/" in name:
        return False
    file = Path(root) / FILES[kind](name)
    return file.is_file() and frontmatter(file.read_text())[0].get("id") == "%s/%s/%s" % (kind, path, name)
