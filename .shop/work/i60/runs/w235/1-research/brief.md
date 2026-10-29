# research of w235

Work-item: .shop/work/i60/w235.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: ae85edd3a2ce3488f4d930ac5814845eea5e6178
Worktree: /tmp/work-run-i60-5vc1dkqs/w235-1-research
Branch: none (a detached checkout)
Work-item branch: work/w235
Accepted scenarios:
- features/requests.feature: delegate given a request that holds <before> writes the delegation given in the request, in place of any it had
- features/requests.feature: delegate writing a delegation in a request commits the request on the current branch
- features/requests.feature: delegate given an empty delegation is refused, and nothing changes
- features/requests.feature: delegate given a request that is <status> is refused, naming <status>, and nothing changes
- features/requests.feature: a session the person gives a delegation for a request writes it, in the same reply, through delegate as the person's words with the date
- features/requests.feature: delegate run in the <side>'s turn writes the delegation
- features/requests.feature: delegate writing a delegation in a request keeps the request's status and turn

Read (paths in your worktree):
- .shop/work/i60/w235.md
- spec/capabilities/requests.md

Run directory: /tmp/work-run-i60-5vc1dkqs/w235-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i60-5vc1dkqs/w235-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i60-5vc1dkqs/w235-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
