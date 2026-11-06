---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-6/review-3
kind: review
batch: batch-6
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/21
head: 7d5c3613c1ca82ae7cda2fee4b109dcb9d002675
range: c886465279e847700eddb0bee7bcc7fb3dd94f22..7d5c3613c1ca82ae7cda2fee4b109dcb9d002675
result: clean
---

# batch-6 review 3

## Verdict

The fix closes f1. The kept file now holds only unreadable comments. r42 is retired, and r44 replaces it with a condition that leaves an unreadable comment out. The `## Implementation, may change` section has a `work watch` bullet, and the b31 bullet is gone from `## Not yet`. The tests now check that a readable unrecorded comment is printed by every watch. All runs exit 0, and the change is well under the size limit. Two leftover observations follow.

## Findings

### f4 Minor observation: an unreadable comment's line says `work sync` records it
- item: b31
- where: scripts/request_watch.py:86
`found` writes the same line for every comment a request does not hold: `"... (`work sync` records it)"`. Under r33, `work sync` prints an unreadable comment and never records it, so for an unreadable comment the line is wrong. A session that reads it will run `work sync` and expect the comment to be recorded, which never happens. `tests/scripts/test_request_watch.py:71` asserts this wording for the unreadable comment `#issuecomment-2`. Suggested fix: when `not is_readable(body)`, print a different ending, for example `(unreadable: `work sync` prints it, never records it)`, and change the test to match.

### f5 Minor observation: CLAUDE.md's module-map row for request_watch still says what it printed is kept
- item: b31
- where: CLAUDE.md:-
The row for `scripts/request_watch.py` says "each comment a request does not hold and each untaken ask printed once and the watch ended; what it printed kept in the git dir". The code now keeps only unreadable comments (`request_watch.py:100,106`), and readable comments and asks are printed by every watch. The module map is binding, so the row should say that only an unreadable comment is kept and printed once. This range did not change the row.

## Earlier findings
- f1: fixed
