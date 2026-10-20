"""migrate's reading of the old ledger, spec/decisions.md: a decision file for each entry (migration-tools r2, r11, r13, r17)."""
import re

from migrate_layout import load_model, tracked

LEDGER = "spec/decisions.md"
ENTRY = re.compile(r"^## decision/(?:(?P<number>\d+)-)?(?P<slug>[\w-]+)\s*$")
FIELD = re.compile(r"^(date|source|supersedes|revisit_when):\s*(.*)$")     # an entry's fields, as the ledger's form gives them


def ledger_entries(plan, text):
    """(number, slug, paragraphs, fields, heading) for each `## decision/<nnnn>-<slug>` or `## decision/<slug>` entry
    of the ledger; an entry with no number is numbered in ledger order from one above the ledger's highest number
    (r13). Each `## ` heading begins an entry; one in another form, one there twice, and text before the first but a
    `# ` title line, is a change migrate cannot make."""
    entries, current, outside, title = [], None, [], None
    for line in text.splitlines():
        if line.startswith("## "):
            m = ENTRY.match(line)
            current = [m.group("number"), m.group("slug"), [], line.strip()] if m else [None, None, [], line.strip()]
            if m and any(e[:2] == current[:2] for e in entries):
                plan.failures.append("could not replace the ledger entry `%s`, which is there twice in %s"
                                     % (line.strip(), LEDGER))
            elif m:
                entries.append(current)
            else:
                plan.failures.append("could not replace the ledger entry `%s` of %s: its heading is not "
                                     "`## decision/<nnnn>-<slug>` or `## decision/<slug>`" % (line.strip(), LEDGER))
        elif current is not None:
            current[2].append(line)
        elif line.startswith("# ") and not outside and not title:
            title = line        # the ledger's title, which the decision files' index replaces: dropped
        elif line.strip():
            outside.append(line.strip())
    if outside:
        plan.failures.append('could not replace the ledger text "%s" outside its entries in %s' % (" ".join(outside), LEDGER))
    highest = max((int(e[0]) for e in entries if e[0]), default=0)
    out = []
    for entry in entries:
        if entry[0] is None:
            highest += 1
            entry[0] = "%04d" % highest
    for number, slug, lines, heading in entries:
        paragraphs, fields, current = [], {}, []
        for line in lines + [""]:
            m = FIELD.match(line)
            if m:
                fields[m.group(1)] = m.group(2).strip()
            if line.strip() and not m:
                current.append(line.rstrip())
            elif current:
                paragraphs.append(current)
                current = []
        out.append((number, slug, paragraphs, fields, heading))
    return out


def quoted(plan, key, value):
    """`value` in quotes that model's frontmatter reader takes off again, giving `value` as it is (it reads no escapes,
    so the quote is the one that does); None when neither quote does."""
    model = load_model()
    for quote in '"\'':
        text = "%s%s%s" % (quote, value, quote)
        if model.frontmatter("---\n%s: %s\n---\n" % (key, text))[0].get(key) == value:
            return text
    plan.failures.append("could not write %s: %s so that model reads it as it is" % (key, value))
    return None


def supersedes_of(plan, fields):
    """(the id of the decision an entry supersedes, its qualifier as written) or (None, None): the reference ends at
    the first whitespace, the rest is the qualifier (r17)."""
    parts = fields.get("supersedes", "").split(None, 1)
    if not parts:
        return None, None
    return plan.renamed.get(parts[0], parts[0]), (parts[1] if len(parts) > 1 else None)


def decision_text(plan, slug, paragraphs, fields, superseded=False):
    """The decision file of an entry: its first paragraph the summary, every paragraph its Decision, its supersedes
    (by the new id of the entry it names, its qualifier going to `by` after the source) and revisit_when where it has
    them, and the status superseded where another entry supersedes it."""
    summary = " ".join(line.strip() for line in paragraphs[0]) if paragraphs else ""
    decision = "\n\n".join("\n".join(p) for p in paragraphs)
    extra, by = "", fields.get("source", "")
    target, qualifier = supersedes_of(plan, fields)
    if target:
        extra += "supersedes: %s\n" % target
        if qualifier:
            by += "; supersedes %s %s" % (target, qualifier)
    if fields.get("revisit_when"):
        extra += "revisit_when: %s\n" % quoted(plan, "revisit_when", fields["revisit_when"])
    return ("---\nid: design-decision/%s/%s\nsummary: %s\ndate: %s\nstatus: %s\nby: %s\n%s---\n\n# %s\n\n"
            "## Decision\n%s\n" % (plan.context, slug, quoted(plan, "summary", summary), fields.get("date", ""),
                                  "superseded" if superseded else "accepted", quoted(plan, "by", by), extra, slug, decision))


def plan_ledger(plan):
    if LEDGER not in tracked(plan.root):
        return
    entries = ledger_entries(plan, plan.read(LEDGER))
    for number, slug, _, _, heading in entries:
        new = "design-decision/%s/%s" % (plan.context, slug)
        plan.renamed["decision/%s-%s" % (number, slug)] = new
        if heading == "## decision/%s" % slug:       # an entry migrate numbered is also named without its number
            plan.renamed["decision/%s" % slug] = new
    superseding = {supersedes_of(plan, fields)[0] for _, _, _, fields, _ in entries}
    for number, slug, paragraphs, fields, heading in entries:
        path = "spec/decisions/%s-%s.md" % (number, slug)
        plan.created[path] = "the ledger entry `%s`" % heading
        plan.texts[path] = decision_text(plan, slug, paragraphs, fields,
                                         plan.renamed["decision/%s-%s" % (number, slug)] in superseding)
    plan.removes.append(LEDGER)
