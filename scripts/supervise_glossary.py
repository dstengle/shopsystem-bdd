"""The glossary-proposals of an initiative (spec-integration r55, design decision 0073): a term reaches spec/index.md only
once the person has approved its glossary-proposal, so an apply round's brief withholds the terms of every glossary-proposal
that is not `approved`; and a question under a delegation that names a term of the glossary or a glossary-proposal is
left for the person (supervision r162). Standard library only."""
import re

import workqueue

FIELDS = ("adds", "changes", "removes")


ROUTES = {"drafted": ("gate", "awaiting-answer"), "awaiting-answer": ("apply", "approved")}     # no further round (r167)


def statuses(directory):
    """(name, status) of each glossary-proposal in the initiative's directory, by name."""
    found = []
    for path in sorted(directory.glob("*.md")):
        data, _ = workqueue.frontmatter(path.read_text())
        if data.get("kind") == "glossary-proposal":
            found.append((path.stem, data.get("status")))
    return found


def route(status, questions, answers):
    """(round, status after) of a glossary-proposal at `status`, else None: a drafted one is given to a gate round (r164,
    r169); an awaiting-answer one with a question, every one answered, to an apply round (r165, r166, r172)."""
    if status == "awaiting-answer" and not (questions and answers >= questions):
        return None
    return ROUTES.get(status)


def withheld(directory, applying=None):
    """The terms (`term/<term>` ids, in the order found) of each glossary-proposal in the initiative's directory whose
    status is not `approved`, the one named `applying` left out: its answers are the approval (r165)."""
    terms = []
    for path in sorted(directory.glob("*.md")):
        data, _ = workqueue.frontmatter(path.read_text())
        if data.get("kind") != "glossary-proposal" or data.get("status") == "approved" or path.stem == applying:
            continue
        terms += [i for f in FIELDS for i in data.get(f) or [] if i not in terms]
    return terms


def terms_of(root):
    """The terms of spec/index.md's `## Glossary`: the bold name of each bullet."""
    path = root / "spec" / "index.md"
    if not path.is_file():
        return []
    terms, inside = [], False
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Glossary"
        elif inside and (m := re.match(r"- \*\*(.+?)\*\*", line)):
            terms.append(m.group(1).strip())
    return terms


def proposals_of(root):
    """The file stem and the full id of every glossary-proposal under .shop/work/, of any initiative and status."""
    names = []
    for path in sorted((root / ".shop" / "work").glob("*/*.md")):
        data, _ = workqueue.frontmatter(path.read_text())
        if data.get("kind") == "glossary-proposal":
            names += [path.stem] + ([data["id"]] if data.get("id") else [])
    return names


def names_one(root, question):
    """Whether the question names a term of the glossary or a glossary-proposal (supervision r162): as a whole word or
    phrase, in any case."""
    return any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), question, re.IGNORECASE)
               for n in terms_of(root) + proposals_of(root))


def text(directory, applying=None):
    """The line an apply round's brief gives about them; empty when no term is withheld."""
    terms = withheld(directory, applying)
    if not terms:
        return ""
    return ("The person has not approved these terms of the initiative's glossary-proposals: %s. Apply none of them to "
            "spec/index.md, also where the drafts hold them." % ", ".join(terms))
