# implement of w185

Work-item: .shop/work/i31/w185.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 9839b05ad9aad4b8f205963f9f056745069a2206
Worktree: /tmp/work-run-i31-t5_5f5um/w185
Branch: work/w185
Work-item branch: work/w185
Suite record: Suite: 890 passed, 8 failed at 159c7530 in 22 s; failing: tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_capabilityproposal_ends_the_proposals_adds_changes_and_removes_are_written_from_the_change_list_the_round_applied, tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_questions_each_is_written_under_the_proposals__questions, tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_a_question_the_proposal_is_awaitinganswer, tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends with no error and before its turn limit, having written no result file], tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends in an error], tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[ends at its turn limit], tests/scenarios/test_supervision.py::test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_ends_without_giving_a_question_the_proposal_is_formulated, tests/scenarios/test_supervision.py::test_when_the_gate_round_of_a_capabilityproposal_ending_the_initiatives_other_nodes_are_taken_through_their_transitions_before_work_run_exits_with_an_error[gives BLOCKED, asking "Is a title given twice one book or two?"]
Answers the person gave, each with the question it answers:
- Question: supervision#r116: its Then (a formulate round was started for p1, given the answer) passes on today's apply-then-formulate chain (1 passed, no production code changed). Should the scenario also assert that no apply round is started, or is r116 met as is?
  Answer: 2026-10-25: r116 is met as is; that no apply round follows a formulate round's answered questions is r70's changed line, whose scenario w185 also accepts: implement r70 so that only a gate round's answered questions start an apply round (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i31/w185.md
- spec/capabilities/supervision.md
- .shop/work/i31/runs/w185/1-research
- .shop/work/i31/runs/w185/2-plan
- .shop/work/i31/runs/w185/3-implement

Run directory: /tmp/work-run-i31-t5_5f5um/w185/.shop/scratch/4-implement
Result file: /tmp/work-run-i31-t5_5f5um/w185/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i31-t5_5f5um/w185: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
