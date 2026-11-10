---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-2
retired: [U1, U2, U3, U6, U9, U10, U11, U4, U5, U7, U8]
---

# Universal conditions

## Purpose

The statements that are true in every state of every trace (design model v5, `docs/design-model/design-model.md`
§2.5). Each is written once here, in the requirement grammar, and is never restated in a requirement: a line that only
restated one is dropped with the U as its reason. `model logic` adds each as an `always` constraint to the background
of every check, and where a U is observable in a test (U12, U13, U16) the scenario conftest checks it after every
scenario that makes its trigger true. They come from the domain model's §7 (`.shop/records/2026-11-02-domain-model/`).
U1, U2, U6, U9 and U10 stated guarantees of `work run`, its stages and initiatives, and are retired in plugin 2.0.0
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired). U11, U4, U5, U7 and U8 are
reworded in grammar 4 (b155, b240) as U12, U16 and U13 to U15. Retired ids are in `retired:` and are never used again.

## Behaviour

- [U12] If a tool refuses a command, then the tool shall exit with an error naming a reason and change nothing.
- [U13] When `work` writes a transition, `work` shall commit the transition and push the commit of the transition.
- [U14] A session shall not write a transition.
- [U15] While a dispatch has a worktree, the dispatch shall change only files in the worktree.
- [U16] When an agent runs a command of a tool with the `--json` option, the tool shall print one JSON object.

## Reading

Each is one statement: what one condition asks is written as verb phrases joined by `and` under one `shall` (U12
"exit with an error naming a reason and change nothing", U13 "commit the transition and push the commit of the
transition"). Each line's intended reading is in the corpus `grammar/corpus/spec/universal.md`. Where the domain
model's §7 said more, the rest is carried by the lexicon and the background theory of `model logic`:

- U12: a refused command changes nothing, whatever tool refused it. The reason the error names is any reason: the
  language cannot yet tie it to the refusal (`grammar/language.md`, "What the language cannot say yet", #15).
- U13: the push of each commit `work` makes of a transition; which remote it goes to is the meaning of *remote* in
  the glossary. The commit is the transition's by the row `commit | of | transition`.
- U13, U14: a transition is the change of a status `work` writes. The language has no form yet for changing the value
  of an attribute ("change the status of an item"), so *transition* stands for it (#8): `work` is the only writer of
  a status.
- U15: a worktree is a task's, made by `work batch start`, and the dispatch that builds the task works in it (the row
  `worktree | of | session | one`). A dispatch with no worktree, such as a reviewer, is not bound by it.
- U16: the `--json` option is in the trigger, given to a command of the tool that prints the object.


### An "If" line takes precedence

This is a rule about how lines are read, not a statement about behaviour, so it has no U id and no tree.
- An EARS "If T, then R" line (`IfThen`, `WhileIf`, `WhereIf`) states unwanted behaviour, and it takes precedence over
  every line that is not an "If" line on the same trigger. When its condition holds, its responses are what happens,
  and the normal line does not apply.
- `model logic` therefore never pairs an "If" line with a non-"If" line (`exc/1` in `grammar/check.lp`). Two "If"
  lines on one trigger are still checked against each other.
- An implementation and a scenario follow the same rule: the "If" line's scenario holds even where a normal line's
  trigger is also true.