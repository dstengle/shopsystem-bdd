"""A driven port an item makes (b701): laid over a spec, the port's model file importing the areas whose words its
lines say, a port area spec/model/ held already among them (f1)."""
from types import SimpleNamespace

import backlog_port
from backlog_section import read

INDEX = "---\nid: bounded-context/ex.com/prod/ctx\nlanguage: codified-2\n---\n\n# Ctx\n"
NOTES = "---\nid: model/ex.com/prod/ctx/notes\narea: notes\nkind: core\nimports: []\n---\n\n# Notes\n\n```model\nobject note\n```\n"
STOCK = "---\nid: model/ex.com/prod/ctx/stock\narea: stock\nkind: port\nimports: []\n---\n\n# Stock\n\n```model\n```\n"
WORDS = "---\nid: vocabulary/ex.com/prod/ctx/notes\narea: notes\n---\n\n# The words of notes\n\n## Terms\n- **note** (noun) → object note. A note. Plural: notes.\n"
REQUIREMENTS = ("### stock-port\n\nnarrator: the notes service\ngroup: service\npurpose: Stock.\narea: stock\nkind: port\n\n"
                "#### [g1] A note reserved is reserved\n- [r1] When the notes service reserves a note, the stock "
                "service shall not refuse the request.")


def _repo(tmp_path, stock=STOCK):
    spec = tmp_path / "spec"
    for rel, text in (("index.md", INDEX), ("model/notes.md", NOTES), ("model/stock.md", stock),
                      ("vocabulary/notes.md", WORDS)):
        (spec / rel).parent.mkdir(parents=True, exist_ok=True)
        (spec / rel).write_text(text)
    return read(SimpleNamespace(sections={"Requirements": REQUIREMENTS}, name="b1"), "the item b1")


def test_an_existing_port_area_imports_the_area_its_lines_say(tmp_path):
    blocks = _repo(tmp_path)
    files = []
    backlog_port.lay(tmp_path, blocks, files)
    stock = tmp_path / "spec" / "model" / "stock.md"
    assert "imports: [notes]\n" in stock.read_text(), stock.read_text()
    assert "spec/model/stock.md" in files


PLOTS = "---\nid: model/ex.com/prod/ctx/plots\narea: plots\nkind: core\nimports: []\n---\n\n# Plots\n\n```model\nobject plot\n```\n"
PLOT_WORDS = "---\nid: vocabulary/ex.com/prod/ctx/plots\narea: plots\n---\n\n# The words of plots\n\n## Terms\n- **plot** (noun) → object plot. A plot. Plural: plots.\n"
TWO = ("### plots\n\nnarrator: a gardener\ngroup: service\npurpose: Plots.\n\n#### [g1] A plot\n- [r1] When the person "
       "adds a note, the notes service shall keep the note.\n\n### watering\n\nnarrator: a gardener\ngroup: service\n"
       "purpose: Watering.\n\n#### [g1] A plot watered\n- [r1] When the person adds a plot, the notes service shall "
       "keep the plot.\n\n### notebook\n\n#### [g2] A plot noted\n- [r2] When the person adds a plot, the notes "
       "service shall keep the plot.")
NOTEBOOK = "---\narea: notes\nlanguage: codified-2\nretired: []\n---\n\n# Notebook\n\n## Behaviour\n"


def test_two_areas_an_item_makes_import_the_one_whose_word_the_other_says(tmp_path):
    """b830: a core area the item makes, whose line says a word of another area it makes, laid with its model file
    importing that area, as is an area the spec holds whose item line says it."""
    _repo(tmp_path)
    (tmp_path / "spec" / "capabilities").mkdir()
    (tmp_path / "spec" / "capabilities" / "notebook.md").write_text(NOTEBOOK)
    blocks = read(SimpleNamespace(sections={"Requirements": TWO}, name="b1"), "the item b1")
    plots, words = tmp_path / "spec" / "model" / "plots.md", tmp_path / "spec" / "vocabulary" / "plots.md"
    plots.write_text(PLOTS)                         # as backlog_model lays the item's model lines before
    words.write_text(PLOT_WORDS)
    files = []
    backlog_port.lay(tmp_path, blocks, files)
    watering = tmp_path / "spec" / "model" / "watering.md"
    assert "plots" in watering.read_text().split("imports: [", 1)[1].split("]")[0], watering.read_text()
    assert "spec/model/watering.md" in files
    assert "imports: [plots]\n" in (tmp_path / "spec" / "model" / "notes.md").read_text()
