"""domain_model: a `spec/model/<area>.md` block read into a Model (the domain contract design, §4.1)."""
import pathlib
import textwrap

import domain_model
import pytest
from plumbing.shop_refused import Refused

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"

DECISIONS = textwrap.dedent("""\
    ---
    id: model/example/specification
    area: specification
    kind: core
    imports: []
    ---

    # The specification

    ## Purpose

    Read by nothing.

    ```model
    object design-decision
      attributes: title, summary, wording (text); date (time);
                  tier: check | requirement | judgement
      lifecycle status: accepted → superseded   # created accepted;
                                                # no operation enters rejected
      relations: supersedes → design-decision (many); enforced by → test | requirement (many);
                 gives → route (one, optional)

    object test, requirement, route

    service decisions
      operation enter(title, summary, tier, wording, supersedes, enforced by,
                      date, form: short | long)     # as decision_write's argparse
        outcomes: done → the design-decision (status accepted) | refused: no tier, no summary,
                  id taken
      operation index()  outcomes: done → the decisions index
      operation audit()
        outcomes: passed | failed → each failing design-decision

    event a design-decision is entered: raised by decisions.enter
    actor the person kind of agent
    actor session
    ```
    """)


def _area(tmp_path, text=DECISIONS, name="specification"):
    (tmp_path / "spec" / "model").mkdir(parents=True, exist_ok=True)
    (tmp_path / "spec" / "model" / ("%s.md" % name)).write_text(text)
    return domain_model.load(tmp_path)


def test_the_design_decision_example_reads_whole(tmp_path):
    model = _area(tmp_path)
    area = model.areas["specification"]
    assert (area.kind, area.imports, area.id) == ("core", (), "model/example/specification")
    dd = model.objects["design-decision"]
    assert [a.name for a in dd.attributes] == ["title", "summary", "wording", "date", "tier", "status"]
    assert dd.attribute("tier").values == ("check", "requirement", "judgement")
    assert dd.attribute("title").type == "text" and dd.attribute("date").type == "time"
    assert dd.attribute("status").values == ("accepted", "superseded")
    assert dd.lifecycles[0].attribute == "status"
    assert dd.lifecycles[0].transitions == (("accepted", "superseded"),)
    rels = {r.phrase: r for r in dd.relations}
    assert rels["supersedes"].targets == ("design-decision",) and rels["supersedes"].card == "many"
    assert rels["enforced by"].targets == ("test", "requirement")
    assert rels["gives"].card == "one, optional"
    assert {"test", "requirement", "route"} <= set(model.objects)
    assert model.events[0].phrase == "a design-decision is entered"
    assert (model.events[0].service, model.events[0].operation) == ("decisions", "enter")
    assert model.actors["the person"].kind_of == "agent" and model.actors["session"].kind_of == ""


def test_an_operation_its_parameters_and_outcomes(tmp_path):
    model = _area(tmp_path)
    enter = model.services["decisions"].operation("enter")
    assert [p.name for p in enter.parameters] == ["title", "summary", "tier", "wording", "supersedes",
                                                   "enforced by", "date", "form"]
    assert enter.object == "design-decision"
    done, refused = enter.outcomes
    assert (done.kind, done.phrase) == ("done", "the design-decision (status accepted)")
    assert (refused.kind, refused.reasons) == ("refused", ("no tier", "no summary", "id taken"))
    audit = model.services["decisions"].operation("audit")
    assert [(o.kind, o.phrase) for o in audit.outcomes] == [("passed", ""), ("failed", "each failing design-decision")]
    assert model.services["decisions"].operation("index").outcomes[0].phrase == "the decisions index"


def test_a_parameter_typed_by_attribute_by_object_else_text(tmp_path):
    enter = _area(tmp_path).services["decisions"].operation("enter")
    types = {p.name: (p.type, p.values, p.targets) for p in enter.parameters}
    assert types["tier"] == ("values", ("check", "requirement", "judgement"), ())
    assert types["supersedes"] == ("object", (), ("design-decision",))
    assert types["enforced by"] == ("object", (), ("test", "requirement"))
    assert types["title"] == ("text", (), ()) and types["date"] == ("time", (), ())
    assert types["form"] == ("values", ("short", "long"), ())


def test_a_parameter_naming_an_object_is_that_object(tmp_path):
    text = DECISIONS.replace("  operation index()", "  operation withdraw(design-decision, reason)\n"
                                                    "  operation index()")
    op = _area(tmp_path, text).services["decisions"].operation("withdraw")
    assert op.object == "design-decision"
    assert [(p.type, p.targets) for p in op.parameters] == [("object", ("design-decision",)), ("text", ())]


