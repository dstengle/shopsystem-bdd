"""The reading of scripts/model: the forms of the model's files (frontmatter, sections, Behaviour lines, scenarios,
glossary bullets) and the EARS shape of a Behaviour line. Standard library only."""

import re
from pathlib import Path

RID = re.compile(r"^\[r(\d+)\]\s*")
ENTRY = re.compile(r"^\*\*(?P<term>[^*]+?)\*\*: (?P<rest>.+)$")    # a glossary bullet, after its "- "
DECISIONS = Path("spec") / "decisions"


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


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def expand(refs):
    """<capability>#r<a>-r<b> (or an en dash) stands for every id from a to b."""
    out = []
    for ref in refs:
        m = re.fullmatch(r"(.+)#r(\d+)\s*[-–]\s*r?(\d+)", str(ref).strip())
        if m and int(m.group(2)) <= int(m.group(3)):
            out += [f"{m.group(1)}#r{n}" for n in range(int(m.group(2)), int(m.group(3)) + 1)]
        else:
            out.append(ref)
    return out


def section(body, title):
    """The lines of a `## <title>` section, up to the next `## `."""
    out, inside = [], False
    for line in body.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower() == title.lower()
            continue
        if inside:
            out.append(line)
    return out


def bullets(lines):
    """Top-level '- ' bullets, with their continuation lines joined."""
    out = []
    for line in lines:
        if line.startswith(("- ", "* ")):
            out.append(line[2:].strip())
        elif out and line.startswith("  ") and line.strip():
            out[-1] += " " + line.strip()
    return out


TABLE_ID = re.compile(r"^\[r\d+\]$")


def behaviour_items(lines):
    """(text, lead) of each requirement of a Behaviour section: a top-level '- ' bullet, its continuation lines joined,
    or a table row whose first cell is `[r<n>]` (a row whose first cell is `r<n>` without brackets is a line with no
    id), its other cells joined by ' | '. `lead` is the sentence just before the table: a bullet with no id that ends
    in ':', or a paragraph; None when something else (a heading, a requirement, another table) comes between.
    A table's header row and separator, a '###' heading and a lead sentence are no requirements."""
    items, lead, open_bullet, paragraph, in_table = [], None, False, False, False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            open_bullet = paragraph = False
            in_table = True
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if cells and (TABLE_ID.match(cells[0]) or re.fullmatch(r"r\d+", cells[0])):
                items.append([cells[0] + " " + " | ".join(cells[1:]), lead])
            elif items and items[-1][1] is None and not RID.match(items[-1][0]) and items[-1][0].endswith(":"):
                lead = items.pop()[0]       # a bullet with no id that ends in ':' above a table leads it
            continue
        if in_table and stripped:
            lead, in_table = None, False
        if line.startswith(("- ", "* ")):
            items.append([stripped[2:].strip(), None])
            lead = None if RID.match(items[-1][0]) else items[-1][0]
            open_bullet, paragraph = True, False
        elif open_bullet and line.startswith("  ") and stripped:
            items[-1][0] += " " + stripped
            lead = None if RID.match(items[-1][0]) else items[-1][0]
        elif stripped.startswith("#"):
            lead, open_bullet, paragraph = None, False, False
        elif stripped and not line.startswith(" "):
            lead = lead + " " + stripped if paragraph else stripped
            open_bullet, paragraph = False, True
        elif not stripped:
            paragraph = False
    return [tuple(i) for i in items]


