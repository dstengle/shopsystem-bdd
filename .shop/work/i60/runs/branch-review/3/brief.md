# branch review of i60

Initiative: .shop/work/i60
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: ae85edd3a2ce3488f4d930ac5814845eea5e6178
Head: 46d6b92a8f9043dd26bb8c4e8525ae22f31d3af8
Worktree: /tmp/work-run-i60-47epophg/branch-review
Run directory: /tmp/work-run-i60-47epophg/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i60-47epophg/branch-review/.shop/scratch/branch-review/result.json

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
- .shop/work/i60/runs/w233/2-plan/plan.md
- .shop/work/i60/runs/w233/3-implement/report.md
- .shop/work/i60/runs/w233/4-review/findings.md

## Runs

Ran at: 46d6b92a8f9043dd26bb8c4e8525ae22f31d3af8

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w233 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 13%]
    ........................................................................ [ 19%]
    .............................................................x...x..x..x [ 26%]
    ......................x...x...x.........x........x............x......... [ 32%]
    x...x.xxxx...x.xx.........................x............................. [ 39%]
    .................................x...................................... [ 45%]
    .............................................................X.......... [ 52%]
    ........................................................................ [ 58%]
    ..............................................................X......... [ 65%]
    ....................................X.....................x......X.x..x. [ 71%]
    ....X...................X...............................uuuuu....uu.uuuu [ 77%]
    u..uuuuu.u................................u.......u...........u......... [ 83%]
    ...u..u.u.u...u......u...u...............u..u...u.........u.......u..u.. [ 88%]
    ....u..u.......u.u...u.u..u.u..u.....u.u..uu..u.u..........su.u.u....u.. [ 93%]
    .....u...u..u.........................................xx................ [ 99%]
    ......                                                                   [100%]
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
    
    tests/scenarios/test_spec_integration.py: 5 warnings
    tests/scenarios/test_supervision.py: 297 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_spec_integration.py: 5 warnings
    tests/scenarios/test_supervision.py: 297 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_given_a_request_that_holds_before_writes_the_delegation_given_in_the_request_in_place_of_any_it_had[no delegation] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_given_a_request_that_holds_before_writes_the_delegation_given_in_the_request_in_place_of_any_it_had[the delegation "answer any question on line 2"] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_run_in_the_sides_turn_writes_the_delegation[asker] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_writing_a_delegation_in_a_request_commits_the_request_on_the_current_branch - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_given_an_empty_delegation_is_refused_and_nothing_changes - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_writing_a_delegation_in_a_request_keeps_the_requests_status_and_turn - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_given_a_request_that_is_status_is_refused_naming_status_and_nothing_changes[delivered-accepted] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_given_a_request_that_is_status_is_refused_naming_status_and_nothing_changes[refused-refused] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_given_a_request_that_is_status_is_refused_naming_status_and_nothing_changes[withdrawn-withdrawn] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_delegate_run_in_the_sides_turn_writes_the_delegation[upstream] - expected: accepted by requests, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[retry-failed-.shop/work/i1/log.jsonl gives w2's last transitions as from claimed to green, then from green to failed-green-i1's capability-proposal p1 is formulated-no request kept in this context names i1] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-no request kept in this context names i1] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is withdrawn and its capability-proposal p2 is formulated-a request q1 kept in this context, whose asker is this context, names i1 and is delivered] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-a request q1 kept in this context, whose asker is another context, names i1 and is accepted] - expected: accepted by work-queue, neither green nor withdrawn
    XFAIL tests/scenarios/test_work_queue.py::test_a_command_whose_change_leaves_an_initiative_with_a_green_workitem_every_workitem_green_or_withdrawn_every_capabilityproposal_formulated_or_withdrawn_and_every_request_this_context_asked_naming_it_delivered_sets_the_initiative_to_done[withdraw-ready-.shop/work/i1/log.jsonl's last line for w2 is its transition to ready-withdrawn-i1's capability-proposal p1 is formulated-a request q1 kept in this context, whose asker is this context, names i2 and is accepted] - expected: accepted by work-queue, neither green nor withdrawn
    1069 passed, 1 skipped, 26 xfailed, 6 xpassed, 732 warnings, 56 subtests passed in 35.22s

