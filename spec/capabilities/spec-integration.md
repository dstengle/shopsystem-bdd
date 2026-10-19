---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids]
retired: []
---

# Spec integration

## Purpose
Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, run by the session
the person talks to, with each round handed to a fresh `initiative-round` that dispatches the
`capability-writer`. It is not formulation and not planning; it writes nothing a client can run.

## Behaviour
- [r1] **When** an approved note is integrated, the session shows the person every added, changed and removed Behaviour line, each with its id, and every question the note left open, each question with the lines its answers would give.
- [r2] **Where** the change comes from a note, a drafted line that quotes no sentence of the note is shown to the person as a question, not as a line.
- [r3] **While** the person has not said yes to the lines and answered every question, nothing under `spec/` changes.
- [r4] **When** the person answers a question, the answer is drafted as a further round and the changed lines are shown again before anything is written.
- [r5] **If** the person rejects a line, that line is not written to `spec/`.
- [r6] **When** the person says yes, the approved drafts are applied to `spec/`, with the Behaviour lines exactly as approved, and committed alone, with the approval and its date in the commit message.
- [r7] **When** a note would start a second spec in a context that has one, the session integrates it into the existing `spec/` instead.
- [r8] **Where** a change adds or changes at most two Behaviour lines in existing capabilities, changes no published contract and leaves nothing unknown, the session writes the lines itself from `spec/` alone and still stops at the gate before writing them.
- [r9] **Where** the person has delegated decisions to the session's recommendations, the commit, and the decision's `by` where the change is a decision, say that the lines were approved under that delegation.
- [r10] **When** this session is the one that brainstormed the note, it says so and recommends a new session for the integration before starting it.
- [r11] **When** integration is applied, the session hands the changed capabilities to formulation.
- [r12] **When** a line is added to a capability, it takes the id one above every id the capability has used or retired, wherever the line sits in the section.
- [r13] **When** a line is changed, it keeps its id.
- [r14] **When** a line is removed, its id is added to the capability's `retired` list and no later line takes it.
- [r15] **When** the approved drafts are committed, the commit message names each id added, changed and removed.
- [r16] **Where** `model check` can run, **when** the approved drafts are applied, the only new problems it may report are: an added line with no scenario yet, a removed line's scenario that now names no line, and a scenario that uses a word the new glossary entry avoids; formulation clears all three, and any other new problem stops the commit.
- [r17] **Where** a repository keeps `.shop/work/`, a change to a glossary term rides with the capability-proposal that needs it, which lists the term in `adds`, `changes` or `removes`.
- [r18] **When** the approved drafts are committed, the commit message names each term added, changed and removed.
- [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, the session shows it to the person like a Behaviour line and writes nothing to `spec/` before the person says yes.
- [r20] **When** a change makes a decision, the person is shown it as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`, with a one-sentence summary and a Decision section, and a Context and Alternatives only where options were weighed.
- [r21] **When** a drafted decision names what it came from, its `source` lists records, initiatives or decisions by id, and the person, a date, a delegation or anything outside the repository is written in its `by`.
- [r22] **When** the approved drafts are committed with a decision, `spec/decisions/index.md` is the one `model decisions` writes, in the same commit.

## Implementation, may change
- The session dispatches `initiative-round` with the job `integrate` or `apply`, the note's path, a drafts path
  `.shop/scratch/drafts/<date>-<note>/` and the round number; the round dispatches `capability-writer`,
  which writes only under `<drafts>/round-<n>/` and replies with the change list, questions, cut sentences
  and paths, last of all to a reply file.
- The round checks `git status --porcelain` against the state before dispatch and sends back an agent that
  wrote outside its drafts path; it checks the change list in both directions.
- The writer drafts a decision as a whole file under `<drafts>/round-<n>/spec/decisions/`; applying it copies the
  file and runs `model decisions`.
- The format the writer follows is `docs/capability-format.md`.

## Not yet
- The gate approves requirement ids listed by a capability-proposal (`adds`, `changes`, `removes`) under `.shop/work/` rather than lines shown as text; until then the gate shows each line with its id — trigger: a consuming repository keeps `.shop/work/` and asks for it.
