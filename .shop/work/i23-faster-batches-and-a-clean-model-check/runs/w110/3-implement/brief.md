# implement of w110

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w110.md
Agent: bdd-implementer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w110
Branch: work/w110
Work-item branch: work/w110
Suite record: Suite: 690 passed, 6 failed at b07ef8f in 13 s; failing: tests/scenarios/test_batch_measurement.py::test_a_time_ending_in_z_in_file_is_read_as_a_time_in_utc[a transcript-2026-10-22T09:55:00+02:00-2026-10-22T11:40:00+02:00-2026-10-22T08:30:00Z], tests/scenarios/test_batch_measurement.py::test_a_transcript_line_with_line_break_inside_a_json_string_is_read_as_one_line[U+2028], tests/scenarios/test_batch_measurement.py::test_a_transcript_line_with_line_break_inside_a_json_string_is_read_as_one_line[U+2029], tests/scenarios/test_batch_measurement.py::test_a_stage_whose_sessionjson_is_empty_is_given_without_its_sessions_figures_named_as_such, tests/scenarios/test_batch_measurement.py::test_a_transcript_line_with_line_break_inside_a_json_string_is_read_as_one_line[U+0085], tests/scenarios/test_batch_measurement.py::test_a_time_ending_in_z_in_file_is_read_as_a_time_in_utc[log.jsonl-2026-10-22T07:55:00Z-2026-10-22T11:40:00+02:00-2026-10-22T08:30:00+00:00]; expected: tests/scenarios/test_design_model_check.py::test_a_bounded_context_with_no_job_gets_no_unservedcapability_warning, tests/scenarios/test_design_model_check.py::test_a_workitem_accepting_a_requirement_of_a_guarantees_capability_that_no_scenario_names_is_no_file_problem, tests/scenarios/test_design_model_check.py::test_a_green_workitem_accepting_a_retired_id_is_no_file_problem, tests/scenarios/test_analysis_tools.py::test_install_puts_in_the_version_of_ruff_the_plugin_pins, tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has the kind capability-proposal and the status built-.shop/work/i1/p1.md], tests/scenarios/test_design_model_check.py::test_a_workitem_accepting_a_requirement_no_scenario_names_yet_with_no_check_is_not_v_w4, tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[U+000B, the vertical tab], tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[U+0085, the next-line control], tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[U+2029, the paragraph separator], tests/scenarios/test_work_queue.py::test_an_answer_of_two_lines_to_a_workitem_not_awaitinganswer_is_refused_as_more_than_one_line_first, tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[U+2028, the line separator], tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[a newline], tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[U+000D, the carriage return], tests/scenarios/test_work_queue.py::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[U+000C, the form feed]

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w110.md
- spec/capabilities/batch-measurement.md
- .shop/work/i23-faster-batches-and-a-clean-model-check/runs/w110/1-research
- .shop/work/i23-faster-batches-and-a-clean-model-check/runs/w110/2-plan

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w110/.shop/scratch/3-implement
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w110/.shop/scratch/3-implement/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w110: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
