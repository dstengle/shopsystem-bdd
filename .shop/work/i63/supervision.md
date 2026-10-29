---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i63-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i63
status: drafted
argues: [supervision]
date: 2026-10-29
adds: [supervision#r214, supervision#r215, supervision#r216, supervision#r217]
changes: []
removes: [supervision#r28]
---

# supervision

The drafts of this proposal are in .shop/work/i63/runs/supervision/8-integrate/drafts/round-1/.

## Questions
- Added lines (supervision):
  [r214] **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side.
  [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it.
  
  Question 1: r215 against r28 (put back `.shop/work/` and fail the work-item when it differs at a worker's end), r6, r34. Readings: (a) RECOMMENDED: r215 is an exception to r28; r28 changes to: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file." (b) r28 stays; r215 covers only sessions that are not workers: "**If** a path under another initiative's directory changed while a session of one initiative that is not a worker worked, **then** ..."
- Line:
  [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it.
  
  Question 2: r215 does not say who made the change. Readings: (a) RECOMMENDED: changed by another initiative's session running side by side; r6 and r34 still apply when the session itself writes there: "**If** a path under another initiative's directory changed, by a session of that initiative, while a session of one initiative worked, **then** ..." (b) changed by anyone, the session itself included; r6 and r34 then need the same exception.
- Line:
  [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it.
  
  Question 3: "another initiative's directory" in r215. Readings: (a) RECOMMENDED: only an initiative `work run` is running side by side: "**If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed while ..." (b) any other initiative: r215 as drafted.
- Line:
  [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it.
  
  Question 4: r215 gives two responses. Readings: (a) RECOMMENDED: two lines: "**If** ..., **then** `work run` shall put back no change of that path." and "**If** ..., **then** `work run` shall fault no session for that change." (b) one line, as the request words it.
- Line:
  [r214] **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side.
  
  Question 5: r214 says "the repository's own checkout"; r28 and r46 say "the main checkout". Readings: (a) RECOMMENDED: r214 says "the main checkout". (b) r214 keeps the request's wording.

## Answers
- 2026-10-29: Reading (a), under the person's delegation of 2026-10-28 ("I take recommendations"): r215 is an exception to r28, and r28 changes to: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file."
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- 2026-10-29: The person's delegation (2026-10-28) takes the recommendation: reading (a), so r215 reads "If a path under another initiative's directory changed, by a session of that initiative, while a session of one initiative worked, then work run shall put back no change of that path and fault no session for it", and r6 and r34 still apply when the session itself writes there.
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- 2026-10-29: Reading (a), the recommended one, under the person's 2026-10-28 delegation ("I take recommendations"): r215 covers only a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side.
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- 2026-10-29: Reading (a), the recommended one: two lines, 'If a path under another initiative's directory changed while a session of one initiative worked, then work run shall put back no change of that path.' and 'If ..., then work run shall fault no session for that change.' (The person's delegation, 2026-10-28: 'I take recommendations'.)
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- 2026-10-29: (a) r214 says "the main checkout".
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
