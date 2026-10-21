"""migrate's changes to spec/ and features/ (ids, Behaviour numbers, @holding), and its rewrite of what names a moved
file or a renamed id (migration-tools r3, r4, r5, r10)."""
import posixpath
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from migrate_layout import load_model, tracked, with_id

BULLET_ID = re.compile(r"^- \[r(\d+)\]")


def number_behaviour(text, retired):
    """`text` with each Behaviour bullet that has no `[r<n>]` numbered, from one above the highest id ever used."""
    lines = text.split("\n")
    inside, bullets = False, []
    for i, line in enumerate(lines):
        if line.startswith("## "):
            inside = line[3:].strip().lower() == "behaviour"
        elif inside and line.startswith("- "):
            bullets.append(i)
    used = [int(m.group(1)) for i in bullets for m in [BULLET_ID.match(lines[i])] if m]
    highest = max(used + retired, default=0)
    for i in bullets:
        if not BULLET_ID.match(lines[i]):
            highest += 1
            lines[i] = "- [r%d] %s" % (highest, lines[i][2:])
    return "\n".join(lines)


def plan_capabilities(plan):
    model = load_model()
    for rel in tracked(plan.root):
        if rel.startswith("spec/capabilities/") and rel.endswith(".md"):
            text = plan.read(rel)
            data, _ = model.frontmatter(text)
            retired = [int(str(r).lstrip("r")) for r in model.as_list(data.get("retired"))]
            full = "capability/%s/%s" % (plan.context, Path(rel).stem)
            short = "capability/%s" % Path(rel).stem
            if data.get("id") == short:         # the short form becomes the full one, and references follow (r9, r5)
                text = re.sub(r"^id:.*$", "id: " + full, text, count=1, flags=re.MULTILINE)
                plan.renamed[short] = full
            text = re.sub(r"^formulated_as:.*\n", "", text, count=1, flags=re.MULTILINE)      # model reads no formulated_as (r6)
            plan.texts[rel] = with_id(number_behaviour(text, retired), full)


def drop_holding(text):
    out = []
    for line in text.split("\n"):
        if line.strip().startswith("@") and "@holding" in line.split():
            indent = line[:len(line) - len(line.lstrip())]
            line = indent + " ".join(t for t in line.split() if t != "@holding")
        out.append(line)
    return "\n".join(out)


def plan_holding(plan):
    """Deprecate each @holding scenario as `features deprecate` does (on a copy outside the repository), then drop
    its @holding tag."""
    model = load_model()
    features_script = str(Path(__file__).resolve().with_name("features"))
    for rel in tracked(plan.root):
        if not (rel.startswith("features/") and rel.endswith(".feature")):
            continue
        text = plan.read(rel)
        held = [title for title, tags, _ in model.scenarios(text) if "@holding" in tags]
        if not held:
            continue
        with tempfile.TemporaryDirectory() as scratch:
            copy = Path(scratch) / rel
            copy.parent.mkdir(parents=True)
            copy.write_text(text)
            for title in held:
                done = subprocess.run([sys.executable, features_script, "deprecate", title, "--for-removal", "--file", rel],
                                      cwd=scratch, capture_output=True, text=True)
                if done.returncode != 0:
                    plan.failures.append("could not deprecate %r in %s: %s" % (title, rel, (done.stdout + done.stderr).strip()))
            plan.texts[rel] = drop_holding(copy.read_text())


def plan_index(plan):
    if "spec/index.md" in tracked(plan.root):
        plan.texts["spec/index.md"] = with_id(plan.read("spec/index.md"), "bounded-context/" + plan.context)


LINK = re.compile(r"(\]\()([^)\s#]+)((?:#[^)\s]*)?\))")


def rewrite_text(plan, old_path, new_path, text):
    """`text`, the file at `old_path` that will be at `new_path`, with each reference to what moved or was renamed
    made to name its new place: a link (relative to the file), a repository path, an id in the frontmatter."""
    def link(m):
        target = m.group(2)
        if re.match(r"^([a-z][a-z0-9+.-]*:|/)", target):
            return m.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(old_path), target))
        if resolved not in plan.moves:
            return m.group(0)
        relative = posixpath.relpath(plan.moves[resolved], posixpath.dirname(new_path) or ".")
        return m.group(1) + relative + m.group(3)
    text = LINK.sub(link, text)
    if plan.moves:
        paths = "|".join(re.escape(p) for p in sorted(plan.moves, key=len, reverse=True))
        text = re.sub(r"(?<![\w./-])(%s)(?![\w/-])" % paths, lambda m: plan.moves[m.group(1)], text)
    if text.startswith("---\n") and plan.renamed:
        end = text.find("\n---", 4)
        head = text[:end] if end > 0 else ""
        ids = "|".join(re.escape(i) for i in plan.renamed)
        if head:
            head = re.sub(r"(?<![\w./-])(%s)(?![\w-])" % ids, lambda m: plan.renamed[m.group(1)], head)
            text = head + text[end:]
    return text


def plan_references(plan):
    """Rewrite what names a moved file or a renamed id, in every tracked text file."""
    for old in tracked(plan.root):
        if old in plan.removes:
            continue
        final = plan.moves.get(old, old)
        try:
            text = plan.texts.get(final) if final in plan.texts else plan.read(old)
        except UnicodeDecodeError:
            continue
        rewritten = rewrite_text(plan, old, final, text)
        if rewritten != text:
            plan.texts[final] = rewritten
    for path in plan.created:       # a file migrate wrote is tracked once the run has added it (r16): its references too
        if path in plan.texts:
            plan.texts[path] = rewrite_text(plan, path, path, plan.texts[path])
