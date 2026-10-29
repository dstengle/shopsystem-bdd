/tmp/work-run-i63-5pski_1g/i63-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source (request q42) |
|---|---|---|---|---|
| added | supervision | r214 | **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side. | Line 1: "**When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side." |
| added | supervision | r215 | **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. | Line 2: "**If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it." |

Capability supervision: adds r214, r215; changes none; removes none. Placed directly after r28, before r34. No glossary change, no decision, frontmatter unchanged.

Ids: the brief asked for r209 (line 1) and r210 (line 2), but supervision.md already uses r209, r210, r211, r212 and r213 in its Behaviour lines. Following the id rule (one above every id used or retired, and above the other initiatives' ids given, up to r208), the lines are numbered r214 (line 1) and r215 (line 2). Taking r209/r210 would give two lines each id.

## Questions

1. supervision r215 vs r28 (and r6, r34): r28 puts back the main checkout's `.shop/work/` and fails the work-item when it differs at a worker's end. Readings:
   (a) r215 is an exception to r28. Paths of another initiative are left out of r28's check, and r28 becomes, as a changed line: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file." (recommended: this matches line 1 and the request's title).
   (b) r28 stays as it is and r215 covers only sessions that are not workers (integrate, gate, apply, formulate, intake rounds and answering sessions). Then r215 becomes: "**If** a path under another initiative's directory changed while a session of one initiative that is not a worker worked, **then** ...".
2. supervision r215 vs r6/r34: "changed" does not say who made the change. Readings:
   (a) Changed by another initiative's sessions running side by side. r6 and r34 still apply when the session itself writes into another initiative's directory, and r215 reads "**If** a path under another initiative's directory changed, by a session of that initiative, while a session of one initiative worked, **then** ..." (recommended).
   (b) Changed by anyone, including the session itself. r6 and r34 then need the same exception for paths under another initiative's directory.
3. supervision r215: "another initiative's directory" could mean any other initiative's, or only one `work run` is running side by side (line 1's scope). Readings:
   (a) Only one running side by side: "**If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed while ..." (recommended, consistent with r214).
   (b) Any other initiative: the line as drafted.
4. supervision r215 has two responses ("put back no change" and "fault no session"). The strict form allows one response a line. Readings:
   (a) Split it into two lines: "**If** ..., **then** `work run` shall put back no change of that path." and "**If** ..., **then** `work run` shall fault no session for that change." (recommended).
   (b) Keep one line, as the request words it.
5. supervision r214: "the repository's own checkout" is the "main checkout" of r28 and r46. Should r214 say "the main checkout" (recommended), or keep the request's wording? No glossary term names either one.

## Cut sentences

- "An answering session is faulted for another initiative's changes" (the request's title: it describes the problem the lines fix and is not a rule).
