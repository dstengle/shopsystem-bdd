"""What a lay's change of grammar 4's inputs reaches beyond the laid capabilities (b707, laying r17, r18): when laying
the picked items changed a file grammar 4's vocabulary is read from (spec_held's `inputs`: the domain model, the
vocabulary, the packs, the index) or `spec/universal.md`, every service capability's feature written again where
`features generate` now writes it differently, and every block of the spec corpus whose form `spec parse --form` now
prints differently given that form, its heading, trace and line kept. A capability the lay laid lines of is
laying_inprocess's prepare's own to generate; a feature that is not there, or that `features generate` refuses, is left
as it is. `prepared`: of a workspace whose items are laid uncommitted, the change told by git since its HEAD (b758);
`reached`: that change touches one of spec_held's `inputs` under the workspace (the plugin's packs and base grammar
among them when the workspace is the plugin's own repository, b763) or `spec/universal.md`.
"""
import os
import re
import subprocess
from pathlib import Path

import spec_corpus_write
import spec_held
import spec_read

READING = re.compile(r"(?ms)^(## [rU][1-9]\d*[ \t]*\n.*?```reading\n)([^\n]*)\n(.*?)\n```")


def features(tree, laid):
    """Each service capability's feature but those of `laid` written again where `features generate` now writes it
    differently; the paths changed."""
    import batch_generator
    import features_generate
    changed, paths = [], []
    for path in sorted((Path(tree) / "spec" / "capabilities").glob("*.md")):
        feature = Path(tree) / "features" / ("%s.feature" % path.stem)
        if path.stem in laid or not feature.is_file() or features_generate.uncodified(tree, [path]) \
                or spec_read.capability(path).frontmatter.get("group") == "guarantees":
            continue
        paths.append(path)
    for path, text in batch_generator.generate_all(tree, paths).items():     # the tree's generator (b740)
        feature = Path(tree) / "features" / ("%s.feature" % path.stem)
        if text is not None and text != feature.read_text():
            feature.write_text(text)
            changed.append(feature.relative_to(tree).as_posix())
    return changed


def corpus(tree):
    """Each block of the tree's corpus, in the file of a codified-2 capability or of the universal conditions, whose form `spec parse --form` now prints differently
    given that form; the paths changed."""
    if not spec_corpus_write.kept(tree):
        return []
    changed = []
    for path in sorted((Path(tree) / spec_corpus_write.CORPUS).glob("*.md")):
        held = path.stem == "universal" or (Path(tree) / "spec" / "capabilities" / path.name).is_file()
        if not held or not spec_corpus_write.codified(tree, path.stem):
            continue
        was = path.read_text()
        text = READING.sub(lambda m: "%s%s\n%s\n```" % (m.group(1), m.group(2),
                                                         spec_corpus_write.form(tree, m.group(2))), was)
        if text != was:
            path.write_text(text)
            changed.append(path.relative_to(tree).as_posix())
    return changed


def inputs(tree):
    """The paths, relative to `tree`, of grammar 4's inputs (spec_held's) under it and `spec/universal.md`, with the
    folder under `spec/` of each, so that a file a lay takes out is told too; the plugin's packs and grammar outside
    `tree` no lay changes."""
    top = os.path.realpath(str(tree))
    out = []
    for path in spec_held.inputs(tree) + [os.path.join(str(tree), "spec", "universal.md")]:
        rel = os.path.relpath(os.path.realpath(path), top)
        if rel == os.pardir or rel.startswith(os.pardir + os.sep):
            continue
        folder = os.path.dirname(rel)
        for each in [rel] + ([folder] if folder.startswith("spec" + os.sep) else []):
            if each not in out:
                out.append(each)
    return out


def reached(tree):
    """Whether the workspace's change since its HEAD (uncommitted, untracked among it) touches one of `inputs`."""
    done = subprocess.run(["git", "status", "--porcelain", "-z", "--untracked-files=all", "--", *inputs(tree)],
                          cwd=str(tree), capture_output=True, text=True, check=True)
    return bool(done.stdout.strip("\0").strip())


def prepared(tree, laid):
    """The features and corpus blocks the workspace's laid items reached written again when its change since its HEAD
    touches grammar 4's inputs (`reached`); the paths changed."""
    if not reached(tree):
        return []
    with spec_held.held(tree):
        return features(tree, laid) + corpus(tree)
