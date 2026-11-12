"""A codified capability's `unbuilt: [r<n>, ...]`: the requirements written in the spec and not yet built (workflow
simplification plan 1). `unbuilt(root)` reads the ids of every codified capability under `root`/spec/capabilities/,
`problems(root)` names each listed id the capability has no requirement for and each `unbuilt:` of a capability that
is not codified (they mark nothing), and `mark(items, root)` puts a strict xfail on each pytest-bdd scenario of a
listed requirement, so a scenario that starts passing fails the suite until its id leaves `unbuilt:`; non-strict when
`$SHOPSYSTEM_UNBUILT_NONSTRICT` names `root`, as `work batch done` sets it for a task's run, where another in-batch
item's scenario that passes is no fault of the task (batches r19). Standard library, and pytest in `mark` only."""
import os
import pathlib
import re

from model_parse import frontmatter
from spec_read import MARKERS, capability

NONSTRICT = "SHOPSYSTEM_UNBUILT_NONSTRICT"


def _listed(root):
    """(capability name, its listed ids, its requirement ids or None when it is not codified) of each capability under
    `root`."""
    for path in sorted((pathlib.Path(root) / "spec" / "capabilities").glob("*.md")):
        data, _ = frontmatter(path.read_text())
        listed = data.get("unbuilt") or []
        listed = [str(one).strip() for one in listed] if isinstance(listed, list) else [str(listed)]
        if str(data.get("language", "")).strip() not in MARKERS:   # codified-1 or codified-2
            yield path.stem, listed, None
            continue
        have = {r.id for g in capability(path).groups for r in g.requirements}
        yield path.stem, listed, have


def unbuilt(root):
    """{capability: {r<n>, ...}} of the listed ids each codified capability has a requirement for."""
    found = {}
    for name, listed, have in _listed(root):
        ids = {one for one in listed if one in (have or ())}
        if ids:
            found[name] = ids
    return found


def problems(root):
    """One line for each listed id the capability has no requirement for, and one for each capability that is not
    codified and lists ids."""
    out = []
    for name, listed, have in _listed(root):
        if have is None:
            out += ["%s: unbuilt is given on a capability that is not codified" % name] if listed else []
        else:
            out += ["%s: unbuilt %s is no requirement of the capability" % (name, one) for one in listed
                    if one not in have]
    return out


def with_unbuilt(text, ids):
    """A capability file's text with `ids` appended to its `unbuilt: [...]`, once each, in the order given; the key is
    written after `retired:` (else last in the frontmatter) when the file has none (workflow simplification plan 4,
    D6)."""
    head_end = text.find("\n---", 4)
    head = text[:head_end]
    found = re.search(r"(?m)^unbuilt:[ \t]*\[(.*)\][ \t]*$", head)
    had = [one.strip() for one in found.group(1).split(",") if one.strip()] if found else []
    listed = "unbuilt: [%s]" % ", ".join(list(dict.fromkeys(had + list(ids))))
    if found:
        return text[:found.start()] + listed + text[found.end():]
    after = re.search(r"(?m)^retired:.*$", head)
    at = after.end() if after else head_end
    return text[:at] + "\n" + listed + text[at:]


def without_unbuilt(text, ids):
    """A capability file's text with `ids` taken out of its `unbuilt: [...]` (plan 4 review, B1); a file with no
    `unbuilt:` is given back as it is."""
    head_end = text.find("\n---", 4)
    found = re.search(r"(?m)^unbuilt:[ \t]*\[(.*)\][ \t]*$", text[:head_end])
    if not found:
        return text
    kept = [one.strip() for one in found.group(1).split(",") if one.strip() and one.strip() not in set(ids)]
    return text[:found.start()] + "unbuilt: [%s]" % ", ".join(kept) + text[found.end():]


def strict(root):
    """False when `$SHOPSYSTEM_UNBUILT_NONSTRICT` names `root` (resolved), else True."""
    named = os.environ.get(NONSTRICT)
    return not named or pathlib.Path(named).resolve() != pathlib.Path(root).resolve()


def mark(items, root):
    """An xfail on each scenario item whose feature's capability lists one of the item's r<n> marks, strict unless
    `strict(root)` says not."""
    import pytest
    found = unbuilt(root)
    if not found:
        return
    hard = strict(root)
    for item in items:
        scenario = getattr(getattr(item, "function", None), "__scenario__", None)
        if scenario is None:
            continue
        cap = pathlib.Path(scenario.feature.filename).stem
        ids = sorted(tag for tag in scenario.tags if tag in found.get(cap, ()))
        if ids:
            item.add_marker(pytest.mark.xfail(
                strict=hard, reason="unbuilt: %s" % ", ".join("%s#%s" % (cap, one) for one in ids)))


def unbuilt_lines(feature, root):
    """The line numbers of `feature` (features/<cap>.feature) that belong to a scenario of an unbuilt requirement, from
    its tag line to the next scenario's: `features vocab --check` wants no handler for their steps."""
    feature = pathlib.Path(feature)
    ids = unbuilt(root).get(feature.stem, set())
    out, inside = set(), False
    for n, line in enumerate(feature.read_text().splitlines() if ids and feature.is_file() else [], 1):
        if line.strip().startswith("@"):
            inside = bool(ids & {tag.lstrip("@") for tag in line.split()})
        if inside:
            out.add(n)
    return out
