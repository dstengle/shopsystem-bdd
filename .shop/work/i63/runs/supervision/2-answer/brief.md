# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i63-i1lwhdly/supervision-2-answer
Branch: none (a detached checkout)
Question: Added lines (supervision): [r214] **When** `work run` checks what changed in the repository's own checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side. [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. Question 1: r215 against r28 (put back `.shop/work/` and fail the work-item when it differs at a worker's end), r6, r34. Readings: (a) RECOMMENDED: r215 is an exception to r28; r28 changes to: "**If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file." (b) r28 stays; r215 covers only sessions that are not workers: "**If** a path under another initiative's directory changed while a session of one initiative that is not a worker worked, **then** ..."
Delegation: The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /tmp/work-run-i63-i1lwhdly/supervision-2-answer/.shop/scratch/2-answer
Result file: /tmp/work-run-i63-i1lwhdly/supervision-2-answer/.shop/scratch/2-answer/result.json

You start in your worktree, /tmp/work-run-i63-i1lwhdly/supervision-2-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
