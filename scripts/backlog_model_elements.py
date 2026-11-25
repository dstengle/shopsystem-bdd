"""A model line that restates an element (b598, batches r116): an item's object, under the name of an object the area
declares, that repeats a member line the object holds already (a line that only added members would declare that one
twice, v_m8) is the object as it is to be: laid in place of the declared object, its members the line's alone, and its
header the line's when it names a kind, else the declared one (`restates`, `restate`). On the unlay the object is put
back as the model file held it before the lay (`unrestate`, over backlog_model_ops' `at_base` or `held`), or left to
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
    """Whether `body` (model lines) declares the element `header` with exactly `members`."""
    from backlog_model import _at, _end
    at = _at(body, header)
    return at is not None and body[at + 1:_end(body, at)] == list(members)


def unrestate(body, at, header, members, held):
    """The element at `at` of `body`, holding exactly `members`, put back as `held(header, None, members)` (the model
    lines before the lay) declares it; False, `body` left alone, when it does not hold the element so or no version
    declares the element."""
    from backlog_model import _at, _end
    end = _end(body, at)
    if not header.startswith("object ") or held is None or body[at + 1:end] != list(members):
        return False
    before = held(header, None, members)
    old = _at(before, header) if before is not None else None
    if old is None:
        return False
    body[at:end] = before[old:_end(before, old)]
    return True
