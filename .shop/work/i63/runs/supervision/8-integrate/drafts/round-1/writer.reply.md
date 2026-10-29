/tmp/work-run-i63-i1lwhdly/supervision-8-integrate/.shop/scratch/8-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list
added | supervision | r214 | **When** `work run` checks what changed in the main checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side. | answer approved under the person's delegation, 2026-10-28, "I take recommendations"
added | supervision | r215 | **If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed, by a session of that initiative, while a session of one initiative worked, **then** `work run` shall put back no change of that path. | answer approved under the person's delegation, 2026-10-28, "I take recommendations"
added | supervision | r216 | **If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed, by a session of that initiative, while a session of one initiative worked, **then** `work run` shall fault no session for that change. | answer approved under the person's delegation, 2026-10-28, "I take recommendations"
added | supervision | r217 | **If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file. | answer approved under the person's delegation, 2026-10-28, "I take recommendations" (replaces r28)
removed | supervision | r28 | **If** the main checkout's `.shop/work/` differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file. | replaced by r217; r28 added to `retired`

No glossary terms added, changed or removed. No decision files.

## Questions
None.

## Cut sentences
None.
