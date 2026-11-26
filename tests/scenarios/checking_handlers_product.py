"""Handlers of checking's product check (r114-r123, b643; decisions 0140-0144), each a `work_queue_world.local` that
takes only a step of a scenario of one of its groups (`mine`). The Givens are taken as said; the world each group's
scenario needs is written at the When over the domain-model fixture (tests/scripts/fixtures/domain-model/, the
bounded context `example.org/fixture/domain-model`): the product file `.shop/product/product.toml` (product_store's
`render`) holding the job `keep-notes` (j1), its need `file-notes` (n1), the product actor `the note keeper` (p1)
played here by the person, the subdomain `note-taking` (s1) and another bounded context `example.org/fixture/other`
(b1), as each group's line says; notebook's g1 serving the job when a group serves it here. Of the capabilities'
groups (r120-r122): notebook's g2 serving the job, whose r2 asks the notes service to archive a note, so the job
reaches `shelf` (product_handlers_trace's, on a request to archive a note: c2, r120); checking_handlers_port's driven
port `stock-port` (c2, r121); a guarantees capability `rules` (c2, r122); and, so that `w_unserved_cap` is seen live,
`drawer`, which no job's trace reaches. The When runs `spec check`; the Thens read its exit and the rows under the
rule the group's line is about (`RULES`)."""
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W = sys.modules["shop_work_queue_world"]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
REL = ".shop/product/product.toml"
CONTEXT, OTHER = "example.org/fixture/domain-model", "example.org/fixture/other"
JOB, NEED, ACTOR, SUBDOMAIN = "keep-notes", "file-notes", "the note keeper", "note-taking"
RULES = {"g114": "w_unheld_job", "g115": "w_unserved_job", "g116": "w_untriggered_actor", "g117": "v_need_cycle",
         "g118": "w_unaddressed_sub", "g119": "w_unreached_sub", "g123": "v_job_elsewhere",
         "g120": "w_unserved_cap", "g121": "w_unserved_cap", "g122": "w_unserved_cap"}
SAYS = {"job": JOB, "need": NEED, "product actor": ACTOR, "subdomain": SUBDOMAIN, "bounded context": OTHER}
CAPABILITY = """---
id: capability/example.org/fixture/domain-model/%(name)s
title: %(title)s
narrator: a person keeping notes
group: %(group)s
area: notes
specifies: service notes
language: codified-2
retired: []
unbuilt: []
---

# %(title)s

## Purpose
%(title)s of the notes.

## Behaviour

### [g1] %(title)s
- [r1] %(line)s
"""
LABELS = "When the person labels a note with a tag, the notes service shall keep the tag."
LISTS = "When the person lists the notes, the notes service shall complete the request."


def _module(name):
    return sys.modules["shop_handlers_%s" % hashlib.sha256(str(HERE / name).encode()).hexdigest()[:12]]


