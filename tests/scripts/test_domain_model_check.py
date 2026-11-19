"""domain_model_check: the domain model's own rules, v_m8 (the domain contract design, §5.5)."""
import pathlib

import domain_model
import domain_model_check

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"


def _model(tmp_path, block):
    (tmp_path / "spec" / "model").mkdir(parents=True)
    (tmp_path / "spec" / "model" / "a.md").write_text("---\narea: a\nkind: core\n---\n\n```model\n" + block + "```\n")
    return domain_model.read(tmp_path)


def _found(tmp_path, block):
    return [(code, subject) for code, subject, _ in domain_model_check.problems(_model(tmp_path, block))]


def test_a_relation_to_an_undeclared_object(tmp_path):
    assert _found(tmp_path, "object note\n  relations: carries → tag (many)\n") == [("v_m8", "note.carries")]


def test_an_attribute_naming_an_undeclared_object(tmp_path):
    assert _found(tmp_path, "object note\n  attributes: shelf → shelf\n") == [("v_m8", "note.shelf")]


def test_a_transition_over_an_undeclared_value(tmp_path):
    block = "object note\n  attributes: status: draft | kept\n  lifecycle status: draft → kept; kept → gone\n"
    found = domain_model_check.problems(_model(tmp_path, block))
    assert [(c, s) for c, s, _ in found] == [("v_m8", "note.status")]
    assert "gone" in found[0][2]


def test_two_operations_of_one_name_in_a_service(tmp_path):
    block = "service notes\n  operation add(text)\n  operation add(title)\n"
    assert _found(tmp_path, block) == [("v_m8", "notes.add")]


def test_an_event_raised_by_no_operation(tmp_path):
    block = "service notes\n  operation add(text)\nevent a note is kept: raised by notes.keep\n"
    assert _found(tmp_path, block) == [("v_m8", "a note is kept")]


def test_an_element_declared_twice(tmp_path):
    assert _found(tmp_path, "object note\nobject note\n") == [("v_m8", "note")]


def test_relations_to_actors_and_services_are_declared(tmp_path):
    block = "object note\n  relations: of → the person (one); for → notes (one)\nactor the person\nservice notes\n"
    assert _found(tmp_path, block) == []


def test_the_fixture_is_clean():
    assert domain_model_check.problems(domain_model.load(FIXTURE)) == []
