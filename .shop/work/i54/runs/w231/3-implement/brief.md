# implement of w231

Work-item: .shop/work/i54/w231.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: a2a53b36c02b74d046b7a490d802403f3f1828a9
Worktree: /tmp/work-run-i54-w4h4vwrv/w231
Branch: work/w231
Work-item branch: work/w231
Suite record: Suite: 1065 passed, 2 failed at 156d2b2b in 35 s; failing: tests/scenarios/test_supervision.py::test_work_run_that_cannot_do_what_it_was_asked_exits_with_an_error_says_why_and_changes_nothing[i1's work-item w1 is drafted, in a directory that is not a git repository-i1-not a git repository], tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_whose_change_list_names_another_capability_the_initiative_holds_a_capabilityproposal_for_adds_the_rounds_ids_for_that_capability_to_that_proposal_keeping_the_ids_it_holds; expected: tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1], tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2], tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"], tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"], tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start, tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests, tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages], tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's]

Read (paths in your worktree):
- .shop/work/i54/w231.md
- spec/capabilities/supervision.md
- .shop/work/i54/runs/w231/1-research
- .shop/work/i54/runs/w231/2-plan

Run directory: /tmp/work-run-i54-w4h4vwrv/w231/.shop/scratch/3-implement
Result file: /tmp/work-run-i54-w4h4vwrv/w231/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i54-w4h4vwrv/w231: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
