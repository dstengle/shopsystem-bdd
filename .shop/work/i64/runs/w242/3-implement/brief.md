# implement of w242

Work-item: .shop/work/i64/w242.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 86582d02951f1643d542fd5f162fb3ba5fd7abc2
Worktree: /tmp/work-run-i64-fow6jpdp/w242
Branch: work/w242
Work-item branch: work/w242
Suite record: Suite: 1086 passed, 2 failed at 082922c2 in 36 s; failing: tests/scenarios/test_supervision.py::test_an_apply_round_that_gives_an_answer_the_drafts_it_applied_do_not_hold_for_a_glossaryproposal_is_followed_by_a_new_integrate_round_for_the_glossaryproposal, tests/scenarios/test_supervision.py::test_a_scenario_that_fails_again_on_its_second_run_alone_has_both_its_runs_in_the_question_written_for_the_workitem; expected: tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"], tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"], tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start, tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests, tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages], tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet], tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1], tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's], tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_that_redrafts_some_of_its_lines_leaves_the_proposal_with_the_requirement_ids_its_change_list_does_not_name, tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_glossaryproposal_that_redrafts_some_of_its_terms_leaves_the_proposal_with_the_terms_its_change_list_does_not_name

Read (paths in your worktree):
- .shop/work/i64/w242.md
- spec/capabilities/supervision.md
- .shop/work/i64/runs/w242/1-research
- .shop/work/i64/runs/w242/2-plan

Run directory: /tmp/work-run-i64-fow6jpdp/w242/.shop/scratch/3-implement
Result file: /tmp/work-run-i64-fow6jpdp/w242/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i64-fow6jpdp/w242: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
