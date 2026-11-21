"""`spec parse --item b<n>` (parsing r19, r20, r22, b452): a line read as it reads once an item's terms, relation rows,
lines and model lines are laid into the specification, as the readiness bar lays them, on a temporary copy of `spec/`
(and the context's construct catalogue, which spec_catalogued reads) so the context itself is never changed; a file
of the context given with `--file` read off the copy, so a capability file holds the item's lines too."""

import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

import backlog_items
import backlog_lines
import spec_catalogued


@contextmanager
def laid(root, name):
    """The root of a copy of `root`'s spec with the item `name` laid on it; an item with no file refused, naming it."""
    item = backlog_items.find(root, name)
    copy = Path(tempfile.mkdtemp(prefix="preview-"))
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")
        catalogue = Path(root) / spec_catalogued.CATALOGUE
        if catalogue.is_file():
            (copy / catalogue.parent.name).mkdir()
            shutil.copy2(catalogue, copy / spec_catalogued.CATALOGUE)
        backlog_lines.lay_onto(copy, item)
        yield copy
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def on_copy(root, copy, file):
    """`file` (as given, relative to the working directory or absolute) as the copy's file when it is under `root`."""
    path, base = Path(file).resolve(), Path(root).resolve()
    return str(copy / path.relative_to(base)) if path.is_relative_to(base) else file