### w233's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w233
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    .....uuuuuuuuuuu.uuuuu.......u.u..................uu...........u..u..u.. [ 27%]
    ....u..u..u..u........u...u..........u.......u.u..u.....u....u.......... [ 61%]
    .....u...uu......u......u.u.u..s.u.u....u....u.u..u.u..u.u..uu...uu..... [ 88%]
    ....u..................                                                  [100%]
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
    
    tests/scenarios/test_supervision.py::test_work_run_reads_the_delegation_the_request_has_when_it_reads_it_the_delegation_given_when_the_initiative_started[before]
    tests/scenarios/test_supervision.py::test_work_run_reads_the_delegation_the_request_has_when_it_reads_it_the_delegation_given_when_the_initiative_started[after]
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_work_run_reads_the_delegation_the_request_has_when_it_reads_it_the_delegation_given_when_the_initiative_started[before]
    tests/scenarios/test_supervision.py::test_work_run_reads_the_delegation_the_request_has_when_it_reads_it_the_delegation_given_when_the_initiative_started[after]
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    182 passed, 1 skipped, 132 warnings, 56 subtests passed in 7.15s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ae85edd3a2ce3488f4d930ac5814845eea5e6178
Exit code: 1
Output:
    == ruff ==
    .shop/work/i60/runs/requests/23-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i60/runs/requests/23-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    tests/scenarios/test_supervision.py:14:1: I001 [*] Import block is un-sorted or un-formatted
    tests/scenarios/work_queue_list_steps.py:134:12: RUF015 Prefer `next(...)` over single element slice
    Found 5 errors.
    [*] 1 fixable with `--fix` (1 unsafe fix available with `--fix --unsafe-fixes`).
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
    6e55ddd3e56305a651df3afacda352dbecb4093d none work add: i54/w231 drafted
    cd273ba8661f7baf4979ec5038164355c6247c08 none work note: i55
    82832c5ee10137d4a86bb08e7d27d401d757a010 none work: w231 drafted -> researched
    2539c8e48ce33611cfaa2a769dd63a580d49673e none Merge branch 'round/supervision-7-integrate'
    5406cde312aa913b78e62a7d2a0a8fd18d12acc4 none work: supervision awaiting-answer -> drafted
    509b51d888fa21cd345e5d85d56c247e57dc075c none work note: i55
    05ebb9c5acd76fa2d120fb0b94ce9eb604d03518 none work: supervision drafted -> awaiting-answer
    56f6efb69af5b66c1db12aaffdf6c740182ab975 none work: w231 researched -> planned
    f5f6671bbe39abbcee3b0b90d31137f15c8aec38 none work: w231 planned -> ready
    21c232e1e8a67571b05e140ee64189ef17e890da none work note: i55
    156d2b2bcb9b5768421dc30920d2c49d124f93f1 none work: w231 ready -> claimed
    1be86700c7de7d3ac2e9b67542a955101890f252 none Merge branch 'round/work-queue-4-apply'
    66f43883b037f8e316322d0fe4fffa188a9caa15 none work: work-queue awaiting-answer -> awaiting-answer
    afc4aa728368e474832b86eba156e1002466367f none supervision r187: steps for an integrate round merging ids into another capability's proposal
    6bf4834a79422c2dd3f86331b50eae45a82d1989 none work note: i55
    3cc54654a998740c9666398cea512e52a17a4116 none work: w231 claimed -> done
    0b981a195f7ee670079618cceb933b286a124ca0 none Merge branch 'round/work-queue-5-integrate'
    7ecda6c0cacc267fee3277872835369035977d44 none work: work-queue awaiting-answer -> drafted
    87d07c300e08743f954111d412e83a9960b82f95 none work: work-queue drafted -> awaiting-answer
    df18eba01e1e0114c59816bc0efd49be8856bc95 none work note: i55
    e6176a783eef5e4aae35c5f078c77d98bf77d016 none work: glossary drafted -> awaiting-answer
    eb1a30ac52528d23385846ad51c1947066590847 none work: w231 done -> green
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
    6b7926df135a5da0951201f6cb9a724210fde131 w233 work add: i60/w233 drafted
    864da987f1369b5bf570105d99cd3e9c1acbb8f8 w233 work: w233 drafted -> researched
    4aa66cd42405ca199c0030acae5d41fb3d44b676 w233 work: w233 researched -> planned
    129a247c195a7d8075c6f0b8162494e507cfcf30 w233 work: w233 planned -> ready
    9b49a82acea471c495e012d3ac16cb9f31d813e8 w233 work: w233 ready -> claimed
    4e206ec401bbad3456fa692991541af3ddc5add4 w233 supervision r211: a Given for a delegation given before or after the initiative started
    de6a60b1ac4bf45bae6f337035c3026a070bc66c w233 work: w233 claimed -> done
    91d43216bef3d0fba6f0d6ffddc3e1ddcb56b669 w233 work: w233 done -> green
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

## Change

