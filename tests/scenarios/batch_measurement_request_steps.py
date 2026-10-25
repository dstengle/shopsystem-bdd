"""batch-measurement's steps about the request an initiative fulfils: the Givens that write its link and the request,
and the Thens that read the origin from the measurement."""
from pytest_bdd import given, parsers, then

from .batch_measurement_world import INITIATIVE

ASKERS = {"this bounded context": "internal", "another bounded context": "bounded-context/ex.com/prod/other"}


@given(parsers.parse("i7-cart fulfils the request {request}, whose asker is {asker}"))
def fulfils(world, request, asker):
    world.requests = [[request, True, ASKERS[asker]]]


@given("i7-cart fulfils no request")
def fulfils_none(world):
    world.requests = []


@given(parsers.re(r"i7-cart fulfils the request (?P<request>\w+)(, which the queue holds)?"))
def fulfils_held(world, request):
    world.requests.append([request, True, "internal"])


@given(parsers.parse("i7-cart fulfils the requests {first} and {second}, which the queue holds, each with an asker"))
def fulfils_two(world, first, second):
    world.requests = [[first, True, "internal"], [second, True, "internal"]]


@given(parsers.parse("the queue does not hold the request {request}"))
def queue_lacks(world, request):
    for entry in world.requests:
        if entry[0] == request:
            entry[1] = False


@given(parsers.parse("the request {request} has no asker"))
def request_no_asker(world, request):
    for entry in world.requests:
        if entry[0] == request:
            entry[2] = ""


@then("measure initiative refuses because the queue does not hold that request")
def refuses_not_held(world):
    assert world.code != 0 and "does not hold" in world.err, world.err


@then("measure initiative refuses because the request has no asker")
def refuses_no_asker(world):
    assert world.code != 0 and "has no asker" in world.err, world.err


@then("measure initiative refuses because the initiative fulfils more than one request")
def refuses_several(world):
    assert world.code != 0 and "more than one request" in world.err, world.err


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
