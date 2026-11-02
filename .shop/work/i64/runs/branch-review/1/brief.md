# branch review of i64

Initiative: .shop/work/i64
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: 86582d02951f1643d542fd5f162fb3ba5fd7abc2
Head: b95f4ce3cca3f3025cd07012d7222ba90cbdf383
Worktree: /tmp/work-run-i64-k7xmcdka/branch-review
Run directory: /tmp/work-run-i64-k7xmcdka/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i64-k7xmcdka/branch-review/.shop/scratch/branch-review/result.json

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
- .shop/work/i64/runs/w242/2-plan/plan.md
- .shop/work/i64/runs/w242/3-implement/report.md
- .shop/work/i64/runs/w242/4-implement/report.md
- .shop/work/i64/runs/w242/5-implement/report.md
- .shop/work/i64/runs/w242/6-review/findings.md

## Runs

Ran at: b95f4ce3cca3f3025cd07012d7222ba90cbdf383

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w242 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 12%]
    ........................................................................ [ 19%]
    ........................................................................ [ 25%]
    .........................x.....x.......x.............................x.. [ 31%]
    .x.x..x.x.x.x.............................X...x.x...x...x.x.....x....... [ 38%]
    xxx..................................................................... [ 44%]
    .......................................................................X [ 51%]
    .....................X.................................................. [ 57%]
    ............................................x..Xx....................... [ 63%]
    ...............................X........................................ [ 70%]
    ...................X........................x........x....X............. [ 76%]
    uuuuu......uu......uuuuuuuuuuu..............x.......................u... [ 81%]
    .....u..u.....u..u.u.....u....X..u....u......u.x...u.......u............ [ 86%]
    ..u..........u....u........u.u....u.........u.uu..u....su...uuu.X..u.... [ 92%]
    ..u.....uu...u..u.......u.u..u........u.uu..........................X... [ 97%]
    ................X.........X.....                                         [100%]
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
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_the_fields_of_a_requests_form_and_nothing_it_says_is_done[on q2 the passing of q2's turn-body-q2's turn is the upstream's-awaiting-upstream] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_answer_and_turn_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the passing of q2's turn-q2's turn is the asker's-the turn on q2] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_the_fields_of_a_requests_form_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"-awaiting-asker] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_the_fields_of_a_requests_form_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"-awaiting-asker] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_writer_writing_the_owners_part_of_a_request_from_another_context_in_its_own_turn_is_refused_naming_the_owner_and_nothing_changes[upstream-asker-the upstream answers that question with "The work queue"-the upstream ctx-u's repository-answers] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_list_prints_each_request_with_its_status_and_whose_turn_it_is - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_askers_repository_in_the_askers_turn_prints_that_it_is_the_askers_turn_with_each_question_the_asker_has_not_answered - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_upstreams_repository_while_the_upstream_holds_unsent_it_has_not_sent_with_the_turn_prints_that_the_asker_has_not_seen_it[the line outcome accepted of line 1-run `work outcome q1 1 accepted`] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_upstreams_repository_while_the_upstream_holds_unsent_it_has_not_sent_with_the_turn_prints_that_the_asker_has_not_seen_it[the question "Which queue?"-asked the question "Which queue?" on line 1 of q1] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_show_run_in_the_askers_repository_after_the_upstream_resolves_the_request_prints_each_accepted_lines_requirement_id_and_the_version_that_holds_it - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_answer_and_turn_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by requests-deda9fa6, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_that_redrafts_some_of_its_lines_leaves_the_proposal_with_the_requirement_ids_its_change_list_does_not_name - expected: accepted by w238, supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_glossaryproposal_that_redrafts_some_of_its_terms_leaves_the_proposal_with_the_terms_its_change_list_does_not_name - expected: accepted by w238, supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_work_run_ends_with_node_awaitinganswer_it_exits_with_an_error_printing_node_with_its_open_questions[p1-i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Which unit is the limit in?" and "Is the old reader kept?", given by its gate round, and its Answers section answering only "Is the old reader kept?" with "Yes."] - expected: accepted by w243, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_work_run_ends_with_node_awaitinganswer_it_exits_with_an_error_printing_node_with_its_open_questions[w2-i1's work-item w2 is awaiting-answer, its ## Questions section with "Which unit is the limit in?" and "Is the old reader kept?", and its Answers section answering only "Is the old reader kept?" with "Yes."] - expected: accepted by w243, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_a_researchers_result_that_gives_an_empty_file_set_is_taken_as_the_researchers_file_set - expected: accepted by w243, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_a_formulate_round_that_formulates_nothing_because_the_proposals_answers_change_lines_not_in_spec_is_followed_by_a_new_integrate_round_for_the_proposal - expected: accepted by w243, neither green nor withdrawn
    1090 passed, 1 skipped, 25 xfailed, 12 xpassed, 1084 warnings, 56 subtests passed in 37.69s

### w242's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w242
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........uu..uuuuu.........uuuuuuuuuuu.....uuu..........uuu.............. [ 27%]
    ....u..u..u...........................u...u..............u......u......u [ 62%]
    ...........u....u..........u..u.....uu.uuus.uu..u..uuuuu..u...uu..u.u... [ 87%]
    ....................uu...                                                [100%]
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
    
    tests/scenarios/test_supervision.py::test_an_apply_round_that_gives_an_answer_the_drafts_it_applied_do_not_hold_for_a_glossaryproposal_is_followed_by_a_new_integrate_round_for_the_glossaryproposal
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_an_apply_round_that_gives_an_answer_the_drafts_it_applied_do_not_hold_for_a_glossaryproposal_is_followed_by_a_new_integrate_round_for_the_glossaryproposal
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    184 passed, 1 skipped, 450 warnings, 56 subtests passed in 6.63s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 86582d02951f1643d542fd5f162fb3ba5fd7abc2
Exit code: 1
Output:
    == ruff ==
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:4:9: SIM115 Use a context manager for opening files
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:5:6: SIM115 Use a context manager for opening files
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:15:5: PLC0206 Extracting value from dictionary without calling `.items()`
    .shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py:42:1: SIM115 Use a context manager for opening files
    scripts/supervise_merge.py:127:13: PLC0206 Extracting value from dictionary without calling `.items()`
    tests/scenarios/supervision_proposal_steps.py:102:62: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_proposal_steps.py:146:94: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_reintegrate_steps.py:13:44: F401 [*] `.supervision_world.git` imported but unused
    tests/scenarios/supervision_reintegrate_steps.py:174:115: FURB167 [*] Use of regular expression alias `re.M`
    tests/scenarios/test_supervision.py:14:1: I001 [*] Import block is un-sorted or un-formatted
    tests/scripts/test_supervise_merge_rerun.py:11:19: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    tests/scripts/test_supervise_merge_rerun.py:12:25: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    tests/scripts/test_supervise_merge_rerun.py:13:36: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    tests/scripts/test_supervise_merge_rerun.py:52:58: PIE807 [*] Prefer `dict` over useless lambda
    Found 15 errors.
    [*] 10 fixable with `--fix`.
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
    6b8591215b42fe3895c917b2d27b3b51d6dc8c6a w242 work add: i64/w242 drafted
    41320afbef4e844b828f70d323e36a2e86f0b9fa w242 work: w242 drafted -> researched
    c0652cd8ebb878cd31cc2143b1ec7625d4ec6507 w242 work: w242 researched -> planned
    0d3fe1d9aeddc361f12a04947955cd8c03f4aad1 w242 work: w242 planned -> ready
    082922c2bf5368961f4625446ad548cd363c7ebf w242 work: w242 ready -> claimed
    a39b47a350c9fd878f39408ad5001b9865df61c4 w242 work: w242 claimed -> awaiting-answer
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
    24a2db83c625014d98464bd680ccd5de41ac62b3 none work add: i62/w245 drafted
    e5df071cb18ab9b5c2df0c001a0bc364df0dbadf none work: w245 drafted -> researched
    f2481751b1da78bcaa63c6a16cb3380fbe44651a none work: w245 researched -> planned
    5189abd228eda0e3c8b9e61ee0bc6065071259f1 none work: w245 planned -> ready
    696ca6c8deb2e407248d6ccd555473f4bb9a484a none work: w245 ready -> claimed
    5695ee5687ada8b59251653d7edf4de9573dbecd none work: w245 claimed -> awaiting-answer
    53c7d203c6b76430b56af181de74c8bf719dce7c none i62: the proposal and w245 name r219 and r220 again
    96e59e4f1877d2e98e5935147c289349c742e9be none work answer: w245 awaiting-answer -> ready
    5a7b2b67b5bf29ae4d723279db117802f36e647e w242 work answer: w242 awaiting-answer -> ready
    f4a60df4c1b6535ccf9e02a28514149f7465fc96 none work answer: w243 awaiting-answer -> ready
    21f8b90f3b08fe6545756faa4f92d3cbad275559 none work: w245 ready -> claimed
    b274fa52c0946750c55fe88294694d9de032b0ed none work run: a scenario failing before a merge gets one second run, alone (r222)
    83e3b8ee0a74a082398c3fa31c27130e670b5804 none work run: r219 and r220 bound; the refused merge's question gives the second run (w245)
    088d32c7d2806021b5fe6c3261a071e94ab4a726 none work: w245 claimed -> done
    4208f8d1b2039c5274fa876b94e7cb11f3f54693 none work: w245 done -> awaiting-answer
    38679e71b88faaf2a12c85188cbfe422d5eae303 w242 work: w242 ready -> claimed
    f58a418121159295a9b09e5cee9a33b2b06bf3da w242 work: w242 claimed -> awaiting-answer
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
    373facfeedb93b10662c328ed28ce1580d1eb161 none work answer: w245 awaiting-answer -> ready
    4f3b78f140bf3918b2c77c7dda845feb030c3d47 w242 work answer: w242 awaiting-answer -> ready
    87cfd675d46e28a5353e6e5e5191cf9c0850e1d3 none work answer: w243 awaiting-answer -> ready
    fafcdba3f1425b592771106c2a551636ad7e34ca none work: w245 ready -> claimed
    588797826bbe6be812f3f53b5eaaea9369effe94 none work run: a scenario failing in several runs gets one run alone before a merge (r219, r222)
    0e0dca3c55604bb234c9e08c77fdcd46398db0cb none work: w245 claimed -> done
    7b95194384eeb3f86403e2db82e031db707970db none work: w245 done -> awaiting-answer
    4a3f3b0d6834115fd3bedc1554d42ee09ae588e2 w242 work: w242 ready -> claimed
    4fa77b4356d50ca9394d39c3574543cb21a9e4b8 w242 supervision r221: a sent-back glossary-proposal gets a new integrate round
    fa0901b0230cf5adf3757de0cf79b93d52610e41 w242 work: w242 claimed -> done
    b95f4ce3cca3f3025cd07012d7222ba90cbdf383 w242 work: w242 done -> green

## Change

The change from 86582d02951f1643d542fd5f162fb3ba5fd7abc2 to b95f4ce3cca3f3025cd07012d7222ba90cbdf383, without the workflow's own files:

    diff --git a/features/requests.feature b/features/requests.feature
    index 9168ca9d..69ad593c 100644
    --- a/features/requests.feature
    +++ b/features/requests.feature
    @@ -236,8 +236,9 @@ Feature: Requests
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
    @@ -246,6 +247,21 @@ Feature: Requests
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
    @@ -408,9 +424,9 @@ Feature: Requests
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
    @@ -425,9 +441,9 @@ Feature: Requests
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
    @@ -436,28 +452,31 @@ Feature: Requests
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
    @@ -465,6 +484,47 @@ Feature: Requests
         Then work prints q1 with open and the upstream's turn
         And it prints q2 with awaiting-asker and the asker's turn
     
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
       @r64
       Scenario: list prints, with its date, each observation that the source of no initiative and of no request names
         Pins that list shows the observations nothing has taken up yet, with the date of each, and leaves out any that an initiative or a request already names.
    diff --git a/features/supervision.feature b/features/supervision.feature
    index 2cc04494..e8f245a7 100644
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
    @@ -1604,8 +1607,9 @@ Feature: Supervision
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
    @@ -1874,10 +1878,11 @@ Feature: Supervision
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
    @@ -1885,9 +1890,11 @@ Feature: Supervision
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
    @@ -2051,3 +2058,74 @@ Feature: Supervision
         Then .shop/work/i1/initiative.md is as its last commit holds it
         And w1 is failed, naming .shop/work/i1/initiative.md
         And nothing recorded of w1 names .shop/work/i2/initiative.md
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
    index 49880cb9..7085f72e 100644
    --- a/features/work-queue.feature
    +++ b/features/work-queue.feature
    @@ -57,37 +57,6 @@ Feature: Work queue
         And nothing under the new initiative's directory under .shop/work/ differs from main's last commit
         And it exits successfully
     
    -  @r23 @deprecated
    -  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done (deprecated)
    -    Deprecated for: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    -    Pins that the command that completes an initiative's work ends the initiative when one of its work-items is green, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    -    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
    -    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    -    And <request>
    -    When the session runs `work withdraw w2`
    -    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    -    And .shop/work/i1/initiative.md gives i1's status as done
    -    And it exits successfully
    -
    -    Examples:
    -      | request                                                                                     |
    -      | no request kept in this context names i1                                                    |
    -      | a request q1 kept in this context, whose asker is this context, names i1 and is delivered   |
    -      | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
    -      | a request q1 kept in this context, whose asker is this context, names i2 and is accepted    |
    -
    -  @r23 @deprecated
    -  Scenario: retry that makes an initiative's last open work-item green again sets the initiative to done (deprecated)
    -    Deprecated for: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    -    Pins that retry, like withdraw, is a command whose change can complete an initiative, and that it ends the initiative when it does.
    -    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is failed
    -    And .shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed
    -    And no request kept in this context names i1
    -    When the session runs `work retry w2`
    -    Then .shop/work/i1/w2.md gives w2's status as green
    -    And .shop/work/i1/initiative.md gives i1's status as done
    -    And it exits successfully
    -
       @r62
       Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
         Pins that whichever command completes an initiative's work, withdraw or retry, ends the initiative when one of its work-items is green and each of its capability-proposals is formulated or withdrawn, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    @@ -120,6 +89,18 @@ Feature: Work queue
         And .shop/work/i1/initiative.md gives i1's status as started
         And it exits successfully
     
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
       @r34 @deprecated
       Scenario: list prints each initiative, each request and each work-item under .shop/work/ with its status (deprecated)
         Deprecated for: removal
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
    diff --git a/scripts/supervise_merge.py b/scripts/supervise_merge.py
    index ccbf71f4..8e3531dd 100644
    --- a/scripts/supervise_merge.py
    +++ b/scripts/supervise_merge.py
    @@ -113,6 +113,26 @@ class Merge:
             with self.lock:
                 git(self.root, "branch", "-q", "-d", "work/" + name)     # merged, so no longer needed; once its worktree is gone (r18)
     
    +    def taken_back(self, name, tree, command, runs):
    +        """Whether every scenario the failing `runs` name passes on one more run, alone (r219, r222); each is run once,
    +        and the run is logged under its own event. A failing run that names no scenario is not taken back."""
    +        failing = {}
    +        for done in runs:
    +            ids = [l.split(" ", 1)[1].split(" - ")[0] for l in (done.stdout + done.stderr).splitlines()
    +                   if l.startswith("FAILED ") and "::" in l]
    +            if done.returncode != 0 and not ids:
    +                return False
    +            failing.update(dict.fromkeys(ids))
    +        alone = [a for i, a in enumerate(command) if a != "-n" and command[max(i - 1, 0)] != "-n"]
    +        for node in failing:
    +            again = subprocess.run(alone + [node], cwd=tree, capture_output=True, text=True, env=with_scripts())
    +            failing[node] = again.returncode == 0
    +            if not failing[node]:
    +                self.second_runs.append("its second run, alone, `%s`:\n%s" % (
    +                    " ".join(again.args), (again.stdout + again.stderr).strip()))
    +            self.log(**{"work-item": name, "stage": "merge", "event": "rerun", "scenario": node, "passed": failing[node]})
    +        return all(failing.values())
    +
         def merge(self, name, tree, tests):
             """The branch rebased on the initiative branch, put back under .shop/work/, tested and merged (r4, r6); None,
             else the question it gives the person instead of the merge. What the worker left uncommitted is cleaned away
    @@ -126,10 +146,13 @@ class Merge:
             record, suite = self.suite_record(tree, tests["suite"])     # its expected red counted (r43)
             self.log(**{"work-item": name, "stage": "merge", "event": "suite", "record": record})
             scenarios = subprocess.run(tests["work_item"], cwd=tree, capture_output=True, text=True, env=with_scripts())
    -        for done in (scenarios, suite):
    -            if done.returncode != 0:
    -                return "commits on which %s's scenarios and the whole suite pass are missing: `%s` failed on %s's branch " \
    -                       "work/%s:\n%s" % (name, " ".join(done.args), name, name, (done.stdout + done.stderr).strip())
    +        self.second_runs = []
    +        failed = [done for done in (scenarios, suite) if done.returncode != 0]
    +        if failed and not self.taken_back(name, tree, tests["work_item"], (scenarios, suite)):     # once, whatever the runs
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
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index b9900647..c975c806 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -64,6 +64,7 @@ from what using it shows.
     - [r172] **While** a glossary-proposal is `awaiting-answer` and a question that a round of the kind `gate` gave on it has no answer, `work run` shall start no round of the kind `apply` for it.
     - [r116] **When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers.
     - [r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
    +- [r221] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold for a glossary-proposal, `work run` shall start a new round of the kind `integrate` for the glossary-proposal.
     - [r151] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied.
     - [r141] **When** `work run` starts a round of the kind `integrate` for a capability-proposal that has answers, `work run` shall give the round the capability-proposal's questions and answers and the initiative's ledger, with the accepted lines of the request the initiative fulfils.
     - [r142] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory.
    @@ -180,6 +181,9 @@ from what using it shows.
     - [r42] **If** a worker ends without a result file that `work run` can read, then `work run` shall transition the work-item to `failed`, recording how its session ended.
     - [r43] **When** `work run` runs the whole suite before a merge, `work run` shall count as expected each failing scenario whose requirement a work-item other than the one being merged accepts and that is neither `green` nor `withdrawn`.
     - [r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.
    +- [r219] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge.
    +- [r220] **If** the second run of a scenario that r219 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item.
    +- [r222] **When** the second run of a scenario that r219 makes passes, `work run` shall take the scenario as passing in r4's merge of the work-item branch.
     - [r44] **When** `work run` writes a worker's brief, `work run` shall tell the worker to write its result file first with the outcome `PARTIAL`, and keep it current as it works.
     - [r45] **If** a worker's session ends in an error or at its turn limit, exits with an error, or leaves output that holds no JSON result, then `work run` shall transition the work-item to `failed`, recording how the session ended.
     - [r46] **If** the main checkout's `.shop/work/` has uncommitted changes when `work run` starts, then `work run` shall exit with an error, naming them, and change nothing.
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
    index 791a4073..6c01e0fa 100644
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
     
     
    @@ -66,10 +66,10 @@ def integrate_brief(repo, context):
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
    diff --git a/tests/scripts/test_supervise_merge_rerun.py b/tests/scripts/test_supervise_merge_rerun.py
    new file mode 100644
    index 00000000..be744d76
    --- /dev/null
    +++ b/tests/scripts/test_supervise_merge_rerun.py
    @@ -0,0 +1,75 @@
    +"""supervise_merge: a scenario that failed gets one run alone however many runs it failed in (r219), and one that passes
    +that run alone counts as passing whatever another run gave (r222)."""
    +import sys
    +from pathlib import Path
    +from types import SimpleNamespace
    +
    +import pytest
    +
    +sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    +
    +import supervise  # noqa: E402,F401  (its import order settles the modules' circular imports)
    +import supervise_merge  # noqa: E402
    +from supervise_merge import Merge  # noqa: E402
    +
    +NODE = "tests/test_thing.py::test_it_closes"
    +
    +
    +def ran(args, code, out=""):
    +    return SimpleNamespace(args=args, returncode=code, stdout=out, stderr="")
    +
    +
    +class Stubbed(Merge):
    +    def __init__(self, root):
    +        self.root, self.branch, self.logged, self.moves = root, "i1", [], []
    +
    +    def under_work(self, tree, name):
    +        return []
    +
    +    def suite_record(self, tree, suite):
    +        return "Suite", ran(suite, 1, "FAILED %s - boom\n" % NODE)
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
    +    alone = []
    +
    +    def run(command, **_):
    +        if any("::" in c for c in command):
    +            alone.append(command)
    +            return ran(command, 0 if alone_passes[len(alone) - 1] else 1, "boom")
    +        return ran(command, 1, "FAILED %s - boom\n" % NODE)
    +
    +    alone_passes = []
    +    monkeypatch.setattr(supervise_merge.subprocess, "run", run)
    +    monkeypatch.setattr(supervise_merge, "git", lambda *a, **k: SimpleNamespace(stdout="x\n", returncode=0))
    +    monkeypatch.setattr(supervise_merge, "with_scripts", lambda: {})
    +    tests = {"work_item": ["pytest", "-n", "auto", "--work-item", "w1"], "suite": ["pytest", "--whole-suite"]}
    +    stubbed = Stubbed(tmp_path)
    +    return stubbed, tests, alone, alone_passes
    +
    +
    +def test_a_scenario_failing_in_both_runs_gets_one_run_alone_and_a_pass_there_merges(merge):
    +    stubbed, tests, alone, passes = merge
    +    passes.extend([True, False])     # a second alone run would fail: it must not happen
    +    assert stubbed.merge("w1", tmp_path_of(stubbed), tests) is None
    +    assert len(alone) == 1 and "-n" not in alone[0]
    +    assert [l["scenario"] for l in stubbed.logged if l.get("event") == "rerun"] == [NODE]
    +
    +
    +def test_a_scenario_failing_in_both_runs_and_failing_alone_refuses_the_merge_after_one_run_alone(merge):
    +    stubbed, tests, alone, passes = merge
    +    passes.extend([False, True])
    +    question = stubbed.merge("w1", tmp_path_of(stubbed), tests)
    +    assert question and "boom" in question
    +    assert len(alone) == 1
    +
    +
    +def tmp_path_of(stubbed):
    +    return stubbed.root
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
