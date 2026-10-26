# Gate, round 1: supervision

## Added Behaviour lines (supervision)
- [r125] **When** `work run` writes the brief of a round of the kind `formulate`, `work run` shall tell the round that a round that has formulated every line with one reading and gives each other line as a question has done its work, with the outcome `DONE`.
- [r126] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall write each question its result gives under the proposal's `## Questions`.
- [r127] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall transition the proposal to `awaiting-answer`.

No changed or removed lines. No glossary entries. No decisions.

## Questions
1. r126/r127 against r112/r113: new lines or changes? Drafted as new lines, r112 and r113 left as they are. If "change": drop r126 and r127; r112 becomes "...gives questions, with the outcome `DONE` or `PARTIAL`, ..." and r113 "...gives a question, with the outcome `DONE` or `PARTIAL`, ...".
2. r86 and r87 (keep status, make no transition on an outcome other than `DONE`) conflict with r127. Exempt a `formulate` round that gives a question with the outcome `PARTIAL` from r86 and r87? If no, r127 cannot hold (drop it, and r126 with it or keep r126 alone).
3. r88 and r115 (exit with an error naming the round): does `work run` still exit with an error for a `formulate` round that gives a question with `PARTIAL`? If no, r88 and r115 take the same exemption and the proposal waits like any `awaiting-answer` node (r81/r32/r101 decide the exit). If yes, they stay.
4. A `formulate` round that ends in an error or at its turn limit but whose result gives a question with `PARTIAL`: do r126/r127 hold then too? If yes, the exemptions read "other than a round of the kind `formulate` whose result gives a question with the outcome `PARTIAL`". If no, r126 and r127 gain "ends neither in an error nor at its turn limit and".
5. "Not yet" lists "continuations after `PARTIAL`": does r126/r127 take a `formulate` round's `PARTIAL` out of it? If yes, it becomes "continuations after `PARTIAL` other than a `formulate` round's questions".

Recommended: 1 new lines; 2 yes; 3 no; 4 no (the exemption only for rounds that ended normally); 5 yes.
