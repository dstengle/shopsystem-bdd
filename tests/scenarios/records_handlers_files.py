"""Records' design, plan and observation (r7, r4, r8, r9, b475), `local`s in records' own groups: a design a Given
brings in written as `.shop/records/2026-01-01-<name>/design.md` and committed before a plan is filed into it (unless a
Given says it does not exist; the design the When files is written by `work record --design`), the commands
`work record --design`, `work record --plan` and `work observe` run with a title, a summary and a body kept outside
the repository, and the Thens of the design's folder, the plan in it and the observation `work` wrote."""
import importlib.util
import re
import sys
from pathlib import Path

from vocab import handler


def shared(name, file):
    """A module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
H = shared("shop_design_model_check_handlers", "design_model_check_handlers.py")
local = W.local
RECORDS = ".shop/records"
DESIGN = re.compile(r"\.shop/records/(\d{4}-\d\d-\d\d-[a-z0-9-]+)/design\.md")
PLAN = re.compile(r"\.shop/records/(\d{4}-\d\d-\d\d-[a-z0-9-]+)/plan-(\d+)\.md")
TEXT = "What a session saw, in one paragraph."


def mine(step):
    """True for a step of features/records.feature's own groups."""
    return sys.modules["vocab"].origin(step.request.node) == "records"


def files(step):
    """{name: rel} of the designs and plans the scenario's Thens bound to what `work` wrote, or the Givens wrote."""
    return step.context.setdefault("record_files", {})


@local("GivenK", "design")
@local("GivenK", "plan")
@local("GivenK", "observation")
def given_file(step):
    """`a design d1`, `a plan p1`, `an observation o1`: nothing written until the When, which knows what it files."""
    if not mine(step):
        return False
    step.context.setdefault("record_given", {})[step.names[0]] = step.kind


@local("GivenDoesNot")
def given_absent(step):
    """`the design d1 does not exist`: its folder is not written before the plan is filed into it."""
    if not mine(step) or step.term != "exist":
        return False
    step.context.setdefault("record_absent", set()).add(step.names[0])


def body(step):
    path = step.fixtures("tmp_path_factory").mktemp("body") / "body.md"
    path.write_text("What it says.\n")
    return str(path)


def ready(step):
    H.built(step)
    H.base(step.repo, step.context)


@handler("WhenRuns", "`work record --design`")
def file_design(step):
    """`work record --design` with a title, the index row's text and a body."""
    ready(step)
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("work", "record", "A design", "--design", "--summary", "a design, in one row",
                                      "--body", body(step))


@handler("WhenRuns", "`work record --plan`")
def file_plan(step):
    """`work record --plan --design <folder>`: the design a Given brought in written and committed first, unless a
    Given said it does not exist; its folder's name is what a refusal names it by."""
    ready(step)
    name = next(n for n, kind in step.context.get("record_given", {}).items() if kind == "design")
    folder = "2026-01-01-%s" % name
    if name not in step.context.get("record_absent", ()):
        H.write(step.repo, "%s/%s/design.md" % (RECORDS, folder), "# The design %s\n\nHow it is built.\n" % name)
        files(step)[name] = "%s/%s/design.md" % (RECORDS, folder)
    H.says(step, name, folder)
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("work", "record", "A plan", "--plan", "--design", folder, "--body", body(step))


@handler("WhenRuns", "`work observe`")
def observe(step):
    """`work observe` with the observation's text."""
    ready(step)
    step.context["head"] = W.init(step.repo)
    step.context["result"] = step.run("work", "observe", TEXT)


def changed(step):
    runs = W.runs(step)
    assert runs, "no command ran: %s" % step.text
    assert step.context["result"].returncode == 0, (step.context["result"].stdout, step.context["result"].stderr)
    return runs[-1]["changed"]


def kept_design(step, name, rels):
    """The design's folder holds `design.md` and the run changed a file in it; a design the When filed bound to the
    folder `work` wrote, its `design.md` of kind design."""
    rel = files(step).get(name) or next((r for r in rels if DESIGN.fullmatch(r)), None)
    assert rel, ("no design written", rels)
    files(step)[name] = rel
    folder = rel.rpartition("/")[0] + "/"
    assert (step.repo / rel).is_file() and any(r.startswith(folder) for r in rels), (rel, rels)
    assert W.git(step.repo, "status", "--porcelain").strip() == "", "left uncommitted"
    if rel in rels:
        assert "\nkind: design\n" in (step.repo / rel).read_text() and "%s/README.md" % RECORDS in rels, rels


@local("ThenDoes")
def writes(step):
    """`work writes the design d1`, `... the plan p1`, `... the observation o1` (the records service keeps it)."""
    found = W.named((step.nps or [""])[-1]) or re.fullmatch(r"the (design|plan|observation) (\S+)", (step.nps or [""])[-1] or "")
    if not mine(step) or step.term != "write" or not found:
        return False
    kind, name = found.groups() if hasattr(found, "groups") else found
    rels = changed(step)
    if kind == "design":
        return kept_design(step, name, rels)
    if kind == "plan":
        rel = next((r for r in rels if PLAN.fullmatch(r)), None)
        assert rel and (step.repo / rel).read_text().startswith("# A plan\n"), ("no plan written", rels)
        files(step)[name] = rel
        return None
    text = (step.repo / RECORDS / "observations.md").read_text()
    assert "%s/observations.md" % RECORDS in rels, rels
    assert re.search(r"^## observation/\S+\nabout: \S+\nby: .+\ndate: \d{4}-\d\d-\d\d\n\n%s$" % re.escape(TEXT), text,
                     re.MULTILINE), text


@local("ThenDoes")
def holds(step):
    """`the design d1 holds the plan p1`: the plan `work` wrote is in the design's folder."""
    if not mine(step) or step.term not in ("hold", "holds", "in") or not step.nps or "plan" not in step.nps[-1]:
        return False
    design, plan = files(step).get(step.names[0]), files(step).get(step.names[-1])
    assert design and plan and plan.rpartition("/")[0] == design.rpartition("/")[0], (design, plan)
