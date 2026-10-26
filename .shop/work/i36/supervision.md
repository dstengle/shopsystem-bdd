---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i36-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i36
status: awaiting-answer
argues: [supervision]
adds: [supervision#r125, supervision#r126, supervision#r127]
changes: []
removes: []
date: 2026-10-26
---

# supervision

The drafts of this proposal are in .shop/work/i36/runs/i36/1-integrate/drafts/round-1/.

## Questions
- New lines or changes? Drafted as new lines (r112 and r113 untouched):
  [r125] **When** `work run` writes the brief of a round of the kind `formulate`, `work run` shall tell the round that a round that has formulated every line with one reading and gives each other line as a question has done its work, with the outcome `DONE`.
  [r126] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall write each question its result gives under the proposal's `## Questions`.
  [r127] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall transition the proposal to `awaiting-answer`.
  Existing:
  [r112] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal's `## Questions`.
  [r113] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`.
  Readings: (a) new lines, r112/r113 as they are; (b) change: drop r126 and r127; r112 reads 'gives questions, with the outcome `DONE` or `PARTIAL`, ...' and r113 'gives a question, with the outcome `DONE` or `PARTIAL`, ...'. Recommended: (a).
- r86 and r87 (keep status; make no transition on an outcome other than `DONE`) conflict with r127:
  [r127] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall transition the proposal to `awaiting-answer`.
  Exempt a `formulate` round that gives a question with `PARTIAL` from r86 and r87? Readings: (a) yes, exempt; (b) no, so r127 cannot hold (drop it, and r126 with it or keep r126 alone). Recommended: (a).
- r88 and r115 (exit with an error naming the round, and take other nodes through their transitions first) apply to any outcome other than `DONE`. Does `work run` still exit with an error for a `formulate` round that gives a question with `PARTIAL`? Readings: (a) no: r88 and r115 take the same exemption and the proposal waits like any `awaiting-answer` node (r81/r32/r101 decide the exit); (b) yes: r88 and r115 stay as they are. Recommended: (a).
- A `formulate` round ends in an error or at its turn limit, but its result gives a question with `PARTIAL`: do r126 and r127 hold then too? Readings: (a) yes: the exemptions read 'other than a round of the kind `formulate` whose result gives a question with the outcome `PARTIAL`'; (b) no: r126 and r127 gain 'ends neither in an error nor at its turn limit and' (exemption only for rounds that ended normally). Recommended: (b).
- 'Not yet' says: 'Retries, continuations after `PARTIAL`, refused claims, the guards between ...'. Does r126/r127 take a `formulate` round's `PARTIAL` out of it? Readings: (a) yes: it becomes 'continuations after `PARTIAL` other than a `formulate` round's questions'; (b) no: left as it is. Recommended: (a).

## Answers
- 2026-10-26: Neither reading: collapse instead (the person, 2026-10-26: "Collapse the delivery of q13"; observation 2026-10-26-outcome-and-lifecycle). work run decides every node's transition from how its session ended and what its result holds, never from the outcome label: (1) a session that ended in an error or at its turn limit, or left no result work run can read, is a fault, whatever its result says (this answers Q4: a crashed round's result is not read); (2) a clean end whose result gives questions sends them where its stage's questions go: a researcher's to the planner's brief, every other stage's under the node's ## Questions with the node set awaiting-answer; (3) a clean end with no question and the stage's output present makes the node's next transition; (4) a clean end with neither writes one question naming the missing output and sets the node awaiting-answer. Each stage names its output: research a fileset; plan a plan and a fileset; implement commits with its scenarios and the suite passing; review its findings; answer an answer; integrate and apply a change list; formulate a scenario for each requirement the proposal adds or changes; intake an outcome or a question on each line; gate its questions. These lines replace r3, r5, r45, r86, r87, r88, r115, r89, r90, r100, r112, r113 and r44's PARTIAL placeholder; r125, r126 and r127 are not added, and q13's three lines resolve to the new lines. The outcome label stays in results for reports only. Not yet loses 'continuations after PARTIAL'. Keep the split of the lifecycles from work run's mechanics out of this initiative.
- 2026-10-26: Neither reading: r86 and r87 are not exempted but replaced by the collapse's rules, and r127 is not added (the person, 2026-10-26: "Collapse the delivery of q13"; see the first answer).
