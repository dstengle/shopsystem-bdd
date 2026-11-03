---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-1
retired: []
---

# Universal conditions

## Purpose

The statements that are true in every state of every trace (design model v5, `docs/design-model/design-model.md`
§2.5). Each is written once here, in the requirement grammar, and is never restated in a requirement: a line that only
restated one is dropped with the U as its reason. `model logic` adds each as an `always` constraint to the background
of every check, and where a U is observable in a test (U3, U8) the scenario conftest checks it after every scenario
that makes its trigger true. They come from the domain model's §7 (`.shop/records/2026-11-02-domain-model/`), worded
to parse.

## Behaviour

- [U1] `work run` shall hold at most `workers` worker slots.
- [U2] While a resource that a stage needs is not free, `work run` shall not start the stage.
- [U3] If a tool refuses a command, then the tool shall exit with an error that names the reason.
- [U4] When a tool commits a change on an initiative branch, the tool shall push the initiative branch to the remote.
- [U5] Only `work` shall write a status.
- [U6] When a stage ends without a readable result, `work run` shall discard the stage.
- [U7] A worker shall not change a file outside its worktree and its stage directory.
- [U8] Where `--json` is given, the tool shall print one JSON object.
- [U9] `work run` shall not change an initiative directory that it does not hold.
- [U10] When `work run` starts a stage, `work run` shall give the stage its brief and no other input.

## Reading

Each statement has one `shall` (design model v5's grammar.md §6). What the domain model said with a second verb is
carried by the lexicon and the background theory of `model logic`, not by a second statement:

- U3: a refused command changes nothing. That is the meaning of *refuse* (its after-state is its before-state), so
  U3 says only the exit and the reason.
- U4: every transition is committed. A transition is written by `work` and committed with it (the transition rows of
  the glossary), so U4 says only the push.
- U6: a round's node keeps its status and a work-item becomes `failed`. That is the meaning of *discard*, given by the
  `discard` transitions of each status attribute in the glossary.
- U1, U2 and U9 follow from the resources of the glossary: a stage holds what it needs while it runs, an exclusive
  resource is held by one session at a time, and a counted one by at most its number.
