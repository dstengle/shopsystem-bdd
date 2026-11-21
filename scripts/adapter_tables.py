"""The operation tables of an adapter contract's TOML text (b355), changed as text so that every other line, comment
and order of the contract is kept: an operation's tables are the `[operations."<service>.<operation>"]` header and
each `[operations."<service>.<operation>".<key>]` under it, each with the lines after it up to the next table.

`table` gives an operation's tables, `without` takes them out, `with_table` puts one in (in place of the operation's
own, after the contract's last operation table, else at its end), `listed` puts an operation into or out of
`[unexposed]`'s `operations`, and `one` reads the text `work line --expose` is given: one operation's tables."""
import re
import tomllib

import adapter_cli
from shop_refused import Refused

HEAD = re.compile(r'^\[\s*operations\s*\.\s*"([^"]+)"')
TABLE = re.compile(r"^\[")
UNEXPOSED = re.compile(r"(?ms)^\[unexposed\][ \t]*\n(.*?)(?=^\[|\Z)")
LISTED = re.compile(r"(?ms)^operations\s*=\s*\[.*?\]")
IDENT = re.compile(r"^[a-z][a-z -]*\.[a-z][a-z -]*$")


def _segments(text):
    """[[operation or "" (another table) or None (before any table), lines]] of `text`."""
    out = [[None, []]]
    for line in text.split("\n"):
        if TABLE.match(line):
            found = HEAD.match(line)
            out.append([found.group(1) if found else "", [line]])
        else:
            out[-1][1].append(line)
    return out


def _trimmed(lines):
    lines = list(lines)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _joined(segments):
    text = "\n".join(line for _, lines in segments for line in lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip("\n")
    return text + "\n" if text else ""


def operations(text):
    """The operations whose tables `text` holds, in order."""
    return list(dict.fromkeys(ident for ident, _ in _segments(text) if ident))


def table(text, ident):
    """The text of `ident`'s tables in `text` (no blank line at its end), or None."""
    return "\n".join(line for i, seg in _segments(text) if i == ident for line in _trimmed(seg)) or None


def without(text, ident):
    """`text` without `ident`'s tables."""
    return _joined([s for s in _segments(text) if s[0] != ident])


def with_table(text, tables):
    """`text` with `tables` (one operation's) in place of that operation's own, after the last operation table."""
    ident = operations(tables)[0]
    segments = [s for s in _segments(text) if s[0] != ident]
    at = max((n for n, (i, _) in enumerate(segments) if i), default=len(segments) - 1)
    segments[at] = [segments[at][0], _trimmed(segments[at][1]) + ([""] if any(segments[at][1]) else [])]
    segments.insert(at + 1, [ident, tables.strip("\n").split("\n") + [""]])
    return _joined(segments)


def unexposed(text):
    """The operations `[unexposed]` lists in `text`."""
    try:
        return list((tomllib.loads(text).get("unexposed") or {}).get("operations") or [])
    except tomllib.TOMLDecodeError as why:
        raise Refused("%s does not read: %s" % (adapter_cli.PATH, why)) from None


def listed(text, ident, present):
    """`text` with `ident` in `[unexposed]`'s `operations` (`present`) or out of it; the table made when missing."""
    names = unexposed(text)
    if (ident in names) == present:
        return text
    names = [n for n in names if n != ident] + ([ident] if present else [])
    line = "operations = [%s]" % ", ".join('"%s"' % n for n in names)
    section = UNEXPOSED.search(text)
    if section is None:
        return (text.rstrip("\n") + "\n\n" if text.strip() else "") + "[unexposed]\n%s\n" % line
    body = section.group(1)
    found = LISTED.search(body)
    body = body[:found.start()] + line + body[found.end():] if found else line + "\n" + body
    return text[:section.start(1)] + body + text[section.end(1):]


def one(text):
    """(operation, its tables' text) of the text `--expose` is given: the tables of one operation, `[operations."<service>.<operation>"]` with its
    `command` (or `hook`) and its `[operations."<service>.<operation>".parameters]`; anything else refused."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as why:
        raise Refused("work line: the operation table does not read as TOML: %s" % why) from None
    ops = data.get("operations")
    found = operations(text)
    stray = [line for i, seg in _segments(text) if not i for line in seg if line.strip() and not line.startswith("#")]
    if set(data) != {"operations"} or not isinstance(ops, dict) or len(ops) != 1 or len(found) != 1 or stray:
        raise Refused('work line: --expose takes the tables of one operation, `[operations."<service>.<operation>"]` '
                      'with its command and its parameters, and nothing else')
    ident = found[0]
    if not IDENT.match(ident):
        raise Refused("work line: the operation table %s does not name an operation `<service>.<operation>`" % ident)
    adapter_cli.parse(text, "the operation table %s" % ident)
    if not (ops[ident].get("command") or ops[ident].get("hook")):
        raise Refused("work line: the operation table %s has no command" % ident)
    return ident, table(text, ident)
