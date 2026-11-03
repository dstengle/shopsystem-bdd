"""The 0.29 reading of scripts/model, for a capability file without `language: codified-1` and an index whose glossary
is not typed (the GF conversion's design §13.4): Behaviour bullets and tables read as requirements, their EARS shape
by pattern, and `- **<term>**: <definition>. Not: <word>.` glossary bullets. The release (plan P14) deletes it.
Standard library only."""

import re

from model_parse import RID, bullets, glossary_entry, section

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


class LegacyReading:
    """The part of Model (model_facts) that reads 0.29 files."""

    def read_glossary_legacy(self, body):
        for n, bullet in enumerate(bullets(section(body, "Glossary")), 1):
            entry = glossary_entry(bullet)
            if entry is None:
                self.problems.append(f"spec/index.md: glossary bullet {n} is not "
                                     "'- **<term>**: <definition>. Not: <word>, <word>.' (Not: optional)")
                continue
            word, avoided = entry
            self.term(word, n, avoided)

    def read_legacy_behaviour(self, cap, entry, body):
        """Each bullet or table row of the Behaviour section a requirement, `[r<n>]` its id, its EARS shape judged."""
        for i, (text, lead) in enumerate(behaviour_items(section(body, "Behaviour")), 1):
            m = RID.match(text)
            if m:
                n = int(m.group(1))
                q = f"{cap}#r{n}"
                if n in entry["reqs"]:
                    q = f"{cap}#r{n}~{i}"   # a second bullet with the same id: its own node, so v15b sees both
                self.fact("req_id", q, cap, n)
                entry["reqs"].setdefault(n, q)
                self.req_text[q] = text[m.end():]
            else:
                q = f"{cap}#line{i}"
                self.req_text[q] = text
            self.node(q, "requirement")
            self.fact("has_req", cap, q)
            shaped, single = ears(lead if lead is not None else text)
            if not shaped:
                self.fact("ears_other", q)
            if not single:
                self.fact("ears_many", q)

    def legacy_scenario(self, cap, key, title, tags, s):
        """has_sc(Q, S) for each @r<n> tag naming a requirement of the capability."""
        for tag in tags:
            m = re.fullmatch(r"@r(\d+)", tag)
            if not m or cap is None:
                continue
            q = f"{cap}#r{m.group(1)}"
            if q in self.nodes:
                self.fact("has_sc", q, s)
            else:
                self.dangling.append(f"{key}: scenario {title!r} names {q}, which {cap} does not have")
