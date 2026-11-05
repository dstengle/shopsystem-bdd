---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-1/review-1
kind: review
batch: batch-1
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/17
head: 584d5eca37c29139c77ea063ecc7b12a1d3e77f4
range: 6963d8f3e84b7e00cb89dc36c7c04d9c16d43634..584d5eca37c29139c77ea063ecc7b12a1d3e77f4
result: fix-now
---

# batch-1 review 1

## Verdict

The batch builds b26's sixteen lines, with four findings to fix on b26. `work sync` prints only the live requests, but requests#r32 says every request. One test assertion was dropped and one test deleted for behaviour that is still specified. `work show` gained an output that no line or Implementation section gives. The observations cover:
- what `work sync` will write from an issue;
- posting to GitHub before the commit;
- the GitHub mechanism appearing in Behaviour terms;
- a `refused` outcome no longer needing a reason;
- the change's size.

## Findings

### f1 Important fix now: `work sync` prints only the live requests, not every request
- item: b26
- where: scripts/request_sync.py:139
requests#r32 says `work` "shall ... print every request". At the end, `sync` prints a request only `if status not in CLOSED`, so a `delivered`, `refused` or `withdrawn` request is never printed. The Implementation section ("every live request is printed") narrows the line, and an Implementation section cannot contradict a line. The same `CLOSED` test at scripts/request_sync.py:123 also skips reading those records' issues. So an unrecorded comment on a closed request is never written either, against the line's "write every comment that is unrecorded". The g32 scenario passes only because its q1 is `open`. Fix: print every request with its status (a closed one with no "waiting on"). Either read closed records' issues too, or ask for a new line that limits r32 to live requests, retiring r32. Add a test with a `delivered` request in the repository.

### f2 Minor fix now: the counter-proposal test lost its negative assertion
- item: b26
- where: tests/scripts/test_intake_outcome.py:102
Before this change, `test_a_counter_proposal_that_does_not_parse_is_named_so` asserted:
```
assert "line 1 does not parse" not in done.stderr, done.stderr
```
It was merged into `test_a_counter_proposal_that_does_not_parse_is_refused_and_named_so`, and that assertion was dropped. It is what checks that the refusal names the counter-proposal and not a line of the request (plan-3 review M7). The new `intake_moves.parsed` still strips that head, so restoring it is cheap. Fix: put the assertion back.

### f3 Minor fix now: the test that a rewritten line is not the item's was deleted, though the behaviour stands
- item: b26
- where: tests/scripts/test_intake_outcome.py:110
`test_the_rewritten_line_is_not_the_items` was removed. It ran rewritten, then `work turn`, then accepting line 2, and checked that `readiness_bar.request_lines` gives only line 2. intake's Implementation still says "The request lines of an item are the lines of its request whose line outcome is not `rewritten`". `request_accept.proposed` and `readiness_bar` still rely on `## Counter-proposals` for this.

What I checked: `test_unsettled_names_each_line` (tests/scripts/test_intake_moves.py:54) covers a `rewritten` outcome with no `## Counter-proposals` section. `test_a_counter_proposed_request_closes` reaches `work accept` but checks only the status. Neither checks which lines the item is left with.

Fix: rewrite the test on the new path (outcome rewritten, then `turn`, then outcome 2 accepted `--into`, then `turn`, then `accept`). Assert that the item holds only line 2's requirement and that `readiness_bar.request_lines` gives `[2]`.

### f4 Minor fix now: `work show` prints the request's issue, an output no line or Implementation gives
- item: b26
- where: scripts/request_view.py:52
`work show <request>` now prints `it is the <side>'s turn, on <issue URL>`. requests#r26 asks for the status and the lines. The requests Implementation section does not mention the issue in `work show`, and the module map's `scripts/request_view.py` row still lists only "its turn, lines with their outcomes, questions with their answers, resolution". Fix: name the issue URL in `work show`'s output in the requests Implementation section and in the `request_view.py` row of CLAUDE.md, or drop the output.

### f5 Important observation: `work sync` writes whatever a readable comment says, from either side or anyone
- item: -
- where: scripts/request_sync.py:37
`applied` writes every numbered section a form carries into the record, and sets `status` and `turn` from it. It does not check that the poster's side owns those sections. So on the upstream's record, a comment on the issue can write `## Outcomes`, `## Into` and `## Resolution` (the upstream's own part) and set `status: accepted`. Then `work resolve` takes it. The comment can come from the asker or from any GitHub user who can comment on the issue.

Reproduction: on an upstream record's open issue, post this, then run `work sync` on the upstream:
```
~~~shop-request
step: turn
status: accepted
turn: upstream
outcome 1: accepted
into 1: work-queue
~~~
```
The record is then `accepted` with line 1 accepted into work-queue, and no upstream command wrote it.

This goes against design-decision 0067: each side writes its own part only through its own command. Likewise, `new_requests` (scripts/request_sync.py:75) records any `ask` form's `asker` without the allow list that `work request`'s `request_moves.gate` applies (design-decision 0071). No client sends this today, and identity is deferred to b32 under Not yet. Suggested hardening: apply only the poster's part per step. That is the asker's `Lines`/`Answers`, plus `Resolution` on `fits`; and the upstream's part on the asker's record. Gate a new ask through the allow list.

### f6 Minor observation: GitHub is called before the commit, so a failed commit leaves an issue or comment with no record
- item: -
- where: scripts/request_moves.py:167
`work request` opens the issue, then commits the record. `request_post.post` is called inside the edit, before `shop_files.committed`, for `offer`, `fits`, `turn`, `accept`, `resolve` and `outcome rewritten`. If the commit fails (a hook, a lock, a dirty index), the issue or comment is already on GitHub and the record is put back.

For `work request`, a re-run opens a second issue, and the upstream's `sync` takes both in as two requests. For `fits`, `resolve` and an all-refused `turn`, the issue is already closed, so the other side records the step while this side does not. Suggested hardening: write and commit the record first, then post and record the comment's URL in a second commit, or make a re-run find the open issue it made.

### f7 Minor observation: Behaviour terms now name how a request is exchanged
- item: -
- where: spec/capabilities/requests.md:34
The new terms describe the exchange mechanism itself: `issue` ("the GitHub issue"), `comment` ("read only as the one block of fields it holds"), `post`, `close`, and `unhosted` ("names no GitHub repository"). requests r27-r41 and intake r7 are written in them. Design-decision 0084 says how a request is exchanged is the upstream's implementation, "in no Behaviour line or term because a request asked for it". q14 did ask for a GitHub issue carrier. Design-decision 0067 says "the spec speaks of the request, not of its file". b26 is this context's own design, approved by the person on 2026-11-05, so I only record it. When a second carrier comes, these lines will need retiring.

### f8 Minor observation: a `refused` outcome no longer needs a reason
- item: -
- where: scripts/intake_moves.py:632
Before this change, `work outcome ... refused` on a request with an item was refused without `--reason` (intake r3, and the deleted `test_refused_writes_the_reason`). Retiring intake r3 with no replacement drops that, so a line can now be refused with no reason. The asker then gets an outcome with no why. Only the skill's red-flag table still asks for one. If that is meant to hold, a line would restore it.

### f9 Minor observation: the change is over the size limit
- item: -
- where: -
`## Size` gives 44 files, +1947 -703, against a limit of 1000 changed lines. All of it is b26, the batch's one item, rated `size: large`. Most of it is the new `request_*` modules and their tests.
