# Gate, round 1 (q20, initiative i54)

## work-queue
- Added [r48] **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.
- Added [r49] **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status.
- Removed [r34] (retired; replaced by r49), it was: **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.

## supervision
- Added [r187] **When** a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds.

## Glossary: none. Decisions: none.

## Questions
1. work-queue r35 says `--json` makes `work list` print "each initiative, request and work-item", contradicting r49. Readings: (a) retire r35 and add r50 "**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object."; (b) keep r35, text and JSON differ. Recommended: (a). Answer (a) gives: remove r35, add r50.
2. supervision r159 (a `drafted` proposal for each capability the change list names) overlaps r187. Readings: (a) retire r159 and add r188 "**When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names for which the initiative holds no capability-proposal, with the requirement ids it adds, changes and removes on that capability."; (b) leave r159. Recommended: (a).
3. r187 wording: (a) verbatim as accepted; (b) matched to r159's form ("that `work run` started", "add to that proposal the requirement ids the change list adds, changes and removes on that capability, keeping the ids the proposal holds"). Recommended: (a).

Cut sentences: 3 (title; two history sentences of the delegation).
