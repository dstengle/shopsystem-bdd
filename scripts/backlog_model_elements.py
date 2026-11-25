"""A model line that restates an element (b598, batches r116): an item's object, under the name of an object the area
declares, that repeats a member line the object holds already (a line that only added members would declare that one
twice, v_m8) is the object as it is to be: laid in place of the declared object, its members the line's alone, and its
header the line's when it names a kind, else the declared one (`restates`, `restate`). On the unlay the object is put
back as the model file held it before the lay, a member line another item added to it since kept (`unrestate`, over
backlog_model_ops' `at_base` or `held`), or left to
backlog_model's unmerged, which takes the members out, when no version held it."""


def restates(header, members, body, at, end):
    """Whether the object chunk `header` with `members` restates the element at `at` of `body` (its members ending at
    `end`): an object that repeats one of the element's member lines."""
    return header.startswith("object ") and bool(set(members) & set(body[at + 1:end]))


def restate(body, at, end, header, members):
    """The element at `at` of `body` replaced by `header` (the declared one kept unless `header` names a kind) and
    `members`."""
    body[at:end] = [header if " kind of " in header else body[at]] + list(members)


def same(body, header, members):
    """Whether `body` (model lines) declares the element `header` with exactly `members` (an event or an actor: as
    its line `header`)."""
    from backlog_model import _at, _end
    at = _at(body, header)
    if at is not None and lone(header):
        return body[at] == header
    return at is not None and holding(body[at + 1:_end(body, at)], members)


def holding(lines, members):
    """Whether an element's member lines `lines` hold each of `members`: as the restatement laid them, with any
    another item added after (batches r119, b647)."""
    return all(line in lines for line in members)


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


def unrestate_lone(body, at, header, held):
    """The event's or the actor's line at `at` of `body`, laid as `header`, put back as `held(header, None, [])`
    (the model lines before the lay) declares it, or taken out with the blank line before it when no version
    declares it; False, `body` left alone, when `header` is no event or actor line or `body` does not hold it so."""
    if not lone(header) or body[at] != header:
        return False
    before = held(header, None, []) if held else None
    old = lone_at(before, header) if before is not None else None
    if old is not None:
        body[at] = before[old]
        return True
    del body[at]
    if at > 0 and not body[at - 1].strip() and (at == len(body) or not body[at].strip()):
        del body[at - 1]
    return True


def unrestate(body, at, header, members, held):
    """The element at `at` of `body`, holding `members`, put back as `held(header, None, members)` (the model lines
    before the lay) declares it, each member line another item added to it since kept at its end (batches r119,
    b647); False, `body` left alone, when it does not hold the element so, no version declares the element or the
    chunk repeats none of the member lines it declared then (a chunk that added members)."""
    from backlog_model import _at, _end
    end = _end(body, at)
    if not header.startswith("object ") or held is None or not holding(body[at + 1:end], members):
        return False
    before = held(header, None, members)
    old = _at(before, header) if before is not None else None
    if old is None or not restates(header, members, before, old, _end(before, old)):
        return False      # no version declares it, or the chunk only added members to it: backlog_model's to take off
    put = before[old:_end(before, old)]
    body[at:end] = put + [line for line in body[at + 1:end] if line not in members and line not in put]
    return True


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
