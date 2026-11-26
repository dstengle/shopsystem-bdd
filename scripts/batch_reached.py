"""What a lay's change of grammar 4's inputs reaches beyond the laid capabilities (b707, batches r157): when laying
the picked items changed a file grammar 4's vocabulary is read from (spec_held's `inputs`: the domain model, the
vocabulary, the packs, the index) or `spec/universal.md`, every service capability's feature written again where
`features generate` now writes it differently, and every block of the spec corpus whose form `spec parse --form` now
prints differently given that form, its heading, trace and line kept. A capability the lay laid lines of is
batch_start's own to generate; a feature that is not there, or that `features generate` refuses, is left as it is.
"""
import hashlib
import re
from pathlib import Path

import spec_corpus_write
import spec_held
import spec_read

READING = re.compile(r"(?ms)^(## [rU][1-9]\d*[ \t]*\n.*?```reading\n)([^\n]*)\n(.*?)\n```")


def digest(tree):
    """The digest of what grammar 4 and the entailed Thens read at `tree`, to tell whether a lay changed it."""
    sha = hashlib.sha256()
    for path in spec_held.inputs(tree) + [str(Path(tree) / "spec" / "universal.md")]:
        p = Path(path)
        sha.update(path.encode() + b"\0" + (p.read_bytes() if p.is_file() else b"-") + b"\0")
    return sha.hexdigest()


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


def regenerated(tree, before, laid):
    """The features and corpus blocks the lay reached written again when the digest of `tree` is no longer `before`;
    the paths changed."""
    if digest(tree) == before:
        return []
    with spec_held.held(tree):
        return features(tree, laid) + corpus(tree)
