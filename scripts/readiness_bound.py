"""The bound check's violations an item owns (b721, items r72, batches r160): v_pb1 names an operation of a driven port
and v_pb2 an outcome of one (`<service>.<operation> <kind>`), never a group or a requirement, so the readiness bar's
and `work batch start`'s check of an item's violations reads them apart: one is the item's when its operation is one
the item's model lines declare (`declared`, readiness_bar's `model_elements`) or one of its lines requests, in its
trigger or its response (`requester`, `asks`: a port line governs it, a core line asks it) (`operations`), each
named with its operation or its outcome and the rule (`reasons`); `work batch start` counts only those its lay adds
to the base's (`before`, b725), as the readiness bar counts only those an item's lay adds. v_m9 names an object, its
attribute and a transition, never a requirement: one is the item's when a requirement of its own sets that attribute
along that transition on the request of an operation of an area other than the object's, the facts model.lp joins,
named with the requirement and the rule (`transitions`, b731)."""
import shutil
import tempfile
from pathlib import Path

BOUND = ("v_pb1", "v_pb2")
KEPT = BOUND + ("v_m9",)    # the codes `before` keeps


def operations(declared, facts, mine):
    """The operations an item's violations of the bound check are its own of: those of `declared` (the qualified ids
    of the elements its model lines declare) that are operations, and those the facts' `requester` and `asks` of a
    requirement of `mine` (`<capability>#r<n>`) name."""
    found = {e for e in declared if "." in e}
    for pred, args in facts:
        if pred in ("requester", "asks") and str(args[0]).rsplit("/", 1)[-1] in mine:
            found.add(str(args[1]))
    return found


def operation(name, args):
    """The operation a violation of the bound check is of: v_pb1's argument, the first word of v_pb2's outcome."""
    return str(args[0]) if name == "v_pb1" else str(args[0]).split(" ", 1)[0]


def reasons(found, ops, labels):
    """A reason for each violation of `found` ((code, args)) of the bound check whose operation is one of `ops`,
    naming the operation or the operation outcome and the rule."""
    out = []
    for name, args in sorted(found):
        if name in BOUND and operation(name, args) in ops:
            what = "the operation" if name == "v_pb1" else "the operation outcome"
            out.append("%s %s: %s %s" % (what, args[0], name, labels.get(name, "")))
    return out


def before(tree):
    """The bound check's violations of the spec at `tree` before a lay, as (code, args) of strings: the readiness bar's
    result of a copy of that spec kept on disk (readiness_before), which its check of the batch's first item kept, else
    `model.lp` solved on the tree (b725)."""
    import readiness_before
    import spec_catalogued
    copy = Path(tempfile.mkdtemp(prefix="bound-"))
    try:
        shutil.copytree(Path(tree) / "spec", copy / "spec")
        spec_catalogued.copy(tree, copy)
        kept = readiness_before.get(copy, readiness_before.key(copy))
    finally:
        shutil.rmtree(copy, ignore_errors=True)
    if kept is not None:
        found = kept[1]
    else:
        from model_check import solve
        from model_facts import Model
        found = {(name, tuple(str(a) for a in args)) for name, args in solve(Model(tree).read())[0]}
    return {(name, args) for name, args in found if name in KEPT}


def transitions(found, facts, mine, labels):
    """A reason for each violation of `found` ((code, args)) of v_m9 (object, attribute, from, to) that a requirement
    of `mine` (`<capability>#r<n>`) brings: it sets the attribute of the object to `to`, from `from` or from any value,
    on the request of an operation whose area is not the object's; naming the requirement and the rule."""
    facts = [(pred, [str(a) for a in args]) for pred, args in facts]
    obj_area = {args[0]: args[1] for pred, args in facts if pred == "obj_area"}
    op_area = {args[0]: args[1] for pred, args in facts if pred == "op_area"}
    ops = {}
    for pred, args in facts:
        if pred == "requester":
            ops.setdefault(args[0].rsplit("/", 1)[-1], set()).add(args[1])
    sets = [(args[0].rsplit("/", 1)[-1], args[1], args[2], args[3] if pred == "sets" else None, args[-1])
            for pred, args in facts if pred in ("sets", "sets_from_any")]
    out = []
    for name, args in sorted(found):
        if name != "v_m9":
            continue
        obj, attr, was, to = args
        for q, o, t, f, v in sets:
            if q in mine and (o, t, v) == (obj, attr, to) and f in (None, was) and any(
                    op_area.get(op) not in (None, obj_area.get(obj)) for op in ops.get(q, ())):
                out.append("%s: %s %s: with %s" % (q, name, labels.get(name, ""), ", ".join(args)))
    return out
