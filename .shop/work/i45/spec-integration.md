---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i45-spec-integration
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i45
status: awaiting-answer
argues: [spec-integration]
date: 2026-10-28
adds: [spec-integration#r58, spec-integration#r59, spec-integration#r60, spec-integration#r61, spec-integration#r62, spec-integration#r63, spec-integration#r64, spec-integration#r65]
changes: []
removes: [spec-integration#r13]
---

# spec-integration

The drafts of this proposal are in .shop/work/i45/runs/spec-integration/3-integrate/drafts/round-3/.

## Questions
- Q1 (spec-integration r48): the check has no visible result. What does the round do with a finding? Line drafted: [r48] **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts.
  A (recommended): add "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions."
  B: the same trigger, but `initiative-round` shall dispatch the `capability-writer` again with the finding before the gate round starts.
  C: r48 only, as the request words it.
- Q2 (spec-integration r48): under the `catch-all trigger` entry the general failure line ("If <system> cannot do what it was asked, then ...") is a catch-all trigger, so r48 would report it every round. Line drafted: [r48] as in Q1.
  A (recommended): it is not a finding; r48 is replaced by (new id): "**When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts."
  B: it is a finding every time: r48 as drafted.
- Q3 (spec-integration r50): what counts as "a convention of the spec"? Line drafted: [r50] **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking.
  A (recommended): a rule `docs/capability-format.md` or a decision under `spec/decisions/` states (the drafted `convention` entry).
  B: also any Behaviour line.
  Clash to decide: r50 settles a question without asking, while r1, r3 and r35 expect every question at the gate. Recommended: a question r50 settles is not one the person is asked, so no change is drafted. If you read it otherwise, r35 takes an exception (r35 retired, a new line added): "**When** `initiative-round` runs the kind `gate`, `initiative-round` shall give in its result one question for each decision the person is asked to make that no convention settles, each marking the recommended reading and giving the lines it concerns in full."
- Q4 (spec-integration r47): what counts as "a session that writes a request's lines"? Line drafted: [r47] The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines.
  A (recommended): every such session, the person's running `work request` and an integrate round giving lines into an upstream (r44) included.
  B: only the plugin's agents and rounds: "The plugin shall give a skill for writing requirement lines to the `capability-writer` and to each of its rounds that gives the lines of a request."
- Q5 (spec-integration r49): "The glossary shall define..." names the glossary as the system, so no round or skill is responsible for it. Line drafted: [r49] The glossary shall define each event and each condition that a line's trigger names.
  A (recommended): replace r49 by: "**When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it."
  B: no spec-integration line; a row in the `spec-checker`'s table in spec-consistency: "| [r29] | an event or a condition that a line's trigger names and the glossary does not define |" (r49 not added).
  C: r49 as the request words it (drafted).
  Note: spec-consistency r27 already finds a word a line depends on that is neither a term nor spelled out; line 4 is stricter.
- Q6 (spec-integration r49): do existing lines count? Most existing triggers name events with no glossary entry. Line drafted: [r49] as in Q5.
  A (recommended): only lines drafted from now on (Q5 A's line).
  B: every line, existing ones included: r49 as drafted, and a work-item that adds the entries.
- Q7 (spec-integration r13, r52, r53; line 7): r13 says the opposite of line 7. Lines: removed [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id.; added [r52] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id.; added [r53] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id.
  A (recommended, drafted): retire r13; add r52 and r53 (spec-consistency r5/r28 are gated in that capability's proposal).
  B: leave r13 and add r52 only; the spec then contradicts itself.
  Formulation r1 and r13 ("added or changed line") still read true under A.
- Q8 (decision; spec-integration r52, r53): line 7 reverses a rule `docs/capability-format.md` states, which decision 0031's Context relies on. Is a decision drafted?
  A: yes: draft `spec/decisions/0073-a-changed-line-is-retired.md` (summary "A changed Behaviour line is retired and its replacement given a new id; no line keeps its id when its words change.", date 2026-10-28, status proposed, source [request/q26, record/2026-10-28-requirement-checking], by "the request q26, line 7, accepted"), and spec-integration's `rests_on` names it.
  B (recommended, drafted): no decision; r52 and r53 are the rule.
- Q1 (r59 against r60): r59 leaves a capability's general failure line out of the check, but r60's trigger does not. Lines: added [r59] **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts.; added [r60] **When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions. A (recommended): replace r60 by "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions." B: r60 as drafted, read as giving only what r59's check finds.
- Q2 (r64, r65 against docs/capability-format.md): the format document still says "A changed line keeps its id" until r64 is delivered. Lines: added [r64] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id.; added [r65] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id.; removed [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id. A (recommended): no further line; r64's work-item changes the format. B: a Not yet entry: "Rounds follow r65 over `docs/capability-format.md`'s Requirement ids — trigger: r64 delivered."
- Q3 (mapping of answers): the answers carried labels from an earlier gate (the answer under Q2 reads "Q4, r47's session"); the integrate round matched each by its words. Lines concerned: added [r58] The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines.; added [r61] **When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it.; added [r62] **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking.; added [r63] **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. A (recommended): the mapping stands. B: an answer that belongs elsewhere is drafted again.

## Answers
- 2026-10-28: Q1, r48's finding: reading A, the finding is given in the round's result and in the gate's questions, naming both lines' ids (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q4, r47's session: reading A, every session that writes a request's lines (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q7, r13 against line 7: reading A, retire r13 and add r52 and r53 (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q8, a decision for line 7: reading B, no decision; r52 and r53 are the rule (decision number 0073 is now taken by i46's) (answered by the coordinator under the person's delegation, 2026-10-28)
- 2026-10-28: Q2, r48 and the general failure line: reading A, it is not a finding; r48 is replaced under a new id excluding a capability's general failure line (answered by the person, 2026-10-28)
- 2026-10-28: Q3, r50's convention: reading A, a rule docs/capability-format.md or a decision under spec/decisions/ states; a question r50 settles is not asked, so r35 is unchanged (answered by the person, 2026-10-28)
- 2026-10-28: Q5, r49's subject: reading A, r49 replaced by: an integrate round that drafts a line whose trigger names an event or condition the glossary does not define drafts a glossary entry for it (answered by the person, 2026-10-28)
- 2026-10-28: Q6, r49 and existing lines: reading A, only lines drafted from now on (answered by the person, 2026-10-28)
- 2026-10-30: A: replace r60 by "When a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/` other than a capability's general failure line, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions." (the person's delegation of 2026-10-29: answer every question with its recommended reading)
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-30: A: no further line; r64's work-item changes the format (the recommended reading, under the person's 2026-10-29 delegation).
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-30: A: the mapping stands (the person's delegation, 2026-10-29: answer every question with its recommended reading).
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
