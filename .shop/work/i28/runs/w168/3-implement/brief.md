# implement of w168

Work-item: .shop/work/i28/w168.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 4b7dca6c200ffc64be3fe1887f1d08a62b311332
Worktree: /tmp/work-run-i28-a0yhlc3a/w168
Branch: work/w168
Work-item branch: work/w168
Suite record: Suite: 858 passed, 3 failed at 39fad50d in 23 s; failing: tests/scenarios/test_work_queue.py::test_answer_named_by_its_initiative_answers_the_kind_name_of_that_initiative[capability-proposal-p1-capability-proposal p1], tests/scenarios/test_work_queue.py::test_answer_named_by_its_initiative_answers_the_kind_name_of_that_initiative[work-item-w2-work-item w1], tests/scenarios/test_supervision.py::test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds_of_different_initiatives_one_at_a_time; expected: tests/scenarios/test_supervision.py::test_the_change_lists_of_two_initiatives_that_name_the_same_capability_give_two_drafted_capabilityproposals_with_different_ids, tests/scenarios/test_supervision.py::test_an_integrate_round_is_given_every_requirement_id_another_initiatives_kept_drafts_add_that_spec_on_the_branch_it_starts_from_does_not_hold_whatever_that_initiatives_capabilityproposals_status, tests/scenarios/test_supervision.py::test_the_gate_round_of_a_capabilityproposal_is_asked_only_for_the_questions_on_the_lines_and_terms_that_proposal_adds_changes_or_removes, tests/scenarios/test_supervision.py::test_an_accepted_request_this_context_is_the_upstream_of_that_no_initiative_fulfils_has_its_initiative_started_with_work_start

Read (paths in your worktree):
- .shop/work/i28/w168.md
- spec/capabilities/work-queue.md
- .shop/work/i28/runs/w168/1-research
- .shop/work/i28/runs/w168/2-plan

Run directory: /tmp/work-run-i28-a0yhlc3a/w168/.shop/scratch/3-implement
Result file: /tmp/work-run-i28-a0yhlc3a/w168/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i28-a0yhlc3a/w168: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
