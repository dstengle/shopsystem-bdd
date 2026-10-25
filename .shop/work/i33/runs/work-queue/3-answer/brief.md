# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i33-9vstbbh_/work-queue-3-answer
Branch: none (a detached checkout)
Question: r120's subject. Line: [r120] When the delegation-answerer answers a reviewer's question on a work-item, the delegation-answerer shall give in its result whether its answer asks for a change or accepts the work-item as it is. "the delegation-answerer" is no glossary term; r77 calls it "a session of its own, given the delegation". Readings: (a, recommended) recast: "[r120] Where the request an initiative fulfils gives a delegation, when a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is."; (b) keep r120 as drafted and add the glossary entry "- **delegation-answerer**: the session `work run` starts under a request's delegation to answer one question of an initiative."
Delegation: The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading.

Read (paths in your worktree):
Run directory: /tmp/work-run-i33-9vstbbh_/work-queue-3-answer/.shop/scratch/3-answer
Result file: /tmp/work-run-i33-9vstbbh_/work-queue-3-answer/.shop/scratch/3-answer/result.json

You start in your worktree, /tmp/work-run-i33-9vstbbh_/work-queue-3-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
