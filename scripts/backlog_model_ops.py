"""A model line that restates an operation (b463): an item's operation line under a service the area declares, of
the same name as an operation the service declares, laid in place of the operation (its line and the lines indented
under it: `outcomes:`, continuations) rather than appended as a second operation of that name (v_m8); a parameter
added, renamed or removed, an outcome or a reason added. backlog_model's `merged` lays it (`restate`), its `unmerged`
puts the operation back as the model file held it before the lay (`at_base`, the batch's base, b485; else `held`,
read off git's history; `unrestate`), or takes the line out when no version held the operation (a new one). A line
that repeats the operation unchanged is a restatement too: only the base tells it from a new operation."""
import re
import subprocess
from pathlib import Path

import backlog_model_elements

OPERATION = re.compile(r"^  operation ([^(]+?)\s*\(")


def units(members):
    """[(operation name or None, [lines])] of a service's member lines: an operation's line with the lines indented
    deeper under it one unit, any other line a unit of its own."""
    out = []
    for line in members:
        found = OPERATION.match(line)
        if found:
            out.append((found.group(1).strip(), [line]))
        elif out and out[-1][0] is not None and line.strip() and len(line) - len(line.lstrip(" ")) > 2:
            out[-1][1].append(line)
        else:
            out.append((None, [line]))
    return out


def span(body, at, end, name):
    """(first, last) of the operation `name` among the member lines body[at + 1:end], or None."""
    n = at + 1
    for op, lines in units(body[at + 1:end]):
        if op == name:
            return n, n + len(lines)
        n += len(lines)
    return None


def restate(body, at, end, members):
    """Each operation of `members` the element at `at` (its members ending at `end`) declares put in place of it in
    `body`; the members left to append and the new end."""
    left = []
    for op, lines in units(members):
        found = span(body, at, end, op) if op else None
        if found is None:
            left.extend(lines)
            continue
        body[found[0]:found[1]] = lines
        end += len(lines) - (found[1] - found[0])
    return left, end


def restated(members, body, at, end):
    """The operations of `members` that the element at `at` of `body` holds exactly as `members` say them: (name,
    lines) each; the other member lines."""
    ops, rest = [], []
    for op, lines in units(members):
        found = span(body, at, end, op) if op else None
        if found is not None and body[found[0]:found[1]] == lines:
            ops.append((op, lines))
        else:
            rest.extend(lines)
    return ops, rest


def unrestate(body, at, end, header, ops, before):
    """Each of `ops` (name, lines) the element at `at` holds put back as `before` (the model lines the file held
    before the lay, or None) declares it under `header`, or taken out when `before` declares no such operation; the
    new end."""
    from backlog_model import _at, _end
    old = _at(before, header) if before is not None else None
    for op, lines in ops:
        here = span(body, at, end, op)
        was = span(before, old, _end(before, old), op) if old is not None else None
        put = before[was[0]:was[1]] if was else []
        body[here[0]:here[1]] = put
        end += len(put) - len(lines)
    return end


def at_base(path, base, header, op, lines):
    """The model lines of `path`'s fence at the commit `base` (the batch's base, which the lay was made on); None when
    that commit holds no such file or no fence. `header`, `op` and `lines` are `held`'s, unread."""
    from backlog_model import _fence
    path = Path(path)

    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    prefix = git("rev-parse", "--show-prefix").stdout.strip()
    shown = git("show", "%s:%s%s" % (base, prefix, path.name))
    if shown.returncode != 0 or "```model" not in shown.stdout:
        return None
    text, start, end = _fence(shown.stdout, path.name)
    return text[start:end]


def held(path, header, op, lines):
    """The model lines of `path`'s fence in the latest version git holds of it that does not hold the operation `op`
    of `header` as `lines` (with `op` None, the element `header` with exactly the members `lines`, b598); None when git holds no such version (the file untracked, or every version holds it)."""
    from backlog_model import _at, _end, _fence
    path = Path(path)

    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    rel = git("ls-files", "--full-name", "--error-unmatch", path.name)
    log = git("log", "--format=%H", "--", path.name) if rel.returncode == 0 else rel
    for sha in log.stdout.split() if log.returncode == 0 else ():
        shown = git("show", "%s:%s" % (sha, rel.stdout.strip()))
        if shown.returncode != 0 or "```model" not in shown.stdout:
            continue
        text, start, end = _fence(shown.stdout, path.name)
        body = text[start:end]
        if op is None:
            if not backlog_model_elements.same(body, header, lines):
                return body
            continue
        at = _at(body, header)
        found = span(body, at, _end(body, at), op) if at is not None else None
        if found is None or body[found[0]:found[1]] != lines:
            return body
    return None
