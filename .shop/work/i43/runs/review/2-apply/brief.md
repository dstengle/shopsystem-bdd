# apply of review

Capability-proposal: .shop/work/i43/review.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i43/runs/i43/1-integrate/drafts/round-1/
Base: ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/review-2-apply
Branch: round/review-2-apply
Answers the person gave, each with the question it answers:
- Question: supervision#r155 (exit code). Line: [r155] When `work run` starts a branch review, `work run` shall give the branch reviewer each run r154 names with its command, how it exited and its output, naming the commit they ran at. Reading A (recommended, drafted): 'how it exited', with the exit code in Implementation. Reading B: 'each run r154 names with its command, exit code and output, naming the commit they ran at.'
  Answer: 2026-10-28: supervision#r155 exit code: Reading A, 'how it exited', with the exit code in Implementation (answered by the coordinator under the person's delegation of 2026-10-28).
- Question: review#r33 (the request's Where). Line: [r33] When a branch review finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction. Reading A (recommended, drafted): When ... Reading B: keep 'Where the branch reviewer finds ...'.
  Answer: 2026-10-28: review#r33: Reading A, 'When a branch review finds ...' as drafted (answered by the coordinator under the person's delegation of 2026-10-28).
- Question: review#r12 ('an observation, with its reproduction') against r32/r33. Reading A (recommended): r12 stands; a reproduction is written, not run. Reading B: retire r12, add [r35] '...as an observation, with its reproduction or, in a branch review, the test r33 names, for hardening, ...'.
  Answer: 2026-10-28: review#r12 against r32/r33: Reading A, r12 stands; a reproduction is written, not run (answered by the coordinator under the person's delegation of 2026-10-28).
- Question: review#r7 (the suite's wall time) against r32. Reading A (recommended): r7 stands; the reviewer reads the wall time from the suite run output r155 gives. Reading B: add supervision [r158] 'When `work run` starts a branch review, `work run` shall give the branch reviewer the wall time of the whole suite's run r154 names.'
  Answer: 2026-10-28: review#r7 against r32: Reading A, r7 stands; the reviewer reads the wall time from the suite run output r155 gives (answered by the coordinator under the person's delegation of 2026-10-28).
- Question: review#r6 (a check the reviewer cannot verify fails a branch review) against r32. Reading A (recommended): r6 stands; the reviewer verifies each check from the run r154/r155 give. Reading B: retire r6, change its branch-review cell to 'fail the review where the run of it that `work run` gave shows it did not exit successfully, or `work run` gave no run of it'.
  Answer: 2026-10-28: review#r6 against r32: Reading A, r6 stands; the reviewer verifies each check from the runs r154/r155 give (answered by the coordinator under the person's delegation of 2026-10-28).
- Question: review Implementation ('Probes go in the scratch directory the brief names'). Reading A (recommended): keep, it covers only the work-item reviewer now. Reading B: reword to 'A work-item reviewer's probes go in the scratch directory the brief names; the branch reviewer makes none (r32).'
  Answer: 2026-10-28: review Implementation probes: Reading A, keep; it covers only the work-item reviewer now (answered by the coordinator under the person's delegation of 2026-10-28).
- Question: Agent tools: design-decision/the-v3-agents gives bdd-branch-reviewer Bash, against review#r32 (runs nothing). Reading A (recommended): no change; r32 is held by the brief. Reading B: a new decision superseding the-v3-agents' row and a role-boundaries line giving the branch reviewer no Bash tool, raised as its own request.
  Answer: 2026-10-28: Agent tools: Reading B, a new decision superseding the-v3-agents' row and a role-boundaries line giving the branch reviewer no Bash tool, raised as its own request (q24); r32 held by the brief until then. Not the recommended reading: without the tool removed, 'runs nothing' is only an instruction, and removing Bash is what removes the sandbox refusals (answered by the coordinator under the person's delegation of 2026-10-28).

Read (paths in your worktree):
- .shop/work/i43/review.md
- .shop/work/i43/runs/review/1-gate
- .shop/work/i43/runs/i43/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/review-2-apply/.shop/scratch/2-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/review-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/review-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