def scenarios(text):
    """(title, tags, steps) for each Scenario or Scenario Outline of a feature file."""
    out, pending, in_doc, feature_tags, steps = [], [], None, [], None
    for raw in text.splitlines():
        line = raw.strip()
        if in_doc:
            if line.startswith(in_doc):
                in_doc = None
            continue
        if line.startswith(('"""', "```")):
            in_doc = line[:3]
            continue
        if line.startswith("@"):
            pending += [t for t in line.split() if t.startswith("@")]
            continue
        m = re.match(r"^(?:Scenario(?: Outline| Template)?|Example):\s*(.*)$", line)
        if m:
            steps = []
            out.append((m.group(1).strip(), feature_tags + pending, steps))
            pending = []
        elif line.startswith("Feature:"):
            feature_tags, pending, steps = pending, [], None
        elif line.startswith(("Background:", "Examples:", "Scenarios:", "Rule:")):
            pending, steps = [], None
        elif steps is not None and re.match(r"^(?:Given|When|Then|And|But|\*)\s", line):
            steps.append(line)
    return out


def glossary_entry(bullet):
    """(term, [avoided words]) of a bullet written **<term>**: <definition>. Not: <word>, <word>.; None otherwise."""
    m = ENTRY.match(bullet)
    if not m or not m.group("rest").endswith("."):
        return None
    definition, _, avoided = m.group("rest").partition(". Not: ")
    words = [" ".join(w.split()).lower() for w in avoided[:-1].split(",")] if avoided else []
    if not definition.strip(" .") or not m.group("term").strip() or any(not w for w in words):
        return None
    return m.group("term").strip(), words


CLAUSE_RANK = {"Where": 1, "While": 2, "When": 3, "If": 3}
CLAUSE = re.compile(r"(Where|While|When|If)\b", re.IGNORECASE)


def ears(line):
    """(in a pattern, one shall and one sentence) of a Behaviour line, or of a table's lead sentence (r103, r104).

    The line is matched after removing `**` and the `[r<n>]` prefix, a code span or a double-quoted string standing
    for a word: `Where`, then `While`, then one `When` or `If ... then`, then the system and `shall` and the response.
    """
    if line is None:
        return False, False
    text = RID.sub("", line).replace("**", "")
    text = re.sub(r'`[^`]*`|"[^"]*"', "X", text).strip().rstrip(":")
    shalls = list(re.finditer(r"\bshall\b", text, re.IGNORECASE))
    plain = re.sub(r"\b(?:e\.g|i\.e|etc)\.", "X", text, flags=re.IGNORECASE)     # an abbreviation ends no sentence
    one = len(shalls) <= 1 and not re.search(r"[.!?](?=\s+\S)", plain)
    if not shalls:
        return False, one
    rest, rank = text[: shalls[0].start()].strip(), 0
    while True:
        m = CLAUSE.match(rest)
        if not m:
            break
        kw = m.group(1)
        if rank == 0 and kw not in CLAUSE_RANK:         # the line opens with its keyword capitalised; later ones may not
            return False, one
        kw = kw.capitalize()
        if CLAUSE_RANK[kw] <= rank:
            return False, one
        rank = CLAUSE_RANK[kw]
        if kw == "If":
            m = re.match(r"if .+?, then (\S.*)$", rest, re.IGNORECASE)
            if m is None:
                return False, one
            rest = m.group(1)       # what follows `then` may be no further clause: the loop refuses it
            continue
        nxt = re.search(r", (?=(?:Where|While|When|If)\b)", rest, re.IGNORECASE)
        if nxt:
            rest = rest[nxt.end():]
            continue
        cut = rest.rfind(", ")
        if cut < 0:
            return False, one
        rest = rest[cut + 2:]
        break
    if rank == 0 and not rest.startswith(("The ", "X")):
        return False, one       # a ubiquitous line names its system: "The <system>" or a code span
    return bool(rest.strip()), one


def mention(word):
    """A whole-word, any-case match of <word>, a plural "s" allowed; a hyphen joins a word."""
    body = r"\s+".join(re.escape(w) for w in word.split())
    return re.compile(rf"(?<![\w-]){body}s?(?![\w-])", re.IGNORECASE)


def decision_files(root):
    """The decision files: every spec/decisions/*.md but the generated index.md and a README.md (r19)."""
    return [p for p in sorted((Path(root) / DECISIONS).glob("*.md")) if p.name not in ("index.md", "README.md")]
