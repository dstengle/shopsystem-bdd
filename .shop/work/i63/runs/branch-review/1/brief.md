# branch review of i63

Initiative: .shop/work/i63
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: db2873b73a08e86a12a10f8de97aae3b22914af6
Head: 331edbd40721c1a35432dbdda0f46b46d915832f
Worktree: /tmp/work-run-i63-dcnr_g9t/branch-review
Run directory: /tmp/work-run-i63-dcnr_g9t/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i63-dcnr_g9t/branch-review/.shop/scratch/branch-review/result.json

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
- .shop/work/i63/runs/w236/2-plan/plan.md
- .shop/work/i63/runs/w236/3-implement/report.md
- .shop/work/i63/runs/w236/4-implement/report.md
- .shop/work/i63/runs/w236/5-implement/report.md
- .shop/work/i63/runs/w236/6-review/findings.md
- .shop/work/i63/runs/w237/3-plan/plan.md
- .shop/work/i63/runs/w237/4-plan/plan.md
- .shop/work/i63/runs/w237/5-implement/report.md
- .shop/work/i63/runs/w237/6-implement/report.md
- .shop/work/i63/runs/w237/7-review/findings.md

## Runs

Ran at: 331edbd40721c1a35432dbdda0f46b46d915832f

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w236 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 13%]
    ........................................................................ [ 19%]
    ........................................................................ [ 26%]
    x....................................................................... [ 32%]
    ....x.x.x...x..................................................xx.x.x... [ 39%]
    ............x.....x..................................................... [ 45%]
    ................................................................X....... [ 52%]
    ........................................................................ [ 58%]
    .................................X...................................... [ 65%]
    ................X.............................x.x....x.X.......X........ [ 71%]
    .X.................................................................uu... [ 77%]
    .............uuuuu........................u......u...............u...u.. [ 83%]
    u....u..u.u.....u.u.....u..u...........uu...................x..x....u... [ 89%]
    .u......u........u..uu.uusu.u...u.uu...uuu.u........u.u..u....u......u.u [ 93%]
    ...u..........................uuuuuuuuuuu............................... [ 99%]
    ...........                                                              [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
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
    
    tests/scenarios/test_supervision.py: 301 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py: 301 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-no request kept in this context names i1] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is withdrawn and its capability-proposal p2 is formulated-a request q1 kept in this context, whose asker is this context, names i1 and is delivered] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[retry-failed-.shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed-green-i1's capability-proposal p1 is formulated-no request kept in this context names i1] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-a request q1 kept in this context, whose asker is another context, names i1 and is accepted] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-a request q1 kept in this context, whose asker is this context, names i2 and is accepted] - expected: accepted by work-queue, neither green nor withdrawn
    1084 passed, 1 skipped, 16 xfailed, 6 xpassed, 868 warnings, 56 subtests passed in 33.36s

### w236's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w236
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    .....uu.........uuuuu....uuuuuuuuuuu.............uu..u............u.u... [ 28%]
    ...uu....u..u....u...............u.u..............u......u....u....u.... [ 62%]
    .u......u...........u.u.u.u.....s.....u...uu.....uuu...uu.uuu......uuu.u [ 89%]
    .....u................                                                   [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
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
    
    tests/scenarios/test_supervision.py::test_a_change_to_shopwork_in_the_repositorys_own_checkout_less_another_initiatives_path_run_side_by_side_that_is_not_committed_when_a_worker_ends_is_put_back_and_the_workitems_transition_is_to_failed_naming_the_file
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_a_change_to_shopwork_in_the_repositorys_own_checkout_less_another_initiatives_path_run_side_by_side_that_is_not_committed_when_a_worker_ends_is_put_back_and_the_workitems_transition_is_to_failed_naming_the_file
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    181 passed, 1 skipped, 258 warnings, 56 subtests passed in 6.84s

### w237's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w237
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........uu...u.uuu.u...uuuuuuuuuuu......u..u.u.......u.....u............ [ 27%]
    uu.....u........u......u.............u....u........uu..u..............u. [ 61%]
    ......u..........u..u.u....s...u.u...u....uu.uu..uu.uuu....u..u.u..u.u.. [ 88%]
    .....u..................                                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
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
    
    tests/scenarios/test_supervision.py::test_a_change_to_another_initiatives_path_under_shopwork_made_by_that_initiatives_session_while_a_session_of_one_initiative_worked_is_not_put_back
    tests/scenarios/test_supervision.py::test_what_changed_in_the_repositorys_own_checkout_while_a_session_of_one_initiative_worked_is_checked_without_the_paths_of_another_initiative_run_side_by_side
    tests/scenarios/test_supervision.py::test_a_change_to_another_initiatives_path_under_shopwork_made_by_that_initiatives_session_while_a_session_of_one_initiative_worked_faults_no_session
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_a_change_to_another_initiatives_path_under_shopwork_made_by_that_initiatives_session_while_a_session_of_one_initiative_worked_is_not_put_back
    tests/scenarios/test_supervision.py::test_what_changed_in_the_repositorys_own_checkout_while_a_session_of_one_initiative_worked_is_checked_without_the_paths_of_another_initiative_run_side_by_side
    tests/scenarios/test_supervision.py::test_a_change_to_another_initiatives_path_under_shopwork_made_by_that_initiatives_session_while_a_session_of_one_initiative_worked_faults_no_session
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    183 passed, 1 skipped, 262 warnings, 56 subtests passed in 4.61s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base db2873b73a08e86a12a10f8de97aae3b22914af6
Exit code: 1
Output:
    == ruff ==
    .shop/work/i63/runs/supervision/1-gate/mk.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i63/runs/supervision/1-gate/mk.py:10:93: SIM115 Use a context manager for opening files
    tests/scripts/stub_claude.py:208:51: FURB167 [*] Use of regular expression alias `re.M`
    tests/scripts/stub_claude.py:209:51: FURB167 [*] Use of regular expression alias `re.M`
    Found 4 errors.
    [*] 3 fixable with `--fix`.
    == vulture ==
    clean
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
    features/supervision.feature: a worker's outcome DONE makes the work-item's transition to its next status (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a researcher's DONE with questions puts those questions into the planner's brief (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply> (deprecated) | for: r209 and r210 | no scenario has that title
    features/supervision.feature: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer (deprecated) | for: removal | deprecated for removal
    features/work-queue.feature: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done (deprecated) | for: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done | features/work-queue.feature @r62
    features/work-queue.feature: retry that makes an initiative's last open work-item green again sets the initiative to done (deprecated) | for: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done | features/work-queue.feature @r62
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
    a1dcd3871a335e24d09fae713a542e1a15567103 w236 work add: i63/w236 drafted
    471affff914ab109c855a576ed84f03990eaa934 w236 work: w236 drafted -> researched
    975cc62dc8e185a723b750f960fe02641e9adae3 w236 work: w236 researched -> planned
    8d2ac2e94146109b51f968abee512fc118d4d6a8 w236 work: w236 planned -> ready
    d857fa764e81aa6a72f8f42f2882f42a9fec2324 w236 work: w236 ready -> claimed
    36bdede78cfd7c1e3da07cd39529eae691c72745 w236 work: w236 claimed -> awaiting-answer
    c03c1c97f079ddd5f7944c1945e79504457cfcab w236 work answer: w236 awaiting-answer -> ready
    defd468467761563cae9bd0e8ce7a3b1cc5bbc7c w236 work: w236 ready -> claimed
    703757dbec0ec95991d11526932bb8a693958590 w236 work: w236 claimed -> awaiting-answer
    a411ea7ac0c1bb7bc1733dbf6c7736a54ea5b341 none work: i63 hand repair: supervision proposal ids restored again after apply round 17 (q34)
    54a128de1d344032493aab17683c91be31bb0a36 w237 work add: i63/w237 drafted
    ded24eb3819a77c507decd0118a700901fccc009 w236 work answer: w236 awaiting-answer -> ready
    f6cebaad94aa098cc993821739b853f04599471d none work note: i63
    9b773e6830b133a4fe2e05fc5da8e4f7b8be31d6 w236 work: w236 ready -> claimed
    d8f57cc87205057f503813fb4d0fc23503333437 w236 supervision: a change under another run's initiative is neither put back nor named (r218)
    94f0a74839197378abc31c92d26dea87614d0cd4 w236 supervision: the r218 scenario's clean-status check leaves out i2's path, which i2's own run may or may not have put back
    e03136b879357dec28654b872c402580ff6d1012 w236 work: w236 claimed -> done
    ca314284728c2c5c1409dcec6f21b1076c16b123 w237 work: w237 drafted -> awaiting-answer
    6305a40288d141619d6d2404dea73862257c46c5 w236 work: w236 done -> green
    79d97ed27f8a2c3f2b006a801c63b593b4967557 w237 work answer: w237 awaiting-answer -> drafted
    c490ee8496fa8b987ebe2cef6d10241c9ca06466 none work request: q43
    898d1e93407044477f4009eed51e653cf61506a2 w237 work: w237 drafted -> researched
    aeaec7551a9a33592bd189bd91c545d63112e8b7 w237 work: w237 researched -> awaiting-answer
    28abf0aafaec94672e110e2e4e087033c67d1324 w237 work answer: w237 awaiting-answer -> researched
    e4d1ffc86e2cceaae939631f9b8b602af969f5e7 w237 work: w237 researched -> planned
    0a5504f1e25a859c581e7cb3a279c9cfe106f184 w237 work: w237 planned -> ready
    441b188d957ddd402efa2b8a0903b82e9f2a4479 w237 work: w237 ready -> claimed
    c06026b933a9aff3460bdca6b57843476b62b978 w237 work: w237 claimed -> awaiting-answer
    d072fdcd90ad88bd0e580b5009254b07236289e6 w237 work answer: w237 awaiting-answer -> ready
    eeb9110eaf4774505848e782b069c56503a51432 w237 work: w237 ready -> claimed
    a9cb75362de65618a885d5c54e0a5e3d94cc5131 w237 Steps for r214-r216: another initiative's change is not checked, put back or faulted
    fd8364d17803abcead31232fac413894a9cf76d6 w237 stub_claude: git commands retry while index.lock is held
    d3935d0a7910bc567ad9278575d662f0025cb1b5 w237 work: w237 claimed -> done
    331edbd40721c1a35432dbdda0f46b46d915832f w237 work: w237 done -> green

## Change

The change from db2873b73a08e86a12a10f8de97aae3b22914af6 to 331edbd40721c1a35432dbdda0f46b46d915832f, without the workflow's own files:

    diff --git a/features/supervision.feature b/features/supervision.feature
    index 0a27c6a2..8000add5 100644
    --- a/features/supervision.feature
    +++ b/features/supervision.feature
    @@ -566,8 +566,9 @@ Feature: Supervision
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
    @@ -1987,3 +1988,42 @@ Feature: Supervision
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
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index 52ddddfd..dd81beb3 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -4,7 +4,7 @@ title: Supervision
     narrator: the person who started `work run`
     group: service
     rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163, r149, r32, r9, r105]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163, r149, r32, r9, r105, r28, r217]
     ---
     
     # Supervision
    @@ -158,7 +158,10 @@ from what using it shows.
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
