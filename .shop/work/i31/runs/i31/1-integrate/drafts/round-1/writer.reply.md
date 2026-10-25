/tmp/work-run-i31-na42kb62/i31-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | from |
|---|---|---|---|---|
| added | supervision | r111 | **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends. | q8 line 1: "When a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends." |
| added | supervision | r115 | **If** a round that `work run` started for one capability-proposal ends with an outcome other than `DONE`, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error. | q8 line 2: "If a round that `work run` started for one capability-proposal ends with an outcome other than `DONE`, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error." |
| added | supervision | r112 | **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions`. | q8 line 3: "When a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions` and transition the proposal to `awaiting-answer`." |
| added | supervision | r113 | **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`. | q8 line 3 (as above; split, one response a line, as r85/r69 are for the gate) |
| changed | supervision | r83 | new: **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`. old: **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `formulated`. | q8 line 3 (as above): a round that gives a question transitions the proposal to `awaiting-answer`, so r83 as written would make two transitions from one round |
| added | supervision | r114 | **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied. | q8 line 4: "When a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied." |

No glossary term added, changed or removed. No decision file.

## Questions

1. supervision r112/r113 against r86, r87, r88: what outcome does a `formulate` round that gives a question give?
   - (a, recommended) `DONE` with questions, as a researcher's may (r16): r86, r87 and r88 stand as they are.
   - (b) `QUESTION`: r86, r87 and r88 then forbid r113's transition, and each changes to begin "**If** a round of any kind that `work run` started for a capability-proposal or an initiative, other than a round of the kind `formulate` that gives a question, gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then ..." with its response unchanged.
2. supervision r70: when the questions a `formulate` round gave are answered, which round does `work run` start?
   - (a) an `apply` round, as r70 says today: no change.
   - (b, recommended) a `formulate` round: add "[r116] **When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers." and change r70 to "**When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers."
3. supervision r115: does it cover only a capability-proposal's round ending with an outcome other than `DONE`, or every ending r86-r88 name?
   - (a, recommended) as the request gives it: r115 as drafted.
   - (b) every such ending: r115 becomes "**If** a round of any kind that `work run` started for a capability-proposal or an initiative gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error."
4. supervision r112: a `formulate` round may give several questions (formulation r3, one for each line with two readings). Does `work run` write each of them?
   - (a, recommended) yes: r112 becomes "**When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal's `## Questions`."
   - (b) r112 as drafted, in the request's words.

## Cut sentences

- "work run takes every node as far as it can go" (q8's title: the intent of its lines, given by r111)
