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


# --- the lines against the model (v_m2-v_m7, model_domain_lines), each on a broken copy of the fixture -------------
def _codes(tmp_path, model=None, line=None, facts=()):
    """`model check`'s v_m and w_m codes on a copy of the fixture, its model's text changed by `model` (old, new) and
    a line added as r10, and `facts` laid beside the copy's."""
    import shutil

    import model_check
    import model_facts
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    if model:
        path = root / "spec" / "model" / "notes.md"
        assert model[0] in path.read_text()
        path.write_text(path.read_text().replace(*model))
    if line:
        cap = root / "spec" / "capabilities" / "notebook.md"
        cap.write_text(cap.read_text() + "\n### [g10] Added\n- [r10] %s\n" % line)
    read = model_facts.Model(root).read()
    read.facts += [(f[0], tuple(f[1:])) for f in facts]
    found, _ = model_check.solve(read)
    return sorted((name,) + tuple(args) for name, args in found if name[:3] in ("v_m", "w_m"))


def test_the_fixture_breaks_none_of_the_line_rules(tmp_path):
    assert _codes(tmp_path) == []


def test_v_m2_a_parameter_or_value_the_operation_does_not_declare(tmp_path):
    # grammar 4 generates only declared parameters and values, so no line that parses says one: the rule's facts
    assert _codes(tmp_path, facts=[("req_param", "q#r1", "notes.add", "colour"),
                                   ("req_value", "q#r1", "notes.add", "priority", "urgent")]) == [
        ("v_m2", "q#r1", "colour"), ("v_m2", "q#r1", "priority")]


def test_v_m3_a_requester_the_operation_does_not_allow(tmp_path):
    found = _codes(tmp_path, model=("operation add(text, priority, reminder (flag))",
                                    "operation add(text, priority, reminder (flag)) by the upstream"))
    assert ("v_m3", "capability/example.org/fixture/domain-model/notebook#r1", "the person") in found


def test_v_m4_a_declared_reason_no_line_states(tmp_path):
    found = _codes(tmp_path, model=("refused: no text", "refused: no text, no priority"))
    assert found == [("v_m4", "notes.add", "no priority")]


def test_w_m5_a_transition_no_line_causes(tmp_path):
    found = _codes(tmp_path, model=("draft → retired", "draft → retired; retired → draft"))
    assert found == [("w_m5", "note", "status", "retired", "draft")]


def test_v_m6_a_set_the_lifecycle_does_not_allow(tmp_path):
    found = _codes(tmp_path, line="While a note is `active`, when the person files the note, the notes service shall "
                                  "set the status of the note to `draft`.")
    assert found == [("v_m6", "capability/example.org/fixture/domain-model/notebook#r10", "status", "active",
                      "draft")]


def test_v_m7_an_operation_no_line_requests(tmp_path):
    found = _codes(tmp_path, model=("  operation list()", "  operation pin(note)  outcomes: done\n  operation list()"))
    assert found == [("v_m7", "notes.pin")]
