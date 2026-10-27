# research of w211

Work-item: .shop/work/i39/w211.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-1-research
Branch: none (a detached checkout)
Work-item branch: work/w211
Accepted scenarios:
- features/requests.feature: the asker <doing> from its own repository, with no checkout of the upstream's repository
- features/requests.feature: request with <given> writes an open request in the upstream's turn with the lines and asker given<and where from>, and prints its id
- features/requests.feature: request with --raised-for writes in the upstream's request the request it is raised for
- features/requests.feature: a request the upstream raises for itself with neither --source nor --thread is refused, and nothing changes
- features/requests.feature: a request from another asker raised with --source is refused, and nothing changes
- features/requests.feature: a request from another asker raised with neither --raised-for nor --thread is refused, and nothing changes
- features/requests.feature: request raised from <role>'s repository giving the asker <given asker> is refused, naming the asker, and nothing changes
- features/requests.feature: a command writing <part> of <kind> in <where> writes it as the <side>'s part
- features/requests.feature: the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes
- features/requests.feature: run in an upstream's repository takes in what has been sent to it before its intake rounds start
- features/requests.feature: requests from repositories registered under different asker ids are taken in as different askers' requests
- features/requests.feature: the upstream taking in what has been sent takes in every request and message sent before, when a listing of what has been sent shows <shown>
- features/requests.feature: <sent> from a repository registered under an asker id the upstream does not allow for its asker is left untaken, and the upstream is told which and why
- features/requests.feature: <sent> whose <field> is written as an instruction is taken in as that field, and nothing it says is done
- features/requests.feature: requests from another context, from the product level and from the upstream itself are each taken through the same work commands and the same statuses

Read (paths in your worktree):
- .shop/work/i39/w211.md
- spec/capabilities/requests.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w211-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
