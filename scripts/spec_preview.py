"""`spec parse --item b<n>` (parsing r19, r20, r22, b452): a line read as it reads once an item's terms, relation rows,
lines and model lines are laid into the specification, as the readiness bar lays them, on a temporary copy of `spec/`
(and the context's construct catalogue, which spec_catalogued reads) so the context itself is never changed; a file
of the context given with `--file` read off the copy, so a capability file holds the item's lines too. `spec check
--item` and `spec trace --item` (b797, checking r152, product r58) read the whole context so laid (`whole`): `spec/`
and `grammar/` copied, every other entry of the context's top folder linked, so its features, backlog and product
file are read as they are."""

import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

import backlog_items
import backlog_lines
import spec_catalogued

COPIED = ("spec", "grammar")      # what the lay may write: copied, never linked, so the context is never changed


@contextmanager
def laid(root, name, whole=False):
    """The root of a copy of `root`'s spec with the item `name` laid on it; an item with no file refused, naming it.
    With `whole`, `grammar/` copied too and every other entry of `root`'s top folder linked beside them."""
    item = backlog_items.find(root, name)
    copy = Path(tempfile.mkdtemp(prefix="preview-"))
    try:
        shutil.copytree(Path(root) / "spec", copy / "spec")
        if whole:
            _beside(Path(root), copy)
        spec_catalogued.copy(root, copy)
        backlog_lines.lay_onto(copy, item)
        yield copy
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def _beside(root, copy):
    """`root`'s `grammar/` copied into `copy`, each other entry of its top folder but `spec/` linked there."""
    if (root / "grammar").is_dir():
        shutil.copytree(root / "grammar", copy / "grammar", symlinks=True)
    for entry in root.iterdir():
        if entry.name not in COPIED:
            (copy / entry.name).symlink_to(entry.resolve(), target_is_directory=entry.is_dir())


def rooted(args, run):
    """`run(args)`, or with `args.item` given, `run` of args whose root is the whole context with the item laid."""
    if not getattr(args, "item", None):
        return run(args)
    import argparse
    with laid(args.root, args.item, whole=True) as copy:
        return run(argparse.Namespace(**{**vars(args), "root": str(copy), "item": None}))


def on_copy(root, copy, file):
    """`file` (as given, relative to the working directory or absolute) as the copy's file when it is under `root`."""
    path, base = Path(file).resolve(), Path(root).resolve()
    return str(copy / path.relative_to(base)) if path.is_relative_to(base) else file
