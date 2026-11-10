"""`model constructs --write` and `--check` (b240, quote-23): the construct catalogue `grammar/constructs.md`, one
entry a construct of grammar 4, so that a requirement line about the language names a construct by its code, as one
about a check names a rule by its code (`grammar/rules.md`, model_rules). Each entry gives the code, its label, its
form, the functions of the grammar it is made of, an example line, the example's reading (its logical form, as
`model parse --form` prints it) and the lines citing the code. It is generated, never edited: model_constructs_table's
entries, each example parsed in the catalogue's context `grammar/corpus/constructs/` before the file is written. The
catalogue cannot be written while a function of that context's grammar is no construct's, word's or glue's, or while
an example does not parse to one tree, is refused by a reading rule, does not linearise back word for word or does
not use its construct."""
import re
import sys
from pathlib import Path

from model_constructs_table import CONSTRUCTS, GLUE, WORDS

PLUGIN = Path(__file__).resolve().parents[1]
CONTEXT = PLUGIN / "grammar" / "corpus" / "constructs"
CATALOGUE = "grammar/constructs.md"


def roles(vocab):
    """{verb function: its frame's roles}: `object` (a kind right after the verb), `to` (a kind after "to"),
    `oblique` (a kind after any other fixed words) and `fixed` (fixed words with no kind after them)."""
    import spec_rgl
    out = {}
    for n, v in enumerate(vocab.verbs, 1):
        for m, (_, pieces) in enumerate(v.frames, 1):
            tags = set()
            for fixed, kind in pieces:
                tags.add("fixed" if kind is None else "object" if not fixed else
                         "to" if fixed == ("to",) else "oblique")
            out["e_%s_%s_%d_%d" % (spec_rgl.slug(v.term.term), v.aspect, n, m)] = tags
    return out


def pattern(funs, frames):
    """The regular expression of an entry's `funs`, a `frame:<role>` written out as the names of its verbs."""
    if funs.startswith("frame:"):
        names = sorted(f for f, tags in frames.items() if funs[len("frame:"):] in tags)
        return "|".join(map(re.escape, names)) or "(?!)"
    return funs


def uncovered(functions, frames):
    """The functions of the grammar that no construct, word or glue family covers."""
    every = [pattern(e["funs"], frames) for e in CONSTRUCTS] + [WORDS, GLUE]
    return sorted(f for f in functions if not any(re.fullmatch(p, f) for p in every))


def uses(entry, tree, frames):
    """Whether a tree uses the construct: holds its `uses`, else a function of its `funs`."""
    if entry["uses"]:
        return re.search(entry["uses"], tree) is not None
    funs = pattern(entry["funs"], frames)
    return re.search(r"(?<![\w])(?:%s)(?![\w])" % funs, tree) is not None


class Grammar:
    """The catalogue's context: its vocabulary, its compiled grammar's functions and its verbs' roles."""

    def __init__(self, root=CONTEXT):
        import spec_grammar4
        self.root = root
        self.vocab, gram = spec_grammar4.load(root)
        self.functions = list(gram.functions)
        self.frames = roles(self.vocab)

    def read(self, line):
        """(tree, reading, refusal): the line's one tree and its logical form, or why it has none."""
        import spec_grammar4
        import spec_lf
        import spec_lf_read
        p = spec_grammar4.parse(self.root, line)
        if not p.tree:
            return None, None, p.refusal
        refused = spec_lf_read.refusal(self.vocab, p.tree)
        if refused:
            return p.tree, None, refused
        if spec_grammar4.linearise(self.root, p.tree) != line:
            return p.tree, None, "it does not linearise back word for word"
        return p.tree, spec_lf.show(spec_lf.form(self.vocab, p.tree)), None


def entries(grammar):
    """(entry, reading) of every construct, and why the catalogue cannot be written (each problem named)."""
    problems = ["%s is no construct's, word's or glue's function" % f
                for f in uncovered(grammar.functions, grammar.frames)]
    codes = [e["code"] for e in CONSTRUCTS]
    problems += ["%s is the code of two constructs" % c for c in sorted({c for c in codes if codes.count(c) > 1})]
    out = []
    for e in CONSTRUCTS:
        if not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", e["code"]):
            problems.append("%s is not a code of words joined by hyphens" % e["code"])
        if not e["example"]:
            problems.append("%s has no example" % e["code"])
            continue
        tree, reading, refusal = grammar.read(e["example"])
        if refusal:
            problems.append("%s's example is refused: %s" % (e["code"], refusal))
        elif not uses(e, tree, grammar.frames):
            problems.append("%s's example does not use it" % e["code"])
        else:
            out.append((e, reading))
    return out, problems


def citing(root):
    """{code: [<capability>#r<n>, ...]}: each requirement line that names a construct's code in backticks."""
    codes = {e["code"] for e in CONSTRUCTS}
    out = {}
    for path in sorted((Path(root) / "spec" / "capabilities").glob("*.md")):
        for n, line in re.findall(r"^- \[r(\d+)\] (.*)$", path.read_text(), re.MULTILINE):
            for code in re.findall(r"`([a-z-]+)`", line):
                if code in codes:
                    out.setdefault(code, []).append("%s#r%s" % (path.stem, n))
    return out


def render(root, done):
    cited = citing(root)
    out = ["# Construct catalogue", "",
           ("Generated by `model constructs --write` from `scripts/model_constructs_table.py` and grammar 4 compiled in "
            "the catalogue's context, `grammar/corpus/constructs/`; do not edit. `model constructs --check` says "
            "whether it is current. A requirement line about the language names a construct by its code. Each "
            "example is parsed to one tree that uses its construct and linearises back word for word, and its "
            "reading is its logical form (`model parse --form`); `tests/scripts/test_model_constructs.py` reads each "
            "example again as part of the acceptance corpus."), "",
           "Words of a context, not constructs: `%s`." % WORDS, "",
           "The joints of every line, not constructs: `%s`." % GLUE, ""]
    for e, reading in done:
        out += ["## %s" % e["code"], "", e["label"], "",
                "- Form: %s" % e["form"],
                "- Functions: `%s`" % e["funs"],
                "- Cited by: %s" % (", ".join(cited.get(e["code"], [])) or "no line"),
                "- Example and its reading:", "",
                "```construct", e["example"], reading, "```", ""]
    return "\n".join(out)


def catalogue(root, write=False):
    """--write writes the construct catalogue, else (--check) says whether the one on disk is what --write would
    write; both refuse when the catalogue cannot be written, naming each problem."""
    done, problems = entries(Grammar())
    if problems:
        print("the construct catalogue cannot be written: " + "; ".join(problems), file=sys.stderr)
        return 1
    text = render(root, done)
    path = Path(root) / CATALOGUE
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print("wrote %s: %d constructs" % (CATALOGUE, len(done)))
        return 0
    if path.is_file() and path.read_text() == text:
        print("%s is current" % CATALOGUE)
        return 0
    print("stale: the construct catalogue %s is not what `model constructs --write` would write" % CATALOGUE)
    return 1
