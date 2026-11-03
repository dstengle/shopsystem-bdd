"""`features generate` (design-r2 §7): each group of a codified service capability is one scenario, read off the
group's minimal trace by spec_trace; this module only writes the file.

A scenario is its group's example data first (the given block's lines that `spec_read_given.example` passes, each
with its docstring or table), then the steps of the trace. A given line that is not example data is left out with a
line on stderr (model check's v15m is its error), and so is a group whose trace has none (its L1, named by `model
logic`). A logic-only group (`spec_tree.logic_only`) has no scenario. A requirement that does not parse is refused.
"""
import sys
from pathlib import Path

import features_vocab as fv
import spec_grammar
import spec_read
import spec_read_given
import spec_solve
import spec_trace
import spec_tree

HEADER = "# generated from spec/capabilities/%s.md by features generate; do not edit"
_CTX = {}


class GenerateError(Exception):
    """A capability that cannot be written: a requirement or an example line that does not parse."""


def context(root, extra=()):
    """spec_solve's translation of the context, with drafted files `extra`; built once per process for each state of
    the spec's files."""
    files = sorted((Path(root) / "spec").rglob("*.md")) + [Path(p) for p in extra]
    key = tuple((str(p.resolve()), p.stat().st_mtime_ns, p.stat().st_size) for p in files if p.is_file())
    if key not in _CTX:
        _CTX[key] = spec_solve.Context(root, list(extra))
    return _CTX[key]


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


def scenario_text(v, ctx, cap, group, found):
    """A group's scenario, or None for a logic-only group or one whose trace has none."""
    gid = "%s#%s" % (cap.name, group.id)
    mine = next((g for g in ctx.groups if g.id == gid), None)
    have = {s.id for s in mine.statements} if mine else set()
    for req in group.requirements:
        if "%s#%s" % (cap.name, req.id) not in have:
            raise GenerateError("%s#%s: %s" % (cap.name, req.id, spec_grammar.parse(v.root, req.text).refusal))
    if not mine or spec_tree.logic_only(mine.trees):
        return None
    if isinstance(found.get(gid), str):
        _warn(gid, "no scenario: %s" % found[gid])
        return None
    try:
        steps = spec_trace.read(found[gid], gid, [s.id for s in mine.statements], ctx.vocab, v)
    except spec_trace.TraceError as err:
        _warn(gid, "no scenario: %s" % err)
        return None
    lines = _example(v, cap, group) + [(k, v.text(t), None) for k, t in steps]
    out = ["  " + " ".join("@" + x for x in [group.id] + [r.id for r in group.requirements]),
           "  Scenario: " + group.title]
    previous = None
    for keyword, text, block in lines:
        out.append("    %s %s" % ("And" if keyword == previous else keyword.capitalize(), text))
        previous = keyword
        if block is not None and block.kind == "table":
            out += ["      " + line for line in block.lines]
        elif block is not None:
            out += ['      """'] + [("      " + line).rstrip() for line in block.lines] + ['      """']
    return "\n".join(out)


def generate(root, path):
    """The feature text of one codified capability file (a draft outside spec/capabilities/ is read beside them)."""
    v, cap, path = fv.load(root), spec_read.capability(path), Path(path).resolve()
    if cap.problems:
        raise GenerateError("; ".join("%s: %s" % (path.name, p) for p in cap.problems))
    drafted = path.parent != (Path(root) / "spec" / "capabilities").resolve()
    ctx = context(root, [path] if drafted else [])
    groups = sorted(cap.groups, key=lambda g: int(g.id[1:]))
    found = spec_trace.traces(ctx, [g for g in ctx.groups if g.capability == cap.name and g.trees
                         and not spec_tree.logic_only(g.trees)])
    out = [HEADER % path.stem, "Feature: %s" % cap.frontmatter.get("title", cap.name),
           "  Narrator: %s" % cap.frontmatter.get("narrator", "")]
    for group in groups:
        text = scenario_text(v, ctx, cap, group, found)
        out += ["", text] if text else []
    return "\n".join(out) + "\n"


def uncodified(root, paths):
    """The refusal of the first capability file of `paths` without `language: codified-1` (§13.4), or None: the 0.29
    reader is gone, so `migrate upgrade` converts it."""
    for path in paths:
        if not spec_read.codified(path):
            return "%s is not codified: run `migrate upgrade`" % Path(path).relative_to(root).as_posix()
    return None
