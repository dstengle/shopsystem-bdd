"""`features bindings --unbound` reads each test module once (b457): one `ast.parse` a module however many of its
readings (bindings, scenarios(...) calls, unbound scenarios) the command makes."""
import ast
import json
from types import SimpleNamespace

import features_bindings

BOUND = 'from pytest_bdd import scenario, scenarios\n\n\n@scenario("a.feature", "one")\ndef test_one():\n    pass\n'
WHOLE = 'from pytest_bdd import scenarios\n\nscenarios("b.feature")\n'


def project(tmp_path):
    tests = tmp_path / "tests"
    (tests / "sub").mkdir(parents=True)
    (tests / "test_a.py").write_text(BOUND)
    (tests / "sub" / "test_b.py").write_text(WHOLE)
    (tests / "sub" / "helper.py").write_text("X = 1\n")
    feature = tmp_path / "features"
    feature.mkdir()
    files = [(str(feature / "a.feature"), SimpleNamespace(scenarios=[SimpleNamespace(title="one"),
                                                                     SimpleNamespace(title="two")])),
             (str(feature / "b.feature"), SimpleNamespace(scenarios=[SimpleNamespace(title="three")]))]
    return SimpleNamespace(tests=str(tests), dir=str(feature), unbound=[], json=True), files


def test_each_module_is_parsed_once(tmp_path, monkeypatch, capsys):
    args, files = project(tmp_path)
    parsed, real = [], ast.parse
    monkeypatch.setattr(features_bindings.ast, "parse", lambda source, path="<unknown>", *a, **k: (
        parsed.append(path), real(source, path, *a, **k))[1])
    assert features_bindings.cmd_bindings(args, files) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["wrong"] == []
    assert [(u["title"], u["bound_by"]) for u in report["unbound"]] == [("two", [])]
    assert sorted(parsed) == sorted(set(parsed)) and len(parsed) == 3, parsed


def test_a_changed_module_is_parsed_again(tmp_path):
    args, _ = project(tmp_path)
    assert [c[3].value for c in features_bindings.binding_calls(args.tests)] == ["one"]
    (tmp_path / "tests" / "test_a.py").write_text(BOUND.replace('"one"', '"one again"'))
    assert [c[3].value for c in features_bindings.binding_calls(args.tests)] == ["one again"]
