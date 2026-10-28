/home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-integrate/.shop/scratch/3-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

supervision: adds r149, r150, r151, r152, r153; changes none; removes r140

| change | capability | id | line | quoted source |
|---|---|---|---|---|
| added | supervision | r149 | **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal." (request q22 line 1) |
| added | supervision | r150 | **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. | "**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal." (request q22 line 3) |
| added | supervision | r151 | **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied. | "**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied." (answer "r150 against r144-r146", the person, 2026-10-28) |
| added | supervision | r152 | **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status. | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status." (answer "r149 against r83") |
| added | supervision | r153 | **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output. | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output." (answer "r149 against r131/r132") |
| removed | supervision | r140 | **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. | answer "r150 against r140", reading (a): "Retire r140 and keep r150: supervision's frontmatter `retired` gets r140, and r140's scenario is deprecated for r150." |

Frontmatter: `retired` becomes [r3, r5, r16, r112, r113, r80, r114, r71, r140]; nothing else in it changes.

No glossary terms added, changed or removed. No decision files. Nothing drafted for spec-integration or formulation.

## Placement

- r150 and r151 stand where r140 stood, after r116 and before r141 (the apply round's answers its drafts do not hold, next to the new integrate round's lines r141-r143).
- r149, r152 and r153 follow r83 (the formulate round's end), in that order, before r86.
- Ids are one above r148 and above every id given for supervision by other initiatives' drafts (all below r148); none is reused.

## Questions

1. supervision, r152 against r83: both trigger when a formulate round formulates nothing for answers that change lines not in `spec/` and gives no question; r152 keeps the status, r83 sets `formulated`. (a) r152 is read as the exception and r83 stands as it is: no change. (b) Narrow r83: r83 retired and r154 **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question and having formulated its scenarios, `work run` shall transition the proposal to `formulated`.
2. supervision, r150/r151 against r144 and r145: the answer "r150 against r144-r146" chose r151 alone, so a partially applying apply round still transitions the proposal to `approved` (r144) and writes its `adds`, `changes` and `removes` (r145) while the new integrate round runs. (a) That is meant: no line. (b) Keep the status: r154 **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall keep the capability-proposal's status.

## Cut sentences

None. Every given line and answer lands in a Behaviour line or in the frontmatter's `retired`.
