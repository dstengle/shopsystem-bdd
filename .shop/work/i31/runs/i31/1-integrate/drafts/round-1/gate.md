# Gate: i31, round 1 (request q8)

## supervision (`spec/capabilities/supervision.md`)

### Added Behaviour lines
- [r111] **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends.
- [r112] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions`.
- [r113] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`.
- [r114] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.
- [r115] **If** a round that `work run` started for one capability-proposal ends with an outcome other than `DONE`, **then** `work run` shall take the initiative's other nodes through their transitions before it exits with an error.

### Changed Behaviour lines
- [r83] now: **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`.
  was: **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `formulated`.

### Removed lines, glossary entries, decisions
None.

## Questions
1. r112/r113 against r86, r87, r88: what outcome does a `formulate` round that gives a question give?
   - (a, recommended) `DONE` with questions, as a researcher's may (r16): r86-r88 stand as they are.
   - (b) `QUESTION`: r86-r88 then forbid r113's transition, and each changes to begin "**If** a round of any kind ... other than a round of the kind `formulate` that gives a question, gives an outcome other than `DONE`, ..." with its response unchanged.
2. r70: when the questions a `formulate` round gave are answered, which round does `work run` start?
   - (a) an `apply` round, as r70 says today: no change.
   - (b, recommended) a `formulate` round: add [r116] "**When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers." and change r70 to "**When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers."
3. r115: only a capability-proposal's round ending with an outcome other than `DONE`, or every ending r86-r88 name?
   - (a, recommended) as the request gives it: r115 as drafted.
   - (b) every such ending: r115 becomes "**If** a round of any kind that `work run` started for a capability-proposal or an initiative gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error."
4. r112: a `formulate` round may give several questions (formulation r3). Does `work run` write each?
   - (a, recommended) yes: r112 becomes "**When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal's `## Questions`."
   - (b) r112 as drafted, in the request's words.

## Cut sentences
- q8's title "work run takes every node as far as it can go" (the intent of its lines, given by r111)
