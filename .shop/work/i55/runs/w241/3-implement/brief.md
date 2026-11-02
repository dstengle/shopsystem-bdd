# implement of w241

Work-item: .shop/work/i55/w241.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /tmp/work-run-i55-t2ssiod4/w241
Branch: work/w241
Work-item branch: work/w241
Suite record: Suite: 1089 passed, 0 failed at 8c3caec6 in 33 s; expected: tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start, tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests, tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages], tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet], tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1], tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2], tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"], tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's], tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_that_redrafts_some_of_its_lines_leaves_the_proposal_with_the_requirement_ids_its_change_list_does_not_name, tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_glossaryproposal_that_redrafts_some_of_its_terms_leaves_the_proposal_with_the_terms_its_change_list_does_not_name, tests/scenarios/test_supervision.py::test_an_initiative_whose_workitems_are_workitems_and_whose_capabilityproposal_is_p1_its_delivery_otherwise_closed_set[w1 is green and w2 is withdrawn-withdrawn-withdrawn-is set done-is done]

Read (paths in your worktree):
- .shop/work/i55/w241.md
- spec/capabilities/supervision.md
- .shop/work/i55/runs/w241/1-research
- .shop/work/i55/runs/w241/2-plan

Run directory: /tmp/work-run-i55-t2ssiod4/w241/.shop/scratch/3-implement
Result file: /tmp/work-run-i55-t2ssiod4/w241/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i55-t2ssiod4/w241: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
