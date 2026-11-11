"""The docs' requirement lines and Gherkin (b263), beside test_docs.py: every requirement line of any code block of
README.md, CHANGELOG.md and the docs pages (docs_lines) parses to one meaning in its block's context, or is refused
there when the page shows it refused; every Gherkin block (docs_gherkin) is valid Gherkin, its steps read in the step
grammar 4 of its context, each instance a Given or a When names brought in by a Given, every value in the full form,
and a scenario a feature file of its context has quoted as the file has it. Each check is shown to catch a broken
copy of a page."""
import pathlib
import sys

import pytest
import spec_grammar4
import spec_lf_read

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import docs_gherkin
import docs_lines
import toolchain
from docs_testing import DOCS, EXAMPLE, REPO, pages

FIXTURES = REPO / "tests" / "scripts" / "fixtures"
_vocabs = {}


def all_pages():
    """pages(), with the whole of CHANGELOG.md in place of its newest section."""
    out = pages()
    out["CHANGELOG.md"] = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    return out


def refusal(root, line):
    """The refusal of a line in a context's grammar 4, or None when it parses to one meaning no reading rule
    refuses."""
    if root not in _vocabs:
        _vocabs[root] = spec_grammar4.load(root)[0]
    p = spec_grammar4.parse(root, line)
    if not p.tree:
        return p.refusal or "refused"
    return spec_lf_read.refusal(_vocabs[root], p.tree)


def line_problems(page, text):
    out = []
    for where, line, refused, root in docs_lines.lines(page, text):
        why = refusal(root, line)
        if refused and not why:
            out.append("%s: shown refused, but parses in %s: %s" % (where, docs_lines.context(root), line))
        elif why and not refused:
            out.append("%s: refused in %s: %s\n  %s" % (where, docs_lines.context(root), line, why))
    return out


def gherkin_problems(page, text):
    return ["%s:%d: %s" % (page, n, why) for lang, body, n, mark in docs_lines.blocks(text) if lang == "gherkin"
            for why in docs_gherkin.problems(mark or docs_lines.page_root(page), body)]


@pytest.fixture(scope="module")
def tools():
    toolchain.require()


def test_every_requirement_line_of_the_docs_reads_as_the_page_shows_it(tools):
    found = [p for page, text in all_pages().items() for p in line_problems(page, text)]
    assert found == [], "\n".join(found)


def test_every_gherkin_block_of_the_docs_is_valid_and_its_steps_read(tools):
    found = [p for page, text in all_pages().items() for p in gherkin_problems(page, text)]
    assert found == [], "\n".join(found)


def test_the_lines_are_found_in_every_kind_of_block_and_in_their_context():
    text = (DOCS / "upgrading.md").read_text(encoding="utf-8")
    shop = [(line, refused) for _, line, refused, root in docs_lines.lines("docs/upgrading.md", text)
            if root == FIXTURES / "docs-shop"]
    assert ("While a shopper does not own a cart, when the shopper picks a cart, the shopper shall watch a till.",
            True) in shop
    assert len(shop) == 4
    notes = docs_lines.lines("docs/examples/notes-cli/README.md",
                             (EXAMPLE / "README.md").read_text(encoding="utf-8"))
    assert {root for *_, root in notes} == {EXAMPLE}
    assert any("\\`" not in line and "`notes add`" in line for _, line, _, _ in notes)


def broken(page, old, new):
    text = (REPO / page).read_text(encoding="utf-8")
    assert old in text, "%s no longer holds %r: pick another line to break" % (page, old)
    return text.replace(old, new, 1)


def test_a_line_that_does_not_parse_is_caught(tools):
    text = broken("docs/how-it-works.md", "shall not print the title of the item.",
                  "shall not print the title of the thing it shows.")
    assert any("refused in this repository" in p for p in line_problems("docs/how-it-works.md", text))


def test_a_line_shown_refused_that_parses_is_caught(tools):
    text = broken("docs/upgrading.md", "While a shopper does not own a cart",
                  "While a shopper owns no cart")
    assert any("shown refused, but parses in tests/scripts/fixtures/docs-shop" in p
               for p in line_problems("docs/upgrading.md", text))


def test_a_sketch_line_read_in_this_repository_is_caught(tools):
    text = broken("docs/recipes.md", "<!-- docs: context tests/scripts/fixtures/docs-labels -->\n```text", "```text")
    assert any("`work label`" in p for p in line_problems("docs/recipes.md", text))


def test_a_scenario_that_is_not_gherkin_is_caught(tools):
    text = broken("docs/index.md", "Scenario: `work shape` shapes an idea", "Scenari `work shape` shapes an idea")
    assert any("not valid Gherkin" in p for p in gherkin_problems("docs/index.md", text))


def test_a_scenario_missing_a_given_is_caught(tools):
    text = broken("docs/tour.md", "    Given an item i1\n    When the person runs `work show`",
                  "    When the person runs `work show`")
    assert any("names i1, which no Given brought in" in p for p in gherkin_problems("docs/tour.md", text))


def test_a_step_that_does_not_read_is_caught(tools):
    text = broken("docs/index.md", "Then `work` sets the status of the item i1 to `shaped`",
                  "Then `work` shapes the item i1")
    assert any("does not" in p and "shapes the item i1" in p for p in gherkin_problems("docs/index.md", text))


def test_a_value_in_the_short_form_is_caught(tools):
    text = broken("docs/index.md", "And the status of the item i1 is `idea`", "And the item i1 is `idea`")
    assert any("short form" in p for p in gherkin_problems("docs/index.md", text))


def test_a_quote_that_differs_from_its_feature_file_is_caught(tools):
    page = "docs/getting-started.md"
    text = broken(page, "    Then `notes` deletes the note n1\n```", "    Then `notes` deletes the note n1\n"
                  "    And `notes` exits successfully\n```")
    assert any("is not as notes.feature has it" in p for p in gherkin_problems(page, text))
    text = broken(page, "Feature: Notes\n  Narrator: the person\n\n  @g1", "Feature: Notes\n  Narrator: a person\n\n  @g1")
    assert any("'Narrator: a person' is not notes.feature's" in p for p in gherkin_problems(page, text))


@pytest.mark.parametrize("fixture", ["docs-shop", "docs-labels"])
def test_a_sketch_context_s_features_are_current(tools, fixture):
    """A page's sketch context's feature files are what `features generate` writes of its spec, so a quote of them
    is a quote of the generator."""
    import subprocess
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "features"), "generate", "--check", "--root", "."],
                          cwd=FIXTURES / fixture, capture_output=True, text=True, timeout=900)
    assert done.returncode == 0, done.stdout + done.stderr
