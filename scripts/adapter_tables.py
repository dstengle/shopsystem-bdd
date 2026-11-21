"""The operation tables of an adapter contract's TOML text (b355), changed as text so that every other line, comment
and order of the contract is kept: an operation's tables are the `[operations."<service>.<operation>"]` header and
each `[operations."<service>.<operation>".<key>]` under it, each with the lines after it up to the next table.

`table` gives an operation's tables, `without` takes them out, `with_table` puts one in (in place of the operation's
own, after the contract's last operation table, else at its end), `listed` puts an operation into or out of
`[unexposed]`'s `operations`, `one` reads the text `work line --expose` is given: one operation's tables, and `of`
writes them from a domain model's operation when it is given the operation alone (b482, the operation-table form)."""
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


EXAMPLES = {"text": "a %s", "number": 1, "time": "2026-01-01", "version": "1.0.0"}


def _program(contract, service):
    """The command's first word: the one of the contract's other operations of `service`, else `service`."""
    for ident in operations(contract):
        if ident.rpartition(".")[0] == service:
            found = re.search(r'(?m)^command\s*=\s*"(\S+)', table(contract, ident))
            if found:
                return found.group(1)
    return service


def _example(param):
    """An example of the parameter's type: its first value, its object's name, else EXAMPLES' of its type."""
    if param.values:
        return param.values[0]
    if param.targets:
        return "%s-1" % param.targets[0]
    found = EXAMPLES.get(param.type, EXAMPLES["text"])
    return found % param.name if isinstance(found, str) and "%s" in found else found


def of(op, contract=""):
    """The operation-table form of the domain model's operation `op`: its command named after the operation (the
    program the contract's other operations of its service are requested by), and each parameter an option named after
    it with an example of its type (a flag `flag = true`)."""
    ident = "%s.%s" % (op.service, op.name)
    lines = ['[operations."%s"]' % ident, 'command = "%s %s"' % (_program(contract, op.service), op.name)]
    if op.parameters:
        lines.append('[operations."%s".parameters]' % ident)
    for param in op.parameters:
        option = "--" + "-".join(param.name.split())
        spec = "flag = true" if param.type == "flag" else "example = %s" % _toml(_example(param))
        lines.append('%s = { option = "%s", %s }' % (_key(param.name), option, spec))
    return "\n".join(lines)


def _key(name):
    return name if re.match(r"^[A-Za-z0-9_-]+$", name) else '"%s"' % name


def _toml(value):
    return str(value) if isinstance(value, int) else '"%s"' % str(value).replace("\\", "\\\\").replace('"', '\\"')
