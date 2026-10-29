# gate of supervision

Capability-proposal: .shop/work/i63/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r214, supervision#r215, supervision#r216, supervision#r217
Changes: none
Removes: supervision#r28
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i63/runs/supervision/8-integrate/drafts/round-1/
Base: db2873b73a08e86a12a10f8de97aae3b22914af6
Worktree: /tmp/work-run-i63-i1lwhdly/supervision-9-gate
Branch: round/supervision-9-gate
Answers the person gave, each with the question it answers:
- Question: Added lines (supervision): [r214] **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side. [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. Question 1: r215 against r28 (put back `.shop/work/` and fail the work-item when it differs at a worker's end), r6, r34. Readings: (a) RECOMMENDED: r215 is an exception to r28; r28 changes to: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file." (b) r28 stays; r215 covers only sessions that are not workers: "**If** a path under another initiative's directory changed while a session of one initiative that is not a worker worked, **then** ..."
  Answer: 2026-10-29: Reading (a), under the person's delegation of 2026-10-28 ("I take recommendations"): r215 is an exception to r28, and r28 changes to: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file." by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- Question: Line: [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. Question 2: r215 does not say who made the change. Readings: (a) RECOMMENDED: changed by another initiative's session running side by side; r6 and r34 still apply when the session itself writes there: "**If** a path under another initiative's directory changed, by a session of that initiative, while a session of one initiative worked, **then** ..." (b) changed by anyone, the session itself included; r6 and r34 then need the same exception.
  Answer: 2026-10-29: The person's delegation (2026-10-28) takes the recommendation: reading (a), so r215 reads "If a path under another initiative's directory changed, by a session of that initiative, while a session of one initiative worked, then work run shall put back no change of that path and fault no session for it", and r6 and r34 still apply when the session itself writes there. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- Question: Line: [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. Question 3: "another initiative's directory" in r215. Readings: (a) RECOMMENDED: only an initiative `work run` is running side by side: "**If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed while ..." (b) any other initiative: r215 as drafted.
  Answer: 2026-10-29: Reading (a), the recommended one, under the person's 2026-10-28 delegation ("I take recommendations"): r215 covers only a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side. by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- Question: Line: [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. Question 4: r215 gives two responses. Readings: (a) RECOMMENDED: two lines: "**If** ..., **then** `work run` shall put back no change of that path." and "**If** ..., **then** `work run` shall fault no session for that change." (b) one line, as the request words it.
  Answer: 2026-10-29: Reading (a), the recommended one: two lines, 'If a path under another initiative's directory changed while a session of one initiative worked, then work run shall put back no change of that path.' and 'If ..., then work run shall fault no session for that change.' (The person's delegation, 2026-10-28: 'I take recommendations'.) by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."
- Question: Line: [r214] **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side. Question 5: r214 says "the repository's own checkout"; r28 and r46 say "the main checkout". Readings: (a) RECOMMENDED: r214 says "the main checkout". (b) r214 keeps the request's wording.
  Answer: 2026-10-29: (a) r214 says "the main checkout". by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's."

Read (paths in your worktree):
- .shop/work/i63/supervision.md
- .shop/work/i63/runs/supervision/1-gate
- .shop/work/i63/runs/supervision/2-answer
- .shop/work/i63/runs/supervision/3-answer
- .shop/work/i63/runs/supervision/4-answer
- .shop/work/i63/runs/supervision/5-answer
- .shop/work/i63/runs/supervision/6-answer
- .shop/work/i63/runs/supervision/7-apply
- .shop/work/i63/runs/supervision/8-integrate
- .shop/work/i63/runs/supervision/8-integrate/drafts/round-1/

Run directory: /tmp/work-run-i63-i1lwhdly/supervision-9-gate/.shop/scratch/9-gate
Result file: /tmp/work-run-i63-i1lwhdly/supervision-9-gate/.shop/scratch/9-gate/result.json

You start in your worktree, /tmp/work-run-i63-i1lwhdly/supervision-9-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
