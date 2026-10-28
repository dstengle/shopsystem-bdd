"""The glossary-proposals of an initiative (spec-integration r55, design decision 0073): a term reaches spec/index.md only
once the person has approved its glossary-proposal, so an apply round's brief withholds the terms of every glossary-proposal
that is not `approved`; and a question under a delegation that names a term of the glossary or a glossary-proposal is
left for the person (supervision r162). Standard library only."""
import re

import workqueue
from supervise_worker import GitFailed, git

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


def approval_question(path):
    """The question a gate round that gave none writes for the glossary-proposal at `path` (r173), else None: it asks the
    person to approve the terms the proposal adds, changes and removes, each by its bare name."""
    data, _ = workqueue.frontmatter(path.read_text())
    if data.get("kind") != "glossary-proposal":
        return None
    named = ["%s \"%s\"" % (verb, i[len("term/"):]) for verb, f in (("adds", "adds"), ("changes", "changes"),
                                                                    ("removes", "removes"))
             for i in data.get(f) or []]
    return "Are the terms of %s approved as drafted? It %s." % (path.stem, ", ".join(named))


def terms_of(root):
    """The terms of spec/index.md's `## Glossary`: the bold name of each bullet."""
    path = root / "spec" / "index.md"
    return terms_in(path.read_text()) if path.is_file() else []


def terms_in(text):
    terms, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Glossary"
        elif inside and (m := re.match(r"- \*\*(.+?)\*\*", line)):
            terms.append(m.group(1).strip())
    return terms


def glossary_only_done(root, directory):
    """Whether the initiative changes only the glossary and is delivered (r161): it has glossary-proposals, no other
    proposal and no work-item, every glossary-proposal is approved, and spec/index.md as committed at HEAD holds each term
    they add or change and none they remove, with no uncommitted change."""
    kinds = [workqueue.frontmatter(p.read_text())[0] for p in sorted(directory.glob("*.md"))
             if p.name not in ("initiative.md", "ledger.md")]
    if not kinds or any(d.get("kind") != "glossary-proposal" or d.get("status") != "approved" for d in kinds):
        return False
    try:
        held = terms_in(git(root, "show", "HEAD:spec/index.md").stdout)
        if git(root, "status", "--porcelain", "--", "spec/index.md").stdout.strip():
            return False
    except GitFailed:
        return False
    return (all(i[len("term/"):] in held for d in kinds for f in ("adds", "changes") for i in d.get(f) or [])
            and not any(i[len("term/"):] in held for d in kinds for i in d.get("removes") or []))


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
