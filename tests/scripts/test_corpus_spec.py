"""The spec corpus (b240's acceptance corpus, grammar/corpus/spec/README.md): each block of a file
`grammar/corpus/spec/<capability>.md` is a requirement line under its id, with its trace and the logical form it is
meant to have. Four checks: (1) the line parses in grammar 4 to one meaning whose form `model parse --form` prints as
the block's; (2) that form translates to the check's facts and, for a "shall" line, to steps, with no refusal; (3) for
each file whose marker is codified-2, its corpus file holds a block for every live id and no other, each block's line
the file's line word for word; (4) the line's tree linearises back to the line.

The checks are proved on a copy of tests/scripts/fixtures/codified-2/ with one capability and its corpus file."""
import pathlib
import re
import shutil
import sys

import pytest
import spec_context
import spec_grammar4
import spec_lf
import spec_lf_read
import spec_read
import spec_rgl_steps
import spec_steps4

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
HEADING = re.compile(r"^## (\S+)\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
CRASH = (AttributeError, IndexError, KeyError, TypeError, ValueError)     # a translator's fault, not a refusal
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


def corpus(root):
    """{file stem: {id: (trace, line, form)}} of the corpus files under `root`; a section with no block or more than
    one gives (trace, None, None)."""
    out = {}
    for path in sorted((pathlib.Path(root) / "grammar" / "corpus" / "spec").glob("*.md")):
        if path.name == "README.md":
            continue
        found = out[path.stem] = {}
        for ident, body in HEADING.findall(path.read_text()):
            trace = body.split("\n", 1)[0].strip()
            blocks = BLOCK.findall(body)
            found[ident] = (trace, *blocks[0].split("\n", 1)) if len(blocks) == 1 else (trace, None, None)
    return out


def live(root):
    """{file stem: {id: line}} of the files of `root`'s spec whose marker is codified-2."""
    spec, out = pathlib.Path(root) / "spec", {}
    for path in sorted((spec / "capabilities").glob("*.md")):
        if spec_read.codified(path, (spec_read.MARKER4,)):
            cap = spec_read.capability(path, (spec_read.MARKER4,))
            out[path.stem] = {r.id: r.text for g in cap.groups for r in g.requirements}
    if spec_read.codified(spec / "universal.md", (spec_read.MARKER4,)):
        out["universal"] = {u.id: u.text for u in spec_read.universal(root)}
    return out


def ident(stem, rid):
    return rid if stem == "universal" else "%s#%s" % (stem, rid)


def reading(root, stem, rid, line):
    """What is wrong with one block's line, by checks 1, 2 and 4: [] when nothing, and the line's form."""
    parsed = spec_grammar4.parse(root, line)
    if not parsed.tree:
        return ["(1) %s" % parsed.refusal], None
    vocab = spec_grammar4.load(root)[0]
    why = spec_lf_read.refusal(vocab, parsed.tree)
    if why:
        return ["(1) %s" % why], None
    form = spec_lf.form(vocab, parsed.tree)
    wrong = []
    try:
        _, why = spec_context.Four(root, True).facts(ident(stem, rid), line)
    except CRASH as err:        # a translator that fails is a fault of the corpus, named as a refusal is
        why = "%s: %s" % (type(err).__name__, err)
    if why:
        wrong.append("(2) facts: %s" % why)
    if form.modality == "shall":        # a permission and a necessity have no steps (features_generate4)
        steps = spec_rgl_steps.load(root)[0]
        try:
            spec_steps4.cases(steps, [(ident(stem, rid), spec_lf.form(steps, parsed.tree))])
        except (spec_steps4.TraceError, ValueError) as err:
            wrong.append("(2) steps: %s" % err)
        except CRASH as err:
            wrong.append("(2) steps: %s: %s" % (type(err).__name__, err))
    back = spec_grammar4.linearise(root, parsed.tree)
    if back != line:
        wrong.append("(4) linearises as %r" % back)
    return wrong, spec_lf.show(form)


def faults(root):
    """Every fault of the corpus under `root` against its spec, each "<file> <id>: (n) why"."""
    out, have, spec = [], corpus(root), live(root)
    for stem, blocks in sorted(have.items()):
        for rid, (trace, line, form) in blocks.items():
            if not trace or trace.startswith("```"):
                out.append("%s %s: no trace line" % (stem, rid))
            if line is None:
                out.append("%s %s: not one reading block" % (stem, rid))
                continue
            wrong, shown = reading(root, stem, rid, line)
            if shown is not None and shown != form:
                wrong.insert(0, "(1) reads as\n%s" % shown)
            out += ["%s %s: %s" % (stem, rid, w) for w in wrong]
    for stem, lines in sorted(spec.items()):
        blocks = have.get(stem, {})
        for rid in sorted(set(lines) - set(blocks)):
            out.append("%s %s: (3) a live line with no block" % (stem, rid))
        for rid in sorted(set(blocks) - set(lines)):
            out.append("%s %s: (3) a block of no live line" % (stem, rid))
        for rid in sorted(set(lines) & set(blocks)):
            if blocks[rid][1] is not None and blocks[rid][1] != lines[rid]:
                out.append("%s %s: (3) the block's line is not the file's" % (stem, rid))
    return out


def test_the_corpus_of_this_repository_holds():
    toolchain.require()
    assert faults(REPO) == []


def test_every_file_of_this_repository_s_spec_says_codified_2():
    """The plan's done (b240, phase 24): every capability file and `spec/universal.md` say codified-2, so check 3
    covers every line of the spec."""
    spec = REPO / "spec"
    files = sorted((spec / "capabilities").glob("*.md")) + [spec / "universal.md"]
    assert [p.name for p in files if not spec_read.codified(p, (spec_read.MARKER4,))] == []


# --- the checks proved on a fixture ---------------------------------------------------------------------------------

LINES = ["When a session ends a stage, `work` shall print the stage.",
         "When the person runs `work backlog` with the `--json` option, `work` shall exit successfully."]
FORMS = [("shall [x3: tool `work` (constant)]\n  when [x1: session, x2: stage]\n    end(e1, subject: x1, object: x2)\n"
          "  response\n    print(e2, subject: x3, object: x2)"),
         None]


def capability(lines):
    body = "\n".join("- [r%d] %s" % (k, line) for k, line in enumerate(lines, 1))
    return ("---\nid: capability/example.org/fixture/shelf\ntitle: shelf\nnarrator: a client\ngroup: service\n"
            "language: codified-2\nrests_on: []\nretired: []\n---\n\n# shelf\n\n## Purpose\nSomething.\n\n"
            "## Behaviour\n\n### [g1] the lines\n%s\n\n## Not yet\n- None.\n" % body)


def block(rid, line, form, trace="Kept."):
    return "## %s\n%s\n\n```reading\n%s\n%s\n```\n" % (rid, trace, line, form)


@pytest.fixture
def world(tmp_path):
    """A copy of the codified-2 fixture with the capability `shelf` of LINES, and a writer of its corpus file."""
    toolchain.require()
    shutil.copytree(FIXTURE, tmp_path, dirs_exist_ok=True)
    (tmp_path / "spec" / "capabilities").mkdir()
    (tmp_path / "spec" / "capabilities" / "shelf.md").write_text(capability(LINES))
    (tmp_path / "grammar" / "corpus" / "spec").mkdir(parents=True)

    def write(*blocks):
        (tmp_path / "grammar" / "corpus" / "spec" / "shelf.md").write_text("# shelf\n\n" + "\n".join(blocks))
        return faults(tmp_path)
    return write


def right(root):
    """The blocks of LINES with their right forms: the second line's form as the parser prints it was read against
    the line, atom by atom (an option of a command, its code a constant)."""
    form = reading(root, "shelf", "r2", LINES[1])[1]
    assert "option" in form and "`--json`" in form
    return [block("r1", LINES[0], FORMS[0]), block("r2", LINES[1], form)]


def test_a_corpus_with_the_right_forms_holds(world, tmp_path):
    world()
    assert world(*right(tmp_path)) == []


def test_a_wrong_form_fails_check_1(world, tmp_path):
    good = right(tmp_path)
    wrong = block("r1", LINES[0], FORMS[0].replace("print(e2", "write(e2"))
    said = world(wrong, good[1])
    assert len(said) == 1 and said[0].startswith("shelf r1: (1) reads as\nshall [x3: tool `work` (constant)]")


def test_a_line_that_does_not_parse_fails_check_1(world, tmp_path):
    good = right(tmp_path)
    said = world(good[0], good[1], block("r9", "When a session ends a stage, `work` shall print the.", "x"))
    assert said[0].startswith("shelf r9: (1) ") and said[1] == "shelf r9: (3) a block of no live line"


def test_a_form_with_no_steps_fails_check_2(world, tmp_path):
    line = "When the person runs `work start`, `work` shall print a stage or a file."
    said = world(*right(tmp_path), block("r9", line, reading(tmp_path, "shelf", "r9", line)[1]))
    assert said == ["shelf r9: (2) facts: refused: no translation of or in a response",
                    "shelf r9: (2) steps: no Then of or", "shelf r9: (3) a block of no live line"]


def test_a_live_line_with_no_block_or_another_line_fails_check_3(world, tmp_path):
    good = right(tmp_path)
    assert world(good[0]) == ["shelf r2: (3) a live line with no block"]
    other = block("r2", LINES[0], FORMS[0])
    assert world(good[0], other) == ["shelf r2: (3) the block's line is not the file's"]


def test_a_block_with_no_trace_fails(world, tmp_path):
    good = right(tmp_path)
    assert world(good[0], good[1].replace("Kept.\n", "")) == ["shelf r2: no trace line"]


def test_a_line_that_linearises_otherwise_fails_check_4(world, tmp_path):
    line = LINES[0].replace(", `work`", ",  `work`")
    world()
    assert reading(tmp_path, "shelf", "r1", line)[0] == ["(4) linearises as %r" % LINES[0]]
