"""spec_packs: the packs a context imports, their layers, v_t16 and v_t17, and the plugin's CLI pack (call 11)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import spec_packs


def context(tmp_path, imports, glossary, **packs):
    (tmp_path / "spec" / "packs").mkdir(parents=True)
    (tmp_path / "spec" / "index.md").write_text("---\nid: bounded-context/x\nimports: [%s]\n---\n# x\n\n## Glossary\n\n%s"
                                                % (imports, glossary))
    for name, text in packs.items():
        (tmp_path / "spec" / "packs" / ("%s.md" % name)).write_text("# %s\n\n## Glossary\n\n%s" % (name, text))
    return tmp_path


def test_the_layers_run_from_the_packs_in_import_order_to_the_glossary(tmp_path):
    root = context(tmp_path, "cli, p1", "- **thing** (noun): a thing.\n", p1="- **widget** (noun): a widget.\n")
    layers = [(layer, t.term) for layer, t in spec_packs.layers(root)]
    assert layers[0] == ("pack cli", "tool")
    assert layers.index(("pack p1", "widget")) < layers.index(("spec/index.md", "thing"))
    assert spec_packs.problems(root) == []


def test_an_import_of_no_pack_is_v_t17(tmp_path):
    root = context(tmp_path, "p9", "- **thing** (noun): a thing.\n")
    assert [p[:2] for p in spec_packs.problems(root)] == [("v_t17", "p9")]


def test_a_word_a_pack_defines_needs_redefines_naming_that_pack(tmp_path):
    root = context(tmp_path, "p1, p2", "- **widget** (noun): a widget. Redefines: p2.\n",
                   p1="- **widget** (noun): one.\n", p2="- **widget** (noun): two.\n")
    assert spec_packs.unmarked(root) == {("spec/index.md", "widget"): ["p1"]}
    assert [p[:2] for p in spec_packs.problems(root)] == [("v_t16", "widget")]


def test_the_cli_pack_holds_the_command_line_words_and_defines_refuse():
    text = (spec_packs.PLUGIN / "cli.md").read_text()
    words = {t.term for t in spec_packs.terms(spec_packs.PLUGIN / "cli.md", "grammar/packs/cli.md")}
    assert words == {"tool", "command", "option", "reason", "output", "artifact", "run", "print", "exit", "change",
                     "refuse", "conform", "name"}
    assert "A tool refuses a command when it exits with an error on it." in text.split("## Definitions", 1)[1]


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_outer_names_the_base_kinds_and_the_cli_packs_kinds():
    """b199: in a codified-2 context the old lexicon reader's frames may name grammar 4's base kinds and the imported
    packs' kinds and actors; a codified-1 context has none."""
    import spec_rgl_vocab
    outer = spec_rgl_vocab.outer(FIXTURES / "codified-2")
    assert {"thing", "agent", "tool", "command", "option", "reason", "output"} <= outer
    assert spec_rgl_vocab.outer(FIXTURES / "glossary") == frozenset()


REPO = Path(__file__).resolve().parents[2]


def test_the_spec_pack_holds_the_words_for_talking_about_specs():
    """b240, quote-23: a line about the language names a construct by its code, "a requirement that uses
    `rc-object`", and a rule finding names its rule, "a term that violates `v_t11`"."""
    path = spec_packs.PLUGIN / "spec.md"
    words = {t.term: t for t in spec_packs.terms(path, "grammar/packs/spec.md")}
    assert set(words) == {"requirement", "construct", "rule", "use", "violate"}
    assert "Frame: requirement uses construct." in words["use"].text
    assert "Frame: thing violates rule." in words["violate"].text
    assert "grammar/constructs.md" in words["construct"].text and "grammar/rules.md" in words["rule"].text


def test_this_repository_imports_the_spec_pack_and_marks_its_own_words():
    assert spec_packs.imports(REPO) == ["cli", "spec"]
    assert spec_packs.problems(REPO) == []


def test_a_line_names_a_construct_by_its_code_in_a_context_importing_the_spec_pack(tmp_path):
    import spec_grammar4
    sys.path.insert(0, str(REPO / "tests"))
    import toolchain
    toolchain.require()
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text(
        "---\nid: bounded-context/x\nlanguage: codified-2\nimports: [cli, spec]\n---\n# x\n\n## Glossary\n\n"
        "- **`model`** (proper noun): the tool of the model. Kind of: tool.\n- **the person** (proper noun): the "
        "human. Kind of: agent.\n")
    uses = "When the person runs `model parse` on a requirement that uses `rc-object`, `model` shall exit successfully."
    violates = ("When the person runs `model check` on a requirement that violates `v_t11`, `model` shall print the "
                "requirement.")
    for line in (uses, violates):
        assert spec_grammar4.parse(tmp_path, line).tree, spec_grammar4.parse(tmp_path, line).refusal
