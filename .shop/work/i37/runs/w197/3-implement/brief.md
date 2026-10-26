# implement of w197

Work-item: .shop/work/i37/w197.md
Agent: bdd-implementer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: 94be81b4c7efa16e4b751858da00db485be242d1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w197
Branch: work/w197
Work-item branch: work/w197
Suite record: Suite: 924 passed, 4 failed at b6815a57 in 26 s; failing: tests/scenarios/test_requests.py::test_resolve_setting_a_requests_status_to_delivered_passes_the_requests_turn_to_its_asker, tests/scenarios/test_requests.py::test_the_upstream_ending_its_turn_on_a_request_that_turn_sets_to_accepted_keeps_the_requests_turn_the_upstreams, tests/scenarios/test_requests.py::test_turn_on_a_request_it_does_not_set_to_accepted_passes_the_requests_turn_from_the_side_to_the_other_side[upstream-asker], tests/scenarios/test_requests.py::test_turn_on_a_request_it_does_not_set_to_accepted_passes_the_requests_turn_from_the_side_to_the_other_side[asker-upstream]

Read (paths in your worktree):
- .shop/work/i37/w197.md
- spec/capabilities/requests.md
- .shop/work/i37/runs/w197/1-research
- .shop/work/i37/runs/w197/2-plan

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w197/.shop/scratch/3-implement
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w197/.shop/scratch/3-implement/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w197: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
