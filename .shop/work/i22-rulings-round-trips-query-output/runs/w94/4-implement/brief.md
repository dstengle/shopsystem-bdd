# implement of w94

Work-item: .shop/work/i22-rulings-round-trips-query-output/w94.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94
Branch: work/w94
Work-item branch: work/w94
Suite record: Suite: 645 passed, 6 failed at db73865 in 23 s; failing: tests/scenarios/test_batch_measurement.py::test_show_prints_each_stages_round_trips_beside_its_turns, tests/scenarios/test_batch_measurement.py::test_show_prints_the_stages_of_a_measurement_that_gives_no_round_trips_without_them, tests/scenarios/test_batch_measurement.py::test_each_stage_is_given_with_its_sessions_round_trips, tests/scenarios/test_batch_measurement.py::test_a_stage_whose_session_has_no_transcript_to_be_found_is_given_without_its_round_trips, tests/scenarios/test_batch_measurement.py::test_each_workitem_is_given_with_its_transitions_its_awaitinganswer_and_failed_counts_and_the_commits_its_merge_brought_in, tests/scenarios/test_batch_measurement.py::test_the_totals_are_over_the_stages_sessions_an_unended_stage_included_and_span_the_first_transition_to_the_last; expected: tests/scenarios/test_analysis_tools.py::test_testsof_with_json_prints_the_tests_their_count_and_the_maps_commit_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_untested_with_json_prints_the_functions_their_count_and_the_maps_commit_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_refs_with_json_prints_the_references_and_the_summary_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_map_with_json_prints_the_maps_commit_and_its_test_count_as_one_json_object, tests/scenarios/test_analysis_tools.py::test_testsof_fails_when_the_file_has_no_function_by_the_name_given, tests/scenarios/test_analysis_tools.py::test_testsof_says_that_no_test_of_the_map_executed_the_target_and_exits_successfully
Answers the person gave, each with the question it answers:
- Question: r41 counts transitions 'to awaiting-answer', but every log written so far (this initiative's included, until w91 and decision 0064's upgrade step land) says awaiting-answer, and the deprecated r41 scenario, which w94 accepts and does not retire, expects '1 time to awaiting-answer'. What does measure count? Reading A, awaiting-answer only: a log with awaiting-answer transitions gives 0 to awaiting-answer; the deprecated r41 scenario goes red and w94 needs it retired (a Retires section). Reading B, awaiting-answer counted as the old name of awaiting-answer (0064: the status 'is' awaiting-answer): a log not yet upgraded gives its awaiting-answer transitions in the one awaiting-answer count; the deprecated scenario is kept, its step asserting that count is 1. Reading C, both counted apart: the measurement and show give an awaiting-answer count and an awaiting-answer count side by side; the deprecated scenario is kept as it reads.
  Answer: 2026-10-23: Reading A: measure counts awaiting-answer only; the r29 upgrade step renames old logs. w94 retires the deprecated r41 scenario (a Retires section).

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w94.md
- spec/capabilities/batch-measurement.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/2-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/3-plan

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94/.shop/scratch/4-implement
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
