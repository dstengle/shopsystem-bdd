"""`work decision --amend <decision>` (decisions r21-r23, b458): the operation decisions.amend, an accepted
design-decision given more enforcers (`--enforced-by`, its `enforced_by`) and foundations (`--rests-on`, its
`rests_on`), each added once after those it names already, nothing else of it changed, and the decisions index
rewritten, the two committed together; a decision whose status is not accepted refused naming it, before anything
is written."""
import re
from pathlib import Path

import shop_files
from model_parse import DECISIONS, decision_files

KEYS = ("enforced_by", "verified_by", "rests_on", "supersedes", "source")    # the lists' order in a decision's head


def found(root, ref, parameter):
    """(path, its path relative to the root, its frontmatter) of the one decision `ref` names by its id, its path or
    its number; none, or more than one, refused naming the parameter."""
    hits = []
    for path in decision_files(root):
        data, _ = shop_files.frontmatter(shop_files.read(path, root))
        rel = path.relative_to(root).as_posix()
        if ref in (data.get("id"), rel, path.name, path.stem) or path.name.startswith(ref + "-"):
            hits.append((path, rel, data))
    if len(hits) != 1:
        raise shop_files.Refused("{names} %s names %s design-decision" % (ref, "no" if not hits else "more than one"),
                                 reason="names no design-decision" if not hits else "names more than one "
                                 "design-decision", names=["parameter:%s" % parameter])
    return hits[0]


def in_force(rel, data, what):
    """Refused, naming the decision, unless its status is accepted."""
    if data.get("status") != "accepted":
        raise shop_files.Refused("%s (%s) is %s, not accepted: only a design-decision in force is %s"
                                 % (rel, data.get("id"), data.get("status") or "of no status", what),
                                 reason="not accepted", names=["design-decision:%s" % data.get("id")])


def listed(line):
    return [x.strip() for x in line.split(":", 1)[1].strip().strip("[]").split(",") if x.strip()]


def amended(text, additions):
    """A decision's text with each list of `additions` ({key: [value]}) extended by the values it lacks, a list it
    has not added after the lists before it in KEYS (else after `tier:`), nothing else changed."""
    head, rest = text[4:].split("\n---\n", 1)
    lines = head.split("\n")
    for key in KEYS:
        values = additions.get(key) or []
        at = next((i for i, line in enumerate(lines) if line.startswith(key + ":")), None)
        if at is not None:
            have = listed(lines[at])
            lines[at] = "%s: [%s]" % (key, ", ".join(have + [v for v in dict.fromkeys(values) if v not in have]))
        elif values:
            before = [i for i, line in enumerate(lines) for k in ("tier",) + KEYS[:KEYS.index(key)]
                      if line.startswith(k + ":")]
            lines.insert(max(before, default=len(lines) - 1) + 1, "%s: [%s]" % (key, ", ".join(dict.fromkeys(values))))
    return "---\n%s\n---\n%s" % ("\n".join(lines), rest)


def amend(root, decision, enforcers=(), foundations=()):
    """The operation decisions.amend: the decision given its enforcers and foundations, the index rewritten, both
    committed; the decision's path, relative to the root."""
    root = Path(root)
    path, rel, data = found(root, decision, "design-decision")
    in_force(rel, data, "amended")
    if not enforcers and not foundations:
        raise shop_files.Refused("an amendment gives {names}", reason="nothing to amend",
                                 names=["parameter:enforcer", "parameter:foundation"])
    for value in [*enforcers, *foundations]:
        if not value.strip() or re.search(r"[\[\],\n\r]", value):
            raise shop_files.Refused("%r is no id: an enforcer or a foundation is one id" % value, reason="not an id",
                                     names=["parameter:enforcer" if value in enforcers else "parameter:foundation"])
    text = amended(path.read_text(encoding="utf-8"), {"enforced_by": list(enforcers), "rests_on": list(foundations)})
    index = (DECISIONS / "index.md").as_posix()
    title = next((line[2:] for line in text.splitlines() if line.startswith("# ")), path.stem)

    from model_report import render_decisions

    def put():
        path.write_text(text, encoding="utf-8")
        (root / index).write_text(render_decisions(root), encoding="utf-8")
    shop_files.committed(root, [rel, index], "work decision --amend: %s" % title, put)
    return rel


def enforcing(root, requirement):
    """The line `work line --retires` prints of each design-decision whose `enforced_by` names the requirement it
    retires (drafting r28): its id and path, and the amendment that names the requirement's replacement."""
    root = Path(root)
    out = []
    for path in decision_files(root):
        data, _ = shop_files.frontmatter(shop_files.read(path, root))
        held = data.get("enforced_by") or []
        if requirement in (held if isinstance(held, list) else [held]):
            out.append("%s enforces %s (%s): name what holds it now with `work decision --amend %s --enforced-by "
                       "<id>`" % (requirement, data.get("id"), path.relative_to(root).as_posix(), data.get("id")))
    return out
