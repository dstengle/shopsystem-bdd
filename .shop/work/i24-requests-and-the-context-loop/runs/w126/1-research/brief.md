# research of w126

Work-item: .shop/work/i24-requests-and-the-context-loop/w126.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w126-1-research
Branch: none (a detached checkout)
Work-item branch: work/w126
Accepted scenarios:
- features/requests.feature: request with <given> writes an open request in the upstream's turn with the lines, asker and <where from> given, and prints its id
- features/requests.feature: request with a line that <fault> is refused, naming the line, and nothing changes
- features/requests.feature: request with neither --source nor --thread is refused, and nothing changes
- features/requests.feature: outcome writing a line outcome leaves the request's lines as the asker wrote them
- features/requests.feature: turn passing a request leaves its line outcomes as they were and writes no resolution

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w126.md
- spec/capabilities/requests.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w126-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w126-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w126-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
