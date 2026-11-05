"""The text of a request file `.shop/work/requests/q<n>.md` (capability requests; workflow simplification plan 4,
D24, D25): its numbered sections read and written, its frontmatter fields, and the turn rule (`turned`), written once
for `work turn` and for `work outcome`'s counter-proposal.

A section holds one entry a line, `<n>. <text>`. `## Counter-proposals` holds `<n>. <m>` for each line n that
`work outcome ... rewritten --line` rewrote as its counter-proposal, line m: line n is no longer proposed, line m is
(requests r20-r22 read the lines proposed in the request). A request without the section reads as before."""
import re

SETTLED = ("accepted", "refused", "withdrawn")
COUNTERS = "Counter-proposals"


def entries(text, name):
    found = re.search(r"(?ms)^## %s\n(.*?)(?=^## |\Z)" % name, text)
    return [line for line in found.group(1).splitlines() if line.strip()] if found else []


def with_entries(text, name, given):
    body = "## %s\n%s\n" % (name, "".join(entry + "\n" for entry in given))
    if re.search(r"(?m)^## %s\n" % name, text):
        return re.sub(r"(?ms)^## %s\n.*?(?=^## |\Z)" % name, lambda _: body, text, count=1)
    return text.rstrip("\n") + "\n\n" + body


def with_field(text, name, value):
    end = text.find("\n---", 4)
    return re.sub(r"(?m)^%s:.*$" % name, lambda _: "%s: %s" % (name, value), text[:end], count=1) + text[end:]


def field(text, name):
    found = re.search(r"(?m)^%s: *(.*)$" % name, text[:text.find("\n---", 4)])
    return found.group(1).strip() if found else None


def numbered(given, number, text):
    kept = [e for e in given if not e.startswith("%d. " % number)] + ["%d. %s" % (number, text)]
    return sorted(kept, key=lambda e: int(e.split(".", 1)[0]))


def countered(text):
    """The numbers n of `## Counter-proposals`' `<n>. <m>` entries: the lines a counter-proposal took the place of."""
    return {e.split(". ", 1)[0] for e in entries(text, COUNTERS) if ". " in e}


def turned(text):
    """The request's text with its turn passed to the other side (requests r7): to the upstream it is
    `awaiting-upstream` (r18). To the asker, the upstream ending its turn with every line proposed settled sets the
    status (r8, r9) and, on `accepted`, keeps the turn (r23); else it is `awaiting-asker` (r17). A line a
    counter-proposal took the place of is not proposed, and neither counted nor read (D24)."""
    if field(text, "turn") == "asker":
        return with_field(with_field(text, "status", "awaiting-upstream"), "turn", "upstream")
    gone = countered(text)
    lines = [e for e in entries(text, "Lines") if e.split(".", 1)[0] not in gone]
    words = [e.split(". ", 1)[1] for e in entries(text, "Outcomes") if ". " in e and e.split(". ", 1)[0] not in gone]
    if len(words) == len(lines) and all(w in SETTLED for w in words):
        if field(text, "status") != "delivered":
            text = with_field(text, "status", "accepted" if "accepted" in words else "refused")
            if "accepted" in words:
                return text  # r23: the upstream's end that sets accepted keeps the turn
    else:
        text = with_field(text, "status", "awaiting-asker")
    return with_field(text, "turn", "asker")
