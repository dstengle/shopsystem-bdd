# Gate: i63, round 1 (request q42)

Draft: `.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md`. No glossary entry, no decision, no changed or removed line.

## supervision, added (after r28)

- [r214] **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side.
- [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it.

(The ids are r214 and r215, not r209 and r210: r209 to r213 are already used in `supervision.md`.)

## Questions

1. r215 against r28 (put back `.shop/work/` and fail the work-item when it differs at a worker's end), and r6, r34. Readings:
   (a) r215 is an exception to r28; r28 changes to: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file." (recommended)
   (b) r28 stays; r215 covers only sessions that are not workers: "**If** a path under another initiative's directory changed while a session of one initiative that is not a worker worked, **then** ..."
2. r215 does not say who made the change. Readings:
   (a) Changed by another initiative's session running side by side; r6 and r34 still apply when the session itself writes there: "**If** a path under another initiative's directory changed, by a session of that initiative, while a session of one initiative worked, **then** ..." (recommended)
   (b) Changed by anyone, the session itself included; r6 and r34 then need the same exception.
3. "another initiative's directory" in r215. Readings:
   (a) Only an initiative `work run` is running side by side: "**If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed while ..." (recommended)
   (b) Any other initiative: r215 as drafted.
4. r215 gives two responses. Readings:
   (a) Two lines: "**If** ..., **then** `work run` shall put back no change of that path." and "**If** ..., **then** `work run` shall fault no session for that change." (recommended)
   (b) One line, as the request words it.
5. r214 says "the repository's own checkout"; r28 and r46 say "the main checkout". Readings:
   (a) r214 says "the main checkout" (recommended).
   (b) r214 keeps the request's wording.
