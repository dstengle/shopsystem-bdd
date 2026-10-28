/tmp/work-run-i48-e5iyn77g/i48-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | supervision | r179 | **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name. | q34 line 1: "**When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name." |

Glossary: no term added, changed or removed.

Decisions: none.

## Questions

1. supervision r179, "terms of the proposal": a capability-proposal lists requirement ids, and terms are listed by a glossary-proposal (glossary, glossary-proposal). Reading A, the terms of the initiative's glossary-proposal that the round's change list does not name are kept as well: keep the line as drafted, or split it into r179 "...shall keep the requirement ids of the capability-proposal that the round's change list does not name." and r180 "**When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name." Reading B, "terms" refers to nothing separate and is dropped: r179 "...shall keep the requirement ids of the capability-proposal that the round's change list does not name." Recommended: A, split into two lines, because a glossary-proposal is the only thing that lists terms.
2. supervision r179, "keep" the ids: Reading A, they stay in the capability-proposal's `adds`, `changes` and `removes` that `work run` writes (r159 and r145), the line as drafted. Reading B, the redrafted round's drafts are also taken with the earlier round's drafts of the lines not named, so the apply round gets both: "...`work run` shall give the round of the kind `apply` the kept drafts of the earlier round for each line the redraft's change list does not name." Recommended: A, which is what the request's sentence says.
3. supervision r145 (no change drafted): r145 writes the proposal's `adds`, `changes` and `removes` "from the change list the round applied". After a partial redraft, that change list leaves out the ids r179 keeps. Does r145 need to change to "...from the change lists of every round of the kind `integrate` the round applied, the latest for each line"? Or is r179 enough as written? The request does not strictly require the change, so nothing is drafted.
4. supervision r179, which redraft: Reading A, any round of the kind `integrate` that starts for a capability-proposal (r141, r150, r149) and redrafts a subset of its lines, the line as drafted. Reading B, only a redraft from answers (r142, r148): "**When** a round of the kind `integrate` drafts some of the lines of a capability-proposal anew from its answers, ...". Recommended: A.

## Cut sentences

- "A redraft of some of a proposal's lines keeps its other ids" (the request's title, said again by line 1).
