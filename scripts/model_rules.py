"""`model rules --write` and `--check` (design-model-check r73, r72): the rule catalogue `grammar/rules.md`, one entry
a rule, so that a requirement line names a rule by its code. Each entry gives the code, its label, its severity,
where it is implemented, the lines citing it and a failing and a passing example. It is generated, never edited:
model.lp's rules with the examples written below each label, then the rules of `model lexicon --check` that model.lp
does not hold (LEXICON). Each example is run before the file is written, so the catalogue never says what the code
does not do."""
import re
import sys
import tempfile
from pathlib import Path

from model_check import LP, solve

PLUGIN = Path(__file__).resolve().parents[1]
CATALOGUE = "grammar/rules.md"
LABEL = re.compile(r'^label\("([^"]+)",\s*"((?:[^"\\]|\\.)+)"\)\.', re.MULTILINE)
EXAMPLE = re.compile(r"^% (fail|pass) (\S+): (.+)$", re.MULTILINE)
INDEX = "---\nid: bounded-context/ex/ctx\nlanguage: codified-1\n---\n# ctx\n\n"
FOUR = {"v_t20"}        # the rules of a codified-2 context's lexicon only: their examples' index says codified-2
# The rules of `model lexicon --check` that model.lp holds no rule of: (label, failing spec/index.md, passing one).
LEXICON = {
    "v_t7": ("a term's gloss is more than one sentence",
             "## Glossary\n\n- **thing** (noun): One thing. Another thing.\n",
             "## Glossary\n\n- **thing** (noun): One thing.\n"),
    "v_t8": ("a relation is written as an entry, not as a row of `## Relations`",
             "## Glossary\n\n- **thing** (noun): A thing.\n- **holds** (relation thing → thing): A thing holds one.\n",
             ("## Glossary\n\n- **thing** (noun): A thing.\n\n## Relations\n\n| from | word | to | how many |\n"
              "|---|---|---|---|\n| thing | holds | thing | many |\n")),
    "v_t9": ("a term's meaning is given as a `Means:` field rather than a sentence",
             "## Glossary\n\n- **thing** (noun): A thing.\n- **ready** (adjective of thing): Means: done.\n",
             "## Glossary\n\n- **thing** (noun): A thing.\n- **ready** (adjective of thing): A thing that is done.\n"),
    "v_t10": ("two relation rows give one (from, word, to)",
              ("## Glossary\n\n- **thing** (noun): A thing.\n\n## Relations\n\n| from | word | to | how many |\n"
               "|---|---|---|---|\n| thing | holds | thing | many |\n| thing | holds | thing | one |\n"),
              ("## Glossary\n\n- **thing** (noun): A thing.\n\n## Relations\n\n| from | word | to | how many |\n"
               "|---|---|---|---|\n| thing | holds | thing | many |\n")),
    "v_t20": ("a relation row's word is neither a preposition of the fixed set nor a role noun (codified-2)",
              ("## Glossary\n\n- **thing** (noun): A thing.\n\n## Relations\n\n| from | word | to | how many |\n"
               "|---|---|---|---|\n| thing | holds | thing |  |\n"),
              ("## Glossary\n\n- **thing** (noun): A thing.\n\n## Relations\n\n| from | word | to | how many |\n"
               "|---|---|---|---|\n| thing | in | thing |  |\n")),
}


class Facts:
    """An example's facts, standing in for a Model in model_check.solve."""

    def __init__(self, text):
        self.text = text

    def asp(self):
        return self.text


def rules():
    """Every rule as (code, label, failing, passing, kind of example): model.lp's in its order, then LEXICON's."""
    text = LP.read_text()
    examples = {(m.group(1), m.group(2)): m.group(3).strip() for m in EXAMPLE.finditer(text)}
    out = [(c, label, examples.get(("fail", c)), examples.get(("pass", c)), "facts")
           for c, label in LABEL.findall(text)]
    return out + [(c, label, fail, ok, "lexicon") for c, (label, fail, ok) in LEXICON.items()]


