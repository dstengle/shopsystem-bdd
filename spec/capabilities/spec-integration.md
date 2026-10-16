---
id: missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: service
rests_on: [decision/one-spec-per-context, decision/gate-on-behaviour-lines, decision/spec-writers-blind-to-code, decision/controller-per-spec-round]
formulated_as: features/spec-integration.feature
retired: []
---

# Spec integration

## Purpose
Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, run by the session
the person talks to, with each round handed to a fresh `spec-round` that dispatches the
`capability-writer`. It is not formulation and not planning; it writes nothing a client can run.

## Behaviour
- [r1] **When** an approved note is integrated, the session shows the person every added, changed and removed Behaviour line and every question the note left open, each question with the lines its answers would give.
- [r2] **Where** the change comes from a note, a drafted line that quotes no sentence of the note is shown to the person as a question, not as a line.
- [r3] **While** the person has not said yes to the lines and answered every question, nothing under `spec/` changes.
- [r4] **When** the person answers a question, the answer is drafted as a further round and the changed lines are shown again before anything is written.
- [r5] **If** the person rejects a line, that line is not written to `spec/`.
- [r6] **When** the person says yes, the approved drafts are applied to `spec/`, with the Behaviour lines exactly as approved, and committed alone, with the approval and its date in the commit message.
- [r7] **When** a note would start a second spec in a context that has one, the session integrates it into the existing `spec/` instead.
- [r8] **Where** a change adds or changes at most two Behaviour lines in existing capabilities, changes no published contract and leaves nothing unknown, the session writes the lines itself from `spec/` alone and still stops at the gate before writing them.
- [r9] **Where** the person has delegated decisions to the session's recommendations, the commit, and the decision's source where the change is a decision, say that the lines were approved under that delegation.
- [r10] **When** this session is the one that brainstormed the note, it says so and recommends a new session for the integration before starting it.
- [r11] **When** integration is applied, the session hands the changed capabilities to formulation.

## Implementation, may change
- The session dispatches `spec-round` with the job `integrate` or `apply`, the note's path, a drafts path
  `.superpowers/spec-drafts/<date>-<note>/` and the round number; the round dispatches `capability-writer`,
  which writes only under `<drafts>/round-<n>/` and replies with the change list, questions, cut sentences
  and paths, last of all to a reply file.
- The round checks `git status --porcelain` against the state before dispatch and sends back an agent that
  wrote outside its drafts path; it checks the change list in both directions.
- Decisions are appended to `spec/decisions.md` (to be replaced by `decisions/` files: initiative i3).
- The format the writer carries is `docs/capability-format.md`.

## Not yet
- The gate approves requirement ids listed by a capability-proposal (`adds`, `changes`, `removes`) rather than lines shown as text — trigger: initiative i3 is approved.
