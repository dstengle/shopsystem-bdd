"""design-model-check's reading of requests (r19, r112), of an initiative's kind (r118) and the request rules
(r113-r117, r119): the Givens."""
import re

from pytest_bdd import given, parsers

from .conftest import CONTEXT, PATH, full


OTHER = "bounded-context/other.com/prod/other"


def request_text(name="q1", asker="internal", links=None, resolution=None, status="open", path=PATH):
    """A request file in the form requests' Implementation gives `work request`; `asker` None leaves the line out.

    `links` are the front matter lines naming where it comes from (default: an observation as its source).
    """
    fm = ["id: %s/%s/%s" % ("request", path, name), "kind: request"]
    if asker:
        fm.append("asker: %s" % asker)
    fm += links or ["source: [%s]" % full("observation", "obs-1")]
    fm += ["status: %s" % status, "turn: upstream"]
    text = "---\n%s\n---\n\n## Lines\n1. Do the thing.\n" % "\n".join(fm)
    if resolution:
        text += "\n## Resolution\n1. %s 1.0\n" % resolution
    return text


def initiative_text(ident="i1", status="started", date="2026-10-15", fulfils=None, source=None, path=PATH):
    fm = ["id: initiative/%s/%s" % (path, ident), "title: t", "summary: s", "kind: capability-change",
          "owner-level: ctx", "status: %s" % status, "priority: 1",
          "source: [%s]" % (source or full("observation", "obs-1")), "date: %s" % date]
    if fulfils:
        fm.append("fulfils: %s" % fulfils)
    return "---\n%s\n---\n" % "\n".join(fm)


def write_initiative(world, ident="i1", **fields):
    world.write(".shop/work/%s/initiative.md" % ident, initiative_text(ident, **fields))


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


# --- the request rules: r113 v16a, r114 v_d1, r119 v_d3, r115 v17, r116 v3, r117 v18 ------------------------------

@given(parsers.re(r"an initiative (?P<ident>i\d) dated (?P<date>[\d-]+) that fulfils no request$"))
def initiative_dated_fulfilling_nothing(world, ident, date):
    world.observation()
    write_initiative(world, ident, date=date)


@given(parsers.re(r"an initiative (?P<ident>i\d) dated (?P<date>[\d-]+) that fulfils the request (?P<q>q\d)$"))
def initiative_dated_fulfilling(world, ident, date, q):
    write_initiative(world, ident, date=date, fulfils=full("request", q))


@given(parsers.re(r"an initiative (?P<ident>i\d) with status (?P<status>[\w-]+)$"))
def initiative_with_status(world, ident, status):
    world.observation()
    write_initiative(world, ident, status=status)


@given(parsers.re(r"an initiative (?P<ident>i\d) with status (?P<status>[\w-]+) that fulfils (?P<q>q\d)$"))
def initiative_with_status_fulfilling(world, ident, status, q):
    write_initiative(world, ident, status=status, fulfils=full("request", q))


@given(parsers.re(r"a request (?P<q>q\d) in (?P<path>\S+) whose asker is (?P<asker>this context|another context), "
                  r"whose (?P<field>source|part_of) names (?P<ident>i\d), with status (?P<status>[\w-]+)$"))
def request_of_an_initiative(world, q, path, asker, field, ident, status):
    who = CONTEXT if asker == "this context" else OTHER
    link = "%s: [%s]" % (field, full("initiative", ident))
    world.write(path, request_text(q, asker=who, links=[link], status=status))


@given(parsers.re(r"a delivered request (?P<q>q\d)$"))
def delivered_request(world, q):
    world.observation()
    world.write(".shop/work/requests/%s.md" % q, request_text(q, status="delivered"))


@given(parsers.re(r"a request (?P<q>q\d) that is part of no job-thread, cites no origin and is raised for no request$"))
def request_with_no_origin(world, q):
    world.write(".shop/work/requests/%s.md" % q, request_text(q, links=["part_of: %s" % full("initiative", "i1")]))


@given(parsers.re(r"a request (?P<q>q\d) that is part of a job-thread$"))
def request_in_a_thread(world, q):
    world.write(".shop/work/requests/%s.md" % q, request_text(q, links=["part_of: %s" % full("job-thread", "save-x")]))


@given(parsers.re(r"a request (?P<q>q\d) raised for the request (?P<ref>\S+)$"))
def request_raised_for(world, q, ref):
    world.write(".shop/work/requests/%s.md" % q, request_text(q, asker=OTHER, links=["raised_for: %s" % ref]))


@given("no request is raised for it")
def no_request_is_raised_for_it():
    """Nothing is written."""


@given(parsers.re(r"a request (?P<q>q\d) of this context is raised for it$"))
def request_of_this_context_raised_for_it(world, q):
    world.write(".shop/work/requests/%s.md" % q,
                request_text(q, asker=OTHER, links=["raised_for: %s" % world.cited]))


@given(parsers.re(r"a request (?P<q>q\d) that cites an observation as its origin$"))
def request_citing_observation(world, q):
    world.observation()
    world.write(".shop/work/requests/%s.md" % q, request_text(q))


@given("a capability thing with requirement r1 and no requirement r9")
def capability_with_r1_only(world):
    world.good()


@given(parsers.re(r"a delivered request (?P<q>q\d) whose resolution names thing#(?P<rid>r\d)$"))
def delivered_request_with_resolution(world, q, rid):
    world.observation()
    world.write(".shop/work/requests/%s.md" % q, request_text(q, status="delivered", resolution="thing#" + rid))


@given(parsers.parse("a repository whose bounded context is {ident}"))
def repository_of_context(world, ident):
    world.write("spec/index.md", "---\nid: %s\n---\n# ctx\n" % ident)
    world.path = ident.split("/", 1)[1]


@given(parsers.re(r"an initiative (?P<ident>i\d) whose source names (?P<ref>\S+)$"))
def initiative_citing(world, ident, ref):
    world.cited = ref
    write_initiative(world, ident, source=ref, path=world.path)


@given(parsers.parse("nothing in the repository has the id {ref}"))
def nothing_has_the_id(world, ref):
    """The Givens before it wrote no file with the id as its own; the id is only named."""
    assert not re.search(r"^id: %s$" % re.escape(ref), "".join(p.read_text() for p in world.root.rglob("*.md")), re.M)
