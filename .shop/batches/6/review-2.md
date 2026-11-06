---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-6/review-2
kind: review
batch: batch-6
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/21
head: c886465279e847700eddb0bee7bcc7fb3dd94f22
range: 6f0a50d5b836dc82b26bc9ff6ca75a75e5e8f1ec..c886465279e847700eddb0bee7bcc7fb3dd94f22
result: fix-now
---

# batch-6 review 2

## Verdict

The fix brings back r42 and r43 for readable comments and untaken asks, adds the `work watch` Implementation bullet and takes the b31 bullet out of `## Not yet`. It still goes against r42 for an unreadable comment, so f1 stays open.

## Findings

None.

## Earlier findings
- f1: not fixed: the fix keeps the de-duplication for unreadable comments, and r42 has no exception for them. The `unrecorded` term (spec/capabilities/requests.md:39) means a comment the request does not yet hold. Per the Implementation section, `work sync` "prints and never records" an unreadable comment, so that comment stays unrecorded for good. r42 says "While a comment is unrecorded, when a session runs `work watch`, `work` shall print the comment and exit successfully". In scripts/request_watch.py:86, a later watch still passes over a kept unreadable URL, `if not (bad and url in before)`, and so exits 1 with `--polls` and polls forever without it. The new test asserts that the line is broken: tests/scripts/test_request_watch.py:179-181 (`again.returncode == 1 and again.stdout == ""`). This is the "or the comment is unreadable" case f1 named. The new Implementation bullet (requests.md:228-230) only describes the exception, and an Implementation section cannot override a requirement line. Fix on b31's branch, one of two ways. (a) Retire r42 into `retired:` and write a new line whose condition leaves out a comment that is unreadable, or one an earlier watch already printed (requirements-retired-never-edited). (b) Drop the kept file, so every watch prints every unrecorded comment, and make the test assert that.
