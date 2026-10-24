"""batch-measurement's steps about the request an initiative fulfils: the Givens that write its link and the request,
and the Thens that read the origin from the measurement."""
from pytest_bdd import given, parsers, then

from .batch_measurement_world import INITIATIVE

ASKERS = {"this bounded context": "internal", "another bounded context": "bounded-context/ex.com/prod/other"}


@given(parsers.parse("i7-cart fulfils the request {request}, whose asker is {asker}"))
def fulfils(world, request, asker):
    world.request = (request, ASKERS[asker])


@given("i7-cart fulfils no request")
def fulfils_none(world):
    world.request = None


@then(parsers.parse("the measurement gives the stage of {item}'s {stage}"))
def gives_the_stage_of(world, item, stage):
    found = [s for s in world.figures()["stages"] if s["work-item"] == item and s["stage"] == stage]
    assert found, world.figures()["stages"]


@then(parsers.parse("the measurement gives the request {request} as {origin}"))
def gives_request(world, request, origin):
    assert world.code == 0, world.err
    assert world.figures()["request"] == {"id": request, "origin": origin}, world.figures()


@then("the measurement gives no request as internal or external")
def gives_no_request(world):
    assert "request" not in world.figures(), world.figures()
    assert INITIATIVE in world.record().name
