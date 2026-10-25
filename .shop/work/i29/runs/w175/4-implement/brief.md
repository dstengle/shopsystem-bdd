# implement of w175

Work-item: .shop/work/i29/w175.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 4640ef08c740b5867638a4ae1f92e94d586c297c
Worktree: /tmp/work-run-i29-uk3_aing/w175
Branch: work/w175
Work-item branch: work/w175
Suite record: Suite: 867 passed, 7 failed at c91dc0cb in 23 s; failing: tests/scenarios/test_requests.py::test_request_with_an_empty_delegation_is_refused_and_nothing_changes, tests/scenarios/test_supervision.py::test_the_kind_round_of_a_capabilityproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[gate-drafted], tests/scenarios/test_supervision.py::test_an_initiative_set_done_is_committed_on_the_initiative_branch, tests/scenarios/test_supervision.py::test_the_kind_round_of_a_capabilityproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[apply-awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", and its Answers section with "One book."], tests/scenarios/test_supervision.py::test_once_the_initiatives_measurement_and_analysis_record_are_written_they_are_committed_on_the_initiative_branch, tests/scenarios/test_supervision.py::test_an_initiative_whose_workitems_are_green_or_withdrawn_whose_branch_review_lists_nothing_to_fix_now_whose_measurement_and_analysis_record_are_committed_and_whose_requests_are_delivered_is_set_done, tests/scenarios/test_supervision.py::test_a_change_list_naming_a_capability_that_neither_speccapabilities_nor_the_rounds_drafts_have_gives_no_capabilityproposal_for_it_and_work_run_exits_with_an_error_naming_it; expected: tests/scenarios/test_supervision.py::test_a_field_of_a_workers_result_giving_a_sentence_longer_than_a_file_name_may_be_is_taken_as_no_file
Answers the person gave, each with the question it answers:
- Question: requests#r22 says work request refuses when 'the delegation given is empty'. Does a delegation of only whitespace (e.g. --delegation "   ") count as empty? Reading A (empty string only): `work request ... --delegation "   "` exits successfully, prints q<n>, and the request is kept and committed with delegation "   " (today's behaviour, under r19); work run then treats "   " as a delegation and sends questions to answer sessions. Reading B (empty after stripping whitespace): the same command is refused because the delegation is empty, exits with an error, and the upstream keeps no request, exactly as for --delegation "". The r22 scenario's Pins line ('a delegation that names no question') leans to B, but the word 'empty' reads as A.
  Answer: 2026-10-25: Reading B: a delegation that is empty after stripping whitespace is refused, exactly as an empty one (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")

Read (paths in your worktree):
- .shop/work/i29/w175.md
- spec/capabilities/requests.md
- .shop/work/i29/runs/w175/1-research
- .shop/work/i29/runs/w175/2-plan
- .shop/work/i29/runs/w175/3-plan

Run directory: /tmp/work-run-i29-uk3_aing/w175/.shop/scratch/4-implement
Result file: /tmp/work-run-i29-uk3_aing/w175/.shop/scratch/4-implement/result.json

You start in your worktree, /tmp/work-run-i29-uk3_aing/w175: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
