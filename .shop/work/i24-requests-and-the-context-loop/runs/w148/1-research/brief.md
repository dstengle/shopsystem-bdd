# research of w148

Work-item: .shop/work/i24-requests-and-the-context-loop/w148.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w148-1-research
Branch: none (a detached checkout)
Work-item branch: work/w148
Accepted scenarios:
- features/work-queue.feature: a command that cannot be done exits with an error, says why and changes nothing
- features/work-queue.feature: a transition of a work-item that does not exist is refused, saying why, and changes nothing
- features/work-queue.feature: add refuses an initiative that is not one directory entry under .shop/work/, saying why, and changes nothing
- features/work-queue.feature: add refuses a field value with a newline in it, saying why, and changes nothing
- features/work-queue.feature: show refuses a file under an initiative that is not UTF-8 text, naming it
- features/work-queue.feature: a transition of a work-item whose file <lacks> is refused, saying why, and changes nothing
- features/work-queue.feature: a transition whose log.jsonl <fault> is refused, saying why, and changes nothing
- features/work-queue.feature: request with a --lines file that does not exist is refused, naming the file, and changes nothing

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w148.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w148-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w148-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-bowwvrlq/w148-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
