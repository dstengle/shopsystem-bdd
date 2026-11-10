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
    assert words == {"tool", "command", "option", "reason", "output", "run", "print", "exit", "change", "refuse",
                     "name"}
    assert "A tool refuses a command when it exits with an error on it." in text.split("## Definitions", 1)[1]
