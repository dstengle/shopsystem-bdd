"""The 3.0.0 upgrade step "verb frames" (migration-tools g25; design 2026-11-07-verb-frames, call 6). `plan` computes
every change and writes none:
- each term entry of `spec/index.md`'s `## Glossary` and of each capability's `## Terms` whose category is one of
  plugin 2.x's has it written as its part of speech, by `spec_lexicon.relabel` (`kind` -> `noun`, `event` -> `verb`,
  `condition of stage` -> `adjective of stage`); nothing else in a file changes;
- `notes`, read off the relabelled spec laid on a copy of `spec/`: each verb that needs a `Frame:` (v_t11) or whose `Frame:` does not read (v_t13), each
  relational condition (v_t12) and each requirement, universal conditions among them, that no longer parses, by file
  and id. It rewords no line: a session writes the frames and rewords the lines, a changed line under a new id."""
import re
import shutil
import tempfile
from pathlib import Path

import spec_grammar
import spec_lexicon
import spec_read
import spec_rgl_vocab
from migrate_upgrade_ids import Changes

NAME = "verb frames"
LABEL = re.compile(r"^(- \*\*.+?\*\*\s*\()([^)]*)(\)\s*:)")


def relabelled(text, heading):
    """`text` with each entry of its `## <heading>` section given its part of speech; other lines as they were."""
    out, inside = [], False
    for line in text.splitlines(True):
        if line.startswith("## "):
            inside = line[3:].strip() == heading
        found = LABEL.match(line) if inside else None
        label = found and spec_lexicon.relabel(found.group(2))
        out.append(line[:found.start(2)] + label + line[found.end(2):] if label else line)
    return "".join(out)


def sources(root):
    """(path relative to root, heading) of each file holding term entries."""
    out = [("spec/index.md", "Glossary")] if (root / "spec/index.md").is_file() else []
    return out + [(p.relative_to(root).as_posix(), "Terms") for p in sorted((root / "spec/capabilities").glob("*.md"))]


def frames(lexicon, outer=frozenset()):
    """Each verb with no frame (v_t11), each whose frame does not read (v_t13) and each relational condition (v_t12):
    the message names its file."""
    return ["%s: %s %s, %s" % (NAME, code, term, message) for code, term, message in spec_lexicon.problems(lexicon, outer)
            if code in ("v_t11", "v_t12", "v_t13")]


def statements(copy):
    """(file, id, text) of each requirement of a codified capability and each universal condition."""
    out = []
    for path in sorted((copy / "spec/capabilities").glob("*.md")):
        if spec_read.codified(path):
            rel = path.relative_to(copy).as_posix()
            out += [(rel, r.id, r.text) for g in spec_read.capability(path).groups for r in g.requirements]
    return out + [("spec/universal.md", u.id, u.text) for u in spec_read.universal(copy)]


def unparsed(copy):
    """Each requirement that does not parse in the relabelled spec's grammar, by file and id; a grammar that cannot
    be built (a term with no part of speech, no gf) said once."""
    out = []
    try:
        for rel, ident, text in statements(copy):
            parsed = spec_grammar.parse(copy, text)
            if parsed.tree is None:
                out.append("%s: %s %s no longer parses: %s" % (NAME, rel, ident, parsed.refusal))
    except spec_grammar.GrammarError as error:
        out.append("%s: the requirements could not be parsed: %s" % (NAME, error))
    return out


def plan(root):
    root = Path(root)
    changes = Changes()
    for rel, heading in sources(root):
        text = (root / rel).read_text()
        if relabelled(text, heading) != text:
            changes.texts[rel] = relabelled(text, heading)
    if not (root / "spec").is_dir():
        return changes
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp)
        shutil.copytree(root / "spec", copy / "spec")
        for rel, text in changes.texts.items():
            (copy / rel).write_text(text)
        changes.notes = frames(spec_lexicon.read(copy), spec_rgl_vocab.outer(copy)) + unparsed(copy)
    return changes
