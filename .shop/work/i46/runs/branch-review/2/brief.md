# branch review of i46

Initiative: .shop/work/i46
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Head: 3779411dd590407e8e3f84075b2725716df68f69
Worktree: /tmp/work-run-i46-vz485uoj/branch-review
Run directory: /tmp/work-run-i46-vz485uoj/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i46-vz485uoj/branch-review/.shop/scratch/branch-review/result.json

Review the initiative branch from its base. You start in your worktree: run every command from there and never change directory. Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` and `questions`.

Read:
- spec/capabilities/spec-integration.md
- spec/capabilities/design-model-check.md
- spec/capabilities/supervision.md
- design-decision/one-spec-per-context
- design-decision/gate-on-behaviour-lines
- design-decision/spec-writers-blind-to-code
- design-decision/controller-per-spec-round
- design-decision/light-decisions
- design-decision/references-are-ids
- design-decision/workflow-capabilities-are-guarantees
- design-decision/the-ledger-is-tracked
- design-decision/the-context-runs-without-a-coordinator
- design-decision/the-glossary-is-a-target-of-spec-work
- design-decision/final-layout
- design-decision/model-check-solves-with-clingo
- design-decision/a-scenario-names-one-requirement
- design-decision/query-commands-answer-in-their-output
- design-decision/retired-ids-in-capability-frontmatter
- design-decision/work-file-forms
- design-decision/capability-ids-are-context-scoped
- design-decision/one-requirement-form
- design-decision/review-of-work-items
- design-decision/work-items-named-by-ids
- design-decision/a-script-supervises-delivery
- design-decision/worker-results-are-files
- design-decision/work-item-lifecycle-as-run
- design-decision/the-file-set-is-the-claim
- design-decision/the-v3-agents
- design-decision/exits-are-successful-or-errors
- design-decision/a-ruling-returns-to-the-asking-stage
- design-decision/answers-not-rulings
- design-decision/requests-written-through-work
- design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done
- .shop/work/i46/runs/w219/2-plan/plan.md
- .shop/work/i46/runs/w219/3-implement/report.md
- .shop/work/i46/runs/w219/4-review/findings.md
- .shop/work/i46/runs/w221/2-plan/plan.md
- .shop/work/i46/runs/w221/3-implement/report.md
- .shop/work/i46/runs/w221/4-implement/report.md
- .shop/work/i46/runs/w221/5-implement/report.md
- .shop/work/i46/runs/w221/6-review/findings.md
- .shop/work/i46/runs/w222/2-plan/plan.md
- .shop/work/i46/runs/w222/3-implement/report.md
- .shop/work/i46/runs/w222/4-implement/report.md
- .shop/work/i46/runs/w222/5-review/findings.md
- .shop/work/i46/runs/w222/6-review/findings.md
- .shop/work/i46/runs/w223/2-plan/plan.md
- .shop/work/i46/runs/w223/3-implement/report.md
- .shop/work/i46/runs/w223/4-review/findings.md
- .shop/work/i46/runs/w224/2-plan/plan.md
- .shop/work/i46/runs/w224/3-implement/report.md
- .shop/work/i46/runs/w224/4-review/findings.md
- .shop/work/i46/runs/w225/2-plan/plan.md
- .shop/work/i46/runs/w225/3-implement/report.md
- .shop/work/i46/runs/w225/4-implement/report.md
- .shop/work/i46/runs/w225/5-review/findings.md
- .shop/work/i46/runs/w225/6-review/findings.md
- .shop/work/i46/runs/w225/7-implement/report.md
- .shop/work/i46/runs/w225/8-review/findings.md
- .shop/work/i46/runs/w226/2-plan/plan.md
- .shop/work/i46/runs/w226/3-implement/report.md
- .shop/work/i46/runs/w226/4-review/findings.md

## Runs

Ran at: 3779411dd590407e8e3f84075b2725716df68f69

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w219 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 13%]
    ........................................................................ [ 20%]
    ........................................................................ [ 26%]
    ..x........x......x............................................xx.x..xx. [ 33%]
    ..............................................xx.x...................... [ 40%]
    ........................................................................ [ 46%]
    ........................................................................ [ 53%]
    ........................................................................ [ 60%]
    ........................................................................ [ 66%]
    ........................................................................ [ 73%]
    ...................................uu..uuuuu......uuuuuuuuuuu........... [ 78%]
    ................................uu..uu..u....u...u..u...........u....... [ 84%]
    ...u........u..u..........u........u............u.u.............uuuu.u.. [ 90%]
    .....u..u.u..u..uuus.uu..u..u.........u..u.u.......u...u.......u........ [ 94%]
    ......................................................                   [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py: 290 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py: 290 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by w212, neither green nor withdrawn
    1066 passed, 1 skipped, 11 xfailed, 622 warnings, 56 subtests passed in 33.64s

### w219's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w219
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    .uuuuuuuuuuuuuuuu.....uu..........................u.u..u............u... [ 29%]
    ....u..u..u......u...uu............u..............u.......u....uu.u..... [ 61%]
    ........u..u.......u.uu..u....u..uu......u..su.uu..uu...u.u...uu.u.u..u. [ 86%]
    ........................                                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_spec_integration.py::test_a_round_of_the_kind_integrate_that_drafts_a_change_to_the_glossary_gives_the_terms_it_adds_changes_and_removes_in_the_change_lists_entry_for_the_glossary_and_in_no_entry_for_a_capability
    tests/scenarios/test_spec_integration.py::test_while_the_person_has_not_approved_the_terms_of_a_glossaryproposal_no_round_applies_any_of_them_to_specindexmd
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_spec_integration.py::test_a_round_of_the_kind_integrate_that_drafts_a_change_to_the_glossary_gives_the_terms_it_adds_changes_and_removes_in_the_change_lists_entry_for_the_glossary_and_in_no_entry_for_a_capability
    tests/scenarios/test_spec_integration.py::test_while_the_person_has_not_approved_the_terms_of_a_glossaryproposal_no_round_applies_any_of_them_to_specindexmd
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    183 passed, 1 skipped, 36 warnings, 56 subtests passed in 6.54s

### w220's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w220
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ...uuuuuuuuuu...u..uuuuu....uu.......................u...uu..u.......... [ 29%]
    ..u......u...u.....u...u.u...........u....................u.u........u.. [ 63%]
    .....u.......u....u..u..u.u.....u....u.u..s.u...uuuuuu..u.uuu...u.uu..u. [ 86%]
    ........................                                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_spec_integration.py::test_a_round_of_the_kind_integrate_that_drafts_a_change_to_the_glossary_gives_the_terms_it_adds_changes_and_removes_in_the_change_lists_entry_for_the_glossary_and_in_no_entry_for_a_capability
    tests/scenarios/test_spec_integration.py::test_while_the_person_has_not_approved_the_terms_of_a_glossaryproposal_no_round_applies_any_of_them_to_specindexmd
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_spec_integration.py::test_a_round_of_the_kind_integrate_that_drafts_a_change_to_the_glossary_gives_the_terms_it_adds_changes_and_removes_in_the_change_lists_entry_for_the_glossary_and_in_no_entry_for_a_capability
    tests/scenarios/test_spec_integration.py::test_while_the_person_has_not_approved_the_terms_of_a_glossaryproposal_no_round_applies_any_of_them_to_specindexmd
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    183 passed, 1 skipped, 36 warnings, 56 subtests passed in 4.45s

### w221's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w221
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ...uu....uuuuuuu.uuuuuuuuu................................u...........u. [ 24%]
    u......u...........u.........u....u....u.u........uu.................... [ 55%]
    .........uu..u.......u.................u.u......u...u...........u.u.u..u [ 83%]
    ..s...uuu...u..uu...u.u.uu...u...u...u....uu.........                    [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    212 passed, 1 skipped, 32 warnings, 56 subtests passed in 4.42s

### w222's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w222
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ...uuuuu...uuuuuuuuuuu....uu......................u.u.....u............. [ 29%]
    ..u...u..u...u....u...u...u............u.....u.......u...............u.. [ 63%]
    ..u..u.u............u.u......u....u......uu..u..u.uuuu..u.u...uu.u..u..u [ 88%]
    ..u...u.....s...........                                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_a_glossaryproposal_awaitinganswer_with_a_question_from_its_gate_round_that_has_no_answer_is_given_to_no_apply_round
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_naming_the_glossary_gives_a_drafted_glossaryproposal_with_the_terms_it_adds_changes_and_removes_in_the_glossary
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_naming_the_glossary_gives_a_drafted_glossaryproposal_with_the_terms_it_adds_changes_and_removes_in_the_glossary
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_a_glossaryproposal_awaitinganswer_with_a_question_from_its_gate_round_that_has_no_answer_is_given_to_no_apply_round
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_naming_the_glossary_gives_a_drafted_glossaryproposal_with_the_terms_it_adds_changes_and_removes_in_the_glossary
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_naming_the_glossary_gives_a_drafted_glossaryproposal_with_the_terms_it_adds_changes_and_removes_in_the_glossary
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    183 passed, 1 skipped, 38 warnings, 56 subtests passed in 4.52s

### w223's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w223
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ...uuuuuuuuuuuuuuuu.......uu............................u..uu...u....... [ 29%]
    ...u.u.u.......u..u.........u........u..u...u..............u.......uu... [ 61%]
    .......u.u.....u..u.......u........uu..us....u..u..u.u.uu...u.uu.u...u.u [ 87%]
    ...u...u..................                                               [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_under_a_delegation_a_question_of_the_initiative_that_names_named_is_left_for_the_person_and_given_to_no_session[the glossary-proposal g1-Does scripts/log.py wait for g1 to be applied?]
    tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_of_the_initiative_that_names_neither_a_term_of_the_glossary_nor_a_glossaryproposal_goes_to_a_session_of_its_own_given_only_the_delegation_and_the_files_it_names_that_reply[Answer only the questions on the queue's tests; ask me everything else.-leaves it for the person-w1's question and p1's question have no answer, w1 and p1 awaiting-answer]
    tests/scenarios/test_supervision.py::test_under_a_delegation_a_question_of_the_initiative_that_names_named_is_left_for_the_person_and_given_to_no_session[the term "ledger"-Does scripts/log.py write the ledger?]
    tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_of_the_initiative_that_names_neither_a_term_of_the_glossary_nor_a_glossaryproposal_goes_to_a_session_of_its_own_given_only_the_delegation_and_the_files_it_names_that_reply[Please get everything delivered. Do not stop to ask me questions or permission.-answers it-w1's question and p1's question each have the session's answer]
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_under_a_delegation_a_question_of_the_initiative_that_names_named_is_left_for_the_person_and_given_to_no_session[the glossary-proposal g1-Does scripts/log.py wait for g1 to be applied?]
    tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_of_the_initiative_that_names_neither_a_term_of_the_glossary_nor_a_glossaryproposal_goes_to_a_session_of_its_own_given_only_the_delegation_and_the_files_it_names_that_reply[Answer only the questions on the queue's tests; ask me everything else.-leaves it for the person-w1's question and p1's question have no answer, w1 and p1 awaiting-answer]
    tests/scenarios/test_supervision.py::test_under_a_delegation_a_question_of_the_initiative_that_names_named_is_left_for_the_person_and_given_to_no_session[the term "ledger"-Does scripts/log.py write the ledger?]
    tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_of_the_initiative_that_names_neither_a_term_of_the_glossary_nor_a_glossaryproposal_goes_to_a_session_of_its_own_given_only_the_delegation_and_the_files_it_names_that_reply[Please get everything delivered. Do not stop to ask me questions or permission.-answers it-w1's question and p1's question each have the session's answer]
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    185 passed, 1 skipped, 40 warnings, 56 subtests passed in 4.46s

### w224's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w224
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ..uuuuuuuuuuu....uuuuu.........uu..................u.uu.....u........... [ 29%]
    ......uu.u.......u..u........u....................u........uu..u........ [ 63%]
    ..u........u....u...u.u.....u..u....us....uu.uu..uu...u..uuu..uu....uu.. [ 88%]
    .u..u...................                                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_the_gate_round_of_a_capabilityproposal_is_asked_only_for_the_questions_on_the_lines_that_proposal_adds_changes_or_removes
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_the_requirement_ids_it_adds_changes_and_removes_on_that_capability
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_the_gate_round_of_a_capabilityproposal_is_asked_only_for_the_questions_on_the_lines_that_proposal_adds_changes_or_removes
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_the_requirement_ids_it_adds_changes_and_removes_on_that_capability
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    183 passed, 1 skipped, 36 warnings, 56 subtests passed in 4.43s

### w225's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w225
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ..uuuuu...uuuuuuuuuuu...uu............................u..uu............. [ 28%]
    ...u.uu.......u...u...........u......u.....u....u...........u..u......u. [ 61%]
    .u....u......u.s..............u...u.....u.....u.uu..uu.u..u..uuu.uu..u.. [ 87%]
    .u.u...u...u..................                                           [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_an_initiative_that_changes_only_the_glossary_its_glossaryproposal_approved_and_its_terms_committed_to_specindexmd_is_set_done
    tests/scenarios/test_supervision.py::test_the_kind_round_of_a_glossaryproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[gate-drafted]
    tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_glossaryproposal_ends_the_proposal_is_awaitinganswer
    tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_glossaryproposal_ends_having_applied_its_drafts_the_proposal_is_approved
    tests/scenarios/test_supervision.py::test_a_drafted_glossaryproposal_is_given_to_a_gate_round_asked_only_for_the_questions_on_the_terms_it_adds_changes_or_removes
    tests/scenarios/test_supervision.py::test_the_kind_round_of_a_glossaryproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[apply-awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", and its Answers section with "One file."]
    tests/scenarios/test_supervision.py::test_a_glossaryproposal_whose_every_question_from_its_gate_round_has_an_answer_is_given_to_an_apply_round_with_its_answers
    tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_glossaryproposal_ends_having_applied_its_drafts_no_formulate_round_is_started_for_the_proposal
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_an_initiative_that_changes_only_the_glossary_its_glossaryproposal_approved_and_its_terms_committed_to_specindexmd_is_set_done
    tests/scenarios/test_supervision.py::test_the_kind_round_of_a_glossaryproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[gate-drafted]
    tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_glossaryproposal_ends_the_proposal_is_awaitinganswer
    tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_glossaryproposal_ends_having_applied_its_drafts_the_proposal_is_approved
    tests/scenarios/test_supervision.py::test_a_drafted_glossaryproposal_is_given_to_a_gate_round_asked_only_for_the_questions_on_the_terms_it_adds_changes_or_removes
    tests/scenarios/test_supervision.py::test_the_kind_round_of_a_glossaryproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[apply-awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", and its Answers section with "One file."]
    tests/scenarios/test_supervision.py::test_a_glossaryproposal_whose_every_question_from_its_gate_round_has_an_answer_is_given_to_an_apply_round_with_its_answers
    tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_glossaryproposal_ends_having_applied_its_drafts_no_formulate_round_is_started_for_the_proposal
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    189 passed, 1 skipped, 48 warnings, 56 subtests passed in 4.41s

### w226's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w226
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    uuu..uuuuuuuu.uuuuu..........uu........................u.uu...u....u.u.. [ 28%]
    u..........u....u....u....u..................u..u....................u.. [ 61%]
    u....u.....u..u..s..............u..u..uu..uuu..uu.u....u.uu.u....u.uu..u [ 89%]
    u...u...................                                                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_the_gate_round_of_a_capabilityproposal_is_asked_only_for_the_questions_on_the_lines_that_proposal_adds_changes_or_removes
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_the_requirement_ids_it_adds_changes_and_removes_on_that_capability
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_the_gate_round_of_a_capabilityproposal_is_asked_only_for_the_questions_on_the_lines_that_proposal_adds_changes_or_removes
    tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_the_requirement_ids_it_adds_changes_and_removes_on_that_capability
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    183 passed, 1 skipped, 36 warnings, 56 subtests passed in 4.31s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 134745663cfa0a109b8564370c2464ef9ee9a7d5
Exit code: 1
Output:
    == ruff ==
    .shop/work/i46/runs/design-model-check/1-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/1-formulate/splice.py:4:7: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/1-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/2-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/2-formulate/splice.py:4:33: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/2-formulate/splice.py:6:1: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/1-formulate/splice.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i46/runs/supervision/1-formulate/splice.py:2:9: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/1-formulate/splice.py:15:7: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/1-formulate/splice.py:23:1: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/6-formulate/splice.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i46/runs/supervision/6-formulate/splice.py:2:9: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/6-formulate/splice.py:9:7: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/6-formulate/splice.py:16:1: SIM115 Use a context manager for opening files
    scripts/supervise_change.py:91:75: B023 Function definition does not bind loop variable `field`
    scripts/supervise_change.py:91:92: B023 Function definition does not bind loop variable `mine`
    scripts/supervise_change.py:118:104: B023 Function definition does not bind loop variable `said`
    scripts/workqueue.py:248:5: I001 [*] Import block is un-sorted or un-formatted
    tests/scenarios/design_model_check_problems.py:6:23: F401 [*] `.conftest.CONTEXT` imported but unused
    tests/scenarios/design_model_check_problems.py:6:32: F401 [*] `.conftest.I1` imported but unused
    tests/scenarios/design_model_check_work.py:6:27: F401 [*] `.conftest.THING` imported but unused
    tests/scenarios/supervision_integrate_steps.py:81:5: RUF059 Unpacked variable `commit` is never used
    tests/scenarios/supervision_proposal_steps.py:102:62: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_proposal_steps.py:137:94: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_reintegrate_steps.py:13:44: F401 [*] `.supervision_world.git` imported but unused
    tests/scenarios/supervision_reintegrate_steps.py:174:115: FURB167 [*] Use of regular expression alias `re.M`
    tests/scenarios/test_design_model_check.py:7:1: I001 [*] Import block is un-sorted or un-formatted
    tests/scripts/test_supervise_answers.py:9:19: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    tests/scripts/test_supervise_answers.py:10:40: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    Found 29 errors.
    [*] 13 fixable with `--fix` (1 unsafe fix available with `--fix --unsafe-fixes`).
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
    features/supervision.feature: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer (deprecated) | for: removal | deprecated for removal
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

    abb7bdd93a28a7f195871b0ae24ec7ea2c66ff65 none work note: i46
    a2a554c4a418a64e31e7321c7d157ebf55c9bffd none work note: i46
    92e82b4e66a3e0ec546c4a4a53a79bd9c1470934 none spec: q30 glossary as a target of spec work (i46), lines approved 2026-10-28 by the person ("yes, all recommended"; round 2 and 3 "yes"), no delegation; adds spec-integration#r54, spec-integration#r55, supervision#r158, supervision#r159, supervision#r160, supervision#r161, supervision#r162, supervision#r163, supervision#r164, supervision#r165, supervision#r166, supervision#r167, supervision#r168, supervision#r169, supervision#r170, design-model-check#r122, design-model-check#r123, design-model-check#r124, term/glossary-proposal, design-decision/the-glossary-is-a-target-of-spec-work; changes term/status, term/answer, spec-consistency rests_on; removes spec-integration#r17, supervision#r92, supervision#r77, supervision#r104, design-model-check#r27 (retired; replaced by r159, r163, r168, r124); decision 0073 supersedes 0033
    15c2f7488a22d20fc0dd862b0258369606e53018 none work: i46 proposed -> started; capability-proposals supervision, spec-integration, design-model-check approved at the gate kept in session (spec commit 92e82b4e)
    a0295498e885e64ca3796519b6227b1c8387ac43 none formulate: design-model-check r123 r124 (r27 scenarios deprecated); r122 left as a question
    0d95185bc55f2f07070403b6e751343b23606862 none work note: i46
    883b574c425b8762096c7548eafb011da5338936 none work: design-model-check approved -> awaiting-answer
    a714768458094610ffaa059b08387b3cad8868b9 none Formulate spec-integration r54 r55
    48d1d0cbc9ff4c38ccfe17a0fdfc2ff9f6c591fe none work note: i46
    7ef2d04f7db49dd08511f59594c3c9a38de39007 none work: spec-integration approved -> formulated
    4580cd4530fec308ae9eadd8f148ad61c4d95e53 none work request: q32
    edf0301ea3bb4fab05f49f245ab197e46df389e3 none formulate i46 supervision: scenarios r159 r161-r170, five scenarios of r92 r77 r104 deprecated; r158 r160 left as questions
    c325cfe510f658460d42aed8c83373c0aa16155a none work note: i46
    441c5954f5c91e8274f50d68280cca7571e1ba01 none Merge branch 'round/supervision-1-formulate'
    ef6956305af28d22a0ac8914cf43952648f813de none work: supervision approved -> awaiting-answer
    942384ff6f751b29cf893d0bcd10eec476a96399 w219 work add: i46/w219 drafted
    b4d3632ed2b9ef3b1452fb8122b4e8cd18f26ccd w219 work: w219 drafted -> researched
    e3c56f80c1815f9f0b717c58d894d737c99854f9 w219 work: w219 researched -> planned
    07da6b11b0f9f06ff6af3a434d62a28e62b0858f w219 work: w219 planned -> ready
    a732bf6ea7033d389f7874fea527b2a0d27793f1 w219 work: w219 ready -> claimed
    085527d80d564642f27e9601f76929a4484655e2 w219 spec-integration r54: a glossary entry in the change list, terms in no capability's entry
    55bed875fca3bd159d7edec923ca70fa30ae0d67 w219 spec-integration r55: an apply round withholds the terms of glossary-proposals the person has not approved
    ae62d73dca681971a1b48ba518d3bb2533fb6bad w219 work: w219 claimed -> done
    1f6680407a4a5a2d5f75dd89d2414238f54dace8 w219 work: w219 done -> green
    44d15c5637c0d279fe6237f21a1e6a5f019f1fde none branch review 1 of i46
    395c23bc43f4a91505e66a7b8e2f378074590a01 w220 work add: i46/w220 drafted
    c407fbccaa9419b04440ab4016a832f80fcf041d w220 work: w220 drafted -> awaiting-answer
    4d8873f53e09da696fa1670fafdd9f815907b9ad none work answer: supervision
    92861a37ab3fd9dfd59744287a06dab62e6b2efa none work answer: supervision
    18d89dc148c1a379fa390d35bb9b283a3cc62e34 none work answer: design-model-check
    9291aae0a8753f17c31b6a60c5b8a7b254307e1d w220 work withdraw: w220 awaiting-answer -> withdrawn
    2029def6ad26d21e5477789983960eb51feda1b5 none work note: i46
    d6c9967635671b5566f62817ebe8aab791937c50 none Formulate design-model-check r122: a term an approved glossary-proposal removes is excused wherever named (the person, 2026-10-28)
    7ac13f449c999d9405353ef3c510b92843e5db93 none work note: i46
    ddd6cc666edb3d058f0076f976a529a5fc55a398 none work: design-model-check awaiting-answer -> formulated
    cc25511436a7a7a839a88aec28962f72cfcea9a1 none work note: i46
    88c15f6e44ab1289aa394fb2c4cfe21478f6559b none work: supervision awaiting-answer -> awaiting-answer
    24f8dc616597699a51a95a1f6f88eebfcb4391d1 none work note: i46
    a56133c36e8ebaa260491f3fd8acab560ea32dbe none work: supervision awaiting-answer -> drafted
    27dcfd0e7369eaeaf4568dc5617292ef9ff2755f none work note: i46
    0243aea5e3b5f00bb2ccc985ee03d801789bc68a none work: supervision drafted -> awaiting-answer
    2d5e55e4ddf9711e9a9d018c0d27f8c7505bd51c w221 work add: i46/w221 drafted
    ad5af4ae662e60277d50d3ae2bced0c24108c4a8 w221 work: w221 drafted -> researched
    4506f01baf52a17f5112d6185173e4d6b03553eb w221 work: w221 researched -> planned
    a6addfa78b06cba63dfa8bc19301d898efa8a6f5 w221 work: w221 planned -> ready
    79f947138d822b4e5b97ee0031057f86a01c78ac w221 work: w221 ready -> claimed
    8c90978ead22e03c3e3186bbf18993c616c7c702 w221 work: w221 claimed -> awaiting-answer
    9f07640c1e31fd425b8ec720c651bc82f584990e none work answer: supervision
    c8ddc7997ceeabf2d6f0bdcb1838ac68b9291fd4 w221 work answer: w221 awaiting-answer -> ready
    d0ac8b33429b2f5b9ddb94aca035fa442694547c none work request: q33
    f19a7713c4e8942d72b3f61e465d8d0e717b6965 none spec: supervision r171 r172 replace r158 r160 (gate answers of the person, 2026-10-28: yes, r171 and r172 approved as drafted)
    a4907ef59b068c0f4ab7bee5b86cf488b7a03a71 none work note: i46
    84b299e5ced5fbb57ac041b721e8d120be89c198 none work: supervision awaiting-answer -> approved
    e41599205eb632abe6e659e8a66a394fe7a160c4 none features: supervision scenarios for r171 r172
    7c7dff7ceddd45cfdf988d44362426c4606d66c1 none work note: i46
    b117d954f4938ab81378fed301e3e6498d49595d none work: supervision approved -> formulated
    a931ff0be62fef4656d8250a0a36d1f266ade04a w222 work add: i46/w222 drafted
    358d6506ca1437990e76d8141cc28de79c466641 w221 work: w221 ready -> claimed
    a5565ffc7710d8522b1b3a10ff8a9d75e8b4c336 w221 work: w221 claimed -> awaiting-answer
    710b488dcc773884f82e3901bda235662144b141 w222 work: w222 drafted -> researched
    de75b7a2add368e8c73fa675838ed87beac0010e w222 work: w222 researched -> planned
    46ea66f390e271eef2e888447ba173031d3b5367 w222 work: w222 planned -> ready
    a299bea08319b0cbee875ee0d848f3322b8f9077 w222 work: w222 ready -> claimed
    5e232a9332e5f7e2f57d94daf92470c396a399cd w222 work: w222 claimed -> awaiting-answer
    7d0e08ca783c63f7ba5c206df242457ca615a4db none work: i46 supervision proposal's lists restored to what the gate approved (ledger 2026-10-28); the redraft for r171 r172 had replaced them (r114)
    d5b60f8b4395dc97f4131bec80962bb4d341dfd2 w223 work add: i46/w223 drafted
    31ada2b62cac87d0e914978fca643e347c8eba34 w224 work add: i46/w224 drafted
    13ded7360112a930753d85050cca7f8effe4cf5c w225 work add: i46/w225 drafted
    e3b914ccc4609d441f6ec1c1c2693b9876990b69 w221 work answer: w221 awaiting-answer -> ready
    e5a774f5cb5046b171668efbb7ee2cd48dbf5111 w222 work answer: w222 awaiting-answer -> ready
    ab75500f3946e61dbe4d97e66b8cdc40d2543504 none work request: q34
    af9394b59ca30f7dce01614dff7b03fbe1f42169 none work note: i46
    5ae2e173eef72b987282c6175dfc7e3694e60f62 w221 work: w221 ready -> claimed
    b7f62e4ecfe8102dd76747d00b6cb9aa244aea49 w222 work: w222 ready -> claimed
    df968241a9421f2a8db5bc7cb86a87a082573647 w221 design-model-check: glossary-proposal is a part kind; r122 terms, r123 approved closes, r124 shapes
    d44c6718cfe84b1d0f28ba8cc002d298c5f6bedd w221 work: w221 claimed -> done
    606654ee5daa4dc0dbddac51f0ee248cceab4cec w222 supervision r171, r172: an integrate round's glossary entry is written as a drafted glossary-proposal
    74432fa66ae0722617dd1a58a450acc579c7501c w222 work: w222 claimed -> done
    727421cff040540a1cb58211e34223867d172cf4 w223 work: w223 drafted -> researched
    26961279be9811e06645e0c4f5c0b383ea8e70cf w224 work: w224 drafted -> researched
    04ab95f7737b041f5652d495491c6d5b2eae047e w224 work: w224 researched -> planned
    abbbc6487ee1cb0eb52e3dfe6325a9088d779a2a w224 work: w224 planned -> ready
    a693a239bae89f8bed1e0a672110a64511797e63 w222 work: w222 done -> awaiting-answer
    e4f508255a2a6b9d955326df4542d638a0d38ee5 w224 work: w224 ready -> claimed
    ff0a457f6728f2bebf6d648cc3d129a16d17b9ff w223 work: w223 researched -> planned
    7de13c9378b51d32fc15ecbd940bc23151f887d5 w223 work: w223 planned -> ready
    884532f513f35aead447dce31580f1e8de337b55 w223 work: w223 ready -> claimed
    32107b5f3b2e5b1eac8764e43a146e3ea345d481 w221 work: w221 done -> green
    77386a008f49e652f2171a94e2e3311c98e45f94 w225 work: w225 drafted -> researched
    87f216564bcc75e48e0bcc13bcecccd617195dc5 w224 Bind the r159 and r168 Thens: the term clause is optional
    7a20968042f9add7e383d821ce85770531f1288a w224 work: w224 claimed -> done
    7581837253f417aea16542d0a7a9952d3c367008 w223 A delegation leaves questions naming a glossary term or glossary-proposal for the person (r162, r163)
    08680274995f89544e2787ad7ee689154c226072 w223 work: w223 claimed -> done
    9eae4e05b3848ca4635012c1ab9af5be4e35e40f w225 work: w225 researched -> planned
    75948cd179322552582dce4db89fc43eb1ab8702 w225 work: w225 planned -> ready
    e786ad996f9fb1623f51e88936d6420df8d4b7c1 w225 work: w225 ready -> claimed
    d2dc7a39a898e2dcceb6b2d3518c7a21017a0c01 w224 work: w224 done -> green
    20af23d1798bcfbc98ff3257273b92f4220d4d6f w223 work: w223 done -> green
    966bce994c469130bc279b5886097082a7d1c1c2 w225 work: w225 claimed -> awaiting-answer
    7bf9820b0aa7ffa71522533ed3d4a05c3f247d0a w222 work answer: w222 awaiting-answer -> done
    7f7b3c3af816c3de32c8fd2aca3d2a83fd168046 w225 work answer: w225 awaiting-answer -> ready
    3d16dfe78c27e364f606b2397ee272cca4bc4ad8 none work request: q35
    509595ba8d3192a884af13310f7e92fd3f98a9f1 none work note: i46
    d5abde5f81be507f069972bf090ecea2868a0a14 w225 work: w225 ready -> claimed
    0f01102ec0dca8da1bf8584500de58a48605ed13 w225 work run: route a glossary-proposal through gate, apply and approved (r164 r165 r166 r167 r169 r170)
    52207c770e139c95c74100f2ec41a4f61cb7da9e w225 work run: an initiative that changes only the glossary is set done (r161)
    54e19c87dfc374123d2dcdda8b5b96d57ab5726b w225 work: w225 claimed -> done
    21a5376b48ddd414fe36a9e44954c6aa52ca9cca w222 work: w222 done -> green
    def7d99dc517c4cad7d666b0d9ba87cb3fc9d67a w225 work: w225 done -> awaiting-answer
    7c4350f9032b5c229e54370faaf5a5605bf28935 w225 work answer: w225 awaiting-answer -> done
    200b3cf1d1416b6feade679539946938d9ebd04a none work request: q36
    6a0efc39e8bedb607de21d634795247467082f7e none work note: i46
    39256f640e5be8cd0b4e6acd79df1f84529c9cdd w225 work: w225 done -> awaiting-answer
    f08d3a136738ca93b7259f1fe03efc73599920a9 w225 work answer: w225 awaiting-answer -> ready
    2b7e18825123e8291d73ff1137f49d140d5f4cdf none work note: i46
    760741c5e604d7cf326c16a9dac9e22385d43e3d w225 work: w225 ready -> claimed
    8322c119896e21c6c573ca391856187b713ea00f w225 work run: glossary-only done skips ledger.md (r161)
    e2ddbd5df8260459f79d6828b7df41a40d19105a w225 work: w225 claimed -> done
    753b97696f569a31dacee8d57a34cef441db791e w225 work: w225 done -> green
    da7397e5389da04533713526e49aa659101abd92 w226 work add: i46/w226 drafted
    42a42f4ab95df195d0ded1b6727c97aee6bedb6e w226 work: w226 drafted -> researched
    9cdae0c2578046f098416989df7324befdaff8fe w226 work: w226 researched -> planned
    fe4fb71e0d9ae2111e92356a3b8593261be161c6 w226 work: w226 planned -> ready
    990601f5233d218908113df49772a041ef7745f0 w226 work: w226 ready -> claimed
    93531c6a004bc0b2b91f57a957665803b98368e0 w226 Retire the deprecated scenarios of r77, r92 and r104 (w226)
    0f0c7d520d38eb99bd6232d38612efb33f4847c4 w226 work: w226 claimed -> done
    3779411dd590407e8e3f84075b2725716df68f69 w226 work: w226 done -> green

## Change

The change from 134745663cfa0a109b8564370c2464ef9ee9a7d5 to 3779411dd590407e8e3f84075b2725716df68f69, without the workflow's own files:

    diff --git a/CLAUDE.md b/CLAUDE.md
    index a0c98f31..63a04be9 100644
    --- a/CLAUDE.md
    +++ b/CLAUDE.md
    @@ -31,9 +31,10 @@ Code and test files, every tracked Python file, stay at 300 lines or fewer. `pyt
     | `scripts/supervise_outputs.py` | `work run`'s reading of what a stage's result must give (its output) and the question naming it when missing (r131, r132) |
     | `scripts/supervise_branch_runs.py` | `work run`'s runs before a branch review (the suite, scenarios, checks, `tools`, `features`) and their text in the reviewer's brief (r154, r155) |
     | `scripts/supervise_review_read.py` | what `work run` gives a branch review to read: its commits with their work-items, the change less `.shop/`, the files to read (r156, r157) |
    -| `scripts/supervise_change.py` | `work run`'s reading of an integrate round's change list and its writing of one drafted capability-proposal for each capability it names |
    +| `scripts/supervise_change.py` | `work run`'s reading of an integrate round's change list and its writing of one drafted capability-proposal for each capability it names and of one drafted glossary-proposal for its glossary entries |
     | `scripts/supervise_all.py` | `work run` with no initiative: every open initiative taken side by side, one `Run` each, and the exit on their statuses |
     | `scripts/supervise_answers.py` | `work run`'s answers under a request's delegation: a session for each question, the answer naming the delegation |
    +| `scripts/supervise_glossary.py` | `work run`'s reading of an initiative's glossary-proposals: the terms of those not approved, withheld from an apply round (spec-integration r55), and the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162) |
     | `scripts/supervise_drafts.py` | `work run`'s reading of the requirement ids other initiatives' kept drafts add, given to an integrate round |
     | `scripts/supervise_analysis.py` | `work run`'s measure of a finished initiative (`measure initiative`) and the analysis session that follows it |
     | `scripts/supervise_done.py` | `work run`'s done: an initiative whose delivery is closed set `done` and committed |
    diff --git a/agents/initiative-round.md b/agents/initiative-round.md
    index e489c702..c3aeebe7 100644
    --- a/agents/initiative-round.md
    +++ b/agents/initiative-round.md
    @@ -25,14 +25,14 @@ You run one round of spec work, started by `work run`, in a context that ends wi
     Your input prompt gives `Scripts:`, the kind (`Kind:`), the drafts path and the round's number. The drafts path is under `.shop/scratch/drafts/`, which git ignores; nothing of yours is written outside it but what your kind commits.
     
     - **`integrate`**: the note's path, or from round 2 the person's answers in their words; in any round, the answers your brief gives. Lines an answer asks for beyond the request's accepted lines are drafted under the capabilities the answer names (a new capability included), each quoting the answer it comes from; such a line is kept, not removed for lacking a note quote. Do integrating-a-proposal's steps 1 and 2: dispatch the writer with the template (the question template from round 2), verify the porcelain, verify the change list in both directions, send back to the writer what fails. When your brief lists requirement ids other initiatives' drafts add (its "Ids drafted elsewhere"; from round 2 on, the ids in this round's own brief), give them to the writer in the dispatch, and check that every id in the change list's `adds` is above every listed id on the same capability (listed ids on other capabilities and `term/` ids do not count; a listed id already in `spec/` is covered by numbering above the highest); send back drafts where one is not. A brief that lists none leaves the numbering as it was. Write the gate's text to `<drafts path>/round-<n>/gate.md`: every added, changed and removed Behaviour line in full, with its id, under its capability, a changed line with what it was, every added, changed and removed glossary entry in full with its `term/<term>` id, a changed entry with what it was, every drafted decision as its file path, summary, `source` ids and `by`, and every question with its readings and the line each answer would give.
    -  When a brief from `work run` gives `Drafts path:`, that is your drafts path, in place of the one under `.shop/scratch/drafts/`: `work run` keeps it with the round's stage directory whatever the round ends with. Give the change list in your result's `changes`, in the form your brief names: one entry for each capability, with its `adds`, `changes` and `removes` as ids (`<capability>#r<n>`, `term/<term>`). A DONE with no change list is an error to `work run`.
    +  When a brief from `work run` gives `Drafts path:`, that is your drafts path, in place of the one under `.shop/scratch/drafts/`: `work run` keeps it with the round's stage directory whatever the round ends with. Give the change list in your result's `changes`, in the form your brief names: one entry for each capability, with its `adds`, `changes` and `removes` as ids (`<capability>#r<n>`), and one entry for the glossary, `{"glossary": true, ...}`, with the terms you add, change or remove as `term/<term>` ids; a term goes in the glossary's entry and in no capability's. A DONE with no change list is an error to `work run`.
       Where your brief names an upstream (its "Upstream:" lines, each with the path of that upstream's published spec), a line you draft that needs what that upstream does not yet give leads to the lines of a request into it: read its published spec, word the lines in its glossary's terms and in the strict form, and give them in your result's `requests` beside `changes`, in the form your brief names. Write nothing into the upstream.
       When your brief names a capability-proposal and gives its questions with their answers, the initiative's ledger and an earlier drafts path to read only, you draft that proposal anew from its answers: your change list rewrites that proposal, one entry for its capability, and the earlier drafts stay where they are.
       Reply: the text of `gate.md` as it is, then one line with the number of cut sentences and the path. Nothing else.
     - **`gate`**: the rounds' drafts and any reports to show; read each round's `gate.md` where it was written. Give in your result `questions`, a list of strings, one question for each decision the person is asked to make. A question names the decision, gives the lines it concerns in full (with their ids, and for a changed line what it was), lists the readings, and marks the recommended reading. Write no card files; `work run` writes the questions on the capability-proposal.
       Reply: the number of questions. Nothing else.
     - **`apply`**: the rounds to apply and the approval, in the person's words or as the file of their answers. Apply exactly the drafts the person approved. Do step 4, `model check` included: drafts applied round by round, decision files copied into `spec/decisions/` and `scripts/model decisions` run, `spec/` (the decision files and the regenerated `spec/decisions/index.md` with it) committed alone with the approval in the message, any delegation it was given under in the decision's `by`.
    -  Give in your result's `changes` the change list of what you applied after the answers, in the form your brief names: one entry for each capability you applied, with its `adds`, `changes` and `removes` as ids, the ids as they stand in `spec/` after the apply (a renumbered id under its new number, a dropped one left out). `work run` writes the proposal's lists from it.
    +  Give in your result's `changes` the change list of what you applied after the answers, in the form your brief names: one entry for each capability you applied, with its `adds`, `changes` and `removes` as ids, the ids as they stand in `spec/` after the apply (a renumbered id under its new number, a dropped one left out). Apply none of the terms your brief says the person has not approved to `spec/index.md`, also where the drafts hold them. `work run` writes the proposal's lists from it.
       After applying, compare each answer your brief gives with the drafts you applied and give in your result `unheld_answers` each answer the applied drafts do not hold, as a list of the answers' texts, beside `changes` when you applied some drafts and beside `nothing_applied` when you applied none; an answer the drafts hold is left out. `work run` keeps the result as you give it.
       When the person's answers ask for what the drafts never held, so that you apply nothing, give in your result `nothing_applied`, a sentence saying that the proposal's answers give what its drafts do not hold, and no `changes` and no `questions`: `work run` then starts an integrate round for the proposal.
       Reply: the commit, the capability paths changed, the decision files added, the change list's path, and `model check`'s last line. Under eight lines.
    diff --git a/features/design-model-check.feature b/features/design-model-check.feature
    index a324ede3..4bcf825a 100644
    --- a/features/design-model-check.feature
    +++ b/features/design-model-check.feature
    @@ -220,6 +220,30 @@ Feature: Design model check
           | formulated | removes | shelf | not printed as unresolved |
           | merged    | adds    | shelf | printed as unresolved     |
     
    +  @r122
    +  Scenario Outline: a glossary-proposal's list naming a term the glossary lacks is unresolved, unless an approved glossary-proposal removes it
    +    Pins that term/<term> in a glossary-proposal's list is read against the glossary, and that a term an approved glossary-proposal removes is excused wherever a glossary-proposal names it, a drafted one included.
    +    Given a glossary with the term store
    +    And <remover>
    +    And a <status> glossary-proposal whose <list> names term/<term>
    +    When `model check` is run
    +    Then term/<term> is <printed>
    +
    +    Examples:
    +      | remover                                                             | status   | list    | term  | printed                   |
    +      | no other glossary-proposal                                          | drafted  | adds    | store | not printed as unresolved |
    +      | no other glossary-proposal                                          | drafted  | changes | store | not printed as unresolved |
    +      | no other glossary-proposal                                          | drafted  | adds    | shelf | printed as unresolved     |
    +      | no other glossary-proposal                                          | drafted  | changes | shelf | printed as unresolved     |
    +      | no other glossary-proposal                                          | drafted  | removes | shelf | printed as unresolved     |
    +      | an approved glossary-proposal whose removes names term/shelf        | drafted  | adds    | shelf | not printed as unresolved |
    +      | an approved glossary-proposal whose removes names term/shelf        | drafted  | changes | shelf | not printed as unresolved |
    +      | an approved glossary-proposal whose removes names term/shelf        | drafted  | removes | shelf | not printed as unresolved |
    +      | no other glossary-proposal                                          | approved | removes | shelf | not printed as unresolved |
    +      | no other glossary-proposal                                          | approved | adds    | shelf | printed as unresolved     |
    +      | an awaiting-answer glossary-proposal whose removes names term/shelf | drafted  | adds    | shelf | printed as unresolved     |
    +      | a withdrawn glossary-proposal whose removes names term/shelf        | drafted  | adds    | shelf | printed as unresolved     |
    +
       @r24
       Scenario Outline: a frontmatter reference to nothing, or to the wrong kind, is unresolved
         Pins that each named frontmatter reference must reach a node, and that supersedes, under, for, blocked_by and depends_on must reach a node of the kind they need.
    @@ -287,60 +311,41 @@ Feature: Design model check
           | features/thing.feature     | a scenario with its own title is tagged @holding                           | prints          |
           | features/thing.feature     | a scenario is tagged @deprecated and @holding                              | prints          |
     
    -  @r27
    -  Scenario Outline: a malformed work directory or work file is a file problem
    -    Pins the shape each initiative and part file must have, and that a missing initiative.md is charged to its directory.
    -    Given a repository with a work directory .shop/work/i1 in which <case>
    -    When `model check` is run
    -    Then it prints a file problem naming <named>
    -
    -    Examples:
    -      | case                                                                 | named                                              |
    -      | there is no initiative.md                                            | .shop/work/i1, and not .shop/work/i1/initiative.md |
    -      | initiative.md has no id                                              | .shop/work/i1/initiative.md                        |
    -      | the part p1.md has no id                                             | .shop/work/i1/p1.md                                |
    -      | the part p1.md has the kind banana                                   | .shop/work/i1/p1.md                                |
    -      | the part p1.md has no status                                         | .shop/work/i1/p1.md                                |
    -      | the part p1.md has a status not in its kind's lifecycle              | .shop/work/i1/p1.md                                |
    -      | the part p1.md has the kind capability-proposal and the status built | .shop/work/i1/p1.md                                |
    -      | initiative.md has the priority high                                  | .shop/work/i1/initiative.md                        |
    -      | initiative.md has a date written 16/10/2026                          | .shop/work/i1/initiative.md                        |
    -
    -  @r27
    -  Scenario: a work-item accepting a requirement no scenario names is a file problem
    -    Pins that a work-item may accept only requirements a scenario already names.
    -    Given a capability thing with requirement r2 that no scenario names
    -    And a work-item in .shop/work/i1/w1.md that accepts thing#r2
    -    When `model check` is run
    -    Then it prints a file problem naming .shop/work/i1/w1.md
    -
    -  @r27
    -  Scenario: a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem
    -    Pins that a guarantees capability's requirements, which no scenario names, may be accepted by a work-item.
    -    Given a capability thing in the guarantees group with requirement r2 that no scenario names
    -    And a work-item in .shop/work/i1/w1.md that accepts thing#r2
    -    When `model check` is run
    -    Then it prints no file problem naming .shop/work/i1/w1.md
    -
    -  @r27
    -  Scenario: a green work-item accepting a retired id is no file problem
    -    Pins that a retired id is left out of what a scenario must name for a work-item to accept it, once that work-item is green.
    -    Given a capability thing whose frontmatter lists r2 as retired
    -    And a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2
    +  @r123
    +  Scenario: an initiative may be `done` when its glossary-proposal is approved
    +    Pins that approved is a closed status for a glossary-proposal under a `done` initiative.
    +    Given a capability-change initiative with status `done`
    +    And under it a glossary-proposal with status approved
         When `model check` is run
    -    Then it prints no file problem naming .shop/work/i1/w1.md
    +    Then no violation names the initiative
     
    -  @r27
    -  Scenario Outline: a status in its kind's lifecycle is no file problem
    -    Pins that each status the glossary gives a kind is in that kind's lifecycle, awaiting-answer a capability-proposal's and withdrawn a request's.
    -    Given a repository in which <case>
    +  @r124
    +  Scenario Outline: a malformed work directory or work file is a file problem
    +    Pins the shape each initiative and part file must have, that a missing initiative.md is charged to its directory, that a glossary-proposal is a part, and which requirements a work-item may accept before a scenario names them.
    +    Given a repository with a work directory .shop/work/i1 in which <case>
         When `model check` is run
    -    Then it prints no file problem naming <file>
    +    Then it <prints> a file problem naming <named>
     
         Examples:
    -      | case                                                                                                       | file                      |
    -      | a work directory .shop/work/i1 has the part p1.md with the kind capability-proposal and the status awaiting-answer | .shop/work/i1/p1.md       |
    -      | a request in .shop/work/requests/q1.md, of the form `work request` writes, has the status withdrawn        | .shop/work/requests/q1.md |
    +      | case                                                                                                         | prints         | named                                              |
    +      | there is no initiative.md                                                                                    | prints         | .shop/work/i1, and not .shop/work/i1/initiative.md |
    +      | initiative.md has no id                                                                                      | prints         | .shop/work/i1/initiative.md                        |
    +      | initiative.md has no status                                                                                  | prints         | .shop/work/i1/initiative.md                        |
    +      | initiative.md has the priority high                                                                          | prints         | .shop/work/i1/initiative.md                        |
    +      | initiative.md has a date written 16/10/2026                                                                  | prints         | .shop/work/i1/initiative.md                        |
    +      | the part p1.md has no id                                                                                     | prints         | .shop/work/i1/p1.md                                |
    +      | the part p1.md has the kind banana                                                                           | prints         | .shop/work/i1/p1.md                                |
    +      | the part p1.md has the kind glossary-proposal and the status drafted                                         | does not print | .shop/work/i1/p1.md                                |
    +      | the part p1.md has no status                                                                                 | prints         | .shop/work/i1/p1.md                                |
    +      | the part p1.md has the kind capability-proposal and the status built                                         | prints         | .shop/work/i1/p1.md                                |
    +      | the part p1.md has the kind capability-proposal and the status awaiting-answer                               | does not print | .shop/work/i1/p1.md                                |
    +      | the part p1.md has the kind glossary-proposal and the status formulated                                      | prints         | .shop/work/i1/p1.md                                |
    +      | the part p1.md has the kind glossary-proposal and the status approved                                        | does not print | .shop/work/i1/p1.md                                |
    +      | the work-item w1.md with status drafted accepts thing#r2, which no scenario names                            | prints         | .shop/work/i1/w1.md                                |
    +      | the work-item w1.md with status withdrawn accepts thing#r2, which no scenario names                          | does not print | .shop/work/i1/w1.md                                |
    +      | the work-item w1.md with status drafted accepts thing#r2, of a guarantees capability thing, which no scenario names | does not print | .shop/work/i1/w1.md                         |
    +      | the work-item w1.md with status green accepts thing#r2, which capability thing lists as retired              | does not print | .shop/work/i1/w1.md                                |
    +      | the work-item w1.md with status done accepts thing#r2, which capability thing lists as retired               | prints         | .shop/work/i1/w1.md                                |
     
       @r110
       Scenario Outline: a work-item not named w<n>.md, or two work-items with one id, is a file problem
    diff --git a/features/spec-integration.feature b/features/spec-integration.feature
    index b2ca94e0..6aa5600c 100644
    --- a/features/spec-integration.feature
    +++ b/features/spec-integration.feature
    @@ -34,3 +34,27 @@ Feature: Spec integration
         Then the round applies those drafts
         And the round's result gives the answer that the customer is told when an order ships
         And the round's result does not give the answer that the customer sees the status of an order
    +
    +  @r54
    +  Scenario: a round of the kind integrate that drafts a change to the glossary gives the terms it adds, changes and removes in the change list's entry for the glossary and in no entry for a capability
    +    Pins that the person at the gate finds every term a round drafts in the one place the glossary's change is listed, and never mixed into the lines listed for a capability.
    +    Given spec/index.md's glossary has the terms order and basket
    +    And an approved note asks that the customer sees the refund of a cancelled order
    +    And that note adds the term refund, changes the term order and removes the term basket
    +    When work run starts a round of the kind integrate on that note
    +    Then the round drafts a line under the capability refunds that the customer sees the refund of a cancelled order
    +    And the round drafts a change to the glossary
    +    And the change list's entry for the glossary gives refund as added, order as changed and basket as removed
    +    And the change list's entry for refunds gives none of the terms refund, order and basket
    +
    +  @r55
    +  Scenario: while the person has not approved the terms of a glossary-proposal, no round applies any of them to spec/index.md
    +    Pins that a term reaches the glossary only through the gate: a glossary-proposal the person has not approved leaves spec/index.md as it was, even while a round applies other drafts of the same initiative.
    +    Given spec/index.md's glossary has the term order and no term refund
    +    And an initiative with a glossary-proposal that adds the term refund and changes the term order
    +    And the person has not approved the terms of that glossary-proposal
    +    And a capability-proposal of that initiative the person has approved
    +    When work run starts a round of the kind apply on that capability-proposal
    +    Then the round applies the capability-proposal's drafts
    +    And spec/index.md's glossary has no term refund
    +    And spec/index.md's glossary has the term order as it was before the round
    diff --git a/features/supervision.feature b/features/supervision.feature
    index 1d1faca2..c5ec0ff3 100644
    --- a/features/supervision.feature
    +++ b/features/supervision.feature
    @@ -1298,10 +1298,25 @@ Feature: Supervision
         When the person runs `work run i1`
         Then a session of analyzing-a-batch was started for i1 once `measure initiative` had written i1's measurement
         And i1's analysis record is not there
    -  @r77
    -  Scenario Outline: under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply>
    +  @r77 @deprecated
    +  Scenario: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated)
    +    Deprecated for: removal
    +    Pins that two questions of one work-item are answered apart, in one `work run`, and that the run keeps every answer its sessions gave instead of losing one to the other.
    +    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    +    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and "Is a title given twice in features/books.feature one book or two?", each with no answer
    +    And the session given "Does scripts/log.py own the log?" under the delegation answers "Yes.", the session given "Is a title given twice in features/books.feature one book or two?" answers "One book.", and every round ends and every worker gives DONE
    +    When the person runs `work run i1`
    +    Then "Does scripts/log.py own the log?" was given to a session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", scripts/log.py, and nothing else
    +    And "Is a title given twice in features/books.feature one book or two?" was given to another session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", features/books.feature, and nothing else
    +    And w1's answer to "Does scripts/log.py own the log?" is "Yes.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    +    And w1's answer to "Is a title given twice in features/books.feature one book or two?" is "One book.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    +    And it exits successfully
    +
    +  @r163
    +  Scenario Outline: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply>
         Pins that a question is weighed against the person's words alone, apart from every other question, and answered only when those words cover it.
    -    Given i1 fulfils the request q1, which gives the delegation "<delegation>"
    +    Given spec/index.md's Glossary holds the term "ledger"
    +    And i1 fulfils the request q1, which gives the delegation "<delegation>"
         And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py or scripts/queue.py own the log?" and no answer
         And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice in features/books.feature one book or two?" and no answer
         And each session given a question under the delegation <reply>, and every round ends and every worker gives DONE
    @@ -1311,22 +1326,27 @@ Feature: Supervision
         And <after>
     
         Examples:
    -      | delegation                                                                       | reply                                   | after                                                                     |
    -      | Please get everything delivered. Do not stop to ask me questions or permission. | answers it                              | w1's question and p1's question each have the session's answer            |
    -      | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person                | w1's question and p1's question have no answer, w1 and p1 awaiting-answer |
    +      | delegation                                                                       | reply                    | after                                                                     |
    +      | Please get everything delivered. Do not stop to ask me questions or permission. | answers it               | w1's question and p1's question each have the session's answer            |
    +      | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person | w1's question and p1's question have no answer, w1 and p1 awaiting-answer |
    +
    +  @r162
    +  Scenario Outline: under a delegation, a question of the initiative that names <named> is left for the person and given to no session
    +    Pins that a question touching the glossary is the person's to answer, whatever the delegation's words allow.
    +    Given spec/index.md's Glossary holds the term "ledger"
    +    And i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    +    And i1's glossary-proposal g1 is awaiting-answer
    +    And i1's work-item w1 is awaiting-answer, its ## Questions section with "<question>" and no answer
    +    And each session given a question under the delegation answers it, and every round ends and every worker gives DONE
    +    When the person runs `work run i1`
    +    Then "<question>" was given to no session
    +    And w1's question "<question>" has no answer
    +    And w1 is awaiting-answer
     
    -  @r77
    -  Scenario: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends
    -    Pins that two questions of one work-item are answered apart, in one `work run`, and that the run keeps every answer its sessions gave instead of losing one to the other.
    -    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    -    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and "Is a title given twice in features/books.feature one book or two?", each with no answer
    -    And the session given "Does scripts/log.py own the log?" under the delegation answers "Yes.", the session given "Is a title given twice in features/books.feature one book or two?" answers "One book.", and every round ends and every worker gives DONE
    -    When the person runs `work run i1`
    -    Then "Does scripts/log.py own the log?" was given to a session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", scripts/log.py, and nothing else
    -    And "Is a title given twice in features/books.feature one book or two?" was given to another session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", features/books.feature, and nothing else
    -    And w1's answer to "Does scripts/log.py own the log?" is "Yes.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    -    And w1's answer to "Is a title given twice in features/books.feature one book or two?" is "One book.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    -    And it exits successfully
    +    Examples:
    +      | named                         | question                                       |
    +      | the term "ledger"             | Does scripts/log.py write the ledger?          |
    +      | the glossary-proposal g1      | Does scripts/log.py wait for g1 to be applied? |
     
       @r78
       Scenario: an answer given by a session started under a delegation is written naming that delegation
    @@ -1433,17 +1453,9 @@ Feature: Supervision
           | gives DONE with a change list naming thing |
           | ends at its turn limit                |
     
    -  @r92
    -  Scenario: an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability
    -    Pins that the change list is split by capability, each proposal holding that capability's requirement ids and terms and nothing of another's.
    -    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    -    And the integrate round for i1 gives DONE with a change list that adds thing#r4 and the term "ledger", changes thing#r2 and removes thing#r3 on thing, and adds other#r1 on other
    -    And every other round ends
    -    When the person runs `work run i1`
    -    Then the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3, and one for other, its adds naming other#r1 and its changes and removes naming nothing
    -
    -  @r92
    -  Scenario: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids
    +  @r92 @deprecated
    +  Scenario: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated)
    +    Deprecated for: removal
         Pins that two initiatives changing one capability each get a capability-proposal of their own, never two proposals sharing one id.
         Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
         And an initiative i2 under .shop/work/, proposed, that fulfils the request q2, whose line 1 has the line outcome accepted
    @@ -1463,6 +1475,26 @@ Feature: Supervision
         Then `work request` was run for the upstream catalogue, with the line "When a book is listed, the catalogue shall give its edition." as its one line
         And the request it wrote in catalogue is raised for q1 and gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
     
    +  @r159
    +  Scenario: an integrate round that ends with a change list gives one drafted capability-proposal for each capability it names, with the requirement ids it adds, changes and removes on that capability
    +    Pins that the change list is split by capability, each proposal holding that capability's requirement ids and nothing of another's.
    +    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    +    And the integrate round for i1 gives DONE with a change list that adds thing#r4, changes thing#r2 and removes thing#r3 on thing, and adds other#r1 on other
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming thing#r4, its changes thing#r2 and its removes thing#r3, and one for other, its adds naming other#r1 and its changes and removes naming nothing
    +
    +  @r171
    +  Scenario: an integrate round that ends with a change list naming the glossary gives a drafted glossary-proposal with the terms it adds, changes and removes in the glossary
    +    Pins that the terms an integration proposes for the glossary come to the gate as a glossary-proposal, holding each term the change list adds, changes or removes there.
    +    Given spec/index.md's Glossary holds the terms "shelf", "loan" and "reader"
    +    And i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
    +    And the integrate round for i1 gives DONE with a change list that adds the term "ledger", changes the term "shelf" and removes the term "loan" in the glossary
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then the commit that wrote i1's glossary-proposal wrote one, drafted, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    +    And it names the term "reader" in none of its adds, changes and removes
    +
       @r68
       Scenario: a drafted capability-proposal is given to a gate round whose brief asks for the gate as questions, each a decision with its readings and the recommended reading marked
         Pins that the gate comes back as decisions the person can answer one by one, with the reading to take already marked.
    @@ -1643,17 +1675,6 @@ Feature: Supervision
         Then a round of the kind integrate was started for i1, given thing#r4 and other#r1
         And the integrate round for i1 was not given thing#r1, thing#r2 or thing#r5
     
    -  @r104
    -  Scenario: the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes
    -    Pins that the gate of one capability-proposal raises no question on what another proposal, or the rest of the capability, holds.
    -    Given the capability thing holds thing#r1, thing#r2 and thing#r3
    -    And i1's capability-proposal p1 is drafted, its adds naming thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3
    -    And i1's capability-proposal p2 is drafted, its adds naming other#r1
    -    And every round ends
    -    When the person runs `work run i1`
    -    Then the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2, thing#r3 and the term "ledger"
    -    And it asks for no question on thing#r1 or on other#r1
    -
       @r107
       Scenario: a change list naming a capability that neither spec/capabilities/ nor the round's drafts have gives no capability-proposal for it, and `work run` exits with an error naming it
         Pins that a change list cannot bring a proposal for a capability that exists nowhere, and that the person learns which capability it named.
    @@ -1681,6 +1702,86 @@ Feature: Supervision
           | gate  | drafted                                                                                                                  |
           | apply | awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", and its Answers section with "One book." |
     
    +  @r164
    +  Scenario: a drafted glossary-proposal is given to a gate round asked only for the questions on the terms it adds, changes or removes
    +    Pins that the gate of a glossary-proposal raises no question on a term of the glossary the proposal leaves as it is.
    +    Given spec/index.md's Glossary holds the terms "shelf", "loan" and "reader"
    +    And i1's glossary-proposal g1 is drafted, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    +    And every round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind gate was started for g1
    +    And the brief of the gate round for g1 asks only for the questions on the terms "ledger", "shelf" and "loan"
    +    And it asks for no question on the term "reader"
    +
    +  @r168
    +  Scenario: the gate round of a capability-proposal is asked only for the questions on the lines that proposal adds, changes or removes
    +    Pins that the gate of one capability-proposal raises no question on what another proposal, or the rest of the capability, holds.
    +    Given the capability thing holds thing#r1, thing#r2 and thing#r3
    +    And i1's capability-proposal p1 is drafted, its adds naming thing#r4, its changes thing#r2 and its removes thing#r3
    +    And i1's capability-proposal p2 is drafted, its adds naming other#r1
    +    And every round ends
    +    When the person runs `work run i1`
    +    Then the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2 and thing#r3
    +    And it asks for no question on thing#r1 or on other#r1
    +
    +  @r170
    +  Scenario Outline: the <kind> round of a glossary-proposal is given the path of the kept drafts of the integrate round that wrote the proposal
    +    Pins that the round weighing or applying a glossary-proposal reads the drafts the proposal came from, without anyone pointing it to them by hand.
    +    Given i1's glossary-proposal g1 is <status>
    +    And g1 was written from the change list of i1's integrate round, whose drafts are kept at .shop/work/i1/runs/i1/2-integrate/drafts/round-1/
    +    And every round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind <kind> was started for g1
    +    And the <kind> round for g1 was given the path .shop/work/i1/runs/i1/2-integrate/drafts/round-1/
    +
    +    Examples:
    +      | kind  | status                                                                                                                    |
    +      | gate  | drafted                                                                                                                   |
    +      | apply | awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", and its Answers section with "One file." |
    +
    +  @r169
    +  Scenario: when the gate round `work run` started for a glossary-proposal ends, the proposal is awaiting-answer
    +    Pins that a glossary-proposal whose gate has been given waits on its answers.
    +    Given i1's glossary-proposal g1 is drafted
    +    And the gate round gives the question "Is a ledger one file or one line an event?" on g1, and every round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind gate was started for g1
    +    And g1 is awaiting-answer
    +
    +  @r165
    +  Scenario: a glossary-proposal whose every question from its gate round has an answer is given to an apply round with its answers
    +    Pins that the person's answers on a glossary-proposal reach the round that applies them, without anyone starting it by hand.
    +    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?" and "Is the term shelf kept?", given by its gate round, and its Answers section with "One file." and "No."
    +    And every round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind apply was started for g1, given the answers "One file." and "No."
    +
    +  @r172
    +  Scenario: a glossary-proposal awaiting-answer with a question from its gate round that has no answer is given to no apply round
    +    Pins that the terms of a glossary-proposal are not applied while any question its gate raised on them waits on the person, even when the other questions have answers.
    +    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?" and "Is the term shelf kept?", given by its gate round, and its Answers section with "One file." only
    +    And every round ends
    +    When the person runs `work run i1`
    +    Then no round of the kind apply was started for g1
    +
    +  @r166
    +  Scenario: when the apply round `work run` started for a glossary-proposal ends having applied its drafts, the proposal is approved
    +    Pins that a glossary-proposal whose drafts have been applied after its answers is approved.
    +    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", given by its gate round, and its Answers section with "One file."
    +    And the apply round for g1 applies g1's drafts and gives DONE with a change list that adds the term "ledger" in the glossary
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then g1's transition to approved was made once the apply round had ended
    +
    +  @r167
    +  Scenario: when the apply round `work run` started for a glossary-proposal ends having applied its drafts, no formulate round is started for the proposal
    +    Pins that applied glossary terms are not taken to a formulation, which has no Behaviour line of theirs to formulate.
    +    Given i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", given by its gate round, and its Answers section with "One file."
    +    And the apply round for g1 applies g1's drafts and gives DONE with a change list that adds the term "ledger" in the glossary
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then no round of the kind formulate was started for g1
    +
       @r106
       Scenario: once the initiative's measurement and analysis record are written, they are committed on the initiative branch
         Pins that what was measured and analysed of an initiative is in the initiative's history, not left uncommitted in the checkout.
    @@ -1705,6 +1806,14 @@ Feature: Supervision
           | w1 is green and w2 is withdrawn     | is set done     | is done     |
           | w1 is withdrawn and w2 is withdrawn | is not set done | is not done |
     
    +  @r161
    +  Scenario: an initiative that changes only the glossary, its glossary-proposal approved and its terms committed to spec/index.md, is set done
    +    Pins that an initiative with no Behaviour line to deliver is done once its terms are in the glossary, without a work-item, a branch review or a measurement.
    +    Given i1 is started, has neither a capability-proposal nor a work-item, and its glossary-proposal g1 is approved, its adds naming the term "ledger"
    +    And spec/index.md's Glossary holds the term "ledger", committed on the initiative branch
    +    When the person runs `work run i1`
    +    Then i1 is done
    +
       @r109
       Scenario: an initiative set done is committed on the initiative branch
         Pins that the initiative's being done is in its history, not only in the checkout.
    diff --git a/scripts/model.lp b/scripts/model.lp
    index e547e38b..e9308c63 100644
    --- a/scripts/model.lp
    +++ b/scripts/model.lp
    @@ -56,6 +56,8 @@ root(P, I)            :- part_of(P, P2), root(P2, I).
     % `merged`. Read with the lifecycle: a capability-proposal is closed at `formulated`, any other part as listed.
     closed(P)             :- status(P, S), S = ("merged"; "built"; "delivered"; "ruled"; "green"; "refused"), not node(P, "capability-proposal").
     closed(P)             :- status(P, "formulated").
    +% design-model-check r123: `approved` closes a glossary-proposal, and no other kind.
    +closed(P)             :- status(P, "approved"), node(P, "glossary-proposal").
     % EXTENSION (proposed against grammar.md v3; design-model-check r58): a part no longer pursued is
     % `withdrawn`, and is closed.
     closed(P)             :- status(P, "withdrawn").
    @@ -194,7 +196,7 @@ v_k1(I) :- ikind(I, "job"),               part_of(P, I), not node(P, "job-propos
     label("v_k2", "a job-path initiative's first part is not a job-thread").
     v_k2(I) :- ikind(I, "job-path"),          part_of(P, I), not node(P, "job-thread").
     label("v_k3", "a capability-change initiative's first part is not a capability-proposal").
    -v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), not node(P, "capability-proposal").
    +v_k3(I) :- ikind(I, "capability-change"), part_of(P, I), not node(P, "capability-proposal"), not node(P, "glossary-proposal").   % r123: a glossary-proposal is a part of one
     label("v_k4", "a defect initiative's first part is not a work-item").
     v_k4(I) :- ikind(I, "defect"),            part_of(P, I), not node(P, "work-item").
     % FIX g:171 (design-decision/one-capability-per-proposal): a capability-change initiative may have several
    diff --git a/scripts/model_work.py b/scripts/model_work.py
    index 376c76c7..96f19d06 100644
    --- a/scripts/model_work.py
    +++ b/scripts/model_work.py
    @@ -11,11 +11,12 @@ STATUSES = {
         "capability-proposal": {"drafted", "approved", "merged", "formulated", "withdrawn", "awaiting-answer"},   # withdrawn: EXTENSION (r58)
         "work-item": {"drafted", "researched", "planned", "ready", "claimed", "done", "green", "awaiting-answer", "failed",
                       "withdrawn"},   # withdrawn: EXTENSION (r58); failed: design-decision/a-failed-work-item
    +    "glossary-proposal": {"drafted", "awaiting-answer", "approved", "withdrawn"},   # the glossary's term `status` (r124)
         "request": {"open", "awaiting-asker", "awaiting-upstream", "accepted", "refused", "delivered", "withdrawn"},
     }
     SETTLED = {"merged", "formulated", "withdrawn"}     # a capability-proposal that may name a retired id (r5, r23)
     PART_KINDS = {"job-proposal", "map-proposal", "vision-proposal", "job-thread", "capability-proposal",
    -              "cross-context-request", "map-escalation", "work-item"}
    +              "cross-context-request", "map-escalation", "work-item", "glossary-proposal"}
     RECORD_KINDS = {"observation", "measurement", "review-finding", "decision-argument", "initiative-archive"}
     WORK = Path(".shop") / "work"
     RECORDS = Path(".shop") / "records"
    @@ -89,7 +90,18 @@ class WorkReading:
             else:
                 held[ident] = where
     
    +    def judge_glossary_refs(self):
    +        """r122: a glossary-proposal's term the glossary lacks is unresolved, unless an approved glossary-proposal removes it."""
    +        for where, rel, t in self.glossary_refs:
    +            if self.nodes.get(t) != "term" and t not in self.glossary_removed:
    +                self.dangling.append(f"{where}: {rel} {t}, which the glossary does not have")
    +
         def read_work(self):
    +        self.glossary_refs, self.glossary_removed = [], set()
    +        self.read_initiatives()
    +        self.judge_glossary_refs()
    +
    +    def read_initiatives(self):
             held = {}
             for idir in sorted(p for p in (self.root / WORK).glob("*") if p.is_dir() and p.name != "requests"):
                 ipath = idir / "initiative.md"
    @@ -173,6 +185,15 @@ class WorkReading:
                             self.fact("req_id", q, cap, int(n))   # grammar.md's refusal table: v15c
                         elif rel != "changes":                     # changes: v15e reports it
                             self.dangling.append(f"{where}: {rel} {q}, which no capability has")
    +        if kind == "glossary-proposal":
    +            for rel in ("adds", "changes", "removes"):
    +                for ref in expand(as_list(data.get(rel))):
    +                    if str(ref).strip().startswith("term/"):
    +                        head, _, name = str(ref).strip().rpartition("/")
    +                        t = self.qualify(f"{head}/{name.lower()}")
    +                        self.glossary_refs.append((where, rel, t))
    +                        if rel == "removes" and data.get("status") == "approved":
    +                            self.glossary_removed.add(t)
             if kind == "work-item":
                 self.check_work_item_name(path, where, held, p)
                 if data.get("wkind"):
    diff --git a/scripts/supervise.py b/scripts/supervise.py
    index 6d728740..e4e8c6a6 100644
    --- a/scripts/supervise.py
    +++ b/scripts/supervise.py
    @@ -227,6 +227,8 @@ class Run(Workers, Briefs, Merge, Faults, Reviews, Pool, Drafts, Rounds, Analyse
                     if self.noted:     # r128: the node whose session faulted is printed with its fault, then the error
                         self.show()
                     raise refused
    +            if not self.items():
    +                self.set_glossary_done()     # r161
                 if self.items() and all(s in ("green", "withdrawn") for _, s in self.items()):     # r94, r97: none is not done
                     kept = self.branch_review()     # inside the try: its worktree goes with the run's (r33)
                     while kept is not None and self.fix_work_item(kept):     # r74: the fix is pulled
    diff --git a/scripts/supervise_answers.py b/scripts/supervise_answers.py
    index d9ded4d1..e30dd259 100644
    --- a/scripts/supervise_answers.py
    +++ b/scripts/supervise_answers.py
    @@ -1,11 +1,13 @@
     """`work run`'s answers under a delegation (capability supervision r77, r78): when the request an initiative fulfils gives
     a delegation, each open question of its awaiting-answer work-items and capability-proposals goes to a session of its own,
     given the question, the delegation and the files the question names, and nothing else. An answer the session gives is
    -written naming the delegation. Standard library only; a part of supervise.Run."""
    +written naming the delegation; a question naming a term of the glossary or a glossary-proposal goes to no session and is
    +left for the person (r162, r163). Standard library only; a part of supervise.Run."""
     import datetime
     import json
     import re
     
    +import supervise_glossary
     import workqueue
     import workqueue_answer
     import workqueue_request
    @@ -70,7 +72,7 @@ class Answers:
                 before = workqueue.agrees(self.root, self.initiative, name)
                 left = False
                 for question in self.open_questions(name):
    -                answer = self.ask(name, question, delegation)
    +                answer = None if supervise_glossary.names_one(self.root, question) else self.ask(name, question, delegation)
                     if answer is None or left:     # the n-th answer answers the n-th question: none is written after a gap
                         left = True
                         continue
    diff --git a/scripts/supervise_brief.py b/scripts/supervise_brief.py
    index dd4bef1b..621920f6 100644
    --- a/scripts/supervise_brief.py
    +++ b/scripts/supervise_brief.py
    @@ -4,13 +4,16 @@ import json
     import re
     
     import supervise_drafts
    +import supervise_glossary
     import workqueue
     import workqueue_request
     from supervise_worker import ROUNDS, SCRIPTS, git
     
     CHANGE_LIST = ("Give your change list in your result's `changes`: a list with one entry for each capability, each "
                    '`{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as '
    -               "`<capability>#r<n>` or `term/<term>`.")
    +               "`<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, "
    +               '`{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, '
    +               "and in no capability's entry.")
     REQUEST_LINES = ("Where a line you draft needs what an upstream above does not yet give, give the lines of a request into "
                      "that upstream in your result's `requests`: a list with one entry for each such upstream, each "
                      '`{"upstream": <its id>, "lines": [...]}`, the lines in strict form, worded in the terms of the '
    @@ -80,6 +83,7 @@ class Briefs:
                 if stage == "apply":     # r114: the list the round applied, which `work run` writes into the proposal
                     lines.append(CHANGE_LIST.replace("Give your change list", "Give the change list of what you applied"))
                     lines.append(UNHELD_ANSWERS)     # spec-integration r46
    +                lines += [supervise_glossary.text(self.dir, name)] if supervise_glossary.withheld(self.dir, name) else []     # r55, r165
                 if stage == "formulate":     # r149: the output of a formulation whose answers change lines outside spec/
                     lines.append(NOTHING_FORMULATED)
                 if stage in ("gate", "apply"):     # r108: the kept drafts of the integrate round that wrote the proposal
    diff --git a/scripts/supervise_change.py b/scripts/supervise_change.py
    index c46f64ad..e9d67217 100644
    --- a/scripts/supervise_change.py
    +++ b/scripts/supervise_change.py
    @@ -1,5 +1,6 @@
     """An integrate or apply round's change list (capability supervision r92, r96, r107, r114): read from the round's result, checked for its form,
    -and written as one `drafted` capability-proposal for each capability it names. Standard library only; a part of
    +and written as one `drafted` capability-proposal for each capability it names and, for its glossary entries, one `drafted`
    +glossary-proposal (r171). Standard library only; a part of
     supervise.Run."""
     import datetime
     import re
    @@ -23,13 +24,15 @@ def entries(data):
             raise BadChanges("its `changes` is not a list of entries")
         found = []
         for each in changes:
    -        if not isinstance(each, dict) or not isinstance(each.get("capability"), str) or not each["capability"].strip():
    +        glossary = isinstance(each, dict) and each.get("glossary") is True and "capability" not in each
    +        if not glossary and (not isinstance(each, dict) or not isinstance(each.get("capability"), str)
    +                             or not each["capability"].strip()):
                 raise BadChanges("an entry of its `changes` names no `capability`")
    -        one = {"capability": each["capability"].strip()}
    +        one = {"capability": None, "glossary": True} if glossary else {"capability": each["capability"].strip()}
             for field in FIELDS:
                 ids = each.get(field, [])
                 if not isinstance(ids, list) or not all(isinstance(i, str) and i.strip() for i in ids):
    -                raise BadChanges("the `%s` of its entry for %s is not a list of ids" % (field, one["capability"]))
    +                raise BadChanges("the `%s` of its entry for %s is not a list of ids" % (field, one["capability"] or "the glossary"))
                 one[field] = [i.strip() for i in ids]
             found.append(one)
         return found
    @@ -44,7 +47,7 @@ class Changes:
             the drafts of all of them count (an apply round's list)."""
             held = {p.stem for p in (self.root / "spec" / "capabilities").glob("*.md")}
             held |= {p.stem for p in stage.glob(("*/" if runs else "") + "drafts/round-*/spec/capabilities/*.md")}
    -        return [one["capability"] for one in found if one["capability"] not in held]
    +        return [one["capability"] for one in found if not one.get("glossary") and one["capability"] not in held]
     
         def kept_path(self, stage):
             """The integrate round's kept drafts directory with the highest round number, relative to the repository with a
    @@ -97,7 +100,7 @@ class Changes:
             ident = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("id:")), "")
             prefix = ident.split("/", 1)[1].rsplit("/", 1)[0] if "/" in ident else ""
             merged = {}
    -        for each in found:     # the entries that name one capability are one proposal's lists, in the order first named
    +        for each in (e for e in found if not e.get("glossary")):     # the entries that name one capability are one proposal's lists, in the order first named
                 one = merged.setdefault(each["capability"], {"capability": each["capability"], **{f: [] for f in FIELDS}})
                 for field in FIELDS:
                     one[field] += [i for i in each[field] if i not in one[field]]
    @@ -123,4 +126,15 @@ class Changes:
                                     prefix, self.dir.name, one["capability"], ident, one["capability"], lists,
                                     datetime.date.today().isoformat(), one["capability"], stage_dir))
                 written.append(path)
    +        terms = {f: [] for f in FIELDS}
    +        for each in (e for e in found if e.get("glossary")):     # r171: the glossary's entries are one proposal's lists
    +            for field in FIELDS:
    +                terms[field] += [i for i in each[field] if i not in terms[field]]
    +        if any(e.get("glossary") for e in found):
    +            path = self.dir / "glossary.md"
    +            path.write_text("---\nid: glossary-proposal/%s/%s-glossary\nkind: glossary-proposal\npart_of: %s\nstatus: drafted\n%sdate: %s\n"
    +                            "---\n\n# glossary\n\nThe drafts of this proposal are in %s.\n" % (
    +                                prefix, self.dir.name, ident, "".join("%s: [%s]\n" % (f, ", ".join(terms[f])) for f in FIELDS),
    +                                datetime.date.today().isoformat(), stage_dir))
    +            written.append(path)
             return written
    diff --git a/scripts/supervise_done.py b/scripts/supervise_done.py
    index 9bbcdbd4..8ccfff57 100644
    --- a/scripts/supervise_done.py
    +++ b/scripts/supervise_done.py
    @@ -4,6 +4,7 @@ record are committed is set `done`, and that is committed on the initiative bran
     supervise.Run."""
     import re
     
    +import supervise_glossary
     import workqueue
     import workqueue_done
     from supervise_worker import git
    @@ -24,6 +25,17 @@ class Dones:
                 return False
             return not git(self.root, "status", "--porcelain", "--", *found).stdout.strip()
     
    +    def set_glossary_done(self):
    +        """The done of an initiative that changes only the glossary (r161), with no branch review, measurement or analysis."""
    +        data, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
    +        before = data.get("status")
    +        if before == "done" or not supervise_glossary.glossary_only_done(self.root, self.dir):
    +            return
    +        with self.lock:
    +            workqueue_done.mark(self.dir, self.root)
    +            self.log(**{"work-item": self.initiative, "before": before, "after": "done", "by": "work run"})
    +            self.commit(self.initiative, before, "done")
    +
         def set_done(self):
             """The initiative's own transition to done (r105), logged and committed on the initiative branch (r109)."""
             data, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
    diff --git a/scripts/supervise_glossary.py b/scripts/supervise_glossary.py
    new file mode 100644
    index 00000000..d0e4c745
    --- /dev/null
    +++ b/scripts/supervise_glossary.py
    @@ -0,0 +1,103 @@
    +"""The glossary-proposals of an initiative (spec-integration r55, design decision 0073): a term reaches spec/index.md only
    +once the person has approved its glossary-proposal, so an apply round's brief withholds the terms of every glossary-proposal
    +that is not `approved`; and a question under a delegation that names a term of the glossary or a glossary-proposal is
    +left for the person (supervision r162). Standard library only."""
    +import re
    +
    +import workqueue
    +from supervise_worker import GitFailed, git
    +
    +FIELDS = ("adds", "changes", "removes")
    +
    +
    +ROUTES = {"drafted": ("gate", "awaiting-answer"), "awaiting-answer": ("apply", "approved")}     # no further round (r167)
    +
    +
    +def statuses(directory):
    +    """(name, status) of each glossary-proposal in the initiative's directory, by name."""
    +    found = []
    +    for path in sorted(directory.glob("*.md")):
    +        data, _ = workqueue.frontmatter(path.read_text())
    +        if data.get("kind") == "glossary-proposal":
    +            found.append((path.stem, data.get("status")))
    +    return found
    +
    +
    +def route(status, questions, answers):
    +    """(round, status after) of a glossary-proposal at `status`, else None: a drafted one is given to a gate round (r164,
    +    r169); an awaiting-answer one with a question, every one answered, to an apply round (r165, r166, r172)."""
    +    if status == "awaiting-answer" and not (questions and answers >= questions):
    +        return None
    +    return ROUTES.get(status)
    +
    +
    +def withheld(directory, applying=None):
    +    """The terms (`term/<term>` ids, in the order found) of each glossary-proposal in the initiative's directory whose
    +    status is not `approved`, the one named `applying` left out: its answers are the approval (r165)."""
    +    terms = []
    +    for path in sorted(directory.glob("*.md")):
    +        data, _ = workqueue.frontmatter(path.read_text())
    +        if data.get("kind") != "glossary-proposal" or data.get("status") == "approved" or path.stem == applying:
    +            continue
    +        terms += [i for f in FIELDS for i in data.get(f) or [] if i not in terms]
    +    return terms
    +
    +
    +def terms_of(root):
    +    """The terms of spec/index.md's `## Glossary`: the bold name of each bullet."""
    +    path = root / "spec" / "index.md"
    +    return terms_in(path.read_text()) if path.is_file() else []
    +
    +
    +def terms_in(text):
    +    terms, inside = [], False
    +    for line in text.splitlines():
    +        if line.startswith("## "):
    +            inside = line.strip() == "## Glossary"
    +        elif inside and (m := re.match(r"- \*\*(.+?)\*\*", line)):
    +            terms.append(m.group(1).strip())
    +    return terms
    +
    +
    +def glossary_only_done(root, directory):
    +    """Whether the initiative changes only the glossary and is delivered (r161): it has glossary-proposals, no other
    +    proposal and no work-item, every glossary-proposal is approved, and spec/index.md as committed at HEAD holds each term
    +    they add or change and none they remove, with no uncommitted change."""
    +    kinds = [workqueue.frontmatter(p.read_text())[0] for p in sorted(directory.glob("*.md"))
    +             if p.name not in ("initiative.md", "ledger.md")]
    +    if not kinds or any(d.get("kind") != "glossary-proposal" or d.get("status") != "approved" for d in kinds):
    +        return False
    +    try:
    +        held = terms_in(git(root, "show", "HEAD:spec/index.md").stdout)
    +        if git(root, "status", "--porcelain", "--", "spec/index.md").stdout.strip():
    +            return False
    +    except GitFailed:
    +        return False
    +    return (all(i[len("term/"):] in held for d in kinds for f in ("adds", "changes") for i in d.get(f) or [])
    +            and not any(i[len("term/"):] in held for d in kinds for i in d.get("removes") or []))
    +
    +
    +def proposals_of(root):
    +    """The file stem and the full id of every glossary-proposal under .shop/work/, of any initiative and status."""
    +    names = []
    +    for path in sorted((root / ".shop" / "work").glob("*/*.md")):
    +        data, _ = workqueue.frontmatter(path.read_text())
    +        if data.get("kind") == "glossary-proposal":
    +            names += [path.stem] + ([data["id"]] if data.get("id") else [])
    +    return names
    +
    +
    +def names_one(root, question):
    +    """Whether the question names a term of the glossary or a glossary-proposal (supervision r162): as a whole word or
    +    phrase, in any case."""
    +    return any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), question, re.IGNORECASE)
    +               for n in terms_of(root) + proposals_of(root))
    +
    +
    +def text(directory, applying=None):
    +    """The line an apply round's brief gives about them; empty when no term is withheld."""
    +    terms = withheld(directory, applying)
    +    if not terms:
    +        return ""
    +    return ("The person has not approved these terms of the initiative's glossary-proposals: %s. Apply none of them to "
    +            "spec/index.md, also where the drafts hold them." % ", ".join(terms))
    diff --git a/scripts/supervise_rounds.py b/scripts/supervise_rounds.py
    index b52dce88..09b86254 100644
    --- a/scripts/supervise_rounds.py
    +++ b/scripts/supervise_rounds.py
    @@ -8,6 +8,7 @@ import json
     import shutil
     import subprocess
     
    +import supervise_glossary
     import supervise_outputs
     import workqueue
     import workqueue_done
    @@ -34,13 +35,17 @@ class Rounds(Changes, Raises):
                     found.append((path.stem, data.get("status")))
             return found
     
    +    def glossary_proposals(self):
    +        """The names of the initiative's glossary-proposals: an output of its integration, as a capability-proposal is."""
    +        return [p.stem for p in sorted(self.dir.glob("*.md")) if workqueue.frontmatter(p.read_text())[0].get("kind") == "glossary-proposal"]
    +
         def due(self, left=()):
             """(name, round, status after) of the first proposal with a round to run, else None; the names in `left` have none.
             Its questions all have an answer when its `## Answers` holds as many bullets as its `## Questions`, none at all
             included (r70)."""
             data, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
             if self.initiative not in left and data.get("fulfils") and (data.get("status") == "proposed" or (     # r79: no request, no lines to integrate
    -                data.get("status") == "started" and not self.proposals() and not self.items())):     # r93
    +                data.get("status") == "started" and not self.proposals() and not self.glossary_proposals() and not self.items())):     # r93
                 try:     # a request the queue lacks gives no round, before anything moves
                     workqueue_request.accepted_lines(self.root, str(data["fulfils"]).rsplit("/", 1)[-1])
                     return (self.initiative, "integrate", "started")
    @@ -50,6 +55,10 @@ class Rounds(Changes, Raises):
                 if name not in left and status in AFTER and (status != "awaiting-answer"
                                         or len(self.held(name, "Answers")) >= len(self.held(name, "Questions"))):
                     return (name, *self.route(name, status))
    +        for name, status in supervise_glossary.statuses(self.dir):     # r164, r165, r169
    +            one = supervise_glossary.route(status, len(self.held(name, "Questions")), len(self.held(name, "Answers")))
    +            if name not in left and one:
    +                return (name, *one)
             return None
     
         def route(self, name, status):
    @@ -161,7 +170,7 @@ class Rounds(Changes, Raises):
                     raise Refused("the apply round of %s (%s) ended, and %s keeps its status %s: its change list names %s, "
                                   "which neither spec/capabilities/ nor its drafts have" % (
                                       name, self.rel(self.dir / "runs" / name / label), name, before, ", ".join(lacking)))
    -            if applied:
    +            if applied and name not in dict(supervise_glossary.statuses(self.dir)):     # r166: a glossary-proposal keeps its lists
                     self.rewrite_lists(name, applied)
                 asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []]
                 if supervise_outputs.gives_nothing(data):     # r147: its output; the proposal stays as it is and the next round is due (r150)
    diff --git a/scripts/workqueue.py b/scripts/workqueue.py
    index 875b2040..2fab0f21 100644
    --- a/scripts/workqueue.py
    +++ b/scripts/workqueue.py
    @@ -152,7 +152,7 @@ def move(root, initiative, name, status, by):
         """
         path = Path(root) / WORK / initiative / (name + ".md")
         text = read(path, root) if path.is_file() else ""
    -    own = STATUSES + PROPOSAL_STATUSES if frontmatter(text)[0].get("kind") == "capability-proposal" else STATUSES
    +    own = STATUSES + PROPOSAL_STATUSES if frontmatter(text)[0].get("kind") in ("capability-proposal", "glossary-proposal") else STATUSES
         if status not in own:
             raise Refused("%s is no status of the work-item lifecycle; %s is not moved" % (status, name))
         before = agrees(root, initiative, name)
    diff --git a/spec/capabilities/design-model-check.md b/spec/capabilities/design-model-check.md
    index 0779fca9..e9447bab 100644
    --- a/spec/capabilities/design-model-check.md
    +++ b/spec/capabilities/design-model-check.md
    @@ -3,8 +3,8 @@ id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
     title: Design model check
     narrator: a person or session verifying a repository against the design model
     group: service
    -rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-names-one-requirement, design-decision/query-commands-answer-in-their-output, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items, design-decision/work-items-named-by-ids]
    -retired: [r28, r30, r31, r32, r38, r39, r40, r41, r42, r44, r45, r47, r50, r56, r57, r58, r60, r62, r63, r67, r115, r117]
    +rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-names-one-requirement, design-decision/query-commands-answer-in-their-output, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items, design-decision/work-items-named-by-ids, design-decision/the-glossary-is-a-target-of-spec-work]
    +retired: [r28, r30, r31, r32, r38, r39, r40, r41, r42, r44, r45, r47, r50, r56, r57, r58, r60, r62, r63, r67, r115, r117, r27]
     ---
     
     # Design model check
    @@ -25,6 +25,7 @@ verifies one bounded context: product-level artifacts are read only where the fi
     - [r111] **While** the bounded context has no job, `model check` shall print no `w_unserved_cap` warning.
     - [r33] **Where** `--json` is given, `model check` shall print its violations, warnings, unresolved references and file problems as one JSON object, each code mapped to its plain label, exiting as it would without `--json`.
     - [r36] **When** `model check` decides whether an initiative may be `done`, `model check` shall count a `formulated` capability-proposal, and any `withdrawn` part, as closed.
    +- [r123] **When** `model check` decides whether an initiative may be `done`, `model check` shall count an `approved` glossary-proposal as closed.
     - [r55] **If** `import clingo` fails, then `model check` shall try again, once, under the first interpreter that has clingo of `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3` and `/usr/bin/python3`, in that order.
     - [r12] **If** no interpreter has clingo, then `model check` shall exit with an error, naming each interpreter it tried and the command that installs clingo.
     
    @@ -64,10 +65,11 @@ problem names the file.
     | [r23] | unresolved | a capability-proposal adds or removes an id its capability neither has nor lists as retired, or removes a retired id while not `merged`, `formulated` or `withdrawn`; a proposal that is may name a retired id in `adds`, `changes` or `removes`, one it removes read as that requirement |
     | [r24] | unresolved | a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by`, `depends_on`, `fixes` or `findings` names nothing in the repository, a node of the wrong kind (`supersedes` needs a design-decision, `under` and `depends_on` a capability, `for`, `blocked_by` and `fixes` a work-item, `findings` a review-finding); or any reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>` |
     | [r66] | unresolved | a capability-proposal's `adds`, `changes` or `removes` names `term/<term>` the glossary does not have, except one a `merged` or `formulated` proposal removes |
    +| [r122] | unresolved | a glossary-proposal's `adds`, `changes` or `removes` names `term/<term>` the glossary does not have, except one an `approved` glossary-proposal removes |
     | [r25] | file problem | `spec/index.md` is missing or has no `id`; a capability's `id` is not `capability/<context path>/<file name>`, it has no `## Behaviour` section, its `retired` lists an entry that is neither `r<n>` nor a number, or its frontmatter has `formulated_as` |
     | [r46] | file problem | a node's `id` is not `<kind>/<context path>/<name>` with its own kind, or `spec/index.md`'s is not `bounded-context/<context path>` |
     | [r26] | file problem | a feature file is not `features/<name>.feature` for a capability `<name>`, two of its scenarios not tagged `@deprecated` share a title, or a scenario is tagged `@holding` |
    -| [r27] | file problem | a work directory has no `initiative.md` (the directory named, not the file), an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date not `YYYY-MM-DD`, or a work-item that is not `withdrawn` accepts a requirement of a capability that is not guarantees and no scenario names it yet, other than a retired id the work-item accepts while `green` |
    +| [r124] | file problem | a work directory has no `initiative.md` (the directory named, not the file), an initiative or part has no `id`, a part's kind is not a part kind, `glossary-proposal` being one, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date not `YYYY-MM-DD`, or a work-item that is not `withdrawn` accepts a requirement of a capability that is not guarantees and no scenario names it yet, other than a retired id the work-item accepts while `green` |
     | [r29] | file problem | a decision has no `id` or no `## Decision` section, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds |
     | [r49] | file problem | a bullet in `spec/index.md`'s `## Glossary` is not of the form r48 gives |
     | [r61] | file problem | the repository has `spec/decisions.md`, or a `decisions/`, `work/` or `records/` directory at its root, each named with `scripts/migrate` |
    diff --git a/spec/capabilities/spec-consistency.md b/spec/capabilities/spec-consistency.md
    index a90dcab3..d31a27d8 100644
    --- a/spec/capabilities/spec-consistency.md
    +++ b/spec/capabilities/spec-consistency.md
    @@ -3,7 +3,7 @@ id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
     title: Spec consistency
     narrator: the person keeping a spec
     group: guarantees
    -rests_on: [design-decision/glossary-terms-are-standing, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code, design-decision/workflow-capabilities-are-guarantees]
    +rests_on: [design-decision/the-glossary-is-a-target-of-spec-work, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code, design-decision/workflow-capabilities-are-guarantees]
     retired: []
     ---
     
    diff --git a/spec/capabilities/spec-integration.md b/spec/capabilities/spec-integration.md
    index 11858b90..5c4b0dd9 100644
    --- a/spec/capabilities/spec-integration.md
    +++ b/spec/capabilities/spec-integration.md
    @@ -3,8 +3,8 @@ id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
     title: Spec integration
     narrator: the person at the gate
     group: guarantees
    -rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator]
    -retired: [r5, r9, r18, r8, r10, r11, r34, r36, r37, r38, r41, r42]
    +rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator, design-decision/the-glossary-is-a-target-of-spec-work]
    +retired: [r5, r9, r18, r8, r10, r11, r34, r36, r37, r38, r41, r42, r17]
     ---
     
     # Spec integration
    @@ -29,7 +29,8 @@ It is not formulation and not planning; it writes nothing a client can run.
     - [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id.
     - [r14] **When** a line is removed, `integrating-a-proposal` shall add its id to the capability's `retired` list.
     - [r16] **Where** `model check` is available, **if** applying the approved drafts makes it print a new problem other than an added line with no scenario yet, a removed line's scenario that now names no line, or a scenario that uses a word the new glossary entry avoids, then `integrating-a-proposal` shall not commit them.
    -- [r17] **Where** a repository keeps `.shop/work/`, **when** a glossary term is changed, `integrating-a-proposal` shall put the change with the capability-proposal that needs it, listing the term in its `adds`, `changes` or `removes`.
    +- [r54] **When** a round of the kind `integrate` drafts a change to the glossary, `initiative-round` shall give the terms the change adds, changes and removes in the change list's entry for the glossary and in no entry for a capability.
    +- [r55] **While** the person has not approved the terms of a glossary-proposal, `initiative-round` shall apply none of them to `spec/index.md`.
     - [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, `integrating-a-proposal` shall put it through the gate like a Behaviour line.
     - [r20] **When** a change makes a decision, `integrating-a-proposal` shall show it to the person as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`.
     - [r21] **When** a drafted decision names what it came from, `integrating-a-proposal` shall list by id in its `source` only records, initiatives and decisions, writing the person, a date, a delegation or anything outside the repository in its `by`.
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index 924c62ab..51f11367 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -3,8 +3,8 @@ id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
     title: Supervision
     narrator: the person who started `work run`
     group: service
    -rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140]
    +rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160]
     ---
     
     # Supervision
    @@ -43,16 +43,22 @@ from what using it shows.
     - [r96] **If** a round of the kind `integrate` that `work run` started ends without a change list, **then** `work run` shall exit with an error, naming the round.
     - [r84] **When** `work run` starts the round of the kind `integrate` of a `proposed` initiative, `work run` shall transition the initiative to `started`.
     - [r91] **When** a round of the kind `integrate` that `work run` started ends, `work run` shall keep the round's drafts on the initiative branch.
    -- [r92] **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability.
    +- [r159] **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids it adds, changes and removes on that capability.
    +- [r171] **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
     - [r135] **When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation.
     - [r107] **If** a change list that `work run` reads names a capability that neither `spec/capabilities/` nor the round's drafts have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability.
     - [r68] **When** a capability-proposal is `drafted`, `work run` shall start a round of the kind `gate` whose brief asks for the gate as questions, each a decision with its readings and the recommended reading marked.
    -- [r104] **When** `work run` starts a round of the kind `gate` for a capability-proposal, `work run` shall ask the round only for the questions on the lines and terms the proposal adds, changes or removes.
    +- [r164] **When** a glossary-proposal is `drafted`, `work run` shall start a round of the kind `gate` for it, asking only for the questions on the terms it adds, changes or removes.
    +- [r168] **When** `work run` starts a round of the kind `gate` for a capability-proposal, `work run` shall ask the round only for the questions on the lines the proposal adds, changes or removes.
     - [r108] **When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the round of the kind `integrate` that wrote the proposal.
    +- [r170] **When** `work run` starts a round of the kind `gate` or `apply` for a glossary-proposal, `work run` shall give the round the path of the kept drafts of the round of the kind `integrate` that wrote the proposal.
     - [r85] **When** a round of the kind `gate` that `work run` started for a capability-proposal ends, `work run` shall write the questions its result gives under the proposal's `## Questions`.
     - [r117] **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
     - [r69] **When** a round of the kind `gate` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `awaiting-answer`.
    +- [r169] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends, `work run` shall transition the proposal to `awaiting-answer`.
     - [r70] **When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.
    +- [r165] **When** every question that a round of the kind `gate` gave on a glossary-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.
    +- [r172] **While** a glossary-proposal is `awaiting-answer` and a question that a round of the kind `gate` gave on it has no answer, `work run` shall start no round of the kind `apply` for it.
     - [r116] **When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers.
     - [r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
     - [r151] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied.
    @@ -60,6 +66,8 @@ from what using it shows.
     - [r142] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory.
     - [r143] **When** `work run` starts a round of the kind `integrate` for a capability-proposal, `work run` shall keep the proposal's status until the round ends.
     - [r144] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall transition the proposal to `approved`.
    +- [r166] **When** a round of the kind `apply` that `work run` started for a glossary-proposal ends having applied its drafts, `work run` shall transition the proposal to `approved`.
    +- [r167] **When** a round of the kind `apply` that `work run` started for a glossary-proposal ends having applied its drafts, `work run` shall start no round of the kind `formulate` for the proposal.
     - [r145] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.
     - [r146] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall start a round of the kind `formulate` for the proposal.
     - [r147] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output.
    @@ -85,8 +93,10 @@ from what using it shows.
     - [r76] **When** the `measure initiative` that `work run` ran on an initiative has written its measurement, `work run` shall start a session of `analyzing-a-batch` that writes the initiative's analysis record.
     - [r106] **When** `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch.
     - [r105] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
    +- [r161] **When** an initiative changes only the glossary, its glossary-proposal is `approved` and its terms are committed to `spec/index.md`, `work run` shall set the initiative's status to `done`.
     - [r109] **When** `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.
    -- [r77] **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
    +- [r163] **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that names neither a term of the glossary nor a glossary-proposal to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
    +- [r162] **When** a question of an initiative names a term of the glossary or a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation.
     - [r78] **Where** the request an initiative fulfils gives a delegation, **when** a session `work run` started under it answers a question, `work run` shall write the answer naming the delegation it was given under.
     - [r118] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`.
     - [r119] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that accepts the work-item as it is, `work run` shall transition the work-item to `done`.
    diff --git a/spec/decisions/0073-the-glossary-is-a-target-of-spec-work.md b/spec/decisions/0073-the-glossary-is-a-target-of-spec-work.md
    new file mode 100644
    index 00000000..efe88d2d
    --- /dev/null
    +++ b/spec/decisions/0073-the-glossary-is-a-target-of-spec-work.md
    @@ -0,0 +1,23 @@
    +---
    +id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-glossary-is-a-target-of-spec-work
    +summary: "The glossary is a target of spec work in its own right, beside the capabilities: its terms are proposed by a glossary-proposal of their own, approved at the gate before they are applied to spec/index.md, and its questions are always the person's."
    +date: 2026-10-28
    +status: proposed
    +supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/glossary-terms-are-standing]
    +source: [request/missingmass.io/shopsystem/shopsystem-bdd/q30]
    +by: "the person's ruling, given as the accepted lines of q30, 2026-10-28"
    +---
    +
    +# 0073. The glossary is a target of spec work
    +
    +## Decision
    +
    +Each bullet of `spec/index.md`'s Glossary, `- **<term>**: <definition>. Not: <word>, <word>.`, is a term of the bounded context with the id `term/<context path>/<term>`, standing and approved at the gate like a Behaviour line; renaming one is removing one and adding another, and `model check` judges requirements and scenarios against the terms and the words they avoid (`v_t1` to `v_t3`). The glossary is a target of spec work in its own right, beside the capabilities: an `integrate` round's change list gives the terms it adds, changes and removes in an entry for the glossary and in no capability's; `work run` writes a glossary-proposal for that entry, whose terms the gate approves before they are applied to `spec/index.md` and which `model check` checks as it checks a capability-proposal's terms; an initiative that changes only the glossary is delivered with no capability-proposal; and a question that names a term or a glossary-proposal is the person's, never answered under a delegation.
    +
    +## Context
    +
    +Under decision 0033 a term change could only ride with the capability-proposal that needed it, and every entry of a change list named a capability, so a change to the glossary alone had no proposal to go in.
    +
    +## Alternatives
    +
    +A term change riding with a capability-proposal, listed in its `adds`, `changes` or `removes` (decision 0033's consequence), kept: rejected by the person's ruling.
    diff --git a/spec/decisions/index.md b/spec/decisions/index.md
    index 0a87a478..cfcf88c3 100644
    --- a/spec/decisions/index.md
    +++ b/spec/decisions/index.md
    @@ -76,3 +76,4 @@ Each decision's `## Decision` section is standing; the rest of its file is recor
     | [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-answer-to-a-reviewer-returns-to-ready-or-done](0069-an-answer-to-a-reviewer-returns-to-ready-or-done.md) | An answer to a reviewer's question on a work-item takes the work-item from `awaiting-answer` to `ready` when it asks for a change and to `done` when it accepts the work-item as it is, replacing decision 0063's row for a reviewer's question. | accepted | design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-ruling-returns-to-the-asking-stage |  |
     | [design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-asker-is-told-by-its-registered-asker-id](0071-an-asker-is-told-by-its-registered-asker-id.md) | For now `work` tells one asker from another by the asker id its repository is registered under, and the upstream's allow list holds those asker ids. | accepted |  |  |
     | [design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-list-and-work-show-replace-work-status](0072-work-list-and-work-show-replace-work-status.md) | `work status` and `work show` are consolidated into `work list`, which lists all work (initiatives, requests and work-items) with its status, and `work show <id>`, which shows the detail of one initiative, request or work-item; `work status` is retired. | proposed |  |  |
    +| [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-glossary-is-a-target-of-spec-work](0073-the-glossary-is-a-target-of-spec-work.md) | The glossary is a target of spec work in its own right, beside the capabilities: its terms are proposed by a glossary-proposal of their own, approved at the gate before they are applied to spec/index.md, and its questions are always the person's. | proposed | design-decision/missingmass.io/shopsystem/shopsystem-bdd/glossary-terms-are-standing |  |
    diff --git a/spec/index.md b/spec/index.md
    index 64592a38..237f14c0 100644
    --- a/spec/index.md
    +++ b/spec/index.md
    @@ -88,7 +88,7 @@ Tools the skills and agents run:
     ## Glossary
     
     - **agent**: a definition under `agents/` (its name, model, tools and skills) that a worker or a dispatch is started as. Not: persona.
    -- **answer**: the answer to a question on a work-item, a capability-proposal or a request, written in it in its answerer's words. Not: ruling.
    +- **answer**: the answer to a question on a work-item, a capability-proposal, a glossary-proposal or a request, written in it in its answerer's words. Not: ruling.
     - **brief**: the input data `work run` writes for one worker in its stage directory, naming the work-item, the files to read, the worktree and where the result goes. Not: task file.
     - **check**: a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.
     - **claim**: the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`; no two claims share a file. Not: lock, reservation.
    @@ -102,6 +102,7 @@ Tools the skills and agents run:
     - **fault**: a failure outside a session's work that stops it: a push or git command failing, a worker changing a file under `.shop/work/` outside its stage directory, or a session `work run` started ending in an error, at its turn limit or without a result `work run` can read.
     - **file set**: the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
     - **gate**: the person's approval of Behaviour lines and glossary entries before they are committed to `spec/`, with the questions they raise. Not: sign-off.
    +- **glossary-proposal**: the part of an initiative, beside its capability-proposals, that proposes the terms the glossary of `spec/index.md` adds, changes and removes, listing each `term/<term>` in its `adds`, `changes` or `removes`.
     - **guarantees capability**: a capability of the group guarantees, checked by `measure` on real batches and not by scenarios.
     - **hand-back**: an implementer's stop with the outcome `HAND-BACK`, giving the condition and its evidence word for word. Not: handback.
     - **initiative branch**: the branch `work run` commits each transition on and merges each work-item branch into; its base is the commit it started from. Not: integration branch.
    @@ -125,7 +126,7 @@ Tools the skills and agents run:
     - **session**: one Claude Code conversation with its own id and transcript: the person's, a worker or a dispatch. Not: conversation, chat.
     - **stage**: one session `work run` starts for a node from its status: research, plan, implementation and review by a worker, a round of a kind, or an answering session. Not: phase.
     - **stage directory**: the directory `runs/<work-item>/<k>-<stage>/` that holds one stage's brief, result, report and session. Not: run directory.
    -- **status**: a node's place in its kind's lifecycle (a work-item's, a capability-proposal's, a decision's), written in its frontmatter; a work-item's are `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-answer`, `failed` and `withdrawn`; a capability-proposal's are `drafted`, `awaiting-answer`, `approved`, `formulated`, `merged` and `withdrawn`; a request's are `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`, `refused` and `withdrawn`; an initiative's are `proposed`, `started`, `done` and `abandoned`. Not: state.
    +- **status**: a node's place in its kind's lifecycle (a work-item's, a capability-proposal's, a decision's), written in its frontmatter; a work-item's are `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-answer`, `failed` and `withdrawn`; a capability-proposal's are `drafted`, `awaiting-answer`, `approved`, `formulated`, `merged` and `withdrawn`; a glossary-proposal's are `drafted`, `awaiting-answer`, `approved` and `withdrawn`; a request's are `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`, `refused` and `withdrawn`; an initiative's are `proposed`, `started`, `done` and `abandoned`. Not: state.
     - **suite**: every test `python3 -m pytest` runs from the root by default. Not: fast suite.
     - **template**: standing text in a skill or an agent definition that a session fills with input to start another session. Not: boilerplate.
     - **tool use**: one call of a tool in a session's transcript, named by the tool.
    diff --git a/tests/scenarios/conftest.py b/tests/scenarios/conftest.py
    index d4694853..00913674 100644
    --- a/tests/scenarios/conftest.py
    +++ b/tests/scenarios/conftest.py
    @@ -158,6 +158,13 @@ class World:
                 ---
                 """ % (full("capability-proposal", ident), initiative, status, argues, adds, changes, removes, date)))
     
    +    def glossary_proposal(self, ident="p1", status="drafted", initiative="i1", **lists):
    +        """A glossary-proposal part; `lists` are its adds, changes and removes, each as the text of a list."""
    +        body = "".join("%s: %s\n" % (k, v) for k, v in lists.items())
    +        self.write(".shop/work/%s/%s.md" % (initiative, ident),
    +                   "---\nid: %s\nkind: glossary-proposal\npart_of: initiative/%s\nstatus: %s\n%s---\n"
    +                   % (full("glossary-proposal", ident), initiative, status, body))
    +
         def observation(self, ident="obs-1"):
             self.write(".shop/records/observations.md", "# Observations\n\n## %s\nabout: %s\nby: someone\ndate: 2026-10-15\n\nSeen.\n"
                        % (full("observation", ident), CONTEXT))
    diff --git a/tests/scenarios/design_model_check_given.py b/tests/scenarios/design_model_check_given.py
    index 388a363e..618ac81c 100644
    --- a/tests/scenarios/design_model_check_given.py
    +++ b/tests/scenarios/design_model_check_given.py
    @@ -123,6 +123,26 @@ def proposal_naming_term(world, context, status, field, term):
         context["term"] = term
     
     
    +@given("no other glossary-proposal")
    +def no_other_glossary_proposal(world):
    +    pass
    +
    +
    +@given(parsers.re(r"(?:an|a) (?P<status>awaiting-answer|withdrawn|(?<=an )approved) glossary-proposal whose removes names term/(?P<term>\w+)"))
    +def remover_glossary_proposal(world, status, term):
    +    world.observation()
    +    world.initiative()
    +    world.glossary_proposal(ident="p2", status=status, removes="[term/%s]" % term)
    +
    +
    +@given(parsers.re(r"a (?P<status>drafted|(?<!n )approved) glossary-proposal whose (?P<field>adds|changes|removes) names term/(?P<term>\w+)"))
    +def glossary_proposal_naming_term(world, context, status, field, term):
    +    world.observation()
    +    world.initiative()
    +    world.glossary_proposal(status=status, **{field: "[term/%s]" % term})
    +    context["term"] = term
    +
    +
     # --- Given: frontmatter references (r24) -----------------------------------------------------------------------
     
     DECISION = "---\nid: %s\nsummary: S\ndate: 2026-01-01\nstatus: accepted\n%s---\n\n## Decision\nWe do it.\n"
    diff --git a/tests/scenarios/design_model_check_problems.py b/tests/scenarios/design_model_check_problems.py
    index 1b4cb134..3cd8a1ae 100644
    --- a/tests/scenarios/design_model_check_problems.py
    +++ b/tests/scenarios/design_model_check_problems.py
    @@ -73,53 +73,6 @@ def _initiative_with(world, old, new):
         p.write_text(p.read_text().replace(old, new))
     
     
    -@given(parsers.parse("a repository with a work directory .shop/work/i1 in which {case}"))
    -def malformed_work(world, case):
    -    def part(**changes):
    -        fm = {"id": full("work-item", "p1"), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted",
    -              "under": "thing", "check": "true"}
    -        fm.update(changes)
    -        world.write(".shop/work/i1/p1.md", "---\n" + "".join("%s: %s\n" % (k, v) for k, v in fm.items() if v is not None) + "---\n")
    -    world.good()
    -    if case == "there is no initiative.md":
    -        part()
    -        return
    -    world.initiative()
    -    if case == "initiative.md has no id":
    -        _initiative_with(world, "id: %s\n" % I1, "")
    -    elif case == "the part p1.md has no id":
    -        part(id=None)
    -    elif case == "the part p1.md has the kind banana":
    -        part(kind="banana")
    -    elif case == "the part p1.md has no status":
    -        part(status=None)
    -    elif case == "the part p1.md has a status not in its kind's lifecycle":
    -        part(status="loved")
    -    elif case == "the part p1.md has the kind capability-proposal and the status built":
    -        part(id=full("capability-proposal", "p1"), kind="capability-proposal", status="built")
    -    elif case == "initiative.md has the priority high":
    -        _initiative_with(world, "priority: 1", "priority: high")
    -    else:
    -        assert case == "initiative.md has a date written 16/10/2026", case
    -        _initiative_with(world, "date: 2026-10-15", "date: 16/10/2026")
    -
    -
    -@given("a work-item in .shop/work/i1/w1.md that accepts thing#r2")
    -def work_item_accepting(world, context):
    -    world.observation()
    -    world.initiative()
    -    world.work_item(accepts="[thing#r2]")
    -    context["mentions"] = THING + "#r2"
    -
    -
    -@given(parsers.parse("a work-item in .shop/work/i1/w1.md with status {status} that accepts thing#r2"))
    -def work_item_with_status_accepting(world, context, status):
    -    world.observation()
    -    world.initiative()
    -    world.work_item(status=status, accepts="[thing#r2]")
    -    context["mentions"] = THING + "#r2"
    -
    -
     @given("a repository with two capabilities that each have no ## Behaviour section")
     def two_capabilities_without_behaviour(world):
         for name in ("thing", "other"):
    diff --git a/tests/scenarios/design_model_check_trace.py b/tests/scenarios/design_model_check_trace.py
    index c2f2ca15..c5a5fbcf 100644
    --- a/tests/scenarios/design_model_check_trace.py
    +++ b/tests/scenarios/design_model_check_trace.py
    @@ -116,6 +116,11 @@ def formulated_proposal(world):
         world.proposal(status="formulated", adds="[thing#r1]")
     
     
    +@given("under it a glossary-proposal with status approved")
    +def approved_glossary_proposal(world):
    +    world.glossary_proposal(status="approved")
    +
    +
     @given(parsers.parse("under it a capability-proposal with status withdrawn, and under that a work-item with status {status}"))
     def withdrawn_proposal_with_item(world, status):
         world.proposal(status="withdrawn", adds="[thing#r1]")
    diff --git a/tests/scenarios/design_model_check_work.py b/tests/scenarios/design_model_check_work.py
    new file mode 100644
    index 00000000..33949a5e
    --- /dev/null
    +++ b/tests/scenarios/design_model_check_work.py
    @@ -0,0 +1,48 @@
    +"""design-model-check's malformed work directories and work files (r124)."""
    +import re
    +
    +from pytest_bdd import given, parsers
    +
    +from .conftest import I1, THING, cap, full
    +from .design_model_check_problems import _initiative_with
    +
    +
    +@given(parsers.parse("a repository with a work directory .shop/work/i1 in which {case}"))
    +def malformed_work(world, case):
    +    def part(**changes):
    +        fm = {"id": full("work-item", "p1"), "kind": "work-item", "part_of": "initiative/i1", "status": "drafted",
    +              "under": "thing", "check": "true"}
    +        fm.update(changes)
    +        world.write(".shop/work/i1/p1.md", "---\n" + "".join("%s: %s\n" % (k, v) for k, v in fm.items() if v is not None) + "---\n")
    +    world.good()
    +    if case == "there is no initiative.md":
    +        part()
    +        return
    +    world.initiative()
    +    typed = re.fullmatch(r"the part p1\.md has the kind ([\w-]+) and the status ([\w-]+)", case)
    +    item = re.fullmatch(r"the work-item w1\.md with status (\w+) accepts thing#r2, (.*)", case)
    +    if case == "initiative.md has no id":
    +        _initiative_with(world, "id: %s\n" % I1, "")
    +    elif case == "initiative.md has no status":
    +        _initiative_with(world, "status: started\n", "")
    +    elif case == "the part p1.md has no id":
    +        part(id=None)
    +    elif case == "the part p1.md has the kind banana":
    +        part(kind="banana")
    +    elif case == "the part p1.md has no status":
    +        part(status=None)
    +    elif typed:
    +        kind, status = typed.groups()
    +        part(id=full(kind, "p1"), kind=kind, status=status)
    +    elif item:
    +        status, why = item.groups()
    +        if "guarantees" in why:
    +            world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], group="guarantees"))
    +        elif "retired" in why:
    +            world.write("spec/capabilities/thing.md", cap("thing", ["- [r1] One."], retired="[r2]"))
    +        world.work_item(status=status, accepts="[thing#r2]")
    +    elif case == "initiative.md has the priority high":
    +        _initiative_with(world, "priority: 1", "priority: high")
    +    else:
    +        assert case == "initiative.md has a date written 16/10/2026", case
    +        _initiative_with(world, "date: 2026-10-15", "date: 16/10/2026")
    diff --git a/tests/scenarios/spec_integration_apply_steps.py b/tests/scenarios/spec_integration_apply_steps.py
    index ec7c9309..93835076 100644
    --- a/tests/scenarios/spec_integration_apply_steps.py
    +++ b/tests/scenarios/spec_integration_apply_steps.py
    @@ -5,6 +5,7 @@ import json
     
     from pytest_bdd import given, then, when
     
    +from .conftest import INDEX
     from .spec_integration_steps import run_integrate
     from .supervision_given import repository
     from .supervision_rounds_steps import formulate_did_its_work, rounds
    @@ -19,12 +20,16 @@ KEPT = ".shop/scratch/1-integrate/drafts/round-1"
            "when an order ships", target_fixture="plan")
     def answered_proposal(repo):
         plan = repository(repo)
    +    answered_proposal_in(repo)
    +    return plan
    +
    +
    +def answered_proposal_in(repo):
         write(repo, ".shop/work/i1/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\n"
               "argues: [thing]\nadds: [thing#r1]\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n\n"
               "The drafts of this proposal are in %s.\n\n## Questions\n\n- Anything shown?\n- Anything told?\n\n"
               "## Answers\n\n- %s\n- %s\n" % (full("capability-proposal", "p1"), full("initiative", "i1"), KEPT, STATUS, SHIPS))
         commit_all(repo, "an answered capability-proposal")
    -    return plan
     
     
     @given("drafts that hold a line that the customer sees the status of an order")
    @@ -47,6 +52,65 @@ def run_apply(repo, plan, context):
         run_integrate(repo, plan, context)
     
     
    +def index_text(repo):
    +    return (repo / "spec/index.md").read_text()
    +
    +
    +@given("spec/index.md's glossary has the term order and no term refund", target_fixture="plan")
    +def glossary_order_only(repo):
    +    plan = repository(repo)
    +    write(repo, "spec/index.md", INDEX + "\n## Glossary\n\n- **order**: a thing a customer buys.\n")
    +    commit_all(repo, "spec/index.md's glossary")
    +    plan["before"] = index_text(repo)
    +    return plan
    +
    +
    +@given("an initiative with a glossary-proposal that adds the term refund and changes the term order")
    +def initiative_glossary_proposal(repo):
    +    write(repo, ".shop/work/i1/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: drafted\n"
    +          "adds: [term/refund]\nchanges: [term/order]\nremoves: []\ndate: 2026-10-28\n---\n\n# glossary\n" % (
    +              full("glossary-proposal", "g1"), full("initiative", "i1")))
    +    commit_all(repo, "a glossary-proposal")
    +
    +
    +@given("the person has not approved the terms of that glossary-proposal")
    +def terms_not_approved(repo):
    +    assert "status: approved" not in (repo / ".shop/work/i1/g1.md").read_text()
    +
    +
    +@given("a capability-proposal of that initiative the person has approved")
    +def approved_proposal(repo, plan):
    +    answered_proposal_in(repo)
    +    write(repo, KEPT + "/spec/capabilities/thing.md", "**When** asked, `thing` shall show the customer the refund of an order.\n")
    +    commit_all(repo, "an answered capability-proposal")
    +    plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", "adds": ["thing#r1"]}]}}
    +    plan["initiative-round"] = {"status": "DONE"}
    +    formulate_did_its_work(plan)
    +
    +
    +@when("work run starts a round of the kind apply on that capability-proposal")
    +def run_apply_on(repo, plan, context):
    +    run_integrate(repo, plan, context)
    +
    +
    +@then("the round applies the capability-proposal's drafts")
    +def round_applies_proposals_drafts(repo, context):
    +    round_applies(repo, context)
    +
    +
    +@then("spec/index.md's glossary has no term refund")
    +def glossary_no_refund(repo, context):
    +    assert "refund" not in index_text(repo), index_text(repo)
    +    brief = apply_round(repo, context)["brief"]
    +    assert "term/refund" in brief and "Apply none of them to spec/index.md" in brief, brief
    +
    +
    +@then("spec/index.md's glossary has the term order as it was before the round")
    +def glossary_order_unchanged(repo, plan, context):
    +    assert index_text(repo) == plan["before"], index_text(repo)
    +    assert "term/order" in apply_round(repo, context)["brief"]
    +
    +
     def apply_round(repo, context):
         found = rounds(repo, "apply")
         assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    diff --git a/tests/scenarios/spec_integration_steps.py b/tests/scenarios/spec_integration_steps.py
    index 6cb26c3c..2013361c 100644
    --- a/tests/scenarios/spec_integration_steps.py
    +++ b/tests/scenarios/spec_integration_steps.py
    @@ -6,7 +6,7 @@ import os
     import subprocess
     import sys
     
    -from pytest_bdd import given, then, when
    +from pytest_bdd import given, parsers, then, when
     
     from .conftest import INDEX, SCRIPTS, cap, full
     from .supervision_given import repository
    @@ -62,6 +62,69 @@ def approved_note(repo, plan):
         plan["initiative-round"] = {"status": "DONE"}
     
     
    +REFUNDS_DRAFTS = ".shop/scratch/1-integrate/drafts/round-1/spec/capabilities/refunds.md"
    +REFUND_LINE = "**When** an order is cancelled, `refunds` shall show the customer the refund of the order."
    +
    +
    +@given(parsers.re(r"spec/index.md's glossary has the terms (?P<first>\w+) and (?P<second>\w+)$"), target_fixture="plan")
    +def glossary_with_terms(repo, first, second):
    +    plan = repository(repo)
    +    write(repo, "spec/index.md", INDEX + "\n## Glossary\n\n- **%s**: a thing.\n- **%s**: a thing.\n" % (first, second))
    +    commit_all(repo, "spec/index.md's glossary")
    +    return plan
    +
    +
    +@given("an approved note asks that the customer sees the refund of a cancelled order")
    +def cancelled_note(repo, plan):
    +    approved_note(repo, plan)
    +
    +
    +@given("that note adds the term refund, changes the term order and removes the term basket")
    +def note_terms(plan):
    +    plan["round:integrate"] = {"status": "DONE", "write": {REFUNDS_DRAFTS: cap("refunds", ["- [r1] " + REFUND_LINE])}, "fields": {
    +        "changes": [entry("refunds", "adds refunds#r1"), {"glossary": True, "adds": ["term/refund"],
    +                                                          "changes": ["term/order"], "removes": ["term/basket"]}]}}
    +
    +
    +def kept_changes(repo, context):
    +    results = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/result.json"))
    +    assert len(results) == 1, (git(repo, "ls-files"), context["done"].stdout, context["done"].stderr)
    +    return json.loads(results[0].read_text()).get("changes") or []
    +
    +
    +def entry_of(repo, context, whose):
    +    found = [e for e in kept_changes(repo, context) if (e.get("glossary") if whose == "glossary" else e.get("capability") == whose)]
    +    assert len(found) == 1, (kept_changes(repo, context), context["done"].stdout, context["done"].stderr)
    +    return found[0]
    +
    +
    +@then("the round drafts a line under the capability refunds that the customer sees the refund of a cancelled order")
    +def drafts_refunds_line(repo, context):
    +    drafts = sorted((repo / ".shop/work/i1/runs/i1").glob("*-integrate/drafts/round-*/spec/capabilities/refunds.md"))
    +    assert any("refund of the order" in p.read_text() for p in drafts), (drafts, context["done"].stdout, context["done"].stderr)
    +    assert (repo / ".shop/work/i1/refunds.md").is_file(), (git(repo, "ls-files", ".shop/work"), context["done"].stderr)
    +
    +
    +@then("the round drafts a change to the glossary")
    +def drafts_glossary_change(repo, context):
    +    brief = integrate_brief(repo, context)
    +    assert "glossary" in brief and "no capability's entry" in brief, brief
    +    assert entry_of(repo, context, "glossary")
    +
    +
    +@then(parsers.re(r"the change list's entry for the glossary gives (?P<a>\w+) as added, (?P<c>\w+) as changed and (?P<r>\w+) as removed$"))
    +def glossary_entry_gives(repo, context, a, c, r):
    +    one = entry_of(repo, context, "glossary")
    +    assert (one["adds"], one["changes"], one["removes"]) == (["term/" + a], ["term/" + c], ["term/" + r]), one
    +
    +
    +@then("the change list's entry for refunds gives none of the terms refund, order and basket")
    +def refunds_entry_no_terms(repo, context):
    +    one = entry_of(repo, context, "refunds")
    +    ids = one["adds"] + one["changes"] + one["removes"]
    +    assert ids and not [i for i in ids if i.startswith("term/")], one
    +
    +
     SHIP = "The customer is told when an order ships."
     SHIP_DRAFTS = ".shop/scratch/1-integrate/drafts/round-1/spec/capabilities/notifications.md"
     
    diff --git a/tests/scenarios/supervision_delegation_steps.py b/tests/scenarios/supervision_delegation_steps.py
    index 73b56998..949e04c7 100644
    --- a/tests/scenarios/supervision_delegation_steps.py
    +++ b/tests/scenarios/supervision_delegation_steps.py
    @@ -20,6 +20,25 @@ def fulfils_with_delegation(repo, context, delegation):
         commit_all(repo, "i1 fulfils q1, which gives a delegation")
     
     
    +@given(parsers.re(r'spec/index\.md\'s Glossary holds the term "(?P<term>[^"]+)"$'))
    +def glossary_holds_term(repo, term):
    +    write(repo, "spec/index.md", "# Index\n\n## Glossary\n\n- **%s**: a thing.\n" % term)
    +    commit_all(repo, "spec/index.md's Glossary holds a term")
    +
    +
    +@given(parsers.re(r"i1's glossary-proposal g1 is awaiting-answer$"))
    +def glossary_proposal_awaiting(repo):
    +    write(repo, DIR + "/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: awaiting-answer\nadds: [term/ledger]\n"
    +          "changes: []\nremoves: []\ndate: 2026-10-15\n---\n" % (full("glossary-proposal", "g1"), full("initiative", "i1")))
    +    commit_all(repo, "an awaiting-answer glossary-proposal")
    +
    +
    +@then(parsers.re(r'"(?P<question>[^"]+)" was given to no session$'))
    +def given_to_no_session(repo, question):
    +    found = [c for c in starts(repo) if c["agent"].endswith("delegation-answerer") and question in c["brief"]]
    +    assert not found, found
    +
    +
     @given(parsers.re(r'i1\'s capability-proposal p1 is awaiting-answer, its ## Questions section with "(?P<question>[^"]+)" and '
                       r"no answer$"))
     def unanswered_proposal(repo, question):
    diff --git a/tests/scenarios/supervision_done_steps.py b/tests/scenarios/supervision_done_steps.py
    index a7a21184..fa3e5e2f 100644
    --- a/tests/scenarios/supervision_done_steps.py
    +++ b/tests/scenarios/supervision_done_steps.py
    @@ -25,6 +25,22 @@ def review_and_records_committed(repo, plan):
         commit_all(repo, "i1's measurement and analysis record")
     
     
    +@given(parsers.re(r'i1 is started, has neither a capability-proposal nor a work-item, and its glossary-proposal g1 is approved, '
    +                  r'its adds naming the term "(?P<term>[^"]+)"$'))
    +def started_glossary_only(repo, term):
    +    write(repo, INITIATIVE, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    +    write(repo, ".shop/work/i1/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: approved\nadds: [term/%s]\n"
    +          "changes: []\nremoves: []\ndate: 2026-10-15\n---\n" % (full("glossary-proposal", "g1"), full("initiative", "i1"), term))
    +    write(repo, ".shop/work/i1/ledger.md", "  - 2026-10-15: gate round 1 glossary: 0 questions\n")
    +    commit_all(repo, "i1 is started with an approved glossary-proposal")
    +
    +
    +@given(parsers.re(r'spec/index\.md\'s Glossary holds the term "(?P<term>[^"]+)", committed on the initiative branch$'))
    +def glossary_committed(repo, term):
    +    write(repo, "spec/index.md", "# Index\n\n## Glossary\n\n- **%s**: a thing.\n" % term)
    +    commit_all(repo, "spec/index.md's Glossary holds %s" % term)
    +
    +
     @given("i1 is started and its work-item w1 is ready")
     def started_with_ready(repo):
         write(repo, INITIATIVE, "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    diff --git a/tests/scenarios/supervision_formulate_steps.py b/tests/scenarios/supervision_formulate_steps.py
    index 849dcf1c..17132d77 100644
    --- a/tests/scenarios/supervision_formulate_steps.py
    +++ b/tests/scenarios/supervision_formulate_steps.py
    @@ -45,6 +45,12 @@ def apply_change_list(plan, text):
         plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"capability": "thing", **entry(text)}]}}
     
     
    +@given(parsers.re(r'the apply round for g1 applies g1\'s drafts and gives DONE with a change list that adds the term "(?P<term>[^"]+)" '
    +                  r"in the glossary$"))
    +def apply_glossary_list(plan, term):
    +    plan["round:apply"] = {"status": "DONE", "fields": {"changes": [{"glossary": True, "adds": ["term/" + term]}]}}
    +
    +
     @given("every other round ends and every worker gives DONE")
     def every_other_round_ends(plan):
         plan["default"] = {"status": "DONE"}
    @@ -72,9 +78,9 @@ def awaiting_after_formulate(repo, context):
         assert ended is not None and moved is not None and ended < moved, (lines, context["done"].stderr)
     
     
    -@then("p1 is awaiting-answer")
    -def proposal_awaiting(repo, context):
    -    text = (repo / DIR / "p1.md").read_text()
    +@then(parsers.re(r"(?P<name>[pg]1) is awaiting-answer$"))
    +def proposal_awaiting(repo, context, name):
    +    text = (repo / DIR / (name + ".md")).read_text()
         assert "\nstatus: awaiting-answer\n" in text, (text, context["done"].stdout, context["done"].stderr)
     
     
    diff --git a/tests/scenarios/supervision_integrate_steps.py b/tests/scenarios/supervision_integrate_steps.py
    index dd1f26eb..8d2bd66d 100644
    --- a/tests/scenarios/supervision_integrate_steps.py
    +++ b/tests/scenarios/supervision_integrate_steps.py
    @@ -4,7 +4,7 @@ import re
     
     from pytest_bdd import given, parsers, then
     
    -from .conftest import cap, full
    +from .conftest import INDEX, cap, full
     from .supervision_rounds_steps import proposed_fulfilling, rounds
     from .supervision_world import commit_all, git, starts, write
     
    @@ -46,6 +46,51 @@ def integrate_with_changes(plan, repo, first, second):
         plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [entry("thing", first), entry("other", second)]}}
     
     
    +@given(parsers.re(r'spec/index\.md\'s Glossary holds the terms "(?P<one>\w+)", "(?P<two>\w+)" and "(?P<three>\w+)"$'))
    +def glossary_holds(repo, one, two, three):
    +    write(repo, "spec/index.md", INDEX + "\n## Glossary\n\n" + "".join("- **%s**: a thing.\n" % t for t in (one, two, three)))
    +    commit_all(repo, "spec/index.md's Glossary")
    +
    +
    +@given(parsers.re(r'the integrate round for i1 gives DONE with a change list that adds the term "(?P<added>\w+)", changes the '
    +                  r'term "(?P<changed>\w+)" and removes the term "(?P<removed>\w+)" in the glossary$'))
    +def integrate_changes_glossary(plan, added, changed, removed):
    +    plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [{
    +        "glossary": True, "adds": ["term/" + added], "changes": ["term/" + changed], "removes": ["term/" + removed]}]}}
    +
    +
    +def glossary_proposals(repo):
    +    """The commits that added a glossary-proposal file under .shop/work/i1/, each with its files' text."""
    +    found = []
    +    for commit in git(repo, "log", "--diff-filter=A", "--format=%H", "--", ".shop/work/i1/").split():
    +        for path in git(repo, "show", "--diff-filter=A", "--name-only", "--format=", commit).split():
    +            if path.startswith(".shop/work/i1/") and path.endswith(".md") and "/runs/" not in path:
    +                text = git(repo, "show", "%s:%s" % (commit, path))
    +                if "\nkind: glossary-proposal\n" in text:
    +                    found.append((commit, path, text))
    +    return found
    +
    +
    +@then(parsers.re(r'the commit that wrote i1\'s glossary-proposal wrote one, drafted, its adds naming the term "(?P<added>\w+)", '
    +                 r'its changes the term "(?P<changed>\w+)" and its removes the term "(?P<removed>\w+)"$'),
    +      target_fixture="glossary_text")
    +def glossary_proposal_written(repo, context, added, changed, removed):
    +    found = glossary_proposals(repo)
    +    where = (found, context["done"].stdout, context["done"].stderr)
    +    assert len(found) == 1, where
    +    commit, _, text = found[0]
    +    assert "\nstatus: drafted\n" in text, where
    +    assert tuple(listed(text, f) for f in ("adds", "changes", "removes")) == (
    +        ["term/" + added], ["term/" + changed], ["term/" + removed]), where
    +    return text
    +
    +
    +@then(parsers.re(r'it names the term "(?P<term>\w+)" in none of its adds, changes and removes$'))
    +def names_in_none(glossary_text, term):
    +    for field in ("adds", "changes", "removes"):
    +        assert "term/" + term not in listed(glossary_text, field), glossary_text
    +
    +
     @given("an initiative i2 under .shop/work/, proposed, that fulfils the request q2, whose line 1 has the line outcome accepted")
     def proposed_i2(repo):
         write(repo, ".shop/work/i2/initiative.md",
    @@ -138,16 +183,16 @@ def listed(text, field):
     
     
     @then(parsers.re(r"the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming "
    -                 r'thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3, and one for other, its '
    -                 r"adds naming other#r1 and its changes and removes naming nothing$"))
    -def proposals_written(repo, context):
    +                 r'thing#r4(?P<term> and the term "ledger")?, its changes thing#r2 and its removes thing#r3, and one for '
    +                 r"other, its adds naming other#r1 and its changes and removes naming nothing$"))
    +def proposals_written(repo, context, term):
         where = (context["done"].stdout, context["done"].stderr)
         commits = git(repo, "log", "--diff-filter=A", "--format=%H", "--", ".shop/work/i1/thing.md").split()
         assert len(commits) == 1, where
         added = git(repo, "show", "--diff-filter=A", "--name-only", "--format=", commits[0]).split()
         assert sorted(p for p in added if p.startswith(".shop/work/i1/") and p.endswith(".md") and "/runs/" not in p) == [
             ".shop/work/i1/other.md", ".shop/work/i1/thing.md"], (added, where)
    -    expected = {"thing": (["thing#r4", "term/ledger"], ["thing#r2"], ["thing#r3"]), "other": (["other#r1"], [], [])}
    +    expected = {"thing": (["thing#r4"] + (["term/ledger"] if term else []), ["thing#r2"], ["thing#r3"]), "other": (["other#r1"], [], [])}
         for name, lists in expected.items():
             text = git(repo, "show", "%s:.shop/work/i1/%s.md" % (commits[0], name))
             assert "\nkind: capability-proposal\n" in text and "\nstatus: drafted\n" in text, text
    diff --git a/tests/scenarios/supervision_proposal_steps.py b/tests/scenarios/supervision_proposal_steps.py
    index d8b63d3e..0dced974 100644
    --- a/tests/scenarios/supervision_proposal_steps.py
    +++ b/tests/scenarios/supervision_proposal_steps.py
    @@ -7,7 +7,7 @@ from pytest_bdd import given, parsers, then
     from .conftest import cap, full
     from .supervision_review_steps import FINDINGS
     from .supervision_rounds_steps import rounds
    -from .supervision_world import calls, commit_all, fields, git, item_text, write
    +from .supervision_world import calls, commit_all, fields, git, item_text, starts, write
     
     DIR = ".shop/work/i1"
     FIX_NOW = ["Important, w1, thing.py:3: the first thing to fix now", "Important, w1, thing.py:9: the second thing to fix now"]
    @@ -122,30 +122,73 @@ def proposal_in_status(repo, plan, status, field, ids):
         commit_all(repo, "p1 is %s" % status)
     
     
    -@given(parsers.re(r"p1 was written from the change list of i1's integrate round, whose drafts are kept at (?P<path>\S+)$"))
    -def written_from_round(repo, path):
    -    file = repo / DIR / "p1.md"
    +@given(parsers.re(r"(?P<name>[pg]1) was written from the change list of i1's integrate round, whose drafts are kept at (?P<path>\S+)$"))
    +def written_from_round(repo, name, path):
    +    file = repo / DIR / (name + ".md")
         head, sep, rest = file.read_text().partition("\n---\n")     # the sentence follows the front matter, as work run writes it
         file.write_text(head + sep + "\n# thing\n\nThe drafts of this proposal are in %s.\n" % path + rest)
         commit_all(repo, "p1 names the drafts it was written from")
     
     
    -@then(parsers.re(r"the (?P<kind>gate|apply) round for p1 was given the path (?P<path>\S+)$"))
    -def round_given_drafts(repo, context, kind, path):
    -    found = rounds(repo, kind, "p1")
    +@given(parsers.re(r"i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with (?P<asked>\"[^,]+?)(?:, given by its "
    +                  r"gate round)?,? and its Answers section with (?P<answers>\"[^,]+?)(?: only)?$"))
    +def glossary_proposal_answered(repo, asked, answers):
    +    """g1 holds each quoted question as a bullet of its Questions and each quoted answer as a bullet of its Answers."""
    +    bullets = lambda text: "".join("- %s\n" % q for q in re.findall(r'"([^"]+)"', text))     # noqa: E731
    +    write(repo, DIR + "/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: awaiting-answer\nadds: [term/ledger]\n"
    +          "changes: [term/shelf]\nremoves: []\ndate: 2026-10-15\n---\n\n## Questions\n\n%s\n## Answers\n\n%s"
    +          % (full("glossary-proposal", "g1"), full("initiative", "i1"), bullets(asked), bullets(answers)))
    +    commit_all(repo, "g1 is awaiting-answer")
    +
    +
    +@then("no round of the kind apply was started for g1")
    +def no_apply_for_g1(repo, context):
    +    assert not rounds(repo, "apply", "g1"), (starts(repo), context["done"].stdout, context["done"].stderr)
    +
    +
    +@then(parsers.re(r"the (?P<kind>gate|apply) round for (?P<name>[pg]1) was given the path (?P<path>\S+)$"))
    +def round_given_drafts(repo, context, kind, name, path):
    +    found = rounds(repo, kind, name)
         assert len(found) == 1, (context["done"].stdout, context["done"].stderr)
         assert "Drafts path: %s\n" % path in found[0]["brief"], found[0]["brief"]
     
     
    -@then(parsers.re(r'the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2, thing#r3 and the '
    -                 r'term "ledger"$'))
    -def gate_names_its_ids(repo, context):
    +@then(parsers.re(r'the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2(?:, | and )thing#r3'
    +                 r'(?P<term> and the term "ledger")?$'))
    +def gate_names_its_ids(repo, context, term):
         found = rounds(repo, "gate", "p1")
         assert len(found) == 1, (context["done"].stdout, context["done"].stderr)
    -    for one in ("thing#r4", "thing#r2", "thing#r3", "term/ledger"):
    +    for one in ("thing#r4", "thing#r2", "thing#r3") + (("term/ledger",) if term else ()):
             assert one in found[0]["brief"], (one, found[0]["brief"])
     
     
    +def terms_of(text):
    +    return re.findall(r'"([^"]+)"', text or "")
    +
    +
    +@given(parsers.re(r"i1's glossary-proposal g1 is drafted(?:, its adds naming the term (?P<adds>\"[^\"]+\"), its changes the term "
    +                  r"(?P<changes>\"[^\"]+\") and its removes the term (?P<removes>\"[^\"]+\"))?$"))
    +def glossary_drafted(repo, adds, changes, removes):
    +    listed = lambda text: ", ".join("term/" + t for t in terms_of(text))
    +    write(repo, DIR + "/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: drafted\nadds: [%s]\nchanges: [%s]\n"
    +          "removes: [%s]\ndate: 2026-10-15\n---\n" % (full("glossary-proposal", "g1"), full("initiative", "i1"),
    +                                                       listed(adds) or "term/ledger", listed(changes), listed(removes)))
    +    commit_all(repo, "g1 is drafted")
    +
    +
    +@then(parsers.re(r"the brief of the gate round for g1 asks only for the questions on the terms (?P<terms>.+)$"))
    +def gate_g1_terms(repo, context, terms):
    +    found = rounds(repo, "gate", "g1")
    +    assert len(found) == 1, (context["done"].stdout, context["done"].stderr)
    +    for one in terms_of(terms):
    +        assert "term/" + one in found[0]["brief"], (one, found[0]["brief"])
    +
    +
    +@then(parsers.re(r'it asks for no question on the term "(?P<term>[^"]+)"$'))
    +def gate_g1_no_other(repo, term):
    +    assert "term/" + term not in rounds(repo, "gate", "g1")[0]["brief"]
    +
    +
     @then("it asks for no question on thing#r1 or on other#r1")
     def gate_names_no_other(repo):
         brief = rounds(repo, "gate", "p1")[0]["brief"]
    diff --git a/tests/scenarios/supervision_reintegrate_steps.py b/tests/scenarios/supervision_reintegrate_steps.py
    index e5d7686a..791a4073 100644
    --- a/tests/scenarios/supervision_reintegrate_steps.py
    +++ b/tests/scenarios/supervision_reintegrate_steps.py
    @@ -80,9 +80,9 @@ def integrate_after_formulate(repo, context):
         assert ended is not None and began is not None and ended < began, (log_lines(repo), context["done"].stderr)
     
     
    -@then("no round of the kind formulate was started for p1")
    -def no_formulate_for_p1(repo, context):
    -    assert rounds(repo, "formulate", "p1") == [], (starts(repo), context["done"].stderr)
    +@then(parsers.re(r"no round of the kind formulate was started for (?P<name>[pg]1)$"))
    +def no_formulate_for_p1(repo, context, name):
    +    assert rounds(repo, "formulate", name) == [], (starts(repo), context["done"].stderr)
     
     
     @then("p1 was awaiting-answer when the formulate round for p1 had ended")
    diff --git a/tests/scenarios/supervision_rounds_steps.py b/tests/scenarios/supervision_rounds_steps.py
    index d2afe1b3..6bfe0fea 100644
    --- a/tests/scenarios/supervision_rounds_steps.py
    +++ b/tests/scenarios/supervision_rounds_steps.py
    @@ -58,7 +58,7 @@ def gate_result(plan, text):
         plan["initiative-round"] = {"status": "DONE", "questions": [gate_question(text)]}
     
     
    -@given(parsers.re(r'the gate round gives the question "(?P<ask>[^"]*)" on p1, and every round ends$'))
    +@given(parsers.re(r'the gate round gives the question "(?P<ask>[^"]*)" on [pg]1, and every round ends$'))
     def gate_gives_question(plan, ask):
         plan["initiative-round"] = {"status": "DONE", "questions": [ask]}
     
    @@ -94,9 +94,10 @@ def bullets(text, heading):
         return found
     
     
    -@then("a round of the kind gate was started for p1")
    -def gate_started(repo, context):
    -    assert len(rounds(repo, "gate")) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    +@then(parsers.re(r"a round of the kind (?P<kind>gate) was started for (?P<name>[pg]1)$"))
    +@then(parsers.re(r"a round of the kind (?P<kind>apply) was started for (?P<name>g1)$"))
    +def gate_started(repo, context, kind, name):
    +    assert len(rounds(repo, kind, name)) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
     
     
     @then("the gate round's brief asks for the gate as questions, each a decision with its readings and the recommended "
    @@ -227,25 +228,25 @@ def started_with_round(repo, context):
         assert "status: started" in (repo / DIR / "initiative.md").read_text()
     
     
    -def position(repo, **wanted):
    -    """The index in log.jsonl of the first line holding every field of `wanted`, else None."""
    +def position(repo, node="p1", **wanted):
    +    """The index in log.jsonl of the first line of `node` holding every field of `wanted`, else None."""
         for number, line in enumerate(log_lines(repo)):
    -        if line.get("work-item") == "p1" and all(line.get(k) == v for k, v in wanted.items()):
    +        if line.get("work-item") == node and all(line.get(k) == v for k, v in wanted.items()):
                 return number
         return None
     
     
    -@then(parsers.re(r'a round of the kind (?P<kind>apply|formulate) was started for p1, given the answers? (?P<answers>.+)$'))
    -def apply_started(repo, context, kind, answers):
    -    found = rounds(repo, kind)
    +@then(parsers.re(r'a round of the kind (?P<kind>apply|formulate) was started for (?P<name>[pg]1), given the answers? (?P<answers>.+)$'))
    +def apply_started(repo, context, kind, name, answers):
    +    found = rounds(repo, kind, name)
         assert len(found) == 1, (found, context["done"].stdout, context["done"].stderr)
         for answer in quoted(answers):
             assert "Answer: %s" % answer in found[0]["brief"], (answer, found[0]["brief"])
     
     
    -@then("p1's transition to approved was made once the apply round had ended")
    -def approved_after_apply(repo, context):
    -    ended, moved = position(repo, stage="apply", event="end"), position(repo, after="approved")
    +@then(parsers.re(r"(?P<node>[pg]1)'s transition to approved was made once the apply round had ended$"))
    +def approved_after_apply(repo, context, node):
    +    ended, moved = position(repo, node, stage="apply", event="end"), position(repo, node, after="approved")
         assert ended is not None and moved is not None and ended < moved, (log_lines(repo), context["done"].stderr)
     
     
    diff --git a/tests/scenarios/test_design_model_check.py b/tests/scenarios/test_design_model_check.py
    index 7be00dcf..db9bce05 100644
    --- a/tests/scenarios/test_design_model_check.py
    +++ b/tests/scenarios/test_design_model_check.py
    @@ -18,6 +18,7 @@ from .design_model_check_reading import *
     from .design_model_check_records import *
     from .design_model_check_then import *
     from .design_model_check_trace import *
    +from .design_model_check_work import *
     
     scenarios("design-model-check.feature")
     
    diff --git a/tests/scripts/test_supervise_answers.py b/tests/scripts/test_supervise_answers.py
    index bb5f2093..35337dc1 100644
    --- a/tests/scripts/test_supervise_answers.py
    +++ b/tests/scripts/test_supervise_answers.py
    @@ -54,3 +54,18 @@ def test_a_reviewers_item_with_every_question_answered_and_no_verdict_from_this_
         assert run.moves == []
         assert run.written == []
         assert run.sessions == []
    +
    +
    +def test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case(tmp_path):
    +    from supervise_glossary import names_one
    +    (tmp_path / "spec").mkdir()
    +    (tmp_path / "spec" / "index.md").write_text("# Index\n\n## Glossary\n\n- **ledger**: a log. Not: journal.\n")
    +    (tmp_path / ".shop" / "work" / "i1").mkdir(parents=True)
    +    (tmp_path / ".shop" / "work" / "i1" / "g1.md").write_text("---\nkind: glossary-proposal\nstatus: drafted\n---\n")
    +    assert names_one(tmp_path, "Does it write the ledger?")
    +    assert names_one(tmp_path, "Is the Ledger kept?")
    +    assert names_one(tmp_path, "Does it wait for g1 to be applied?")
    +    assert not names_one(tmp_path, "Does the pledger own it?")
    +    assert not names_one(tmp_path, "Does it wait for g10?")
    +    assert not names_one(tmp_path, "Is a journal kept?")
    +    assert not names_one(tmp_path, "Which module owns the log?")
