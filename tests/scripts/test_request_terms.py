"""Term proposals (b42, context-requests r57-r60): the vocabulary-entry form checked, an accepted proposal settled by
`work outcome` against its form, not the grammar, and its entries written into the item by `work accept`: a term
bullet of the capability's block, or, in a context with a domain model, an entry of the area's model block."""
import shutil
from pathlib import Path

import backlog_items
import backlog_section
import pytest
import request_lines
import request_terms
import spec_lexicon
from plumbing.shop_files import Refused

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "domain-model"
SHELF = "- **shelf** (noun) → object shelf. A place the person keeps books on."
BOOK = "- **book** (noun) → object book. What the person keeps."


def test_entries_are_read_side_by_side_or_on_lines_of_their_own():
    assert request_terms.entries("%s %s" % (SHELF, BOOK)) == [SHELF, BOOK]
    assert request_terms.entries("%s\n%s\n" % (SHELF, BOOK)) == [SHELF, BOOK]
    assert request_terms.is_proposal(SHELF) and not request_terms.is_proposal("When the person adds a note, ...")


@pytest.mark.parametrize("proposal", ["shelf: a place for books", "- **shelf** (noun): a place for books.", ""])
def test_a_proposal_out_of_the_form_is_refused_naming_it(proposal):
    with pytest.raises(Refused) as refused:
        request_terms.check(proposal)
    assert "the term proposal %s is not in the vocabulary-entry form" % proposal.strip() in str(refused.value)


def test_an_accepted_proposal_is_checked_against_its_form_not_parsed(tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    assert request_lines.check(tmp_path, [SHELF]) is None
    with pytest.raises(Refused, match="vocabulary-entry form"):
        request_lines.check(tmp_path, ["- **shelf** a place"])


def item(name="b1"):
    return backlog_items.Item(name=name, ident="item/ex.com/prod/ctx/%s" % name, title="Shelves", status="shaped",
                              provenance="peer", sections={})


def test_into_the_model_block_of_the_capability_s_area(tmp_path):
    shutil.copytree(FIXTURE / "spec", tmp_path / "spec")
    found = item()
    request_terms.into_item(tmp_path, found, "notebook", "%s %s" % (SHELF, BOOK))
    request_terms.into_item(tmp_path, found, "notebook", SHELF)        # a term held once
    blocks = backlog_section.read(found, "b1")
    assert [(m.area, m.terms) for m in blocks.models] == [("notes", (SHELF, BOOK))]


def test_into_a_term_bullet_of_the_capability_without_a_domain_model(tmp_path):
    (tmp_path / "spec").mkdir()
    found = item()
    request_terms.into_item(tmp_path, found, "work-queue", SHELF)
    blocks = backlog_section.read(found, "b1")
    assert [(b.capability, b.terms) for b in blocks] == [
        ("work-queue", ["- **shelf** (noun): A place the person keeps books on."])]
    read = spec_lexicon.entry(blocks[0].terms[0], "work-queue")
    assert (read.term, read.category) == ("shelf", "kind")
