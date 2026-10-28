---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
title: Spec consistency
narrator: the person keeping a spec
group: guarantees
rests_on: [design-decision/the-glossary-is-a-target-of-spec-work, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code, design-decision/workflow-capabilities-are-guarantees]
retired: []
---

# Spec consistency

## Purpose
Verifies a bounded context's spec against itself: that one word means one thing, that one thing has one word,
that a line has one reading, that the lines leave nothing to infer and that a scenario says what its line says. It is `checking-spec-consistency`,
used on demand by the session the person talks to, with a blind `spec-checker` dispatch for each judgment of
meaning. It reads nothing but `spec/` and `features/`, and integration and formulation do not use it.

## Behaviour
- [r1] **When** the person asks for a consistency pass, `checking-spec-consistency` shall run `model check` before anything else and give its `v_t1`, `v_t2` and `v_t3` rows as findings.
- [r2] **When** the pass starts, `checking-spec-consistency` shall say how many `spec-checker` dispatches it will make, one for each capability and one for the whole context, before it dispatches any.
- [r3] **When** a `spec-checker` is dispatched, the `spec-checker` shall read only `spec/` and `features/`, never the source.
- [r4] **Where** the pass is in findings mode, **when** the pass ends, `checking-spec-consistency` shall have changed nothing but one findings file, each finding in it naming its ids.
- [r5] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term.
- [r6] **Where** fix mode is asked for, **when** the terms are settled, `checking-spec-consistency` shall have a scenario that uses an avoided word reworded to its line through formulation's small-change path, with no further approval.
- [r7] **Where** fix mode is asked for, **when** a line has two readings, `checking-spec-consistency` shall ask the person one question with its readings, to be integrated through the question path of `integrating-a-proposal`.
- [r8] **Where** fix mode is asked for, **when** a finding is drift other than a term or a line with two readings, `checking-spec-consistency` shall ask the person which side is right, one finding at a time.
- [r9] **Where** fix mode is asked for, **when** a step is complete, `checking-spec-consistency` shall tell the person what `model check` finds before the next step.
- [r10] **When** every finding is applied, rejected or written as an observation, `checking-spec-consistency` shall end fix mode with `model check` printing no `v_t1`, `v_t2` or `v_t3` row.
- [r11] `checking-spec-consistency` shall start only when the person asks for it, never during an integration or a formulation.
- [r21] **If** `checking-spec-consistency` cannot do what it was asked, then `checking-spec-consistency` shall stop, saying why, and change nothing.
- **When** a `spec-checker` finds one of the following in what it reads, the `spec-checker` shall write it as a finding, naming its ids:

  | id | found |
  |---|---|
  | [r22] | a scenario that shows observable behaviour, such as an output, a file written or a status, that no Behaviour line of its capability asks for |
  | [r23] | two lines that act on one thing, such as one file, one status or one command, without saying which of them wins |
  | [r24] | a line that leaves to inference which runs, workers or commands it applies to |
  | [r25] | a scenario that shows the response of a line other than the one it names, an exit or a refusal of the capability's general failure line included, or that gives an exit code |
  | [r26] | a status or a mode that the lines name, with a way into it or out of it that no line gives |
  | [r27] | a word a line depends on that is neither a glossary term nor spelled out in the line |


## Implementation, may change
- The skill is `skills/checking-spec-consistency/SKILL.md`; the agent is `agents/spec-checker.md`
  (tools Read, Glob, Grep, Write; model sonnet).
- One dispatch for each capability judges its lines against its scenarios (r22, r23, r24 and r25 within the
  capability); one for the context judges every Behaviour line and the glossary, with no scenarios (r23 and r24
  across capabilities, r26 and r27).
- A `spec-checker` writes its findings to a file under the drafts path and replies with a short summary. The
  findings file is grouped by term cluster (r27 among them), then lines with two readings, lines in the wrong
  pattern, lines left to infer (r23, r24, r26), behaviour no line asks for (r22), scenarios showing another
  line's response (r25), then other drift.

## Not yet
- The pass is used during integration and formulation — trigger: a measured initiative shows drift the on-demand pass would have caught.
