# review of w178

Work-item: .shop/work/i26/w178.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i26-_dp917i5/w178-5-review
Branch: none (a detached checkout)
Work-item branch: work/w178
Answers the person gave, each with the question it answers:
- Question: Which requests whose asker is this context count as 'in the asker's turn' for supervision r9, r82 and r101? Reading A: every request whose turn is the asker's, whatever its status. A request the upstream has settled (accepted, refused or delivered, which `work turn` leaves in the asker's turn) then also stops the run. For example, an internal request taken in and accepted by an intake round makes `work run` exit with an error that prints the request with no open questions, in every run until something passes the turn back. Reading B: only a request in the asker's turn that is awaiting-asker, its negotiation still open. Then `work run` exits with an error, printing the request and its open questions, only while it waits on an answer; settled requests leave the exit successful.
  Answer: 2026-10-25: Reading B: only a request whose asker is this context and whose status is awaiting-asker, its negotiation still open; a settled request (accepted, refused, delivered) leaves the exit successful (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")

Read (paths in your worktree):
- .shop/work/i26/w178.md
- spec/capabilities/supervision.md
- .shop/work/i26/runs/w178/1-research
- .shop/work/i26/runs/w178/2-plan
- .shop/work/i26/runs/w178/3-plan
- .shop/work/i26/runs/w178/4-implement

Run directory: /tmp/work-run-i26-_dp917i5/w178-5-review/.shop/scratch/5-review
Result file: /tmp/work-run-i26-_dp917i5/w178-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /tmp/work-run-i26-_dp917i5/w178-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
