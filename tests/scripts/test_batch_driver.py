"""The batch brief `work batch start` writes (b389): its acceptance-test command loads the plugin's pytest plugin, and
for a context with no step bindings, program or adapter contract yet it says how the first task makes them."""
from types import SimpleNamespace

import batch_driver
from batch_git import SCRIPTS
from batch_plan import Batch, Task


def _brief(root, monkeypatch, ids=("notes#r1", "notes#r2")):
    monkeypatch.setattr(batch_driver, "push_prefix", lambda root: None)
    monkeypatch.setattr(batch_driver.backlog_lines, "read", lambda item, rel: None)
    monkeypatch.setattr(batch_driver.backlog_lines, "ids", lambda _blocks: list(ids))
    monkeypatch.setattr(batch_driver.backlog_chore, "said", lambda item: [])
    batch = Batch(name="batch-1", ident="batch/x/batch-1", status="building", base="main", forked_from="0",
                  branch="batch-1", pull_request=None, tasks=[Task("t1", "b7", "pending", "batch-1-b7")])
    return batch_driver.text(root, batch, [SimpleNamespace(name="b7", title="Add a note")])


def _built(root):
    (root / "spec" / "model").mkdir(parents=True)
    (root / "spec" / "adapters").mkdir()
    (root / "spec" / "adapters" / "cli.toml").write_text("[programs]\n", encoding="utf-8")
    (root / "tests" / "scenarios").mkdir(parents=True)
    (root / "tests" / "scenarios" / "test_notes.py").write_text("", encoding="utf-8")


def test_the_acceptance_tests_load_the_plugins_pytest_plugin(tmp_path, monkeypatch):
    _built(tmp_path)
    text = _brief(tmp_path, monkeypatch)
    assert ("`PYTHONPATH=%s python3 -m pytest -p work_items -q tests/scenarios/test_notes.py -m \"r1 or r2\"`"
            % SCRIPTS) in text


def test_a_context_with_its_bindings_and_contract_gets_no_first_batch_section(tmp_path, monkeypatch):
    _built(tmp_path)
    assert "## A fresh context" not in _brief(tmp_path, monkeypatch)


def test_a_capability_with_no_test_module_is_bound_by_its_task(tmp_path, monkeypatch):
    _built(tmp_path)
    (tmp_path / "tests" / "scenarios" / "test_notes.py").unlink()
    text = _brief(tmp_path, monkeypatch)
    assert "- Step bindings: none yet; this task writes tests/scenarios/test_notes.py" in text
    assert "## A fresh context" in text and "features vocab" in text
    assert "%s, step 6, shows a whole module" % (SCRIPTS.parent / "docs" / "getting-started.md") in text


def test_a_context_with_a_model_and_no_adapter_contract_is_told_how_to_make_one(tmp_path, monkeypatch):
    _built(tmp_path)
    (tmp_path / "spec" / "adapters" / "cli.toml").unlink()
    text = _brief(tmp_path, monkeypatch)
    assert "## A fresh context" in text
    assert "spec/adapters/cli.toml" in text and "spec annotate" in text and "v_a1" in text
    assert "a remote and gh" in text


def test_batch_rules_that_are_not_a_list_of_texts_are_refused(tmp_path):
    (tmp_path / ".shop").mkdir()
    (tmp_path / ".shop" / "delivery.toml").write_text('[batch]\nrules = "one"\n', encoding="utf-8")
    try:
        batch_driver.batch_rules(tmp_path)
    except batch_driver.Refused as why:
        assert "[batch] rules is not a list of texts" in str(why)
    else:
        raise AssertionError("a text in place of a list was taken")
