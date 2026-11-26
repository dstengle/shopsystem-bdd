"""The frontmatter reader every file of .shop/ and spec/ is read with: the YAML subset those files use, which
scripts/spec's model_parse re-exports, so the two never disagree on a file. Standard library only."""

import re


def frontmatter(text):
    """The YAML subset the model's files use: scalars, [a, b] lists and '- x' block lists."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    head, body = text[4:end], text[end + 4:].lstrip("\n")
    data, key, unread = {}, None, []
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        line = strip_comment(line)
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and key is not None and (data.get(key) is None or isinstance(data.get(key), list)):
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(scalar(m.group(1)))
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in (">", ">-", ">+", "|", "|-", "|+"):
            unread.append(key)
            data[key] = None
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [scalar(v) for v in split_list(inner)] if inner else []
        elif value == "":
            data[key] = None
        else:
            data[key] = scalar(value)
    if unread:
        data["__unread__"] = unread
    return data, body


def strip_comment(line):
    """Drop a ' # comment' that is outside quotes."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and i > 0 and line[i - 1] in " \t":
            return line[:i].rstrip()
    return line


def split_list(inner):
    out, cur, quote = [], "", None
    for ch in inner:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote, cur = ch, cur + ch
        elif ch == ",":
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    return v
