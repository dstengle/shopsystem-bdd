# Gate: supervision, round 1 (request q42)

All five questions answered 2026-10-29 under the person's delegation of 2026-10-28, recommended readings.

## supervision

Draft: `.shop/scratch/8-integrate/drafts/round-1/spec/capabilities/supervision.md`

Added:
- [r214] **When** `work run` checks what changed in the main checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side.
- [r215] **If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed, by a session of that initiative, while a session of one initiative worked, **then** `work run` shall put back no change of that path.
- [r216] **If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed, by a session of that initiative, while a session of one initiative worked, **then** `work run` shall fault no session for that change.
- [r217] **If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file.

Removed (retired):
- [r28] **If** the main checkout's `.shop/work/` differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file. (replaced by r217)

No glossary entry, no decision, no question.
