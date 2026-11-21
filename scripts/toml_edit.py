"""One key of a TOML file set in its text (b462): the key's entry replaced where it stands in its own table, or added
after the table's last entry, the table added at the end when the file has none of it; every comment, other key and
table kept as written. A table and a key are paths of keys (`("review",)`, `("constructs", "when")`; `()` the top level, its
keys before the first table). Standard library only."""
import json
import re
import tomllib

BARE = re.compile(r"[A-Za-z0-9_-]+")
HEADER = re.compile(r"^\s*\[")


def name(path):
    """A path of keys as TOML writes it: `prices."claude-x.1"`."""
    return ".".join(k if BARE.fullmatch(k) else json.dumps(k) for k in path)


def literal(value):
    """A value as a TOML literal: a string, a whole number, a number, a boolean, a list or an inline table of them."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float, str)):
        return json.dumps(value)
    if isinstance(value, list):
        return "[%s]" % ", ".join(literal(v) for v in value)
    if isinstance(value, dict):
        return "{ %s }" % ", ".join("%s = %s" % (name((k,)), literal(v)) for k, v in value.items())
    raise TypeError("no TOML literal of %r" % (value,))


def _path(data):
    """The one path of keys a parsed header or entry holds (`{"a": {"b": ...}}`: ("a", "b"))."""
    out = []
    while isinstance(data, dict) and len(data) == 1:
        key, data = next(iter(data.items()))
        out.append(key)
    return tuple(out)


def _header(line):
    """The table path of a `[table]` line; None of an array of tables or a line that is no header."""
    if not HEADER.match(line) or line.lstrip().startswith("[["):
        return None
    try:
        return _path(tomllib.loads(line + "\n"))
    except tomllib.TOMLDecodeError:
        return None


def _entries(lines, start, end):
    """[(first, past, key path)] of the entries between two headers, an entry's lines as many as make it parse."""
    out, i = [], start
    while i < end:
        if not lines[i].strip() or lines[i].lstrip().startswith("#"):
            i += 1
            continue
        for j in range(i + 1, end + 1):
            try:
                found = tomllib.loads("\n".join(lines[i:j]) + "\n")
            except tomllib.TOMLDecodeError:
                continue
            out.append((i, j, _path(found)))
            break
        else:
            return out
        i = j
    return out


def _regions(lines):
    """{table path: (first line, past line)} of each table's body; () the top level's."""
    heads = [i for i, line in enumerate(lines) if HEADER.match(line)]
    out = {(): (0, heads[0] if heads else len(lines))}
    for n, i in enumerate(heads):
        path = _header(lines[i])
        if path is not None and path not in out:
            out[path] = (i + 1, heads[n + 1] if n + 1 < len(heads) else len(lines))
    return out


def with_key(text, table, key, value):
    """`text` with the key `key` of the table `table` set to `value`."""
    lines = text.splitlines()
    entry = "%s = %s" % (name(key), literal(value))
    regions = _regions(lines)
    if tuple(table) not in regions:
        while lines and not lines[-1].strip():
            lines.pop()
        lines += ([""] if lines else []) + ["[%s]" % name(table), entry]
    else:
        start, end = regions[tuple(table)]
        entries = _entries(lines, start, end)
        same = [(i, j) for i, j, path in entries if path == tuple(key)]
        if same:
            i, j = same[0]
            lines[i:j] = [entry]
        elif entries:
            lines.insert(entries[-1][1], entry)
        else:
            at = end
            if end < len(lines):            # the comments right above the next header are that table's
                while at > start and lines[at - 1].lstrip().startswith("#"):
                    at -= 1
            while at > start and not lines[at - 1].strip():
                at -= 1
            lines[at:at] = [entry] if at == start or end == len(lines) and at == end else [entry, ""]
    out = "\n".join(lines) + "\n"
    read = tomllib.loads(out)
    for part in tuple(table) + tuple(key):
        read = read[part]
    if read != value:
        raise ValueError("%s did not read back as written" % name(tuple(table) + tuple(key)))
    return out
