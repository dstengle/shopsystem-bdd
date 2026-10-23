---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: guarantees
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids, design-decision/the-session-keeps-the-gate, design-decision/workflow-capabilities-are-guarantees]
retired: [r5, r9, r18]
---

# Spec integration

## Purpose
Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, used by the session
the person talks to, each round a fresh dispatch of `initiative-round`, which dispatches the
`capability-writer`. It is not formulation and not planning; it writes nothing a client can run.

## Behaviour
- [r1] **When** an approved note is integrated, `integrating-a-proposal` shall show the person every added, changed and removed Behaviour line, each with its id, and every question the note left open, each with the lines its answers would give.
- [r2] **When** a line drafted from a note quotes no sentence of the note, `integrating-a-proposal` shall show it to the person as a question, not as a line.
- [r3] **While** the person has not said yes to the lines and answered every question, `integrating-a-proposal` shall change nothing under `spec/`.
- [r4] **When** the person answers a question, `integrating-a-proposal` shall show the changed lines again, the answer drafted as a further round, before anything is written.
- [r6] **When** the person says yes, `integrating-a-proposal` shall commit the approved drafts to `spec/` alone, with the Behaviour lines exactly as approved.
- [r15] **When** the approved drafts are committed, `integrating-a-proposal` shall name in the commit message the approval and its date, any delegation it was given under, and each id and each glossary term added, changed and removed.
- [r7] **When** a note would start a second spec in a context that has one, `integrating-a-proposal` shall integrate it into the existing `spec/` instead.
- [r8] **Where** a change adds or changes at most two Behaviour lines in existing capabilities, changes no published contract and leaves nothing unknown, `integrating-a-proposal` shall write the lines itself from `spec/` alone.
- [r10] **When** an integration is started in the session that brainstormed the note, `integrating-a-proposal` shall recommend a new session for the integration before starting it, saying that this session brainstormed the note.
- [r11] **When** integration is applied, `integrating-a-proposal` shall hand the changed capabilities to formulation.
- [r12] **When** a line is added to a capability, `integrating-a-proposal` shall give it the id one above every id the capability has used or retired, wherever the line sits in the section.
- [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id.
- [r14] **When** a line is removed, `integrating-a-proposal` shall add its id to the capability's `retired` list.
- [r16] **Where** `model check` is available, **if** applying the approved drafts makes it print a new problem other than an added line with no scenario yet, a removed line's scenario that now names no line, or a scenario that uses a word the new glossary entry avoids, then `integrating-a-proposal` shall not commit them.
- [r17] **Where** a repository keeps `.shop/work/`, **when** a glossary term is changed, `integrating-a-proposal` shall put the change with the capability-proposal that needs it, listing the term in its `adds`, `changes` or `removes`.
- [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, `integrating-a-proposal` shall put it through the gate like a Behaviour line.
- [r20] **When** a change makes a decision, `integrating-a-proposal` shall show it to the person as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`.
- [r21] **When** a drafted decision names what it came from, `integrating-a-proposal` shall list by id in its `source` only records, initiatives and decisions, writing the person, a date, a delegation or anything outside the repository in its `by`.
- [r22] **When** the approved drafts are committed with a decision, `integrating-a-proposal` shall commit in the same commit the `spec/decisions/index.md` that `model decisions` writes.
- [r34] **When** the rounds' drafts are ready to show the person, `integrating-a-proposal` shall dispatch `initiative-round` with the job `gate`, naming the rounds' drafts and any reports to show.
- [r35] **When** `initiative-round` runs the job `gate`, `initiative-round` shall write under `<drafts path>/gate/` one card for each decision the person is asked to make, each card marking the coordinator's recommendation and giving the lines it concerns in full.
- [r36] **When** the job `gate` has written its cards, `initiative-round` shall reply with the path of `<drafts path>/gate/`.
- [r37] **When** the job `gate` replies, `integrating-a-proposal` shall publish the gate page from the files under `<drafts path>/gate/`.
- [r38] **While** the gate page is published, `integrating-a-proposal` shall read only the person's answers, none of the rounds' drafts.
- [r39] **When** `initiative-round` runs the job `apply` with the file of the person's answers, or with the person's approval in their words, `initiative-round` shall apply exactly the drafts the person approved.
- [r40] **When** `initiative-round` finishes a round, `initiative-round` shall append one line to the initiative's ledger `.shop/scratch/run/ledger-<initiative>.md`, naming the job, the round, and what the round ended with or the answers it applied.
- [r41] **When** `integrating-a-proposal` dispatches an agent, `integrating-a-proposal` shall ask it to reply in a few lines and leave the rest in files.
- [r42] **When** a dispatch `integrating-a-proposal` started has replied, `integrating-a-proposal` shall read a file the dispatch wrote only to decide what to do next.
- [r33] **If** `integrating-a-proposal` cannot do what it was asked, then `integrating-a-proposal` shall stop, saying why, and change nothing under `spec/`.

## Implementation, may change
- The session dispatches `initiative-round` with an input giving the job `integrate`, `gate` or `apply`, the note's path, a drafts path
  `.shop/scratch/drafts/<date>-<note>/` and the round number; the round dispatches `capability-writer`,
  which writes only under `<drafts>/round-<n>/` and replies with the change list, questions, cut sentences
  and paths, last of all to a reply file.
- The job `gate` is given the rounds' drafts and any reports to show; the job `apply` is given the file of the
  person's answers or their approval in their words.
- The round compares `git status --porcelain` with the porcelain before dispatch and sends back a dispatch that
  wrote outside its drafts path; it verifies the change list in both directions.
- The writer drafts a decision as a whole file under `<drafts>/round-<n>/spec/decisions/`; applying it copies the
  file and runs `model decisions`.
- The format the writer follows is `docs/capability-format.md`. A decision has a one-sentence summary and a
  Decision section, and a Context and Alternatives only where options were weighed (design-decision/light-decisions).

## Not yet
- The gate approves requirement ids listed by a capability-proposal (`adds`, `changes`, `removes`) under `.shop/work/` rather than lines shown as text; until then the gate shows each line with its id — trigger: a consuming repository keeps `.shop/work/` and asks for it.
