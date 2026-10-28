# Gate, integrate round 1 (q32)

## work-queue (adds r42, r43, r44, r45; Purpose gains one clause)
- [r42] **When** the person approves drafted lines at a gate that a session keeps, `work` shall write a capability-proposal for each capability the drafts change, with the requirement ids it adds, changes and removes.
- [r43] **When** the drafts that the person approves at a gate a session keeps change the glossary, `work` shall write a glossary-proposal with the terms the drafts add, change and remove.
- [r44] **When** `work` writes a proposal from a gate that a session kept, `work` shall write the proposal as `approved` and log each of its transitions, naming the gate and the commit that applied its drafts.
- [r45] **When** `work` writes the first proposal of a `proposed` initiative from a gate that a session kept, `work` shall transition the initiative to `started`.

## spec-integration (adds r56)
- [r56] **When** a session keeps the gate of an initiative, `integrating-a-proposal` shall hand the approved drafts to `work run` through `work`, writing no proposal file by hand.

## Glossary
No term added, changed or removed. No decision drafted.

## Questions
1. r42, r43: the trigger is the person's approval, which `work` cannot see; the command a session runs to hand over is not given. Reading A: a command `work <cmd>` given the drafts path and approval; r42 would read "**When** `work <cmd>` is run with drafts the person approved at a gate a session keeps, ..." (command name an Implementation line). Reading B: keep as drafted. 
2. r44, where the log goes. Reading A: the initiative's `log.jsonl` (as r5): "...append a line to `.shop/work/<initiative>/log.jsonl` for each of its transitions, naming the gate and the commit..." Reading B: the ledger.
3. r44, which transitions: Reading A: one transition into `approved`; line stands. Reading B: each status a gate goes through (`drafted`, `awaiting-answer`, `approved`): "...log the transitions `drafted`, `awaiting-answer` and `approved`, each naming the gate and the commit...".
4. Whether `work` commits the proposals it writes (as r25, r20). If yes: [r46] **When** `work` writes a proposal from a gate that a session kept, `work` shall commit the proposal and its log on the current branch.
5. r56, "through `work`". Reading A: "...shall give the approved drafts to `work`, writing no proposal file by hand." Reading B: as drafted.
6. supervision: what `work run` does next with an `approved` proposal written from a session's gate. If it should formulate: [r183] **When** a capability-proposal is `approved` and `work` wrote it from a gate that a session kept, `work run` shall start a round of the kind `formulate` for the proposal (above supervision#r182).
7. Lines 3 and 4 of the request say "move", which the glossary lists after `Not:` under transition; drafted as "transition". Keep, or change the glossary entry.
