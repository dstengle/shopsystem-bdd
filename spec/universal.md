---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-1
retired: [U1, U2, U3, U6, U9, U10]
---

# Universal conditions

## Purpose

The statements that are true in every state of every trace (design model v5, `docs/design-model/design-model.md`
§2.5). Each is written once here, in the requirement grammar, and is never restated in a requirement: a line that only
restated one is dropped with the U as its reason. `model logic` adds each as an `always` constraint to the background
of every check, and where a U is observable in a test (U11, U8) the scenario conftest checks it after every scenario
that makes its trigger true. They come from the domain model's §7 (`.shop/records/2026-11-02-domain-model/`), worded
to parse. U1, U2, U6, U9 and U10 stated guarantees of `work run`, its stages and initiatives, and are retired in plugin
2.0.0 (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): their ids are in
`retired:` and are never used again. U7 is kept, still true of a batch's task subagent in its worktree, until a line
on that subagent is written.

## Behaviour

- [U11] If a tool refuses a command, then the tool shall exit with an error naming the reason and change nothing.
- [U4] `work` shall commit every transition and push the commit.
- [U5] A session shall not write a status.
- [U7] A worker shall change only files in its worktree.
- [U8] Where `--json` is given, a tool shall print one JSON object.

## Reading

Each is one statement (design-r2 §4.1): what one condition asks is written as verb phrases joined by `and` under one
`shall` (U11 "exit with an error naming the reason and change nothing", U4 "commit every transition and push the
commit"), and `model logic` reads each conjunct as its own constraint under the one U id. The wording is the
grammar's corpus (`grammar/corpus/universal.txt`). Where the domain model's §7 said more, the rest is carried by the
lexicon and the background theory of `model logic`, not by a second statement:

- U11: a refused command changes nothing, whatever tool refused it (the glossary's *refuse* said so until revision 2).
  It is U3 reworded for verb frames (b82): U3's "a command is refused" is a passive with no agent, and *refuse*
  takes a subject.
- U4: the push of each commit on the initiative branch is the second conjunct of the statement; which remote it goes
  to is the meaning of *remote* in the glossary.
- U5: `work` is the only writer of a status (the glossary's *`work`* said so until revision 2): a session writes
  none, and `work run` has `work` write each one.
- U7: narrowed to the worktree. The domain model also lets a worker change its stage directory. `or` now joins
  conditions (`CondOr`) and the verb phrases under `shall not`, but not noun phrases, so "files in its worktree or its
  stage directory" has no tree; a worker's stage directory holds only what `work run` reads back from it (its result
  and report). Carried forward to R14: a core fun for "X or Y" of two noun phrases.


### An "If" line takes precedence

This is a rule about how lines are read, not a statement about behaviour, so it has no U id and no tree.
- An EARS "If T, then R" line (`IfThen`, `WhileIf`, `WhereIf`) states unwanted behaviour, and it takes precedence over
  every line that is not an "If" line on the same trigger. When its condition holds, its responses are what happens,
  and the normal line does not apply.
- `model logic` therefore never pairs an "If" line with a non-"If" line (`exc/1` in `grammar/check.lp`). Two "If"
  lines on one trigger are still checked against each other.
- An implementation and a scenario follow the same rule: the "If" line's scenario holds even where a normal line's
  trigger is also true.