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

- [U1] `work run` shall hold at most `workers` worker slots at a time.
- [U2] `work run` shall not start a stage that needs a resource that is not free.
- [U3] If a command is refused, then it shall exit with an error naming the reason and change nothing.
- [U4] `work` shall commit every transition and push the commit.
- [U5] A session shall not write a status.
- [U6] When a session ends a stage with no result, `work run` shall discard the stage.
- [U7] A worker shall change only files in its worktree.
- [U8] Where `--json` is given, a tool shall print one JSON object.
- [U9] A delivery shall change no file of an initiative outside the delivery.
- [U10] When `work run` starts a stage, `work run` shall give the stage only a brief.

## Reading

Each statement has one `shall` (design model v5's grammar.md §6), in the wording of the grammar's corpus
(`grammar/corpus/universal.txt`). Where the domain model's §7 said more, the rest is carried by the lexicon and the
background theory of `model logic`, not by a second statement:

- U2: a stage starts only when every resource it needs is free (domain model §11). "Free" for a counted resource
  (a worker slot) means fewer than its number are held.
- U4: the push of each commit on the initiative branch is the second half of the statement; which remote it goes to is
  the meaning of *remote* in the glossary.
- U6: a round's node keeps its status and a work-item becomes `failed`. That is the meaning of *discard*, given by the
  `discard` transitions of each status attribute in the glossary.
- U7: narrowed to the worktree. The domain model also lets a worker change its stage directory; the grammar does not
  coordinate noun phrases of two kinds, and a worker's stage directory holds only what `work run` reads back from it
  (its result and report). Carried forward: a core fun for "X or Y" of two kinds, if two capabilities need it.
- U1, U2 and U9 follow from the resources of the glossary: a stage holds what it needs while it runs, an exclusive
  resource is held by one session at a time, and a counted one by at most its number.
