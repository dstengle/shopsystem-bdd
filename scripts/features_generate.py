"""`features generate` (design-r3 §5): each group of a codified service capability is one scenario, read off its
requirements' facts by spec_steps, with no solver; this module only writes the file.

A scenario is its group's example data first (the given block's lines that `spec_read_given.example` passes, each
with its docstring or table), then the steps of its requirements. A given line that is not example data is left out
with a line on stderr (model check's v15m is its error), and so is a group with a fact no step words. A logic-only
group (`spec_tree.logic_only`) has no scenario. A requirement that does not parse is refused. The context is read
once per state of its files (`spec_context.load`).
"""
import sys
from pathlib import Path

import features_generate4
import features_vocab as fv
import spec_context
import spec_grammar4
import spec_read
import spec_read_given
import spec_steps
import spec_tree

HEADER = "# generated from spec/capabilities/%s.md by features generate; do not edit"


class GenerateError(Exception):
    """A capability that cannot be written: a requirement or an example line that does not parse."""


FOUR = (spec_grammar4.MARKER,)


def _warn(gid, text):
    print("features generate: %s: %s" % (gid, text), file=sys.stderr)


def _example(v, cap, group):
    """The (keyword, text, block) lines of a group's example data; any other given line is left out, with a warning."""
    out = []
    for text, block in group.given:
        if not spec_read_given.example(text, block):
            _warn("%s#%s" % (cap.name, group.id), "the given line %r is not example data; left out" % text)
            continue
        try:
            out.append(("given", v.text(fv.parse(v, "given", text)), block))
        except fv.StepError as err:
            raise GenerateError("%s#%s: the given line %s" % (cap.name, group.id, err))
    return out


def scenario_text(v, ctx, cap, group, skipped=None):
    """A group's scenario, or None for a logic-only group or one with a fact no step words (its reason kept in
    `skipped`, by group id, when given)."""
    gid = "%s#%s" % (cap.name, group.id)
    refused(ctx, cap, group)
    mine = [s for s in ctx.statements if s.group == gid]
    if not mine or spec_tree.logic_only([s.tree for s in mine]):
        return None
    try:
        steps = spec_steps.read([ctx.facts[s.id] for s in mine], ctx.vocab, v)
    except spec_steps.TraceError as err:
        _warn(gid, "no scenario: %s" % err)
        if skipped is not None:
            skipped[gid] = str(err)
        return None
    return written(group, _example(v, cap, group) + [(k, v.text(t), None) for k, t in steps])


def refused(ctx, cap, group):
    """GenerateError when a requirement of the group does not parse."""
    for req in group.requirements:
        ident = "%s#%s" % (cap.name, req.id)
        if ident in ctx.refused:
            raise GenerateError("%s: %s" % (ident, ctx.refused[ident]))


def written(group, lines):
    """A scenario's text: its tags, its title and its (keyword, text, block) lines, a comment's keyword "#"."""
    out = ["  " + " ".join("@" + x for x in [group.id] + [r.id for r in group.requirements]),
           "  Scenario: " + group.title]
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
    four = spec_read.codified(path, FOUR)
    cap, path = spec_read.capability(path, spec_context.MARKERS), Path(path).resolve()
    v = None if four else fv.load(root)
    if cap.problems:
        raise GenerateError("; ".join("%s: %s" % (path.name, p) for p in cap.problems))
    drafted = path.parent != (Path(root) / "spec" / "capabilities").resolve()
    ctx = spec_context.load(root, [path] if drafted else [])
    groups = sorted(cap.groups, key=lambda g: int(g.id[1:]))
    out = [HEADER % path.stem, "Feature: %s" % cap.frontmatter.get("title", cap.name),
           "  Narrator: %s" % cap.frontmatter.get("narrator", "")]
    for group in groups:
        text = scenario_four(root, ctx, cap, group, skipped) if four else scenario_text(v, ctx, cap, group, skipped)
        out += ["", text] if text else []
    return "\n".join(out) + "\n"


def scenario_four(root, ctx, cap, group, skipped=None):
    """A codified-2 group's scenario (features_generate4), or None."""
    refused(ctx, cap, group)
    try:
        found = features_generate4.lines(root, ctx, cap, group, skipped)
    except features_generate4.GenerateError as err:
        raise GenerateError(str(err))
    return written(group, found) if found else None


def uncodified(root, paths):
    """The refusal of the first capability file of `paths` without `language: codified-1` (§13.4), or None: the 0.29
    reader is gone, so `migrate upgrade` converts it."""
    for path in paths:
        if not spec_read.codified(path, spec_context.MARKERS):
            return "%s is not codified: run `migrate upgrade`" % Path(path).relative_to(root).as_posix()
    return None
