"""`features generate` (design-r3 §5): each group of a codified-2 service capability is one scenario, or one a case
of its `or` boxes, read off its requirements' logical forms by features_generate4, with no solver; this module only
writes the file.

A scenario is its group's example data first, then the steps of its requirements; a comment line is written as
`# <text>`. A requirement that does not parse is refused. A capability file in `codified-1`, or with no marker, is
refused naming `migrate upgrade`; a lexicon with a term that names no part of speech is
refused naming each such term (`spec_lexicon.unlabelled`). The context is read once per state of its files (`spec_context.load`).
"""
from pathlib import Path

import features_generate4
import spec_context
import spec_grammar4
import spec_lexicon
import spec_read

HEADER = "# generated from spec/capabilities/%s.md by features generate; do not edit"


class GenerateError(Exception):
    """A capability that cannot be written: a requirement or an example line that does not parse."""


FOUR = (spec_grammar4.MARKER,)


def refused(ctx, cap, group):
    """GenerateError when a requirement of the group does not parse."""
    for req in group.requirements:
        ident = "%s#%s" % (cap.name, req.id)
        if ident in ctx.refused:
            raise GenerateError("%s: %s" % (ident, ctx.refused[ident]))


def written(group, lines, case=None):
    """A scenario's text: its tags, its title (with its case, of a group of several) and its (keyword, text, block)
    lines, a comment's keyword "#"."""
    out = ["  " + " ".join("@" + x for x in [group.id] + [r.id for r in group.requirements]),
           "  Scenario: " + group.title + ("" if case is None else " (case %d)" % case)]
    previous = None
    for keyword, text, block in lines:
        if keyword == "#":
            out.append("    # %s" % text)
            continue
        out.append("    %s %s" % ("And" if keyword == previous else keyword.capitalize(), text))
        previous = keyword
        if block is not None and block.kind == "table":
            out += ["      " + line for line in block.lines]
        elif block is not None:
            out += ['      """'] + [("      " + line).rstrip() for line in block.lines] + ['      """']
    return "\n".join(out)


def generate(root, path, skipped=None):
    """The feature text of one codified capability file (a draft outside spec/capabilities/ is read beside them);
    `skipped`, when given, gets the reason of each group with a fact no step words, by group id."""
    old = uncodified(root, [path])
    if old:
        raise GenerateError(old)
    unlabelled = spec_lexicon.unlabelled(spec_lexicon.read(root))
    if unlabelled:
        raise GenerateError(unlabelled)
    cap, path = spec_read.capability(path, FOUR), Path(path).resolve()
    if cap.problems:
        raise GenerateError("; ".join("%s: %s" % (path.name, p) for p in cap.problems))
    drafted = path.parent != (Path(root) / "spec" / "capabilities").resolve()
    ctx = spec_context.load(root, [path] if drafted else [])
    groups = sorted(cap.groups, key=lambda g: int(g.id[1:]))
    out = [HEADER % path.stem, "Feature: %s" % cap.frontmatter.get("title", cap.name),
           "  Narrator: %s" % cap.frontmatter.get("narrator", "")]
    for group in groups:
        text = scenario_four(root, ctx, cap, group, skipped)
        out += ["", text] if text else []
    return "\n".join(out) + "\n"


def scenario_four(root, ctx, cap, group, skipped=None):
    """A codified-2 group's scenarios (features_generate4), one a case of its `or` boxes, or None."""
    refused(ctx, cap, group)
    try:
        found = features_generate4.lines(root, ctx, cap, group, skipped)
    except features_generate4.GenerateError as err:
        raise GenerateError(str(err))
    if not found:
        return None
    return "\n\n".join(written(group, lines, k if len(found) > 1 else None) for k, lines in enumerate(found, 1))


def uncodified(root, paths):
    """The refusal of the first capability file of `paths` without `language: codified-2` (§13.4), or None: the 0.29
    reader and the codified-1 one are gone, so `migrate upgrade` converts it."""
    for path in paths:
        shown = Path(path).resolve()
        shown = shown.relative_to(Path(root).resolve()).as_posix() if shown.is_relative_to(Path(root).resolve()) \
            else Path(path).name
        if spec_read.codified(path, (spec_read.MARKER,)):
            return "%s says `language: codified-1`: run `migrate upgrade`" % shown
        if not spec_read.codified(path, FOUR):
            return "%s is not codified: run `migrate upgrade`" % shown
    return None
