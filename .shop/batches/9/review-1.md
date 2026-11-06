---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-9/review-1
kind: review
batch: batch-9
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/24
head: 020c9461b8d8204f962bccb82c3f28b71a4f23d1
range: 77465f122e57d951e9ee9fe079d3f7ad4c9ab6c9..020c9461b8d8204f962bccb82c3f28b71a4f23d1
result: fix-now
---

# batch-9 review 1

## Verdict

The batch builds b46, b30 and b37 and most of b36. Two findings need fixing before the merge. First, `work turn` can still post a comment that has no commit behind it, which breaks requests#r46 (b36). Second, `tools check` passes at the base but fails at the head (b30).

## Findings

### f1 Important fix now: `work turn` posts with no commit before it when the turn leaves the record unchanged
- item: b36
- where: scripts/request_post.py:120
`request_post.committed` makes the first commit only when `changed` is true. When nothing changed it skips that commit but still posts `posted` (lines 123-128), and only then commits the comment's URL.

`request_text.turned` returns the text unchanged in one case, at line 65 (r36): the upstream's turn on a request whose lines proposed are all settled and one of them is `accepted`. `work outcome` writes outcomes without changing the status, so this request can still be `open`. In that state `work turn` goes like this:
1. `turned` returns the record unchanged.
2. The record has an `issue`, so `turn_posting` gives a `Posting`.
3. No commit is attempted.
4. `gh issue comment` runs.
5. Only then does the commit of the URL fail in an uncommittable repository.

That is a comment on GitHub with no record behind it, which requests#r46 forbids for a request that is `open`. It is also the defect b36 was taken in to remove. The r46 scenario does not catch this because its request has no settled outcomes.

Fix: in this case, do not post until a commit is known to be possible. One way is to make the first commit even when the text is unchanged, for example a commit with no file changes. Another is to check committability before posting. Add a case to `tests/scripts/test_request_commit_first.py`: an `open` request whose single line is `accepted`, a pre-commit hook that fails, `work turn`, and no `gh issue` call.

### f2 Minor fix now: `tools check` fails at the head (ruff I001 in request_side.py)
- item: b30
- where: scripts/request_side.py:10
The run of `tools check --base 77465f12…` exits 1 at the head and 0 at the base:
```
scripts/request_side.py:10:5: I001 [*] Import block is un-sorted or un-formatted
```
The cause is the function-local `import request_moves      # request_moves calls this module` in `_own`. The same file also has three blank lines at lines 28-30, before `refuse_turn`. Fix: run `ruff --fix` on the file, or reformat the import and its comment so ruff accepts it, and remove the extra blank line.

### f3 Minor observation: no test fails without `refuse_reply`
- item: b30
- where: scripts/request_side.py:24
Commits e440280f and 39ecb13b say the r49 scenario "already passes at the batch base (a strict XPASS)". So the scenario is refused for some other reason, and passes whether or not `request_side.refuse_reply` exists. Nothing under `tests/` names `request_side` or its message `received from` (I searched for both). The new refusal on a received request in the asker's turn therefore has no test that would catch its removal. Hardening: add a script test that writes a received request (`upstream` this context, `asker` another) in the asker's turn, runs `work reply`, and checks the exit is 1 with the `received from` message.

### f4 Minor observation: requests' Implementation section still says accept is one commit and posts first
- item: b36
- where: spec/capabilities/requests.md:239
The Implementation bullets still describe the old order:
- line 239: `work accept` "sets the request `accepted` and posts the acceptance, one commit"
- lines 222-224: `work request` "opens the issue … and writes the record"

The change now commits the record first, posts after, and commits the URL in a second commit (put back in a third if GitHub refuses). The module map and `test_request_accept.py` were updated, but the capability's Implementation section was not. Fix: describe the commit-then-post order there.

### f5 Minor observation: an issue opened whose URL commit fails is left with a record that looks issue-less
- item: b36
- where: scripts/request_moves.py:369
In `request()`, if `open_issue` succeeds and the second commit then fails (the index lock taken in between, or a hook that has become refusing), the record stays committed without `issue:`. Every reader treats such a record as kept from before issues, so it "posts nothing", and the opened issue is orphaned. The `posted.close` path at `request_post.py:135` has a similar gap: if the close fails after the URL commit, the record is `refused` or `delivered` while the issue stays open. Neither state is in a line. Reproduction: make the hook refuse only the second commit of `work request`.