def test_a_parameter_naming_an_imported_packs_kind_the_model_refers_to_is_that_kind(tmp_path):
    """b618: with `imports: [request, base]` the parameter `version`, which no object declares but a relation of the
    model names, is the base pack's kind, as an object's is; `reason`, the request pack's kind no element of the model
    names, stays text."""
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text("---\nid: bounded-context/x\nimports: [request, base]\n---\n# x\n")
    text = DECISIONS.replace("  operation index()", "  operation publish(design-decision, version, reason)\n"
                                                    "  operation index()")
    text = text.replace("object test, requirement, route", "object test, requirement\n\nobject route\n"
                        "  relations: has → version (one)")
    op = _area(tmp_path, text).services["decisions"].operation("publish")
    assert [(p.type, p.targets) for p in op.parameters] == [
        ("object", ("design-decision",)), ("object", ("version",)), ("text", ())]


def test_a_flag_parameter_is_written_with_flag(tmp_path):
    text = DECISIONS.replace("  operation index()", "  operation withdraw(design-decision, discard (flag))\n"
                                                    "  operation index()")
    op = _area(tmp_path, text).services["decisions"].operation("withdraw")
    assert [(p.name, p.type) for p in op.parameters] == [("design-decision", "object"), ("discard", "flag")]


def test_an_operation_names_the_actors_that_may_request_it_with_by(tmp_path):
    text = DECISIONS.replace("  operation index()", "  operation withdraw(design-decision) by the person, a session"
                                                    "  outcomes: done\n  operation index()")
    op = _area(tmp_path, text).services["decisions"].operation("withdraw")
    assert op.by == ("the person", "a session") and [o.kind for o in op.outcomes] == ["done"]
    assert _area(tmp_path / "2").services["decisions"].operation("index").by == ()


def test_an_object_kind_of_another_and_values_written_in_order(tmp_path):
    (tmp_path / "spec" / "model").mkdir(parents=True)
    (tmp_path / "spec" / "model" / "a.md").write_text("---\narea: a\n---\n\n```model\nobject session kind of agent\n"
                                                     "  attributes: rank: low < high; colour: red | blue\n```\n")
    obj = domain_model.load(tmp_path).objects["session"]
    assert obj.kind_of == "agent"
    assert [(a.name, a.values, a.ordered) for a in obj.attributes] == [("rank", ("low", "high"), True),
                                                                        ("colour", ("red", "blue"), False)]


def test_elements_resolve_by_their_qualified_id(tmp_path):
    model = _area(tmp_path)
    assert model.resolve("object design-decision").kind == "object"
    assert model.resolve("attribute design-decision.tier").kind == "attribute"
    assert model.resolve("value design-decision.status accepted").id == "design-decision.status accepted"
    assert model.resolve("relation design-decision.enforced by").kind == "relation"
    assert model.resolve("service decisions").kind == "service"
    assert model.resolve("operation decisions.enter").kind == "operation"
    assert model.resolve("actor the person").kind == "actor"
    assert model.resolve("event a design-decision is entered").kind == "event"
    for missing in ("object decision", "value design-decision.status proposed", "operation decisions.leave",
                    "relation design-decision.cites", "frobnicate x"):
        assert model.resolve(missing) is None, missing


@pytest.mark.parametrize("bad, line", [
    ("object x\n  colours: red\n", 2),
    ("object x\n  attributes: tier: \n", 2),
    ("object x\n  relations: cites design-decision (many)\n", 2),
    ("object x\n  relations: cites → design-decision (some)\n", 2),
    ("object x\n  lifecycle status: a → b; c\n", 2),
    ("service s\n  operation o(\n", 2),
    ("service s\n  operation o()\n    outcomes: finished\n", 3),
    ("event e: raised by nothing\n", 1),
    ("thing x\n", 1),
])
def test_a_line_that_does_not_read_is_refused_naming_file_and_line(tmp_path, bad, line):
    text = "---\narea: a\nkind: core\n---\n\n```model\n" + bad + "```\n"
    with pytest.raises(Refused) as found:
        _area(tmp_path, text, "a")
    assert "spec/model/a.md:%d" % (line + 6) in str(found.value)


def test_no_model_directory_is_an_empty_model(tmp_path):
    model = domain_model.load(tmp_path)
    assert not domain_model.exists(tmp_path)
    assert (model.areas, model.objects, model.services) == ({}, {}, {})


def test_the_model_is_read_once_per_state_of_its_files(tmp_path):
    first = _area(tmp_path)
    assert domain_model.load(tmp_path) is first
    _area(tmp_path, DECISIONS.replace("actor session", "actor agent2"))
    assert "agent2" in domain_model.load(tmp_path).actors


def test_the_fixture_reads():
    model = domain_model.load(FIXTURE)
    assert set(model.areas) == {"notes"}
    assert model.services["notes"].operation("add").object == "note"
