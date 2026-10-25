## Budget
- skills/delivering-an-initiative/SKILL.md

## Changed
SKILL.md rewritten: it only starts `work run` (r4), drafts nothing from proposals, commits nothing of its own, starts no `claude -p` and merges no branch (r19, r20), drafts only a trial's fix (r10), puts a refused tool and a failed work-item / `work:` stop to the person as questions (r21, r22). Status named `awaiting-answer`. Formulated-proposal precondition, Drafting and Commit sections removed.

## Red/green
Guarantees-only work-item: no scenario, nothing red. `python3 -m pytest -q --work-item w141`: 142 passed, 1 skipped. Suite at start: 794 passed, 0 failed (with listed expected failures).
The plan contained no code.

## Tests changed under an allowance
none

## Open questions
- r21 cannot fire until `work run` prints a refused tool (notes D3, supervision).
- Exit code 0 "every work-item green" over an empty list (notes D1).
- Which proposal a trial's fix names for --part-of/--under is left as the invocation's placeholder.
- Whether `work run` refusing to start is an r22 question or r7 stop: left unchosen (shown as a `work:` stop, i.e. a question).
- Stale drafting lines in README.md (57, 149, 206, 229, 250), outside the file set.

## Size
`tools size --limit 300` printed nothing.

## Commits
36ecb74
