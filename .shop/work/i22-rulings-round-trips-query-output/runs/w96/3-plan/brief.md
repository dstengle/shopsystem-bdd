# plan of w96

Work-item: .shop/work/i22-rulings-round-trips-query-output/w96.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w96
Answers the person gave, each with the question it answers:
- Question: F7: when `.shop/plugin-version` holds no version (e.g. `next`, or nothing), what does `migrate status --hook`, the SessionStart hook, do? `--hook`'s help says it exits 0; the work-item says 'refuse, saying why'; no requirement settles which governs. Reading A, exit 0 with text: the hook prints to stdout a line saying the version file holds no version, naming what it holds and telling the session to tell the person. The session is told at its start and passes it on, and the hook keeps its exit-0 contract. Reading B, exit 1 as `migrate status` does: the hook prints the reason on stderr and exits 1. The session's context gets nothing; the person sees only the hook error that Claude Code reports, and the session never learns why.
  Answer: 2026-10-23: Reading A: migrate status --hook exits 0 and prints one line saying the version file holds no version, naming what it holds and telling the session to tell the person.

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w96.md
- spec/capabilities/migration-tools.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w96/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w96/2-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96-3-plan/.shop/scratch/3-plan
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w96-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
