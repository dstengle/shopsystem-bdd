"""`spec parse --item b<n>` (parsing r19, r20, r22, b452): a line read as it reads once an item's terms, relation rows,
lines and model lines are laid into the specification, as the readiness bar lays them, on a temporary copy of `spec/`
(and the context's construct catalogue, which spec_catalogued reads) so the context itself is never changed; a file
of the context given with `--file` read off the copy, so a capability file holds the item's lines too. `spec check
--item` and `spec trace --item` (b797, checking r152, product r58) read the whole context so laid (`whole`): `spec/`
and `grammar/` copied, every other entry of the context's top folder linked, so its features, backlog and product
file are read as they are. Of `spec check --item`, the violations the lay alone brings left out (`lay_only`, b808,
checking r153-r155): v_s3 of a group the item lays, whose scenarios only a batch's lay writes, and v_a5 of a
requirement it lays, which only a batch's lay annotates in the adapter contract, as the readiness bar leaves them out;
every other violation of the item's reported, and each lexicon problem the lay brings that the specification without
it has not, as the readiness bar's lexicon stage finds them (`lexicon`, b848, checking r160). The item is laid by the
specification service's lay (spec_apply, b871), and `spec check --item` is its check of what the item brings
(spec_apply_check's `brought`, checking r164-r167): a finding the context has without the item is not returned, and
the bound check's and v_m9's violations the item brings are named by its operation, outcome or line."""

import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

import backlog_items
import backlog_section
import spec_apply
import spec_catalogued

# The rules whose violations of the item's own ids only a batch's lay clears (`lay_only`), each with the place of the
# id in its row: skipped, so that the rule catalogue does not take this module for where they are implemented
# (model_rules.skipped, b467).
SKIPPED_RULES = {"v_s3": 0, "v_a5": 1}
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
        spec_apply.lay(copy, item)       # the specification service's lay (b871)
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
    """`run(args)`, or with `args.item` given, `run` of args whose root is the whole context with the item laid, its
    `lexicon` the lexicon problems the lay brings and `brought` the specification service's check of what the item
    brings (spec_apply_check's `brought`, b871: the findings of `args.root` left out, the bound check's and v_m9's
    reasons of the item named)."""
    if not getattr(args, "item", None):
        return run(args)
    import argparse

    import spec_apply_check
    item = backlog_items.find(args.root, args.item)
    left_out, brought = lay_only(item), spec_apply_check.brought(args.root, item)
    with laid(args.root, args.item, whole=True) as copy:
        return run(argparse.Namespace(**{**vars(args), "root": str(copy), "item": None, "lay_only": left_out,
                                         "brought": brought, "lexicon": lexicon(args.root, copy)}))


def lexicon(root, copy):
    """The lexicon problems `(code, term, message)` of `copy` (the item laid) that `root`'s has not, each read with
    the kinds of the packs its spec imports, as the readiness bar's lexicon stage reads them."""
    import spec_lexicon
    import spec_rgl_vocab
    before = set(spec_lexicon.problems(spec_lexicon.read(root), spec_rgl_vocab.outer(root)))
    return [p for p in spec_lexicon.problems(spec_lexicon.read(copy), spec_rgl_vocab.outer(copy)) if p not in before]


def lay_only(item):
    """Whether a violation `(code, args)` is one the lay of `item` alone brings: v_s3 of a group it lays, v_a5 of a
    requirement it lays (the module's doc)."""
    blocks = backlog_section.read(item, "the item %s" % item.name)
    groups = {"%s#%s" % (b.capability, g.id) for b in blocks for g in b.groups}
    lines = set(backlog_section.ids(blocks))
    ids = dict(zip(SKIPPED_RULES, (groups, lines)))

    def brought(code, found):
        at = SKIPPED_RULES.get(code)
        return at is not None and len(found) > at and any(str(found[at]).endswith("/" + i) for i in ids[code])
    return brought


def on_copy(root, copy, file):
    """`file` (as given, relative to the working directory or absolute) as the copy's file when it is under `root`."""
    path, base = Path(file).resolve(), Path(root).resolve()
    return str(copy / path.relative_to(base)) if path.is_relative_to(base) else file
