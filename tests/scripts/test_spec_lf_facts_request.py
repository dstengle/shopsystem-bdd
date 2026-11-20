"""spec_lf_facts_request, and spec_lf_ids in a context with a domain model (the domain contract design, §5.2, §5.3): a
request's trigger with its parameter set as one key, `param` and `noparam`, the request pack's verbs as outcomes, a
refusal with what it names, every id a model element qualified by its area, and two areas' one word never one id."""
import pathlib
import shutil

import pytest
import spec_context
import toolchain

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "domain-model"


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def facts(root, ident):
    ctx = spec_context.load(root)
    assert ident in ctx.facts, ctx.refused
    return [f.split("(", 1)[0] + "(" + f.split(",", 1)[1] for f in ctx.facts[ident] if "," in f]


def test_a_request_with_parameters_given_and_absent():
    got = facts(FIXTURE, "notebook#r3")
    # a value of an attribute's parameter is `val` in the key and a named term in the object (b418)
    assert "trig(req,req(e_notes__add,(p(priority,val),p(text,some))),a_notes__the_person,pair(x2,pv_priority))." \
        in got
    assert 'named(pv_priority,"`high`").' in got and "role(pv_priority,k_priority)." in got
    assert 'param(1,priority,"high").' in got and "param(1,text,some)." in got
    got = facts(FIXTURE, "notebook#r4")
    assert "trig(req,req(e_notes__add,(p(reminder,no),p(text,no))),a_notes__the_person,x2)." in got
    assert "noparam(1,reminder)." in got and "noparam(1,text)." in got


def test_a_thing_a_parameter_names_is_part_of_the_trigger_object():
    got = facts(FIXTURE, "notebook#r5")
    assert "trig(req,req(e_notes__label,(p(tag,thing),)),a_notes__the_person,pair(x2,x3))." in got
    assert "param(1,tag,x3)." in got


def test_a_refusal_with_what_it_names_and_the_pack_verbs_as_outcomes():
    got = facts(FIXTURE, "notebook#r4")
    assert "resp(1,pos,refused,a_notes__notes,x4)." in got
    assert "resp(2,pos,named,a_notes__notes,x5)." in got and "names(2,x5)." in got
    assert 'named(x5,"text").' in got and "role(x5,k_parameter)." in got
    assert "resp(1,pos,done,a_notes__notes,x3)." in facts(FIXTURE, "notebook#r6")
    assert "resp(1,pos,kept,a_notes__notes,x2)." in facts(FIXTURE, "notebook#r3")


def test_ids_are_model_elements_qualified_by_their_area():
    ctx = spec_context.load(FIXTURE)
    assert "kind(k_notes__note)." in ctx.domain and "kind(k_note)." not in ctx.domain
    assert "val(k_notes__note,t_notes__note__status,v_notes__note__status__draft)." in ctx.domain
    assert "actor(a_notes__the_person)." in ctx.domain
    assert any("crel(" in f and "e_notes__note__carries" in f for f in ctx.facts["notebook#r2"])


def two_areas(tmp_path):
    """The fixture with a second area, shelves, whose own `note` names another object (a shelf note)."""
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    (root / "spec" / "model" / "shelves.md").write_text(
        "---\nid: model/x/shelves\narea: shelves\nkind: core\nimports: []\n---\n\n# Shelves\n\n```model\n"
        "object shelf note\n  attributes: text (text)\n\nservice shelves\n  operation pin(shelf note)  outcomes: done\n"
        "```\n")
    (root / "spec" / "vocabulary" / "shelves.md").write_text(
        "---\nid: vocabulary/x/shelves\narea: shelves\n---\n\n# Shelves\n\n## Terms\n\n"
        "- **note** (noun) → object shelf note. A note pinned to a shelf.\n"
        "- **pin** (verb, action) → operation shelves.pin. Forms: pins, pinned. Frame: <actor> pins <shelf note>.\n"
        "- **the shelves service** (proper noun) → service shelves.\n")
    return root


def test_two_areas_one_word_never_one_id(tmp_path):
    ctx = spec_context.load(two_areas(tmp_path))
    kinds = sorted(f for f in ctx.domain if f.startswith("kind(k_") and "__" in f)
    assert kinds == ["kind(k_notes__note).", "kind(k_notes__tag).", "kind(k_shelves__shelf_note)."]
