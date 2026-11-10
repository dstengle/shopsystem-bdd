"""The 4.0.0 upgrade step "the controlled language 4" (migration-tools g61; the CNL 4 design, I29 and call 15). `plan`
computes every change and writes none. It rewrites only what is mechanical:
- each file's marker `language: codified-1` to `language: codified-2` (`spec/index.md`, every capability,
  `spec/universal.md`), and `spec/index.md` given one when it has none;
- `imports: [cli]` into `spec/index.md` when a line uses a word of the CLI pack;
- `(verb)` to `(verb, action)` for a verb no line uses in a While clause or a relative clause, and to `(verb, state)`
  for one the lines use only there; a verb used both ways is left for a session and named (v_t14).
`notes` is what it cannot reword, by file and id, read off the rewritten spec laid on a copy of `spec/`
(migrate_upgrade_cnl4_report). It rewords no requirement."""
import re
import shutil
import tempfile
from pathlib import Path

import migrate_upgrade_cnl4_report as report
import spec_frames
import spec_lexicon
import spec_packs
from migrate_upgrade_frames import LABEL, sources
from migrate_upgrade_ids import Changes

NAME = report.NAME
OLD, NEW = "language: codified-1", "language: codified-2"
FRONT = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
REQ = re.compile(r"^- \[([rU][1-9]\d*)\] (\S.*)$", re.MULTILINE)
RELATIVE = r"\b(?:that|which|who)\s+(?:(?:does|do)\s+not\s+)?"


def files(root):
    """The spec files a marker is read from, relative to root: the index, the universal conditions, the capabilities."""
    out = [rel for rel in ("spec/index.md", "spec/universal.md") if (root / rel).is_file()]
    return out + [p.relative_to(root).as_posix() for p in sorted((root / "spec/capabilities").glob("*.md"))]


def front(text, edit):
    """`text` with its frontmatter given to `edit` (frontmatter text -> frontmatter text); no frontmatter, as it was."""
    found = FRONT.match(text)
    return "---\n%s---\n%s" % (edit(found.group(1)), text[found.end():]) if found else text


def remarked(text, index=False):
    """`text` with `language: codified-1` written `codified-2`; the index given the marker when it has none."""
    def edit(head):
        if re.search(r"^language:", head, re.MULTILINE):
            return re.sub(r"^%s[ \t]*$" % re.escape(OLD), NEW, head, flags=re.MULTILINE)
        return head + NEW + "\n" if index else head
    return front(text, edit)


def imported(text):
    """The index's text importing the CLI pack, after any pack it imports already."""
    def edit(head):
        found = spec_packs.IMPORTS.search(head)
        if not found:
            return head + "imports: [cli]\n"
        names = [n.strip() for n in found.group("names").split(",") if n.strip()]
        return head if "cli" in names else (head[:found.start("names")] + ", ".join(names + ["cli"])
                                             + head[found.end("names"):])
    return front(text, edit)


def lines(root, rels):
    """(file, id, text) of every requirement and universal condition the files hold."""
    return [(rel, m.group(1), m.group(2)) for rel in rels for m in REQ.finditer((root / rel).read_text())]


def cli_words():
    """The words of the CLI pack a line may use: each term, its plural, a verb's forms."""
    path = spec_packs.path_of(Path("."), "cli")
    out = set()
    for t in spec_packs.terms(path, "grammar/packs/cli.md") if path else []:
        out |= {t.term, t.plural or t.term + "s"} | set(t.forms)
        if t.category == "event":
            out.add(spec_frames.s3(t))
    return out


def uses(text, words):
    return any(re.search(r"(?<![\w`-])%s(?![\w`-])" % re.escape(w), text) for w in words)


def while_clause(text):
    """The words of a line's While clause: from "While" to its comma before "when", "if" or the main clause."""
    found = re.match(r"While (.*?), (?:when|if) ", text) or re.match(r"While (.*), .*? shall ", text)
    return found.group(1) if found else ""


def stative(text, forms):
    """(whether the line uses one of a verb's `forms` as a state, whether it uses one as an action): a state in its
    While clause or after "that", "which" or "who"; an action anywhere else."""
    pattern = r"(?<![\w`-])(?:%s)(?![\w`-])" % "|".join(re.escape(f) for f in sorted(forms, key=len, reverse=True))
    head = while_clause(text)
    state = action = False
    for m in re.finditer(pattern, text):
        inside = m.start() < len("While ") + len(head) and text.startswith("While ")
        relative = re.search(RELATIVE + r"$", text[:m.start()])
        state, action = state or bool(inside or relative), action or not (inside or relative)
    return state, action


def aspects(root, said):
    """{verb: `action` or `state`} for each verb of the lexicon whose entry says no aspect, and the notes of those
    that the lines use both ways (v_t14)."""
    out, notes = {}, []
    for t in spec_lexicon.read(root).of("event"):
        if t.aspect or t.label != "verb":
            continue
        forms = {t.term, t.term.split()[0], spec_frames.s3(t)} | set(t.forms)
        state = [i for _, i, text in said if stative(text, forms)[0]]
        action = [i for _, i, text in said if stative(text, forms)[1]]
        if state and action:
            notes.append("%s: v_t14 %s, %s: a state in %s and an action in %s; write (verb, state) or (verb, action)"
                         % (NAME, t.term, t.where, ", ".join(state), ", ".join(action)))
        else:
            out[t.term] = "state" if state else "action"
    return out, notes


def aspected(text, heading, chosen):
    """`text` with each `(verb)` entry of its `## <heading>` section given the aspect `chosen` says."""
    out, inside = [], False
    for line in text.splitlines(True):
        if line.startswith("## "):
            inside = line[3:].strip() == heading
        found = LABEL.match(line) if inside else None
        term = found and re.match(r"- \*\*(.+?)\*\*", line).group(1)
        if found and found.group(2).strip() == "verb" and term in chosen:
            line = line[:found.start(2)] + "verb, " + chosen[term] + line[found.end(2):]
        out.append(line)
    return "".join(out)


def plan(root):
    root = Path(root)
    changes = Changes()
    changes.notes = []
    rels = files(root)
    if not any(re.search(r"^%s[ \t]*$" % re.escape(OLD), (root / r).read_text(), re.MULTILINE) for r in rels):
        return changes
    said = lines(root, rels)
    chosen, changes.notes = aspects(root, said)
    for rel in rels:
        text = remarked((root / rel).read_text(), rel == "spec/index.md")
        if rel == "spec/index.md" and any(uses(t, cli_words()) for _, _, t in said):
            text = imported(text)
        for where, heading in sources(root):
            text = aspected(text, heading, chosen) if where == rel else text
        if text != (root / rel).read_text():
            changes.texts[rel] = text
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp)
        shutil.copytree(root / "spec", copy / "spec")
        for rel, text in changes.texts.items():
            (copy / rel).write_text(text)
        changes.notes += report.notes(copy, lines(copy, rels))
    return changes
