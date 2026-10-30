# supervision, formulate round 1: reply

## Coverage

| id | line | scenario |
|---|---|---|
| r188 | "**When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids of the proposal that the round's change list does not name." | an integrate round started for a capability-proposal that redrafts some of its lines leaves the proposal holding the requirement ids its change list does not name |
| r189 | "**When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name." | an integrate round started for a glossary-proposal that redrafts some of its terms leaves the proposal holding the terms its change list does not name |

Every other Behaviour line already has its scenario in features/supervision.feature; none was changed.

## Questions

None. Neither line admits two readings.

## Cases no line mentions (no scenario written)

- No Behaviour line says when `work run` starts a round of the kind `integrate` for a glossary-proposal (r150, r141 and r142 name only a capability-proposal), so r189's scenario takes such a round as given ("a round of the kind integrate is started for g1") rather than from a trigger.
- r188 and r189 do not say which list a kept id or term stays in. The scenarios take it that each stays in the list it was in (adds, changes or removes).
- A redraft that drops a line or term altogether. The change list does not name it, so r188 and r189 keep it in the proposal even though the new drafts no longer hold it. No line says how such an id or term leaves the proposal.
- A change list that names an id or term the proposal held in a different list, for example in `adds` before and in `changes` now. No line says whether the earlier entry is replaced or kept alongside the new one.
- A redraft that ends in questions rather than DONE. No line says whether the ids or terms the round did not name are still kept.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-9-formulate/.shop/scratch/9-formulate/drafts/round-1/features/supervision.feature
