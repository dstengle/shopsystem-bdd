"""Grammar 4's relative clauses factored as the RGL's RelCN does (b437): a relative clause is built once, of the kind
it may follow (`O_RS`), and attached to the noun of each kind under it (`K_RelCN_O`), in place of a fun per gap and
kind. A refactor with no change of meaning: every live line of this repository and of docs/examples/notes-cli/ reads
to the logical form it read to before, kept in tests/scripts/fixtures/grammar4-factored/forms.json, which `write`
made from the grammar before the factoring."""
import json
import pathlib
import sys

import spec_grammar4
import spec_lf
import spec_lf_read
import spec_read

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
ROOTS = {"repository": REPO, "notes-cli": REPO / "docs" / "examples" / "notes-cli"}
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "grammar4-factored" / "forms.json"


def lines(root):
    """{id: line} of every live line of `root`'s codified-2 files."""
    spec, out = pathlib.Path(root) / "spec", {}
    for path in sorted((spec / "capabilities").glob("*.md")):
        if spec_read.codified(path, (spec_read.MARKER4,)):
            cap = spec_read.capability(path, (spec_read.MARKER4,))
            out.update(("%s#%s" % (path.stem, r.id), r.text) for g in cap.groups for r in g.requirements)
    if spec_read.codified(spec / "universal.md", (spec_read.MARKER4,)):
        out.update((u.id, u.text) for u in spec_read.universal(root))
    return out


def reading(root, line):
    """The logical form `spec parse --form` prints of `line`, or its refusal."""
    parsed = spec_grammar4.parse(root, line)
    if not parsed.tree:
        return "refused: %s" % parsed.refusal
    vocab = spec_grammar4.load(root)[0]
    why = spec_lf_read.refusal(vocab, parsed.tree)
    return "refused: %s" % why if why else spec_lf.show(spec_lf.form(vocab, parsed.tree))


def forms():
    """{root's name: {id: {line, form}}} of every live line."""
    return {name: {rid: {"line": line, "form": reading(root, line)} for rid, line in sorted(lines(root).items())}
            for name, root in ROOTS.items()}


def write():
    """The fixture written from the grammar as it is."""
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(forms(), indent=1, sort_keys=True) + "\n")


def test_every_live_line_reads_to_the_form_it_read_to_before_the_factoring():
    toolchain.require()
    kept, now = json.loads(FIXTURE.read_text()), forms()
    changed = ["%s %s: %s\n  was: %s\n  now: %s" % (name, rid, line["line"], line["form"],
                                                   now[name].get(rid, {}).get("form"))
               for name, ids in kept.items() for rid, line in ids.items()
               if now[name].get(rid, {}).get("line") == line["line"] and now[name][rid]["form"] != line["form"]]
    assert changed == []


def test_no_live_line_is_refused():
    assert [(name, rid) for name, ids in json.loads(FIXTURE.read_text()).items() for rid, line in ids.items()
            if line["form"].startswith("refused")] == []


def test_the_grammar_makes_no_fun_per_gap_and_kind():
    toolchain.require()
    for root in ROOTS.values():
        source = "\n".join(spec_grammar4.sources(root)[1].values())
        assert "_Obj_" not in source
