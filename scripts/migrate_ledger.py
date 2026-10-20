"""migrate's reading of the old ledger, spec/decisions.md: a decision file for each entry (migration-tools r2, r11)."""
import re

from migrate_layout import load_model, tracked

LEDGER = "spec/decisions.md"
ENTRY = re.compile(r"^## decision/(?P<number>\d+)-(?P<slug>[\w-]+)\s*$")
FIELD = re.compile(r"^(date|source|supersedes|revisit_when):\s*(.*)$")     # an entry's fields, as the ledger's form gives them


def ledger_entries(plan, text):
    """(number, slug, first paragraph, fields) for each `## decision/<nnnn>-<slug>` entry of the ledger. Each `## `
    heading begins an entry; one in another form, and text before the first, is a change migrate cannot make."""
    entries, current, outside = [], None, []
    for line in text.splitlines():
        if line.startswith("## "):
            m = ENTRY.match(line)
            current = [m.group("number"), m.group("slug"), []] if m else [None, None, []]
            if m:
                entries.append(current)
            else:
                plan.failures.append("could not replace the ledger entry `%s` of %s: its heading is not "
                                     "`## decision/<nnnn>-<slug>`" % (line.strip(), LEDGER))
        elif current is not None:
            current[2].append(line)
        elif line.strip():
            outside.append(line.strip())
    if outside:
        plan.failures.append('could not replace the ledger text "%s" outside its entries in %s' % (" ".join(outside), LEDGER))
    out = []
    for number, slug, lines in entries:
        paragraph, fields, in_head = [], {}, True
        for line in lines:
            m = FIELD.match(line)
            if in_head and line.strip() and not m:
                paragraph.append(line.strip())
                continue
            in_head = False
            if m:
                fields[m.group(1)] = m.group(2).strip()
        out.append((number, slug, " ".join(paragraph), fields))
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


def decision_text(plan, slug, summary, fields):
    return ("---\nid: design-decision/%s/%s\nsummary: %s\ndate: %s\nstatus: accepted\nby: %s\n---\n\n# %s\n\n"
            "## Decision\n%s\n" % (plan.context, slug, quoted(plan, "summary", summary), fields.get("date", ""),
                                  quoted(plan, "by", fields.get("source", "")), slug, summary))


def plan_ledger(plan):
    if LEDGER not in tracked(plan.root):
        return
    for number, slug, summary, fields in ledger_entries(plan, plan.read(LEDGER)):
        path = "spec/decisions/%s-%s.md" % (number, slug)
        plan.created[path] = "the ledger entry `## decision/%s-%s`" % (number, slug)
        plan.texts[path] = decision_text(plan, slug, summary, fields)
        plan.renamed["decision/%s-%s" % (number, slug)] = "design-decision/%s/%s" % (plan.context, slug)
    plan.removes.append(LEDGER)
