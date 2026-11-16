# Release 0.35.2, part 2: batches 41 and 42, and b300's regression fixed

The first plan (plan.md in this folder) was carried out on `plan-release-0.35.2`, and its review (the record 2026-11-16-release-review-0-35-2, to be written beside this one) found that b300 made `model parse` refuse "every K in the Y, ordered by T" after a verb whose frame names K, a line 0.35.1 read: a regression, which would make the release 0.36.0. The release was held. b328 fixed it in batch-42 (PR #64), so 0.35.2 stays a z release. The release now also ships batch-41 (PR #63) and batch-42 (PR #64):

- b65: `work shape` refuses an idea with no shaping note and no `--note`; `work backlog` shows such an idea as needing a note;
- b77: the readiness bar refuses an item whose group shares its condition and trigger with another group (v15n);
- b6: `work batch merged` resolves the accepted request an item was taken in from;
- b286: `features generate` brings in by a Given the thing a printed thing holds;
- b328: "every K in the Y, ordered by T" after a verb whose frame names K reads one way (the order on the Ks);
- b39: `work show` prints a line's reason; `work sync` records an unreadable comment and prints it once; `offer`, `propose`, `reply` and `turn` print a one-line confirmation; `work request --from` is optional;
- b40: `work offer --capability` quotes the capability's requirements and only the terms they mention; an offer with no `--capability` posts no glossary;
- b52: `work quote` finds a message the person sent mid-turn.

## Tasks, on the same branch, after merging main into it

1. **Merge main** into `plan-release-0.35.2` (a merge commit). Resolve any conflict in favour of main's code and the branch's release text.
2. **Check the bump again.** `git diff v0.35.1 HEAD -- features/`: name any scenario that existed at v0.35.1 and changed. b286 and b39 may change the steps of existing lines' scenarios (a new Given, a retired requests#r77): say for each whether a consuming repository's handlers must change, and if so that it is in the Upgrading bullet. Check that the line of the review's finding 1 (in a copy of grammar/corpus/constructs/spec, "When the person runs `work start` on a worktree, `work` shall give every file in the worktree, ordered by version, in ascending order to the person.") parses to one meaning with HEAD's scripts.
3. **CHANGELOG.md's 0.35.2 section**: its title names the release's whole content; one bullet per item above with its PR, in the section's voice; the b300 bullet says "every K in the Y, ordered by T" reads with the order on the Ks (b328). Upgrading: no upgrade step; regenerate features; `work shape` now needs a note on an idea that has none; an offer with no `--capability` posts no glossary.
4. **docs/upgrading.md** "From 0.35.1 to 0.35.2" says the same.
5. **b332's text**: `skills/taking-in-a-request/SKILL.md` step 2 and `docs/reference/commands.md` (`work offer`: it quotes each named capability's requirements and the terms they mention, no glossary without `--capability`; `work request --from`: optional, defaulting to this context, and the `internal` value), `docs/reference/commands.md` and any docs page showing `work shape` on an idea with no note (b329), and CLAUDE.md's module-map rows of request_sync.py, request_view.py, request_steps.py and conversation_read.py, readiness_bar.py (b77's v15n, b307's unread, b305 not yet), backlog_moves.py and backlog_view.py (b65), batch_close.py (b6), spec_steps4_boxes.py (b286) (b330). Withdrawing b329, b330 and b332 is the session's after the merge.
6. **Checks** as plan.md's task 6, plus the docs tests. Commit messages end with `Release: 0.35.2`.
