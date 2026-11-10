"""`work line --recodify` (CNL 4's I19, call 15): an item switches a codified capability to the new language. The
item's block for the capability is given the line `language: codified-2` (backlog_section), so its lines, and the
capability's own, are read in grammar 4 once the item is laid.

Laid over a spec (`lay`), the capability file's frontmatter says `language: codified-2`; taken out again (`unlay`), it
says `language: codified-1` again, the one marker a capability is switched from."""
import re

import spec_read
from backlog_items import Refused, label
from backlog_section import SECTION, Block, capability_file, read, render, takes

MARKER, OLD = spec_read.MARKER4, spec_read.MARKER


def check(root, item, capability):
    """Refused unless the item takes lines, `capability` is a codified capability still in the old language, and the
    item does not switch it already."""
    takes(item)
    path = capability_file(root, capability)
    if not spec_read.codified(path, (OLD,)):
        raise Refused("work line: %s says `language: %s` already" % (capability, MARKER))
    if any(b.capability == capability and b.language for b in read(item, "the item %s" % item.name)):
        raise Refused("work line: %s recodifies %s already" % (label(item), capability))


def with_language(item, capability):
    """The item's block for `capability` (made when it has none) given the marker; nothing is committed."""
    blocks = read(item, "the item %s" % item.name)
    at = next((k for k, b in enumerate(blocks) if b.capability == capability), None)
    if at is None:
        blocks.append(Block(capability, [], []))
        at = len(blocks) - 1
    blocks[at] = blocks[at]._replace(language=MARKER)
    item.sections[SECTION] = render(blocks)


def _marked(text, old, new):
    """A capability file's text with its frontmatter's `language: <old>` written `language: <new>`."""
    head_end = text.find("\n---", 4)
    found = re.search(r"(?m)^language:[ \t]*%s[ \t]*$" % re.escape(old), text[:head_end])
    return text if found is None else text[:found.start()] + "language: %s" % new + text[found.end():]


def lay(text):
    return _marked(text, OLD, MARKER)


def unlay(text):
    return _marked(text, MARKER, OLD)
