"""The bound check's violations an item owns (b721, items r72, batches r160): v_pb1 names an operation of a driven port
and v_pb2 an outcome of one (`<service>.<operation> <kind>`), never a group or a requirement, so the readiness bar's
and `work batch start`'s check of an item's violations reads them apart: one is the item's when its operation is one
the item's model lines declare (`declared`, readiness_bar's `model_elements`) or one of its lines requests, in its
trigger or its response (`requester`, `asks`: a port line governs it, a core line asks it) (`operations`), each
named with its operation or its outcome and the rule (`reasons`)."""

BOUND = ("v_pb1", "v_pb2")


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
