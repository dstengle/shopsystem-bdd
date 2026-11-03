"""The reading of scripts/model: the forms of the model's files (frontmatter, sections, bullets, scenarios, glossary
bullets). The 0.29 Behaviour lines and their EARS shape are model_legacy's. Standard library only."""

import re
from pathlib import Path

RID = re.compile(r"^\[r(\d+)\]\s*")
ENTRY = re.compile(r"^\*\*(?P<term>[^*]+?)\*\*(?: \((?P<cat>[^)]*)\))?: (?P<rest>.+)$")   # a glossary bullet, after "- "
CATEGORY = re.compile(r"^(?:actor|kind|event|value|resource(?:, (?:exclusive|counted by `[^`]+`))?"
                      r"|(?P<of>attribute|condition) of (?P<kind>\S.*)|relation (?P<k1>\S.*?) → (?P<k2>\S.*))$")
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
    """(term, [avoided words]) of a bullet written **<term>** (<category>): <definition>. Not: <word>, <word>.; None
    otherwise. The category is optional here (0.29 entries have none) and, in design model v5's typed form, one of
    actor, kind, event, value, resource (exclusive or counted by `<code>`), attribute or condition of <kind>, or
    relation <kind> → <kind>. Only the term and Not: are read, backticks dropped (spec_lexicon reads the rest). A word
    with entries for several kinds is defined once: the entry with a sentence is the term, and an attribute or
    condition entry that opens with `Values:` or `Means:` is read as `<term> of <kind>`; a relation is always read as
    `<term> of <kind> to <kind>`. So one word in several kinds has one entry as a term (v_t2)."""
    m = ENTRY.match(bullet)
    if not m or not m.group("rest").endswith("."):
        return None
    definition, _, avoided = m.group("rest").partition(". Not: ")
    words = [" ".join(w.split()).lower() for w in avoided[:-1].split(",")] if avoided else []
    word = m.group("term").replace("`", "").strip()
    if not definition.strip(" .") or not word or any(not w for w in words):
        return None
    if m.group("cat") is not None:
        cat = CATEGORY.match(m.group("cat").strip())
        if not cat:
            return None
        if cat.group("of") and re.match(r"(?:Values|Means): ", definition):
            word = f"{word} of {cat.group('kind').strip()}"
        elif cat.group("k1"):
            word = f"{word} of {cat.group('k1').strip()} to {cat.group('k2').strip()}"
    return word, words


def mention(word):
    """A whole-word, any-case match of <word>, a plural "s" allowed; a hyphen joins a word."""
    body = r"\s+".join(re.escape(w) for w in word.split())
    return re.compile(rf"(?<![\w-]){body}s?(?![\w-])", re.IGNORECASE)


def decision_files(root):
    """The decision files: every spec/decisions/*.md but the generated index.md and a README.md (r19)."""
    return [p for p in sorted((Path(root) / DECISIONS).glob("*.md")) if p.name not in ("index.md", "README.md")]