def fires(code, example, kind):
    """Whether the rule `code` fires on the example: model.lp solved over its facts, or `model lexicon --check`'s
    problems of a spec/index.md written from it."""
    if kind == "facts":
        return any(name == code for name, _ in solve(Facts(example))[0])
    import spec_lexicon
    with tempfile.TemporaryDirectory() as root:
        (Path(root) / "spec").mkdir()
        index = INDEX.replace("codified-1", "codified-2") if code in FOUR else INDEX
        (Path(root) / "spec" / "index.md").write_text(index + example)
        return any(found[0] == code for found in spec_lexicon.problems(spec_lexicon.read(root)))


def wrong(entries):
    """Why each example does not do what it says: a rule with no example, a failing one it does not fire on, a
    passing one it fires on."""
    out = []
    for code, _, fail, ok, kind in entries:
        if not fail or not ok:
            out.append("%s has no %s example" % (code, "failing" if not fail else "passing"))
            continue
        if not fires(code, fail, kind):
            out.append("%s does not fire on its failing example" % code)
        if fires(code, ok, kind):
            out.append("%s fires on its passing example" % code)
    return out


def implemented(code, kind):
    """Where a rule is implemented: model.lp for its rules, and each module of the plugin that gives the code."""
    found = ["scripts/model.lp"] if kind == "facts" else []
    here = Path(__file__).resolve()
    for path in sorted((PLUGIN / "scripts").glob("*.py")):
        if path != here and '"%s"' % code in path.read_text():
            found.append(path.relative_to(PLUGIN).as_posix())
    return found


def citing(root):
    """{code: [<capability>#r<n>, ...]}: each requirement line of the context's capabilities that names a code in
    backticks or quotes."""
    out = {}
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        for n, line in re.findall(r"^- \[r(\d+)\] (.*)$", path.read_text(), re.MULTILINE):
            for code in re.findall(r"[`\"](v\w+|w_\w+)[`\"]", line):
                out.setdefault(code, []).append("%s#r%s" % (path.stem, n))
    return out


def block(example, kind):
    text = "\n".join(re.split(r"(?<=\.) +", example)) if kind == "facts" else example.rstrip("\n")
    return "  ```%s\n%s\n  ```" % ("prolog" if kind == "facts" else "markdown",
                                   "\n".join("  " + line if line else "" for line in text.splitlines()))


def render(root, entries):
    cited = citing(root)
    out = ["# Rule catalogue", "",
           ("Generated by `model rules --write` from `scripts/model.lp` and the rules of `model lexicon --check`; do "
            "not edit. `model rules --check` says whether it is current. A requirement line names a rule by its code."),
           ""]
    for code, label, fail, ok, kind in entries:
        out += ["## %s" % code, "", label, "",
                "- Severity: %s" % ("warning" if code.startswith("w_") else "violation"),
                "- Implemented in: %s" % ", ".join("`%s`" % p for p in implemented(code, kind)),
                "- Cited by: %s" % (", ".join(cited.get(code, [])) or "no line"),
                "- Fails on:", "", block(fail, kind), "",
                "- Passes on:", "", block(ok, kind), ""]
    return "\n".join(out)


def catalogue(root, write=False, check=False):
    """--write writes the rule catalogue, --check says whether the one on disk is what --write would write; both
    refuse when an example does not do what it says."""
    entries = rules()
    problems = wrong(entries)
    if problems:
        print("the rule catalogue cannot be written: " + "; ".join(problems), file=sys.stderr)
        return 1
    text = render(root, entries)
    path = Path(root) / CATALOGUE
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print("wrote %s: %d rules" % (CATALOGUE, len(entries)))
        return 0
    if path.is_file() and path.read_text() == text:
        print("%s is current" % CATALOGUE)
        return 0
    print("stale: the rule catalogue %s is not what `model rules --write` would write" % CATALOGUE)
    return 1
