---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-2
retired: [U1, U2, U3, U6, U9, U10, U11, U4, U5, U7, U8, U12, U13, U14, U15, U16]
---

# Universal conditions

## Purpose

The statements that are true in every state of every trace (design model v5, `docs/reference/design-model.md`). Each
is written once here, in the requirement grammar, and is never restated in a requirement: a line that only restated
one is dropped with the U as its reason. `model logic` adds each as an `always` constraint to the background
of every check, and where a U is observable in a test (U17, U20) the scenario conftest checks it after every
scenario that makes its trigger true. They come from the domain model's §7 (`.shop/records/2026-11-02-domain-model/`).
U1, U2, U6, U9 and U10 stated guarantees of `work run`, its stages and initiatives, and are retired in plugin 0.31.0
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired). U11, U4, U5, U7 and U8 are
reworded in grammar 4 (b155, b240) as U12, U16 and U13 to U15. Retired ids are in `retired:` and are never used again.

## Behaviour
- [U17] If a service refuses a request, then the service shall name a reason and change nothing.
- [U18] A session shall not change an item.
- [U19] While a session has a workspace, the session shall change only files in the workspace.
- [U20] While this repository is in the workspace of a task, if a service keeps a kept change, then the service shall refuse the request and name the task.

## Reading

Plugin 0.38.0 (the domain contract, `.shop/records/2026-11-19-domain-contract/`) rewords U12, U14 and U15 in request
words as U17 to U19, and retires U13 into the design-decision "Git is the store and the isolation" and U16 into "The
response envelope": a commit, a push and `--json` are the adapters', not the domain's.

- U17: a refused request changes nothing, whatever service refused it, and names a reason. The reason is any reason:
  the language cannot yet tie it to the refusal (`grammar/language.md`, "What the language cannot say yet", #15).
- U18: an item, its status among its fields, is changed only by the backlog's, the drafting's, the batches' and the context requests' services, never by a
  session's own edit.
- U19: a workspace is a task's, made when a batch is opened, and the session that builds the task works in it. A
  session with no workspace, such as a reviewer, is not bound by it.
- U20: a task's workspace is its branch; every service that keeps a change refuses there, naming the task, so what
  it keeps lands on the base branch, never in the item's work. The batches service keeps its own changes on the base
  branch's checkout, so it is not refused by it.

### An "If" line takes precedence

This is a rule about how lines are read, not a statement about behaviour, so it has no U id and no tree.
- An EARS "If T, then R" line (`IfThen`, `WhileIf`, `WhereIf`) states unwanted behaviour, and it takes precedence over
  every line that is not an "If" line on the same trigger. When its condition holds, its responses are what happens,
  and the normal line does not apply.
- `model logic` therefore never pairs an "If" line with a non-"If" line (`exc/1` in `grammar/check.lp`). Two "If"
  lines on one trigger are still checked against each other.
- An implementation and a scenario follow the same rule: the "If" line's scenario holds even where a normal line's
  trigger is also true.