---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-10/review-1
kind: review
batch: batch-10
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/25
head: 27005b2f84ea97251703b69ab4a90e352910e69d
range: 6a44cfb31b8e1d1efdfa14ecacfa4438eb43e9ef..27005b2f84ea97251703b69ab4a90e352910e69d
result: fix-now
---

# batch-10 review 1

## Verdict

The batch builds all seven lines of b55, b58, b35 and b47. Two findings on b55 need fixing before the merge. First, `tools check` fails at the head but passed at the base, on six ruff errors in the new `scripts/batch_driver.py`. Second, `work batch merged` and `abandon` now also delete the batch brief's folder, and no line or Implementation text asks for that.

## Findings

### f1 Important fix now: `tools check` fails on the new batch_driver.py (ISC004)
- item: b55
- where: scripts/batch_driver.py:20
`python3 scripts/tools check --base 6a44cfb3…` exits 1 at the head and exited 0 at the base. Its output:
```
scripts/batch_driver.py:20:5: ISC004 Unparenthesized implicit string concatenation in collection
scripts/batch_driver.py:25:5: ISC004 ...
scripts/batch_driver.py:28:5: ISC004 ...
scripts/batch_driver.py:33:5: ISC004 ...
scripts/batch_driver.py:94:13: ISC004 ...
scripts/batch_driver.py:99:13: ISC004 ...
Found 6 errors.
```
Lines 20, 25, 28 and 33 are entries of the `RULES` tuple. Lines 94 and 99 are entries of the `out` list in `text()` ("At `-> awaiting-merge`…" and "The pull request's URL…"). Each is two string literals joined only by sitting next to each other inside a collection. That is the pattern that hides a missing comma, and the repository's check refuses it. Fix: wrap each joined literal in its own parentheses, or join it explicitly, so that `tools check` exits 0.

### f2 Minor fix now: `merged` and `abandon` remove the batch brief's folder, which no line asks for
- item: b55
- where: scripts/batch_close.py:40
Commit 36fe5dfe adds this to `_remove_trees`:
```
shutil.rmtree(trees / ("%s-driver" % batch.name), ignore_errors=True)     # the batch brief (r14)
```
That deletes a file, which a person can see. But r14 only says `work batch start` writes and prints the brief. r15 and r16 only name review folders. The new Implementation bullet in `spec/capabilities/batches.md` says the brief is "never committed" and says nothing about removing it. The comment's citation of r14 is therefore wrong. The CLAUDE.md row for `batch_close.py` names only "worktrees, review folders". Fix: either say in batches' Implementation section (and in the `batch_close.py` row) that `merged` and `abandon` remove `batch-<n>-driver/`, or take the removal out.

### f3 Minor observation: r14's "print the batch brief" is built as printing its path, and CLAUDE.md and the skill disagree on which
- item: b55
- where: scripts/batch_start.py:148
r14 says `work` shall "print the batch brief". `said` prints `batch brief: <path>`, and the handler `prints_brief` checks only for the path. The new CLAUDE.md rule says the starting session dispatches the agent "with the batch brief it printed as its whole prompt". That reads as the brief's text. The SKILL says "the brief's path as its whole prompt". The path is a reasonable reading, but r14, CLAUDE.md and the SKILL should say the same thing. Suggest rewording the CLAUDE.md sentence to "the path of the batch brief it printed".

### f4 Minor observation: the batch brief ships rules from one person's own environment to every consumer
- item: b55
- where: scripts/batch_driver.py:30
`RULES` includes "Don't chain `cp` and `rm` in one shell command; keep shell variables few." It also includes the rule that leftover `.shop/worktrees/*` and `.claude/worktrees/` are never reference material. Both come from this person's session memory (shell approval prompts, leftover worktrees). The batch brief is written by the plugin in every consuming repository, so these rules reach repositories they were never meant for. The rule saying commits end with `Item:` and `Finding:` trailers is general and fine. Consider keeping environment-specific rules in a setting (`.shop/delivery.toml`) rather than in code.

### f5 Minor observation: a late `turn` comment on a closed request is now read as the asker's, and the test was moved off that case
- item: b35
- where: tests/scripts/test_request_flow.py:146
`poster()` decides who posted a `turn` from the record's own `turn`. A delivered request's turn is always `asker`. So on a closed request, a `turn` comment from the upstream holding a `question` now counts as a foreign entry and is not written. Before this batch it was written. `test_sync_writes_a_closed_requests_comment_and_prints_every_request` changed its comment from `step: turn` to `step: resolve` so that its assertion still holds. Only the test's setup changed and the assertion is the same, so this is not a weakened test. I checked whether the upstream can actually post that comment: `request_side` refuses `work turn` on the other side's turn, so the upstream cannot post such a `turn` through `work` today. It stays an edge for a hand-posted comment.

None of the other changes I checked showed a problem:
- `batch_review`'s own take-out still works after a park has already taken the lines out. `backlog_lines.unlay` writes nothing when the text is unchanged, and review commits only when `git status` shows a change.
- On r53, "side" is the request's `turn` attribute (`spec/index.md:203`), and `applied` stops setting it on a closed request.
- `features generate --check` exits 0, so the `.feature` changes are generated.
- The change is 21 files, +534 −33, within the 1000-line limit.
