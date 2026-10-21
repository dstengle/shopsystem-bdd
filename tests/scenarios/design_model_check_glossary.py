"""design-model-check's glossary, read (r48, r49) and checked (r52-r54)."""

from pytest_bdd import given, parsers, then

from .conftest import CONTEXT, INDEX, I1, THING, cap, feature, full
from .design_model_check_then import found


# === the glossary (r48, r49) ======================================================================================

def _glossary(world, *bullets):
    """spec/index.md with a ## Glossary section with these bullets."""
    world.write("spec/index.md", INDEX + "\n## Glossary\n\n" + "\n".join(bullets) + "\n\n## Where things live\n\n- Here.\n")


def _term(name):
    return full("term", name)


@given(parsers.parse("a bounded context whose glossary has the bullet {bullet}"))
def glossary_with_bullet(world, context, bullet):
    if bullet.startswith('"') and bullet.endswith('"'):  # r48 quotes its bullet; r49's examples do not
        _glossary(world, bullet[1:-1])
    else:
        _glossary(world, "- **slice**: a unit of work.", bullet)


@given("a bounded context whose glossary defines batch, avoiding sprint and lot, and slice, avoiding nothing")
def glossary_batch_and_slice(world):
    _glossary(world, "- **batch**: the slices one session plans. Not: sprint, lot.",
              "- **slice**: a unit of work with an observable done.")


def _fact_lines(context):
    result = context["result"]
    assert result.returncode == 0, result.stderr
    return result.stdout.splitlines()


@then("it prints the term term/ex.com/prod/ctx/suite-record")
def prints_term(context):
    assert 'node("%s", "term").' % _term("suite-record") in _fact_lines(context)


@then('its avoided words are "test record" and "run", and nothing else')
def avoided_words(context):
    lines = _fact_lines(context)
    assert 'avoid("%s", "test record").' % _term("suite-record") in lines
    assert 'avoid("%s", "run").' % _term("suite-record") in lines
    assert [l for l in lines if l.startswith("avoid(")] == [
        'avoid("%s", "test record").' % _term("suite-record"), 'avoid("%s", "run").' % _term("suite-record")]


@then("it prints one file problem naming spec/index.md")
def one_file_problem_in_index(world, context):
    data = found(world, context)
    assert len(data["problems"]) == 1, data
    assert data["problems"][0].startswith("spec/index.md"), data


@then("each term has a node fact of kind term and a term_of fact naming the bounded context")
def terms_have_kind_and_context(context):
    lines = _fact_lines(context)
    for t in ("batch", "slice"):
        assert 'node("%s", "term").' % _term(t) in lines
        assert 'term_of("%s", "%s").' % (_term(t), CONTEXT) in lines


@then("batch has an avoid fact for sprint and one for lot")
def batch_avoids(context):
    lines = _fact_lines(context)
    assert 'avoid("%s", "sprint").' % _term("batch") in lines
    assert 'avoid("%s", "lot").' % _term("batch") in lines


@then("slice has no avoid fact")
def slice_avoids_nothing(context):
    assert not [l for l in _fact_lines(context) if l.startswith('avoid("%s"' % _term("slice"))]


# === the glossary checked (r52-r54) ================================================================================

@given("a glossary term slice that avoids chunk")
def glossary_slice_avoids_chunk(world):
    _glossary(world, "- **slice**: a unit of work. Not: chunk.")


@given('a requirement that says "chunk", a scenario titled "chunks are planned" and a deprecated scenario titled "a chunk as it was"')
def chunk_everywhere(world):
    world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it plans each chunk.", "- [r2] It plans a slice."]))
    world.write("features/thing.feature", feature("thing", ("@r1", "it plans"), ("@r2", "chunks are planned"),
                                                  ("@r2 @deprecated", "a chunk as it was")))


def _v_t1(world, context):
    return [a for name, a in found(world, context)["violations"] if name == "v_t1"]


@then("v_t1 names the requirement, chunk and the term slice")
def v_t1_names_requirement(world, context):
    assert [THING + "#r1", "chunk", _term("slice")] in _v_t1(world, context), found(world, context)


@then("v_t1 names the scenario, chunk and the term slice")
def v_t1_names_scenario(world, context):
    assert ["features/thing.feature:chunks are planned", "chunk", _term("slice")] in _v_t1(world, context), found(world, context)


@then("v_t1 does not name the deprecated scenario")
def v_t1_not_deprecated(world, context):
    assert not [a for a in _v_t1(world, context) if "as it was" in a[0]], found(world, context)


@given("a glossary with an entry for slice and another for Slice")
def glossary_slice_twice(world):
    _glossary(world, "- **slice**: a unit of work.", "- **Slice**: a piece of a batch.")


@then("v_t2 names term/ex.com/prod/ctx/slice")
def v_t2_names_slice(world, context):
    assert [a for name, a in found(world, context)["violations"] if name == "v_t2"] == [[_term("slice")]], found(world, context)


@given("a glossary where slice avoids batch, batch is a term, and hand-back avoids Hand-back")
def glossary_avoiding_terms(world):
    _glossary(world, "- **slice**: a unit of work. Not: batch.", "- **batch**: the slices one session plans.",
              "- **hand-back**: an implementer's stop. Not: Hand-back, halt.")


@then("v_t3 names batch and hand-back")
def v_t3_names(world, context):
    rows = [a for name, a in found(world, context)["violations"] if name == "v_t3"]
    assert sorted(rows) == [["batch"], ["hand-back"]], found(world, context)


# === an abandoned initiative (r59) ===============================================================================

@given("an abandoned capability-change initiative")
def abandoned_initiative(world):
    world.good()
    world.observation()
    world.initiative(status="abandoned")


@then("v_d2 names the initiative")
def v_d2_names_initiative(world, context):
    assert [a for name, a in found(world, context)["violations"] if name == "v_d2"] == [[I1]], found(world, context)


@then("once the work-item is withdrawn too, no violation names the initiative")
def withdrawn_too(world):
    world.work_item(status="withdrawn", part_of="capability-proposal/p1")
    data, _ = world.check_json()
    assert [v for v in data["violations"] if I1 in v[1]] == [], data
