"""The glossary-proposals of an initiative (spec-integration r55, design decision 0073): a term reaches spec/index.md only
once the person has approved its glossary-proposal, so an apply round's brief withholds the terms of every glossary-proposal
that is not `approved`. Standard library only."""
import workqueue

FIELDS = ("adds", "changes", "removes")


def withheld(directory):
    """The terms (`term/<term>` ids, in the order found) of each glossary-proposal in the initiative's directory whose
    status is not `approved`."""
    terms = []
    for path in sorted(directory.glob("*.md")):
        data, _ = workqueue.frontmatter(path.read_text())
        if data.get("kind") != "glossary-proposal" or data.get("status") == "approved":
            continue
        terms += [i for f in FIELDS for i in data.get(f) or [] if i not in terms]
    return terms


def text(directory):
    """The line an apply round's brief gives about them; empty when no term is withheld."""
    terms = withheld(directory)
    if not terms:
        return ""
    return ("The person has not approved these terms of the initiative's glossary-proposals: %s. Apply none of them to "
            "spec/index.md, also where the drafts hold them." % ", ".join(terms))
