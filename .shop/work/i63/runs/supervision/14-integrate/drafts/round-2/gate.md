# Gate: supervision, round 2 (request q42)

Answer 2026-10-29 under the person's delegation of 2026-10-28: for r217, "another initiative" is one that `work run` is running side by side, as in r214 to r216.

## supervision

Draft: `.shop/scratch/14-integrate/drafts/round-2/spec/capabilities/supervision.md`

Removed (retired):
- [r217] **If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file. (replaced by r218)

Added:
- [r218] **If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file.

No glossary entry, no decision, no question.
