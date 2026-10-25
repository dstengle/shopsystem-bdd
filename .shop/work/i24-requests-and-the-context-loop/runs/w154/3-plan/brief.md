# plan of w154

Work-item: .shop/work/i24-requests-and-the-context-loop/w154.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-_64lmssk/w154-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w154
Questions the researcher gave with its DONE, for you to settle or ask:
- Does a non-DONE gate round write its questions under the proposal's ## Questions (r85 says it ends; r86/r87 keep the status and make no transition)?
- When an integrate round gives BLOCKED or faults, does the initiative stay started (r84 order) or go back to proposed (r86 keep-status)?
- Should work run <initiative> with a proposal awaiting-answer exit with an error, as r81 requires for a run with no initiative? (D3, observed exit 0)
- The r88 Then says 'left no result it can read'; the message says 'wrote no result file'. Change the step's match or the message?
Answers the person gave, each with the question it answers:
- Question: When a gate round gives a readable result whose outcome is not DONE (e.g. BLOCKED or QUESTION) and lists questions, does `work run` still write those questions under the capability-proposal's ## Questions (r85 'when a gate round ends') while keeping the status and making no transition (r86/r87)? Reading A (r85 applies to any gate round that ends): the person sees p1 still drafted with the round's questions under ## Questions, and `work run` exits with an error naming the round; the next run starts the gate round again on a proposal that already has questions, which may then be listed twice. Reading B ('ends' in r85 means ends with DONE, as r69's 'ends' has to under r87): the person sees p1 drafted with nothing written on it, the questions only in the round's committed result.json, and `work run` exits with an error naming the round and its outcome. Under B, a gate agent that gives its gate with the outcome QUESTION instead of DONE would stop the run every time.
  Answer: 2026-10-25: Reading B (the coordinator, under the person's delegation): 'ends' in r85 means ends with DONE, as r69's does under r87; a gate round with any other outcome writes nothing on the proposal, its questions stay in its committed result.json, and work run exits with an error naming the round and its outcome.

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w154.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w154/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w154/2-plan

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-_64lmssk/w154-3-plan/.shop/scratch/3-plan
Result file: /tmp/work-run-i24-requests-and-the-context-loop-_64lmssk/w154-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-_64lmssk/w154-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
