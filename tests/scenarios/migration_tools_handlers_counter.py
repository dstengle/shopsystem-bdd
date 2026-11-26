"""migration-tools' counter-examples (b273): the Givens that bring into the repository `migrate` runs in the thing a
negated Then says it leaves alone, beside the given block's files, and what those Thens read of it. A file that
mentions no old-layout directory, a work-item file that mentions no requirement and a feature that holds no
deprecated scenario are written as tracked files (`FILES`) and kept by name, for "`migrate` does not rewrite" to find
byte for byte; a term that violates no rule is a glossary entry added to the given block's `spec/index.md` (`TERMS`),
for "`migrate` does not print the term t3" to find no report line of; the release of an upgrade step is kept, for
"`migrate` does not print the upgrade step u3" to look for that release's steps' titles."""
import re
import sys

from scenarios import migration_tools_handlers as M

local = M.local
ID = "example.org/acme/shop"
FILES = {   # (the Given's subject kind, its verb): (where it is written, its text)
    ("file", "mention"): ("notes/%s.md", "A note that names no directory of the old layout: see spec/index.md.\n"),
    ("work-item file", "mention"): (".shop/work/i1/%s.md",
                                    "---\nid: work-item/" + ID + "/%s\nkind: work-item\naccepts: []\n---\n# %s\n"),
    ("feature", "holds"): ("features/%s.feature", "Feature: %s\n  Scenario: a code is kept\n    Given a cart\n"),
}
TERMS = {"v_t11": "- **pay** (event): a shopper pays for a cart. Forms: pays, paid. Frame: shopper pays for cart.\n",
         "w_value_kind": "- **colour** (attribute of cart): Values (adjective): `red`, `blue`.\n"}


def counter(step):
    return step.context.setdefault("counter", {})


def subject_kind(step):
    return re.sub(r"^the ", "", step.subject).rsplit(" ", 1)[0]


@local("GivenDoesNot")
def given_not(step):
    """A file, a work-item file or a feature of the counter-example, written; a term that violates no rule, added."""
    if not M.migration(step):
        return False
    name, key = step.names[0] if step.names else None, (subject_kind(step), step.term)
    if key in FILES:
        rel, text = FILES[key]
        M.held(step)[rel % name] = text.replace("%s", name)
        counter(step)[name] = rel % name
    elif step.term == "violate" and subject_kind(step) == "term":
        code = re.search(r"`([^`]+)`", step.text).group(1)
        M.held(step)["spec/index.md"] += TERMS[code]
        counter(step)[name] = (code, re.match(r"- \*\*(\w+)\*\*", TERMS[code]).group(1))
    return False     # recorded too


@local("GivenK_A")
def given_release(step):
    """The release of an upgrade step, kept for the Then that it is not printed."""
    if M.migration(step) and step.text.startswith("the release of the upgrade step "):
        step.context.setdefault("releases", {})[step.names[0]] = M.bare(step.values[0])
    return False


def unchanged(step, name):
    """`migrate` does not rewrite the counter-example's file: it is there, byte for byte as the Given wrote it."""
    rel = counter(step).get(name)
    assert rel, "no counter-example %s in the repository: %s" % (name, sorted(M.held(step)))
    assert (step.repo / rel).is_file(), "%s gone" % rel
    assert M.read(step, rel) == M.held(step)[rel], (rel, M.read(step, rel))


def step_not_printed(step, name):
    """The titles of the plugin's upgrade steps of the release the Given gave the step: none printed."""
    sys.path.insert(0, str(M.ours(step)[0] / "scripts"))
    from upgrades import migrate_upgrade
    release = step.context.get("releases", {}).get(name)
    titles = [title for r, title, *_ in migrate_upgrade.STEPS if r == release]
    assert titles, "no upgrade step of release %s" % release
    out = step.context["done"].stdout
    assert not [t for t in titles if t in out], (titles, out)


def term_not_printed(step, name):
    """The term the Given added, in the rewritten index (or, past 0.38.0's step, which moves the glossary, in the
    vocabulary), on no report line of its rule."""
    code, word = counter(step)[name]
    kept = M.read(step, "spec/index.md") + "".join(
        p.read_text() for p in sorted((step.repo / "spec" / "vocabulary").glob("*.md")))
    assert re.search(r"\*\*%s\*\*" % word, kept), kept
    out = step.context["done"].stdout
    assert not re.search(r"\b%s %s\b" % (code, word), out), (code, word, out)
