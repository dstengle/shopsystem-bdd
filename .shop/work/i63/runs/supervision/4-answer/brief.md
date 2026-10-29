# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i63-i1lwhdly/supervision-4-answer
Branch: none (a detached checkout)
Question: Line: [r215] **If** a path under another initiative's directory changed while a session of one initiative worked, **then** `work run` shall put back no change of that path and fault no session for it. Question 3: "another initiative's directory" in r215. Readings: (a) RECOMMENDED: only an initiative `work run` is running side by side: "**If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed while ..." (b) any other initiative: r215 as drafted.
Delegation: The person, 2026-10-28: "i am delegating to you", "I take recommendations" and "Please do what is necessary to get the system back into working condition": answer every question with its recommended reading. Questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /tmp/work-run-i63-i1lwhdly/supervision-4-answer/.shop/scratch/4-answer
Result file: /tmp/work-run-i63-i1lwhdly/supervision-4-answer/.shop/scratch/4-answer/result.json

You start in your worktree, /tmp/work-run-i63-i1lwhdly/supervision-4-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
