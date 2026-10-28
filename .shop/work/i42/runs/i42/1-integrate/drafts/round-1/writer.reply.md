/home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md
/home/vscode/shopsystem-bdd/.shop/worktrees/i42-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/spec-integration.md

## Change list

supervision: adds r149, r150; changes none; removes none

| change | capability | id | line | request sentence |
|---|---|---|---|---|
| added | supervision | r149 | **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal." (q22 line 1) |
| added | supervision | r150 | **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. | "**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal." (q22 line 3) |

spec-integration: adds r46; changes none; removes none

| change | capability | id | line | request sentence |
|---|---|---|---|---|
| added | spec-integration | r46 | **When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold. | "**When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold." (q22 line 2) |

Placement: r149 follows r83 (the formulate round's end), r150 follows r140, and r46 follows r39. No glossary terms are added, changed or removed. No decision files.

## Questions

1. supervision, r150 against r140 (possible duplicate): with spec-integration r46, an apply round that applies nothing also gives in its result each answer its drafts do not hold, so r150 already covers r140's case. (a) Retire r140 and keep r150: supervision's frontmatter `retired` gets r140, and r140's scenario is deprecated for r150. (b) Keep both: no change.
2. supervision, r150 against r144, r145 and r146: when an apply round applies some drafts and gives an answer they do not hold, r144 to r146 still fire ("having applied its drafts"), so the proposal becomes `approved` and a formulate round starts next to the new integrate round. (a) That is meant: no line. (b) It is not meant: r151 **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied. (c) As (b), and also keep the status: r152 **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall keep the capability-proposal's status.
3. supervision, r149 against r83: a formulate round that formulates nothing and gives no question would be set `formulated` by r83. (a) Keep the status instead: r151 **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status. (b) Let r83 apply: no line.
4. supervision, r149 against r131 and r132: a formulate round's output is "a scenario for each requirement its proposal adds or changes", so a round that formulates nothing would get a question about missing output (r131). (a) Treat it the way r147 treats the apply round: r151 **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output. (b) No line.
5. formulation, the counterpart of spec-integration r46: the request does not say how the formulate round reports that it formulated nothing because answers change lines not in `spec/`. (a) Add to formulation r24 **When** a round of the kind `formulate` is given answers that change lines not in `spec/`, `initiative-round` shall formulate nothing and give in its result each answer that changes them. (b) No line.

## Cut sentences

- "Answers that a formulate or a partial apply round cannot hold start a new integrate round" (the request's title; lines 1 to 3 cover it)
