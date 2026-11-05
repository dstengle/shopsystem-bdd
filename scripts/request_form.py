"""The form of a comment on a request's issue (capability requests, r32, r33): one fenced block of fields, `~~~shop-request`
to `~~~`, above any free text. Only the block is read; the free text is for the people browsing GitHub.

A field is `<name>: <value>`, a value of more than one line continued on the lines after it, each indented by two
spaces. The single fields are `step` (one of STEPS, the first field), `request` (the poster's request id), `asker`,
`upstream`, `title`, `status`, `turn`, `ask` and `offer`; a numbered field `<name> <n>: <value>` is entry n of a
section of the request (NUMBERED). A body with no block is no form; one with a block that does not parse, with more
than one block, with a field not known or with no known step is unreadable (`Unreadable`), and is shown, never acted
on. Standard library only."""
import re
from dataclasses import dataclass, field

FENCE, END = "~~~shop-request", "~~~"
STEPS = ("ask", "offer", "fits", "turn", "accept", "resolve")
SINGLE = ("step", "request", "asker", "upstream", "title", "status", "turn", "ask", "offer")
# A numbered field's name, and the section of the request file its entries are.
NUMBERED = {"line": "Lines", "answer": "Answers", "question": "Questions", "outcome": "Outcomes", "into": "Into",
            "counter": "Counter-proposals", "reason": "Reasons", "resolution": "Resolution"}
BLOCK = re.compile(r"(?ms)^%s[ \t]*\n(.*?)^%s[ \t]*$" % (re.escape(FENCE), re.escape(END)))
LINE = re.compile(r"^(%s)(?: ([1-9]\d*))?: ?(.*)$" % "|".join(sorted(set(SINGLE) | set(NUMBERED), key=len,
                                                                       reverse=True)))


class Unreadable(Exception):
    """A body whose block of fields does not parse; its message says why."""


@dataclass
class Form:
    fields: dict = field(default_factory=dict)        # {single field: value}
    sections: dict = field(default_factory=dict)      # {section of the request: {number: text}}

    @property
    def step(self):
        return self.fields.get("step")


def _value(text):
    lines = str(text).split("\n")
    return "\n".join([lines[0]] + ["  " + line for line in lines[1:]])


def render(fields, sections=None, text=""):
    """The body of a comment: the block of `fields` (single fields, `step` first) and of `sections` ({section:
    {number: text}}), then the free text `text`."""
    out = [FENCE]
    for name in sorted(fields, key=lambda n: (n != "step", SINGLE.index(n))):
        if fields[name] is not None:
            out.append("%s: %s" % (name, _value(fields[name])))
    names = {section: name for name, section in NUMBERED.items()}
    for section, entries in (sections or {}).items():
        for number in sorted(entries, key=int):
            out.append("%s %s: %s" % (names[section], number, _value(entries[number])))
    out.append(END)
    return "\n".join(out) + "\n" + ("\n" + text.strip() + "\n" if text and text.strip() else "")


def is_form(body):
    """Whether `body` holds a block of fields at all: a request's comment, readable or not."""
    return bool(BLOCK.search((body or "").replace("\r\n", "\n")))


def parse(body):
    """The Form of `body`'s one block; None when it holds no block; Unreadable when the block does not parse."""
    blocks = BLOCK.findall((body or "").replace("\r\n", "\n"))
    if not blocks:
        return None
    if len(blocks) > 1:
        raise Unreadable("it holds %d blocks of fields, not one" % len(blocks))
    form, last = Form(), None
    for number, line in enumerate(blocks[0].split("\n"), 1):
        if line.startswith("  ") and last is not None:
            target, key = last
            target[key] += "\n" + line[2:]
            continue
        if not line.strip():
            continue
        found = LINE.match(line)
        if not found:
            raise Unreadable("line %d of its block is no field: %s" % (number, line))
        name, n, value = found.groups()
        if (name in NUMBERED) != (n is not None):
            raise Unreadable("line %d of its block: %s %s" % (number, name, "takes no number" if n else "needs a number"))
        if n is None:
            if name in form.fields:
                raise Unreadable("its block gives %s twice" % name)
            form.fields[name], last = value, (form.fields, name)
        else:
            entries = form.sections.setdefault(NUMBERED[name], {})
            entries[n], last = value, (entries, n)
    if form.step not in STEPS:
        raise Unreadable("its block names no step of %s" % ", ".join(STEPS))
    return form
