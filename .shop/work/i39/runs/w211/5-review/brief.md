# review of w211

Work-item: .shop/work/i39/w211.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-5-review
Branch: none (a detached checkout)
Work-item branch: work/w211
Answers the person gave, each with the question it answers:
- Question: Carrier of what an asker sends (requests r28, r39-r44, decision 0071): r28/r44/r29 say the upstream keeps the request right after the asker's work request, with no checkout of the upstream; r39/r41 say it is kept only once taken in; r28 rows 2-3 and r33 row 1 have the asker answer a question only the upstream wrote. Reading A (git transport): the asker pushes each request or message to a ref namespace named by its asker id on the upstream's remote and fetches the upstream's requests to read questions; the narrator configures the upstream's remote, the upstream's work list shows nothing until take-in, and the namespace is the registration. Reading B (drop directory): a shared directory set in each repository's settings, one subdirectory per registered asker id, and the asker keeps its own copy of each request it raised; the narrator configures a drop path, the upstream sees nothing until take-in, and the asker sees questions only from what the upstream writes back to the drop.; Does requests r28 bind supervision's raise (supervision r135)? Reading A (no): work run keeps writing a raised request straight into the upstream's checkout, and the r30-r32 checks run only in the work request command; supervision's narrator sees no change, and features/supervision.feature:1445-1452 stays green. Reading B (yes): work run sends the raised request through the carrier like any asker; the request is in the upstream only after its take-in, the hold (r136) reads it through the carrier, and supervision r135's scenario ('the request it wrote in catalogue') must first be reformulated by a supervision proposal.
  Answer: 2026-10-27: Carrier: Reading A (git transport): the asker pushes each request, answer or turn to a ref namespace named by its asker id on the upstream's remote and fetches the upstream's requests to read its questions; the upstream's work list shows nothing until take-in, and the namespace is the registration. Chosen because it works across machines, a test can run it with a local bare remote, and each push is one turn of the request's conversation. Supervision's raise: Reading A (no): work run keeps writing a raised request into the upstream's checkout for now and supervision's scenario stays green; sending it through the carrier is a follow-up (answered by the coordinator under the person's delegation of 2026-10-27; no reading was recommended, and the person ruled that where a request is kept is the upstream's implementation).

Read (paths in your worktree):
- .shop/work/i39/w211.md
- spec/capabilities/requests.md
- .shop/work/i39/runs/w211/1-research
- .shop/work/i39/runs/w211/2-plan
- .shop/work/i39/runs/w211/3-plan
- .shop/work/i39/runs/w211/4-implement

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-5-review/.shop/scratch/5-review
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w211-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
