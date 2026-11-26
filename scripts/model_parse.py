"""The reading of scripts/spec: the forms of the model's files (frontmatter, sections, scenarios). A spec file's
groups and term entries are spec_read's and spec_lexicon's. Standard library and the plumbing's frontmatter reader."""

import re
from pathlib import Path

# the frontmatter reader, the plumbing's (b614): model_parse.frontmatter is plumbing.frontmatter's
from plumbing.frontmatter import frontmatter, scalar  # noqa: F401

DECISIONS = Path("spec") / "decisions"


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


def mention(word):
    """A whole-word, any-case match of <word>, a plural "s" allowed; a hyphen joins a word."""
    body = r"\s+".join(re.escape(w) for w in word.split())
    return re.compile(rf"(?<![\w-]){body}s?(?![\w-])", re.IGNORECASE)


def decision_files(root):
    """The decision files: every spec/decisions/*.md but the generated index.md and a README.md (r19)."""
    return [p for p in sorted((Path(root) / DECISIONS).glob("*.md")) if p.name not in ("index.md", "README.md")]
