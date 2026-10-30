# branch review of i54

Initiative: .shop/work/i54
Agent: bdd-branch-reviewer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Initiative branch: main
Base: a2a53b36c02b74d046b7a490d802403f3f1828a9
Head: c25a4c0d22c882d576e5b09f38c2b9f3335b74e1
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/branch-review
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/branch-review/.shop/scratch/branch-review
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/branch-review/.shop/scratch/branch-review/result.json

Review the initiative branch from its base. You start in your worktree: run every command from there and never change directory. Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` and `questions`.

Read:
- spec/capabilities/supervision.md
- spec/capabilities/work-queue.md
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
- design-decision/work-file-forms
- design-decision/plugin-takes-the-dependencies-it-needs
- design-decision/work-retry-reads-the-log
- design-decision/query-commands-answer-in-their-output
- design-decision/work-items-named-by-ids
- design-decision/the-ledger-is-tracked
- design-decision/work-list-and-work-show-replace-work-status
- .shop/work/i54/runs/w231/2-plan/plan.md
- .shop/work/i54/runs/w231/3-implement/report.md
- .shop/work/i54/runs/w231/4-review/findings.md
- .shop/work/i54/runs/w232/2-plan/plan.md
- .shop/work/i54/runs/w232/3-implement/report.md
- .shop/work/i54/runs/w232/4-review/findings.md
- .shop/work/i54/runs/w232/6-implement/report.md
- .shop/work/i54/runs/w232/7-review/findings.md

## Runs

Ran at: c25a4c0d22c882d576e5b09f38c2b9f3335b74e1

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w231 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 12%]
    ........................................................................ [ 19%]
    ........................................................................ [ 25%]
    ....x........x................................x..x..x................... [ 32%]
    ........................................................................ [ 38%]
    ....xx.x..xx.............................X...x.......................... [ 45%]
    ........................................................................ [ 51%]
    ........................................................................ [ 58%]
    ..................x.x......X............................................ [ 64%]
    ............X.........................................x.xx.............. [ 71%]
    ...............................................x...x...............uuuuu [ 77%]
    ...uu...uuuuuuuuuuu...................................................u. [ 82%]
    .......u...u.......uu....u...u...u...........u...u......u.u............. [ 88%]
    .........uu..u.u...............uu..u.uu......suuu.u.u...u...u.......uu.. [ 93%]
    ..u..u......u......u..u.u......................u.u...................... [ 98%]
    ..............                                                           [100%]
    =============================== warnings summary ===============================
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r209 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r210 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r211 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r214 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r215 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r216 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r218 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py: 303 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py: 303 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_that_redrafts_some_of_its_lines_leaves_the_proposal_with_the_requirement_ids_its_change_list_does_not_name - expected: accepted by w238, supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_glossaryproposal_that_redrafts_some_of_its_terms_leaves_the_proposal_with_the_terms_its_change_list_does_not_name - expected: accepted by w238, supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is withdrawn and its capability-proposal p2 is formulated-a request q1 kept in this context, whose asker is this context, names i1 and is delivered] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-no request kept in this context names i1] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-a request q1 kept in this context, whose asker is another context, names i1 and is accepted] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-a request q1 kept in this context, whose asker is this context, names i2 and is accepted] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[retry-failed-.shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed-green-i1's capability-proposal p1 is formulated-no request kept in this context names i1] - expected: accepted by work-queue, neither green nor withdrawn
    1088 passed, 1 skipped, 18 xfailed, 3 xpassed, 872 warnings, 56 subtests passed in 35.10s

### w231's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w231
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ...........uu..uuuuuuuuuuu.u...uuuu...........uu..u...u......u.u........ [ 27%]
    ....u...u..u.u..............u............u.............u.u.......u..u... [ 61%]
    .........u.............u.u..u....u.s...uu..u.u.uuuu...u.u..uu.....u..u.u [ 89%]
    u.....u................                                                  [100%]
    =============================== warnings summary ===============================
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r209 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r210 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r211 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r214 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r215 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r216 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r218 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_whose_change_list_names_another_capability_the_initiative_holds_a_capabilityproposal_for_adds_the_rounds_ids_for_that_capability_to_that_proposal_keeping_the_ids_it_holds
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_an_integrate_round_started_for_a_capabilityproposal_whose_change_list_names_another_capability_the_initiative_holds_a_capabilityproposal_for_adds_the_rounds_ids_for_that_capability_to_that_proposal_keeping_the_ids_it_holds
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    182 passed, 1 skipped, 258 warnings, 56 subtests passed in 6.91s

### w232's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w232
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ....uu.........u.uu.uuuuuuu..uuuuu.u......u....u..uu..u.u...u........... [ 27%]
    ....u..u..u.............u.....u............u.......u..uu....u........... [ 60%]
    .........uu.....u.....u..........u....u..uu...uuus.u..u...uu..u....uu.u. [ 88%]
    ..u..u...................                                                [100%]
    =============================== warnings summary ===============================
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r209 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r210 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r211 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r214 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r215 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r216 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    ../../../../.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.r218 - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    184 passed, 1 skipped, 256 warnings, 56 subtests passed in 4.59s

### tools check
Command: python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts/tools check --base a2a53b36c02b74d046b7a490d802403f3f1828a9
Exit code: 1
Output:
    == ruff ==
    .shop/work/i50/runs/supervision/2-apply/splice.py:1:5: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/2-apply/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/2-apply/splice.py:6:1: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/3-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/3-formulate/splice.py:3:8: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/3-formulate/splice.py:9:1: SIM115 Use a context manager for opening files
    .shop/work/i59/runs/i59/1-integrate/cmp.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i59/runs/i59/1-integrate/cmp.py:5:11: SIM115 Use a context manager for opening files
    .shop/work/i59/runs/i59/1-integrate/cmp.py:6:11: SIM115 Use a context manager for opening files
    .shop/work/i59/runs/i59/1-integrate/cmp.py:7:21: C402 Unnecessary generator (rewrite as a dict comprehension)
    .shop/work/i59/runs/i59/1-integrate/cmp.py:7:99: FURB167 [*] Use of regular expression alias `re.M`
    .shop/work/i60/runs/requests/23-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/29-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/29-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/29-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    .shop/work/i63/runs/supervision/1-gate/mk.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i63/runs/supervision/1-gate/mk.py:10:93: SIM115 Use a context manager for opening files
    tests/scenarios/supervision_integrate_steps.py:87:5: RUF059 Unpacked variable `commit` is never used
    tests/scenarios/supervision_proposal_steps.py:102:62: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_proposal_steps.py:137:94: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/test_supervision.py:14:1: I001 [*] Import block is un-sorted or un-formatted
    tests/scenarios/work_queue_list_steps.py:134:12: RUF015 Prefer `next(...)` over single element slice
    tests/scripts/stub_claude.py:208:51: FURB167 [*] Use of regular expression alias `re.M`
    tests/scripts/stub_claude.py:209:51: FURB167 [*] Use of regular expression alias `re.M`
    tests/scripts/test_supervise_answers.py:9:19: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    tests/scripts/test_supervise_answers.py:10:40: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
    Found 28 errors.
    [*] 10 fixable with `--fix` (3 unsafe fixes available with `--fix --unsafe-fixes`).
    == vulture ==
    clean
    == import-linter ==
    the project states no import contracts

### tools size
Command: python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts/tools size
Exit code: 0
Output:

### features deprecated
Command: python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts/features deprecated
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
Command: python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts/features bindings
Exit code: 0
Output:
    every binding names a scenario

## Commits

    c53a7c25e23bac68cae83b147c9dd66a2e6c6227 none work: start i55, fulfilling q21
    e98fc9bc6920b3c087107007edae5053502f0dcc none work: start i56, fulfilling q27
    ba786220582dd893205e255a321e988ef0c26fa7 none work: start i57, fulfilling q31
    ff10524ccd60ee2fedd13a4601e0fd5049868de1 none work: start i58, fulfilling q32
    57dc35330914792c994bc38e14a9c151c1e7e25c none work outcome: q25
    e91c783974a5afb57712882a8ca683250c903792 none work outcome: q25
    7c185789081ca62ca971d88f1a01d8b3e8bd6faf none work outcome: q25
    1f70d24b6e3163bf4854c9a154a6376cb3001205 none work turn: q25
    1fcce12cc8745c7973aa3116fc41767b98b88a0e none work: q25 intake round 2-intake ended
    7543cbbc2f4b2c90d6c832042a77e2787a5f0566 none work: i58 proposed -> started
    3ed81b19ccd65195e4db5fbf5ff209002f008314 none work note: i58
    1be0a48470dec20c7e820c3bc7d74dc12ac6b616 none work: i58 started -> started
    ebb680debff32cca1086d3d39481c49619f91650 none work: i53 proposed -> started
    1cfa0177d3472aa965c4dc87302fc2c5693e7870 none work note: i58
    140dc2f2312692c3766d74395fe02d40ca307189 none work: spec-integration drafted -> awaiting-answer
    ead359af0e058fdd23b4083cedc16f41cb058a61 none work note: i58
    da663c089ff3810f9d26295852cb32cf776a8407 none work: work-queue drafted -> awaiting-answer
    11569e6a84d2e34f21fe2781b75baff0f8f842f3 none work note: i58
    c4f5612c194d05ad12ff923476cb366fedb97798 none work: glossary drafted -> awaiting-answer
    a3671cc1843836a6fb401c2b456d7658cc6aace8 none work note: i53
    40fe05d273c98278279977b275f69d8a2473a24b none Merge branch 'round/i53-1-integrate'
    6919b92b9b612809da33478a2112de9f99b39ea1 none work: i53 started -> started
    be92994d289f34293c291d716d2524b54b6b942a none work: i56 proposed -> started
    428164a4be9f186abbada7614ef7176805f9732e none work note: i53
    51bbb7a6190c496eee64b7aa0a8c074f953e4f20 none work: spec-integration drafted -> awaiting-answer
    16c8ca7f4f4e4ddac774e7bff7c511c01c5d2d6a none work note: i56
    4549d3842d849b8915ebcb34aa4638f7e4d94bfe none Merge branch 'round/i56-1-integrate'
    920046658bda1e719fc7276ed7291d61cca7041c none work: i56 started -> started
    345633d283031194f80b132340e57bbd45566a0e none work: i57 proposed -> started
    8649577492c3f4721155d81f2c536b18f23e51cb none work note: i56
    9a96746d16b4e6b5938eac3c500299a4daa23166 none work note: i56
    d460f9c4f1aa495cc99c48a7bef4be667af1735c none work: requests drafted -> awaiting-answer
    74f5beda1dbc32979ff1f8974fe28a69c693ce34 none work note: i56
    f0c265a698ed608b808d2040f9c3f30516734dcd none work: supervision drafted -> awaiting-answer
    06322e7a755811b43751a278fea08f9a7a9b31f1 none work note: i56
    ff206e885390545766c8522ab77753f7f28a0aa6 none work: work-queue drafted -> awaiting-answer
    d7baddd8457b4ea2e005280f4096d25ba239baa4 none work note: i57
    426ef4ade6cb05622ffa3c2a85673fa3183e2646 none Merge branch 'round/i57-1-integrate'
    cb817a192f44cac70f90b0529d9166336d5dda45 none work: i57 started -> started
    78f23faec97e71aae35eab7be7b537a83508f84e none spec: supervision r173, approved 2026-10-28 (Q1 reading a, Q2 reading a, answered by the person)
    e4016b701c61791de5e2ab9c799d7c3250f0bf20 none work note: i50
    5adbcf40c28ce97091811433e2738b2764e52bbc none work note: i57
    506c83d8913882c9e4bda8c62e07a45a1d89177d none work: supervision awaiting-answer -> approved
    8c6d302c3b59205b7a5c7f6d5f51bbffb075cb33 none Merge branch 'round/backlog-1-gate'
    2a7db47fc40aa11fe9a27a820760195059990688 none work: backlog drafted -> awaiting-answer
    1417a6b476854213375d11df21a0313351e77c7f none work note: i57
    67363a6a9c4a8752a813269d8f56a5586e50ece6 none work note: i48
    480cb02482b3869c940ca5d3204eea867e2d4790 none work: migration-tools drafted -> awaiting-answer
    fba55a7cc013a98d367da25b79295e9bbe7858fa none Merge branch 'round/supervision-2-apply'
    6025932872bc79d8a2b9749915720f424a916750 none work: supervision awaiting-answer -> awaiting-answer
    73db354e12fb2c39adc861bb753bcf8ab7ddccec none work note: i57
    cf77bc276949f80d41fb6d01e7eff26ac3e1e002 none Merge branch 'round/glossary-1-gate'
    2554c1a3581b19165cd865846f505032bbe5d51b none work: glossary drafted -> awaiting-answer
    86104ff49056408531b4423b4fe696920b79062e none spec: supervision r180 replaces r93 (i49), approved by the person 2026-10-28 (r180 reading a)
    941efe363deffcff6a6170c177ebf516ec6b19db none work note: i49
    58489e774851bfeaad094db0fcf135f73bd453db none Merge branch 'round/supervision-2-apply'
    b897d9ccb404711ddeedbea715b29b4ead93415b none work: supervision awaiting-answer -> approved
    f6b68a250585f3e8f85eab396f8618123a1cfe81 none work note: i51
    f58c01918b5a69b42926ee665bdfd9be7245e146 none work: supervision awaiting-answer -> awaiting-answer
    2e01c61b4c994ac2052fad4d5d0ca0fd37f2b224 none work note: i47
    bb42f87ac25836ead9d807831471834d0ae43ed6 none work: requests awaiting-answer -> awaiting-answer
    0bc6e3cff01fc8f1c92b9ef0d9b6a6ddb6a3cf3d none work note: i52
    dd2145aba115a2f814359bf25411660b39c3b872 none work: supervision awaiting-answer -> awaiting-answer
    b65e5ba22143be2da3db838f7fdf1c1f983c9757 none work note: i45
    c4af595df53b5eed9ee00fff6251b20df291fe58 none work: requests awaiting-answer -> awaiting-answer
    3cad769cc105975b3207411a8e0041dfc787b6d4 none work: i55 proposed -> started
    a6599e865a600c9d6e16b80335aceb7602b7b33f none work note: i55
    ac23c4b92370f6328fbe8a6b579bfad69f802bbb none work: i55 started -> started
    49d8369f8d167ce75e5b44f1e2c498941c0bc922 none work: i54 proposed -> started
    23f5f9b5e4bf7b3c455e1a15d748906c46a96bdf none work note: i55
    ec060370be4e86b337d0280b8c0c642907b8dabb none work: requests drafted -> awaiting-answer
    6550e41561b6a2ce8023a5a258254e1f57972625 none work note: i55
    12f14ba22b23cff7531c5ed249bd15cb577f07b5 none work: supervision drafted -> awaiting-answer
    dbd21f8529de3e7d3f9c39017b44129c4c35b25c none work note: i55
    477d47d4ef26a75977281c072cb8ba8ff43b7414 none work: work-queue drafted -> awaiting-answer
    ffdbb842fbe54b1a597b6c8c6163da7963a60d67 none work note: i54
    c1aa3af965afea4c324cabc88b6d96448c0ae8fe none Merge branch 'round/i54-1-integrate'
    97c440d1644dce3357d6143523fbb2c4d38546ef none work: i54 started -> started
    0a02fc9a914a5df9e761d0ddd75853ede1e49ac3 none work note: i54
    985c02044ad2b9b5befbc5efe586c6edc4518470 none work: supervision drafted -> awaiting-answer
    9e93a1662b2ba5794bdd4c60db4a0987aa7af7f5 none work note: i54
    afb6841af323e58a4857213db1cecaedd1dc2301 none work: work-queue drafted -> awaiting-answer
    e4e584453aa8532cd9103525d853e35fa3accdc1 none features: supervision r173 scenario
    505ec02dbd30d4a5347f1a6317f91ae91622eeaf none work note: i50
    2ef78061d78fd5e2e5c148c78aca99be39db8781 none Merge branch 'round/supervision-3-formulate'
    a50e1b35f6c9e96385de16a91962fc23a87ea0df none work: supervision approved -> formulated
    829bd273887ab195824aaf4bcfee1bb1270cc234 none work add: i50/w228 drafted
    2bd22e3357ca162131942ba9dcdc1d970914a818 none work: w228 drafted -> researched
    09c07229e1ee99139fc32210e1c715a0dd827739 none work: w228 researched -> planned
    5773b8b85276ab523354c73adbe1a530d542c19e none work: w228 planned -> ready
    c7a1994d68a10d82357753b8530c1684e0d529a6 none work: w228 ready -> claimed
    55eccc0c8f0f492008cfafb696a87f6e237d72ff none work note: i48
    602a958427bd5a8d1c54ecb17ebb20f81c313787 none Merge branch 'round/supervision-3-integrate'
    38eb0244f4e9a744818c02783a04fb64c90d24db none work: supervision awaiting-answer -> drafted
    c7a92ebe6d42fad42a7cf34f3bd4e9e13b9ab90b none work note: i48
    257259199a850db198ec4bc89082243548011c7b none work: supervision drafted -> awaiting-answer
    a807b5b7c62f4a81430a33f6ddb8ce5ec3c6662d none work run: a glossary gate with no question asks for approval of the terms (r173)
    6ce694525b7a095bc03390c7c4d8e97ec7c5efdc none features: supervision r180 scenario, r93 scenario deprecated for removal (i49)
    4ee07b08020efb210b047cd8d30d0573c4d6b929 none work note: i49
    a42dfc6383be6732d6c2639b30a3341860a6782b none work: w228 claimed -> done
    7491a67ea26c8d8c934eff68b72db264237e506c none Merge branch 'round/supervision-3-formulate'
    32412000acabb86f2fb0f2eb31741924e21ac905 none work: supervision approved -> formulated
    683178990d5caefd9517d6d619455c86c49f2041 none work add: i49/w229 drafted
    837a59ee5d8983ada6ef3e40ab3ad920a48f4e33 none work: w228 done -> green
    6cf988e130c307462e5957a4695417b2c131801b none work: w229 drafted -> researched
    7425183638523e6f0839751b4d8f756dcc3df940 none work: w229 researched -> planned
    1c86af3d0a9c3c5fe9624290d01707f67c3b5892 none work: w229 planned -> ready
    2dcd11ce8b749545f741db207a0a9f79fa60e5cb none work note: i51
    2357b0434ca0d9334ea3247c9713db6cc137424c none work: w229 ready -> claimed
    23744d407840ea34e5928642a118b4ae2699f6c9 none Merge branch 'round/supervision-3-integrate'
    15c35fcb638d36028bdcbcaf1ca6550f9a536830 none work: supervision awaiting-answer -> drafted
    57661882c1764c736abfd34b094f980c9d2cb083 none work note: i51
    df68b98adee30fcdbe2adbe5f5861b900f8e77ee none work: supervision drafted -> awaiting-answer
    bf55e7e7f855a6fb5204af131334b9334ff0ea3f none work: w229 claimed -> awaiting-answer
    a746612bbe722527d174a437d91bd5ac9b2d8330 none branch review 1 of i50
    257bb8b31d1909f9c2847781b310c93419b06a7e none work note: i47
    bdc3f63598c87fc772c898a92ab1c9862a05434d none Merge branch 'round/requests-3-integrate'
    68aec4ac5ce50d98857a12e7200f6a491d9708b9 none work: requests awaiting-answer -> drafted
    fb5fe1321db9a94a03809763b0ec1eb116e267d7 none work note: i47
    ab2b6f1f87abc228154462c8b886109896324118 none work: requests drafted -> awaiting-answer
    ace6a93e28e190af49d17ad960798c11134d2376 none work: i50 measurement and analysis record
    6f298c54004ac0fbf750b6698c9bc9dbb3ac475a none work: i50 started -> done
    ffdc6771f4c2b2bb951fdddb9e370914cdfabfc5 none work note: i52
    6a413595abb52c6a7f95d17002eb58f96908613e none Merge branch 'round/supervision-3-integrate'
    9874a34d114ea1f88aecb7e44b20fafa7af0ce8e none work: supervision awaiting-answer -> drafted
    babb06ef95150bf95cd18cc82c3158d3ae6fce1b none work note: i52
    ce07b9940ca12fca2a42c58f1cacc1bf6d4224bf none work: supervision drafted -> awaiting-answer
    aa631ea79b4c8f7fcea8797c6a6ab50f5a397c22 none work note: i45
    59a38277259ff2f061a241c9bc202d0b3101f832 none Merge branch 'round/requests-3-integrate'
    b3bfdbbf4581013dda22dd5bf409d545b25ab54c none work: requests awaiting-answer -> drafted
    d9fee89cd63382b38445df009665a3b90913e586 none work note: i45
    3ffee76b0a7a611ddbd93146fb7b0809ab426f54 none work: requests drafted -> awaiting-answer
    4e3d4fd98250888d9590a8dc26febf6a9b64f541 none work note: i47
    6c4f1eafc10e95180d40514962255f0e3424a7c7 none Merge branch 'round/supervision-2-apply'
    3303662b2ca7c5848ba71483f4b43bf6b0585507 none work: supervision awaiting-answer -> awaiting-answer
    aa4c9df0d8bc01f9091479e18e515b4aaa4e8bc7 none work note: i52
    76358f46ccc33d4e51e56442cfc53ec50c4beebf none work: work-queue awaiting-answer -> awaiting-answer
    d27c27d3b7d86c2d37d61dd9e622e81ec6a8f400 none spec-consistency: retire r5, add r28 (a changed line is retired, its replacement given a new id)
    9b2d58d76dfe126dca90e5216ecf4b23a17aac65 none work note: i45
    5d5c73db7554b45fba794df7e17ac3004ad04f66 none work: spec-consistency awaiting-answer -> approved
    ec7cc0d7eca218628315222cf8f13223dfaa8f4b none work note: i47
    aaad66d256081f85db7a35094b63a867a2a4e161 none work: supervision awaiting-answer -> drafted
    f01c8e29a32d5cf9960d13e9c79b8a74eb926a70 none work note: i47
    a8d356e991fffc42098c82350072f6f0fd2cd351 none work: supervision drafted -> awaiting-answer
    44edf99fc764510c09b331d8a4e3ec756ae10608 none work note: i52
    a74a211cf284ef2575917bd765122964aba8a5c8 none Merge branch 'round/work-queue-3-integrate'
    15cc1c72380923c9050e150e363a477c8e5191d8 none work: work-queue awaiting-answer -> drafted
    3e1ff498cc35245521fc8679755bcc53afff621e none work note: i52
    46b22c394c9b9e36344590b9937d998a7e4a3691 none work: work-queue drafted -> awaiting-answer
    a3da368cccbf05fc0e7d6b21b40a5c07dcbac98a none features: spec-consistency formulated (r1-r8, r10, r21-r28; r9, r11 asked)
    4b67847ae3b1898cec2311ecc7f12bb4bf79db96 none work note: i45
    277302a9d519076318224f16eef69207eb7342a8 none Merge branch 'round/spec-consistency-3-formulate'
    2061fb575dfcbd90e7efe741566185d48420d854 none work: spec-consistency approved -> awaiting-answer
    da62802ac0c5d013cbe20da4ddfd21e2be61bf7e none work note: i45
    e8afebd10defcb6f059f915295a28c035d89c7eb none work: spec-integration awaiting-answer -> awaiting-answer
    b62e0d1954a940a7182e1b4b681392ef021cc34c none work note: i45
    0e402fd0a630d2aa4521bb728ed9d97f22c74742 none work: spec-integration awaiting-answer -> drafted
    ebed879da55c78913963f60311d7cb952b05d3f1 none work note: i45
    69cd0c47872c21c5811964e1891a3bf08dca688f none work: spec-integration drafted -> awaiting-answer
    33c465bb11a26265fc254441c34183df1139fa20 none work note: i45
    3582ba4a86af2632aa3142f48dcbaecb3248067e none work: glossary drafted -> awaiting-answer
    c6068c50ad6dea6c8a1315372887a36fd5a3e693 none work answer: supervision
    a0f959c2fada90be7c5f7bd169d3ba4109559c8b none work request: q39
    3be48327e94e2ec17ea63d9334f33dd184b148e0 none work: start i59, fulfilling q25
    848c4864bbcb366c152be8c6fb8ff3cc6e37508a none work outcome: q39
    edc5c1d2a526f015ac777c3f5c1a0d973c0c8a03 none work outcome: q39
    3796fed5d8310e6e36093791bd513a52b0ab5c34 none work outcome: q39
    ed38dda5f36f7b21a5b3284c93c3dba66817453d none work outcome: q39
    50fa8f22158d3610e757540eff614d35300dcaf6 none work outcome: q39
    33a8a14b78e352461d56b6f6c8c61ba0477f2be0 none work turn: q39
    1f8fc9c491373a902acb65e83b88471d7327e2ee none work: q39 intake round 1-intake ended
    c0def062bd32c26622ae5e056ddc37c4be5fc681 none work: i59 proposed -> started
    6015ec9f148e5fa73f8209f503e34ed5e85f7012 none work note: i59
    393cdfa09ce475552069413aa3021e896675b483 none work: i59 started -> started
    cc52ef1f8ea777bbed9234c214599ec1af02e630 none work note: i51
    c89203dbdbe175421182622287c6dc21db181064 none work: supervision awaiting-answer -> awaiting-answer
    9a45b1a3e2d89bfe475eb91279ba137ad20a32c2 none work note: i59
    1a165bcc9d5cc53f8a82aeec3bcea062df5193ae none Merge branch 'round/analysis-tools-1-gate'
    a82f108ad5651c8f2f0fb7509fa73578d104352a none work: analysis-tools drafted -> awaiting-answer
    c0eef86357f97b2eea5cfc090490dcaa490dabc3 none work note: i59
    1b208485ee88ef8e8b0f8d1f15b164c4a33b5922 none work: batch-measurement drafted -> awaiting-answer
    4d5da17645dbcfc6ca9522d9222e3330cd42dfdd none work note: i59
    c3c352c00f4cec5b5e47616dc46d54546b48b508 none work: delivery drafted -> awaiting-answer
    bdaca99b62148ff11e87f44dbd1c0cedba3236d4 none work note: i59
    b82f2e2965d5d02a7b1ba21d75a0b7e91176eea0 none work: design-model-check drafted -> awaiting-answer
    39d800983cfcee1b1785e5d58afcf382efc75590 none work note: i51
    2bec4b00c30877dcd2c2b1b23534d7ca5a9d5e9d none Merge branch 'round/supervision-6-integrate'
    52bac6ba6dfbb92d7fc2d9889dfd0e9fec5f0d0b none work: supervision awaiting-answer -> drafted
    abf112202c4d0842f65cb9eca21bb13735c81542 none work note: i51
    8dd6ea47d2cff43be03b462c4cb2b345cdfdd101 none work note: i59
    0834337e285f8d671d65fd27841404e3fe7b2631 none work: supervision drafted -> awaiting-answer
    ca4fdaf6ddf96c71af2787e77bd59fa142babb82 none Merge branch 'round/feature-file-tools-1-gate'
    427f8a115ab4c4a48cd5ec44b23d7dc7049d0524 none work: feature-file-tools drafted -> awaiting-answer
    af949c5f3c47a054b358b2519d3d788e65982542 none work note: i59
    ab47c22215738ad6f7fb6d4344396cdff722dac1 none work: migration-tools drafted -> awaiting-answer
    e1188d27d21e8e2722f70dd819bf49fe1b9089f2 none work note: i59
    f700ac037f811df54411b600960a7528b9369cbc none work: role-boundaries drafted -> awaiting-answer
    baa835a2f3502a130c3dcf8cb2b53cee11ef57f4 none work note: i59
    c2a55f8abba5448da0d5ce104ff4dfc7ef6bbfc8 none work: supervision drafted -> awaiting-answer
    4236abbeed7f8c9f90759c9817292dec6eb8c283 none work note: i59
    f77af623c6ffd248efa0018c7d6b63ab2b2858ea none work: work-queue drafted -> awaiting-answer
    49a9e231ec241da2355a8eb12068b94777ee549f none work note: i59
    a8baeeae3f86085faf4d9f7d15e2b3de955749a9 none work: glossary drafted -> awaiting-answer
    e8a62e35fb439d11193922d8dafbb43d8c30f936 none work answer: supervision
    4c5eca99cb65a52b149916f35e32e8c81963c7b4 none work note: i51
    72bc565f2f86fb1425c367c840c90150de178911 none work: supervision awaiting-answer -> awaiting-answer
    1dcd7013a21c161d80a4c20bcb4f17bfb04b7c6b none work note: i51
    d60dc6b440006f85645cc601fd9e714c51ca5760 none work: supervision awaiting-answer -> drafted
    7b2463b6c90de15d19bac15b6daec978bfed8ada none work note: i51
    e2b6f148c3189e1c213c8a5a46868a03efebfd10 none work: supervision drafted -> awaiting-answer
    00bbf612ab5068ed0856270532c290e998377f67 none work note: i51
    d9f5c2ebbd1b6f92aec858cee7e96be94956f131 none work: glossary drafted -> awaiting-answer
    407c74387b5a94154c958e7a63aaf84585ed0459 none work answer: supervision
    2c74c3a66092a5dd39986d640fe79ec3147ac1f4 none spec: supervision r209, r210 replace r162, r163
    8517d823bcd6b3e6d7182033ef90d0b2469d9f91 none work note: i51
    e59e4883fba0e7967f24a2501e0c47c3bbc380ce none work: supervision awaiting-answer -> approved
    1a3447406da528852812650ce4b818df3c9a4b2c none work note: i51
    6c5518bd490a146726ac0ab7d87cdfff72bd5fb9 none work: supervision approved -> drafted
    8e621bcf91ff9a378c61366c3a18f1658ef979c9 none work note: i51
    d55c6832a1c7e3f24161db2b5d94eb77f0ca3df5 none work: supervision drafted -> awaiting-answer
    73758cad8cb4248f6e2560f64de218383d8c6dbf none work: i51 hand repair: supervision back to approved with r209 r210 (applied 2c74c3a6), empty glossary-proposal withdrawn
    d528b7a9635aa948830d488335a12797870fcb4a none work note: i51
    20cca0c80d5b9646aa0a0c029b46bc09ed091bd6 none work request: q40
    af49d7ff96e078bfaf489e88f277d492d56bd1d4 none Formulate supervision r209, r210; deprecate r162, r163 scenarios
    0eb49c95a1f27ebbfc20cdb5a8cbc25db439e8b6 none work note: i51
    8e3926dabe48d0fc6ad9caae74f0f92ad1dd88db none work: supervision approved -> awaiting-answer
    8f55b7fc1ec646a9c3298d88ad24370d3fccf5f5 none work answer: supervision
    508cc4293bef258d5ce9837979efceac9cf99a4b none work answer: supervision
    1ff52140b39f1134c6fabb3b067745fcf6bf09fe none work note: i51
    c2973b4548490d2247849fa115b6dfffc356a9f3 none work: supervision awaiting-answer -> formulated
    67f24af1f7ab9554a3317141abaf8452964a3973 none work add: i51/w230 drafted
    03955071c395ec4c07c050a680dde2d700bef50a none work: w230 drafted -> researched
    93b6fdaf0f89e47a75cad5c6dd7818ddfbd010ad none work: w230 researched -> planned
    401384a7311283eb2ec30de685cc9c77eab08fdf none work: w230 planned -> ready
    d3ed8a916d2a985206c4cb9dea907a4eda553c82 none work: w230 ready -> claimed
    365932d67f8f3697553f4a5831644afd51737562 none work: w230 claimed -> awaiting-answer
    085d138371ba6409464cb40a1cd09f6739a930fd none work answer: w230 awaiting-answer -> ready
    e9da7125ceacaf723c8258f0a332b9de04ce139f none work request: q41
    1db40f6e21cbfcddee79190e606e2a4301c9c749 none work: w230 ready -> claimed
    998966626eaac9e687ab55d5463ca3600d54a9b3 none supervision: a question outside a glossary-proposal goes to a session whatever words it names (r209, r210)
    3eb7a99946cc63db26d075413ac428c2e15dbe72 none work: w230 claimed -> done
    4380a2a6686f486490fdf290b671cb822fe83c25 none work: w230 done -> awaiting-answer
    9235b274f0d45ef13b237ad8058b387bd3ec76c8 none work answer: w230 awaiting-answer -> done
    eadc07902810f1f79cb7ad2cba621fbf1635c787 none work: w230 done -> green
    9e8c48dc06f7323083ec782361090c19fbefac4b none branch review 1 of i51
    e4b65fa5a353aef723820b5bd4cca4fd431d89fb none work: i51 measurement and analysis record
    c8d0d35ee0dd2b30f5b3c58280b130ca2ce3cf20 none work: i51 started -> done
    ae85edd3a2ce3488f4d930ac5814845eea5e6178 none work: start i60, fulfilling q39
    ad289756e8a7ce3952da11da2d1efcacf36d40b3 none work outcome: q40
    ce0d059f54aaaaa167ea230e4c4adbcb5b3085f4 none work outcome: q40
    984891a33dc321a9f12f42477a5e7620bbfed301 none work outcome: q40
    02ae10846bafc40288013d35352c77b9476d24e1 none work outcome: q40
    e7e95b3a1484057d38c700a283f8891e9bcb99a3 none work turn: q40
    af69e589bfb94bbe55ab4a0eb64167e4292f9a1f none work: q40 intake round 1-intake ended
    0b0c66e09e4d6804c26d30776dd90ff82c345f16 none work outcome: q41
    5a78ff45d9375136546abd616347c8ac0f2b05e5 none work outcome: q41
    149cdb9cdfb9b59785ea6a755e9a0d8f92e569a3 none work turn: q41
    cfecb433b85bc926da289f30aa4f5485b02e36a2 none work: q41 intake round 1-intake ended
    08e1fdea9978b2c12ab1ee59d0bd7a9abbe50448 none work: i60 proposed -> started
    02f08c2342038b56beb77c5005d994fb424b6c91 none work: supervision awaiting-answer -> awaiting-answer
    9ca35c57f70ce9c1bb9e6351d4ecb2ec867c2648 none work: requests awaiting-answer -> awaiting-answer
    facd69ef5ccafacd06e954e0a9268b4fb27ba697 none work: work-queue awaiting-answer -> awaiting-answer
    77e2522de180db778c6e339c8d5c01ab591880de none work: requests awaiting-answer -> awaiting-answer
    2910b26aafaf2454549b9a9ce28315226b86eb36 none work: requests awaiting-answer -> awaiting-answer
    6580ec263a092823919bca36b4e514f6902e2903 none work: requests awaiting-answer -> awaiting-answer
    95b2e536ff2d5c51eeae5943e624e9e6ec841b62 none work: requests awaiting-answer -> awaiting-answer
    e2127d8e5065bbb8fe2c09e284b21f68249656da none work: requests awaiting-answer -> awaiting-answer
    7219d44dc1fee63c4af7d67ef94e531b939aa7b4 none work: requests awaiting-answer -> awaiting-answer
    59a901fcd797389d6ac6ae7b8b64283caff2c1ef none work: requests awaiting-answer -> awaiting-answer
    4abe2c0b27df19ed9dbe4c3937c68d8fb8fe1f20 none work: requests awaiting-answer -> awaiting-answer
    f98897104d712652e04a79910c35c24c84fb57ed none work: requests awaiting-answer -> awaiting-answer
    07a3316befcc215756ffecc7a64f0fa0b521cb25 none work: supervision awaiting-answer -> awaiting-answer
    3821c6c499efd08ea4f9fde040fa06f9ac3e598c none work: supervision awaiting-answer -> awaiting-answer
    213b5b8ee7c69ed1d2c110e2bda8fc30a26797f1 none work note: i60
    6a25ebd73036b90d3110a54eea30069aebe6c73a none work: supervision awaiting-answer -> awaiting-answer
    be2b2e2700b05c71029d25e4525efa15f59347ef none Merge branch 'round/i60-1-integrate'
    3075f560cc62e8b7ddd82a636d8044cb271b4054 none work: i60 started -> started
    4b70fa06ad36571539432d416fd20c79180a654f none work: supervision awaiting-answer -> awaiting-answer
    555e5e51f5c47684efc88356530bf33ba1a3724d none work: work-queue awaiting-answer -> awaiting-answer
    3bc1804985d75bc02027e76cb865fc97cc98e816 none work note: i60
    926b84991f2ec2748758b8fe9adf7b16120b1c7a none Merge branch 'round/requests-1-gate'
    3eb6412eed7baa679417b916afaceeacb0d75873 none work: requests drafted -> awaiting-answer
    b1849b94f302d152ce4320631479ce7450b6a8df none work: work-queue awaiting-answer -> awaiting-answer
    ec944d154fd6cd3353a6fdfdc916ebc69d46575d none spec: supervision r187, approved 2026-10-29 under the person's delegation of 2026-10-27 (i54)
    bd12cddb4e59055cb724de1bfdf2768d4218f7e5 none work note: i54
    3a7e7695aff2b09b724942bf8c81bf7b8d883445 none work note: i60
    1980fcc013c727b0ec68807a051082d4c1c84f4b none Merge branch 'round/supervision-1-gate'
    ce5d751c3c2f92440cd9913933a4c3ff3dd5adbb none work: supervision drafted -> awaiting-answer
    3fc55100ff69c2a0fae571043ef5d0e91f433f67 none Merge branch 'round/supervision-3-apply'
    f0321b5fdd78faeb8cce4289cf0eeab258df93b2 none work: supervision awaiting-answer -> approved
    deda9fa6e1f1969073ec0b8d29673ad94bc7dd7d none spec: requests (i55), lines approved 2026-10-29 under the person's delegation of 2026-10-27 ("I'm delegating this to you. Please get the new version delivered without involving me."); adds requests#r50, r51, r52, r53, r54, r55, r56, r57, r58, supervision#r184, r185, r186, work-queue#r47; changes none; removes requests#r13, r34, r39, r41, r43
    782b76d99fe84a054690328373318c60f2601ae3 none work note: i55
    f8c0a26f9c02ec089cdef21a4125401724e2cc98 none work: requests awaiting-answer -> approved
    bb2caaeb966336119a0f38ac00f54938a0d7b87a none Formulate supervision r187: one scenario
    6f1b593130f1e92a96412955e16b5a5cff06ccdb none work note: i54
    11726fc2486da952d08aff09a91d58ec20a0510f none work: supervision approved -> formulated
    eb2eb87f9badf1bfd9c976da20a939c282c91401 none work note: i55
    1d645008ee2d5bc85b07bb5d1440abc7582b3ac1 none work: requests approved -> drafted
    b6e06e6469d074319b55e8983fbfaee460fb306c none work note: i55
    3e4b438a6ed6156b82e32343bb317ec8084d722e none work: requests drafted -> awaiting-answer
    054a77b059f3af15a5b0c1e0e69bf29d36bf20ce none work note: i54
    346c2612743856e9ff6274c8566b18cf7046dee3 none Merge branch 'round/work-queue-3-apply'
    5a4b691fceb397189834e9ec1ff374adc5f77de3 none work: work-queue awaiting-answer -> awaiting-answer
    af1a393ef9ab4c23c8dbb05823a996156c2bfef3 none work note: i55
    79e4b21015d3586990030d54f5bedaa518605724 none work: supervision awaiting-answer -> awaiting-answer
    e3655ce638aea623a283cff6c2ed36fd3c61d3c2 none work note: i54
    59256f4c5dbbce25355cbff4bb3958f9d6aa2590 none work: work-queue awaiting-answer -> drafted
    b8f38ec72e165e3fc57dd2cbb94c0a862f1f3722 none work note: i54
    147ad5896b0a6a85a85eeeaa5e6bf6fb7b85ecd7 none work: work-queue drafted -> awaiting-answer
    6e55ddd3e56305a651df3afacda352dbecb4093d w231 work add: i54/w231 drafted
    cd273ba8661f7baf4979ec5038164355c6247c08 none work note: i55
    82832c5ee10137d4a86bb08e7d27d401d757a010 w231 work: w231 drafted -> researched
    2539c8e48ce33611cfaa2a769dd63a580d49673e none Merge branch 'round/supervision-7-integrate'
    5406cde312aa913b78e62a7d2a0a8fd18d12acc4 none work: supervision awaiting-answer -> drafted
    509b51d888fa21cd345e5d85d56c247e57dc075c none work note: i55
    05ebb9c5acd76fa2d120fb0b94ce9eb604d03518 none work: supervision drafted -> awaiting-answer
    56f6efb69af5b66c1db12aaffdf6c740182ab975 w231 work: w231 researched -> planned
    f5f6671bbe39abbcee3b0b90d31137f15c8aec38 w231 work: w231 planned -> ready
    21c232e1e8a67571b05e140ee64189ef17e890da none work note: i55
    156d2b2bcb9b5768421dc30920d2c49d124f93f1 w231 work: w231 ready -> claimed
    1be86700c7de7d3ac2e9b67542a955101890f252 none Merge branch 'round/work-queue-4-apply'
    66f43883b037f8e316322d0fe4fffa188a9caa15 none work: work-queue awaiting-answer -> awaiting-answer
    afc4aa728368e474832b86eba156e1002466367f w231 supervision r187: steps for an integrate round merging ids into another capability's proposal
    6bf4834a79422c2dd3f86331b50eae45a82d1989 none work note: i55
    3cc54654a998740c9666398cea512e52a17a4116 w231 work: w231 claimed -> done
    0b981a195f7ee670079618cceb933b286a124ca0 none Merge branch 'round/work-queue-5-integrate'
    7ecda6c0cacc267fee3277872835369035977d44 none work: work-queue awaiting-answer -> drafted
    87d07c300e08743f954111d412e83a9960b82f95 none work: work-queue drafted -> awaiting-answer
    df18eba01e1e0114c59816bc0efd49be8856bc95 none work note: i55
    e6176a783eef5e4aae35c5f078c77d98bf77d016 none work: glossary drafted -> awaiting-answer
    eb1a30ac52528d23385846ad51c1947066590847 w231 work: w231 done -> green
    850ce9d3667c427dfdb88b3eb2b380edb1a0cef8 none branch review 1 of i54
    35f74d76f826d7379661b138e039589813a82db3 none work: i54 measurement and analysis record
    2b30178d6a0c7fa1a9a62466e6f99ddcaada2805 none work: start i61, fulfilling q40
    955ad466c30a8e870af65b406cdd4b241699f24e none work: start i62, fulfilling q41
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
    911cac0f2bb6d6c963950fceee664ffa892b0de1 w232 work add: i54/w232 drafted
    77390a137b114bc21d6678c02f6aaf522f4208c7 none work note: i55
    e704d1f8f311021ce31a849ccbe5ae9faa3a171a none Merge branch 'round/requests-17-integrate'
    b35a33b07de9a8da709a19b71cea84f220d42d5d none work: requests approved -> drafted
    d85af1964db06f8763dc75a71cb19a5443cb8b1f none work note: i55
    1ec90b32b061096f8ac9e25113a274f6f6ce1886 none work: requests drafted -> awaiting-answer
    63e2202657ca3fad91c9128d86c2a1e89df404d1 w232 work: w232 drafted -> researched
    7d69212bbce334baefa651983d0e5467c72d8493 none work note: i55
    0abdbc0b7af8a1a0cbc6e573e076154642c54c68 none Merge branch 'round/supervision-10-apply'
    5ff00cb425e61ef0b7f96e7683b903ff27f55e73 none work: supervision awaiting-answer -> awaiting-answer
    ddcb3e7322ee4a2d6af844d9f108b3f7ba5510a1 none spec: work-queue r62 replaces r23 (r23 retired), approved 2026-10-29 under the person's delegation of 2026-10-27 ("I'm delegating this to you. Please get the new version delivered without involving me."); supervision r213 already applied; draft's r59 renumbered r62 as r59 is taken
    01ae9093ceb152f03b30b0341a3da259f3b5ac6b none work note: i55
    5d64a25bbbb792148c0acf895ef637e3f027ec5d none work: work-queue awaiting-answer -> approved
    3fe3a53843196fdcb59b29a9dcf535a180694b42 w232 work: w232 researched -> planned
    a2c10dd22f88581bb2173fab75300f8cee831d5b w232 work: w232 planned -> ready
    7b1e1e12fe3a273f0ffcdad3a73d642d5031661c w232 work: w232 ready -> claimed
    a5d6b59bd3a1bd818ca314a4bd9cb91f20e6bc2b w232 work show of a request prints its turn, line outcomes, questions, answers and resolution (r59)
    19c0bc4d311658bba9264df458d46c3906019b46 none features: work-queue r62 formulated; r23's two scenarios deprecated for it
    13ebc3c6b7bf07422948e0593692709e2d1dbe8f none work note: i55
    14e01547b29352ee59301d56fc4cb3350dc68dea w232 work: w232 claimed -> done
    e27f603d095baf0711092e57f6a52c67b902848c none Merge branch 'round/work-queue-9-formulate'
    248f031b7aa5150b7d960c8d8dd95b4ff2803077 none work: work-queue approved -> awaiting-answer
    069d133de7725d093c8d65680106f7161c8b7640 w232 work: w232 done -> awaiting-answer
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
    74c02e0ce0c416ce42eecdbc0976b93739bd4d4f w232 work: w232 awaiting-answer -> awaiting-answer
    9d5b527a5f493e6ed6deab92daacf85b10f4dde1 w232 work: w232 awaiting-answer -> ready
    0f44ddf19b9577763453ccb057b19a98ee3fc413 none work: w229 awaiting-answer -> awaiting-answer
    11619129e884a2450f083d31b2eb80b8db3e2217 none work: requests awaiting-answer -> awaiting-answer
    e49440e22caf8f4c579102a0085fa19db38103dd w232 work: w232 ready -> claimed
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
    cb26926247a31f6adf5067b10507f6e8b7603d77 w232 work show of a request lists every line, an unsettled one as unsettled (r59)
    ae9065779007e7fb7147d89b6389d24ec5bc1916 none spec: requests r59, a line naming an implementation detail or an unknown word is refused (approved 2026-10-30 under the person's 2026-10-29 delegation; Q1 A, Q7 A, Q12 A)
    1748d85081b397bdede60d2625c67c763175bc7f none work note: i45
    20334492877707c12556218000af8b4677722666 w232 work: w232 claimed -> done
    5beff3da36278ac526aa8dbe44d9955a817a876f none Merge branch 'round/requests-6-apply'
    65cb6a6133766137520646833abd8e7f2a9d61bd none work: requests awaiting-answer -> approved
    cf607ca51f70e6c63a0f6ae7e45a6422b45e1919 none branch review 6 of i60
    c25a4c0d22c882d576e5b09f38c2b9f3335b74e1 w232 work: w232 done -> green

## Change

The change from a2a53b36c02b74d046b7a490d802403f3f1828a9 to c25a4c0d22c882d576e5b09f38c2b9f3335b74e1, without the workflow's own files:

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
    index b76d999a..b87e478e 100644
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
    diff --git a/features/spec-consistency.feature b/features/spec-consistency.feature
    new file mode 100644
    index 00000000..9a8888bc
    --- /dev/null
    +++ b/features/spec-consistency.feature
    @@ -0,0 +1,187 @@
    +# formulated from spec/capabilities/spec-consistency.md
    +Feature: Spec consistency
    +  Narrator: the person keeping a spec
    +
    +  @r1
    +  Scenario: when the person asks for a consistency pass, model check runs before anything else and its v_t rows are findings
    +    Pins that the pass starts from what model check already finds, and that those rows reach the person as findings rather than being left out.
    +    Given model check gives a v_t1 row naming r3 and a v_t2 row naming r7
    +    When the person asks for a consistency pass
    +    Then checking-spec-consistency runs model check before it does anything else
    +    And the pass gives the v_t1 row naming r3 as a finding
    +    And the pass gives the v_t2 row naming r7 as a finding
    +
    +  @r2
    +  Scenario: when the pass starts, it says how many spec-checker dispatches it will make before it dispatches any
    +    Pins that the person knows the size of the pass, one dispatch a capability and one for the whole context, before any dispatch starts.
    +    Given a spec with the capabilities orders, payments and refunds
    +    When the person asks for a consistency pass
    +    Then checking-spec-consistency says it will make 4 spec-checker dispatches
    +    And it says so before it dispatches any spec-checker
    +
    +  @r3
    +  Scenario: a spec-checker that is dispatched reads only spec/ and features/, never the source
    +    Pins that a spec-checker judges the spec blind to the code.
    +    Given a repository with files under spec/, features/ and scripts/
    +    When checking-spec-consistency dispatches a spec-checker
    +    Then the spec-checker reads files under spec/ and features/
    +    And the spec-checker reads no file outside spec/ and features/
    +
    +  @r4
    +  Scenario: when a pass in findings mode ends, it has changed nothing but one findings file whose findings name their ids
    +    Pins that findings mode leaves the spec and the feature files as they were, with every finding written in one file and traceable to its ids.
    +    Given a consistency pass in findings mode
    +    And the spec-checkers find a scenario of r3 that shows a status no line asks for
    +    When the pass ends
    +    Then the only file the pass changed is one findings file
    +    And each finding in that file names its ids
    +
    +  @r28
    +  Scenario: in fix mode, the pass first proposes a glossary entry for a term cluster and puts it with the line changes that apply it through one gate pass
    +    Pins that a word used for one thing under several names is settled at the gate as one glossary entry, its avoided words and the lines it rewrites together, with every changed line retired and replaced under a new id.
    +    Given fix mode is asked for
    +    And the lines r3 and r7 say cart and the line r5 says basket, for one thing
    +    When checking-spec-consistency starts fixing
    +    Then it proposes a glossary entry basket with the Not: word cart
    +    And it proposes the line changes that say basket in r3 and r7, with r3 and r7 retired and their replacements given new ids
    +    And it puts the entry and those line changes through one gate pass for the term basket
    +    And it does so before it rewords any scenario or asks the person any other question
    +
    +  @r6
    +  Scenario: in fix mode, once the terms are settled, a scenario using an avoided word is reworded to its line with no further approval
    +    Pins that a scenario's wording follows its settled line through formulation's small-change path, without the person approving it again.
    +    Given fix mode is asked for
    +    And the glossary entry basket with the Not: word cart is settled at the gate
    +    And the line r9 says basket
    +    And the scenario of r9 says cart
    +    When the terms are settled
    +    Then checking-spec-consistency has the scenario of r9 reworded to say basket, as r9 does, through formulation's small-change path
    +    And the person is asked for no approval of that rewording
    +
    +  @r7
    +  Scenario: in fix mode, a line with two readings becomes one question to the person giving its readings
    +    Pins that a line with two readings is never decided by the pass: the person is asked once, and the answer goes through integrating-a-proposal's question path.
    +    Given fix mode is asked for
    +    And the line r12 has two readings
    +    When checking-spec-consistency reaches r12
    +    Then it asks the person one question about r12
    +    And that question gives both readings of r12
    +    And the person's answer is integrated through the question path of integrating-a-proposal
    +
    +  @r8
    +  Scenario: in fix mode, drift other than a term or a line with two readings is asked about one finding at a time
    +    Pins that for the rest of the drift the person, not the pass, decides which side is right, and decides them one by one.
    +    Given fix mode is asked for
    +    And a finding that the scenario of r4 shows a status r4 does not give
    +    And a finding that the lines r5 and r6 act on one file without saying which of them wins
    +    When checking-spec-consistency reaches those findings
    +    Then it asks the person which side is right for the finding on r4
    +    And it asks which side is right for the finding on r5 and r6 only after the person has answered about r4
    +
    +  @r10
    +  Scenario: when every finding is applied, rejected or written as an observation, fix mode ends with model check printing no v_t row
    +    Pins that fix mode leaves the spec with no v_t1, v_t2 or v_t3 row once each finding has been dealt with.
    +    Given fix mode is asked for
    +    And model check gave a v_t1 row naming r3, found as a finding
    +    And the finding on the v_t1 row is applied
    +    And a finding on r5 is rejected
    +    And a finding on r8 is written as an observation
    +    When every finding is applied, rejected or written as an observation
    +    Then checking-spec-consistency ends fix mode
    +    And model check prints no v_t1, v_t2 or v_t3 row
    +
    +  @r21
    +  Scenario: when the pass cannot do what it was asked, it stops, says why and changes nothing
    +    Pins that a pass that cannot be done leaves the repository as it was and tells the person the reason.
    +    Given a repository with no spec/ directory
    +    When the person asks for a consistency pass
    +    Then the pass is rejected because checking-spec-consistency cannot do what it was asked
    +    And checking-spec-consistency says why
    +    And no file is changed
    +
    +  @r22
    +  Scenario Outline: a spec-checker writes a finding for a scenario showing behaviour no Behaviour line of its capability asks for
    +    Pins that observable behaviour a scenario adds beyond its capability's lines is found and traced to its ids.
    +    Given the capability orders has no Behaviour line that asks for <behaviour>
    +    And the scenario of r4 in orders shows <behaviour>
    +    When a spec-checker reads orders and its scenarios
    +    Then the spec-checker writes a finding for the scenario of r4
    +    And that finding names r4
    +
    +    Examples:
    +      | behaviour                           |
    +      | an output listing the open orders   |
    +      | a file written under exports/       |
    +      | the status shipped                  |
    +
    +  @r23
    +  Scenario Outline: a spec-checker writes a finding for two lines that act on one thing without saying which wins
    +    Pins that two lines acting on one thing with no word on which wins are found, with both their ids.
    +    Given the line r5 acts on <thing>
    +    And the line r9 acts on <thing>
    +    And neither line says which of them wins
    +    When a spec-checker reads those lines
    +    Then the spec-checker writes a finding for r5 and r9
    +    And that finding names r5 and r9
    +
    +    Examples:
    +      | thing                    |
    +      | the file orders.csv      |
    +      | the status shipped       |
    +      | the command orders close |
    +
    +  @r24
    +  Scenario Outline: a spec-checker writes a finding for a line that leaves to inference which runs, workers or commands it applies to
    +    Pins that a line whose reach must be guessed is found, with its id.
    +    Given the line r6 applies to <what> but does not say which
    +    When a spec-checker reads r6
    +    Then the spec-checker writes a finding for r6
    +    And that finding names r6
    +
    +    Examples:
    +      | what                  |
    +      | some runs             |
    +      | some workers          |
    +      | some commands         |
    +
    +  @r25
    +  Scenario Outline: a spec-checker writes a finding for a scenario that shows another line's response or gives an exit code
    +    Pins that a scenario shows only the response of the line it names, and that no scenario gives an exit code.
    +    Given the capability orders has the lines r4 and r8 and the general failure line r21
    +    And the scenario tagged r4 <shows>
    +    When a spec-checker reads orders and its scenarios
    +    Then the spec-checker writes a finding for the scenario of r4
    +    And that finding names r4
    +
    +    Examples:
    +      | shows                                     |
    +      | shows the response of r8                  |
    +      | shows the command exiting with an error under r21 |
    +      | shows the code rejected under r21         |
    +      | gives an exit code                        |
    +
    +  @r26
    +  Scenario Outline: a spec-checker writes a finding for a status or a mode with a way into it or out of it that no line gives
    +    Pins that every status and mode the lines name is reached and left only by ways a line gives.
    +    Given the lines name the <kind> <name>
    +    And the spec shows a way <direction> <name> that no line gives
    +    When a spec-checker reads the context's Behaviour lines
    +    Then the spec-checker writes a finding for <name>
    +    And that finding names the ids of the lines that name <name>
    +
    +    Examples:
    +      | kind   | name     | direction |
    +      | status | shipped  | into      |
    +      | status | shipped  | out of    |
    +      | mode   | dry mode | into      |
    +      | mode   | dry mode | out of    |
    +
    +  @r27
    +  Scenario: a spec-checker writes a finding for a word a line depends on that is neither a glossary term nor spelled out in the line
    +    Pins that a word whose meaning a line relies on is either in the glossary or said in the line itself.
    +    Given the line r7 depends on the word backorder
    +    And the glossary has no term backorder
    +    And r7 does not spell out what a backorder is
    +    When a spec-checker reads the context's Behaviour lines and the glossary
    +    Then the spec-checker writes a finding for backorder
    +    And that finding names r7
    diff --git a/features/supervision.feature b/features/supervision.feature
    index c5ec0ff3..2cc04494 100644
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
    @@ -1163,6 +1164,30 @@ Feature: Supervision
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
    @@ -1312,8 +1337,9 @@ Feature: Supervision
         And w1's answer to "Is a title given twice in features/books.feature one book or two?" is "One book.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
         And it exits successfully
     
    -  @r163
    -  Scenario Outline: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply>
    +  @r163 @deprecated
    +  Scenario Outline: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply> (deprecated)
    +    Deprecated for: r209 and r210
         Pins that a question is weighed against the person's words alone, apart from every other question, and answered only when those words cover it.
         Given spec/index.md's Glossary holds the term "ledger"
         And i1 fulfils the request q1, which gives the delegation "<delegation>"
    @@ -1330,23 +1356,59 @@ Feature: Supervision
           | Please get everything delivered. Do not stop to ask me questions or permission. | answers it               | w1's question and p1's question each have the session's answer            |
           | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person | w1's question and p1's question have no answer, w1 and p1 awaiting-answer |
     
    -  @r162
    -  Scenario Outline: under a delegation, a question of the initiative that names <named> is left for the person and given to no session
    -    Pins that a question touching the glossary is the person's to answer, whatever the delegation's words allow.
    +  @r209
    +  Scenario Outline: under a delegation, a question of the initiative's glossary-proposal is left for the person and given to no session, whatever words it uses, here <words>
    +    Pins that a question the glossary-proposal asks is the person's to answer, whatever the delegation's words allow and whatever the question's words name.
         Given spec/index.md's Glossary holds the term "ledger"
         And i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    -    And i1's glossary-proposal g1 is awaiting-answer
    -    And i1's work-item w1 is awaiting-answer, its ## Questions section with "<question>" and no answer
    +    And i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "<question>" and no answer
         And each session given a question under the delegation answers it, and every round ends and every worker gives DONE
         When the person runs `work run i1`
         Then "<question>" was given to no session
    -    And w1's question "<question>" has no answer
    -    And w1 is awaiting-answer
    +    And g1's question "<question>" has no answer
    +    And g1 is awaiting-answer
    +
    +    Examples:
    +      | words                                  | question                                                  |
    +      | naming the term "ledger"               | Is the ledger the record of every entry or the open ones? |
    +      | naming no term of the glossary         | Does scripts/log.py keep its reader?                      |
    +
    +  @r210
    +  Scenario Outline: under a delegation, each question of the initiative that is not a question of a glossary-proposal goes to a session of its own, given only the delegation and the files it names, even when it names a term of the glossary or a glossary-proposal, that <reply>
    +    Pins that a question outside the glossary-proposal is weighed against the person's words alone, apart from every other question, whatever its own words name, and answered only when the delegation covers it.
    +    Given spec/index.md's Glossary holds the term "ledger"
    +    And i1 fulfils the request q1, which gives the delegation "<delegation>"
    +    And i1's glossary-proposal g1 is awaiting-answer
    +    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py or scripts/queue.py own the log?" and no answer
    +    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice in features/books.feature one book or two?" and no answer
    +    And i1's work-item w2 is awaiting-answer, its ## Questions section with "Does scripts/log.py write the ledger?" and "Does scripts/queue.py wait for g1 to be applied?", each with no answer
    +    And each session given a question under the delegation <reply>, and every round ends and every worker gives DONE
    +    When the person runs `work run i1`
    +    Then w1's question was given to a session of its own, given the question, the delegation "<delegation>", scripts/log.py and scripts/queue.py, and nothing else
    +    And p1's question was given to a session of its own, given the question, the delegation "<delegation>", features/books.feature, and nothing else
    +    And "Does scripts/log.py write the ledger?" was given to a session of its own, given the question, the delegation "<delegation>", scripts/log.py, and nothing else
    +    And "Does scripts/queue.py wait for g1 to be applied?" was given to another session of its own, given the question, the delegation "<delegation>", scripts/queue.py, and nothing else
    +    And <after>
    +
    +    Examples:
    +      | delegation                                                                       | reply                    | after                                                                                          |
    +      | Please get everything delivered. Do not stop to ask me questions or permission. | answers it               | w1's question, p1's question and each of w2's questions have the session's answer               |
    +      | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person | w1's question, p1's question and w2's questions have no answer, w1, w2 and p1 awaiting-answer |
    +
    +  @r211
    +  Scenario Outline: `work run` reads the delegation the request has when it reads it, the delegation given <when> the initiative started
    +    Pins that a question is answered under the delegation the request holds now, whether the person gave it with the request or after the initiative was already under way.
    +    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", given <when> i1 started
    +    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and no answer
    +    And the session answering under the delegation answers "Yes.", and every worker gives DONE
    +    When the person runs `work run i1`
    +    Then "Does scripts/log.py own the log?" was given to a session of its own, given the question, the delegation "Please get everything delivered. Do not stop to ask me questions or permission.", scripts/log.py, and nothing else
    +    And w1's answer to "Does scripts/log.py own the log?" is "Yes.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
     
         Examples:
    -      | named                         | question                                       |
    -      | the term "ledger"             | Does scripts/log.py write the ledger?          |
    -      | the glossary-proposal g1      | Does scripts/log.py wait for g1 to be applied? |
    +      | when   |
    +      | before |
    +      | after  |
     
       @r78
       Scenario: an answer given by a session started under a delegation is written naming that delegation
    @@ -1402,14 +1464,23 @@ Feature: Supervision
           | ends at its turn limit                                               |
           | ends with no error and before its turn limit, writing no result file |
     
    -  @r93
    -  Scenario: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils
    +  @r93 @deprecated
    +  Scenario: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils (deprecated)
    +    Deprecated for: removal
         Pins that an initiative whose integration left nothing behind is integrated again, from the lines its upstream accepted and no other.
         Given i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
         And every round ends
         When the person runs `work run i1`
         Then a round of the kind integrate was started for i1, given q1's lines 1 and 3, and not line 2
     
    +  @r180
    +  Scenario: a started initiative fulfilling a request, with neither a capability-proposal, a glossary-proposal nor a work-item, is given to an integrate round with the accepted lines of the request
    +    Pins that an initiative whose integration left nothing behind, not even a glossary-proposal, is integrated again, from the lines its upstream accepted and no other.
    +    Given i1 is started, has neither a capability-proposal, a glossary-proposal nor a work-item, and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused
    +    And every round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind integrate was started for i1, given q1's lines 1 and 3, and not line 2
    +
       @r96
       Scenario: an integrate round that ends DONE without a change list ends `work run` with an error naming the round
         Pins that an integration that names no capability to change is reported to the person, even when the round says its work is done.
    @@ -1484,6 +1555,18 @@ Feature: Supervision
         When the person runs `work run i1`
         Then the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming thing#r4, its changes thing#r2 and its removes thing#r3, and one for other, its adds naming other#r1 and its changes and removes naming nothing
     
    +  @r187
    +  Scenario: an integrate round started for a capability-proposal whose change list names another capability the initiative holds a capability-proposal for adds the round's ids for that capability to that proposal, keeping the ids it holds
    +    Pins that the ids a proposal's new integration gives on another capability join the initiative's proposal for that capability, without losing the ids it already named.
    +    Given i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted
    +    And i1's capability-proposal p1, for thing, is awaiting-answer, its ## Questions section with "Is a title given twice one book or two?", given by its gate round, and its Answers section with "One book, and a book's edition is listed with it."
    +    And i1's capability-proposal p2, for other, is awaiting-answer, its adds naming other#r1, its changes naming other#r2 and its removes naming nothing
    +    And the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold
    +    And the integrate round for p1 gives DONE with a change list that adds thing#r4 on thing, and adds other#r6, changes other#r3 and removes other#r5 on other
    +    And every other round ends
    +    When the person runs `work run i1`
    +    Then p2's adds name other#r1 and other#r6, its changes name other#r2 and other#r3, and its removes name other#r5
    +
       @r171
       Scenario: an integrate round that ends with a change list naming the glossary gives a drafted glossary-proposal with the terms it adds, changes and removes in the glossary
         Pins that the terms an integration proposes for the glossary come to the gate as a glossary-proposal, holding each term the change list adds, changes or removes there.
    @@ -1833,6 +1916,16 @@ Feature: Supervision
         Then a round of the kind gate was started for p1
         And p1's ## Questions holds one question, asking for the approval of p1's lines as drafted
     
    +  # [r173] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes.
    +  @r173
    +  Scenario: when the gate round `work run` started for a glossary-proposal ends with no question, one question asking the person to approve the terms it adds, changes and removes is written
    +    Pins that a glossary gate with nothing to decide still reaches the person as a question to answer, so the proposal's terms are not taken as approved unasked.
    +    Given i1's glossary-proposal g1 is drafted, its adds naming the term "ledger", its changes the term "shelf" and its removes the term "loan"
    +    And the gate round's result gives no question, and every round ends
    +    When the person runs `work run i1`
    +    Then a round of the kind gate was started for g1
    +    And one question was written for g1, asking the person to approve the terms "ledger", "shelf" and "loan"
    +
       @r110
       Scenario: when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits
         Pins that fixing what a branch review found brings a new branch review in the same delivery, rather than leaving the fix unreviewed until the next `work run`.
    @@ -1919,3 +2012,42 @@ Feature: Supervision
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
    diff --git a/features/work-queue.feature b/features/work-queue.feature
    index 0bcd307d..88bacb91 100644
    --- a/features/work-queue.feature
    +++ b/features/work-queue.feature
    @@ -57,8 +57,9 @@ Feature: Work queue
         And nothing under the new initiative's directory under .shop/work/ differs from main's last commit
         And it exits successfully
     
    -  @r23
    -  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    +  @r23 @deprecated
    +  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done (deprecated)
    +    Deprecated for: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
         Pins that the command that completes an initiative's work ends the initiative when one of its work-items is green, and that only requests this context asked and keeps, naming the initiative, can hold it open.
         Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
         And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    @@ -75,8 +76,9 @@ Feature: Work queue
           | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
           | a request q1 kept in this context, whose asker is this context, names i2 and is accepted    |
     
    -  @r23
    -  Scenario: retry that makes an initiative's last open work-item green again sets the initiative to done
    +  @r23 @deprecated
    +  Scenario: retry that makes an initiative's last open work-item green again sets the initiative to done (deprecated)
    +    Deprecated for: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
         Pins that retry, like withdraw, is a command whose change can complete an initiative, and that it ends the initiative when it does.
         Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is failed
         And .shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed
    @@ -86,6 +88,26 @@ Feature: Work queue
         And .shop/work/i1/initiative.md gives i1's status as done
         And it exits successfully
     
    +  @r62
    +  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, every capability-proposal formulated or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    +    Pins that whichever command completes an initiative's work, withdraw or retry, ends the initiative when one of its work-items is green and each of its capability-proposals is formulated or withdrawn, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    +    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is <before>
    +    And <log>
    +    And <proposals>
    +    And <request>
    +    When the session runs `work <command> w2`
    +    Then .shop/work/i1/w2.md gives w2's status as <after>
    +    And .shop/work/i1/initiative.md gives i1's status as done
    +    And it exits successfully
    +
    +    Examples:
    +      | command  | before | log                                                                                     | after     | proposals                                                                             | request                                                                                     |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is formulated                                             | no request kept in this context names i1                                                    |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is withdrawn and its capability-proposal p2 is formulated | a request q1 kept in this context, whose asker is this context, names i1 and is delivered   |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is formulated                                             | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
    +      | withdraw | ready  | .shop/work/i1/log.jsonl's last line for w2 is its transition to ready                   | withdrawn | i1's capability-proposal p1 is formulated                                             | a request q1 kept in this context, whose asker is this context, names i2 and is accepted    |
    +      | retry    | failed | .shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed | green     | i1's capability-proposal p1 is formulated                                             | no request kept in this context names i1                                                    |
    +
       @r31
       Scenario: withdraw that leaves every work-item of an initiative withdrawn leaves the initiative's status as it is
         Pins that an initiative none of whose work was delivered is not ended by withdrawing the last of it, even with no request holding it open.
    @@ -97,8 +119,9 @@ Feature: Work queue
         And .shop/work/i1/initiative.md gives i1's status as started
         And it exits successfully
     
    -  @r34
    -  Scenario: list prints each initiative, each request and each work-item under .shop/work/ with its status
    +  @r34 @deprecated
    +  Scenario: list prints each initiative, each request and each work-item under .shop/work/ with its status (deprecated)
    +    Deprecated for: removal
         Pins that list reads the whole queue, initiatives that have ended among them, and gives every initiative, request and work-item in it with its status.
         Given an initiative i1 under .shop/work/ that is started, whose work-items w1 is drafted and w2 is ready
         And an initiative i2 under .shop/work/ that is done, whose work-item w3 is green
    @@ -110,8 +133,9 @@ Feature: Work queue
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
    @@ -121,6 +145,27 @@ Feature: Work queue
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
    @@ -159,6 +204,21 @@ Feature: Work queue
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
    diff --git a/scripts/supervise_answers.py b/scripts/supervise_answers.py
    index e30dd259..43bbb6ec 100644
    --- a/scripts/supervise_answers.py
    +++ b/scripts/supervise_answers.py
    @@ -1,13 +1,12 @@
     """`work run`'s answers under a delegation (capability supervision r77, r78): when the request an initiative fulfils gives
     a delegation, each open question of its awaiting-answer work-items and capability-proposals goes to a session of its own,
     given the question, the delegation and the files the question names, and nothing else. An answer the session gives is
    -written naming the delegation; a question naming a term of the glossary or a glossary-proposal goes to no session and is
    -left for the person (r162, r163). Standard library only; a part of supervise.Run."""
    +written naming the delegation; a question of a glossary-proposal goes to no session and is left for the person, whatever
    +words it uses (r209, r210). Standard library only; a part of supervise.Run."""
     import datetime
     import json
     import re
     
    -import supervise_glossary
     import workqueue
     import workqueue_answer
     import workqueue_request
    @@ -72,7 +71,7 @@ class Answers:
                 before = workqueue.agrees(self.root, self.initiative, name)
                 left = False
                 for question in self.open_questions(name):
    -                answer = None if supervise_glossary.names_one(self.root, question) else self.ask(name, question, delegation)
    +                answer = self.ask(name, question, delegation)
                     if answer is None or left:     # the n-th answer answers the n-th question: none is written after a gap
                         left = True
                         continue
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
    diff --git a/scripts/supervise_glossary.py b/scripts/supervise_glossary.py
    index d0e4c745..64be2612 100644
    --- a/scripts/supervise_glossary.py
    +++ b/scripts/supervise_glossary.py
    @@ -1,7 +1,6 @@
     """The glossary-proposals of an initiative (spec-integration r55, design decision 0073): a term reaches spec/index.md only
     once the person has approved its glossary-proposal, so an apply round's brief withholds the terms of every glossary-proposal
    -that is not `approved`; and a question under a delegation that names a term of the glossary or a glossary-proposal is
    -left for the person (supervision r162). Standard library only."""
    +that is not `approved`. Standard library only."""
     import re
     
     import workqueue
    @@ -43,10 +42,16 @@ def withheld(directory, applying=None):
         return terms
     
     
    -def terms_of(root):
    -    """The terms of spec/index.md's `## Glossary`: the bold name of each bullet."""
    -    path = root / "spec" / "index.md"
    -    return terms_in(path.read_text()) if path.is_file() else []
    +def approval_question(path):
    +    """The question a gate round that gave none writes for the glossary-proposal at `path` (r173), else None: it asks the
    +    person to approve the terms the proposal adds, changes and removes, each by its bare name."""
    +    data, _ = workqueue.frontmatter(path.read_text())
    +    if data.get("kind") != "glossary-proposal":
    +        return None
    +    named = ["%s \"%s\"" % (verb, i[len("term/"):]) for verb, f in (("adds", "adds"), ("changes", "changes"),
    +                                                                    ("removes", "removes"))
    +             for i in data.get(f) or []]
    +    return "Are the terms of %s approved as drafted? It %s." % (path.stem, ", ".join(named))
     
     
     def terms_in(text):
    @@ -77,23 +82,6 @@ def glossary_only_done(root, directory):
                 and not any(i[len("term/"):] in held for d in kinds for i in d.get("removes") or []))
     
     
    -def proposals_of(root):
    -    """The file stem and the full id of every glossary-proposal under .shop/work/, of any initiative and status."""
    -    names = []
    -    for path in sorted((root / ".shop" / "work").glob("*/*.md")):
    -        data, _ = workqueue.frontmatter(path.read_text())
    -        if data.get("kind") == "glossary-proposal":
    -            names += [path.stem] + ([data["id"]] if data.get("id") else [])
    -    return names
    -
    -
    -def names_one(root, question):
    -    """Whether the question names a term of the glossary or a glossary-proposal (supervision r162): as a whole word or
    -    phrase, in any case."""
    -    return any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), question, re.IGNORECASE)
    -               for n in terms_of(root) + proposals_of(root))
    -
    -
     def text(directory, applying=None):
         """The line an apply round's brief gives about them; empty when no term is withheld."""
         terms = withheld(directory, applying)
    diff --git a/scripts/supervise_rounds.py b/scripts/supervise_rounds.py
    index 09b86254..b7062e51 100644
    --- a/scripts/supervise_rounds.py
    +++ b/scripts/supervise_rounds.py
    @@ -157,7 +157,8 @@ class Rounds(Changes, Raises):
             found = [one for one in found if one["capability"] not in absent]
             asked = [q if isinstance(q, str) else json.dumps(q) for q in data.get("questions") or []] if kind == "gate" else None
             if kind == "gate" and not asked:     # r117: a gate with nothing to decide still asks for the approval of the lines
    -            asked = ["Are the lines of %s approved as drafted? Readings: approve %s as drafted (recommended), "
    +            glossary = supervise_glossary.approval_question(self.dir / (name + ".md"))
    +            asked = [glossary] if glossary else ["Are the lines of %s approved as drafted? Readings: approve %s as drafted (recommended), "
                          "or change its lines." % (name, name)]
             if kind == "apply":     # r114: the proposal names what the round applied; a round giving no list leaves it as it was
                 try:
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
    diff --git a/scripts/workqueue_list.py b/scripts/workqueue_list.py
    index c1ce936e..b87d5705 100644
    --- a/scripts/workqueue_list.py
    +++ b/scripts/workqueue_list.py
    @@ -76,12 +76,30 @@ def work_item(root, target, as_json):
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
    diff --git a/spec/capabilities/requests.md b/spec/capabilities/requests.md
    index 7bfb4318..7e315c0c 100644
    --- a/spec/capabilities/requests.md
    +++ b/spec/capabilities/requests.md
    @@ -4,7 +4,7 @@ title: Requests
     narrator: a context taking in or raising a request
     group: service
     rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
    -retired: [r6, r1, r3]
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
    @@ -32,7 +40,7 @@ what using it shows.
     - [r4] `work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question.
     - [r5] `work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run.
     - [r33] **When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument.
    -- [r34] **If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
    +- [r55] **If** a side writes a part of a request that is the other side's part, and the request's asker is not the upstream itself, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
     - [r15] **When** `work outcome <request> <n> <outcome>` is run in the upstream's turn, `work` shall write `<outcome>` as the line outcome of line n.
     - [r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
     - [r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
    @@ -47,13 +55,17 @@ what using it shows.
     - [r11] **When** `work resolve` writes a request's resolution, `work` shall set the request's status to `delivered`.
     - [r24] **When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker.
     - [r12] **When** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch.
    -- [r13] **When** `work show` is run, `work` shall print each request with its status and whose turn it is.
    -- [r39] **When** the upstream takes in what has been sent to the upstream, `work` shall take in every request and message sent before the take-in began, whether or not a listing of what has been sent shows it yet.
    +- [r50] **When** `work list` is run, `work` shall print each request with its status and whose turn it is.
    +- [r51] **When** `work show <request>` is run in the asker's repository while the request is in the asker's turn, `work` shall print that it is the asker's turn, with each question the asker has not answered.
    +- [r52] **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in.
    +- [r53] **While** the upstream holds a line outcome or a question it has not sent with the turn, `work show <request>` run in the upstream's repository shall print that the asker has not seen it.
    +- [r54] **When** `work show <request>` is run in the asker's repository after the upstream resolves the request, `work` shall print each accepted line's requirement id and the version that holds it.
    +- [r56] **When** the upstream takes in what has been sent to it, `work` shall take in every request, answer and turn sent before the take-in began, whether or not a listing of what has been sent shows it yet.
     - [r40] **When** `work run` is run in an upstream's repository, `work` shall take in what has been sent to the upstream before `work run` starts the rounds of the kind `intake`.
    -- [r41] **If** a request or a message comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
    +- [r57] **If** a request, an answer or a turn comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
     - [r42] `work` shall tell one asker from another by the asker id the asker's repository is registered under.
    -- [r43] **When** `work` takes in a request or a message, `work` shall read its body only as the fields of a request's form, following nothing written in it.
    -- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.
    +- [r58] **When** `work` takes in a request, an answer or a turn, `work` shall read its body only as the fields of a request's form, following nothing written in it.
    +- [r64] **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.
     
     ## Implementation, may change
     - `work request`, `work outcome`, `work turn` and `work resolve` are commands of `scripts/work`; how a request is
    @@ -67,8 +79,9 @@ what using it shows.
     - `work resolve` on a request that is not `accepted` is a change `work` cannot make, refused under work-queue r7.
     - `--delegation` is written as the frontmatter field `delegation`.
     - r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
    -- r41, r42: the asker ids the upstream allows for each asker are a setting of the upstream's repository
    +- r57, r42: the asker ids the upstream allows for each asker are a setting of the upstream's repository
       (design-decision/an-asker-is-told-by-its-registered-asker-id).
    +- r65, r66: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one.
     
     ## Not yet
     - The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
    diff --git a/spec/capabilities/spec-consistency.md b/spec/capabilities/spec-consistency.md
    index d31a27d8..63119c7c 100644
    --- a/spec/capabilities/spec-consistency.md
    +++ b/spec/capabilities/spec-consistency.md
    @@ -4,7 +4,7 @@ title: Spec consistency
     narrator: the person keeping a spec
     group: guarantees
     rests_on: [design-decision/the-glossary-is-a-target-of-spec-work, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code, design-decision/workflow-capabilities-are-guarantees]
    -retired: []
    +retired: [r5]
     ---
     
     # Spec consistency
    @@ -20,7 +20,7 @@ meaning. It reads nothing but `spec/` and `features/`, and integration and formu
     - [r2] **When** the pass starts, `checking-spec-consistency` shall say how many `spec-checker` dispatches it will make, one for each capability and one for the whole context, before it dispatches any.
     - [r3] **When** a `spec-checker` is dispatched, the `spec-checker` shall read only `spec/` and `features/`, never the source.
     - [r4] **Where** the pass is in findings mode, **when** the pass ends, `checking-spec-consistency` shall have changed nothing but one findings file, each finding in it naming its ids.
    -- [r5] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term.
    +- [r28] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, each changed line retired and its replacement given a new id, through one gate pass for the term.
     - [r6] **Where** fix mode is asked for, **when** the terms are settled, `checking-spec-consistency` shall have a scenario that uses an avoided word reworded to its line through formulation's small-change path, with no further approval.
     - [r7] **Where** fix mode is asked for, **when** a line has two readings, `checking-spec-consistency` shall ask the person one question with its readings, to be integrated through the question path of `integrating-a-proposal`.
     - [r8] **Where** fix mode is asked for, **when** a finding is drift other than a term or a line with two readings, `checking-spec-consistency` shall ask the person which side is right, one finding at a time.
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index 51f11367..b9900647 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -4,7 +4,7 @@ title: Supervision
     narrator: the person who started `work run`
     group: service
     rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163, r149, r32, r9, r105, r28, r217]
     ---
     
     # Supervision
    @@ -31,6 +31,7 @@ from what using it shows.
     - [r130] **When** a session that `work run` started ends with a result that gives no question and its stage's output, `work run` shall make the node's next transition.
     - [r131] **When** a session that `work run` started ends with a result that gives neither a question nor its stage's output, `work run` shall write under the node's `## Questions` a question naming the output missing and transition the node to `awaiting-answer`.
     - [r132] `work run` shall take as a stage's output: a researcher's file set; a planner's plan and file set; an implementer's commits on which the work-item's scenarios and the whole suite pass; a reviewer's findings; an answering session's answer; an integrate or apply round's change list; a formulate round's scenario for each requirement its proposal adds or changes; an intake round's line outcome or question on each line of its request; a gate round's questions.
    +- [r185] **When** a researcher's result gives an empty file set, `work run` shall take it as the researcher's file set.
     - [r133] `work run` shall make no transition from the outcome a session's result gives.
     - [r95] `work run` shall start the rounds of the kind `integrate`, `apply` and `formulate` of different initiatives one at a time.
     - [r67] **When** a request of which this context is the upstream is `open` or `awaiting-upstream`, `work run` shall start an `initiative-round` session of the kind `intake`, given the request, that writes each line's line outcome or a question on it and passes the turn with `work turn`.
    @@ -38,12 +39,13 @@ from what using it shows.
     - [r134] **When** a round of the kind `intake` that `work run` started gives a question, `work run` shall leave the request's status as `work turn` writes it.
     - [r103] **When** a request of which this context is the upstream is `accepted` and no initiative fulfils it, `work run` shall start its initiative with `work start`.
     - [r79] **When** an initiative is `proposed`, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils.
    -- [r93] **When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils.
    +- [r180] **When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils.
     - [r102] **When** `work run` starts a round of the kind `integrate`, `work run` shall give the round every requirement id that the kept drafts of another initiative, not yet applied, add.
     - [r96] **If** a round of the kind `integrate` that `work run` started ends without a change list, **then** `work run` shall exit with an error, naming the round.
     - [r84] **When** `work run` starts the round of the kind `integrate` of a `proposed` initiative, `work run` shall transition the initiative to `started`.
     - [r91] **When** a round of the kind `integrate` that `work run` started ends, `work run` shall keep the round's drafts on the initiative branch.
     - [r159] **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids it adds, changes and removes on that capability.
    +- [r187] **When** a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds.
     - [r171] **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
     - [r135] **When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation.
     - [r107] **If** a change list that `work run` reads names a capability that neither `spec/capabilities/` nor the round's drafts have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability.
    @@ -56,6 +58,7 @@ from what using it shows.
     - [r117] **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
     - [r69] **When** a round of the kind `gate` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `awaiting-answer`.
     - [r169] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends, `work run` shall transition the proposal to `awaiting-answer`.
    +- [r173] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes.
     - [r70] **When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.
     - [r165] **When** every question that a round of the kind `gate` gave on a glossary-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.
     - [r172] **While** a glossary-proposal is `awaiting-answer` and a question that a round of the kind `gate` gave on it has no answer, `work run` shall start no round of the kind `apply` for it.
    @@ -72,8 +75,10 @@ from what using it shows.
     - [r146] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall start a round of the kind `formulate` for the proposal.
     - [r147] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output.
     - [r148] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall write no second capability-proposal for that proposal's capability.
    +- [r188] **When** a round of the kind `integrate` redrafts some of the lines of a capability-proposal it was started for, `work run` shall keep the requirement ids of the proposal that the round's change list does not name.
    +- [r189] **When** a round of the kind `integrate` redrafts some of the terms of a glossary-proposal it was started for, `work run` shall keep the terms of the glossary-proposal that the round's change list does not name.
     - [r83] **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`.
    -- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
    +- [r186] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
     - [r152] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status.
     - [r153] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output.
     - [r86] **If** a round of any kind that `work run` started for a capability-proposal or an initiative ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall keep the proposal's or initiative's status.
    @@ -92,11 +97,12 @@ from what using it shows.
     - [r97] **While** an initiative has no work-item, `work run` shall run no `measure initiative` on it.
     - [r76] **When** the `measure initiative` that `work run` ran on an initiative has written its measurement, `work run` shall start a session of `analyzing-a-batch` that writes the initiative's analysis record.
     - [r106] **When** `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch.
    -- [r105] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
    +- [r213] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose every capability-proposal is `formulated` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
     - [r161] **When** an initiative changes only the glossary, its glossary-proposal is `approved` and its terms are committed to `spec/index.md`, `work run` shall set the initiative's status to `done`.
     - [r109] **When** `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.
    -- [r163] **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that names neither a term of the glossary nor a glossary-proposal to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
    -- [r162] **When** a question of an initiative names a term of the glossary or a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation.
    +- [r210] **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that is not a question of a glossary-proposal, whatever words it uses, to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
    +- [r211] **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started.
    +- [r209] **When** a question of an initiative is a question of a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation.
     - [r78] **Where** the request an initiative fulfils gives a delegation, **when** a session `work run` started under it answers a question, `work run` shall write the answer naming the delegation it was given under.
     - [r118] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`.
     - [r119] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that accepts the work-item as it is, `work run` shall transition the work-item to `done`.
    @@ -111,9 +117,9 @@ from what using it shows.
     - [r7] **When** `work run` makes a work-item's transition, `work run` shall commit the work-item's file, its stage directories and `log.jsonl` on the initiative branch, and nothing else.
     - [r8] **When** a worker starts or ends, `work run` shall append a line to `log.jsonl` with the time, the work-item, the stage, the agent and the session id.
     - [r62] **When** `work run` writes a stage's `session.json`, `work run` shall record in it the path of the transcript of the stage's session.
    -- [r9] **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status.
    +- [r212] **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status.
     - [r101] **When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions.
    -- [r32] **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall exit with an error, printing each work-item's status and each open question.
    +- [r184] **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall exit with an error, printing each with its open questions.
     - [r52] **When** no work-item can make a transition and a work-item is `failed`, `work run` shall exit with an error, printing each work-item's status and each fault.
     - [r81] **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and one such node is `awaiting-answer` or `failed`, `work run` shall exit with an error, printing the status of each initiative it took.
     - [r82] **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and none is `awaiting-answer` or `failed` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing the status of each initiative it took.
    @@ -154,7 +160,10 @@ from what using it shows.
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
    diff --git a/spec/capabilities/work-queue.md b/spec/capabilities/work-queue.md
    index 8be4ca64..51d65507 100644
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
    @@ -23,13 +23,15 @@ work-item's status; `work run` (supervision) takes them through it. It judges no
     - [r32] **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.
     - [r22] **When** `work start <request>` is run on an `accepted` request, `work` shall write `.shop/work/<initiative>/initiative.md` as a `proposed` initiative of kind `capability-change` that fulfils the request, with the request's origins as its source, and print its id.
     - [r25] **When** `work start` writes an initiative, `work` shall commit the initiative on the current branch.
    -- [r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
    +- [r62] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
     - [r31] **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.
    -- [r34] **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.
    -- [r35] **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.
    +- [r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`.
    +- [r60] **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status.
    +- [r61] **Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.
     - [r39] **While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.
     - [r36] **When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`.
     - [r37] **When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions.
    +- [r59] **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.
     - [r38] **Where** `--json` is given, `work show` shall print its result as one JSON object.
     - [r19] **When** `work note <initiative> <line>` is run, `work` shall append the line, with the date, to the initiative's ledger `.shop/work/<initiative>/ledger.md`.
     - [r20] **When** `work note` appends a line to an initiative's ledger, `work` shall commit the ledger on the current branch.
    @@ -59,7 +61,7 @@ work-item's status; `work run` (supervision) takes them through it. It judges no
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
    index 949e04c7..4f75459d 100644
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
    @@ -26,10 +46,11 @@ def glossary_holds_term(repo, term):
         commit_all(repo, "spec/index.md's Glossary holds a term")
     
     
    -@given(parsers.re(r"i1's glossary-proposal g1 is awaiting-answer$"))
    -def glossary_proposal_awaiting(repo):
    +@given(parsers.re(r"i1's glossary-proposal g1 is awaiting-answer(?:, its ## Questions section with \"(?P<question>[^\"]+)\" and no answer)?$"))
    +def glossary_proposal_awaiting(repo, question=None):
    +    body = "\n## Questions\n\n- %s\n" % question if question else ""
         write(repo, DIR + "/g1.md", "---\nid: %s\nkind: glossary-proposal\npart_of: %s\nstatus: awaiting-answer\nadds: [term/ledger]\n"
    -          "changes: []\nremoves: []\ndate: 2026-10-15\n---\n" % (full("glossary-proposal", "g1"), full("initiative", "i1")))
    +          "changes: []\nremoves: []\ndate: 2026-10-15\n---\n%s" % (full("glossary-proposal", "g1"), full("initiative", "i1"), body))
         commit_all(repo, "an awaiting-answer glossary-proposal")
     
     
    @@ -66,11 +87,11 @@ def sessions_reply(repo, plan, reply):
         plan["delegation-answerer"] = {"fields": {"answer": ANSWER}} if reply == "answers it" else {}
     
     
    -@given(parsers.re(r'i1\'s work-item w1 is awaiting-answer, its ## Questions section with "(?P<one>[^"]+)" and "(?P<two>[^"]+)", '
    +@given(parsers.re(r'i1\'s work-item (?P<name>w\d+) is awaiting-answer, its ## Questions section with "(?P<one>[^"]+)" and "(?P<two>[^"]+)", '
                       r"each with no answer$"))
    -def two_unanswered(repo, one, two):
    -    write(repo, DIR + "/w1.md", "---\nid: %s\nkind: work-item\npart_of: %s\nstatus: awaiting-answer\nunder: thing\n"
    -          "accepts: [thing#r1]\n---\n\n## Questions\n\n- %s\n- %s\n" % (full("work-item", "w1"), full("initiative", "i1"), one, two))
    +def two_unanswered(repo, name, one, two):
    +    write(repo, DIR + "/%s.md" % name, "---\nid: %s\nkind: work-item\npart_of: %s\nstatus: awaiting-answer\nunder: thing\n"
    +          "accepts: [thing#r1]\n---\n\n## Questions\n\n- %s\n- %s\n" % (full("work-item", name), full("initiative", "i1"), one, two))
         commit_all(repo, "a work-item with two unanswered questions")
     
     
    @@ -127,9 +148,9 @@ def session_at_turn_limit(repo, plan, answer):
         plan["delegation-answerer"] = {"fields": {"answer": answer}, "subtype": "error_max_turns", "num_turns": 26}
     
     
    -@then(parsers.re(r'w1\'s question "(?P<question>[^"]+)" has no answer$'))
    -def question_unanswered(repo, question):
    -    text = (repo / (DIR + "/w1.md")).read_text()
    +@then(parsers.re(r'(?P<name>w1|g1)\'s question "(?P<question>[^"]+)" has no answer$'))
    +def question_unanswered(repo, name, question):
    +    text = (repo / (DIR + "/%s.md" % name)).read_text()
         assert question in section(text, "Questions") and not section(text, "Answers").strip(), text
     
     
    @@ -210,6 +231,20 @@ def have_none(repo, context):
             assert not answers_of(repo, name).strip() and "status: awaiting-answer" in text, (name, text)
     
     
    +@then("w1's question, p1's question and each of w2's questions have the session's answer")
    +def have_answer_with_w2(repo, context):
    +    have_answer(repo, context)
    +    assert len(re.findall(r"^- ", answers_of(repo, "w2"), re.MULTILINE)) == 2, answers_of(repo, "w2")
    +    assert ANSWER in answers_of(repo, "w2"), context["done"].stderr
    +
    +
    +@then("w1's question, p1's question and w2's questions have no answer, w1, w2 and p1 awaiting-answer")
    +def have_none_with_w2(repo, context):
    +    for name in ("w1", "w2", "p1"):
    +        text = (repo / (DIR + "/%s.md" % name)).read_text()
    +        assert not answers_of(repo, name).strip() and "status: awaiting-answer" in text, (name, text)
    +
    +
     @then(parsers.re(r'w1\'s answer to "(?P<question>[^"]+)" is "(?P<answer>[^"]+)", naming the delegation "(?P<delegation>[^"]+)"$'))
     def answer_names_delegation(repo, context, question, answer, delegation):
         text = (repo / (DIR + "/w1.md")).read_text()
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
    diff --git a/tests/scenarios/supervision_integrate_steps.py b/tests/scenarios/supervision_integrate_steps.py
    index 8d2bd66d..ed18be41 100644
    --- a/tests/scenarios/supervision_integrate_steps.py
    +++ b/tests/scenarios/supervision_integrate_steps.py
    @@ -19,6 +19,12 @@ def started_fulfilling(repo, text):
         proposed_fulfilling(repo, text, "started")
     
     
    +@given(parsers.re(r"i1 is started, has neither a capability-proposal, a glossary-proposal nor a work-item, and fulfils the "
    +                  r"request q1, whose (?P<text>lines? .+)$"))
    +def started_fulfilling_bare(repo, text):
    +    proposed_fulfilling(repo, text, "started")
    +
    +
     @given("the integrate round for i1 gives DONE with no change list")
     def integrate_without_changes(plan):
         plan["round:integrate"] = {"status": "DONE"}
    diff --git a/tests/scenarios/supervision_merge_steps.py b/tests/scenarios/supervision_merge_steps.py
    new file mode 100644
    index 00000000..5a569b49
    --- /dev/null
    +++ b/tests/scenarios/supervision_merge_steps.py
    @@ -0,0 +1,39 @@
    +"""supervision's steps about an integrate round whose change list names another capability the initiative holds a
    +capability-proposal for (r187): that proposal, the change list on two capabilities, and the lists read back."""
    +import re
    +
    +from pytest_bdd import given, parsers, then
    +
    +from .conftest import full
    +from .supervision_formulate_steps import entry
    +from .supervision_rounds_steps import DIR
    +from .supervision_world import commit_all, write
    +
    +
    +def names(text):
    +    return re.findall(r"[\w-]+#r\d+", text)
    +
    +
    +@given(parsers.re(r"i1's capability-proposal p2, for (?P<cap>\w+), is awaiting-answer, its adds naming (?P<adds>\S+), "
    +                  r"its changes naming (?P<changes>\S+) and its removes naming nothing$"))
    +def other_proposal(repo, cap, adds, changes):
    +    write(repo, DIR + "/p2.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: awaiting-answer\nargues: [%s]\n"
    +          "adds: [%s]\nchanges: [%s]\nremoves: []\ndate: 2026-10-15\n---\n\n# %s\n" % (
    +              full("capability-proposal", "p2"), full("initiative", "i1"), cap, adds, changes, cap))
    +    write(repo, "spec/capabilities/%s.md" % cap, "# %s\n" % cap)     # the capability exists, or the round's list naming it is refused (r107)
    +    commit_all(repo, "p2 is awaiting-answer")
    +
    +
    +@given(parsers.re(r"the integrate round for p1 gives DONE with a change list that (?P<first>.+) on thing, and "
    +                  r"(?P<second>.+) on other$"))
    +def integrate_on_two(plan, first, second):
    +    plan["round:integrate:p1"] = {"status": "DONE", "fields": {"changes": [
    +        {"capability": "thing", **entry(first)}, {"capability": "other", **entry(second)}]}}
    +
    +
    +@then(parsers.re(r"p2's adds name (?P<adds>.+), its changes name (?P<changes>.+), and its removes name (?P<removes>\S+)$"))
    +def p2_lists(repo, context, adds, changes, removes):
    +    text = (repo / DIR / "p2.md").read_text()
    +    held = lambda field: set(names(next(l for l in text.splitlines() if l.startswith(field + ":"))))
    +    assert (held("adds"), held("changes"), held("removes")) == (set(names(adds)), set(names(changes)), set(names(removes))), (
    +        text, context["done"].stderr)
    diff --git a/tests/scenarios/supervision_proposal_steps.py b/tests/scenarios/supervision_proposal_steps.py
    index 0dced974..bb21d8eb 100644
    --- a/tests/scenarios/supervision_proposal_steps.py
    +++ b/tests/scenarios/supervision_proposal_steps.py
    @@ -6,7 +6,7 @@ from pytest_bdd import given, parsers, then
     
     from .conftest import cap, full
     from .supervision_review_steps import FINDINGS
    -from .supervision_rounds_steps import rounds
    +from .supervision_rounds_steps import bullets, rounds
     from .supervision_world import calls, commit_all, fields, git, item_text, starts, write
     
     DIR = ".shop/work/i1"
    @@ -184,6 +184,15 @@ def gate_g1_terms(repo, context, terms):
             assert "term/" + one in found[0]["brief"], (one, found[0]["brief"])
     
     
    +@then(parsers.re(r"one question was written for g1, asking the person to approve the terms (?P<terms>.+)$"))
    +def g1_one_question(repo, terms):
    +    held = [" ".join(" ".join(b).split())[2:] for b in bullets((repo / DIR / "g1.md").read_text(), "Questions")]
    +    assert len(held) == 1, held
    +    assert "approv" in held[0].lower(), held
    +    for one in terms_of(terms):
    +        assert one in held[0], (one, held)
    +
    +
     @then(parsers.re(r'it asks for no question on the term "(?P<term>[^"]+)"$'))
     def gate_g1_no_other(repo, term):
         assert "term/" + term not in rounds(repo, "gate", "g1")[0]["brief"]
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
    index 815ae44a..fc1292b0 100644
    --- a/tests/scenarios/test_supervision.py
    +++ b/tests/scenarios/test_supervision.py
    @@ -33,6 +33,7 @@ from .supervision_formulate_steps import *
     from .supervision_given import *
     from .supervision_integrate_steps import *
     from .supervision_intake_steps import *
    +from .supervision_merge_steps import *
     from .supervision_outputs_steps import *
     from .supervision_parallel_steps import *
     from .supervision_proposal_steps import *
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
    diff --git a/tests/scripts/test_supervise_answers.py b/tests/scripts/test_supervise_answers.py
    index 35337dc1..bb5f2093 100644
    --- a/tests/scripts/test_supervise_answers.py
    +++ b/tests/scripts/test_supervise_answers.py
    @@ -54,18 +54,3 @@ def test_a_reviewers_item_with_every_question_answered_and_no_verdict_from_this_
         assert run.moves == []
         assert run.written == []
         assert run.sessions == []
    -
    -
    -def test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case(tmp_path):
    -    from supervise_glossary import names_one
    -    (tmp_path / "spec").mkdir()
    -    (tmp_path / "spec" / "index.md").write_text("# Index\n\n## Glossary\n\n- **ledger**: a log. Not: journal.\n")
    -    (tmp_path / ".shop" / "work" / "i1").mkdir(parents=True)
    -    (tmp_path / ".shop" / "work" / "i1" / "g1.md").write_text("---\nkind: glossary-proposal\nstatus: drafted\n---\n")
    -    assert names_one(tmp_path, "Does it write the ledger?")
    -    assert names_one(tmp_path, "Is the Ledger kept?")
    -    assert names_one(tmp_path, "Does it wait for g1 to be applied?")
    -    assert not names_one(tmp_path, "Does the pledger own it?")
    -    assert not names_one(tmp_path, "Does it wait for g10?")
    -    assert not names_one(tmp_path, "Is a journal kept?")
    -    assert not names_one(tmp_path, "Which module owns the log?")
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
