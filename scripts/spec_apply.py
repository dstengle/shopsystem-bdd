"""The specification service's apply (b871, checking r164-r168; the item 1 of b861's split): an item applied to a
specification, the spec of a tree (a batch's workspace, the readiness bar's copy, the preview's copy).

`lay(tree, item)`: the item's lines and the other pieces of its `## Requirements` laid into the tree's `spec/`
(backlog_lines' `lay_onto`) and their ids appended to `unbuilt:`, nothing else; the paths changed. `prepare(tree,
items)`, once the items are laid, once for all of them: the feature of each service capability they laid written again
by the tree's generator (batch_generator), and the bookkeeping of the lay (b333): the corpus's blocks
(spec_corpus_write), each accepted decision a retirement leaves unenforced superseded (decision_successor, b741), the
features and corpus blocks the lay's change of grammar 4's inputs reaches (batch_reached, b707), spec/index.md's
Composition (spec_composition, b606), the adapter contracts annotated (b379) and the catalogues (batch_catalogues), a
catalogue that cannot be written given back. `apply(tree, items)`: each item laid and the specification prepared once,
answered as a domain_envelope Response: done with the paths changed, or refused when the feature generator is
unresponsive (batch_generator's `Unresponsive`), naming it, the tree's files the apply changed put back (U17); any other
generator's refusal raised as Refused. The check of what an item brings is spec_apply_check's."""
import subprocess
from pathlib import Path

import adapter_annotate
import backlog_items
import backlog_lines
import batch_catalogues
import batch_generator
import batch_reached
import decision_successor
import features_generate
import spec_composition
import spec_corpus_write
import spec_held
import spec_read
import spec_unbuilt
from plumbing.domain_envelope import Response, error
from plumbing.shop_files import Refused

COMMAND = "work batch start"
UNRESPONSIVE = "feature generator unresponsive"


def ids(items):
    """{capability: [requirement id, ...]} of the items' lines."""
    found = {}
    for item in items:
        for block in backlog_lines.read(item, backlog_items.rel_of(item.name)):
            found.setdefault(block.capability, []).extend(r for g in block.groups for r, _ in g.requirements)
    return found


@spec_held.writes
def lay(tree, item, files=None):
    """The item's lines laid into the tree's `spec/` and their ids into `unbuilt:`; the paths changed, each also added
    to `files` when it is given."""
    laid = []
    backlog_lines.lay_onto(tree, item, laid)
    changed = []
    for capability, listed in ids([item]).items():
        path = backlog_lines.capability_file(tree, capability)
        if not listed or not path.is_file():
            continue
        path.write_text(spec_unbuilt.with_unbuilt(path.read_text(), listed))
        changed.append(path.relative_to(tree).as_posix())
    changed = list(dict.fromkeys(changed + laid))
    if files is not None:
        files.extend(changed)
    return changed


def prepare(tree, items, unwritten=None, command=COMMAND, superseded=None):
    """The tree, its `items` laid, made whole for them (the module's doc), a catalogue that cannot be written added to
    `unwritten`, `(item, path, old id)` of each decision superseded added to `superseded`; a generator's refusal said
    as `command`'s (b486), an unresponsive one raised as it is; the paths changed."""
    laid, changed = ids(items), []
    for capability in laid:
        changed += generated(tree, capability, command)
    changed += spec_corpus_write.write(tree, items)
    changed += decision_successor.lay(tree, items, superseded)
    changed += batch_reached.prepared(tree, set(laid))
    changed += spec_composition.write(tree)
    changed += _annotated(tree)
    catalogues, problems = batch_catalogues.write(tree, ["%s#%s" % (c, r) for c, rs in laid.items() for r in rs])
    if unwritten is not None:
        unwritten.extend(problems)
    return list(dict.fromkeys(changed + catalogues))


def apply(tree, items, command=COMMAND):
    """The specification service's reply to the apply of `items` to the tree's specification: each laid, then the
    specification prepared once; done {"changed", "unwritten", "superseded"}, or refused naming the feature generator
    when it is unresponsive, the files it changed put back."""
    dirty = _dirty(tree)
    unwritten, superseded, files = [], [], []
    try:
        for item in items:
            lay(tree, item, files)
        changed = prepare(tree, items, unwritten, command, superseded)
    except batch_generator.Unresponsive as err:
        _put_back(tree, dirty)
        return Response("refused", errors=[error("%s: %s" % (UNRESPONSIVE, err),
                                                 ["feature generator:%s" % err.program])])
    return Response("done", {"changed": list(dict.fromkeys(changed + files)), "unwritten": unwritten,
                             "superseded": superseded})


def _git(tree, *args):
    return subprocess.run(["git", "-C", str(tree), *args], capture_output=True, text=True)


def _dirty(tree):
    """The paths of the tree git holds changed or untracked, or None when the tree is no git worktree."""
    done = _git(tree, "status", "--porcelain", "-z", "--untracked-files=all")
    if done.returncode != 0:
        return None
    return {entry[3:] for entry in done.stdout.split("\0") if entry}


def _put_back(tree, before):
    """Each path the apply changed since `before` (`_dirty`'s) put back as git holds it, an untracked one removed; a
    tree that is no git worktree left as it is (a copy, thrown away by its caller)."""
    if before is None:
        return
    for rel in sorted(_dirty(tree) - before):
        if _git(tree, "cat-file", "-e", "HEAD:%s" % rel).returncode == 0:
            _git(tree, "checkout", "HEAD", "--", rel)
        else:
            (Path(tree) / rel).unlink(missing_ok=True)


def _annotated(tree):
    """Each adapter contract of the tree that does not hold the requirements governing its operations written as
    `spec annotate` writes it (b379); their paths."""
    found = adapter_annotate.stale(tree)
    for rel, text in found:
        (Path(tree) / rel).write_text(text, encoding="utf-8")
    return [Path(rel).as_posix() for rel, _ in found]


def generated(tree, capability, command=COMMAND):
    """The capability file's path and, for a service capability, its feature written again from it by the tree's
    generator (b740); an unresponsive generator raised as it is, another refusal said as `command`'s."""
    path = backlog_lines.capability_file(tree, capability)
    changed = [path.relative_to(tree).as_posix()]
    if spec_read.capability(path).frontmatter.get("group") == "guarantees":
        return changed
    try:
        text = batch_generator.generate(tree, path)
    except batch_generator.Unresponsive:
        raise
    except features_generate.GenerateError as err:
        raise Refused("%s: features generate of %s failed: %s" % (command, capability, err)) from None
    feature = Path(tree) / "features" / ("%s.feature" % capability)
    feature.parent.mkdir(parents=True, exist_ok=True)
    feature.write_text(text)
    return changed + [feature.relative_to(tree).as_posix()]
