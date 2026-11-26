"""The 0.38.0 upgrade step "the domain contract" (the domain contract design, §9.6). `plan` computes every change and
writes none. What is mechanical is rewritten, read off the glossary, each capability's `## Terms` and the `##
Relations` tables (spec_lexicon's old reading) and the lines (migrate_upgrade_domain_scaffold builds the files):
- `spec/model/<context>.md`, one area named after the context: each noun an object, each attribute with its values
  and its `Transitions:` a lifecycle, each relation row and each state verb a relation, each actor of `Kind of: agent`
  an actor, one `service <tool>` per tool the lines run and one operation per command they run, named the command
  minus the tool (`notes add` -> `add`), its parameters the options the lines give it (`--title` -> `title`) and the
  thing it is run on;
- `spec/vocabulary/<context>.md` and `shared.md`: every entry moved with its `→ element` where the scaffold made one;
- `spec/adapters/cli.toml`: each operation with the command and the options it was scaffolded from;
- `imports: [cli]` -> `imports: [request]`, `## Glossary`, `## Terms` and `## Relations` taken out, each capability
  given `area: <context>`, and `spec/moves.json` written empty.
`notes` is what a session rewords, by file and id (migrate_upgrade_domain_report); no line is reworded and no id is
given. A context with `spec/model/` already is left alone, so a second run changes nothing."""
import re
from pathlib import Path

import spec_lexicon
import spec_packs
import spec_read
from model_parse import frontmatter

from upgrades import migrate_upgrade_domain_report as report
from upgrades import migrate_upgrade_domain_scaffold as scaffold
from upgrades.migrate_upgrade_ids import Changes

NAME = report.NAME
REQ = re.compile(r"^- \[([rU][1-9]\d*)\] (\S.*)$")
SECTIONS = ("Glossary", "Terms", "Relations")


def files(root):
    out = [rel for rel in ("spec/index.md", "spec/universal.md") if (root / rel).is_file()]
    return out + [p.relative_to(root).as_posix() for p in sorted((root / "spec/capabilities").glob("*.md"))]


def lines(root):
    """(file, id, text) of every requirement and universal condition, a wrapped one's continuation lines joined as
    spec_read joins them."""
    out = []
    for rel in files(root):
        for _, bullet in spec_read.items(enumerate((root / rel).read_text().splitlines())):
            found = REQ.match(bullet)
            if found:
                out.append((rel, found.group(1), found.group(2)))
    return out


def context(root):
    """(the context's path after `bounded-context/`, its last segment: the area's name)."""
    found = frontmatter((root / "spec/index.md").read_text())[0].get("id") or "bounded-context/context"
    path = str(found).partition("bounded-context/")[2] or str(found)
    return path, path.rstrip("/").rpartition("/")[2] or "context"


def without_sections(text):
    """`text` with each `## Glossary`, `## Terms` and `## Relations` section taken out, up to the next `## `."""
    out, skipping = [], False
    for line in text.splitlines(True):
        if line.startswith("## "):
            skipping = line[3:].strip() in SECTIONS
        if not skipping:
            out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "".join(out))


def reimported(text):
    def edit(found):
        names = [n.strip() for n in found.group("names").split(",") if n.strip()]
        names = list(dict.fromkeys("request" if n == "cli" else n for n in names))
        return "imports: [%s]" % ", ".join(names)
    return spec_packs.IMPORTS.sub(edit, text, count=1)


def with_area(text, area):
    """A capability's text given `area:` in its frontmatter, after its `group:` (else first), unless it has one."""
    if not text.startswith("---\n") or re.search(r"^area:", text.split("\n---", 1)[0], re.MULTILINE):
        return text
    head, sep, body = text[4:].partition("\n---")
    rows = head.split("\n")
    at = next((n + 1 for n, row in enumerate(rows) if row.startswith("group:")), 0)
    return "---\n" + "\n".join(rows[:at] + ["area: %s" % area] + rows[at:]) + sep + body


def plan(root):
    root = Path(root)
    changes = Changes()
    changes.notes = []
    if not (root / "spec/index.md").is_file() or (root / "spec/model").is_dir():
        return changes
    lexicon = spec_lexicon.read(root)
    said = lines(root)
    path, area = context(root)
    built = scaffold.Scaffold(lexicon, said, area)
    changes.texts["spec/model/%s.md" % area] = built.model(path, root)
    changes.texts["spec/vocabulary/%s.md" % area] = built.vocabulary(path, own=True)
    changes.texts["spec/vocabulary/shared.md"] = built.vocabulary(path, own=False)
    changes.texts["spec/adapters/cli.toml"] = built.contract()
    changes.texts["spec/moves.json"] = "{}\n"
    for rel in files(root):
        text = (root / rel).read_text()
        new = without_sections(text)
        if rel == "spec/index.md":
            new = reimported(new)
        elif rel.startswith("spec/capabilities/"):
            new = with_area(new, area)
        if new != text:
            changes.texts[rel] = new
    changes.notes = report.notes(lexicon, said, built)
    return changes
