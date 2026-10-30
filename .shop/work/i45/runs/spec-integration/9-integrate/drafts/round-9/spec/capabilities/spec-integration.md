frontmatter

---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: guarantees
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator, design-decision/the-glossary-is-a-target-of-spec-work]
retired: [r5, r9, r18, r8, r10, r11, r34, r36, r37, r38, r41, r42, r17, r13]
---

## Behaviour
- [r1] **When** an approved note is integrated, `integrating-a-proposal` shall show the person every added, changed and removed Behaviour line, each with its id, and every question the note left open, each with the lines its answers would give.
- [r2] **When** a line drafted from a note quotes no sentence of the note, `integrating-a-proposal` shall show it to the person as a question, not as a line.
- [r3] **While** the person has not said yes to the lines and answered every question, `integrating-a-proposal` shall change nothing under `spec/`.
- [r4] **When** the person answers a question, `integrating-a-proposal` shall show the changed lines again, the answer drafted as a further round, before anything is written.
- [r6] **When** the person says yes, `integrating-a-proposal` shall commit the approved drafts to `spec/` alone, with the Behaviour lines exactly as approved.
- [r15] **When** the approved drafts are committed, `integrating-a-proposal` shall name in the commit message the approval and its date, any delegation it was given under, and each id and each glossary term added, changed and removed.
- [r7] **When** a note would start a second spec in a context that has one, `integrating-a-proposal` shall integrate it into the existing `spec/` instead.
- [r12] **When** a line is added to a capability, `integrating-a-proposal` shall give it the id one above every id the capability has used or retired, wherever the line sits in the section.
- [r67] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id.
- [r14] **When** a line is removed, `integrating-a-proposal` shall add its id to the capability's `retired` list.
- [r16] **Where** `model check` is available, **if** applying the approved drafts makes it print a new problem other than an added line with no scenario yet, a removed line's scenario that now names no line, or a scenario that uses a word the new glossary entry avoids, then `integrating-a-proposal` shall not commit them.
- [r54] **When** a round of the kind `integrate` drafts a change to the glossary, `initiative-round` shall give the terms the change adds, changes and removes in the change list's entry for the glossary and in no entry for a capability.
- [r55] **While** the person has not approved the terms of a glossary-proposal, `initiative-round` shall apply none of them to `spec/index.md`.
- [r59] **When** a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes.
- [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, `integrating-a-proposal` shall put it through the gate like a Behaviour line.
- [r20] **When** a change makes a decision, `integrating-a-proposal` shall show it to the person as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`.
- [r21] **When** a drafted decision names what it came from, `integrating-a-proposal` shall list by id in its `source` only records, initiatives and decisions, writing the person, a date, a delegation or anything outside the repository in its `by`.
- [r22] **When** the approved drafts are committed with a decision, `integrating-a-proposal` shall commit in the same commit the `spec/decisions/index.md` that `model decisions` writes.
- [r35] **When** `initiative-round` runs the kind `gate`, `initiative-round` shall give in its result one question for each decision the person is asked to make, each marking the recommended reading and giving the lines it concerns in full.
- [r64] **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking.
- [r39] **When** `initiative-round` runs the kind `apply` with the file of the person's answers, or with the person's approval in their words, `initiative-round` shall apply exactly the drafts the person approved.
- [r46] **When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold.
- [r40] **When** `initiative-round` finishes a round, `initiative-round` shall append one line to the initiative's ledger with `work note`, naming the kind, the round, and what the round ended with or the answers it applied.
- [r43] **When** a round of the kind `integrate` is given requirement ids that other initiatives' drafts add, `initiative-round` shall number the round's added lines above every id it is given on the same capability.
- [r45] **When** a round of the kind `integrate` is given answers that ask for lines the request's accepted lines do not, `initiative-round` shall draft those lines under the capabilities the answers name.
- [r44] **Where** `spec/index.md` names an upstream bounded-context, **when** a round of the kind `integrate` drafts a line that needs what the upstream does not yet give, `initiative-round` shall give in its result the lines of a request into that upstream, in the upstream's terms.
- [r61] **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts.
- [r62] **When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions.
- [r63] **When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it.
- [r65] **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading.
- [r60] The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines.
- [r66] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id.
- [r33] **If** `integrating-a-proposal` cannot do what it was asked, then `integrating-a-proposal` shall stop, saying why, and change nothing under `spec/`.