def group_of(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "checking":
        return None
    return next((t for t in found.tags if t in RULES), None)


def mine(step):
    return group_of(step) is not None


def given(step):
    """Each Given of the product check's groups: an instance kept by its kind, what it says of it taken as said."""
    if not mine(step):
        return False
    if step.template == "GivenK" and step.names:
        step.context.setdefault("product check", {})[step.names[0]] = step.kind
    step.context.setdefault("product check", {})


def product(group):
    """The product file's product the group's line describes, or None when the group needs none."""
    jobs = {JOB: {"actors": [], "statement": "When notes pile up, %s wants them kept, so they can find them." % ACTOR,
                  "needs": []}}
    out = {"id": "example.org/fixture", "purpose": "Notes kept.", "actors": [ACTOR], "jobs": jobs}
    if group == "g114":
        return out
    if group == "g117":
        jobs[JOB]["needs"] = [NEED]
        jobs[NEED] = {**jobs[JOB], "needs": [JOB]}
        return out
    if group == "g118":
        return {**out, "subdomains": {SUBDOMAIN: {"type": "core", "serves": []}}}
    if group == "g123":
        return {**out, "contexts": {OTHER: {"addresses": [], "jobs": [JOB]}}}
    here = {"addresses": [], "jobs": [JOB]}
    if group == "g116":
        jobs[JOB]["actors"] = [ACTOR]
        here["actors"] = {ACTOR: "the person"}
    if group == "g119":
        out["subdomains"] = {SUBDOMAIN: {"type": "core", "serves": [JOB]}}
    return {**out, "contexts": {CONTEXT: here}} if group in ("g115", "g116", "g119") else None


def capability(spec, name, line, group="service"):
    (spec / "capabilities" / ("%s.md" % name)).write_text(CAPABILITY % {
        "name": name, "title": name.capitalize(), "group": group, "line": line})
    index = spec / "index.md"
    index.write_text(index.read_text().replace("| notes | core | notebook", "| notes | core | notebook, %s" % name, 1))


def build(step, group):
    """The world the group's line needs, written into the repository; the capability c2 stands for (r120-r122)."""
    repo, T = step.repo, _module("product_handlers_trace.py")
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    spec = repo / "spec"
    notebook = spec / "capabilities" / "notebook.md"
    if group in ("g119", "g121", "g122", "g123"):
        T.serve(notebook, "g1", JOB)
    said = None
    if group == "g120":
        T.serve(notebook, "g2", JOB)
        capability(spec, "shelf", T.ARCHIVES)
        said = "shelf"
    elif group == "g121":
        port = _module("checking_handlers_port.py")
        (spec / "model" / "stock.md").write_text(port.MODEL % "port")
        (spec / "vocabulary" / "stock.md").write_text(port.VOCABULARY)
        (spec / "capabilities" / "stock-port.md").write_text(port.PORT % "Relied on by: notebook#r10.\n")
        notes = spec / "model" / "notes.md"
        notes.write_text(notes.read_text().replace("imports: []\n", "imports: [stock]\n"))
        notebook.write_text(notebook.read_text() + port.CORE)
        index = spec / "index.md"
        index.write_text(index.read_text().replace("| notes | core | notebook |\n",
                                                   "| notes | core | notebook |\n| stock | port | stock-port |\n"))
        said = "stock-port"
    elif group == "g122":
        capability(spec, "rules", LISTS, "guarantees")
        said = "rules"
    if said:
        capability(spec, "drawer", LABELS)
    held = product(group)
    if held is not None:
        (repo / REL).parent.mkdir(parents=True, exist_ok=True)
        (repo / REL).write_text(T.P.scripts("product_store").render(held))
    for args in (("features", "generate"), ("spec", "annotate")):
        done = step.run(*args)
        assert done.returncode == 0, done.stdout + done.stderr
    return said


def runs(step):
    group = group_of(step)
    if group is None or step.term != "`spec check`":
        return False
    step.context["product said"] = build(step, group)
    step.context["result"] = step.run("spec", "check")


def rows(out, code):
    """The rows `spec check` printed under the rule `code`: its heading, then each row it names, indented."""
    found, inside = [], False
    for line in out.splitlines():
        if not line.startswith(" "):
            inside = line.removeprefix("warning ").split("  ")[0] == code
        elif inside:
            found.append(line.strip())
    return found


def ran(step):
    return mine(step) and "product said" in step.context


def then_completes(step):
    """`the specification service completes this request`: no violation, no file problem."""
    if not ran(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_fails(step):
    """`the specification service fails this check`."""
    if not ran(step):
        return False
    done = step.context["result"]
    assert done.returncode == 1 and "Traceback" not in done.stderr, done.stdout + done.stderr


def then_names(step):
    """`the specification service names the job j1` (the need, the product actor, the subdomain): a row of the rule the
    group's line is about names what the instance stands for."""
    if not ran(step) or step.term != "name":
        return False
    done = step.context["result"]
    said = SAYS[step.context["product check"][step.names[-1]]]
    assert any(said in row for row in rows(done.stdout, RULES[group_of(step)])), done.stdout + done.stderr


def then_not_returned(step):
    """`the specification service does not return the capability c2`: no row of `w_unserved_cap` names the
    capability c2 stands for, while one names drawer, which contributes to no job."""
    if not ran(step):
        return False
    unserved = rows(step.context["result"].stdout, "w_unserved_cap")
    assert any(row.endswith("/drawer") for row in unserved), step.context["result"].stdout
    assert not any(row.endswith("/%s" % step.context["product said"]) for row in unserved), unserved


for template in ("GivenK", "GivenDoes", "GivenDoesNot", "GivenK_A", "GivenCode"):
    W.local(template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_completes)
W.local("ThenExitsErr")(then_fails)
W.local("ThenDoes")(then_names)
W.local("ThenPrintsNot")(then_not_returned)
