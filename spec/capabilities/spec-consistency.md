---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
title: Spec consistency
narrator: the person keeping a spec
group: service
rests_on: [design-decision/glossary-terms-are-standing, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code]
formulated_as: features/spec-consistency.feature
retired: []
---

# Spec consistency

## Purpose
Checks a bounded context's spec against itself: that one word means one thing, that one thing has one word,
that a line has one reading and that a scenario says what its line says. It is `checking-spec-consistency`,
run on demand by the session the person talks to, with a blind `spec-checker` agent for each judgment of
meaning. It reads nothing but `spec/` and `features/`, and it is not run by integration or formulation.

## Behaviour
- [r1] **When** the person asks for a consistency check, `checking-spec-consistency` shall run `model check` before anything else and report its `v_t1`, `v_t2` and `v_t3` rows as findings.
- [r2] **When** the check starts, `checking-spec-consistency` shall state how many `spec-checker` dispatches it will make, one for each capability and one for the whole context, before it dispatches any.
- [r3] **When** a `spec-checker` is dispatched, the `spec-checker` shall read only `spec/` and `features/`, never the source.
- [r4] **Where** the check runs in report mode, **when** the check ends, `checking-spec-consistency` shall have changed nothing but one findings file, each finding in it naming its ids.
- [r5] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term.
- [r6] **Where** fix mode is asked for, **when** the terms are settled, `checking-spec-consistency` shall have a scenario that uses an avoided word reworded to its line through formulation's small-change path, with no further approval.
- [r7] **Where** fix mode is asked for, **when** a line has two readings, `checking-spec-consistency` shall ask the person one question with its readings, to be integrated through the question path of `integrating-a-proposal`.
- [r8] **Where** fix mode is asked for, **when** a finding is drift other than a term or a line with two readings, `checking-spec-consistency` shall ask the person which side is right, one finding at a time.
- [r9] **Where** fix mode is asked for, **when** a step is done, `checking-spec-consistency` shall report what `model check` finds before the next step.
- [r10] **When** every finding is applied, rejected or recorded as an observation, `checking-spec-consistency` shall end fix mode with `model check` reporting no `v_t1`, `v_t2` or `v_t3` row.
- [r11] `checking-spec-consistency` shall run only when the person asks for it, never in an integration or formulation round.
- [r21] **If** `checking-spec-consistency` cannot do what it was asked, then `checking-spec-consistency` shall stop, saying why, and change nothing.

## Implementation, may change
- The skill is `skills/checking-spec-consistency/SKILL.md`; the agent is `agents/spec-checker.md`
  (tools Read, Glob, Grep, Write; model sonnet).
- One dispatch for each capability judges its lines against its scenarios; one for the context judges every
  Behaviour line and the glossary, with no scenarios.
- A `spec-checker` writes its findings to a file under the drafts path and replies with a short summary. The
  findings file is grouped by term cluster, then lines with two readings, then other drift.

## Not yet
- The check runs in integration and formulation rounds — trigger: a measured initiative shows drift the on-demand check would have caught.
