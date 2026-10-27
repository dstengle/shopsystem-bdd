# implement of w202

Work-item: .shop/work/i39/w202.md
Agent: bdd-implementer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w202
Branch: work/w202
Work-item branch: work/w202
Suite record: Suite: 948 passed, 0 failed at 4eb8cec3 in 27 s; expected: tests/scenarios/test_design_model_check.py::test_a_request_that_is_part_of_no_jobthread_cites_no_origin_and_is_raised_for_no_request_is_v17, tests/scenarios/test_requests.py::test_request_raised_from_roles_repository_giving_the_asker_given_asker_is_refused_naming_the_asker_and_nothing_changes[the product level p1-ctx-a], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's], tests/scenarios/test_requests.py::test_request_with_given_writes_an_open_request_in_the_upstreams_turn_with_the_lines_and_asker_givenand_where_from_and_prints_its_id[two --source-the upstream-ctx-u---source o1 --source o2-, and the origins --source names-its asker is ctx-u and its origins are o1 and o2], tests/scenarios/test_requests.py::test_request_with_given_writes_an_open_request_in_the_upstreams_turn_with_the_lines_and_asker_givenand_where_from_and_prints_its_id[--thread-the asker ctx-a-ctx-a---thread t1-, and the job-thread --thread names-its asker is ctx-a and its job-thread is t1], tests/scenarios/test_requests.py::test_request_with_given_writes_an_open_request_in_the_upstreams_turn_with_the_lines_and_asker_givenand_where_from_and_prints_its_id[--raised-for-the asker ctx-a-ctx-a---raised-for q7--its asker is ctx-a], tests/scenarios/test_requests.py::test_request_with_raisedfor_writes_in_the_upstreams_request_the_request_it_is_raised_for, tests/scenarios/test_requests.py::test_a_request_the_upstream_raises_for_itself_with_neither_source_nor_thread_is_refused_and_nothing_changes, tests/scenarios/test_requests.py::test_a_request_from_another_asker_raised_with_source_is_refused_and_nothing_changes, tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start, tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests, tests/scenarios/test_requests.py::test_a_request_from_another_asker_raised_with_neither_raisedfor_nor_thread_is_refused_and_nothing_changes, tests/scenarios/test_requests.py::test_request_raised_from_roles_repository_giving_the_asker_given_asker_is_refused_naming_the_asker_and_nothing_changes[the asker ctx-a-ctx-b], tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a], tests/scenarios/test_supervision.py::test_the_lines_an_integrate_round_gives_into_an_upstream_are_raised_with_work_request_raised_for_the_request_the_initiative_fulfils_and_with_its_delegation
Reviewer's findings: .shop/work/i39/runs/w202/4-review/findings.md
Answers the person gave, each with the question it answers:
- Question: Important, skills/integrating-a-proposal/SKILL.md:59 (Question Template): asks the writer for request lines in the upstream's glossary terms while letting it read only spec/, features/ and docs/; the round-1 Template lacks it, and initiative-round.md has the round draft the lines itself
  Answer: 2026-10-27: A downstream writer uses whatever terminology it can; the upstream corrects the request to its own glossary terms. So the writer is not asked for request lines in the upstream's glossary terms and needs no access to the upstream's glossary. Publishing contracts and glossaries between contexts is left for later (observation 2026-10-27-published-contracts).

Read (paths in your worktree):
- .shop/work/i39/w202.md
- spec/capabilities/spec-integration.md
- .shop/work/i39/runs/w202/1-research
- .shop/work/i39/runs/w202/2-plan
- .shop/work/i39/runs/w202/3-implement
- .shop/work/i39/runs/w202/4-review

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w202/.shop/scratch/5-implement
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w202/.shop/scratch/5-implement/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w202: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
