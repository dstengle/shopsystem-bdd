"""design-model-check's reading of requests (r19, r112) and of an initiative's kind (r118): the Givens."""
from pytest_bdd import given, parsers

from .conftest import full


def request_text(name="q1", asker="internal"):
    """A request file in the form requests' Implementation gives `work request`; `asker` None leaves the line out."""
    fm = ["id: %s" % full("request", name), "kind: request"]
    if asker:
        fm.append("asker: %s" % asker)
    fm += ["source: [%s]" % full("observation", "obs-1"), "status: open", "turn: upstream"]
    return "---\n%s\n---\n\n## Lines\n1. Do the thing.\n" % "\n".join(fm)


@given(parsers.parse("a request in {path} with no asker"))
def request_with_no_asker(world, path):
    world.observation()
    world.write(path, request_text(asker=None))


@given(parsers.parse("a request in {path} that `work request` wrote"))
def request_work_request_wrote(world, path):
    world.observation()
    world.write(path, request_text("q2"))


@given(parsers.parse("a repository with an initiative in {path} of kind {kind}"))
def repository_with_initiative_of_kind(world, path, kind):
    assert path == ".shop/work/i1/initiative.md", path
    world.observation()
    world.initiative(kind=kind)
