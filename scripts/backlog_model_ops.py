"""A model line that restates an operation (b463): an item's operation line under a service the area declares, of
the same name as an operation the service declares, laid in place of the operation (its line and the lines indented
under it: `outcomes:`, continuations) rather than appended as a second operation of that name (v_m8); a parameter
added, renamed or removed, an outcome or a reason added. backlog_model's `merged` lays it (`restate`)."""
import re

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
