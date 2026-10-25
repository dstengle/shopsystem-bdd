# plan of w175

Work-item: .shop/work/i29/w175.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 4640ef08c740b5867638a4ae1f92e94d586c297c
Worktree: /tmp/work-run-i29-uk3_aing/w175-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w175
Answers the person gave, each with the question it answers:
- Question: requests#r22 says work request refuses when 'the delegation given is empty'. Does a delegation of only whitespace (e.g. --delegation "   ") count as empty? Reading A (empty string only): `work request ... --delegation "   "` exits successfully, prints q<n>, and the request is kept and committed with delegation "   " (today's behaviour, under r19); work run then treats "   " as a delegation and sends questions to answer sessions. Reading B (empty after stripping whitespace): the same command is refused because the delegation is empty, exits with an error, and the upstream keeps no request, exactly as for --delegation "". The r22 scenario's Pins line ('a delegation that names no question') leans to B, but the word 'empty' reads as A.
  Answer: 2026-10-25: Reading B: a delegation that is empty after stripping whitespace is refused, exactly as an empty one (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")

Read (paths in your worktree):
- .shop/work/i29/w175.md
- spec/capabilities/requests.md
- .shop/work/i29/runs/w175/1-research
- .shop/work/i29/runs/w175/2-plan

Run directory: /tmp/work-run-i29-uk3_aing/w175-3-plan/.shop/scratch/3-plan
Result file: /tmp/work-run-i29-uk3_aing/w175-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /tmp/work-run-i29-uk3_aing/w175-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
