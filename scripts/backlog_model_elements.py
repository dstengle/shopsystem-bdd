"""A model line that restates an element (b598, batches r116): an item's object, under the name of an object the area
declares, that repeats a member line the object holds already (a line that only added members would declare that one
twice, v_m8) is the object as it is to be: laid in place of the declared object, its members the line's alone, and its
header the line's when it names a kind, else the declared one (`restates`, `restate`)."""


def restates(header, members, body, at, end):
    """Whether the object chunk `header` with `members` restates the element at `at` of `body` (its members ending at
    `end`): an object that repeats one of the element's member lines."""
    return header.startswith("object ") and bool(set(members) & set(body[at + 1:end]))


def restate(body, at, end, header, members):
    """The element at `at` of `body` replaced by `header` (the declared one kept unless `header` names a kind) and
    `members`."""
    body[at:end] = [header if " kind of " in header else body[at]] + list(members)


def lone(line):
    """Whether a model line declares an event or an actor, an element of one line and no members (b647)."""
    return line.startswith(("event ", "actor "))


def key(line):
    """What names an event's or an actor's line: its kind and phrase (the text before the last `:` and any
    property after `;`) or its name (the text before ` kind of `)."""
    word, _, rest = line.partition(" ")
    if word == "event":
        return word, rest.partition(";")[0].rpartition(":")[0].strip()
    return word, rest.partition(" kind of ")[0].strip()


def lone_at(body, header):
    """The index of the event or the actor of `header`'s phrase or name in `body`, or None (batches r120, r121)."""
    return next((n for n, line in enumerate(body) if lone(line) and key(line) == key(header)), None)


def left_out(body, chunks):
    """The member lines of each element of `body` (model lines) that one of `chunks` ([(header, members)]) restates
    and does not hold, stripped, in the element's order (drafting r70, b647): the lay would cut them."""
    from backlog_model import _at, _end
    out = []
    for header, members in chunks:
        at = _at(body, header)
        if at is not None and restates(header, members, body, at, _end(body, at)):
            out += [line.strip() for line in body[at + 1:_end(body, at)] if line not in members and line.strip()]
    return out
