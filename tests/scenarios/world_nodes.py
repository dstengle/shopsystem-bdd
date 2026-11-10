"""Shared handlers for the domain kinds (design §14.3): a Given writes the node, the spec file or the record its
step names into the scenario's repository, in the files today's world helpers write (conftest's World, requests'
write_request); a Then reads a node's status back. Frozen after layer 2: a capability adds its own handlers in
`<capability>_handlers*.py`, and a change here goes through the orchestrator."""
import re
import textwrap

from vocab import handler

PATH = "ex.com/prod/ctx"
NODE_KINDS = ("request",)     # the frozen queue's kinds are written only as citations (work_queue_world.cite)


def full(kind, name):
    return "%s/%s/%s" % (kind, PATH, name)


def bare(word):
    return word.strip("`")


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def index(repo):
    """spec/index.md, written once: the context's id and a Glossary a term step adds to."""
    path = repo / "spec" / "index.md"
    if not path.is_file():
        write(repo, "spec/index.md", "---\nid: bounded-context/%s\n---\n# ctx\n\n## Glossary\n\n" % PATH)
    return path


def initiative_of(context):
    return context.get("initiative", "i1")


def node_path(context, kind, name):
    """Where a node of a kind is kept: an initiative's directory, its parts beside it, requests apart."""
    if kind == "initiative":
        return ".shop/work/%s/initiative.md" % name
    if kind == "request":
        return ".shop/requests/%s.md" % name
    return ".shop/work/%s/%s.md" % (context.get("part_of", {}).get(name, initiative_of(context)), name)


def node_text(kind, name, status, initiative):
    if kind == "initiative":
        return textwrap.dedent("""\
            ---
            id: %s
            title: t
            summary: s
            kind: capability-change
            owner-level: ctx
            status: %s
            priority: 1
            source: [observation/obs-1]
            date: 2026-10-15
            ---
            """ % (full("initiative", name), status))
    if kind == "request":
        return ("---\nid: %s\nkind: request\nasker: other\nstatus: %s\nturn: upstream\n---\n\n# %s\n\n## Lines\n"
                "1. line 1\n\n## Outcomes\n\n## Resolution\n" % (full("request", name), status, name))
    fields = {"work-item": "under: thing\ncheck: true\n", "capability-proposal":
              "argues: [thing]\nadds: []\nchanges: []\nremoves: []\ndate: 2026-10-15\n"}.get(kind, "")
    return "---\nid: %s\nkind: %s\npart_of: initiative/%s\nstatus: %s\n%s---\n" % (
        full(kind, name), kind, initiative, status, fields)


def write_node(step, kind, name, status):
    index(step.repo)
    rel = node_path(step.context, kind, name)
    step.context.setdefault("nodes", {})[name] = (kind, rel)
    return write(step.repo, rel, node_text(kind, name, bare(status), initiative_of(step.context)))


def frontmatter_field(text, name):
    found = re.search(r"^%s: (.*)$" % re.escape(name), text, re.MULTILINE)
    return found.group(1).strip() if found else None


for _kind in NODE_KINDS:
    @handler("GivenK_A", _kind)
    def given_node(step):
        """`a K x that is v` writes the node; `the K x is v` after it sets the status and keeps what other Givens
        wrote into it (its relations)."""
        known = step.context.get("nodes", {}).get(step.names[0])
        path = step.repo / known[1] if known else None
        if path and path.is_file():
            path.write_text(re.sub(r"^status: .*$", "status: %s" % bare(step.values[0]), path.read_text(), count=1,
                                   flags=re.MULTILINE))
            return
        write_node(step, step.kind, step.names[0], step.values[0])

    @handler("GivenK", _kind)
    def given_bare_node(step):
        write_node(step, step.kind, step.names[0], {"initiative": "started", "request": "open"}.get(
            step.kind, "drafted"))

    @handler("ThenK_A", _kind)
    def node_is(step):
        _, rel = step.context["nodes"][step.names[0]]
        status = frontmatter_field((step.repo / rel).read_text(), "status")
        wanted = bare(step.values[0])
        assert (status != wanted) if " is not " in step.text else (status == wanted), (step.text, status)


@handler("GivenK", "capability")
def given_capability(step):
    index(step.repo)
    name = bare(step.names[0])
    write(step.repo, "spec/capabilities/%s.md" % name, textwrap.dedent("""\
        ---
        id: capability/%s/%s
        title: %s
        narrator: a client
        group: service
        language: codified-2
        rests_on: []
        retired: []
        ---

        # %s

        ## Purpose
        Something.

        ## Behaviour

        ## Not yet
        ## Dropped
        """ % (PATH, name, name, name)))


@handler("GivenK", "term")
def given_term(step):
    path = index(step.repo)
    path.write_text(path.read_text() + "- **%s** (noun): a thing.\n" % bare(step.names[0]))


@handler("GivenK", "design-decision")
def given_decision(step):
    name = bare(step.names[0])
    write(step.repo, "spec/decisions/%s.md" % name, "---\nid: design-decision/%s/%s\nstatus: accepted\n---\n# %s\n"
          % (PATH, name, name))
