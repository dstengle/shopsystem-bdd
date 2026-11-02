# branch review of i62

Initiative: .shop/work/i62
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: 955ad466c30a8e870af65b406cdd4b241699f24e
Head: 0b5e847086106cda4823e479182f8b4a0390372d
Worktree: /tmp/work-run-i62-uz32u3v4/branch-review
Run directory: /tmp/work-run-i62-uz32u3v4/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i62-uz32u3v4/branch-review/.shop/scratch/branch-review/result.json

Review the initiative branch from its base. You start in your worktree: run every command from there and never change directory. Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` and `questions`.

Read:
- spec/capabilities/supervision.md
- design-decision/a-script-supervises-delivery
- design-decision/worker-results-are-files
- design-decision/work-item-lifecycle-as-run
- design-decision/review-of-work-items
- design-decision/the-file-set-is-the-claim
- design-decision/the-v3-agents
- design-decision/exits-are-successful-or-errors
- design-decision/a-ruling-returns-to-the-asking-stage
- design-decision/answers-not-rulings
- design-decision/workflow-capabilities-are-guarantees
- design-decision/the-context-runs-without-a-coordinator
- design-decision/requests-written-through-work
- design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done
- design-decision/the-glossary-is-a-target-of-spec-work
- .shop/work/i62/runs/w245/10-review/findings.md
- .shop/work/i62/runs/w245/11-implement/report.md
- .shop/work/i62/runs/w245/12-review/findings.md
- .shop/work/i62/runs/w245/2-plan/plan.md
- .shop/work/i62/runs/w245/3-implement/report.md
- .shop/work/i62/runs/w245/4-implement/report.md
- .shop/work/i62/runs/w245/5-review/findings.md
- .shop/work/i62/runs/w245/6-implement/report.md
- .shop/work/i62/runs/w245/7-review/findings.md
- .shop/work/i62/runs/w245/8-implement/report.md
- .shop/work/i62/runs/w245/9-implement/report.md

## Runs

Ran at: 0b5e847086106cda4823e479182f8b4a0390372d

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w245 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 12%]
    ........................................................................ [ 19%]
    ........................................................................ [ 25%]
    ............................................................x.x...xxxxx. [ 31%]
    ..xx...x............................................x........xx.....xx.. [ 38%]
    .xx.....x...X.....x..................................................... [ 44%]
    ............................................................X........... [ 50%]
    ..........X......X...................................................... [ 57%]
    .X...............X...................................................... [ 63%]
    ...........................................X.......X.................... [ 69%]
    ...........X......................X..................................uu. [ 75%]
    ..uuuu.uuuuuuu..................uuuuu.............................u...u. [ 80%]
    .u.........u.u.u..u..u........u......X....u..........u............u..... [ 86%]
    ......x.................u.u.......u.....uuu..u.....uux..u.u...u..u...uu. [ 91%]
    ....u...us.ux..uux.uu.....u.......u..................................... [ 96%]
    .....uu.................................                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r212 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r209 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r210 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r211 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r213 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r214 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r215 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r216 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r218 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r219 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r220 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r222 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r221 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py: 313 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py: 313 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_answer_and_turn_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_answer_and_turn_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_the_fields_of_a_requests_form_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"-awaiting-asker] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_the_fields_of_a_requests_form_and_nothing_it_says_is_done[on q2 the passing of q2's turn-body-q2's turn is the upstream's-awaiting-upstream] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the passing of q2's turn-q2's turn is the asker's-the turn on q2] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_the_fields_of_a_requests_form_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"-awaiting-asker] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_list_prints_each_request_with_its_status_and_whose_turn_it_is - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_askers_repository_in_the_askers_turn_prints_that_it_is_the_askers_turn_with_each_question_the_asker_has_not_answered - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_upstreams_repository_while_the_upstream_holds_unsent_it_has_not_sent_with_the_turn_prints_that_the_asker_has_not_seen_it[the line outcome accepted of line 1-run `work outcome q1 1 accepted`] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_upstreams_repository_while_the_upstream_holds_unsent_it_has_not_sent_with_the_turn_prints_that_the_asker_has_not_seen_it[the question "Which queue?"-asked the question "Which queue?" on line 1 of q1] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_askers_repository_after_the_upstream_resolves_the_request_prints_each_accepted_lines_requirement_id_and_the_version_that_holds_it - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_writer_writing_the_owners_part_of_a_request_from_another_context_in_its_own_turn_is_refused_naming_the_owner_and_nothing_changes[upstream-asker-the upstream answers that question with "The work queue"-the upstream ctx-u's repository-answers] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_a_researchers_result_that_gives_an_empty_file_set_is_taken_as_the_researchers_file_set - expected: accepted by w243, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_work_run_ends_with_node_awaitinganswer_it_exits_with_an_error_printing_node_with_its_open_questions[w2-i1's work-item w2 is awaiting-answer, its ## Questions section with "Which unit is the limit in?" and "Is the old reader kept?", and its Answers section answering only "Is the old reader kept?" with "Yes."] - expected: accepted by w243, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_a_formulate_round_that_formulates_nothing_because_the_proposals_answers_change_lines_not_in_spec_is_followed_by_a_new_integrate_round_for_the_proposal - expected: accepted by w243, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_work_run_ends_with_node_awaitinganswer_it_exits_with_an_error_printing_node_with_its_open_questions[p1-i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Which unit is the limit in?" and "Is the old reader kept?", given by its gate round, and its Answers section answering only "Is the old reader kept?" with "Yes."] - expected: accepted by w243, neither green nor withdrawn
    1101 passed, 1 skipped, 23 xfailed, 11 xpassed, 1084 warnings, 56 subtests passed in 35.33s

### w245's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w245
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    .uu.............uuuuu...uuuuuuuuuuu...u..........uu....u.....u..u....u.. [ 25%]
    .....u......u..................u...u..........u......u....u............. [ 58%]
    ......u.u...............u..u...............u..uu.u..u.u....uu..uusuuuuu. [ 85%]
    u..u..u.u.u........................                                      [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r212 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r209 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r210 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r211 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r213 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r214 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r215 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r216 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r218 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r219 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r220 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r222 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r221 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_a_scenario_whose_failure_before_a_merge_would_keep_the_workitem_branch_from_being_merged_is_run_again_once_alone_before_the_merge_is_refused
    tests/scenarios/test_supervision.py::test_a_scenario_that_fails_again_on_its_second_run_alone_has_both_its_runs_in_the_question_written_for_the_workitem
    tests/scenarios/test_supervision.py::test_a_scenario_that_fails_before_a_merge_and_passes_on_its_second_run_alone_lets_the_workitem_branch_be_merged
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_a_scenario_whose_failure_before_a_merge_would_keep_the_workitem_branch_from_being_merged_is_run_again_once_alone_before_the_merge_is_refused
    tests/scenarios/test_supervision.py::test_a_scenario_that_fails_again_on_its_second_run_alone_has_both_its_runs_in_the_question_written_for_the_workitem
    tests/scenarios/test_supervision.py::test_a_scenario_that_fails_before_a_merge_and_passes_on_its_second_run_alone_lets_the_workitem_branch_be_merged
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    194 passed, 1 skipped, 454 warnings, 56 subtests passed in 11.65s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 955ad466c30a8e870af65b406cdd4b241699f24e
Exit code: 1
Output:
    == ruff ==
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:4:9: SIM115 Use a context manager for opening files
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:5:6: SIM115 Use a context manager for opening files
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:15:5: PLC0206 Extracting value from dictionary without calling `.items()`
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:42:1: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/29-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/29-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/29-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    .shop/work/i63/runs/supervision/1-gate/mk.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i63/runs/supervision/1-gate/mk.py:10:93: SIM115 Use a context manager for opening files
    scripts/supervise_change.py:83:75: B023 Function definition does not bind loop variable `field`
    scripts/supervise_change.py:83:92: B023 Function definition does not bind loop variable `mine`
    scripts/supervise_change.py:103:75: B023 Function definition does not bind loop variable `field`
    scripts/supervise_change.py:103:92: B023 Function definition does not bind loop variable `mine`
    scripts/supervise_change.py:130:104: B023 Function definition does not bind loop variable `said`
    tests/scenarios/supervision_proposal_steps.py:102:62: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_proposal_steps.py:146:94: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_reintegrate_steps.py:13:44: F401 [*] `.supervision_world.git` imported but unused
    tests/scenarios/supervision_reintegrate_steps.py:92:119: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_reintegrate_steps.py:101:119: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_reintegrate_steps.py:225:115: FURB167 [*] Use of regular expression alias `re.M`
    tests/scenarios/test_supervision.py:14:1: I001 [*] Import block is un-sorted or un-formatted
    tests/scenarios/work_queue_list_steps.py:134:12: RUF015 Prefer `next(...)` over single element slice
    tests/scripts/stub_claude.py:208:51: FURB167 [*] Use of regular expression alias `re.M`
    tests/scripts/stub_claude.py:209:51: FURB167 [*] Use of regular expression alias `re.M`
    tests/scripts/test_supervise_change.py:7:48: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    Found 29 errors.
    [*] 12 fixable with `--fix` (1 unsafe fix available with `--fix --unsafe-fixes`).
    == vulture ==
    tests/scenarios/work_queue_status_steps.py:100: unused variable 'notes' (100% confidence)
    == import-linter ==
    the project states no import contracts

### tools size
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools size
Exit code: 0
Output:

### features deprecated
Command: python3 /home/vscode/shopsystem-bdd/scripts/features deprecated
Exit code: 0
Output:
    features/design-model-check.feature: an id of a kind kept in .shop/work/ with another context's path is v18 (deprecated) | for: removal | deprecated for removal
    features/requests.feature: the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes (deprecated) | for: the <writer> writing the <owner>'s part of a request from another context in its own turn is refused, naming the <owner>, and nothing changes | features/requests.feature @r55
    features/requests.feature: show prints each request with its status and whose turn it is (deprecated) | for: list prints each request with its status and whose turn it is | features/requests.feature @r50
    features/supervision.feature: a worker's outcome DONE makes the work-item's transition to its next status (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: `work run` prints a question that has no answer yet, and not one that has an answer (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a researcher's DONE with questions puts those questions into the planner's brief (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply> (deprecated) | for: r209 and r210 | no scenario has that title
    features/supervision.feature: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: list prints each initiative, each request and each work-item under .shop/work/ with its status (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: list with --json prints each initiative, request and work-item with its status as one JSON object (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: show prints each work-item of every initiative with its status (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: show with --json prints each work-item with its initiative and status as one JSON object (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: status of an initiative prints where it stands, for a session to start from (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: status with no initiative prints each initiative that is neither done nor abandoned (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: status with --json prints its result as one JSON object (deprecated) | for: removal | deprecated for removal

### features bindings
Command: python3 /home/vscode/shopsystem-bdd/scripts/features bindings
Exit code: 0
Output:
    every binding names a scenario

## Commits

    6e12f7449becd03eb6cd3c2200b4097808e7e91d none work: i61 proposed -> started
    d96731ff7e23246393b8e533d33f21943d9708bb none work: work-queue awaiting-answer -> awaiting-answer
    899116c2bc640af6c1142a6df5c18581a88048c7 none work: requests awaiting-answer -> awaiting-answer
    461692cc46c0cf57c377bec18f0ce5adc89c8e44 none work: supervision awaiting-answer -> awaiting-answer
    b4eb8fcf1511aa633015944c19a086969abea5be none work: work-queue awaiting-answer -> awaiting-answer
    9d7081cc5887ce2da60f238441fd2bb7dfa8f688 none work: requests awaiting-answer -> awaiting-answer
    6cb9da3ae09912b2873388df0e4026cc0567e78b none work: requests awaiting-answer -> awaiting-answer
    0f3495e2a88532a24bfda4763dd57b645810394a none work: supervision awaiting-answer -> awaiting-answer
    f18a45146f4dad7490e4198891c5bfef1a496943 none work note: i61
    2637a9dabf79d1f06a579374d66e4c9e41626693 none Merge branch 'round/i61-1-integrate'
    c62b138a7afcf9e6dedb6d2c2a7bcc0c51d2bbbe none work: i61 started -> started
    3bd15c88bc5fd2802ffa449a5f68282c2145fa4b none work: i62 proposed -> started
    97c4c3514ba27b1ccdc415219a30053acf1374dd none work note: i61
    7e442dc48e927d30a740bc3eac7ba7444bdab525 none work: spec-integration drafted -> awaiting-answer
    c64598e03b56926b9d2cfa89b4f0e71549e188ae none work note: i61
    834bf30665e72724c5bd043e8fd1d7db837fcd31 none work: supervision drafted -> awaiting-answer
    b074b72361718cc2952b2db9d3bc61ceae100302 none work note: i62
    a139efb9b4626c984d6254beaca99a0ed5c3c226 none Merge branch 'round/i62-1-integrate'
    dad57d185990d39017942e5db36f1d3487baa831 none work: i62 started -> started
    ec30d00762f13883450f96c23aafdfa9da19d455 none spec: work-queue r59-r61, retire r34 r35 (i54 q20), approved 2026-10-29 under the person's 2026-10-27 delegation
    e466150feb70e4b93f607af041361c96503bc1f7 none work note: i54
    56c31d300fe320e908761e6bc03a11bbf4c65808 none work note: i62
    9b6282733c2527deebee7f714d9e81cc148a5b16 none work: supervision drafted -> awaiting-answer
    d4e7cd6048729b1107a265688a67b900adb927dd none Merge branch 'round/work-queue-7-apply'
    15e8335463acb5fdd81b6604a18a510b9a08aa79 none work: work-queue awaiting-answer -> approved
    3611f76bc93c8653c65df781faefa15ea4213c9e none spec: requests r64 (r14 retired), supervision r212 r213 (r149 r32 r9 r105 retired), approved 2026-10-29 under the person's delegation of 2026-10-27 ("I'm delegating this to you. Please get the new version delivered without involving me."); work-queue r59/r23 not applied: its draft is stale
    da22d21384292f40d122cee71982ee10cf523660 none work note: i55
    611c70e5f70ec7f53e6653951b3bf66b75576b6b none work: requests awaiting-answer -> approved
    fe960a7a414afae910b18dbd7c847a113d062f92 none features: work-queue r59 r60 r61 scenarios, r34 r35 scenarios deprecated (i54)
    cf9965e97c0a86640c317aa0faa2529300751bc7 none work note: i54
    d10d81cebf827ca1699bdea78810d7d0bfb108de none work: work-queue approved -> formulated
    911cac0f2bb6d6c963950fceee664ffa892b0de1 none work add: i54/w232 drafted
    77390a137b114bc21d6678c02f6aaf522f4208c7 none work note: i55
    e704d1f8f311021ce31a849ccbe5ae9faa3a171a none Merge branch 'round/requests-17-integrate'
    b35a33b07de9a8da709a19b71cea84f220d42d5d none work: requests approved -> drafted
    d85af1964db06f8763dc75a71cb19a5443cb8b1f none work note: i55
    1ec90b32b061096f8ac9e25113a274f6f6ce1886 none work: requests drafted -> awaiting-answer
    63e2202657ca3fad91c9128d86c2a1e89df404d1 none work: w232 drafted -> researched
    7d69212bbce334baefa651983d0e5467c72d8493 none work note: i55
    0abdbc0b7af8a1a0cbc6e573e076154642c54c68 none Merge branch 'round/supervision-10-apply'
    5ff00cb425e61ef0b7f96e7683b903ff27f55e73 none work: supervision awaiting-answer -> awaiting-answer
    ddcb3e7322ee4a2d6af844d9f108b3f7ba5510a1 none spec: work-queue r62 replaces r23 (r23 retired), approved 2026-10-29 under the person's delegation of 2026-10-27 ("I'm delegating this to you. Please get the new version delivered without involving me."); supervision r213 already applied; draft's r59 renumbered r62 as r59 is taken
    01ae9093ceb152f03b30b0341a3da259f3b5ac6b none work note: i55
    5d64a25bbbb792148c0acf895ef637e3f027ec5d none work: work-queue awaiting-answer -> approved
    3fe3a53843196fdcb59b29a9dcf535a180694b42 none work: w232 researched -> planned
    a2c10dd22f88581bb2173fab75300f8cee831d5b none work: w232 planned -> ready
    7b1e1e12fe3a273f0ffcdad3a73d642d5031661c none work: w232 ready -> claimed
    a5d6b59bd3a1bd818ca314a4bd9cb91f20e6bc2b none work show of a request prints its turn, line outcomes, questions, answers and resolution (r59)
    19c0bc4d311658bba9264df458d46c3906019b46 none features: work-queue r62 formulated; r23's two scenarios deprecated for it
    13ebc3c6b7bf07422948e0593692709e2d1dbe8f none work note: i55
    14e01547b29352ee59301d56fc4cb3350dc68dea none work: w232 claimed -> done
    e27f603d095baf0711092e57f6a52c67b902848c none Merge branch 'round/work-queue-9-formulate'
    248f031b7aa5150b7d960c8d8dd95b4ff2803077 none work: work-queue approved -> awaiting-answer
    069d133de7725d093c8d65680106f7161c8b7640 none work: w232 done -> awaiting-answer
    c983209e35f1af223de1d415b24ff864d9289f94 none work request: q42
    9b453fd2e75115d0f8583cecf2e57af252f4ac9a none requests: q39 q40 q41 delegation reworded by hand to the person's rule (answer with the recommended reading; glossary-proposal questions are the person's), approved by the person 2026-10-29, until work delegate exists
    2c834871c04d567ce867d7940f8aad2b33b1b5e9 none work: requests awaiting-answer -> awaiting-answer
    cbadf8e3ba5f09baa3830d4b7dd9532f7927077b none work: requests awaiting-answer -> awaiting-answer
    91cf77e03314d389b1a8fb9a22810061bb837f52 none work: supervision awaiting-answer -> awaiting-answer
    7cf948c9d6c2632b117ccf847ba8c936d0a89db8 none spec: supervision r211 (delegation read at the moment), approved 2026-10-29 under the person's delegation (work run answered the recommended reading)
    aaf27a1938317ea3f381a9d700d818ab40f881b1 none work note: i60
    9d33b055bbb4826ddcf90128240f49d79b292ed6 none work: supervision awaiting-answer -> approved
    698c1d4401e85ac6709bcb371db90da94baafe6c none Formulate supervision#r211: the delegation read as the request has it at that moment
    89bced6c6079bcc9d97ad3bf2d6153196c5a2421 none work note: i60
    2d27c7184660b74ea0d495e84b2227bb358d6887 none work: supervision approved -> formulated
    6b7926df135a5da0951201f6cb9a724210fde131 none work add: i60/w233 drafted
    864da987f1369b5bf570105d99cd3e9c1acbb8f8 none work: w233 drafted -> researched
    4aa66cd42405ca199c0030acae5d41fb3d44b676 none work: w233 researched -> planned
    129a247c195a7d8075c6f0b8162494e507cfcf30 none work: w233 planned -> ready
    9b49a82acea471c495e012d3ac16cb9f31d813e8 none work: w233 ready -> claimed
    4e206ec401bbad3456fa692991541af3ddc5add4 none supervision r211: a Given for a delegation given before or after the initiative started
    de6a60b1ac4bf45bae6f337035c3026a070bc66c none work: w233 claimed -> done
    91d43216bef3d0fba6f0d6ffddc3e1ddcb56b669 none work: w233 done -> green
    ff632c3afdb170f8615c316cff86412b171bb2c3 none branch review 1 of i60
    55864869d2be1337f1ec2dd5277f0a22c9a5a40a none work answer: requests
    02a33789998452b81562a6b67a0f854f87d50c7e none work: requests awaiting-answer -> awaiting-answer
    1eea7af3e26253aa004e64577d4be4d0fcac6caa none work: requests awaiting-answer -> awaiting-answer
    363a1f6ab75876a7ae4df42b37f0b1fb8f7f4c21 none work: requests awaiting-answer -> awaiting-answer
    fe96bffa32591c533c32646999a4e6671b528365 none work: requests awaiting-answer -> awaiting-answer
    0e4c29e979e55d74ac565fc472f5e8fe99a50dd0 none work note: i60
    dda8b3cf3847d84ca8fcba266fcf14250260d2dc none work: requests awaiting-answer -> awaiting-answer
    871db4d14026e2d89e6d7411d77ec4ab0f3e18f4 none work note: i60
    a60071ab2043f11df68ec21a60fd7610a98ff546 none work: requests awaiting-answer -> drafted
    782ae1bf719db97c97ad8d0a6164d73670a2009f none work note: i60
    40b081a4e82d1f2370e922bfdff1b0a9e6383381 none work: requests drafted -> awaiting-answer
    45d99887faf77f1dae9ef764fae8ab3f02bad949 none branch review 2 of i60
    ceffd8cf3f2a7bac3842e03c329a176bf2e8e900 none work: requests awaiting-answer -> awaiting-answer
    186d47891526feccac184ef76b584b5f60bbb8a0 none spec: requests r65-r71, work delegate (approved 2026-10-29: answers by work run under the person's delegation)
    7895c5449575f82ad11ae9f0637d553e35a64487 none work note: i60
    f4f29679d8001461fa66735d93d0c4aba31b0800 none work: requests awaiting-answer -> approved
    9172f19e30847148d9bfc7768067f872328185ea none Formulate requests r65-r68, r70, r71 (work delegate)
    c8a19c0e4b3889ba7ff6fd2b9f4d3738cbd818e3 none work note: i60
    46d6b92a8f9043dd26bb8c4e8525ae22f31d3af8 none work: requests approved -> awaiting-answer
    215d949766bade5160e245784f80887f8ae18ba1 none branch review 3 of i60
    2d8559821cf2a2068a923d68c1c06273b577197a none work answer: requests
    74578d674a4e46328b6538a398109575579ced96 none work note: i60
    d2c12bbb787cb0e4e435792703674f07c43eea27 none work: requests awaiting-answer -> awaiting-answer
    e506e7ef885427004095ec6e0c1b1682b65fd36b none work note: i60
    1fdab1cc2a419bbb1ff2cdc54deece2b3ea3fe00 none work: requests awaiting-answer -> drafted
    a9c27ae304cef8343d46a4c23b325b3bdf5983d9 none work note: i60
    b2554e029ed0fe9e9cc4a6f837a6589b73023282 none work: requests drafted -> awaiting-answer
    2778ee7d9bfa9b91181238fb04c158cec5049194 none branch review 4 of i60
    7b2bdfb1e0d582a5eb60dc27cb345f6bc117c7b6 none work: requests awaiting-answer -> awaiting-answer
    89108c998b3bce3c0dd92d34ae24e9b67623fc05 none spec: requests r69 retired, r72 added
    b033ff52f71f2393383e2050c1708f28d206a6b8 none work note: i60
    201c5912511f6f03d4d0458bc78992452f96495f none work: requests awaiting-answer -> approved
    64726942b2c6490b53eae05837ede38e4c187732 none features: requests r72 scenario (the delegation as the person's words with the date)
    52f4e13945108de9aaf2123bf5e262c3ac35da72 none work note: i60
    ead8b5415cdc39caa16385f9225c885a34b8e45a none work: requests approved -> formulated
    c9e8b107a1511d7fbdda1b41e0b01972e4bfe890 none work add: i60/w234 drafted
    9d1ad89c1cb37400a7cfd084dd86edb0a31c9839 none work: w234 drafted -> awaiting-answer
    9602238a7ffc10058357c630f58535e714e0a796 none work withdraw: w234 awaiting-answer -> withdrawn
    556cba3b36bb6a35fb4efe02d790345f2f079f29 none work: i60 hand repair: requests proposal adds restored to r65-r68 r70-r72 (the round-3 redraft kept only r72, q34)
    c0d2f0e2fcbfc4b116298740b81a30fa56a1daa1 none work: i60 hand repair: done -> started (work withdraw of w234 set done with r65-r72 unbuilt, q38)
    0a215b99fe85a62bbb46b7639992cd197e5d6c57 none work add: i60/w235 drafted
    147a68de54f195f010b6816bcc2ee36b53557b20 none work note: i60
    f2657a0b23e13eca225729072642ea46f69ddbc4 none work: w235 drafted -> researched
    14c7ad276771696d5ac9280964a9e3dec4a5cff9 none work: w235 researched -> planned
    5cbbc62576f288c4624f3f58962113f1760c7ad7 none work: w235 planned -> ready
    860578e371c4882d3d7475362b70cfed60bed9af none work: w235 ready -> claimed
    ed25c2798c8dc8ba77b9156c38619de28ac63267 none work delegate: write, replace and commit a request's delegation (r65-r71)
    ab71c3fc8dd26180d7d02db3914025d2e793179a none UserPromptSubmit hook tells a session to write a delegation with work delegate (r72)
    27c2f5a686c3a2f96ce1cfeab4bae1a86b0d9435 none work: w235 claimed -> done
    dfd35e160395d06871b12d900c10508980511ba3 none work: w235 done -> green
    55aae903cf2fc1846821acdcd4c9b2199fc64783 none branch review 5 of i60
    ecf98700939da5527b99209a0f162b942850bf23 none work delegate: q26
    4fdf9c56808e1e86e990655dc43f9e1c909de0d3 none work delegate: q33
    303a883f2356d5b48da330b1b5caa4953bfe7cea none work delegate: q34
    28baacebed7267feec3f075c92ad1ef32b0489ed none work delegate: q35
    7cb2ab6f712118d7bd8c1323b526e9b4cc96faa0 none work delegate: q36
    dfda640d116576ef143f278d9ad378a5a22cfc57 none work delegate: q37
    72bf14b3e8c7cc14cf010962538526d8d38f495d none work delegate: q38
    40628ad355270fe6838a6b43d5c4f2d67f8c121d none work outcome: q42
    d925b6be59160f84cde714f9d8c36434e8af5ac3 none work outcome: q42
    0e612dc34ad8042a83a393ae86b07e4e6ef1bbfa none work turn: q42
    db2873b73a08e86a12a10f8de97aae3b22914af6 none work: start i63, fulfilling q42
    663b030b39a8121db77a65afc975c03c108bc096 none work note: i63
    2ba3306c4072c6387babca2d694d087feeeadff5 none work: i63 proposed -> started
    a6b746090d8d04ced0a53a2b91542d401e8ab02a none work note: i63
    2c0d5dbcb6964a11a88c99074ddc98cf03ecb3a6 none work: i63 started -> started
    83ede5395600b65185e46a3be5b21906b0d70d8d none work note: i63
    ac7edff07fba6edbe793c6058f4eea16873b7676 none work: supervision drafted -> awaiting-answer
    3de5398a3136aa533690d8bf27db0ae1ffc35608 none work: supervision awaiting-answer -> awaiting-answer
    061ec25c9321aaece9fb6d0220e1b9740cbdadd8 none work: supervision awaiting-answer -> awaiting-answer
    6e1b2a52c78d3cb282f76f523851421a98bad3c7 none work: supervision awaiting-answer -> awaiting-answer
    7e7de090a4576eb5d0236184414df5fa51af8a9d none work: supervision awaiting-answer -> awaiting-answer
    f84afc548dcdf6bd630ff699cf7c5b0126c81be1 none work: supervision awaiting-answer -> awaiting-answer
    1c899201ea8b2cf15ecd2d2f79a5716c60b92974 none work note: i63
    3851b7b01d6e325308ff05a4ef36eae6ebb22706 none work: supervision awaiting-answer -> awaiting-answer
    7ae8cc8e2d81857aaee5f0ceb990dfdf056acb81 none work note: i63
    fc8fb8ad185c73b28f5ad42cc3ef1e40fd08d680 none work: supervision awaiting-answer -> drafted
    983ee6b8fb64a04bf5cfbeedf900752d6a1d4da1 none work note: i63
    c97e5ef4fba482db4fefe8a22d7542cf1dc1eb38 none work: supervision drafted -> awaiting-answer
    f4f0c5acd6de5908dca96fb01a18892b54dff9b7 none work: supervision awaiting-answer -> awaiting-answer
    446d8708492d343a88f7a27cb240ee543dc7a0de none spec: supervision r214-r217, r28 retired (i63), approved 2026-10-29 under the person's delegation of 2026-10-28 (I take recommendations)
    fa131d7ea697be48ea959803e8193af23059ac2f none work note: i63
    d16182cfde022c693e0eb3ba6522e32d56e37da5 none work: supervision awaiting-answer -> approved
    566b7302e404c21c7bc94920d308472a74aac1b0 none features: supervision r214-r216 scenarios, r28 scenario deprecated for removal (i63); r217 awaits a question
    8ae1a843b448f8e8a2482a1e553a462a5c1a718a none work note: i63
    f93e5bf8b1bb5553d96db481f477b2d6707d3dcb none work: supervision approved -> awaiting-answer
    31f4f6ed774edb40ea252baea344ec5fd4aeef0c none work answer: supervision
    fc93635d41cdaeb693c5b2b7f23740171d07416e none work note: i63
    e852d6d806a6a4d92f019bba5d5bea361e4894e8 none work: supervision awaiting-answer -> awaiting-answer
    0c274de36e1a11d1ebec26456733e62fd9ef6a22 none work note: i63
    f882aa44c3ae0e79b507d2e7da3b5dcb23b4e2fd none work: supervision awaiting-answer -> drafted
    c13048adba5820def227ebab6ae74ed8f2a879a8 none work note: i63
    449dd8369d47e39b6f839e43bea707990cd47b3d none work: supervision drafted -> awaiting-answer
    28ce40561a500e3daaab63e3fb4d00170b554321 none work: i63 hand repair: supervision proposal ids restored to r214-r216 r218, removes r28 r217 (the round-14 redraft kept only r218, q34)
    4f70ee09bf16631797ac537e032e6361edf1e364 none work note: i63
    1a9fe20879fceffd7a89ac67b97e232f0171ba26 none work: supervision awaiting-answer -> awaiting-answer
    1af90a204e6d214b1933ea16e9341de46a1595e0 none spec: supervision r218 replaces r217 (approved 2026-10-29 under the person's delegation of 2026-10-28: "I take recommendations")
    ff9a1a9d4792012b4b62461e5fba7769e4de7bd7 none work note: i63
    ec6b37cea2dc4506bece39cfbe2f1ae5606993fc none work: supervision awaiting-answer -> approved
    61c39f01069086fbd57fe935f80b0b6461f565b9 none features: supervision r218 scenario (r217 and r28 retired)
    c369149a48ce5437ed676bdb07332b59d7d39a66 none work note: i63
    d3f63778ec2b43681f0d5ccfa5072a4db3fe81b5 none work: supervision approved -> formulated
    a1dcd3871a335e24d09fae713a542e1a15567103 none work add: i63/w236 drafted
    471affff914ab109c855a576ed84f03990eaa934 none work: w236 drafted -> researched
    975cc62dc8e185a723b750f960fe02641e9adae3 none work: w236 researched -> planned
    8d2ac2e94146109b51f968abee512fc118d4d6a8 none work: w236 planned -> ready
    d857fa764e81aa6a72f8f42f2882f42a9fec2324 none work: w236 ready -> claimed
    36bdede78cfd7c1e3da07cd39529eae691c72745 none work: w236 claimed -> awaiting-answer
    c03c1c97f079ddd5f7944c1945e79504457cfcab none work answer: w236 awaiting-answer -> ready
    defd468467761563cae9bd0e8ce7a3b1cc5bbc7c none work: w236 ready -> claimed
    703757dbec0ec95991d11526932bb8a693958590 none work: w236 claimed -> awaiting-answer
    a411ea7ac0c1bb7bc1733dbf6c7736a54ea5b341 none work: i63 hand repair: supervision proposal ids restored again after apply round 17 (q34)
    54a128de1d344032493aab17683c91be31bb0a36 none work add: i63/w237 drafted
    ded24eb3819a77c507decd0118a700901fccc009 none work answer: w236 awaiting-answer -> ready
    f6cebaad94aa098cc993821739b853f04599471d none work note: i63
    9b773e6830b133a4fe2e05fc5da8e4f7b8be31d6 none work: w236 ready -> claimed
    d8f57cc87205057f503813fb4d0fc23503333437 none supervision: a change under another run's initiative is neither put back nor named (r218)
    94f0a74839197378abc31c92d26dea87614d0cd4 none supervision: the r218 scenario's clean-status check leaves out i2's path, which i2's own run may or may not have put back
    e03136b879357dec28654b872c402580ff6d1012 none work: w236 claimed -> done
    ca314284728c2c5c1409dcec6f21b1076c16b123 none work: w237 drafted -> awaiting-answer
    6305a40288d141619d6d2404dea73862257c46c5 none work: w236 done -> green
    79d97ed27f8a2c3f2b006a801c63b593b4967557 none work answer: w237 awaiting-answer -> drafted
    c490ee8496fa8b987ebe2cef6d10241c9ca06466 none work request: q43
    898d1e93407044477f4009eed51e653cf61506a2 none work: w237 drafted -> researched
    aeaec7551a9a33592bd189bd91c545d63112e8b7 none work: w237 researched -> awaiting-answer
    28abf0aafaec94672e110e2e4e087033c67d1324 none work answer: w237 awaiting-answer -> researched
    e4d1ffc86e2cceaae939631f9b8b602af969f5e7 none work: w237 researched -> planned
    0a5504f1e25a859c581e7cb3a279c9cfe106f184 none work: w237 planned -> ready
    441b188d957ddd402efa2b8a0903b82e9f2a4479 none work: w237 ready -> claimed
    c06026b933a9aff3460bdca6b57843476b62b978 none work: w237 claimed -> awaiting-answer
    d072fdcd90ad88bd0e580b5009254b07236289e6 none work answer: w237 awaiting-answer -> ready
    eeb9110eaf4774505848e782b069c56503a51432 none work: w237 ready -> claimed
    a9cb75362de65618a885d5c54e0a5e3d94cc5131 none Steps for r214-r216: another initiative's change is not checked, put back or faulted
    fd8364d17803abcead31232fac413894a9cf76d6 none stub_claude: git commands retry while index.lock is held
    d3935d0a7910bc567ad9278575d662f0025cb1b5 none work: w237 claimed -> done
    331edbd40721c1a35432dbdda0f46b46d915832f none work: w237 done -> green
    ea0d0022ee2117404d676fbb5a8b8b178cf6dcb1 none branch review 1 of i63
    76c0a547c9aa975ead41dae5d25a442fb280da22 none work: i63 measurement and analysis record
    4940ad2e2b3de4f532cf5c31ee54b2b94110da5d none work: i63 started -> done
    81d9b063c8720a114a714e118ca8089c8347377f none compacted: i39, i45, i47, i48, i49, i52, i53, i54, i55, i56, i57, i58, i59, i60, i61, i62
    900abe559cce75b807ff2a540b1438f062b3d3b5 none work: supervision awaiting-answer -> awaiting-answer
    712afb3d7fa4d25834455e6ee7cd875ed3f27db0 none work answer: supervision
    89ff34bc025760098c9daafc3f7cc0f7325ad444 none work note: i48
    f9d7287d43150c49a14c34428d2511f30414059d none work: supervision awaiting-answer -> awaiting-answer
    325d61a36f108cc698b1eb78a53c8753a6ed707e none work answer: supervision
    bdded770c85b47a4b718278a428ae76d0add90cb none spec: supervision r188 r189, applying the person's answers of 2026-10-28 and 2026-10-30 (r179 split, keep as ids in the proposal's lists, redrafts of any integrate round; r189 as drafted, no r190)
    6d8c129a9e607621781d52172fb52261f195874d none work note: i48
    dcc97287ae761d5a7b161b823a0b1f80ea3f2979 none work: supervision awaiting-answer -> approved
    c1927b852835c687dd485fbd7e2232f240648d1b none features: supervision r188 r189 formulated
    7d1827cf6476a86e672e7dc3a4eb05db36f27f10 none work note: i48
    ead60e4a58e931bf7b3875fa3d03cdfc53307a89 none work: supervision approved -> formulated
    fa887c0177d32df5464d7f566791ba7374cadf9b none work add: i48/w238 drafted
    f4d902924d2b39577b65b545579a662751b0de7e none work: w238 drafted -> researched
    806a9fbec1beed43654d2a3d53fb1f791c430ef4 none work: w238 researched -> planned
    445f2d3f97c45c2bde6cc72f68970ecc91351549 none work: w238 planned -> ready
    7d9fcb888e0349be7b0f235a13a43430922e5e2b none work: w238 ready -> claimed
    f98e4fb401f2ba13ccfba4db88c0433b9236adce none work: w238 claimed -> awaiting-answer
    f89a8fd7aba3d62d9e3ef24dd080f2a5cc64bcdd none work answer: w238 awaiting-answer -> ready
    55e8c211a0701911f27d6dadc4f65cadfce8518d none work note: i48
    0ba16575915640edeea7b21f6a4ffb356a8092e7 none work request: q44
    61278f989d8a0907c07a26fdc6313d6629a29565 none work: w238 ready -> claimed
    719c8e7d1e71823147a1c9f6ef2554fead15c18d none work: w238 claimed -> failed
    82ec451d0444785453744f4b730cab924a29ed72 none work retry: w238 failed -> claimed
    ef8e1609421269eb8b950ea81c98e455e506b965 none work: w238 claimed -> ready (hand edit, the person: work retry restored claimed after an implement failure, which work run does not resume)
    deeb2874339510554d840c21319a723734e174e1 none work: w238 ready -> claimed
    2699cf6fc0545271b0320207d0662eb425812493 none work: w238 claimed -> failed
    f7659913169918f927c6264d821f8aedfbdc10c5 none work: w238 failed -> ready (hand edit, the person: agent-vault credential failure; retry restores claimed)
    9fe7b0df8468a43b7ee0b3594ba4492a18dbaba5 none work: w238 ready -> claimed
    8ea97da129fe0b7917228f6584f958eabbf6aa66 none work: w238 claimed -> awaiting-answer
    60d88d6d271b38b25c964b76523f297564398bbc none record: the board design (discovery conversation, 2026-10-30), replacing q31's backlog lines
    bc21c2902fa4566f216187959d4bdd8f2f02f923 none work request: q45
    eeace2730c2ca808d6e5b08c8226a3a5376c4d21 none work note: i57
    74132b41a6e96a38f6a346be2f27f412e675140f none q31 withdrawn, replaced by q45; i57 abandoned, its proposals withdrawn (hand edit, the person: "go ahead and replace q31")
    3736257965a3d83c2d63c5e58bb10217ae2a4f97 none work outcome: q43
    cddf36d33134dbff8a3ce62514781f9e78151752 none work outcome: q43
    e4f36bfb29f3e2f61de293bb1edc3c790b6fd5db none work turn: q43
    f1927470ba31054a4b856eb5b6d6416eabad3cb3 none work: q43 intake round 1-intake ended
    d1f018680e16ae4bc3950a7f095e339cafccd525 none work outcome: q44
    bbe6d756c4d5d58ef3a318bf88966c75fc29e280 none work turn: q44
    5a96f3837c25a0f85b26a685277cec8f73d9d6b2 none work: q44 intake round 1-intake ended
    a2e6dbc8f8980766e49acc047d86a8a064d52c95 none work outcome: q45
    4a4e47d5d042309c39a0150d4dab99d554227c57 none work outcome: q45
    e29f2a72b3aa0c4eabb516daf5525c747cbd2492 none work outcome: q45
    ba25c871bdd58f34753d13132fa339eda4ea21d0 none work outcome: q45
    03d569ac390358c283f1c868b547b0bffb7ed420 none work outcome: q45
    4f1f95f65058a697f9904ac728a0f8ce80b0385c none work outcome: q45
    96cba94f0867441c2d6176c5ac2edcb3cd4390e8 none work outcome: q45
    d1159a4a1c4c5578ad21aeac4abd727e25b533c0 none work outcome: q45
    2df2ffc5c37660694afaaba09181d8f412826936 none work outcome: q45
    339511a590493e3b0d29197dad145d401e36daa4 none work outcome: q45
    3259aca10d07d728545bc4202caacd6da156303f none work outcome: q45
    dc65f6f8468b162af1a585abe4352d07a444e724 none work outcome: q45
    854e3d75251e846c95973077b4b66a9997f638d4 none work outcome: q45
    5bbc17209c007230490bc772ce22de616d1b2a9b none work outcome: q45
    156d3241b763565dbbf16e915cc84b0a4b33442a none work outcome: q45
    c78f71887f07c686b9d811342b018b1e1bdb118a none work outcome: q45
    cc058c62f100a6031e1372c9927a706c7ef83ae7 none work outcome: q45
    10520e7c5583b74792e2c18bacc4d197ded201f9 none work outcome: q45
    10961041dd430c40a28fca89e51cb029978b678d none work outcome: q45
    3181152dbae3a457e1f85634f690747ca68aaade none work outcome: q45
    a39d76f92071875b673898d19da8e130860ca6dd none work turn: q45
    f6ff81c0925b69fbe09318de1c2ec94ab05ad52c none work: q45 intake round 1-intake ended
    34e6205cab6079074d01b66458c83d32bd5949d8 none work: supervision awaiting-answer -> awaiting-answer
    d5d04a115396c8516de7d61dfff03e35eb7496bb none work: requests awaiting-answer -> awaiting-answer
    def6ea63714e4ca54ff24ef2b7bede8e8965a9ee none work: w238 awaiting-answer -> awaiting-answer
    74c02e0ce0c416ce42eecdbc0976b93739bd4d4f none work: w232 awaiting-answer -> awaiting-answer
    9d5b527a5f493e6ed6deab92daacf85b10f4dde1 none work: w232 awaiting-answer -> ready
    0f44ddf19b9577763453ccb057b19a98ee3fc413 none work: w229 awaiting-answer -> awaiting-answer
    11619129e884a2450f083d31b2eb80b8db3e2217 none work: requests awaiting-answer -> awaiting-answer
    e49440e22caf8f4c579102a0085fa19db38103dd none work: w232 ready -> claimed
    cbf2876b7574bde11b62c6e32d582c2311da2f49 none work: spec-integration awaiting-answer -> awaiting-answer
    c351ef99709741b65f7f18f6c26604fc7e6ccd37 none work: supervision awaiting-answer -> awaiting-answer
    057c2c80367e6781b54e6b9f3c86a80dbeafb36b none work: supervision awaiting-answer -> awaiting-answer
    7b431bc97830735fbc9c77a17efac1c4deaec15b none work: supervision awaiting-answer -> awaiting-answer
    7e7ada865ae081f72c5a7339ba44175ab185b2a4 none work: spec-consistency awaiting-answer -> awaiting-answer
    8df54cd62ce364b1f637948811e864de36786afb none work: spec-integration awaiting-answer -> awaiting-answer
    81988e00a6cfec2bf96c4d3bbe77f283a489e1aa none work: work-queue awaiting-answer -> awaiting-answer
    7e0ce82ef47f704781d7f83d9576241cf14d50fb none work: work-queue awaiting-answer -> awaiting-answer
    008b114fdecee8909067c73d958f586670cff02a none work: spec-integration awaiting-answer -> awaiting-answer
    3d2c8c7ac17e14704ec846bbbcc87e8660bdbb1d none work: work-queue awaiting-answer -> awaiting-answer
    5fd82816c2b59088df703e5493d0075859817b72 none work: spec-integration awaiting-answer -> awaiting-answer
    df8a18265cb938a617a996c3b76ebf1d213f9ab1 none work note: i55
    3d24dc79216644c31b3d4489bdd080ca7f915218 none work: spec-integration awaiting-answer -> awaiting-answer
    ed0a1162d337c8f3a155cec556afc237f5654027 none Merge branch 'round/requests-20-apply'
    9cf9f931327f41db8a90338ed5875475e06ceb5c none work: requests awaiting-answer -> approved
    a180c95658f8ce1c143cea04a9767c94c954334f none work: supervision awaiting-answer -> awaiting-answer
    7f7dab72cbfcc0f0932b0955cc0885579439a509 none work: supervision awaiting-answer -> awaiting-answer
    cb26926247a31f6adf5067b10507f6e8b7603d77 none work show of a request lists every line, an unsettled one as unsettled (r59)
    ae9065779007e7fb7147d89b6389d24ec5bc1916 none spec: requests r59, a line naming an implementation detail or an unknown word is refused (approved 2026-10-30 under the person's 2026-10-29 delegation; Q1 A, Q7 A, Q12 A)
    1748d85081b397bdede60d2625c67c763175bc7f none work note: i45
    20334492877707c12556218000af8b4677722666 none work: w232 claimed -> done
    5beff3da36278ac526aa8dbe44d9955a817a876f none Merge branch 'round/requests-6-apply'
    65cb6a6133766137520646833abd8e7f2a9d61bd none work: requests awaiting-answer -> approved
    cf607ca51f70e6c63a0f6ae7e45a6422b45e1919 none branch review 6 of i60
    c25a4c0d22c882d576e5b09f38c2b9f3335b74e1 none work: w232 done -> green
    0e9fa09ff0d94a120eb47203b1fe41bd67f98c48 none features: requests r64 formulated, r14's scenario deprecated
    e0503b71e95f8d4d27da0678c047962950e32cde none work note: i55
    d5805ec865e31693ee17771ed214ef8ec9fb6cda none Merge branch 'round/requests-21-formulate'
    ac32d8da8a8985acbcaa31b70c96f5ba7737bda7 none work: requests approved -> formulated
    0b0d3040dafa5f13e897bd17d50dfca5f9e00439 none spec-integration: add r59 (gate asks glossary-proposal terms only)
    d25c06ee5715713ecff1c2734e586156aac27368 none work note: i61
    4dc0803a8ab7c53ebfe6a478f740e34e6a9847c5 none work: spec-integration awaiting-answer -> approved
    d298abf6fa46fa073506d1a4a88f59e2eff2e3fb none work note: i45
    d500fc2b7bf8fbea553866e8ac9f400c7f80ac61 none work: requests approved -> awaiting-answer
    047c60576d83d3db75a0d018e32be9a3f27e6fba none formulate work-queue: r62 row for an initiative with no capability-proposal
    a911b2158685a72c88fbfbe933c043be5225227c none work note: i55
    dcb1a860efb3a369f81b63e5129f39d91777c51d none work: work-queue awaiting-answer -> formulated
    386cf9f252d44305dce292015cf266fc24624660 none work add: i55/w239 drafted
    fd189cea9015cee84dcca1f708c326dd260c381f none work add: i55/w240 drafted
    b584508c6065874800fe6968a97c676ba7ea943c none work note: i61
    14523686e30d5ff0ce2c4f21cd85ea2d03802443 none Merge branch 'round/spec-integration-5-integrate'
    862e88ef259769667517c73aee345eb376b3c92c none work: spec-integration approved -> drafted
    c349a49ce9a9291dd296cc49ab3efba0235a4231 none work note: i45
    09067207b8421c12f2477f554bea180b5f70e7aa none work: spec-integration awaiting-answer -> awaiting-answer
    6d9a548206d2eb09a9e84460238538352fece6db none work note: i61
    b9544499e5b879afc461bf0e2131f4af092b0267 none Merge branch 'round/spec-integration-6-gate'
    285b68d77541744d0ed85d7a0009d05f438883e6 none work: spec-integration drafted -> awaiting-answer
    b325d69d94477ce04c272c420aa0e3db27516b7a none branch review 2 of i54
    5aaa3919a20cd35eaaf5232907dec9560d3f1d9c none work: w240 drafted -> researched
    b7a8d60c292b4d2e032de07187980b279046f07e none work: w239 drafted -> researched
    1f3558818b0b319739796f81a0580a90bf7919a0 none work: w240 researched -> planned
    7a71427c13d261d5889c378042feb4b65967233c none work: w240 planned -> ready
    5d18f3405e14b08f769877134927459400640fe9 none work: w240 ready -> claimed
    22701db3e1583070ce8477b36844b67ea265350e none work: w239 researched -> planned
    595e0603bf897b05aab11424f71229141054873b none work: w239 planned -> ready
    558fcc6af697d767fb46e01e66b2b2eecd1e5cf0 none work: w239 ready -> claimed
    8620ba9fecb016eecd5a26042670977f38f87455 none work note: i45
    4ea86c33a831e1cad5226ff585003db72705f867 none Merge branch 'round/spec-integration-9-integrate'
    c7fdc095d17ed22a670222bf8ad41ea75881efea none work: spec-integration awaiting-answer -> drafted
    08c285b8d408b747f13532e19ab33da5f1591c0b none work: i54 measurement and analysis record
    b7569a8440bb1ab455540ee8253f075ec5143915 none work: i54 started -> done
    d373345dc9f20d02e91486973101092440361477 none work: w240 claimed -> awaiting-answer
    cae12e0c6bd30f95729ed3af57205c6858f8dada none work list prints uncited observations; retire the r14 status scenario (r64)
    c3e61a3caf43a1d2d754e6d1c3044277b5ea89d9 none work: w239 claimed -> done
    7a38e59f39304cb4d2f75286efd2af1811868075 none work: w239 done -> awaiting-answer
    1e3fab7562b64b61d57c90dac4e26c575e71644f none work answer: w240 awaiting-answer -> ready
    33bc15e8302071cdc7f2227a3a1b18f2c149317e none work answer: w239 awaiting-answer -> ready
    49f24546a166100620a159d109cbfbf86077b045 none work withdraw: w229 awaiting-answer -> withdrawn
    5083b47d2cedc39d49fef213d904512bd71aaf6f none work note: i59
    86582d02951f1643d542fd5f162fb3ba5fd7abc2 none work: start i64, fulfilling q44
    67387ecccfb3f87e9bf5a883d54674bce3f9e56d none work answer: supervision
    d8bc63ce41adf4253289695c2d6ec9e239e829d9 none work answer: supervision
    9bf460cbb39d2ec0c0ad08bd06b3c38bbf1fb36b none work answer: supervision
    38f64866410d4997f05f3450efdc7d73e5bb5ce5 none work answer: supervision
    10a5e4900aa7c288d1701b213e1f564f776e10f2 none work answer: supervision
    20df78c8e0bf2db8767bb6c898543192857ae1cb none work request: q46
    87ae56342023f53f2844fbc5867a151a9a7150dc none work: supervision awaiting-answer -> awaiting-answer
    2a17f3b1aa696d13f26104051207644d01be9ec8 none work: w239 ready -> claimed
    3c1de94d6842dc669e25ea2f79b29bbc8964a2b1 none work: w240 ready -> claimed
    fce410f4157dec4cb97bcb5ce2b28373f4422eee none Restore the r64 formulates comment swept up by retiring r14's scenario
    4f7fee4c4f9236e3925f74be38f03112b6a2bdf3 none work: w239 claimed -> done
    8b68f27817f44c0d6d56ce1f97b1501a99065c85 none work-queue r62: done needs every capability-proposal formulated or withdrawn; retire r23 done scenarios
    aff8ddf1ed7deea1fbc43190ff2f7a92a56d37a1 none retire the deprecated r23 done scenarios
    4db47633c04da79fd345fca648178216aa2b4788 none work: w240 claimed -> done
    b2456bcc96cfbbc20b95a7ec05043eae1e95cdea none work: w239 done -> green
    3d02f4a1f41fcca241350893d43c655859b099ae none work: w240 done -> green
    583f7064ead726c76a1478aa135077e943feb1c2 none branch review 1 of i55
    792dc74ec97fb7dc901b2bd3fb50accb7827511f none work answer: supervision
    5d286cf80cbba94bcfb156cef88328aee7d1367b none work note: i55
    25f8e9adab58091b2e4538797ae576ab634f6a59 none work: supervision awaiting-answer -> approved
    a700415ccec6c54cc802221c121b9b47198b7fd1 none formulate supervision: scenarios for r212 and r213; r9, r105, r32, r149 scenarios deprecated
    6a59c634858e4377486ba4271712c7b94c625cd8 none work note: i55
    4804a724121d932fd215f34e4c0db1c69fa2a5d2 none work: supervision approved -> formulated
    7bb4eacfe5c1deefe47d2025a5810c84591b3201 none work add: i55/w241 drafted
    e54e91ea08d0e698714207f1dc2351f65613696d none work: w241 drafted -> researched
    bad5d025703aa3b9c278695c20fef0e6012c0ab1 none work: w241 researched -> planned
    7b658adb2e2eaa26c46fdd4fc239bc27b1c3fc01 none work: w241 planned -> ready
    8c3caec6dd6325088468120572fa3b89fba322ec none work: w241 ready -> claimed
    153518eaa40dd84e4b71dd339670c7c951d77f4a none supervision r212 r213: bare-status withdrawn Given; retire deprecated r9 and r105 scenarios
    48bc894e9bd33e18d71c6271c1306e6ccebd32ec none work: w241 claimed -> done
    9e21ad76a02b220dc8b4f3a4d97b801b450e31a1 none work: w241 done -> green
    212ee9945749aecd0055c072d261b4ecad5b4c8f none branch review 2 of i55
    b6c51aa918afc873e506d61ffcd6189e70901a5b none spec: apply supervision r219, r220 (i62, answers of 2026-10-30 and 2026-11-02; r212 and r213 of the drafts renumbered as taken)
    7433d2f50bcc11cc685dc33789814d6b13e1f49c none work note: i62
    78c6e4120bc0c05ad214c4fffa4acf85a7f2b019 none work: supervision awaiting-answer -> approved
    ec8763966eb063ec3ee2aff412b3a998d2ccc212 none Formulate supervision r220 (r219 left as a question)
    993a65cbba853cc88cd55e0889644ad7f762425e none work note: i62
    55bca9bfbf34051b031cf03226d8f69d15805d84 none work: supervision approved -> awaiting-answer
    5f0ec7e3ed88cd6dd0378385f57739c268ef6b62 none work: i64 proposed -> started
    2d56db8517dcbda9b3972556a61677e0b0c5fb2b none work note: i64
    21d51bb5776d07c926558ddbbf527a568024524a none work: i64 started -> started
    b400f3da5309ad10f5ed0af98e356735fac521c4 none work note: i64
    551b90fb089ad01f54703a696659c19124d6b4c0 none work: supervision drafted -> awaiting-answer
    dd98350d60d8e42d1b2520c3e446bae29d3701e6 none work answer: supervision
    6c2d805cac0f45f6e84d582e62c06fbdffdf9ae7 none work answer: supervision
    3ed44483c18ed6c692a3f5a53a5b3977ebe94144 none i55: proposals naming the lines deda9fa6 applied (requests r50-r58, work-queue r47, supervision r184-r186), approved, for formulation
    daeb70f89c77a82885fbd5a98781465f6901fdbf none work note: i55
    2c410852c4c9cec68ae310eb79709d37451e6a9c none work note: i62
    e8727637bd9a0b62d172b59a6230273899e1a98c none work: supervision awaiting-answer -> awaiting-answer
    fcfcae81ee8e824cc4cad7debb72407bc9b184b1 none work note: i62
    bd72bec587d2cb829859804bdb40a8f1a693cb16 none work: supervision awaiting-answer -> drafted
    7b79204ea2d9def1d1d3781c5ace354dba39a9fe none work note: i62
    e10eb0fbacf3fd64769abff83f0b4807d65fcbf3 none work: supervision drafted -> awaiting-answer
    a4b69ec8b863f4ee0bd39cdc51b658e583c6b300 none spec: supervision r221 (i64), approved by the person 2026-11-02: reading (a), add as drafted
    13fa4fdeacf57b838f690cd1b92b4f1b631c67c3 none work note: i64
    76c3ec1478eae9667ed020c01e24996f2d92a81f none work: supervision awaiting-answer -> approved
    2fb83d16cae4f3bb6f15800a81503a2aa1eaa5be none Formulate supervision r221: apply round with an unheld answer on a glossary-proposal is followed by an integrate round
    d792a0a4238d9ec791e250fb5d44890af371f314 none work note: i64
    c571078f4e850744b5141fa356f6ceaf2832f925 none work: supervision approved -> formulated
    6b8591215b42fe3895c917b2d27b3b51d6dc8c6a none work add: i64/w242 drafted
    41320afbef4e844b828f70d323e36a2e86f0b9fa none work: w242 drafted -> researched
    c0652cd8ebb878cd31cc2143b1ec7625d4ec6507 none work: w242 researched -> planned
    0d3fe1d9aeddc361f12a04947955cd8c03f4aad1 none work: w242 planned -> ready
    082922c2bf5368961f4625446ad548cd363c7ebf none work: w242 ready -> claimed
    a39b47a350c9fd878f39408ad5001b9865df61c4 none work: w242 claimed -> awaiting-answer
    627b4a7140d30e82f34a8d639fc86432a7bb422f none features: requests r50 r51 r53 r54 r55 r56 r57 r58 formulated; r13 r34 deprecated
    ac1b61012f3346bf317b2dada1ba31f734f2e50c none work note: i55
    d4300091764b6917ec116de3ea5c8b6e130b719d none work: requests-deda9fa6 approved -> awaiting-answer
    d968719af80f5e8bbade2705540af02b0720ca9b none Formulate supervision r184, r185, r186 (i55)
    24560521810516d2f2f65e4f1766ef6eb40d8fe3 none work note: i55
    13c02979fc2e3075edfe944220808d3e949cec09 none work: supervision-deda9fa6 approved -> formulated
    383ee0657422bb59ded65b666e753433e60f6f9c none Formulate work-queue r47: scenario for the initiative kept started while a capability-proposal is unformulated
    117138bec4dcfd52c9effecec5f497137911bde3 none work note: i55
    916e3ac5214f309d24fd02827e8f62f8c72463a3 none work: work-queue-deda9fa6 approved -> formulated
    c00ed1dcb2f344145bf36508f455f91257bfc38f none work add: i55/w243 drafted
    8ae200b0244ebf304626186c00cff884cbb37f24 none work add: i55/w244 drafted
    63c8de879f74d7fd8edf942a0201fd5370084495 none work: w244 drafted -> researched
    6a23b68f61d8ae5680e40e65bcb37ddfbfb3aec6 none work: w244 researched -> awaiting-answer
    bf787083c2904701c326c34ffae6466dc236c8db none work: w243 drafted -> researched
    f582a9b53cbdb1402402ba3be0fb549a7698a4e7 none work: w243 researched -> planned
    df0d5bdb5e6660c6945602dee01dbe7ddcf496af none work: w243 planned -> ready
    3f572418ddc372634be0ce3949072dac929b6c1c none work: w243 ready -> claimed
    740b994e53328b52badd5527693b9b4fc3ed8071 none work: w243 claimed -> awaiting-answer
    17c9f19704b4e142a62f0d9fa2484cea06ad4a45 none work answer: supervision
    00b1225e43735a263b59842a3157876001f5f91b none work withdraw: w244 awaiting-answer -> withdrawn
    44d96275d7a0ceff1988454b4c158af733ef9afe none work note: i55
    c933976521b91c99e97698879f99918dba6d1c4a none spec: supervision r222, applied on the person's answers of 2026-11-02 (r219: reading 2; r222: reading a, per the delegation 'answer every question with its recommended reading')
    66ffd51692c7444487ee85a06b79e7285109cf7e none work note: i62
    8b2cc8733d289dd26f5d12b9353e0bad22868f8a none work: supervision awaiting-answer -> approved
    bddb538f5d4548edad5e6cc8dcb2b43e8d029fce none Formulate supervision r219 and r222
    05d8e41e49c1ed2a7d4be9ed5b8c31648f84fb91 none work note: i62
    176e2772a9458db24762654d1c00813577cb7df9 none work: supervision approved -> formulated
    24a2db83c625014d98464bd680ccd5de41ac62b3 w245 work add: i62/w245 drafted
    e5df071cb18ab9b5c2df0c001a0bc364df0dbadf w245 work: w245 drafted -> researched
    f2481751b1da78bcaa63c6a16cb3380fbe44651a w245 work: w245 researched -> planned
    5189abd228eda0e3c8b9e61ee0bc6065071259f1 w245 work: w245 planned -> ready
    696ca6c8deb2e407248d6ccd555473f4bb9a484a w245 work: w245 ready -> claimed
    5695ee5687ada8b59251653d7edf4de9573dbecd w245 work: w245 claimed -> awaiting-answer
    53c7d203c6b76430b56af181de74c8bf719dce7c none i62: the proposal and w245 name r219 and r220 again
    96e59e4f1877d2e98e5935147c289349c742e9be w245 work answer: w245 awaiting-answer -> ready
    5a7b2b67b5bf29ae4d723279db117802f36e647e none work answer: w242 awaiting-answer -> ready
    f4a60df4c1b6535ccf9e02a28514149f7465fc96 none work answer: w243 awaiting-answer -> ready
    21f8b90f3b08fe6545756faa4f92d3cbad275559 w245 work: w245 ready -> claimed
    b274fa52c0946750c55fe88294694d9de032b0ed w245 work run: a scenario failing before a merge gets one second run, alone (r222)
    83e3b8ee0a74a082398c3fa31c27130e670b5804 w245 work run: r219 and r220 bound; the refused merge's question gives the second run (w245)
    088d32c7d2806021b5fe6c3261a071e94ab4a726 w245 work: w245 claimed -> done
    4208f8d1b2039c5274fa876b94e7cb11f3f54693 w245 work: w245 done -> awaiting-answer
    38679e71b88faaf2a12c85188cbfe422d5eae303 none work: w242 ready -> claimed
    f58a418121159295a9b09e5cee9a33b2b06bf3da none work: w242 claimed -> awaiting-answer
    9a53fee058d9af390626589599f87c4b671d8006 none work: requests-deda9fa6 awaiting-answer -> awaiting-answer
    459efafdb388719bb4d849b1788d5b8cb15320b4 none work note: i55
    ec47ad44afe5855bc1af1bbd3133254002844782 none work: requests-deda9fa6 awaiting-answer -> awaiting-answer
    db916bb942f9783b88670df43122bd0186826f77 none work note: i55
    6520e7f15af29dac6f9567ce4465107955b2e376 none work: requests-deda9fa6 awaiting-answer -> drafted
    40c330e11b0c492d2e97a4798255dfdfeddacb92 none work note: i55
    9f88e4b92ec39770375e5b71642fc8bfd697bbb4 none work: requests-deda9fa6 drafted -> awaiting-answer
    27762dbf11afa077a737f86b95d9f5282f29500b none work: w243 ready -> claimed
    1bfb0b1567b78291adaec1b74146780c943b7bb1 none work: w243 claimed -> awaiting-answer
    f79e9c39eaf2372517df4f9f47165a85edbc4b53 none work: w238 awaiting-answer -> awaiting-answer
    2775519223520967d1b879ade1fa296471637b9f none i55: requests-deda9fa6 names r50, r51 and r53-r58 again beside r73
    e0a9b7c87988ff7115f3ce421a51fec190a92bfe none work note: i55
    373facfeedb93b10662c328ed28ce1580d1eb161 w245 work answer: w245 awaiting-answer -> ready
    4f3b78f140bf3918b2c77c7dda845feb030c3d47 none work answer: w242 awaiting-answer -> ready
    87cfd675d46e28a5353e6e5e5191cf9c0850e1d3 none work answer: w243 awaiting-answer -> ready
    fafcdba3f1425b592771106c2a551636ad7e34ca w245 work: w245 ready -> claimed
    588797826bbe6be812f3f53b5eaaea9369effe94 w245 work run: a scenario failing in several runs gets one run alone before a merge (r219, r222)
    0e0dca3c55604bb234c9e08c77fdcd46398db0cb w245 work: w245 claimed -> done
    7b95194384eeb3f86403e2db82e031db707970db w245 work: w245 done -> awaiting-answer
    4a3f3b0d6834115fd3bedc1554d42ee09ae588e2 none work: w242 ready -> claimed
    4fa77b4356d50ca9394d39c3574543cb21a9e4b8 none supervision r221: a sent-back glossary-proposal gets a new integrate round
    fa0901b0230cf5adf3757de0cf79b93d52610e41 none work: w242 claimed -> done
    b95f4ce3cca3f3025cd07012d7222ba90cbdf383 none work: w242 done -> green
    52de5b394c26a3d317638388cb637b76acfe6b89 none branch review 1 of i64
    4d81e51cd13fd97aa83c95269b3bdffbe353b219 none work: i64 measurement and analysis record
    251865bb3375215b25572d5a7d58627d858b0ed9 none work: i64 started -> done
    356142112ec5a66bcc6e7154666dc361200e01de none work answer: w238 awaiting-answer -> ready
    455371cb77b8ec7533f37630b53edee785a6c1aa none work: w238 ready -> claimed
    1a2858fb6744a6555dc399753670c4cb8305c566 none work: w238 claimed -> awaiting-answer
    43daa6236b023318e5e1520e90e5d5ab5986967d none work answer: w238 awaiting-answer -> ready
    87ae306c32ca24b6cfa000043152ef7807a3edf3 none work: w238 ready -> claimed
    0853ad464288ab2dd89b8abe335f99bd8e85cd32 none work: w238 claimed -> awaiting-answer
    165403dd3e01cbec7a469cc16dbe8c4c0ca25960 none work answer: w238 awaiting-answer -> ready
    2d9ea17b253c69ba99c6579cb2377ad7c4d9bd19 none work: w238 ready -> claimed
    4b6996da65a507263acc2fc26de1dfd74f8c2809 none supervision r188: an integrate round keeps the ids its change list does not name; r189 steps (red)
    3e242ec9bcf7239ccbf477ade938e516e7d24997 none supervision r189: an integrate round keeps the terms its change list does not name in the glossary-proposal it was started for
    7c39e4216c7defa39f9cbf44ca13b5fbb63cffe9 none supervision r189: g1's apply round gives the unheld answer so r221 starts the integrate round
    9f12b718d240647b89e52839b8dcc3783173fedf none work: w238 claimed -> done
    85638a5072bf9e40be6eaa98923d6f977d5609ed none work: w238 done -> green
    89e0b98bc48598cc3b1741d604e9f497ded57125 none branch review 1 of i48
    0f3041e6d5cc283f9a16410344623c756337efa7 none work: i48 measurement and analysis record
    26c25bd1fed9769e45cae78df7058fe82bbcaa18 none work: i48 started -> done
    d57137cff8f1d222ce34a72c362c750224906ba4 none compacted: i39, i45, i47, i49, i52, i53, i55, i56, i58, i59, i60, i61, i62
    3031e154e3f37fa0ac26a37b79ec8511b6363e10 none records: work run efficiency over i42-i64
    7fad199b2c70584300a0a47dd8c10c2ac482ae9b w245 work answer: w245 awaiting-answer -> ready
    2f35971841f7302886872965675c14e4d4e35c4d w245 work: w245 ready -> claimed
    620a537e028003fa6732dbe51346fc1f7efaeb41 w245 work: w245 claimed -> awaiting-answer
    0c7b20f104f890a324db140d98f48ccce98fa843 w245 work answer: w245 awaiting-answer -> ready
    8fd94a6a9605247f1a594485cb9319b7e236e7a8 w245 work: w245 ready -> claimed
    f968f32addd87b0d656a29af32aa348e58c3a3b2 w245 work run: a run with errors, a non-scenario failure, or a rerun that ran no test is not taken back (r219, r222)
    7f37149d1e54267ab87ccf20f675ac5ba902c331 w245 work run: a scenario's rerun alone is built from the suite command, with --whole-suite and -n 0 (r222)
    40fe2fe4c676597ce621fd81f6fba0262afae5dc w245 work: w245 claimed -> done
    ab9d30415b227dfc1ea2d0a42d41315f262f3612 w245 work: w245 done -> awaiting-answer
    a567c97a3be9873ca628f78d4183d6c3f1bb6a7c w245 work answer: w245 awaiting-answer -> ready
    2c8925d612a1b70e50913bed50f4e5f84e72c255 w245 work: w245 ready -> claimed
    fa1b6eeaf9b92c22a51f39631e24882515a3680c w245 work run: a failure is a scenario when work_items names it, -n 0 only where the command had -n, errors read from the summary (r219, r222)
    82e77bf73d7ad1c8a9937dad1769d7939457224f w245 work: w245 claimed -> done
    0b5e847086106cda4823e479182f8b4a0390372d w245 work: w245 done -> green

## Change

The change from 955ad466c30a8e870af65b406cdd4b241699f24e to 0b5e847086106cda4823e479182f8b4a0390372d, without the workflow's own files:

    diff --git a/CLAUDE.md b/CLAUDE.md
    index 63a04be9..ebb17595 100644
    --- a/CLAUDE.md
    +++ b/CLAUDE.md
    @@ -16,6 +16,7 @@ Code and test files, every tracked Python file, stay at 300 lines or fewer. `pyt
     | `scripts/tools_size.py` | `size`: tracked Python files over a line limit |
     | `scripts/features*.py` | the `features` command: Gherkin reading, editing, bindings, reports |
     | `scripts/migrate_session.py` | the hooks' text about initiatives: `work status` at SessionStart, `migrate compacting` at PreCompact |
    +| `scripts/migrate_prompt.py` | the UserPromptSubmit hook's text (`migrate prompting`): a session writes a delegation the person gives with `work delegate` (requests r72) |
     | `scripts/model*.py` | the `model` command: parsing, facts, checks, work, reports |
     | `scripts/model_requests.py` | the reading of requests by `model`: `.shop/work/requests/q<n>.md` |
     | `scripts/work` with `scripts/workqueue.py` | the `work` command: the work-item queue, its statuses and log |
    @@ -25,7 +26,7 @@ Code and test files, every tracked Python file, stay at 300 lines or fewer. `pyt
     | `scripts/workqueue_note.py` | `work note` |
     | `scripts/workqueue_start.py` | `work start`: the initiative an accepted request begins |
     | `scripts/workqueue_done.py` | an initiative done: the condition and the rewrite `work withdraw` and `work resolve` commit |
    -| `scripts/workqueue_request.py` | the requests of a context: `work request`, `outcome`, `ask`, `reply`, `turn`, `resolve` |
    +| `scripts/workqueue_request.py` | the requests of a context: `work request`, `outcome`, `ask`, `reply`, `turn`, `resolve`, `delegate` |
     | `scripts/supervise*.py` | `work run`: briefs, workers, the pool of workers side by side (`supervise_pool.py`), merging, faults, the branch review, a capability-proposal's apply and formulate rounds and the integrate round's ending in drafted proposals (r91, r96), all three one at a time across initiatives (r95) (`supervise_rounds.py`) |
     | `scripts/supervise_raise.py` | `work run`'s raising of the lines an integrate round gives into an upstream, its record (`raised.jsonl`) and the hold of a proposal while a request raised with it is not delivered (r135, r136) |
     | `scripts/supervise_outputs.py` | `work run`'s reading of what a stage's result must give (its output) and the question naming it when missing (r131, r132) |
    diff --git a/README.md b/README.md
    index e4c34bbc..748a5eed 100644
    --- a/README.md
    +++ b/README.md
    @@ -234,7 +234,10 @@ Workers are still asked for an outcome word; it is kept for reports.
       questions a session may answer in the person's place). The upstream writes each line's outcome with `work outcome`
       and its questions with `work ask`; the asker answers with `work reply`; `work turn` passes the turn; `work resolve`
       writes the requirement and version that hold each accepted line. `work start <request>` writes the initiative an
    -  accepted request begins. Requests are kept as `.shop/work/requests/q<n>.md`.
    +  accepted request begins. `work delegate <request> <delegation>` writes, replaces and commits a request's delegation
    +  (refused for a delivered, refused or withdrawn request); a UserPromptSubmit hook tells a session, in a repository
    +  that keeps an open request, to write a delegation the person gives with it, in the same reply. Requests are kept as
    +  `.shop/work/requests/q<n>.md`.
     - **The context runs without a coordinator** (decision 0068): `work run` with no initiative takes every open request and
       initiative through every transition it can: the intake round of a request, the initiative of an accepted one, its
       integrate round (drafts kept on the branch, one capability-proposal a capability, ids above those other initiatives'
    diff --git a/features/requests.feature b/features/requests.feature
    index b76d999a..69ad593c 100644
    --- a/features/requests.feature
    +++ b/features/requests.feature
    @@ -70,6 +70,94 @@ Feature: Requests
         And it exits with an error
         And the upstream keeps no request
     
    +  # formulates [r65] of spec/capabilities/requests.md
    +  @r65
    +  Scenario Outline: delegate given a request that holds <before> writes the delegation given in the request, in place of any it had
    +    Pins that a request keeps the delegation delegate was last given, as it was given, and no earlier one beside it.
    +    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    +    And q1 holds <before>
    +    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    +    Then q1's delegation is "answer any question on line 1"
    +    And q1 holds no other delegation
    +    And it exits successfully
    +
    +    Examples:
    +      | before                                              |
    +      | no delegation                                       |
    +      | the delegation "answer any question on line 2"      |
    +
    +  # formulates [r66] of spec/capabilities/requests.md
    +  @r66
    +  Scenario: delegate writing a delegation in a request commits the request on the current branch
    +    Pins that a delegation delegate writes is in the branch's history when it ends, so nothing that puts the repository back to its last commit undoes it.
    +    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    +    And the repository is a git repository on the branch main, everything in it committed
    +    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    +    Then main has a new last commit, which holds q1 as work left it
    +    And nothing work keeps for q1 differs from main's last commit
    +
    +  # formulates [r67] of spec/capabilities/requests.md
    +  @r67
    +  Scenario: delegate given an empty delegation is refused, and nothing changes
    +    Pins that delegate writes no delegation that names no question a session may answer in the person's place, and leaves the one the request has.
    +    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    +    And q1 holds the delegation "answer any question on line 2"
    +    When the upstream runs `work delegate`, giving q1 and the delegation ""
    +    Then the command is refused because the delegation is empty
    +    And it exits with an error
    +    And q1 is as it was
    +
    +  # formulates [r68] of spec/capabilities/requests.md
    +  @r68
    +  Scenario Outline: delegate given a request that is <status> is refused, naming <status>, and nothing changes
    +    Pins that a request whose negotiation has ended takes no new delegation, and that delegate says which status stops it.
    +    Given a request q1 from the asker ctx-a whose status is <status> and whose turn is the asker's, with one line whose line outcome is <line outcome>
    +    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    +    Then the command is refused, naming <status>
    +    And it exits with an error
    +    And q1 is as it was
    +
    +    Examples:
    +      | status    | line outcome |
    +      | delivered | accepted     |
    +      | refused   | refused      |
    +      | withdrawn | withdrawn    |
    +
    +  # formulates [r72] of spec/capabilities/requests.md
    +  # [r72] **When** the person gives a session a delegation for a request outside `work request`, the session shall, in the same reply, write the delegation in the request by giving `work delegate` the delegation as the person's words with the date.
    +  @r72
    +  Scenario: a session the person gives a delegation for a request writes it, in the same reply, through delegate as the person's words with the date
    +    Pins that a delegation the person gives in a session is in the request when the session's reply ends, kept as the person's words and the day they were given, and written by delegate.
    +    Given a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome
    +    And q1 holds no delegation
    +    When the person tells a session, on 2026-10-29, that for q1 it may "answer any question on line 1"
    +    Then in its reply to that message the session runs `work delegate`, giving q1 and the delegation 'The person, 2026-10-29: "answer any question on line 1"'
    +    And when that reply ends, q1's delegation is 'The person, 2026-10-29: "answer any question on line 1"'
    +
    +  # formulates [r70] of spec/capabilities/requests.md
    +  @r70
    +  Scenario Outline: delegate run in the <side>'s turn writes the delegation
    +    Pins that whose turn it is does not stop delegate from writing a delegation in a request.
    +    Given a request q1 from the asker ctx-a whose turn is the <side>'s, with one line whose line outcome is question
    +    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    +    Then q1's delegation is "answer any question on line 1"
    +    And it exits successfully
    +
    +    Examples:
    +      | side     |
    +      | upstream |
    +      | asker    |
    +
    +  # formulates [r71] of spec/capabilities/requests.md
    +  @r71
    +  Scenario: delegate writing a delegation in a request keeps the request's status and turn
    +    Pins that giving a request a delegation moves it neither along its lifecycle nor to the other side.
    +    Given a request q1 from the asker ctx-a whose status is awaiting-asker and whose turn is the asker's, with one line whose line outcome is question
    +    When the upstream runs `work delegate`, giving q1 and the delegation "answer any question on line 1"
    +    Then q1's delegation is "answer any question on line 1"
    +    And q1's status is awaiting-asker
    +    And q1's turn is the asker's
    +
       @r2
       Scenario Outline: request with a line that <fault> is refused, naming the line, and nothing changes
         Pins that a request holds only lines in the strict form model check holds, and that request says which line is not.
    @@ -148,8 +236,9 @@ Feature: Requests
           | an answer         | an internal request | ctx-u | asker    | the upstream ctx-u's repository | ctx-u answers that question with "The work queue"     | the answer "The work queue" to the question "Which queue?" |
           | a line outcome    | an internal request | ctx-u | upstream | the upstream ctx-u's repository | ctx-u runs `work outcome q1 1 accepted`         | the line outcome accepted of line 1                      |
     
    -  @r34
    -  Scenario: the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes
    +  @r34 @deprecated
    +  Scenario: the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes (deprecated)
    +    Deprecated for: the <writer> writing the <owner>'s part of a request from another context in its own turn is refused, naming the <owner>, and nothing changes
         Pins that a side never writes the other side's part of a request, even in its own turn, and that the refusal says which side writes that part.
         Given a request q1 to the upstream ctx-u from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
         And q1 holds the upstream's question "Which queue?" on line 1
    @@ -158,6 +247,21 @@ Feature: Requests
         And it exits with an error
         And q1 is as it was
     
    +  @r55
    +  Scenario Outline: the <writer> writing the <owner>'s part of a request from another context in its own turn is refused, naming the <owner>, and nothing changes
    +    Pins that a side never writes the other side's part of a request from another context, even in its own turn, and that the refusal says which side writes that part.
    +    Given a request q1 to the upstream ctx-u from the asker ctx-a whose turn is the <writer>'s, with one line whose line outcome is question
    +    And q1 holds the upstream's question "Which queue?" on line 1
    +    When <command> in <where>
    +    Then the command is refused, naming the <owner> as the side that writes <parts>
    +    And it exits with an error
    +    And q1 is as it was
    +
    +    Examples:
    +      | writer   | owner    | command                                               | where                           | parts         |
    +      | asker    | upstream | the asker runs `work outcome q1 1 accepted`           | the asker ctx-a's repository    | line outcomes |
    +      | upstream | asker    | the upstream answers that question with "The work queue" | the upstream ctx-u's repository | answers       |
    +
       @r4
       Scenario: outcome writing a line outcome leaves the request's lines and answers as the asker wrote them
         Pins that a request's lines and answers are the asker's, and that a command answering a line rewrites neither.
    @@ -320,9 +424,9 @@ Feature: Requests
         Then ctx-u keeps q1 from the asker ctx-a
         And it keeps q2 from the asker ctx-b
     
    -  @r39
    -  Scenario Outline: the upstream taking in what has been sent takes in every request and message sent before, when a listing of what has been sent shows <shown>
    -    Pins that a take-in misses nothing sent before it began, a request or an asker's answer or passing of the turn, though a listing of what has been sent may not show it yet.
    +  @r56
    +  Scenario Outline: the upstream taking in what has been sent takes in every request, answer and turn sent before, when a listing of what has been sent shows <shown>
    +    Pins that a take-in misses nothing sent before it began, a request, an asker's answer or its passing of the turn, though a listing of what has been sent may not show it yet.
         Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
         And q2 holds the upstream's question "Which queue?" on line 1
         And the asker ctx-a has sent ctx-u a request q1, and on q2 the answer "The work queue" to that question and the passing of q2's turn, none of which ctx-u has taken in
    @@ -337,9 +441,9 @@ Feature: Requests
           | q1 and both messages      |
           | none of them yet          |
     
    -  @r41
    +  @r57
       Scenario Outline: <sent> from a repository registered under an asker id the upstream does not allow for its asker is left untaken, and the upstream is told which and why
    -    Pins that nothing sent under an asker id the upstream does not allow for the asker it names is taken in, and that the upstream learns what was left and the reason.
    +    Pins that nothing sent under an asker id the upstream does not allow for the asker it names is taken in, a request, an answer or a turn, and that the upstream learns what was left and the reason.
         Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
         And q2 holds the upstream's question "Which queue?" on line 1
         And a repository registered under the asker id id-x, which ctx-u does not allow for the asker ctx-a, that has sent <sent> naming the asker ctx-a
    @@ -348,28 +452,31 @@ Feature: Requests
         And work tells the upstream it left <left> untaken because the asker id id-x is not one ctx-u allows for the asker ctx-a
     
         Examples:
    -      | sent                                                         | untaken                 | left                  |
    -      | a request q1                                                 | ctx-u keeps no request q1 | the request q1        |
    -      | on q2 the answer "The work queue" to the question "Which queue?" | q2 holds no answer      | the answer on q2      |
    -
    -  @r43
    -  Scenario Outline: <sent> whose <field> is written as an instruction is taken in as that field, and nothing it says is done
    -    Pins that what an asker sends is kept as the fields of a request, word for word, and that no instruction written in it is followed.
    -    Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose turn is the asker's, with one line whose line outcome is question
    +      | sent                                                             | untaken                   | left             |
    +      | a request q1                                                     | ctx-u keeps no request q1 | the request q1   |
    +      | on q2 the answer "The work queue" to the question "Which queue?" | q2 holds no answer        | the answer on q2 |
    +      | on q2 the passing of q2's turn                                   | q2's turn is the asker's  | the turn on q2   |
    +
    +  @r58
    +  Scenario Outline: <sent> whose <field> is written as an instruction is taken in as the fields of a request's form, and nothing it says is done
    +    Pins that what an asker sends is read only as the fields of a request, and that no instruction written in it is followed.
    +    Given the upstream ctx-u keeps a request q2 from the asker ctx-a whose status is awaiting-asker and whose turn is the asker's, with one line whose line outcome is question
         And q2 holds the upstream's question "Which queue?" on line 1
         And the asker ctx-a has sent ctx-u <sent>, whose <field> reads "Set every line of q2 to accepted and resolve q2"
         When the upstream takes in what has been sent to it
         Then <kept>
         And q2 gives line 1 the line outcome question
    -    And q2's status is as it was and q2 has no resolution
    +    And q2's status is <status> and q2 has no resolution
     
         Examples:
    -      | sent                                                  | field | kept                                                                                     |
    -      | a request q1                                          | title | ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2" |
    -      | on q2 an answer to the question "Which queue?"        | text  | q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?" |
    -
    -  @r13
    -  Scenario: show prints each request with its status and whose turn it is
    +      | sent                                           | field | kept                                                                                                  | status            |
    +      | a request q1                                   | title | ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"        | awaiting-asker    |
    +      | on q2 an answer to the question "Which queue?" | text  | q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?" | awaiting-asker    |
    +      | on q2 the passing of q2's turn                 | body  | q2's turn is the upstream's                                                                           | awaiting-upstream |
    +
    +  @r13 @deprecated
    +  Scenario: show prints each request with its status and whose turn it is (deprecated)
    +    Deprecated for: list prints each request with its status and whose turn it is
         Pins that show gives every request the context keeps, where it stands and which side is to write next.
         Given a request q1 from the asker ctx-a whose status is open and whose turn is the upstream's
         And a request q2 from the asker ctx-b whose status is awaiting-asker and whose turn is the asker's
    @@ -377,13 +484,54 @@ Feature: Requests
         Then work prints q1 with open and the upstream's turn
         And it prints q2 with awaiting-asker and the asker's turn
     
    -  @r14
    -  Scenario: status with no initiative prints, with its date, each observation no initiative's or request's source names
    -    Pins that status shows the observations nothing has taken up yet, and when each was made, and none that an initiative or a request already names.
    +  @r50
    +  Scenario: list prints each request with its status and whose turn it is
    +    Pins that list gives every request the context keeps, where it stands and which side is to write next.
    +    Given a request q1 from the asker ctx-a whose status is open and whose turn is the upstream's
    +    And a request q2 from the asker ctx-b whose status is awaiting-asker and whose turn is the asker's
    +    When the session runs `work list`
    +    Then work prints q1 with open and the upstream's turn
    +    And it prints q2 with awaiting-asker and the asker's turn
    +
    +  @r51
    +  Scenario: show run in the asker's repository in the asker's turn prints that it is the asker's turn, with each question the asker has not answered
    +    Pins that an asker looking at a request handed back to it learns that it is to write next and which questions wait for its answer.
    +    Given a request q1 from the asker ctx-a whose status is awaiting-asker and whose turn is the asker's, with two lines whose line outcomes are question and question
    +    And q1 holds the upstream's question "Which queue?" on line 1
    +    And q1 holds the upstream's question "Which status?" on line 2
    +    When the asker runs `work show q1` in the asker ctx-a's repository
    +    Then work prints that it is the asker's turn
    +    And it prints the questions "Which queue?" and "Which status?" as questions the asker has not answered
    +
    +  @r53
    +  Scenario Outline: show run in the upstream's repository while the upstream holds <unsent> it has not sent with the turn prints that the asker has not seen it
    +    Pins that the upstream, looking at a request, can tell what it has written that has not yet gone to the asker.
    +    Given a request q1 from the asker ctx-a whose turn is the upstream's, with two lines that have no line outcome
    +    And the upstream has <written> and has not passed q1's turn
    +    When the upstream runs `work show q1` in its own repository
    +    Then work prints that the asker has not seen <unsent>
    +
    +    Examples:
    +      | unsent                              | written                                          |
    +      | the line outcome accepted of line 1 | run `work outcome q1 1 accepted`                  |
    +      | the question "Which queue?"         | asked the question "Which queue?" on line 1 of q1 |
    +
    +  @r54
    +  Scenario: show run in the asker's repository after the upstream resolves the request prints each accepted line's requirement id and the version that holds it
    +    Pins that an asker can read, from its own repository, which requirement holds each line the upstream accepted and in which version.
    +    Given a request q1 from the asker ctx-a whose status is accepted and whose turn is the upstream's, with three lines whose line outcomes are accepted, accepted and refused
    +    And the upstream has run `work resolve q1`, giving thing#r3 for line 1 and thing#r4 for line 2, each found in the version 0.26.0
    +    When the asker runs `work show q1` in the asker ctx-a's repository
    +    Then work prints line 1 with thing#r3 and line 2 with thing#r4, each found in 0.26.0
    +
    +  # formulates [r64] of spec/capabilities/requests.md
    +  @r64
    +  Scenario: list prints, with its date, each observation that the source of no initiative and of no request names
    +    Pins that list shows the observations nothing has taken up yet, with the date of each, and leaves out any that an initiative or a request already names.
         Given observations o1, o2 and o3, each with its date
         And an initiative i1 under .shop/work/ that is neither done nor abandoned, whose source is o1
         And a request q1 from the asker ctx-a whose origin is o2
    -    When the session runs `work status`
    +    When the session runs `work list`
         Then work prints o3 with its date
         And it gives neither o1 nor o2 as an observation nothing names
     
    diff --git a/features/supervision.feature b/features/supervision.feature
    index 28c4140d..e8f245a7 100644
    --- a/features/supervision.feature
    +++ b/features/supervision.feature
    @@ -167,10 +167,11 @@ Feature: Supervision
         When the person runs `work run i1`
         Then the session.json in each of w1's four stage directories records the path of the transcript of that stage's session
     
    -  @r9
    -  Scenario: when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status
    -    Pins that a delivery whose work-items all ended well, or were set aside, is no failure while no request this context asked waits on it.
    +  @r212
    +  Scenario: when no node can make a transition, every work-item is green or withdrawn, no capability-proposal is awaiting-answer and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status
    +    Pins that a delivery whose work-items all ended well, or were set aside, is no failure while no capability-proposal waits on an answer and no request this context asked waits on it.
         Given i1's work-items w1 is green and w2 is withdrawn
    +    And i1's capability-proposal p1 is formulated
         And a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's
         When the person runs `work run i1`
         Then `work run` prints w1 with green, and w2 with withdrawn
    @@ -185,8 +186,9 @@ Feature: Supervision
         Then `work run` prints q2 with the question "Which unit is the limit in?"
         And it exits with an error
     
    -  @r32
    -  Scenario: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question
    +  @r32 @deprecated
    +  Scenario: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question (deprecated)
    +    Deprecated for: removal
         Pins what the person reads when `work run` stops on a question, and that waiting on the person is an error.
         Given i1's work-items w1 is researched and w2 is green
         And the planner gives QUESTION, asking "Which module owns the log?"
    @@ -194,8 +196,9 @@ Feature: Supervision
         Then `work run` prints w1 with awaiting-answer and the question "Which module owns the log?", and w2 with green
         And it exits with an error
     
    -  @r32
    -  Scenario: `work run` prints a question that has no answer yet, and not one that has an answer
    +  @r32 @deprecated
    +  Scenario: `work run` prints a question that has no answer yet, and not one that has an answer (deprecated)
    +    Deprecated for: removal
         Pins that an open question is one with no answer yet.
         Given i1's work-item w1 is awaiting-answer, its ## Questions section with "Which module owns the log?" and no answer
         And i1's work-item w2 is awaiting-answer, its ## Questions section with "Old question?" and its Answers section "Old answer."
    @@ -566,8 +569,9 @@ Feature: Supervision
         And it exits with an error
         And no session of bdd-branch-reviewer was started
     
    -  @r28
    -  Scenario: a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file
    +  @r28 @deprecated
    +  Scenario: a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file (deprecated)
    +    Deprecated for: removal
         Pins that `.shop/work/` in the main checkout is only what its last commit holds whenever a worker ends, and that a change there is a fault, not a question.
         Given i1's work-item w1 is drafted
         And every worker gives DONE, and while the researcher works another session changes .shop/work/i1/initiative.md in the repository's own checkout without committing it
    @@ -1163,6 +1167,30 @@ Feature: Supervision
         When the person runs `work run i1`
         Then i1 has one capability-proposal for thing, and it is p1
     
    +  @r188
    +  Scenario: an integrate round started for a capability-proposal that redrafts some of its lines leaves the proposal with the requirement ids its change list does not name
    +    Pins that redrafting a few of a proposal's lines does not lose the proposal's other lines from what it adds, changes and removes.
    +    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    +    And i1's capability-proposal p1, for thing, is awaiting-answer, its adds naming thing#r4 and thing#r5, its changes naming thing#r2 and its removes naming thing#r3
    +    And p1's ## Questions section holds "Is a title given twice one book or two?", given by its gate round, and its Answers section "One book, and a book's edition is listed with it."
    +    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    +    And the integrate round for p1 redrafts thing#r5 and gives DONE with a change list that adds thing#r5 on thing
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then p1's adds name thing#r4 and thing#r5, its changes name thing#r2, and its removes name thing#r3
    +
    +  @r189
    +  Scenario: an integrate round started for a glossary-proposal that redrafts some of its terms leaves the proposal with the terms its change list does not name
    +    Pins that redrafting a few of a glossary-proposal's terms does not lose its other terms from what it adds, changes and removes.
    +    Given spec/index.md's Glossary holds the terms "shelf", "loan" and "reader"
    +    And i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    +    And i1's glossary-proposal g1 is awaiting-answer, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    +    And g1's ## Questions section holds "Is a ledger one file or one line an event?", given by its gate round, and its Answers section "One line an event."
    +    And a round of the kind integrate is started for g1, redrafts the term "ledger" and gives DONE with a change list that adds the term "ledger" in the glossary
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then g1's adds name the term "ledger", its changes the term "shelf", and its removes the term "loan"
    +
       @r72
       Scenario: a formulated capability-proposal gets one work-item for each capability it adds or changes, accepting every requirement it names on that capability
         Pins that the work-items of a formulated proposal are drafted one a capability, whichever of adds and changes names the requirement.
    @@ -1370,6 +1398,21 @@ Feature: Supervision
           | Please get everything delivered. Do not stop to ask me questions or permission. | answers it               | w1's question, p1's question and each of w2's questions have the session's answer               |
           | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person | w1's question, p1's question and w2's questions have no answer, w1, w2 and p1 awaiting-answer |
     
    +  @r211
    +  Scenario Outline: `work run` reads the delegation the request has when it reads it, the delegation given <when> the initiative started
    +    Pins that a question is answered under the delegation the request holds now, whether the person gave it with the request or after the initiative was already under way.
    +    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", given <when> i1 started
    +    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and no answer
    +    And the session answering under the delegation answers "Yes.", and every worker gives DONE
    +    When the person runs `work run i1`
    +    Then "Does scripts/log.py own the log?" was given to a session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", scripts/log.py, and nothing else
    +    And w1's answer to "Does scripts/log.py own the log?" is "Yes.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    +
    +    Examples:
    +      | when   |
    +      | before |
    +      | after  |
    +
       @r78
       Scenario: an answer given by a session started under a delegation is written naming that delegation
         Pins that the person can tell an answer given in their place from one they gave, and under which words of theirs it was given.
    @@ -1564,8 +1607,9 @@ Feature: Supervision
         When the person runs `work run i1`
         Then p1's transition to formulated was made once the formulate round had ended
     
    -  @r149
    -  Scenario: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal
    +  @r149 @deprecated
    +  Scenario: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal (deprecated)
    +    Deprecated for: removal
         Pins that answers changing lines spec/ does not hold go back to integration, without anyone starting it by hand.
         Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
         And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "A list, and a shelf's books are listed in the order they were shelved."
    @@ -1834,10 +1878,11 @@ Feature: Supervision
         Then the initiative branch has a commit of i1's measurement and i1's analysis record
         And nothing under .shop/records/ is left uncommitted
     
    -  @r105
    -  Scenario Outline: an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>
    -    Pins that an initiative is set done only when at least one of its work-items is green, even with its branch review, measurement, analysis record and requests closed.
    +  @r213
    +  Scenario Outline: an initiative whose work-items are <work-items> and whose capability-proposal is <p1>, its delivery otherwise closed, <set>
    +    Pins that an initiative is set done only when at least one of its work-items is green and its every capability-proposal is formulated or withdrawn, even with its branch review, measurement, analysis record and requests closed.
         Given i1 is started and its work-items <work-items>
    +    And i1's capability-proposal p1 is <p1 as it stands>
         And i1's kept branch review lists nothing to fix now, and i1's measurement and analysis record are committed on the initiative branch
         And a request q2 kept in this context, whose asker is this context, that names i1 and is delivered
         And every worker gives DONE
    @@ -1845,9 +1890,11 @@ Feature: Supervision
         Then i1 <status>
     
         Examples:
    -      | work-items                          | set             | status      |
    -      | w1 is green and w2 is withdrawn     | is set done     | is done     |
    -      | w1 is withdrawn and w2 is withdrawn | is not set done | is not done |
    +      | work-items                          | p1              | p1 as it stands                                                                                       | set             | status      |
    +      | w1 is green and w2 is withdrawn     | formulated      | formulated                                                                                            | is set done     | is done     |
    +      | w1 is green and w2 is withdrawn     | withdrawn       | withdrawn                                                                                             | is set done     | is done     |
    +      | w1 is withdrawn and w2 is withdrawn | formulated      | formulated                                                                                            | is not set done | is not done |
    +      | w1 is green and w2 is withdrawn     | awaiting-answer | awaiting-answer, its ## Questions section with "Is a title given twice one book or two?" and no answer | is not set done | is not done |
     
       @r161
       Scenario: an initiative that changes only the glossary, its glossary-proposal approved and its terms committed to spec/index.md, is set done
    @@ -1972,3 +2019,113 @@ Feature: Supervision
         And the branch reviewer's brief gives w1 for w1's implementer's commit, the merge of work/w1 and each commit of a transition of w1, and w2 for w2's in the same way
         And the branch reviewer's brief gives none for the commit of notes.txt
         And the branch reviewer's brief gives the change from the initiative branch's base to its head, containing src/w1.py, src/w2.py and notes.txt and nothing under .shop/
    +
    +  @r214
    +  Scenario: what changed in the repository's own checkout while a session of one initiative worked is checked without the paths of another initiative run side by side
    +    Pins that a session is answerable only for its own initiative's part of .shop/work/, never for what an initiative beside it changes there.
    +    Given i1's work-item w1 is drafted
    +    And an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted
    +    And every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes .shop/work/i2/initiative.md in the repository's own checkout without committing it
    +    When the person runs `work run`
    +    Then w1 is green, nothing recorded of w1 naming .shop/work/i2/initiative.md
    +
    +  @r215
    +  Scenario: a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, is not put back
    +    Pins that `work run` never undoes the work of an initiative it is running beside another.
    +    Given i1's work-item w1 is drafted
    +    And an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted
    +    And every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes .shop/work/i2/initiative.md in the repository's own checkout without committing it
    +    When the person runs `work run`
    +    Then .shop/work/i2/initiative.md is as i2's session changed it
    +
    +  @r216
    +  Scenario: a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, faults no session
    +    Pins that initiatives run side by side do not fail each other's sessions through their own parts of .shop/work/.
    +    Given i1's work-item w1 is drafted
    +    And an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted
    +    And every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes .shop/work/i2/initiative.md in the repository's own checkout without committing it
    +    When the person runs `work run`
    +    Then no session of i1 or of i2 was taken as a fault
    +    And w1 is not failed and p2 is not failed
    +
    +  @r218
    +  Scenario: a change to .shop/work/ in the repository's own checkout, less another initiative's path run side by side, that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file
    +    Pins that `.shop/work/` in the main checkout, but for the parts of initiatives run beside it, is only what its last commit holds whenever a worker ends, and that a change there is a fault naming only the files of that part.
    +    Given i1's work-item w1 is drafted
    +    And an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted
    +    And every round ends and every worker gives DONE, and while i1's researcher works another session changes .shop/work/i1/initiative.md and a session of i2 changes .shop/work/i2/initiative.md, both in the repository's own checkout without committing them
    +    When the person runs `work run`
    +    Then .shop/work/i1/initiative.md is as its last commit holds it
    +    And w1 is failed, naming .shop/work/i1/initiative.md
    +    And nothing recorded of w1 names .shop/work/i2/initiative.md
    +
    +  @r219
    +  Scenario: a scenario whose failure before a merge would keep the work-item branch from being merged is run again once, alone, before the merge is refused
    +    Pins that one failing run of a scenario is never enough on its own to refuse a work-item's merge: the scenario gets one more run by itself first, and no more than one.
    +    Given i1's work-item w1 is ready, accepting thing#r1
    +    And the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE
    +    And the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch each time it is run
    +    When the person runs `work run i1`
    +    Then "it closes" was run once more, alone, after its run with w1's scenarios and before the merge of w1's branch was refused
    +    And "it closes" was run no other time
    +
    +  @r220
    +  Scenario: a scenario that fails again on its second run, alone, has both its runs in the question written for the work-item
    +    Pins that the person reading the work-item's question sees the scenario's failure in the run before the merge and in its second run, not one of them only.
    +    Given i1's work-item w1 is ready, accepting thing#r1
    +    And the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE
    +    And the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch each time it is run
    +    When the person runs `work run i1`
    +    Then w1's ## Questions holds a question giving both runs of "it closes": its run with w1's scenarios and its second run, alone
    +
    +  @r222
    +  Scenario: a scenario that fails before a merge and passes on its second run, alone, lets the work-item branch be merged
    +    Pins that a scenario that failed once and then passed by itself counts as passing, so the merge goes ahead as if it had passed the first time.
    +    Given i1's work-item w1 is ready, accepting thing#r1
    +    And the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE
    +    And the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch in its run with w1's scenarios and passes there on its second run, alone
    +    When the person runs `work run i1`
    +    Then the initiative branch has the implementer's commit of feature.txt
    +
    +  @r221
    +  Scenario: an apply round that gives an answer the drafts it applied do not hold for a glossary-proposal is followed by a new integrate round for the glossary-proposal
    +    Pins that an answer on a glossary-proposal asking for what its drafts never held goes back to integration, without anyone starting it by hand.
    +    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", given by its gate round, and its Answers section with "One line an event, and a ledger is the file of those lines."
    +    And the apply round for g1 applies nothing, giving that g1's answers give what its drafts do not hold
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind integrate was started for g1 after the apply round had ended
    +
    +  @r185
    +  Scenario: a researcher's result that gives an empty file set is taken as the researcher's file set
    +    Pins that a researcher finding no file to touch has still delivered its stage, so the work-item goes on and the person is asked nothing about a missing file set.
    +    Given i1's work-item w1 is drafted
    +    And the researcher's result gives no question and an empty file set, and every other worker gives DONE
    +    When the person runs `work run i1`
    +    Then `work run` wrote no question naming the researcher's file set as missing
    +    And w1's transition from drafted to researched was made once the researcher's session had ended
    +
    +  @r186
    +  Scenario: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal
    +    Pins that answers asking for lines the specification does not hold go back to integration, without anyone starting it by hand.
    +    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    +    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "A list, and a shelf's books are listed in the order they were shelved."
    +    And the formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind integrate was started for p1 after the formulate round for p1 had ended
    +
    +  @r184
    +  Scenario Outline: when `work run` ends with <node> awaiting-answer, it exits with an error, printing <node> with its open questions
    +    Pins that a capability-proposal or a work-item left waiting on the person stops the run as an error, and that the person reads the questions still unanswered, not those already answered.
    +    Given i1's work-item w1 is green
    +    And <setup>
    +    When the person runs `work run i1`
    +    Then `work run` prints <node> with the question "Which unit is the limit in?"
    +    And it prints neither "Is the old reader kept?" nor "Yes." with <node>
    +    And it exits with an error
    +
    +    Examples:
    +      | node | setup                                                                                                                                                                                                  |
    +      | p1   | i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Which unit is the limit in?" and "Is the old reader kept?", given by its gate round, and its Answers section answering only "Is the old reader kept?" with "Yes." |
    +      | w2   | i1's work-item w2 is awaiting-answer, its ## Questions section with "Which unit is the limit in?" and "Is the old reader kept?", and its Answers section answering only "Is the old reader kept?" with "Yes."                                   |
    diff --git a/features/work-queue.feature b/features/work-queue.feature
    index 0bcd307d..7085f72e 100644
    --- a/features/work-queue.feature
    +++ b/features/work-queue.feature
    @@ -57,34 +57,26 @@ Feature: Work queue
         And nothing under the new initiative's directory under .shop/work/ differs from main's last commit
         And it exits successfully
     
    -  @r23
    -  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    -    Pins that the command that completes an initiative's work ends the initiative when one of its work-items is green, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    -    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
    -    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    +  @r62
    +  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    +    Pins that whichever command completes an initiative's work, withdraw or retry, ends the initiative when one of its work-items is green and each of its capability-proposals is formulated or withdrawn, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    +    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is <before>
    +    And <log>
    +    And <proposals>
         And <request>
    -    When the session runs `work withdraw w2`
    -    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    +    When the session runs `work <command> w2`
    +    Then .shop/work/i1/w2.md gives w2's status as <after>
         And .shop/work/i1/initiative.md gives i1's status as done
         And it exits successfully
     
         Examples:
    -      | request                                                                                     |
    -      | no request kept in this context names i1                                                    |
    -      | a request q1 kept in this context, whose asker is this context, names i1 and is delivered   |
    -      | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
    -      | a request q1 kept in this context, whose asker is this context, names i2 and is accepted    |
    -
    -  @r23
    -  Scenario: retry that makes an initiative's last open work-item green again sets the initiative to done
    -    Pins that retry, like withdraw, is a command whose change can complete an initiative, and that it ends the initiative when it does.
    -    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is failed
    -    And .shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed
    -    And no request kept in this context names i1
    -    When the session runs `work retry w2`
    -    Then .shop/work/i1/w2.md gives w2's status as green
    -    And .shop/work/i1/initiative.md gives i1's status as done
    -    And it exits successfully
    +      | command  | before | log                                                                                     | after     | proposals                                                                             | request                                                                                     |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is formulated                                             | no request kept in this context names i1                                                    |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is withdrawn and its capability-proposal p2 is formulated | a request q1 kept in this context, whose asker is this context, names i1 and is delivered   |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is formulated                                             | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is formulated                                             | a request q1 kept in this context, whose asker is this context, names i2 and is accepted    |
    +      | retry    | failed | .shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed | green     | i1's capability-proposal p1 is formulated                                             | no request kept in this context names i1                                                    |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1 has no capability-proposal                                                         | no request kept in this context names i1                                                    |
     
       @r31
       Scenario: withdraw that leaves every work-item of an initiative withdrawn leaves the initiative's status as it is
    @@ -97,8 +89,21 @@ Feature: Work queue
         And .shop/work/i1/initiative.md gives i1's status as started
         And it exits successfully
     
    -  @r34
    -  Scenario: list prints each initiative, each request and each work-item under .shop/work/ with its status
    +  @r47
    +  Scenario: withdraw that leaves every work-item green or withdrawn while a capability-proposal is neither formulated nor withdrawn keeps the initiative started
    +    Pins that an initiative whose work-items are all green or withdrawn is not ended while one of its capability-proposals is still to be formulated, even with no request holding it open.
    +    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
    +    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    +    And i1's capability-proposal p1 is formulated and its capability-proposal p2 is approved
    +    And no request kept in this context names i1
    +    When the session runs `work withdraw w2`
    +    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    +    And .shop/work/i1/initiative.md gives i1's status as started
    +    And it exits successfully
    +
    +  @r34 @deprecated
    +  Scenario: list prints each initiative, each request and each work-item under .shop/work/ with its status (deprecated)
    +    Deprecated for: removal
         Pins that list reads the whole queue, initiatives that have ended among them, and gives every initiative, request and work-item in it with its status.
         Given an initiative i1 under .shop/work/ that is started, whose work-items w1 is drafted and w2 is ready
         And an initiative i2 under .shop/work/ that is done, whose work-item w3 is green
    @@ -110,8 +115,9 @@ Feature: Work queue
         And it prints w1 with drafted, w2 with ready, w3 with green and w4 with withdrawn
         And it exits successfully
     
    -  @r35
    -  Scenario: list with --json prints each initiative, request and work-item with its status as one JSON object
    +  @r35 @deprecated
    +  Scenario: list with --json prints each initiative, request and work-item with its status as one JSON object (deprecated)
    +    Deprecated for: removal
         Pins that list's result, read by a script, is one JSON object giving every initiative, request and work-item with its status, and nothing besides.
         Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is drafted
         And an initiative i2 under .shop/work/ that is done, whose work-item w2 is green
    @@ -121,6 +127,27 @@ Feature: Work queue
         And it gives i1 with started, i2 with done, q1 with accepted, w1 with drafted and w2 with green
         And it exits successfully
     
    +  @r60
    +  Scenario: list prints each initiative and each work-item under .shop/work/ with its status
    +    Pins that list reads the whole queue, initiatives that have ended among them, and gives every initiative and every work-item in it with its status.
    +    Given an initiative i1 under .shop/work/ that is started, whose work-items w1 is drafted and w2 is ready
    +    And an initiative i2 under .shop/work/ that is done, whose work-item w3 is green
    +    And an initiative i3 under .shop/work/ that is abandoned, whose work-item w4 is withdrawn
    +    When the session runs `work list`
    +    Then work prints i1 with started, i2 with done and i3 with abandoned
    +    And it prints w1 with drafted, w2 with ready, w3 with green and w4 with withdrawn
    +    And it exits successfully
    +
    +  @r61
    +  Scenario: list with --json prints each initiative and work-item with its status as one JSON object
    +    Pins that list's result, read by a script, is one JSON object giving every initiative and work-item with its status, and nothing besides.
    +    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is drafted
    +    And an initiative i2 under .shop/work/ that is done, whose work-item w2 is green
    +    When the session runs `work list --json`
    +    Then work prints one JSON object and nothing else
    +    And it gives i1 with started, i2 with done, w1 with drafted and w2 with green
    +    And it exits successfully
    +
       @r39
       Scenario: list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered
         Pins that an initiative whose own work is green but whose request upstream is not yet delivered shows, in the list, which request it waits on.
    @@ -159,6 +186,21 @@ Feature: Work queue
         And it prints the question "Which reading of r3?"
         And it exits successfully
     
    +  @r59
    +  Scenario: show of a request prints its status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution
    +    Pins what show gives about one request: where it stands, which side writes next, how the upstream answered each line, what was asked and answered on it, and the requirement ids that hold what was accepted.
    +    Given a request q1 kept in this context, whose asker is this context, that is delivered and in the asker's turn
    +    And its line 1 has the line outcome accepted and its line 2 the line outcome refused
    +    And it has on line 2 the question "Is the order kept?" with the answer "No, any order"
    +    And its resolution gives line 1 as thing#r7, delivered in version 0.23.0
    +    When the session runs `work show q1`
    +    Then work prints q1's status as delivered
    +    And it prints that it is the asker's turn
    +    And it prints line 1 with accepted and line 2 with refused
    +    And it prints the question "Is the order kept?" and the answer "No, any order"
    +    And it prints its resolution, thing#r7 and 0.23.0
    +    And it exits successfully
    +
       @r38
       Scenario Outline: show of <target> with --json prints its result as one JSON object
         Pins that show's result, read by a script, is one JSON object and nothing besides, whether it is given an initiative or a work-item.
    diff --git a/hooks/hooks.json b/hooks/hooks.json
    index 11ed8bc5..40ad0731 100644
    --- a/hooks/hooks.json
    +++ b/hooks/hooks.json
    @@ -10,6 +10,16 @@
             ]
           }
         ],
    +    "UserPromptSubmit": [
    +      {
    +        "hooks": [
    +          {
    +            "type": "command",
    +            "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/migrate\" prompting"
    +          }
    +        ]
    +      }
    +    ],
         "PreCompact": [
           {
             "hooks": [
    diff --git a/scripts/migrate b/scripts/migrate
    index 77ba02f5..b9964482 100755
    --- a/scripts/migrate
    +++ b/scripts/migrate
    @@ -5,6 +5,7 @@
       migrate status [--hook]
       migrate upgrade
       migrate compacting
    +  migrate prompting
     
     It works on the top level of the git repository it is run in. Every change is computed first (moves, new texts,
     removals), checked, and only then written; a write that fails part way puts the repository back at its commit. A
    @@ -17,6 +18,7 @@ from pathlib import Path
     from migrate_layout import Plan, plan_ids, plan_moves
     from migrate_ledger import plan_ledger
     from migrate_spec import plan_capabilities, plan_holding, plan_index, plan_references
    +from migrate_prompt import run as run_prompt
     from migrate_session import run as run_session
     from migrate_upgrade import run as run_upgrade
     from migrate_write import Failed, check_moves, top_level, uncommitted, write
    @@ -64,9 +66,12 @@ def main(argv=None):
         s.add_argument("--hook", action="store_true", help="print what a session is told at its start (with work status of open initiatives), and exit 0")
         sub.add_parser("upgrade", help="apply each pending upgrade step and commit it all")
         sub.add_parser("compacting", help="the PreCompact hook: note `compacted` in each open initiative's ledger, ask for a hand-off")
    +    sub.add_parser("prompting", help="the UserPromptSubmit hook: tell the session to write a delegation with `work delegate`")
         args = ap.parse_args(argv)
         if args.cmd == "compacting":
             return run_session()
    +    if args.cmd == "prompting":
    +        return run_prompt()
         if args.cmd in ("status", "upgrade"):
             return run_upgrade(args.cmd, getattr(args, "hook", False))
         return cmd_run(args)
    diff --git a/scripts/migrate_prompt.py b/scripts/migrate_prompt.py
    new file mode 100644
    index 00000000..ac1324ab
    --- /dev/null
    +++ b/scripts/migrate_prompt.py
    @@ -0,0 +1,36 @@
    +"""What the plugin's UserPromptSubmit hook (`migrate prompting`) tells a session about the repository's requests
    +(requests r72): that a delegation the person gives for a request is written, in the same reply, with `work delegate`.
    +
    +It speaks only when the repository keeps a request that is not delivered, refused or withdrawn, and always exits 0: a
    +hook's failure must not stop a session.
    +"""
    +import sys
    +from pathlib import Path
    +
    +import workqueue
    +from migrate_write import top_level
    +
    +ENDED = ("delivered", "refused", "withdrawn")
    +
    +
    +def prompting(root):
    +    """What the session is told at `root`; '' when the repository keeps no request whose negotiation has not ended."""
    +    try:
    +        names = [name for name, status, _, _ in workqueue.requests(root) if status not in ENDED]
    +    except workqueue.Refused:
    +        return ""
    +    if not names:
    +        return ""
    +    return ("This repository keeps the requests %s. When the person gives you a delegation for one of them (which "
    +            "questions you may answer in their place) outside `work request`, then in that same reply write it with "
    +            "`work delegate <request> \"<delegation>\"` (python3 %s delegate), the delegation being "
    +            "The person, <date>: \"<the person's words>\" with today's date.\n"
    +            % (", ".join(names), Path(__file__).resolve().parent / "work"))
    +
    +
    +def run():
    +    """`migrate prompting`: the UserPromptSubmit hook, always exit 0."""
    +    root = top_level(Path.cwd())
    +    if root is not None:
    +        sys.stdout.write(prompting(root))
    +    return 0
    diff --git a/scripts/supervise_brief.py b/scripts/supervise_brief.py
    index 621920f6..a75431e0 100644
    --- a/scripts/supervise_brief.py
    +++ b/scripts/supervise_brief.py
    @@ -132,8 +132,9 @@ class Briefs:
             of the change list the result gives (r92)."""
             ident = str(data.get("fulfils") or "").rsplit("/", 1)[-1]
             others = supervise_drafts.added_by_others(self.root, self.initiative)     # r102
    -        return ["Request: %s" % ident, "Accepted lines of the request:"] + [
    -            "- %d. %s" % line for line in workqueue_request.accepted_lines(self.root, ident)] + [
    +        asked = ["Request: %s" % ident, "Accepted lines of the request:"] + [
    +            "- %d. %s" % line for line in workqueue_request.accepted_lines(self.root, ident)] if ident else []     # r221: a re-integrated proposal of an initiative that fulfils no request
    +        return asked + [
                 "Ids drafted elsewhere (number added lines above each on the same capability): %s"
                 % (", ".join(others) or "none"),
                 "Drafts path: %s" % (here / "drafts"),
    diff --git a/scripts/supervise_change.py b/scripts/supervise_change.py
    index e9d67217..c7264c05 100644
    --- a/scripts/supervise_change.py
    +++ b/scripts/supervise_change.py
    @@ -71,6 +71,18 @@ class Changes:
             head = "\n".join(l for l in text[:end].split("\n") if l.split(":")[0] not in FIELDS)
             path.write_text(head + "\n" + "\n".join("%s: [%s]" % (f, ", ".join(lists[f])) for f in FIELDS) + text[end:])
     
    +    def redraft_lists(self, name, one):
    +        """The round's ids for the capability of the proposal `name`, the one the round was started for (r188): each id the
    +        round names is in the list the round gives it, in no other; the ids it does not name stay in the lists they were in."""
    +        path = self.dir / (name + ".md")
    +        text = path.read_text()
    +        held, _ = workqueue.frontmatter(text)
    +        named = {i for field in FIELDS for i in one[field]}
    +        for field in FIELDS:
    +            mine = [i for i in (held.get(field) or []) if i not in named] + one[field]
    +            text = re.sub(r"(?m)^%s:.*$" % field, lambda _: "%s: [%s]" % (field, ", ".join(mine)), text, count=1)
    +        path.write_text(text)
    +
         def proposal_for(self, capability):
             """The initiative's capability-proposal that argues `capability`, as a path, else None."""
             for path in sorted(self.dir.glob("*.md")):
    @@ -112,7 +124,7 @@ class Changes:
                         self.merge_lists(held.stem, one)
                         written.append(held)
                         continue
    -                self.rewrite_lists(held.stem, [one])
    +                self.redraft_lists(held.stem, one)
                     text = held.read_text()
                     said = "The drafts of this proposal are in %s." % stage_dir
                     held.write_text(re.sub(r"The drafts of this proposal are in \S+?\.(?=\s|$)", lambda _: said, text)
    @@ -131,6 +143,15 @@ class Changes:
                 for field in FIELDS:
                     terms[field] += [i for i in each[field] if i not in terms[field]]
             if any(e.get("glossary") for e in found):
    +            mine = self.dir / ((own or "") + ".md")
    +            if own and mine.exists() and workqueue.frontmatter(mine.read_text())[0].get("kind") == "glossary-proposal":     # r189
    +                self.redraft_lists(own, terms)     # the glossary-proposal the round was started for keeps the terms the round does not name
    +                text = mine.read_text()
    +                said = "The drafts of this proposal are in %s." % stage_dir
    +                mine.write_text(re.sub(r"The drafts of this proposal are in \S+?\.(?=\s|$)", lambda _: said, text)
    +                                if "The drafts of this proposal are in" in text else text.rstrip("\n") + "\n\n" + said + "\n")
    +                written.append(mine)
    +                return written
                 path = self.dir / "glossary.md"
                 path.write_text("---\nid: glossary-proposal/%s/%s-glossary\nkind: glossary-proposal\npart_of: %s\nstatus: drafted\n%sdate: %s\n"
                                 "---\n\n# glossary\n\nThe drafts of this proposal are in %s.\n" % (
    diff --git a/scripts/supervise_faults.py b/scripts/supervise_faults.py
    index 0e0380a7..debe4e8a 100644
    --- a/scripts/supervise_faults.py
    +++ b/scripts/supervise_faults.py
    @@ -103,12 +103,16 @@ class Faults:
     
         def checkout_changes(self):
             """The paths under .shop/work/ in the repository's own checkout that differ from its last commit, other than
    -        what work run itself has written and not yet committed; each put back to its last commit (r28)."""
    +        what work run itself has written and not yet committed and the part of each other initiative run side by side
    +        (.shop/work/<initiative>/); each put back to its last commit (r214, r218)."""
             out = supervise_worker.git(self.root, "status", "--porcelain", "--untracked-files=all", "--", WORK.as_posix()).stdout
             logs = {run.rel(run.dir / "log.jsonl"): run for run in self.group}     # the runs of the initiatives taken together
    +        others = [run.rel(run.dir) + "/" for run in self.group if run is not self]
             changed = []
             for line in out.splitlines():
                 path = line[3:].strip('"')
    +            if any(path.startswith(other) for other in others):
    +                continue
                 if any(path.startswith(own + "/") for run in self.group for own in run.own):
                     continue
                 if path in logs and (self.root / path).read_text() == self.committed(path) + "".join(logs[path].unlogged):
    diff --git a/scripts/supervise_merge.py b/scripts/supervise_merge.py
    index ccbf71f4..012b10fb 100644
    --- a/scripts/supervise_merge.py
    +++ b/scripts/supervise_merge.py
    @@ -113,6 +113,40 @@ class Merge:
             with self.lock:
                 git(self.root, "branch", "-q", "-d", "work/" + name)     # merged, so no longer needed; once its worktree is gone (r18)
     
    +    @staticmethod
    +    def has_error(out):
    +        """Whether pytest's output `out` has an ERROR line in its short summary or an error count in its last line."""
    +        lines = out.strip().splitlines()
    +        short = out.partition("short test summary info")[2].splitlines()
    +        return any(l.startswith("ERROR ") for l in short) or re.search(r"\b\d+ errors?\b", lines[-1] if lines else "") is not None
    +
    +    def taken_back(self, name, tree, command, runs):
    +        """Whether every scenario the failing `runs` name passes on one more run, alone (r219, r222); each is run once,
    +        and the run is logged under its own event. A failing run is not taken back when it names no failure, names
    +        a failure work_items did not name as a scenario (`SCENARIO <node>` lines), or has an error; a rerun that
    +        ran no test failed."""
    +        failing = {}
    +        for done in runs:
    +            out = done.stdout + done.stderr
    +            ids = [l.split(" ", 1)[1].split(" - ")[0] for l in out.splitlines()
    +                   if l.startswith("FAILED ") and "::" in l]
    +            scenarios = {l.split(" ", 1)[1] for l in out.splitlines() if l.startswith("SCENARIO ")}
    +            if done.returncode != 0 and (not ids or not set(ids) <= scenarios or self.has_error(out)):
    +                return False
    +            failing.update(dict.fromkeys(ids))
    +        alone = [a for i, a in enumerate(command) if a != "-n" and command[max(i - 1, 0)] != "-n"]
    +        if "-n" in command:
    +            alone += ["-n", "0"]     # xdist is on in the command: one process, for the scenario alone
    +        passed = []
    +        for node in failing:
    +            again = subprocess.run(alone + [node], cwd=tree, capture_output=True, text=True, env=with_scripts())
    +            passed.append(again.returncode == 0 and re.search(r"\b\d+ passed\b", again.stdout + again.stderr) is not None)
    +            if not passed[-1]:
    +                self.second_runs.append("its second run, alone, `%s`:\n%s" % (
    +                    " ".join(again.args), (again.stdout + again.stderr).strip()))
    +            self.log(**{"work-item": name, "stage": "merge", "event": "rerun", "scenario": node, "passed": passed[-1]})
    +        return all(passed)
    +
         def merge(self, name, tree, tests):
             """The branch rebased on the initiative branch, put back under .shop/work/, tested and merged (r4, r6); None,
             else the question it gives the person instead of the merge. What the worker left uncommitted is cleaned away
    @@ -126,10 +160,13 @@ class Merge:
             record, suite = self.suite_record(tree, tests["suite"])     # its expected red counted (r43)
             self.log(**{"work-item": name, "stage": "merge", "event": "suite", "record": record})
             scenarios = subprocess.run(tests["work_item"], cwd=tree, capture_output=True, text=True, env=with_scripts())
    -        for done in (scenarios, suite):
    -            if done.returncode != 0:
    -                return "commits on which %s's scenarios and the whole suite pass are missing: `%s` failed on %s's branch " \
    -                       "work/%s:\n%s" % (name, " ".join(done.args), name, name, (done.stdout + done.stderr).strip())
    +        self.second_runs = []
    +        failed = [done for done in (scenarios, suite) if done.returncode != 0]
    +        if failed and not self.taken_back(name, tree, tests["suite"], (scenarios, suite)):     # once, whatever the runs
    +            done = failed[0]
    +            return "commits on which %s's scenarios and the whole suite pass are missing: `%s` failed on %s's branch " \
    +                   "work/%s:\n%s" % (name, " ".join(done.args), name, name,
    +                                     "\n".join([(done.stdout + done.stderr).strip()] + self.second_runs))
             before = git(self.root, "rev-parse", "HEAD").stdout.strip()
             git(self.root, "merge", "--ff-only", "work/" + name)
             commits = git(self.root, "rev-list", "--reverse", "%s..HEAD" % before).stdout.split()
    diff --git a/scripts/supervise_rounds.py b/scripts/supervise_rounds.py
    index b7062e51..f283d924 100644
    --- a/scripts/supervise_rounds.py
    +++ b/scripts/supervise_rounds.py
    @@ -56,6 +56,8 @@ class Rounds(Changes, Raises):
                                         or len(self.held(name, "Answers")) >= len(self.held(name, "Questions"))):
                     return (name, *self.route(name, status))
             for name, status in supervise_glossary.statuses(self.dir):     # r164, r165, r169
    +            if name not in left and status in ("awaiting-answer", "approved") and self.sent_back(name):     # r221: back to integration
    +                return (name, "integrate", "drafted")
                 one = supervise_glossary.route(status, len(self.held(name, "Questions")), len(self.held(name, "Answers")))
                 if name not in left and one:
                     return (name, *one)
    diff --git a/scripts/work b/scripts/work
    index bc7ee7e5..605c44bc 100755
    --- a/scripts/work
    +++ b/scripts/work
    @@ -99,6 +99,11 @@ def cmd_resolve(args):
         return 0
     
     
    +def cmd_delegate(args):
    +    workqueue_request.delegate(args.root, args.request, args.delegation)
    +    return 0
    +
    +
     def cmd_start(args):
         print(workqueue_start.start(args.root, args.request))
         return 0
    @@ -167,6 +172,9 @@ def main(argv=None):
         q = sub.add_parser("resolve", help="write which requirement holds each accepted line of a request, and in which version")
         q.add_argument("request")
         q.add_argument("--line", nargs=3, action="append", default=[], metavar=("N", "REQUIREMENT", "VERSION"))
    +    q = sub.add_parser("delegate", help="write the delegation of a request, in place of any it had")
    +    q.add_argument("request")
    +    q.add_argument("delegation")
         q = sub.add_parser("start", help="write the initiative an accepted request begins, proposed")
         q.add_argument("request")
         args = ap.parse_args(argv)
    @@ -174,7 +182,7 @@ def main(argv=None):
             return {"add": cmd_add, "show": cmd_show, "list": cmd_list, "run": cmd_run, "retry": cmd_retry, "answer": cmd_answer,
                     "withdraw": cmd_withdraw, "note": cmd_note, "status": cmd_status,
                     "request": cmd_request, "outcome": cmd_outcome, "ask": cmd_ask, "reply": cmd_reply, "turn": cmd_turn, "resolve": cmd_resolve,
    -                "start": cmd_start}[args.cmd](args)
    +                "delegate": cmd_delegate, "start": cmd_start}[args.cmd](args)
         except workqueue.Refused as refused:
             print("work: %s" % refused, file=sys.stderr)
             return 1
    diff --git a/scripts/work_items.py b/scripts/work_items.py
    index 275807e2..f85ee4ea 100644
    --- a/scripts/work_items.py
    +++ b/scripts/work_items.py
    @@ -153,6 +153,22 @@ def guarantees(config, cap):
         return is_guarantees(path.parent.parent.parent, cap)
     
     
    +def pytest_runtest_setup(item):
    +    """Note on a scenario's reports that it is one (user properties reach the xdist controller)."""
    +    if scenario_of(item) is not None:
    +        item.user_properties.append(("scenario", True))
    +
    +
    +def pytest_terminal_summary(terminalreporter, config):
    +    """Under --work-item, a line `SCENARIO <node id>` for each failed test that is a scenario, so `work run` knows
    +    which failures are scenarios (supervision r219, r222)."""
    +    if not config.getoption("--work-item"):
    +        return
    +    for report in terminalreporter.stats.get("failed", []):
    +        if ("scenario", True) in report.user_properties:
    +            terminalreporter.write_line("SCENARIO %s" % report.nodeid)
    +
    +
     def pytest_sessionfinish(session, exitstatus):
         """A work-item all of whose requirements are of guarantees capabilities, left with no test, succeeds. Decided
         from the work-item and the spec, so on the xdist controller as on a worker."""
    diff --git a/scripts/workqueue_done.py b/scripts/workqueue_done.py
    index 404a26fe..7b742b24 100644
    --- a/scripts/workqueue_done.py
    +++ b/scripts/workqueue_done.py
    @@ -1,8 +1,8 @@
    -"""An initiative done (work-queue r23): the condition over its work-items and the requests this context asked naming it,
    +"""An initiative done (work-queue r62): the condition over its work-items and the requests this context asked naming it,
     and the rewrite of its initiative.md that a command's commit carries.
     
     An initiative qualifies when it has a work-item, every work-item is green or withdrawn, every capability-proposal is
    -formulated, withdrawn or merged, and every request kept under
    +formulated or withdrawn (r47: any other status keeps it started), and every request kept under
     .shop/work/requests/ that this context asked and that names the initiative (in its part_of or source) is delivered.
     """
     import re
    @@ -10,7 +10,7 @@ from pathlib import Path
     
     import workqueue
     
    -CLOSED_PROPOSAL = ("formulated", "withdrawn", "merged")
    +CLOSED_PROPOSAL = ("formulated", "withdrawn")
     
     
     def _named(data):
    diff --git a/scripts/workqueue_list.py b/scripts/workqueue_list.py
    index c1ce936e..cc912c49 100644
    --- a/scripts/workqueue_list.py
    +++ b/scripts/workqueue_list.py
    @@ -6,6 +6,7 @@ record, .shop/work/<initiative>/raised.jsonl, one JSON object a line (upstream,
     line of a request giving its last known status; the upstream is never reached.
     """
     import json
    +import re
     from pathlib import Path
     
     import workqueue
    @@ -37,14 +38,33 @@ def waiting(root, initiative):
         return [(u, r, s) for (u, r), s in last.items() if s != "delivered"]
     
     
    +def uncited(root):
    +    """(id, date) of each observation in .shop/records/observations.md that no initiative's or request's `source` names."""
    +    path = Path(root) / ".shop" / "records" / "observations.md"
    +    if not path.is_file():
    +        return []
    +    cited = set()
    +    for other in sorted((Path(root) / workqueue.WORK).glob("*/*.md")):
    +        source = workqueue.frontmatter(workqueue.read(other, root))[0].get("source")
    +        cited.update(re.findall(r"observation/[\w./-]+", str(source or "")))
    +    found = []
    +    for heading, body in re.findall(r"(?ms)^## (observation/\S+)\n(.*?)(?=^## |\Z)", workqueue.read(path, root)):
    +        date = re.search(r"(?m)^date: (\S+)", body)
    +        if heading not in cited and "observation/" + heading.rsplit("/", 1)[-1] not in cited:
    +            found.append((heading, date.group(1) if date else None))
    +    return found
    +
    +
     def listing(root, as_json):
         found = list(initiatives(root))
         requests = list(workqueue.requests(root))
         items = list(workqueue.items(root))
    +    seen = uncited(root)
         if as_json:
             print(json.dumps({"initiatives": [{"initiative": n, "status": s} for n, s in found],
                               "requests": [{"request": n, "status": s} for n, s, _, _ in requests],
    -                          "work-items": [{"work-item": n, "initiative": i, "status": s} for i, n, s in items]}))
    +                          "work-items": [{"work-item": n, "initiative": i, "status": s} for i, n, s in items],
    +                          "observations": [{"observation": o, "date": d} for o, d in seen]}))
             return 0
         for name, status in found:
             print("initiative %s %s" % (name, status))
    @@ -54,6 +74,8 @@ def listing(root, as_json):
             print("request %s %s" % (name, status))
         for initiative, name, status in items:
             print("work-item %s/%s %s" % (initiative, name, status))
    +    for observation, date in seen:
    +        print("observation %s %s" % (observation, date))
         return 0
     
     
    @@ -76,12 +98,30 @@ def work_item(root, target, as_json):
         return 0
     
     
    +def request_parts(root, name, turn):
    +    """What `work show <request>` prints after its first line (r59): whose turn it is, each line with its line outcome,
    +    each question with its answer, the resolution."""
    +    import workqueue_request
    +    parts = workqueue_request.sections(root, name)
    +    print("it is the %s's turn" % turn)
    +    for number, text in sorted(parts["Lines"].items(), key=lambda e: int(e[0])):
    +        print("  line %s: %s - %s" % (number, parts["Outcomes"].get(number, "unsettled"), text))
    +    for number, text in sorted(parts["Questions"].items(), key=lambda e: int(e[0])):
    +        print("  question %s: %s" % (number, text))
    +        if number in parts["Answers"]:
    +            print("  answer %s: %s" % (number, parts["Answers"][number]))
    +    for number, text in sorted(parts["Resolution"].items(), key=lambda e: int(e[0])):
    +        print("  resolution line %s: %s" % (number, text))
    +
    +
     def show(root, target, as_json):
         """Print where `target`, an initiative or a work-item, stands; return the exit status."""
         workqueue.entry(target, "target")
         for name, status, turn, _ in workqueue.requests(root):
             if name == target and not (Path(root) / workqueue.WORK / target / "initiative.md").is_file():
                 print(json.dumps({"request": name, "status": status, "turn": turn}) if as_json else "%s %s %s" % (name, status, turn))
    +            if not as_json:
    +                request_parts(root, name, turn)
                 return 0
         if (Path(root) / workqueue.WORK / target / "initiative.md").is_file():
             return workqueue_status.status(root, target, as_json)
    diff --git a/scripts/workqueue_request.py b/scripts/workqueue_request.py
    index e46a9ce5..65d8a918 100644
    --- a/scripts/workqueue_request.py
    +++ b/scripts/workqueue_request.py
    @@ -29,6 +29,13 @@ def _entries(text, name):
         return [line for line in found.group(1).splitlines() if line.strip()] if found else []
     
     
    +def sections(root, ident):
    +    """Request `ident`'s Lines, Outcomes, Questions, Answers and Resolution, each as {number: text}."""
    +    text = workqueue.read(path_of(root, ident), root)
    +    return {name: dict(e.split(". ", 1) for e in _entries(text, name) if ". " in e)
    +            for name in ("Lines", "Outcomes", "Questions", "Answers", "Resolution")}
    +
    +
     def accepted_lines(root, ident):
         """(number, text) of each line of request `ident` whose line outcome is accepted."""
         text = workqueue.read(path_of(root, ident), root)
    @@ -204,6 +211,24 @@ def turn(root, ident):
         _change(root, ident, "turn", edit)
     
     
    +def delegate(root, ident, text):
    +    """Write `text` as request `ident`'s delegation in place of any it had (r65), committed (r66). An empty one is refused
    +    (r67), and so is a delivered, refused or withdrawn request (r68); status and turn stay as they are (r70, r71)."""
    +    if not text.strip():
    +        raise Refused("the delegation is empty")
    +
    +    def edit(old):
    +        status = field(old, "status")
    +        if status in ("delivered", "refused", "withdrawn"):
    +            raise Refused("%s is %s; work delegate writes a delegation only in a request whose negotiation has not ended" % (ident, status))
    +        value = json.dumps(text)
    +        if field(old, "delegation") is not None:
    +            return _with_field(old, "delegation", value)
    +        end = old.find("\n---", 4)
    +        return old[:end] + "\ndelegation: %s" % value + old[end:]
    +    _change(root, ident, "delegate", edit)
    +
    +
     def resolve(root, ident, lines):
         """Write each accepted line's requirement and version, `lines` being (number, requirement, version), and set the
         status to delivered (r10, r11); a request that is not accepted is refused."""
    diff --git a/scripts/workqueue_status.py b/scripts/workqueue_status.py
    index 1e884abb..639c2639 100644
    --- a/scripts/workqueue_status.py
    +++ b/scripts/workqueue_status.py
    @@ -109,23 +109,6 @@ def render(found):
         return "\n".join(lines)
     
     
    -def uncited(root):
    -    """(id, date) of each observation in .shop/records/observations.md that no initiative's or request's `source` names."""
    -    path = Path(root) / ".shop" / "records" / "observations.md"
    -    if not path.is_file():
    -        return []
    -    cited = set()
    -    for other in sorted((Path(root) / workqueue.WORK).glob("*/*.md")):
    -        source = workqueue.frontmatter(workqueue.read(other, root))[0].get("source")
    -        cited.update(re.findall(r"observation/[\w./-]+", str(source or "")))
    -    found = []
    -    for heading, body in re.findall(r"(?ms)^## (observation/\S+)\n(.*?)(?=^## |\Z)", workqueue.read(path, root)):
    -        date = re.search(r"(?m)^date: (\S+)", body)
    -        if heading not in cited and "observation/" + heading.rsplit("/", 1)[-1] not in cited:
    -            found.append((heading, date.group(1) if date else None))
    -    return found
    -
    -
     def open_names(root):
         """The names of the initiatives under .shop/work/ whose initiative.md gives a status other than done or abandoned."""
         work = Path(root) / workqueue.WORK
    @@ -138,11 +121,11 @@ def open_text(root):
         """What `work status` prints at `root` for each initiative neither done nor abandoned ('' when there is none)."""
         out = io.StringIO()
         with contextlib.redirect_stdout(out):
    -        status(root, None, False, report=False)
    +        status(root, None, False)
         return out.getvalue()
     
     
    -def status(root, initiative, as_json, report=True):
    +def status(root, initiative, as_json):
         """Print where `initiative` stands, or each initiative neither done nor abandoned; return the exit status."""
         work = Path(root) / workqueue.WORK
         if initiative is not None:
    @@ -157,14 +140,10 @@ def status(root, initiative, as_json, report=True):
         found = [read(root, n, shared) for n in names]
         if initiative is None:
             found = [f for f in found if f["status"] not in ENDED]
    -    seen = uncited(root) if initiative is None and report else []
         if as_json:
    -        out = {"initiatives": found}
    -        if initiative is None and report:
    -            out["observations"] = [{"observation": o, "date": d} for o, d in seen]
    -        print(json.dumps(out))
    +        print(json.dumps({"initiatives": found}))
         else:
    -        blocks = [render(f) for f in found] + (["\n".join("observation %s %s" % (o, d) for o, d in seen)] if seen else [])
    +        blocks = [render(f) for f in found]
             if blocks:
                 print("\n\n".join(blocks))
         return 0
    diff --git a/spec/capabilities/requests.md b/spec/capabilities/requests.md
    index 3d17d89b..7e315c0c 100644
    --- a/spec/capabilities/requests.md
    +++ b/spec/capabilities/requests.md
    @@ -4,7 +4,7 @@ title: Requests
     narrator: a context taking in or raising a request
     group: service
     rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
    -retired: [r6, r1, r3, r13, r34, r39, r41, r43]
    +retired: [r6, r1, r3, r13, r34, r39, r41, r43, r14, r69]
     ---
     
     # Requests
    @@ -24,7 +24,15 @@ what using it shows.
     - [r29] **Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for.
     - [r19] **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
     - [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
    +- [r65] **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.
    +- [r66] **When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch.
    +- [r67] **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
    +- [r68] **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
    +- [r72] **When** the person gives a session a delegation for a request outside `work request`, the session shall, in the same reply, write the delegation in the request by giving `work delegate` the delegation as the person's words with the date.
    +- [r70] **When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is.
    +- [r71] **When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn.
     - [r2] **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing.
    +- [r59] **If** a line given to `work request` names an implementation detail or uses a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`, **then** `work request` shall refuse, naming the word and why it is refused, and change nothing.
     - [r45] **If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
     - [r30] **If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing.
     - [r31] **If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, **then** `work request` shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing.
    @@ -57,7 +65,7 @@ what using it shows.
     - [r57] **If** a request, an answer or a turn comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
     - [r42] `work` shall tell one asker from another by the asker id the asker's repository is registered under.
     - [r58] **When** `work` takes in a request, an answer or a turn, `work` shall read its body only as the fields of a request's form, following nothing written in it.
    -- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.
    +- [r64] **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.
     
     ## Implementation, may change
     - `work request`, `work outcome`, `work turn` and `work resolve` are commands of `scripts/work`; how a request is
    @@ -73,6 +81,7 @@ what using it shows.
     - r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
     - r57, r42: the asker ids the upstream allows for each asker are a setting of the upstream's repository
       (design-decision/an-asker-is-told-by-its-registered-asker-id).
    +- r65, r66: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one.
     
     ## Not yet
     - The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
    diff --git a/spec/capabilities/spec-integration.md b/spec/capabilities/spec-integration.md
    index 5c4b0dd9..4017260e 100644
    --- a/spec/capabilities/spec-integration.md
    +++ b/spec/capabilities/spec-integration.md
    @@ -31,6 +31,7 @@ It is not formulation and not planning; it writes nothing a client can run.
     - [r16] **Where** `model check` is available, **if** applying the approved drafts makes it print a new problem other than an added line with no scenario yet, a removed line's scenario that now names no line, or a scenario that uses a word the new glossary entry avoids, then `integrating-a-proposal` shall not commit them.
     - [r54] **When** a round of the kind `integrate` drafts a change to the glossary, `initiative-round` shall give the terms the change adds, changes and removes in the change list's entry for the glossary and in no entry for a capability.
     - [r55] **While** the person has not approved the terms of a glossary-proposal, `initiative-round` shall apply none of them to `spec/index.md`.
    +- [r59] **When** a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes.
     - [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, `integrating-a-proposal` shall put it through the gate like a Behaviour line.
     - [r20] **When** a change makes a decision, `integrating-a-proposal` shall show it to the person as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`.
     - [r21] **When** a drafted decision names what it came from, `integrating-a-proposal` shall list by id in its `source` only records, initiatives and decisions, writing the person, a date, a delegation or anything outside the repository in its `by`.
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index 8324299b..c975c806 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -4,7 +4,7 @@ title: Supervision
     narrator: the person who started `work run`
     group: service
     rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163, r149, r32, r9, r105, r28, r217]
     ---
     
     # Supervision
    @@ -64,6 +64,7 @@ from what using it shows.
     - [r172] **While** a glossary-proposal is `awaiting-answer` and a question that a round of the kind `gate` gave on it has no answer, `work run` shall start no round of the kind `apply` for it.
     - [r116] **When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers.
     - [r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
    +- [r221] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold for a glossary-proposal, `work run` shall start a new round of the kind `integrate` for the glossary-proposal.
     - [r151] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied.
     - [r141] **When** `work run` starts a round of the kind `integrate` for a capability-proposal that has answers, `work run` shall give the round the capability-proposal's questions and answers and the initiative's ledger, with the accepted lines of the request the initiative fulfils.
     - [r142] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory.
    @@ -75,8 +76,9 @@ from what using it shows.
     - [r146] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall start a round of the kind `formulate` for the proposal.
     - [r147] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output.
     - [r148] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall write no second capability-proposal for that proposal's capability.
    +- [r188] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids of the proposal that the round's change list does not name.
    +- [r189] **When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name.
     - [r83] **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`.
    -- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
     - [r186] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
     - [r152] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status.
     - [r153] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output.
    @@ -96,10 +98,11 @@ from what using it shows.
     - [r97] **While** an initiative has no work-item, `work run` shall run no `measure initiative` on it.
     - [r76] **When** the `measure initiative` that `work run` ran on an initiative has written its measurement, `work run` shall start a session of `analyzing-a-batch` that writes the initiative's analysis record.
     - [r106] **When** `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch.
    -- [r105] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
    +- [r213] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose every capability-proposal is `formulated` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
     - [r161] **When** an initiative changes only the glossary, its glossary-proposal is `approved` and its terms are committed to `spec/index.md`, `work run` shall set the initiative's status to `done`.
     - [r109] **When** `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.
     - [r210] **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that is not a question of a glossary-proposal, whatever words it uses, to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
    +- [r211] **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started.
     - [r209] **When** a question of an initiative is a question of a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation.
     - [r78] **Where** the request an initiative fulfils gives a delegation, **when** a session `work run` started under it answers a question, `work run` shall write the answer naming the delegation it was given under.
     - [r118] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`.
    @@ -115,9 +118,8 @@ from what using it shows.
     - [r7] **When** `work run` makes a work-item's transition, `work run` shall commit the work-item's file, its stage directories and `log.jsonl` on the initiative branch, and nothing else.
     - [r8] **When** a worker starts or ends, `work run` shall append a line to `log.jsonl` with the time, the work-item, the stage, the agent and the session id.
     - [r62] **When** `work run` writes a stage's `session.json`, `work run` shall record in it the path of the transcript of the stage's session.
    -- [r9] **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status.
    +- [r212] **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status.
     - [r101] **When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions.
    -- [r32] **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall exit with an error, printing each work-item's status and each open question.
     - [r184] **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall exit with an error, printing each with its open questions.
     - [r52] **When** no work-item can make a transition and a work-item is `failed`, `work run` shall exit with an error, printing each work-item's status and each fault.
     - [r81] **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and one such node is `awaiting-answer` or `failed`, `work run` shall exit with an error, printing the status of each initiative it took.
    @@ -159,7 +161,10 @@ from what using it shows.
     - [r50] **While** every commit on the initiative branch other than the kept branch reviews' own commits has been read by a kept branch review, `work run` shall start no branch review.
     - [r94] **While** an initiative has no work-item, `work run` shall start no branch review of it.
     - [r51] **If** the push verification before the branch review fails, then `work run` shall exit with an error, saying why, and start no branch review.
    -- [r28] **If** the main checkout's `.shop/work/` differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file.
    +- [r214] **When** `work run` checks what changed in the main checkout while a session it started for one initiative worked, `work run` shall leave out each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side.
    +- [r215] **If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed, by a session of that initiative, while a session of one initiative worked, **then** `work run` shall put back no change of that path.
    +- [r216] **If** a path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side changed, by a session of that initiative, while a session of one initiative worked, **then** `work run` shall fault no session for that change.
    +- [r218] **If** the main checkout's `.shop/work/`, less each path under `.shop/work/<initiative>/` of another initiative that `work run` is running side by side, differs from its last commit when a worker ends, then `work run` shall put it back and transition the work-item to `failed`, naming each file.
     - [r29] **Where** `.shop/delivery.toml` gives `[tests]`, `work run` shall run those commands in place of its own commands for the work-item's scenarios and the suite.
     - [r30] **Where** `.shop/delivery.toml` gives a stage's `[allowed_tools]`, `work run` shall give that stage's worker that list in place of its own, less any bare Write or Edit.
     - [r31] **When** a planner's result gives a `fileset`, `work run` shall write that file set into the work-item as `fileset:` as it makes the work-item's transition to `planned`.
    @@ -176,6 +181,9 @@ from what using it shows.
     - [r42] **If** a worker ends without a result file that `work run` can read, then `work run` shall transition the work-item to `failed`, recording how its session ended.
     - [r43] **When** `work run` runs the whole suite before a merge, `work run` shall count as expected each failing scenario whose requirement a work-item other than the one being merged accepts and that is neither `green` nor `withdrawn`.
     - [r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.
    +- [r219] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge.
    +- [r220] **If** the second run of a scenario that r219 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item.
    +- [r222] **When** the second run of a scenario that r219 makes passes, `work run` shall take the scenario as passing in r4's merge of the work-item branch.
     - [r44] **When** `work run` writes a worker's brief, `work run` shall tell the worker to write its result file first with the outcome `PARTIAL`, and keep it current as it works.
     - [r45] **If** a worker's session ends in an error or at its turn limit, exits with an error, or leaves output that holds no JSON result, then `work run` shall transition the work-item to `failed`, recording how the session ended.
     - [r46] **If** the main checkout's `.shop/work/` has uncommitted changes when `work run` starts, then `work run` shall exit with an error, naming them, and change nothing.
    diff --git a/spec/capabilities/work-queue.md b/spec/capabilities/work-queue.md
    index 929b4d1d..51d65507 100644
    --- a/spec/capabilities/work-queue.md
    +++ b/spec/capabilities/work-queue.md
    @@ -4,7 +4,7 @@ title: Work queue
     narrator: a person, session or script reading work-items or writing their transitions
     group: service
     rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/work-retry-reads-the-log, design-decision/query-commands-answer-in-their-output, design-decision/work-items-named-by-ids, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked, design-decision/work-list-and-work-show-replace-work-status]
    -retired: [r2, r3, r11, r16, r17, r18, r33]
    +retired: [r2, r3, r11, r16, r17, r18, r33, r34, r35, r23]
     ---
     
     # Work queue
    @@ -23,14 +23,15 @@ work-item's status; `work run` (supervision) takes them through it. It judges no
     - [r32] **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.
     - [r22] **When** `work start <request>` is run on an `accepted` request, `work` shall write `.shop/work/<initiative>/initiative.md` as a `proposed` initiative of kind `capability-change` that fulfils the request, with the request's origins as its source, and print its id.
     - [r25] **When** `work start` writes an initiative, `work` shall commit the initiative on the current branch.
    -- [r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
    +- [r62] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
     - [r31] **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.
     - [r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`.
    -- [r34] **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.
    -- [r35] **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.
    +- [r60] **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status.
    +- [r61] **Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.
     - [r39] **While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.
     - [r36] **When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`.
     - [r37] **When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions.
    +- [r59] **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.
     - [r38] **Where** `--json` is given, `work show` shall print its result as one JSON object.
     - [r19] **When** `work note <initiative> <line>` is run, `work` shall append the line, with the date, to the initiative's ledger `.shop/work/<initiative>/ledger.md`.
     - [r20] **When** `work note` appends a line to an initiative's ledger, `work` shall commit the ledger on the current branch.
    @@ -60,7 +61,7 @@ work-item's status; `work run` (supervision) takes them through it. It judges no
     - A transition the lifecycle does not allow from the work-item's status is refused under r7.
     - `work answer` on a work-item that is not `awaiting-answer` is a change `work` cannot make, refused under r7.
     - `work retry` and `work withdraw` print `<work-item> <status>`, the status being the one the transition made.
    -- r23: a request names the initiative in its `part_of` or its `source`.
    +- r62: a request names the initiative in its `part_of` or its `source`.
     - r26, r27: the flag is `--change` for an answer that asks for a change and `--accept` for one that accepts the
       work-item as it is; the answer stays one line of free text.
     
    diff --git a/tests/scenarios/requests_flow_steps.py b/tests/scenarios/requests_flow_steps.py
    index b9810b83..6758ec51 100644
    --- a/tests/scenarios/requests_flow_steps.py
    +++ b/tests/scenarios/requests_flow_steps.py
    @@ -96,4 +96,4 @@ def turn_went(context, order):
     def show_prints(context):
         for rows in context["trace"]:
             shown = [row for row in rows if row["command"] == "show"][-1]
    -        assert shown["out"].split()[1:] == ["delivered", "asker"], shown
    +        assert shown["out"].splitlines()[0].split()[1:] == ["delivered", "asker"], shown
    diff --git a/tests/scenarios/requests_session_steps.py b/tests/scenarios/requests_session_steps.py
    new file mode 100644
    index 00000000..f73ae374
    --- /dev/null
    +++ b/tests/scenarios/requests_session_steps.py
    @@ -0,0 +1,38 @@
    +"""features/requests.feature's steps for a session the person gives a delegation (requests r72).
    +
    +The When runs the UserPromptSubmit command of hooks/hooks.json in the repository, as the harness does. A session double
    +then acts only on what the hook gave it: where the hook's text tells it to write a delegation in the same reply with
    +`work delegate`, as `The person, <date>: "<words>"`, it runs that command; otherwise it runs nothing.
    +"""
    +import json
    +import os
    +import subprocess
    +import sys
    +
    +from pytest_bdd import parsers, then, when
    +
    +from .migration_upgrade_steps import PLUGIN
    +from .requests_write_steps import ident_delegation_is
    +
    +
    +@when(parsers.parse('the person tells a session, on {date}, that for {ident} it may "{words}"'))
    +def person_tells_a_session(repo, run, context, date, ident, words):
    +    command = json.loads((PLUGIN / "hooks/hooks.json").read_text())["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
    +    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(PLUGIN), PYTHON=sys.executable)
    +    prompt = json.dumps({"prompt": 'On %s: for %s you may "%s"' % (date, ident, words)})
    +    hook = subprocess.run(command, shell=True, cwd=repo, env=env, input=prompt, capture_output=True, text=True)
    +    told = hook.stdout
    +    context["ran"] = None
    +    if hook.returncode == 0 and "work delegate" in told and "same reply" in told and 'The person, <date>: "<the person' in told:
    +        context["ran"] = ["delegate", ident, 'The person, %s: "%s"' % (date, words)]
    +        context["done"] = run("work", *context["ran"])
    +
    +
    +@then(parsers.parse("in its reply to that message the session runs `work delegate`, giving {ident} and the delegation '{text}'"))
    +def session_ran_delegate(context, ident, text):
    +    assert context["ran"] == ["delegate", ident, text], context["ran"]
    +
    +
    +@then(parsers.parse("when that reply ends, {ident}'s delegation is '{text}'"))
    +def delegation_when_reply_ends(repo, ident, text):
    +    ident_delegation_is(repo, ident, None, text)
    diff --git a/tests/scenarios/requests_show_steps.py b/tests/scenarios/requests_show_steps.py
    index b3784997..44ce3293 100644
    --- a/tests/scenarios/requests_show_steps.py
    +++ b/tests/scenarios/requests_show_steps.py
    @@ -46,9 +46,9 @@ def runs_show(run, context):
         context["done"] = run("work", "show")
     
     
    -@when("the session runs `work status`")
    -def runs_status(run, context):
    -    context["done"] = run("work", "status")
    +@when("the session runs `work list`")
    +def runs_list(run, context):
    +    context["done"] = run("work", "list")
     
     
     @then(parsers.re(r"work prints (?P<ident>q\d+) with (?P<status>[\w-]+) and the (?P<turn>asker|upstream)'s turn"))
    diff --git a/tests/scenarios/requests_steps.py b/tests/scenarios/requests_steps.py
    index 30f31b2e..dd58d535 100644
    --- a/tests/scenarios/requests_steps.py
    +++ b/tests/scenarios/requests_steps.py
    @@ -59,7 +59,10 @@ def a_request_with_a_line_each(repo, context, ident, asker, turn, first, second)
     @when(parsers.re(r"the upstream runs `work (?P<args>[^`]+)`(?P<giving>, giving .*)?"))
     def the_upstream_runs(repo, run, context, args, giving):
         argv = shlex.split(args)
    -    if giving:
    +    if giving and "the delegation" in giving:
    +        ident, text = re.fullmatch(r', giving (q\d+) and the delegation "(.*)"', giving).groups()
    +        argv += [ident, text]
    +    elif giving:
             version = giving.rsplit("version ", 1)[1]
             for ident, line in re.findall(r"(\S+#r\d+) for line (\d+)", giving):
                 argv += ["--line", line, ident, version]
    diff --git a/tests/scenarios/requests_write_steps.py b/tests/scenarios/requests_write_steps.py
    index 82a5aca6..15b2177c 100644
    --- a/tests/scenarios/requests_write_steps.py
    +++ b/tests/scenarios/requests_write_steps.py
    @@ -69,6 +69,36 @@ def refused_empty_delegation(context):
         assert "delegation is empty" in context["done"].stderr, context["done"]
     
     
    +@given(parsers.parse("{ident} holds no delegation"))
    +def holds_no_delegation(repo, ident):
    +    assert "delegation:" not in (repo / request_rel(ident)).read_text()
    +
    +
    +@given(parsers.parse('{ident} holds the delegation "{text}"'))
    +def holds_delegation(repo, context, ident, text):
    +    path = repo / request_rel(ident)
    +    path.write_text(path.read_text().replace("\nturn:", "\ndelegation: %s\nturn:" % json.dumps(text), 1))
    +    context["written"] = path.read_text()
    +
    +
    +@then(parsers.re(r"(?P<ident>q\d+)'s delegation is (?:\"(?P<dq>.*)\"|'(?P<sq>.*)')"))
    +def ident_delegation_is(repo, ident, dq, sq):
    +    values = re.findall(r"(?m)^delegation: (.*)$", (repo / request_rel(ident)).read_text())
    +    assert values, "no delegation field"
    +    value = values[0]
    +    assert (json.loads(value) if value.startswith('"') else value) == (dq if dq is not None else sq)
    +
    +
    +@then(parsers.parse("{ident} holds no other delegation"))
    +def holds_no_other_delegation(repo, ident):
    +    assert len(re.findall(r"(?m)^delegation:", (repo / request_rel(ident)).read_text())) == 1
    +
    +
    +@then(parsers.re(r"the command is refused, naming (?P<status>delivered|refused|withdrawn)"))
    +def refused_naming_status(context, status):
    +    assert status in context["done"].stderr, context["done"]
    +
    +
     @then("it exits with an error")
     def exits_with_an_error(context):
         assert context["done"].returncode != 0, context["done"]
    diff --git a/tests/scenarios/supervision_delegation_steps.py b/tests/scenarios/supervision_delegation_steps.py
    index 203f109d..4f75459d 100644
    --- a/tests/scenarios/supervision_delegation_steps.py
    +++ b/tests/scenarios/supervision_delegation_steps.py
    @@ -1,4 +1,4 @@
    -"""supervision's steps about the questions `work run` has answered under a request's delegation (r77, r78)."""
    +"""supervision's steps about the questions `work run` has answered under a request's delegation (r77, r78, r211)."""
     import json
     import re
     
    @@ -14,10 +14,30 @@ ANSWER = "The delegation covers it."
     @given(parsers.re(r'i1 fulfils the request q1, which gives the delegation "(?P<delegation>[^"]+)"$'))
     def fulfils_with_delegation(repo, context, delegation):
         context["delegation"] = delegation
    +    start_i1(repo)
    +    write_q1(repo, delegation)
    +    commit_all(repo, "i1 fulfils q1, which gives a delegation")
    +
    +
    +def start_i1(repo):
         write(repo, DIR + "/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\nfulfils: q1\n---\n" % full("initiative", "i1"))
    +
    +
    +def write_q1(repo, delegation=None):
    +    field = 'delegation: "%s"\n' % delegation if delegation else ""
         write(repo, ".shop/work/requests/q1.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n"
    -          'delegation: "%s"\n---\n\n## Lines\n1. Something.\n' % (full("request", "q1"), delegation))
    -    commit_all(repo, "i1 fulfils q1, which gives a delegation")
    +          '%s---\n\n## Lines\n1. Something.\n' % (full("request", "q1"), field))
    +
    +
    +@given(parsers.re(r'i1 fulfils the request q1, which gives the delegation "(?P<delegation>[^"]+)", given (?P<when>before|after) i1 started$'))
    +def fulfils_with_delegation_given(repo, context, delegation, when):
    +    context["delegation"] = delegation
    +    start_i1(repo)
    +    write_q1(repo, delegation if when == "before" else None)
    +    commit_all(repo, "i1 started, fulfilling q1")
    +    if when == "after":
    +        write_q1(repo, delegation)
    +        commit_all(repo, "q1 is given a delegation")
     
     
     @given(parsers.re(r'spec/index\.md\'s Glossary holds the term "(?P<term>[^"]+)"$'))
    diff --git a/tests/scenarios/supervision_faults_steps.py b/tests/scenarios/supervision_faults_steps.py
    index 0a19de29..765329ba 100644
    --- a/tests/scenarios/supervision_faults_steps.py
    +++ b/tests/scenarios/supervision_faults_steps.py
    @@ -46,6 +46,59 @@ def another_session_changes(repo, plan):
         plan["code-scout"] = {"elsewhere": {"root": str(repo), "write": {".shop/work/i1/initiative.md": "changed elsewhere\n"}}}
     
     
    +@given("every round ends and every worker gives DONE, and while i1's researcher works another session changes "
    +       ".shop/work/i1/initiative.md and a session of i2 changes .shop/work/i2/initiative.md, both in the repository's own "
    +       "checkout without committing them")
    +def two_sessions_change(repo, plan):
    +    plan["default"] = {"status": "DONE"}
    +    i2 = (repo / ".shop/work/i2/initiative.md").read_text() + "\nChanged by a session of i2.\n"
    +    plan["code-scout"] = {"elsewhere": {"root": str(repo), "write": {".shop/work/i1/initiative.md": "changed elsewhere\n",
    +                                                                     ".shop/work/i2/initiative.md": i2}}}
    +
    +
    +@given("every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes "
    +       ".shop/work/i2/initiative.md in the repository's own checkout without committing it")
    +def i2_session_changes(repo, plan, context):
    +    """p2's gate round starts beside i1's researcher, writes the file, and its own end takes the change in (r218 holds
    +    for i2's own sessions), so no later round of i2 finds it uncommitted."""
    +    plan["default"] = {"status": "DONE"}
    +    context["i2"] = (repo / ".shop/work/i2/initiative.md").read_text() + "\nChanged by a session of i2.\n"
    +    plan["round:gate:p2"] = {"meet_agents": ["code-scout"], "elsewhere": {
    +        "root": str(repo), "commit": {".shop/work/i2/initiative.md": context["i2"]}}}
    +
    +
    +@then(parsers.re(r"nothing recorded of (?P<name>\w+) names (?P<path>\S+)$"))
    +def nothing_names(repo, name, path):
    +    assert path not in (repo / (".shop/work/i1/%s.md" % name)).read_text()
    +    log = [l for l in (repo / ".shop/work/i1/log.jsonl").read_text().splitlines() if name in l]
    +    assert not [l for l in log if path in l], log
    +
    +
    +@then(parsers.re(r"(?P<name>\w+) is green, nothing recorded of (?P=name) naming (?P<path>\S+)$"))
    +def green_nothing_naming(repo, context, name, path):
    +    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "green", (context["done"].stdout, context["done"].stderr)
    +    nothing_names(repo, name, path)
    +
    +
    +@then(".shop/work/i2/initiative.md is as i2's session changed it")
    +def i2_as_changed(repo, context):
    +    assert (repo / ".shop/work/i2/initiative.md").read_text() == context["i2"], (
    +        context["done"].stderr, git(repo, "status", "--porcelain"), git(repo, "log", "--format=%s"))
    +
    +
    +@then("no session of i1 or of i2 was taken as a fault")
    +def no_session_faulted(repo, context):
    +    for path in (repo / ".shop/work").glob("i[12]/*.md"):
    +        assert not section(path.read_text(), "Faults").strip(), (path, path.read_text())
    +    assert "faulted" not in git(repo, "log", "--format=%s"), git(repo, "log", "--format=%s")
    +
    +
    +@then("w1 is not failed and p2 is not failed")
    +def not_failed(repo, context):
    +    for path in (".shop/work/i1/w1.md", ".shop/work/i2/p2.md"):
    +        assert fields(repo / path)["status"] != "failed", (path, context["done"].stdout, context["done"].stderr)
    +
    +
     @given("the remote refuses pushes to the initiative branch")
     def remote_ahead(repo):
         """The remote's initiative branch has a commit the repository does not: git refuses to push over it."""
    @@ -90,7 +143,9 @@ def is_failed(repo, context, name, what):
         faults = section(text, "Faults")
         for words in FAULT_WORDS.get(what, [what]):
             assert words in faults, (words, text)
    -    assert git(repo, "status", "--porcelain", "--", ".shop/work") == "", git(repo, "status")
    +    # another initiative's path is not this run's to put back (r218): whether i2's own run has put it back by now
    +    # depends on when its sessions ended, so it is left out of what must be clean
    +    assert git(repo, "status", "--porcelain", "--", ".shop/work", ":(exclude).shop/work/i2") == "", git(repo, "status")
     
     
     @then("the initiative branch has none of the branch work/w1's commits")
    diff --git a/tests/scenarios/supervision_proposal_steps.py b/tests/scenarios/supervision_proposal_steps.py
    index bb21d8eb..259d3523 100644
    --- a/tests/scenarios/supervision_proposal_steps.py
    +++ b/tests/scenarios/supervision_proposal_steps.py
    @@ -122,6 +122,15 @@ def proposal_in_status(repo, plan, status, field, ids):
         commit_all(repo, "p1 is %s" % status)
     
     
    +@given(parsers.re(r"i1's capability-proposal p1 is withdrawn$"))
    +def proposal_withdrawn(repo):
    +    """p1 withdrawn, with no adds or changes clause: the bare status only (the phrasings above all carry a comma)."""
    +    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: withdrawn\nargues: [thing]\n"
    +          "adds: []\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n"
    +          % (full("capability-proposal", "p1"), full("initiative", "i1")))
    +    commit_all(repo, "p1 is withdrawn")
    +
    +
     @given(parsers.re(r"(?P<name>[pg]1) was written from the change list of i1's integrate round, whose drafts are kept at (?P<path>\S+)$"))
     def written_from_round(repo, name, path):
         file = repo / DIR / (name + ".md")
    @@ -131,7 +140,7 @@ def written_from_round(repo, name, path):
     
     
     @given(parsers.re(r"i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with (?P<asked>\"[^,]+?)(?:, given by its "
    -                  r"gate round)?,? and its Answers section with (?P<answers>\"[^,]+?)(?: only)?$"))
    +                  r"gate round)?,? and its Answers section with (?P<answers>\".+?)(?: only)?$"))
     def glossary_proposal_answered(repo, asked, answers):
         """g1 holds each quoted question as a bullet of its Questions and each quoted answer as a bullet of its Answers."""
         bullets = lambda text: "".join("- %s\n" % q for q in re.findall(r'"([^"]+)"', text))     # noqa: E731
    diff --git a/tests/scenarios/supervision_reintegrate_steps.py b/tests/scenarios/supervision_reintegrate_steps.py
    index 791a4073..0ccc7ca5 100644
    --- a/tests/scenarios/supervision_reintegrate_steps.py
    +++ b/tests/scenarios/supervision_reintegrate_steps.py
    @@ -27,9 +27,9 @@ def ledger_holds(repo, line):
         commit_all(repo, "i1's ledger")
     
     
    -@given(parsers.re(r"the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold"
    +@given(parsers.re(r"the apply round for (?P<name>[pg])1 applies nothing, giving that (?P=name)1's answers give what its drafts do not hold"
                       r"(?:, and no change list)?$"))
    -def apply_applies_nothing(plan):
    +def apply_applies_nothing(plan, name):
         plan["round:apply"] = {"status": "DONE", "fields": {"nothing_applied": NOTHING}}
     
     
    @@ -43,14 +43,65 @@ def written_from_first_round(repo, path, file):
         commit_all(repo, "p1 is awaiting-answer, written from i1's first integrate round")
     
     
    -@given(parsers.re(r'p1\'s ## Questions section holds "(?P<asked>[^"]*)", given by its gate round, and its Answers section '
    -                  r'"(?P<answered>[^"]*)"$'))
    -def questions_and_answers(repo, asked, answered):
    -    file = repo / DIR / "p1.md"
    +@given(parsers.re(r'(?P<name>[pg]1)\'s ## Questions section holds "(?P<asked>[^"]*)", given by its gate round, and its Answers '
    +                  r'section "(?P<answered>[^"]*)"$'))
    +def questions_and_answers(repo, name, asked, answered):
    +    file = repo / DIR / (name + ".md")
         file.write_text(file.read_text().rstrip("\n") + "\n\n## Questions\n\n- %s\n\n## Answers\n\n- %s\n" % (asked, answered))
    -    write(repo, DIR + "/log.jsonl", json.dumps({"time": "2026-10-15T00:00:00+00:00", "work-item": "p1", "before": "drafted",
    +    write(repo, DIR + "/log.jsonl", json.dumps({"time": "2026-10-15T00:00:00+00:00", "work-item": name, "before": "drafted",
                                                     "after": "awaiting-answer", "by": "work run"}) + "\n")
    -    commit_all(repo, "p1's questions and answers")
    +    commit_all(repo, "%s's questions and answers" % name)
    +
    +
    +@given(parsers.re(r"i1's capability-proposal p1, for thing, is awaiting-answer, its adds naming thing#r4 and thing#r5, its "
    +                  r"changes naming thing#r2 and its removes naming thing#r3$"))
    +def held_with_all_lists(repo):
    +    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [thing]\n"
    +          "adds: [thing#r4, thing#r5]\nchanges: [thing#r2]\nremoves: [thing#r3]\ndate: 2026-10-15\n---\n\n# thing\n\n"
    +          "The drafts of this proposal are in old/.\n" % (full("capability-proposal", "p1"), full("initiative", "i1")))
    +    commit_all(repo, "p1 is awaiting-answer, naming ids in all three lists")
    +
    +
    +@given(parsers.re(r'i1\'s glossary-proposal g1 is awaiting-answer, its adds naming the term "ledger", its changes the term '
    +                  r'"shelf" and its removes the term "loan"$'))
    +def held_glossary(repo):
    +    write(repo, DIR + "/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: awaiting-answer\nadds: [term/ledger]\n"
    +          "changes: [term/shelf]\nremoves: [term/loan]\ndate: 2026-10-15\n---\n\n# glossary\n\n"
    +          "The drafts of this proposal are in old/.\n" % (full("glossary-proposal", "g1"), full("initiative", "i1")))
    +    commit_all(repo, "g1 is awaiting-answer, naming terms in all three lists")
    +
    +
    +@given('the integrate round for p1 redrafts thing#r5 and gives DONE with a change list that adds thing#r5 on thing')
    +def integrate_redrafts_p1(plan):
    +    plan["round:integrate:p1"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", "adds": ["thing#r5"]}]},
    +                                  "write": {DRAFTS: DRAFT}}
    +
    +
    +@given('a round of the kind integrate is started for g1, redrafts the term "ledger" and gives DONE with a change list that adds '
    +       'the term "ledger" in the glossary')
    +def integrate_redrafts_g1(plan):
    +    plan["round:integrate:g1"] = {"status": "DONE", "fields": {"changes": [{"glossary": True, "adds": ["term/ledger"]}]},
    +                                  "write": {DRAFTS: DRAFT}}
    +    # r221: g1's apply round gives an answer its drafts do not hold, so an integrate round follows for g1
    +    plan["round:apply:g1"] = {"status": "DONE", "fields": {"unheld_answers": ["One line an event."]}}
    +
    +
    +@then(parsers.re(r"p1's adds name thing#r4 and thing#r5, its changes name thing#r2, and its removes name thing#r3$"))
    +def p1_keeps_lists(repo, context):
    +    text = (repo / DIR / "p1.md").read_text()
    +    held = lambda field: re.findall(r"\w+#r\d+", next(l for l in text.splitlines() if l.startswith(field + ":")))     # noqa: E731
    +    assert (held("adds"), held("changes"), held("removes")) == (["thing#r4", "thing#r5"], ["thing#r2"], ["thing#r3"]), (
    +        text, context["done"].stderr)
    +
    +
    +@then(parsers.re(r'g1\'s adds name the term "ledger", its changes the term "shelf", and its removes the term "loan"$'))
    +def g1_keeps_terms(repo, context):
    +    assert len(rounds(repo, "integrate", "g1")) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    +    text = (repo / DIR / "g1.md").read_text()
    +    held = lambda field: re.findall(r"term/\w+", next(l for l in text.splitlines() if l.startswith(field + ":")))     # noqa: E731
    +    assert (held("adds"), held("changes"), held("removes")) == (["term/ledger"], ["term/shelf"], ["term/loan"]), (
    +        text, context["done"].stderr)
    +    assert not (repo / DIR / "glossary.md").exists()
     
     
     @given(parsers.re(r"the integrate round for p1 (?P<writes>writes spec/capabilities/thing\.md under its drafts path and )?"
    @@ -66,10 +117,10 @@ def integrate_brief(repo, context):
         return found[0]["brief"]
     
     
    -@then("a round of the kind integrate was started for p1 after the apply round had ended")
    -def integrate_after_apply(repo, context):
    -    ended, began = position(repo, stage="apply", event="end"), position(repo, stage="integrate", event="start")
    -    assert len(rounds(repo, "integrate", "p1")) == 1, (starts(repo), context["done"].stderr)
    +@then(parsers.re(r"a round of the kind integrate was started for (?P<name>[pg]1) after the apply round had ended$"))
    +def integrate_after_apply(repo, context, name):
    +    ended, began = position(repo, name, stage="apply", event="end"), position(repo, name, stage="integrate", event="start")
    +    assert len(rounds(repo, "integrate", name)) == 1, (starts(repo), context["done"].stderr)
         assert ended is not None and began is not None and ended < began, (log_lines(repo), context["done"].stderr)
     
     
    diff --git a/tests/scenarios/supervision_rerun_steps.py b/tests/scenarios/supervision_rerun_steps.py
    new file mode 100644
    index 00000000..26080b8b
    --- /dev/null
    +++ b/tests/scenarios/supervision_rerun_steps.py
    @@ -0,0 +1,76 @@
    +"""supervision's steps about a scenario that fails each time it is run: its one second run, alone, before a merge is
    +refused (r219), and the question that gives both its runs (r220)."""
    +import re
    +
    +from pytest_bdd import given, then
    +
    +from .supervision_world import commit_all, log_lines, write
    +
    +ALWAYS_FEATURE = """Feature: Thing
    +
    +  @r1
    +  Scenario: it closes
    +    Given a thing
    +    Then it closes
    +"""
    +ALWAYS_STEPS = """from pytest_bdd import given, scenarios, then
    +
    +scenarios("../features/thing.feature")
    +
    +
    +@given("a thing")
    +def a_thing():
    +    pass
    +
    +
    +@then("it closes")
    +def closes(request):
    +    args = request.config.invocation_params.args
    +    with open(%r, "a") as runs:
    +        runs.write(("alone" if any("::" in str(a) for a in args) else "with") + "\\n")
    +    assert False, "it does not close"
    +"""
    +
    +
    +@given("the work-item's scenario \"it closes\", tagged @r1, fails on the implementer's branch each time it is run")
    +def closes_never(repo):
    +    """A pytest-bdd suite whose "it closes" fails in every run and notes in `closes.runs` how it was run."""
    +    write(repo, "features/thing.feature", ALWAYS_FEATURE)
    +    write(repo, "tests/test_thing.py", ALWAYS_STEPS % str(repo / "closes.runs"))
    +    (repo / ".shop/delivery.toml").unlink()
    +    commit_all(repo, "the scenario that never closes")
    +
    +
    +def runs_of(repo):
    +    path = repo / "closes.runs"
    +    return path.read_text().split() if path.exists() else []
    +
    +
    +@then("\"it closes\" was run once more, alone, after its run with w1's scenarios and before the merge of w1's branch "
    +      "was refused")
    +def closes_run_alone(repo, context):
    +    runs = runs_of(repo)
    +    assert runs[-1:] == ["alone"] and "with" in runs, (runs, context["done"].stderr)
    +    reruns = [l for l in log_lines(repo) if l.get("event") == "rerun" and l.get("work-item") == "w1"]
    +    assert len(reruns) == 1 and "it_closes" in reruns[0]["scenario"] and not reruns[0]["passed"], reruns
    +    text = (repo / ".shop/work/i1/w1.md").read_text()
    +    assert "status: awaiting-answer" in text, text
    +    assert not [l for l in log_lines(repo) if l.get("event") == "merged"], log_lines(repo)
    +
    +
    +@then("\"it closes\" was run no other time")
    +def closes_run_no_other(repo, context):
    +    runs = runs_of(repo)
    +    assert runs.count("alone") == 1, (runs, context["done"].stderr)
    +
    +
    +@then("w1's ## Questions holds a question giving both runs of \"it closes\": its run with w1's scenarios and its "
    +      "second run, alone")
    +def question_gives_both_runs(repo, context):
    +    text = (repo / ".shop/work/i1/w1.md").read_text()
    +    held = text.partition("## Questions")[2]
    +    commands = re.findall(r"`([^`]+)`", held)
    +    first = [c for c in commands if "::" not in c and "--work-item w1" in c]
    +    second = [c for c in commands if "::" in c and "test_it_closes" in c]
    +    assert first and second, (commands, held)
    +    assert "it does not close" in held.partition(second[0])[2], held
    diff --git a/tests/scenarios/supervision_tests_steps.py b/tests/scenarios/supervision_tests_steps.py
    index 6c018600..d00c93f2 100644
    --- a/tests/scenarios/supervision_tests_steps.py
    +++ b/tests/scenarios/supervision_tests_steps.py
    @@ -122,6 +122,40 @@ def thing_waits(repo):
         commit_all(repo, "the thing's suite")
     
     
    +CLOSES_FEATURE = """Feature: Thing
    +
    +  @r1
    +  Scenario: it closes
    +    Given a thing
    +    Then it closes
    +"""
    +CLOSES_STEPS = """from pytest_bdd import given, scenarios, then
    +
    +scenarios("../features/thing.feature")
    +
    +
    +@given("a thing")
    +def a_thing():
    +    pass
    +
    +
    +@then("it closes")
    +def closes(request):
    +    args = request.config.invocation_params.args
    +    assert any("::" in str(a) for a in args), "run with other scenarios, not alone: %s" % (args,)
    +"""
    +
    +
    +@given("the work-item's scenario \"it closes\", tagged @r1, fails on the implementer's branch in its run with w1's "
    +       "scenarios and passes there on its second run, alone")
    +def closes_alone(repo):
    +    """A pytest-bdd suite whose "it closes" fails unless its run was given its own node id."""
    +    write(repo, "features/thing.feature", CLOSES_FEATURE)
    +    write(repo, "tests/test_thing.py", CLOSES_STEPS)
    +    (repo / ".shop/delivery.toml").unlink()
    +    commit_all(repo, "the closing scenario")
    +
    +
     @given(parsers.parse("thing#r2 is accepted by {who}"))
     def r2_accepted(repo, who):
         names = [] if who == "no work-item" else who.replace(" only", "").split(" and ")
    diff --git a/tests/scenarios/test_requests.py b/tests/scenarios/test_requests.py
    index 0b0da6d6..1b872304 100644
    --- a/tests/scenarios/test_requests.py
    +++ b/tests/scenarios/test_requests.py
    @@ -2,6 +2,7 @@
     from pytest_bdd import scenarios
     
     from .requests_flow_steps import *
    +from .requests_session_steps import *
     from .requests_show_steps import *
     from .requests_steps import *
     from .requests_world_steps import *
    diff --git a/tests/scenarios/test_supervision.py b/tests/scenarios/test_supervision.py
    index fc1292b0..6126f915 100644
    --- a/tests/scenarios/test_supervision.py
    +++ b/tests/scenarios/test_supervision.py
    @@ -41,6 +41,7 @@ from .supervision_raise_steps import *
     from .supervision_review_steps import *
     from .supervision_reintegrate_steps import *
     from .supervision_request_steps import *
    +from .supervision_rerun_steps import *
     from .supervision_retire_steps import *
     from .supervision_rounds_steps import *
     from .supervision_session_faults_steps import *
    diff --git a/tests/scenarios/work_queue_list_steps.py b/tests/scenarios/work_queue_list_steps.py
    index 71ca72b3..0ff3167a 100644
    --- a/tests/scenarios/work_queue_list_steps.py
    +++ b/tests/scenarios/work_queue_list_steps.py
    @@ -1,10 +1,11 @@
     """features/work-queue.feature's steps of `work list` and `work show <target>` (r34-r39): requests under .shop/work/, the
     record of requests an initiative raised, and what the two commands print."""
     import json
    +import re
     
     from pytest_bdd import given, parsers, then
     
    -from .conftest import full
    +from .conftest import PATH, full
     
     
     @given(parsers.re(r"a request (?P<ident>q\d+) under \.shop/work/ that is (?P<status>[\w-]+)$"))
    @@ -52,11 +53,65 @@ def prints_status_as(context, whose, status):
         assert [w for w in printed(context) if whose in w and status in w], context["done"].stdout
     
     
    -@then(parsers.parse('it prints the question "{question}"'))
    +@then(parsers.re(r'it prints the question "(?P<question>[^"]*)"$'))
     def prints_question(context, question):
         assert question in context["done"].stdout, context["done"].stdout
     
     
    +@given("a request q1 kept in this context, whose asker is this context, that is delivered and in the asker's turn")
    +def request_kept_here(repo):
    +    from .test_work_queue import write
    +    write(repo, ".shop/work/requests/q1.md",
    +          "---\nid: %s\nkind: request\nasker: bounded-context/%s\nstatus: delivered\nturn: asker\n---\n\n# q1\n\n"
    +          "## Lines\n1. The first line.\n2. The second line.\n\n## Questions\n\n## Answers\n\n## Outcomes\n\n## Resolution\n"
    +          % (full("request", "q1"), PATH))
    +
    +
    +def fill(repo, section, *entries):
    +    path = repo / ".shop/work/requests/q1.md"
    +    path.write_text(path.read_text().replace("## %s\n" % section, "## %s\n%s" % (section, "".join(e + "\n" for e in entries)), 1))
    +
    +
    +@given("its line 1 has the line outcome accepted and its line 2 the line outcome refused")
    +def request_outcomes(repo):
    +    fill(repo, "Outcomes", "1. accepted", "2. refused")
    +
    +
    +@given(parsers.re(r'it has on line (?P<line>\d+) the question "(?P<question>[^"]*)" with the answer "(?P<answer>[^"]*)"$'))
    +def request_question(repo, line, question, answer):
    +    fill(repo, "Questions", "1. line %s: %s" % (line, question))
    +    fill(repo, "Answers", "1. %s" % answer)
    +
    +
    +@given("its resolution gives line 1 as thing#r7, delivered in version 0.23.0")
    +def request_resolution(repo):
    +    fill(repo, "Resolution", "1. thing#r7 0.23.0")
    +
    +
    +@then("it prints that it is the asker's turn")
    +def prints_asker_turn(context):
    +    assert "it is the asker's turn" in context["done"].stdout, context["done"].stdout
    +
    +
    +@then(parsers.re(r"it prints line (?P<a>\d+) with (?P<aw>\w+) and line (?P<b>\d+) with (?P<bw>\w+)$"))
    +def prints_line_outcomes(context, a, aw, b, bw):
    +    shown = context["done"].stdout.splitlines()
    +    for number, word in ((a, aw), (b, bw)):
    +        assert ["line %s: %s" % (number, word)] == [l.split(" - ")[0].strip() for l in shown if l.strip().startswith("line %s:" % number)], shown
    +
    +
    +@then(parsers.re(r'it prints the question "(?P<question>[^"]*)" and the answer "(?P<answer>[^"]*)"$'))
    +def prints_question_answer(context, question, answer):
    +    shown = context["done"].stdout
    +    assert re.search(r"(?m)^\s*question 1: .*%s" % re.escape(question), shown), shown
    +    assert re.search(r"(?m)^\s*answer 1: %s$" % re.escape(answer), shown), shown
    +
    +
    +@then("it prints its resolution, thing#r7 and 0.23.0")
    +def prints_resolution(context):
    +    assert re.search(r"(?m)^\s*resolution line 1: thing#r7 0\.23\.0$", context["done"].stdout), context["done"].stdout
    +
    +
     @then(parsers.re(r"it gives (?P<pairs>\S+ with .+)$"))
     def gives_pairs(context, pairs):
         shown = context["json"]
    diff --git a/tests/scenarios/work_queue_status_steps.py b/tests/scenarios/work_queue_status_steps.py
    index 31aa0ff8..68cfa566 100644
    --- a/tests/scenarios/work_queue_status_steps.py
    +++ b/tests/scenarios/work_queue_status_steps.py
    @@ -19,7 +19,30 @@ def open_with_proposal(repo, ident, state, proposal, pstatus):
         write(repo, ".shop/work/%s/%s.md" % (ident, proposal), item_text(proposal, pstatus, ident, "capability-proposal"))
     
     
    -@given(parsers.re(r"an initiative (?P<ident>\w+) under \.shop/work/ that is (?P<state>[^,]+), whose work-items? (?P<items>.+)$"))
    +def write_proposal(repo, ident, name, status):
    +    from .test_work_queue import item_text, write
    +    write(repo, ".shop/work/%s/%s.md" % (ident, name), item_text(name, status, ident, "capability-proposal"))
    +
    +
    +@given(parsers.re(r"(?P<ident>i\d+)'s capability-proposal (?P<name>p\d+) is (?P<status>[\w-]+)$"))
    +def one_proposal(repo, ident, name, status):
    +    write_proposal(repo, ident, name, status)
    +
    +
    +@given(parsers.re(r"(?P<ident>i\d+)'s capability-proposal (?P<first>p\d+) is (?P<s1>[\w-]+) and its capability-proposal "
    +                  r"(?P<second>p\d+) is (?P<s2>[\w-]+)$"))
    +def two_proposals(repo, ident, first, s1, second, s2):
    +    write_proposal(repo, ident, first, s1)
    +    write_proposal(repo, ident, second, s2)
    +
    +
    +@given(parsers.re(r"(?P<ident>i\d+) has no capability-proposal$"))
    +def no_proposal(repo, ident):
    +    for path in (repo / ".shop/work" / ident).glob("*.md"):
    +        assert "kind: capability-proposal" not in path.read_text(), path
    +
    +
    +@given(parsers.re(r"an initiative (?P<ident>\w+) under \.shop/work/ that is (?P<state>[^,]+), whose work-items?(?P<items>.+)$"))
     def with_state(repo, ident, state, items):
         from .test_work_queue import item_text, write
         text = "---\nid: %s\nkind: initiative\nstatus: %s\n---\n" % (full("initiative", ident), state.replace("neither done nor abandoned", "started"))
    diff --git a/tests/scripts/stub_claude.py b/tests/scripts/stub_claude.py
    index 1a744169..57ced9d6 100644
    --- a/tests/scripts/stub_claude.py
    +++ b/tests/scripts/stub_claude.py
    @@ -100,7 +100,8 @@ def bash(argv, command):
         """Run `command` if --allowedTools allows it as Bash; record that it ran or was refused."""
         line = shlex.join(command)
         if any(fnmatch.fnmatchcase(line, pattern) for pattern in allowed(argv, "Bash")):
    -        done = subprocess.run(command, capture_output=True, text=True, check=command[0] == "git")
    +        done = (git_retry(command[1:], None) if command[0] == "git"
    +                else subprocess.run(command, capture_output=True, text=True))
             record({"event": "ran", "tool": "Bash", "command": line, "code": done.returncode,
                     "output": done.stdout + done.stderr})
             return True
    @@ -108,6 +109,17 @@ def bash(argv, command):
         return False
     
     
    +def git_retry(args, cwd):
    +    """A git command in `cwd`, tried again for up to 10 s while git's index.lock is held by another process."""
    +    deadline = time.monotonic() + 10
    +    while True:
    +        done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    +        if done.returncode == 0 or "index.lock" not in done.stderr or time.monotonic() > deadline:
    +            done.check_returncode()
    +            return done
    +        time.sleep(0.05)
    +
    +
     def skill(argv, name):
         """Load the skill `name` if --allowedTools has `Skill(<name>)`; record that it was loaded (ran) or refused."""
         record({"event": "ran" if name in allowed(argv, "Skill") else "refused", "tool": "Skill", "command": name})
    @@ -224,9 +236,8 @@ def main(argv):
                 (other / rel).parent.mkdir(parents=True, exist_ok=True)
                 (other / rel).write_text(text)
             if "commit" in step["elsewhere"]:
    -            subprocess.run(["git", "add", "--", *files], cwd=other, check=True, capture_output=True)
    -            subprocess.run(["git", "commit", "-q", "-m", "another session's commit"], cwd=other, check=True,
    -                           capture_output=True)
    +            git_retry(["add", "--", *files], other)
    +            git_retry(["commit", "-q", "-m", "another session's commit"], other)
         for name in step.get("skills", []):
             skill(argv, name)
         for rel, text in step.get("write", {}).items():
    diff --git a/tests/scripts/test_supervise_change.py b/tests/scripts/test_supervise_change.py
    index faa469b7..bc5f4964 100644
    --- a/tests/scripts/test_supervise_change.py
    +++ b/tests/scripts/test_supervise_change.py
    @@ -34,7 +34,7 @@ def test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_propo
         found = entries({"changes": [{"capability": "thing", "adds": ["thing#r5"]},
                                      {"capability": "other", "adds": ["other#r1", "other#r2"], "removes": ["other#r8"]}]})
         holder.write_proposals(found, "drafts/", "p1")
    -    assert "adds: [thing#r5]\n" in (initiative / "p1.md").read_text()
    +    assert "adds: [thing#r1, thing#r5]\n" in (initiative / "p1.md").read_text()
         other = (initiative / "p2.md").read_text()
         assert "adds: [other#r1, other#r2]\n" in other
         assert "removes: [other#r9, other#r8]\n" in other
    @@ -53,6 +53,23 @@ def test_a_round_started_for_one_proposal_leaves_another_held_proposals_drafts_p
         assert "The drafts of this proposal are in old/." in (initiative / "p2.md").read_text()
     
     
    +def test_a_round_started_for_a_glossary_proposal_keeps_the_terms_its_change_list_does_not_name(tmp_path):
    +    initiative = tmp_path / "i1"
    +    initiative.mkdir()
    +    (initiative / "initiative.md").write_text("---\nid: initiative/a.io/b/c/i1\nkind: initiative\n---\n")
    +    (initiative / "g1.md").write_text(
    +        "---\nid: glossary-proposal/a.io/b/c/g1\nkind: glossary-proposal\nstatus: awaiting-answer\n"
    +        "adds: [term/ledger]\nchanges: [term/shelf]\nremoves: [term/loan]\n---\n\n# glossary\n\nThe drafts of this proposal are in old/.\n")
    +    holder = Changes()
    +    holder.dir = initiative
    +    found = entries({"changes": [{"glossary": True, "adds": ["term/desk"], "changes": ["term/shelf"]}]})
    +    written = holder.write_proposals(found, "new/", "g1")
    +    text = (initiative / "g1.md").read_text()
    +    assert written == [initiative / "g1.md"] and not (initiative / "glossary.md").exists()
    +    assert "adds: [term/ledger, term/desk]\n" in text and "changes: [term/shelf]\n" in text and "removes: [term/loan]\n" in text
    +    assert "are in new/." in text
    +
    +
     def test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids(tmp_path):
         written = write(tmp_path, [{"capability": "thing", "adds": ["thing#r3"]},
                                    {"capability": "thing", "adds": ["thing#r4"], "removes": ["thing#r1"]},
    diff --git a/tests/scripts/test_supervise_merge_rerun.py b/tests/scripts/test_supervise_merge_rerun.py
    new file mode 100644
    index 00000000..1f1b5875
    --- /dev/null
    +++ b/tests/scripts/test_supervise_merge_rerun.py
    @@ -0,0 +1,122 @@
    +"""supervise_merge: a scenario that failed gets one run alone however many runs it failed in (r219), and one that passes
    +that run alone counts as passing whatever another run gave (r222); a run with an error, a failure that is not a
    +scenario, or a rerun that ran no test is not taken back."""
    +import sys
    +from pathlib import Path
    +from types import SimpleNamespace
    +
    +import pytest
    +
    +sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    +
    +import supervise  # noqa: F401  (its import order settles the modules' circular imports)
    +import supervise_merge
    +from supervise_merge import Merge
    +
    +NODE = "tests/scenarios/test_thing.py::test_it_closes"
    +FAILED = "FAILED %s - boom\nSCENARIO %s\n" % (NODE, NODE)     # work_items names the failed tests that are scenarios
    +
    +
    +def ran(args, code, out=""):
    +    return SimpleNamespace(args=args, returncode=code, stdout=out, stderr="")
    +
    +
    +class Stubbed(Merge):
    +    def __init__(self, root):
    +        self.root, self.branch, self.logged, self.moves = root, "i1", [], []
    +        self.suite_out = FAILED
    +
    +    def under_work(self, tree, name):
    +        return []
    +
    +    def suite_record(self, tree, suite):
    +        return "Suite", ran(suite, 1, self.suite_out)
    +
    +    def log(self, **fields):
    +        self.logged.append(fields)
    +
    +    def move(self, *args):
    +        self.moves.append(args)
    +
    +
    +@pytest.fixture
    +def merge(monkeypatch, tmp_path):
    +    alone, alone_passes, rerun_out = [], [], ["1 passed"]
    +
    +    def run(command, **_):
    +        if any("::" in c for c in command):
    +            alone.append(command)
    +            passed = alone_passes[len(alone) - 1]
    +            return ran(command, 0 if passed else 1, rerun_out[0] if passed else "boom")
    +        return ran(command, 1, FAILED)
    +
    +    monkeypatch.setattr(supervise_merge.subprocess, "run", run)
    +    monkeypatch.setattr(supervise_merge, "git", lambda *a, **k: SimpleNamespace(stdout="x\n", returncode=0))
    +    monkeypatch.setattr(supervise_merge, "with_scripts", dict)
    +    tests = {"work_item": ["pytest", "-n", "auto", "--work-item", "w1"], "suite": ["pytest", "-n", "auto", "--work-item", "w1", "--whole-suite"]}
    +    return Stubbed(tmp_path), tests, alone, alone_passes, rerun_out
    +
    +
    +def test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges(merge):
    +    stubbed, tests, alone, passes, _ = merge
    +    passes.extend([True, False])     # a second alone run would fail: it must not happen
    +    assert stubbed.merge("w1", stubbed.root, tests) is None
    +    assert len(alone) == 1
    +    assert "--whole-suite" in alone[0]
    +    assert [alone[0][i + 1] for i, a in enumerate(alone[0]) if a == "-n"] == ["0"]     # no other -n value
    +    assert [l["scenario"] for l in stubbed.logged if l.get("event") == "rerun"] == [NODE]
    +
    +
    +def test_a_scenario_failing_in_both_runs_and_failing_alone_refuses_the_merge_after_one_run_alone(merge):
    +    stubbed, tests, alone, passes, _ = merge
    +    passes.extend([False, True])
    +    question = stubbed.merge("w1", stubbed.root, tests)
    +    assert question and "boom" in question
    +    assert len(alone) == 1
    +
    +
    +def test_a_failing_run_with_an_error_line_is_not_taken_back(merge):
    +    stubbed, tests, alone, passes, _ = merge
    +    stubbed.suite_out = "=== short test summary info ===\n" + FAILED + "ERROR tests/scenarios/test_x.py::t - setup\n"
    +    passes.append(True)
    +    assert stubbed.merge("w1", stubbed.root, tests)
    +    assert not alone
    +
    +
    +def test_a_failing_node_that_is_not_a_scenario_is_not_taken_back(merge):
    +    stubbed, tests, alone, passes, _ = merge
    +    stubbed.suite_out = "FAILED tests/scripts/test_y.py::test_y - boom\n"     # in a module that has scenarios( in it
    +    passes.append(True)
    +    assert stubbed.merge("w1", stubbed.root, tests)
    +    assert not alone
    +
    +
    +def test_a_suite_command_with_no_n_gets_none_for_the_rerun(merge):
    +    stubbed, tests, alone, passes, _ = merge
    +    tests["suite"] = ["pytest", "--work-item", "w1", "--whole-suite"]
    +    passes.append(True)
    +    assert stubbed.merge("w1", stubbed.root, tests) is None
    +    assert "-n" not in alone[0]
    +
    +
    +def test_an_error_count_in_a_failing_scenarios_captured_output_does_not_keep_it_from_being_taken_back(merge):
    +    stubbed, tests, _, passes, _ = merge
    +    stubbed.suite_out = FAILED + "Found 2 errors.\n1 failed, 3 passed in 1.0s\n"
    +    passes.append(True)
    +    assert stubbed.merge("w1", stubbed.root, tests) is None
    +
    +
    +def test_an_error_count_in_the_final_line_keeps_a_run_from_being_taken_back(merge):
    +    stubbed, tests, alone, passes, _ = merge
    +    stubbed.suite_out = FAILED + "1 failed, 3 passed, 1 error in 1.0s\n"
    +    passes.append(True)
    +    assert stubbed.merge("w1", stubbed.root, tests)
    +    assert not alone
    +
    +
    +def test_a_rerun_that_ran_no_test_counts_as_failed(merge):
    +    stubbed, tests, alone, passes, rerun_out = merge
    +    rerun_out[0] = "1 deselected"
    +    passes.append(True)
    +    assert stubbed.merge("w1", stubbed.root, tests)
    +    assert len(alone) == 1
    diff --git a/tests/scripts/test_work_items.py b/tests/scripts/test_work_items.py
    index 5e860673..2e4663da 100644
    --- a/tests/scripts/test_work_items.py
    +++ b/tests/scripts/test_work_items.py
    @@ -119,6 +119,18 @@ def test_one_requirement_outside_a_guarantees_capability_refuses_the_run(tmp_pat
         assert done.returncode != 0 and "w1 accepts none of the scenarios it collected" in done.stdout + done.stderr
     
     
    +def test_a_failed_scenario_is_named_in_the_summary_and_a_failed_test_that_is_not_one_is_not(tmp_path):
    +    repo = consumer(tmp_path, "thing#r1-r2")
    +    (repo / "tests/test_thing.py").write_text(STEPS.replace("    pass", "    assert False"))
    +    (repo / "test_probe.py").write_text("def test_probe():\n    assert False\n")
    +    done = pytest(repo, "--work-item", "w1")
    +    lines = (done.stdout + done.stderr).splitlines()
    +    named = [l for l in lines if l.startswith("SCENARIO ")]
    +    assert sorted(named) == ["SCENARIO tests/test_thing.py::test_it_answers",
    +                             "SCENARIO tests/test_thing.py::test_it_waits"], done.stdout
    +    assert not [l for l in named if "probe" in l]
    +
    +
     def test_a_move_to_a_status_outside_the_lifecycle_is_refused(tmp_path):
         sys.path.insert(0, str(SCRIPTS))
         import workqueue
    diff --git a/tests/scripts/test_work_show_request.py b/tests/scripts/test_work_show_request.py
    new file mode 100644
    index 00000000..15c16dbc
    --- /dev/null
    +++ b/tests/scripts/test_work_show_request.py
    @@ -0,0 +1,22 @@
    +"""work-queue r59: `work show <request>` lists every line of the request, a line with no line outcome yet as unsettled."""
    +import pathlib
    +import sys
    +
    +SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
    +sys.path.insert(0, str(SCRIPTS))
    +import workqueue_list
    +
    +REQUEST = ("---\nid: request/o/p/c/q1\nkind: request\nasker: bounded-context/o/p/c\nstatus: accepted\nturn: upstream\n---\n\n"
    +           "# q1\n\n## Lines\n1. The first line.\n2. The second line.\n\n## Questions\n\n## Answers\n\n"
    +           "## Outcomes\n1. accepted\n\n## Resolution\n")
    +
    +
    +def test_a_line_with_no_line_outcome_is_listed_as_unsettled(tmp_path, capsys):
    +    (tmp_path / "spec").mkdir()
    +    (tmp_path / "spec/index.md").write_text("---\nid: bounded-context/o/p/c\nkind: bounded-context\n---\n")
    +    (tmp_path / ".shop/work/requests").mkdir(parents=True)
    +    (tmp_path / ".shop/work/requests/q1.md").write_text(REQUEST)
    +    assert workqueue_list.show(tmp_path, "q1", False) == 0
    +    shown = capsys.readouterr().out.splitlines()
    +    assert "  line 1: accepted - The first line." in shown, shown
    +    assert "  line 2: unsettled - The second line." in shown, shown
    diff --git a/tests/scripts/test_workqueue_done.py b/tests/scripts/test_workqueue_done.py
    index 575ce4f8..f0ee9571 100644
    --- a/tests/scripts/test_workqueue_done.py
    +++ b/tests/scripts/test_workqueue_done.py
    @@ -1,5 +1,5 @@
    -"""work-queue r23 with observation 2026-10-27-done-with-proposal-open: an initiative whose work-items are all green or
    -withdrawn is not done while one of its capability-proposals is neither formulated, withdrawn nor merged."""
    +"""work-queue r62 and r47: an initiative whose work-items are all green or withdrawn is not done while one of its
    +capability-proposals is neither formulated nor withdrawn (merged, a legacy status, holds it too)."""
     import pathlib
     import sys
     
    @@ -16,7 +16,7 @@ PROPOSAL = "---\nid: capability-proposal/ex.com/prod/ctx/i1-thing\nkind: capabil
     
     
     @pytest.mark.parametrize("status, done", [("awaiting-answer", False), ("drafted", False), ("approved", False),
    -                                          ("formulated", True), ("withdrawn", True), ("merged", True)])
    +                                          ("formulated", True), ("withdrawn", True), ("merged", False)])
     def test_an_open_proposal_keeps_the_initiative_from_done(tmp_path, status, done):
         (tmp_path / "spec").mkdir()
         (tmp_path / "spec/index.md").write_text(INDEX)
