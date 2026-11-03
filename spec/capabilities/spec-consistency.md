---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
title: Spec consistency
narrator: the person keeping a spec
group: guarantees
rests_on: [design-decision/the-glossary-is-a-target-of-spec-work, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Spec consistency

## Purpose
Verifies a bounded context's spec against itself: that one word means one thing, that one thing has one word,
that a line has one reading, that the lines leave nothing to infer and that a scenario says what its line says. It is `checking-spec-consistency`,
used on demand by the session the person talks to, with a blind `spec-checker` dispatch for each judgment of
meaning. It reads nothing but `spec/` and `features/`, and integration and formulation do not use it.

## Terms

- **`checking-spec-consistency`** (actor): the skill that checks the spec's consistency, run only when the person asks.
- **violation** (kind): a row `model check` prints.
- **consistency finding** (kind): one finding of a consistency pass, naming its ids, written in its findings file.
- **competing pair** (kind): two requirements that act on one thing, such as one file, one status or one command, without saying which of them wins.
- **unscoped requirement** (kind): a requirement that leaves to inference which runs, workers or commands it applies to.
- **misplaced scenario** (kind): a scenario that shows the response of a requirement other than the one it names, or that gives an exit code.
- **orphan status** (kind): a status or a mode the requirements name, with a way into it or out of it that no requirement gives.
- **undefined word** (kind): a word a requirement depends on that is neither a term nor spelled out in the requirement.

## Behaviour

### [g1] A pass starts with `model check` and shows what it finds
Restates: r1@0.29, r2@0.29.
- [r1] When the person runs `checking-spec-consistency`, `checking-spec-consistency` shall start `model check`.
- [r2] When the person runs `checking-spec-consistency`, `checking-spec-consistency` shall show every violation.
- [r3] When the person runs `checking-spec-consistency`, `checking-spec-consistency` shall show the number of dispatches.

### [g2] A `spec-checker` reads no source
Restates: r3@0.29.
- [r4] `spec-checker` shall not read a module.

### [g3] A pass ends with its findings written
Restates: r4@0.29.
- [r5] When `checking-spec-consistency` ends, `checking-spec-consistency` shall write every consistency finding.

### [g4] The skill commits no requirement itself
Restates: r4@0.29.
- [r6] `checking-spec-consistency` shall not commit a requirement.

### [g5] Fix mode proposes a glossary entry for each term
Restates: r28@0.29.
- [r7] Where `--fix` is given, when `checking-spec-consistency` finds a term, `checking-spec-consistency` shall write a glossary-proposal.

### [g6] Fix mode asks about each finding
Restates: r8@0.29.
- [r8] Where `--fix` is given, when `checking-spec-consistency` finds a consistency finding, `checking-spec-consistency` shall ask a question.

### [g7] Fix mode runs `model check` after each answer
Restates: r9@0.29.
- [r9] Where `--fix` is given, when the person gives an answer, `checking-spec-consistency` shall start `model check`.

### [g8] Fix mode ends with no violation
Restates: r10@0.29.
- [r10] Where `--fix` is given, when `checking-spec-consistency` ends, `model` shall print no violation.

### [g9] The skill starts no round
Restates: r11@0.29.
- [r11] `checking-spec-consistency` shall not start a round.

### [g10] A refused command is shown and changes nothing
Restates: r21@0.29.
- [r12] If a command is refused, then `checking-spec-consistency` shall show the reason.
- [r13] If a command is refused, then `checking-spec-consistency` shall change nothing.

### [g11] Unrequested behaviour in a scenario is a finding
Restates: r22@0.29.
- [r14] When `spec-checker` finds an unrequested behaviour, `spec-checker` shall write a consistency finding.

### [g12] A competing pair is a finding
Restates: r23@0.29.
- [r15] When `spec-checker` finds a competing pair, `spec-checker` shall write a consistency finding.

### [g13] An unscoped requirement is a finding
Restates: r24@0.29.
- [r16] When `spec-checker` finds an unscoped requirement, `spec-checker` shall write a consistency finding.

### [g14] A misplaced scenario is a finding
Restates: r25@0.29.
- [r17] When `spec-checker` finds a misplaced scenario, `spec-checker` shall write a consistency finding.

### [g15] An orphan status is a finding
Restates: r26@0.29.
- [r18] When `spec-checker` finds an orphan status, `spec-checker` shall write a consistency finding.

### [g16] An undefined word is a finding
Restates: r27@0.29.
- [r19] When `spec-checker` finds an undefined word, `spec-checker` shall write a consistency finding.

### [g17] A finding names its ids
Restates: r4@0.29.
- [r20] When `spec-checker` writes a consistency finding, `spec-checker` shall name a requirement.

## Implementation, may change
- `skills/checking-spec-consistency/`, `agents/spec-checker.md`. The pass dispatches one `spec-checker` for each
  capability and one for the whole context, and says how many before it dispatches any. A `spec-checker` reads only
  `spec/` and `features/`.
- The findings it shows from `model check` are its `v_t1`, `v_t2` and `v_t3` rows. In findings mode the pass changes
  nothing but one findings file. In fix mode a glossary entry with its `Not:` words goes, with the statements that
  apply it, through one gate pass for the term; a changed statement is retired and its replacement given a new id.
- The pass starts only when the person asks, never during an integration or a formulation.

## Not yet
- None.

## Dropped
- r6@0.29: scenarios are generated from parsed statements, so no scenario uses a word the glossary avoids and none is reworded by hand.
- r7@0.29: no statement has two readings: one that does not parse to exactly one tree is refused (v_p1, v_p2).
