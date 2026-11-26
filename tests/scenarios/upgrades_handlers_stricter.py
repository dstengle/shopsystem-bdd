"""upgrades' upgrade to 0.45.0 (r47, b851), each handler a `local` of work_queue_world's table taken before
migration-tools' own, of upgrades' g47 alone (`mine`): the given block's index file, with its old `### Areas`
Composition, beside a domain model written at the When (`WORLD`: the domain-model fixture's notes area and its words,
and the area `desk`, whose words and lines are the scenario's things), so the upgrade runs from the release the
scenario gives through the 0.38.0 step, which leaves a context with `spec/model/` alone. Each term and transition the
Givens bring in is one of desk's, in their order of each rule and polarity (`THINGS`): a Frame: with no slot in angle
brackets and one whose slot names nothing (v_t13), against `publish`'s; an adjective naming an actor and one naming
an object (v_t22), against `the desk service`; the transitions `draft → active` and `active → retired` of the note's
status that desk's lines set on its own operation's request (v_m9), against `draft → retired`, which notes' own
`archive` sets. The Thens read the report line `migrate upgrade` printed of each (`code` and the thing, `said`) and the
index file of its one commit, its Composition in the index form."""
import re
import sys
from pathlib import Path

from scenarios import migration_tools_handlers as M

local = M.local
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
THINGS = {("v_t13", True): ["stamp", "seal"], ("v_t13", False): ["publish"],
          ("v_t22", True): ["personal", "noted"], ("v_t22", False): ["the desk service"],
          ("v_m9", True): ["draft → active", "active → retired"], ("v_m9", False): ["draft → retired"]}

MODEL = """---
id: model/example.org/acme/desk
area: desk
kind: core
imports: [notes]
---

# Desk

## Purpose

The desk a person publishes notes from.

```model
service desk
  operation publish(note)  outcomes: done
  operation stamp(note)  outcomes: done
  operation seal(note)  outcomes: done
```
"""

VOCABULARY = """---
id: vocabulary/example.org/acme/desk
area: desk
---

# The words of desk

## Terms

- **publish** (verb, action) → operation desk.publish. Forms: publishes, published. Frame: <actor> publishes <note>.
- **stamp** (verb, action) → operation desk.stamp. Forms: stamps, stamped. Frame: actor stamps note.
- **seal** (verb, action) → operation desk.seal. Forms: seals, sealed. Frame: <actor> seals <note> with <wax>.
- **personal** (adjective) → actor the person.
- **noted** (adjective) → object note.
- **the desk service** (proper noun) → service desk.
"""

CAPABILITY = """---
id: capability/example.org/acme/shop/%s
title: %s
narrator: a person keeping notes
group: service
area: %s
specifies: service %s
language: codified-2
retired: []
unbuilt: []
---

# %s

## Purpose
A person keeps notes and publishes them from the desk.

## Behaviour

%s"""
DESK = """### [g1] A draft note published becomes active
- [r1] While a note is `draft`, when the person publishes the note, the desk service shall set the status of the note
  to `active`.

### [g2] An active note published is retired
- [r2] While a note is `active`, when the person publishes the note, the desk service shall set the status of the note
  to `retired`.
"""
NOTEBOOK = """### [g1] A note archived is retired
- [r1] When the person archives a note, the notes service shall set the status of the note to `retired`.
"""


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (found is not None and Path(found.feature.filename).stem == "upgrades" and "g47" in found.tags
            and M.migration(step))


def world(step):
    return step.context.setdefault("stricter", {})


@local("GivenK")
def given_thing(step):
    """`a term t1`, `a transition t7`: brought in, its rule told by the Given after it."""
    if not mine(step) or step.kind not in ("term", "transition"):
        return False
    return None


def given_rule(step, held):
    if not mine(step) or step.term != "violate":
        return False
    code = re.search(r"`([^`]+)`", step.text).group(1)
    kept = step.context.setdefault("stricter rules", [])     # (code, held) of each Given so far, in order
    world(step)[step.names[0]] = (code, THINGS[(code, held)][kept.count((code, held))])
    kept.append((code, held))
    return None


local("GivenDoes")(lambda step: given_rule(step, True))
local("GivenDoesNot")(lambda step: given_rule(step, False))


@local("WhenRuns")
def written(step):
    """The domain model beside the given block's index file, written before `migrate upgrade` runs (False: it runs)."""
    if not mine(step):
        return False
    held = M.held(step)
    for rel in ("model/notes.md", "vocabulary/notes.md", "vocabulary/shared.md"):
        held["spec/" + rel] = (FIXTURE / rel).read_text()
    held["spec/model/desk.md"], held["spec/vocabulary/desk.md"] = MODEL, VOCABULARY
    for name, area, body in (("desk", "desk", DESK), ("notebook", "notes", NOTEBOOK)):
        title = name.capitalize()
        held["spec/capabilities/%s.md" % name] = CAPABILITY % (name, title, area, area, title, body)
    return False


def said(step, name):
    """The report lines `migrate upgrade` printed of the thing `name`: its rule's code, then the thing."""
    code, thing = world(step)[name]
    said = thing if code != "v_m9" else "note, status, " + thing.replace(" → ", ", ")
    return [line for line in step.context["done"].stdout.splitlines()
            if re.search(r"\b%s %s:" % (code, re.escape(said)), line)]


@local("ThenPrints")
def returned(step):
    if not mine(step) or not step.names or step.names[0] not in world(step):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert said(step, step.names[0]), (world(step)[step.names[0]], step.context["done"].stdout)
    return None


@local("ThenPrintsNot")
def not_returned(step):
    if not mine(step) or not step.names or step.names[0] not in world(step):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert (step.repo / "spec/vocabulary/desk.md").is_file()
    assert not said(step, step.names[0]), (world(step)[step.names[0]], said(step, step.names[0]))
    return None


@local("ThenDoes")
def changed(step):
    """The index file in the upgrade's one commit, its Composition the index form's one table."""
    if not mine(step) or not step.nps or "index file" not in step.nps[0] or step.term == "has":
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    old = step.context["old"]
    assert "spec/index.md" in old.git("show", "--name-only", "--format=", "HEAD").stdout.split()
    index = M.read(step, "spec/index.md")
    section = index.split("## Composition", 1)[1]
    assert "### Areas" not in section and "| area | kind | capabilities |" in section, index
    assert "| desk | core | desk |" in section and "| notes | core | notebook |" in section, index
    return None