The change from ae85edd3a2ce3488f4d930ac5814845eea5e6178 to 46d6b92a8f9043dd26bb8c4e8525ae22f31d3af8, without the workflow's own files:

    diff --git a/features/requests.feature b/features/requests.feature
    index b76d999a..ea3cf9fa 100644
    --- a/features/requests.feature
    +++ b/features/requests.feature
    @@ -70,6 +70,83 @@ Feature: Requests
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
    diff --git a/features/supervision.feature b/features/supervision.feature
    index 4f3c348c..0a27c6a2 100644
    --- a/features/supervision.feature
    +++ b/features/supervision.feature
    @@ -1370,6 +1370,21 @@ Feature: Supervision
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
    @@ -1515,6 +1530,18 @@ Feature: Supervision
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
    diff --git a/scripts/workqueue_list.py b/scripts/workqueue_list.py
    index c1ce936e..67416e4e 100644
    --- a/scripts/workqueue_list.py
    +++ b/scripts/workqueue_list.py
    @@ -76,12 +76,32 @@ def work_item(root, target, as_json):
         return 0
     
     
    +def request_parts(root, name, turn):
    +    """What `work show <request>` prints after its first line (r59): whose turn it is, each line with its line outcome,
    +    each question with its answer, the resolution."""
    +    import workqueue_request
    +    parts = workqueue_request.sections(root, name)
    +    print("it is the %s's turn" % turn)
    +    for number, text in sorted(parts["Lines"].items(), key=lambda e: int(e[0])):
    +        outcome = parts["Outcomes"].get(number)
    +        if outcome is not None:
    +            print("  line %s: %s - %s" % (number, outcome, text))
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
    index e46a9ce5..79bffa84 100644
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
    diff --git a/spec/capabilities/requests.md b/spec/capabilities/requests.md
    index 7bfb4318..238b084f 100644
    --- a/spec/capabilities/requests.md
    +++ b/spec/capabilities/requests.md
    @@ -4,7 +4,7 @@ title: Requests
     narrator: a context taking in or raising a request
     group: service
     rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
    -retired: [r6, r1, r3]
    +retired: [r6, r1, r3, r13, r34, r39, r41, r43, r14]
     ---
     
     # Requests
    @@ -24,6 +24,13 @@ what using it shows.
     - [r29] **Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for.
     - [r19] **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
     - [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
    +- [r65] **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.
    +- [r66] **When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch.
    +- [r67] **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
    +- [r68] **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
    +- [r69] **When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date.
    +- [r70] **When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is.
    +- [r71] **When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn.
     - [r2] **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing.
     - [r45] **If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
     - [r30] **If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing.
    @@ -32,7 +39,7 @@ what using it shows.
     - [r4] `work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question.
     - [r5] `work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run.
     - [r33] **When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument.
    -- [r34] **If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
    +- [r55] **If** a side writes a part of a request that is the other side's part, and the request's asker is not the upstream itself, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
     - [r15] **When** `work outcome <request> <n> <outcome>` is run in the upstream's turn, `work` shall write `<outcome>` as the line outcome of line n.
     - [r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
     - [r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
    @@ -47,13 +54,17 @@ what using it shows.
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
    @@ -67,8 +78,9 @@ what using it shows.
     - `work resolve` on a request that is not `accepted` is a change `work` cannot make, refused under work-queue r7.
     - `--delegation` is written as the frontmatter field `delegation`.
     - r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
    -- r41, r42: the asker ids the upstream allows for each asker are a setting of the upstream's repository
    +- r57, r42: the asker ids the upstream allows for each asker are a setting of the upstream's repository
       (design-decision/an-asker-is-told-by-its-registered-asker-id).
    +- r65, r66: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one.
     
     ## Not yet
     - The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index c7f80e59..52ddddfd 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -4,7 +4,7 @@ title: Supervision
     narrator: the person who started `work run`
     group: service
     rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163, r149, r32, r9, r105]
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
    @@ -44,6 +45,7 @@ from what using it shows.
     - [r84] **When** `work run` starts the round of the kind `integrate` of a `proposed` initiative, `work run` shall transition the initiative to `started`.
     - [r91] **When** a round of the kind `integrate` that `work run` started ends, `work run` shall keep the round's drafts on the initiative branch.
     - [r159] **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids it adds, changes and removes on that capability.
    +- [r187] **When** a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds.
     - [r171] **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
     - [r135] **When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation.
     - [r107] **If** a change list that `work run` reads names a capability that neither `spec/capabilities/` nor the round's drafts have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability.
    @@ -74,7 +76,7 @@ from what using it shows.
     - [r147] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output.
     - [r148] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall write no second capability-proposal for that proposal's capability.
     - [r83] **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`.
    -- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
    +- [r186] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
     - [r152] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status.
     - [r153] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output.
     - [r86] **If** a round of any kind that `work run` started for a capability-proposal or an initiative ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall keep the proposal's or initiative's status.
    @@ -93,10 +95,11 @@ from what using it shows.
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
    @@ -112,9 +115,9 @@ from what using it shows.
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
