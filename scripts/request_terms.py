"""Term proposals (context-requests r57-r60, b42): the asker of a request proposes terms for the upstream to take
into its own vocabulary in its own words, as a line of the request. A term proposal is one vocabulary entry or more
in the vocabulary-entry form, `- **<word>** (<part of speech>) → <model element>. <definition>`, kept as one line
under the request's `## Lines` (its entries side by side), which a line that is a requirement never opens with.

`work suggest <request> --term-proposal <entries>` (`suggest`): the proposal checked against the form, then the
request in the asker's turn, appended to `## Lines` numbered on and posted on its issue as the step `suggest`, the
asker's part, which the upstream's `work sync` takes in as it takes the asker's lines. The upstream settles it with
`work outcome` as any line (an accepted one is checked against the form, not parsed: `check`), and `work accept`
writes each term an accepted proposal concerns into the item (`into_item`): into the model block of the area of the
capability its outcome named in a context with a domain model, else as a term bullet of that capability's block, in
the capability term form `- **<word>** (<part of speech>): <definition>` (`term_entry`)."""
import re
from pathlib import Path

from backlog_items import one_line
from shop_files import Refused

FORM = "`- **<word>** (<part of speech>) → <model element>. <definition>`"
START = "- **"


def is_proposal(line):
    """Whether a request's line is a term proposal."""
    return line.lstrip().startswith(START)


def entries(proposal):
    """The vocabulary entries of a term proposal, one a bullet, given on lines of their own or side by side."""
    text = " ".join(part.strip() for part in proposal.replace("\r\n", "\n").split("\n") if part.strip())
    return [e.strip() for e in re.split(r"\s+(?=- \*\*)", text) if e.strip()]


def check(proposal, command="work suggest"):
    """The term proposal's entries, refused naming it unless each is in the vocabulary-entry form."""
    import spec_vocabulary
    found = entries(proposal)
    for entry in found:
        match = spec_vocabulary.ENTRY.match(entry)
        if not match or not match.group("arrow") or not spec_vocabulary.REF.match(match.group("text")):
            break
    else:
        if found:
            return found
    raise Refused("%s: the term proposal %s is not in the vocabulary-entry form: give each term as %s"
                  % (command, proposal.strip(), FORM))


def suggest(root, ident, proposal):
    """`work suggest` (r57, r59, r60): the term proposal appended to the request's `## Lines` in the asker's turn,
    committed and posted on its issue as the step `suggest`."""
    import request_post
    import request_steps
    from request_text import entries as held_entries
    from request_text import with_entries
    check(proposal)
    one = one_line(" ".join(entries(proposal)), "term proposal")
    said = {}

    def edit(text):
        request_steps.refuse_asker_part(root, text, ident, "its term proposals")
        request_steps.in_turn(text, ident, "asker", ("awaiting-asker",), "work suggest")
        held = held_entries(text, "Lines")
        at = max([int(e.split(".", 1)[0]) for e in held if e.split(".", 1)[0].isdigit()], default=0) + 1
        said["number"] = str(at)
        return with_entries(text, "Lines", held + ["%d. %s" % (at, one)])
    request_steps.change(root, ident, "suggest", edit, lambda after: request_post.posting(
        after, "suggest", {"Lines": {said["number"]: one}}, "work suggest"))


def into_item(root, item, capability, proposal):
    """Each entry of an accepted term proposal written into the item (nothing committed): into its model block of
    the capability's area where the context has a domain model (`spec/model/`), else a term bullet of the
    capability's block."""
    import backlog_lines
    import backlog_model
    from backlog_section import SECTION, read, render
    bullets = check(proposal, "work accept")
    blocks = read(item, "the item %s" % item.name)
    if (Path(root) / "spec" / "model").is_dir():
        area = backlog_model.area_of(root, capability, blocks)
        at = backlog_model.block_of(blocks, area)
        blocks.models[at] = blocks.models[at]._replace(terms=blocks.models[at].terms + tuple(
            b for b in bullets if b not in blocks.models[at].terms))
    else:
        block = backlog_lines.block_of(blocks, capability)
        terms = [term_entry(b, capability, proposal) for b in bullets]
        block.terms.extend(t for t in terms if t not in block.terms)
    item.sections[SECTION] = render(blocks)


def term_entry(entry, capability, proposal):
    """A vocabulary entry written in the capability term form, `- **<word>** (<part of speech>): <definition>`, which
    spec_lexicon reads; refused naming the proposal when it does not read so (f1)."""
    import spec_lexicon
    import spec_vocabulary
    match = spec_vocabulary.ENTRY.match(entry)
    ref = spec_vocabulary.REF.match(match.group("text"))
    term = "- **%s** (%s): %s" % (match.group("term").strip(), match.group("label").strip(),
                                  (ref.group("rest") or "").strip())
    if spec_lexicon.entry(term, capability) is None:
        raise Refused("work accept: the term proposal %s gives no term entry `- **<term>** (<part of speech>): "
                      "<text>` of %s" % (proposal.strip(), capability))
    return term
