# Gate, round 1 (q34)

## supervision

Added:
- [r179] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids and terms of the proposal that the round's change list does not name.

Changed: none. Removed: none. Glossary: none. Decisions: none.

## Questions

1. r179, "terms of the proposal": a capability-proposal lists requirement ids; terms are listed by a glossary-proposal. Reading A: keep the line as drafted, or split it into r179 (requirement ids of the capability-proposal) and r180 "**When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name." Reading B: drop "terms": r179 "...shall keep the requirement ids of the capability-proposal that the round's change list does not name." Recommended: A, split.
2. r179, "keep" the ids: Reading A: they stay in the proposal's `adds`, `changes` and `removes` that `work run` writes (r159, r145), line as drafted. Reading B: the apply round is also given the earlier round's drafts of the lines not named: "...`work run` shall give the round of the kind `apply` the kept drafts of the earlier round for each line the redraft's change list does not name." Recommended: A.
3. r145 (no change drafted) writes the proposal's lists "from the change list the round applied"; after a partial redraft that list lacks the kept ids. Change r145 to "from the change lists of every round of the kind `integrate` the round applied, the latest for each line", or is r179 enough? Nothing drafted.
4. r179, which redraft: Reading A: any round of the kind `integrate` started for a capability-proposal (r141, r150, r149) that redrafts a subset of its lines, as drafted. Reading B: only a redraft from answers (r142, r148). Recommended: A.

Cut sentences: 1 (the request's title, repeated by line 1).
