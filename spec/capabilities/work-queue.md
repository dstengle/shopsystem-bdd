---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, agent or script reading or moving work-items
group: service
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs]
formulated_as: features/work-queue.feature
retired: []
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them and
what can move, moves them through their lifecycle checking each transition's guard, takes claims and rulings, and
logs every move. It is the only writer of a work-item's status. It also writes `work_expectations.py`, the pytest
plugin that expects the scenarios of work-items not yet claimed to fail. `work run`, the supervisor, is the
supervision capability; this one is the queue it runs on. It judges nothing and starts no worker.

## Behaviour
- [r1] `work` reads the work-items of every initiative under `.shop/work/`, each `.shop/work/<initiative>/<name>.md` whose frontmatter `kind` is `work-item`, and the scenarios under `features/`, and needs nothing beyond the standard library.
- [r2] **When** `work add <initiative> <name>` is run with `--part-of`, `--under` and either `--accepts` or `--check`, `work` writes `.shop/work/<initiative>/<name>.md` with the status `drafted`, the fields given, and the sections Observable, Unknown and Risk from `--observable`, `--unknown` and `--risk`, and prints the work-item's id.
- [r3] **If** `work add` names an initiative with no `initiative.md`, a `--part-of` that is not a capability-proposal of that initiative, a `--blocked-by` that is no work-item, a `--risk` other than `contract`, `concurrency`, `data` or `none`, or a requirement in `--accepts` that no scenario names, `work` refuses, naming it, and writes nothing.
- [r4] **If** the work-item's file already exists, `work add` refuses and leaves it as it was.
- [r5] **When** `work show` is run, `work` prints each work-item, one a line, with its status, its capability, what it waits on and the number of paths in its file set, grouped by initiative; `--status <status>` keeps only those with that status.
- [r6] **When** `work next` is run, `work` prints each move that can be made now, as the work-item, its status before and after and the worker that would make it, and changes nothing.
- [r7] **When** `work` moves a work-item, it writes the new status into the work-item's file and appends one line to `.shop/work/<initiative>/log.jsonl` giving the time, the work-item, the status before and after, who moved it (a worker's session id, `person` or `work`) and why.
- [r8] **If** a work-item's status in its file is not the last status `log.jsonl` gives it, `work` refuses to move it and names the file and both statuses.
- [r9] `work` moves a work-item from `planned` to `ready` only when every work-item it is `blocked_by` is `green` and no `claimed` work-item's file set has a path in its file set.
- [r10] **While** two `ready` work-items' file sets share a path, `work` lets at most one of them be claimed.
- [r11] **When** `work claim <work-item> <path>...` is run on a `claimed` work-item, `work` adds each path to its file set and prints them. **If** another `claimed` work-item's file set has one of the paths, `work` refuses, naming that work-item and the path, and adds none.
- [r12] **If** `work claim` names a work-item that is not `claimed`, `work` refuses and changes nothing.
- [r13] **When** `work questions` is run, `work` prints each `awaiting-ruling` work-item with each open question, numbered, its readings, and the `work rule` command that answers it.
- [r14] **When** `work rule <work-item> <n> "<answer>"` is run on an `awaiting-ruling` work-item, `work` writes the answer, its date and the question it answers under the work-item's `## Rulings`, and moves the work-item to `planned` once every open question has an answer.
- [r15] **If** `work rule` names a work-item that is not `awaiting-ruling`, or a question it does not have, `work` refuses and changes nothing.
- [r16] **When** `work withdraw <work-item> "<why>"` is run, `work` moves the work-item to `withdrawn` with the reason. **If** the work-item is `claimed` or `green`, `work` refuses.
- [r17] **When** `work log <work-item>` is run, `work` prints the work-item's lines of `log.jsonl` in order.
- [r18] **If** `work` refuses a command, it says why on stderr and exits 1; a command given wrongly exits 2.
- [r19] **When** `work plugin <directory>` is run, `work` writes `work_expectations.py` into the directory, over any there, and prints the line that registers it in the `conftest.py` beside it, importing it relative to the package where the directory has an `__init__.py`. **If** the path is not a directory, `work` refuses and writes nothing.
- [r20] A scenario is accepted by a work-item when it is in the feature file of the work-item's capability and its `@r<n>` tag is a requirement the work-item `accepts`.
- [r21] **Where** `work_expectations.py` is registered, a scenario that some work-item accepts, while none of the work-items that accept it has reached `claimed`, is expected to fail: its failure is reported as expected and its pass fails the run.
- [r22] **Where** `work_expectations.py` is registered, a scenario that a `claimed`, `done` or `green` work-item accepts, or that no work-item accepts, runs as it is.
- [r23] **Where** `--work-item <name>` is given to pytest, only the scenarios that work-item accepts are run, each as it is, and the run fails when there are none.
- [r24] **Where** `work_expectations.py` is registered, the run's header names the `.shop/work` directory it read, or says none was found and nothing is expected to fail, and its summary says how many scenarios of which work-items were expected to fail.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`; the frontmatter subset `scripts/model` reads. A work-item's
  fields are `design-decision/work-file-forms`', plus `risk`, `plan`, `notes`, `fixes` and `findings`; its body
  sections are Observable, Unknown, Risk, Retires, Rulings, and the paths of its notes, plan, report and findings.
- `work_expectations.py` reads pytest-bdd's scenario object for the feature file and the tags, and marks a waiting
  scenario `xfail(strict=True)`.
- `log.jsonl` is one JSON object a line; a move and its file are written together, the log line last.

## Not yet
- A work-queue across bounded contexts (an upstream's items for a cross-context-request) — trigger: a second bounded context is delivered by `work run`.
