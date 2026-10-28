# branch review of i46

Initiative: .shop/work/i46
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Head: 1f6680407a4a5a2d5f75dd89d2414238f54dace8
Worktree: /tmp/work-run-i46-0i81ojqg/branch-review
Run directory: /tmp/work-run-i46-0i81ojqg/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i46-0i81ojqg/branch-review/.shop/scratch/branch-review/result.json

Review the initiative branch from its base. You start in your worktree: run every command from there and never change directory. Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` and `questions`.

Read:
- spec/capabilities/spec-integration.md
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
- .shop/work/i46/runs/w219/2-plan/plan.md
- .shop/work/i46/runs/w219/3-implement/report.md
- .shop/work/i46/runs/w219/4-review/findings.md

## Runs

Ran at: 1f6680407a4a5a2d5f75dd89d2414238f54dace8

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w219 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    .........x...........x..........x....................X...x.............. [  6%]
    .........x..X.....x........x...........................X....X........... [ 13%]
    ........X...X.......xx.......x......x...........X....................... [ 19%]
    ......X................................................................. [ 26%]
    ........................................................................ [ 33%]
    .............x.x...xxx.....x.x...................x...x.....x............ [ 39%]
    ..........................................................x............. [ 46%]
    ........................................................................ [ 53%]
    .........................................................x.............. [ 59%]
    .........................................x.............x..x....x.x.xx... [ 66%]
    ...............x..x..x...........x........................x............. [ 73%]
    ...................................uu......uuuuu........................ [ 79%]
    ...........uuuuuuuuuuu........u........u...........u.....u.u.......u.... [ 84%]
    .....u...............u.x.......u....u..u..u.u...u..uu........u......u.uu [ 90%]
    ......suu.u...u..u..uu.......u.u.......uu...u...u.u....u........u....... [ 94%]
    ..................................u.u....................                [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py: 291 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py: 291 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the work-item w1.md with status drafted accepts thing#r2, which no scenario names-prints-.shop/work/i1/w1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the work-item w1.md with status withdrawn accepts thing#r2, which no scenario names-does not print-.shop/work/i1/w1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the work-item w1.md with status drafted accepts thing#r2, of a guarantees capability thing, which no scenario names-does not print-.shop/work/i1/w1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the work-item w1.md with status green accepts thing#r2, which capability thing lists as retired-does not print-.shop/work/i1/w1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the work-item w1.md with status done accepts thing#r2, which capability thing lists as retired-prints-.shop/work/i1/w1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_an_initiative_may_be_done_when_its_glossaryproposal_is_approved - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has the kind glossary-proposal and the status drafted-does not print-.shop/work/i1/p1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has the kind capability-proposal and the status awaiting-answer-does not print-.shop/work/i1/p1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[initiative.md has no status-prints-.shop/work/i1/initiative.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has the kind glossary-proposal and the status formulated-prints-.shop/work/i1/p1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has the kind glossary-proposal and the status approved-does not print-.shop/work/i1/p1.md] - expected: accepted by design-model-check, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_under_a_delegation_a_question_of_the_initiative_that_names_named_is_left_for_the_person_and_given_to_no_session[the glossary-proposal g1-Does scripts/log.py wait for g1 to be applied?] - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_an_integrate_round_that_ends_with_a_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_the_requirement_ids_it_adds_changes_and_removes_on_that_capability - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_of_the_initiative_that_names_neither_a_term_of_the_glossary_nor_a_glossaryproposal_goes_to_a_session_of_its_own_given_only_the_delegation_and_the_files_it_names_that_reply[Please get everything delivered. Do not stop to ask me questions or permission.-answers it-w1's question and p1's question each have the session's answer] - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_of_the_initiative_that_names_neither_a_term_of_the_glossary_nor_a_glossaryproposal_goes_to_a_session_of_its_own_given_only_the_delegation_and_the_files_it_names_that_reply[Answer only the questions on the queue's tests; ask me everything else.-leaves it for the person-w1's question and p1's question have no answer, w1 and p1 awaiting-answer] - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_under_a_delegation_a_question_of_the_initiative_that_names_named_is_left_for_the_person_and_given_to_no_session[the term "ledger"-Does scripts/log.py write the ledger?] - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_glossaryproposal_ends_the_proposal_is_awaitinganswer - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_a_glossaryproposal_whose_every_question_from_its_gate_round_has_an_answer_is_given_to_an_apply_round_with_its_answers - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_glossaryproposal_ends_having_applied_its_drafts_the_proposal_is_approved - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_the_gate_round_of_a_capabilityproposal_is_asked_only_for_the_questions_on_the_lines_that_proposal_adds_changes_or_removes - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_the_kind_round_of_a_glossaryproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[gate-drafted] - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_the_kind_round_of_a_glossaryproposal_is_given_the_path_of_the_kept_drafts_of_the_integrate_round_that_wrote_the_proposal[apply-awaiting-answer, its ## Questions section with "Is a ledger one file or one line an event?", and its Answers section with "One file."] - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_when_the_apply_round_work_run_started_for_a_glossaryproposal_ends_having_applied_its_drafts_no_formulate_round_is_started_for_the_proposal - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_an_initiative_that_changes_only_the_glossary_its_glossaryproposal_approved_and_its_terms_committed_to_specindexmd_is_set_done - expected: accepted by supervision, neither green nor withdrawn
    XFAIL tests/scenarios/test_supervision.py::test_a_drafted_glossaryproposal_is_given_to_a_gate_round_asked_only_for_the_questions_on_the_terms_it_adds_changes_or_removes - expected: accepted by supervision, neither green nor withdrawn
    1036 passed, 1 skipped, 36 xfailed, 8 xpassed, 624 warnings, 56 subtests passed in 33.74s

### w219's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w219
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ....uuuuu..uuuuuuuuuuu.......uu.......................u.u.u............. [ 29%]
    .u.u.........u.........u....u....................uu.....u..........u...u [ 64%]
    ..u.u......u...u.....u....u.u.s..u.u.uu.u.u.u....u.u..u.uuu..u..uu..u... [ 88%]
    u......................                                                  [100%]
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
    182 passed, 1 skipped, 36 warnings, 56 subtests passed in 6.95s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 134745663cfa0a109b8564370c2464ef9ee9a7d5
Exit code: 1
Output:
    == ruff ==
    .shop/work/i46/runs/design-model-check/1-formulate/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/1-formulate/splice.py:4:7: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/design-model-check/1-formulate/splice.py:8:1: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/1-formulate/splice.py:1:1: I001 [*] Import block is un-sorted or un-formatted
    .shop/work/i46/runs/supervision/1-formulate/splice.py:2:9: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/1-formulate/splice.py:15:7: SIM115 Use a context manager for opening files
    .shop/work/i46/runs/supervision/1-formulate/splice.py:23:1: SIM115 Use a context manager for opening files
    scripts/supervise_change.py:90:75: B023 Function definition does not bind loop variable `field`
    scripts/supervise_change.py:90:92: B023 Function definition does not bind loop variable `mine`
    scripts/supervise_change.py:117:104: B023 Function definition does not bind loop variable `said`
    Found 10 errors.
    [*] 1 fixable with `--fix`.
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
    features/design-model-check.feature: a malformed work directory or work file is a file problem (deprecated) | for: a malformed work directory or work file is a file problem | features/design-model-check.feature @r124
    features/design-model-check.feature: a work-item accepting a requirement no scenario names is a file problem (deprecated) | for: a malformed work directory or work file is a file problem | features/design-model-check.feature @r124
    features/design-model-check.feature: a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem (deprecated) | for: a malformed work directory or work file is a file problem | features/design-model-check.feature @r124
    features/design-model-check.feature: a green work-item accepting a retired id is no file problem (deprecated) | for: a malformed work directory or work file is a file problem | features/design-model-check.feature @r124
    features/design-model-check.feature: a status in its kind's lifecycle is no file problem (deprecated) | for: a malformed work directory or work file is a file problem | features/design-model-check.feature @r124
    features/design-model-check.feature: an id of a kind kept in .shop/work/ with another context's path is v18 (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a worker's outcome DONE makes the work-item's transition to its next status (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: a researcher's DONE with questions puts those questions into the planner's brief (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply> (deprecated) | for: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply> | features/supervision.feature @r163
    features/supervision.feature: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability (deprecated) | for: an integrate round that ends with a change list gives one drafted capability-proposal for each capability it names, with the requirement ids it adds, changes and removes on that capability | features/supervision.feature @r159
    features/supervision.feature: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer (deprecated) | for: removal | deprecated for removal
    features/supervision.feature: the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes (deprecated) | for: the gate round of a capability-proposal is asked only for the questions on the lines that proposal adds, changes or removes | features/supervision.feature @r168
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

## Change

The change from 134745663cfa0a109b8564370c2464ef9ee9a7d5 to 1f6680407a4a5a2d5f75dd89d2414238f54dace8, without the workflow's own files:

    diff --git a/CLAUDE.md b/CLAUDE.md
    index a0c98f31..1badc3e9 100644
    --- a/CLAUDE.md
    +++ b/CLAUDE.md
    @@ -34,6 +34,7 @@ Code and test files, every tracked Python file, stay at 300 lines or fewer. `pyt
     | `scripts/supervise_change.py` | `work run`'s reading of an integrate round's change list and its writing of one drafted capability-proposal for each capability it names |
     | `scripts/supervise_all.py` | `work run` with no initiative: every open initiative taken side by side, one `Run` each, and the exit on their statuses |
     | `scripts/supervise_answers.py` | `work run`'s answers under a request's delegation: a session for each question, the answer naming the delegation |
    +| `scripts/supervise_glossary.py` | `work run`'s reading of an initiative's glossary-proposals: the terms of those not approved, withheld from an apply round (spec-integration r55) |
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
    index a324ede3..87fa691a 100644
    --- a/features/design-model-check.feature
    +++ b/features/design-model-check.feature
    @@ -287,8 +287,9 @@ Feature: Design model check
           | features/thing.feature     | a scenario with its own title is tagged @holding                           | prints          |
           | features/thing.feature     | a scenario is tagged @deprecated and @holding                              | prints          |
     
    -  @r27
    -  Scenario Outline: a malformed work directory or work file is a file problem
    +  @r27 @deprecated
    +  Scenario Outline: a malformed work directory or work file is a file problem (deprecated)
    +    Deprecated for: a malformed work directory or work file is a file problem
         Pins the shape each initiative and part file must have, and that a missing initiative.md is charged to its directory.
         Given a repository with a work directory .shop/work/i1 in which <case>
         When `model check` is run
    @@ -306,32 +307,36 @@ Feature: Design model check
           | initiative.md has the priority high                                  | .shop/work/i1/initiative.md                        |
           | initiative.md has a date written 16/10/2026                          | .shop/work/i1/initiative.md                        |
     
    -  @r27
    -  Scenario: a work-item accepting a requirement no scenario names is a file problem
    +  @r27 @deprecated
    +  Scenario: a work-item accepting a requirement no scenario names is a file problem (deprecated)
    +    Deprecated for: a malformed work directory or work file is a file problem
         Pins that a work-item may accept only requirements a scenario already names.
         Given a capability thing with requirement r2 that no scenario names
         And a work-item in .shop/work/i1/w1.md that accepts thing#r2
         When `model check` is run
         Then it prints a file problem naming .shop/work/i1/w1.md
     
    -  @r27
    -  Scenario: a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem
    +  @r27 @deprecated
    +  Scenario: a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem (deprecated)
    +    Deprecated for: a malformed work directory or work file is a file problem
         Pins that a guarantees capability's requirements, which no scenario names, may be accepted by a work-item.
         Given a capability thing in the guarantees group with requirement r2 that no scenario names
         And a work-item in .shop/work/i1/w1.md that accepts thing#r2
         When `model check` is run
         Then it prints no file problem naming .shop/work/i1/w1.md
     
    -  @r27
    -  Scenario: a green work-item accepting a retired id is no file problem
    +  @r27 @deprecated
    +  Scenario: a green work-item accepting a retired id is no file problem (deprecated)
    +    Deprecated for: a malformed work directory or work file is a file problem
         Pins that a retired id is left out of what a scenario must name for a work-item to accept it, once that work-item is green.
         Given a capability thing whose frontmatter lists r2 as retired
         And a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2
         When `model check` is run
         Then it prints no file problem naming .shop/work/i1/w1.md
     
    -  @r27
    -  Scenario Outline: a status in its kind's lifecycle is no file problem
    +  @r27 @deprecated
    +  Scenario Outline: a status in its kind's lifecycle is no file problem (deprecated)
    +    Deprecated for: a malformed work directory or work file is a file problem
         Pins that each status the glossary gives a kind is in that kind's lifecycle, awaiting-answer a capability-proposal's and withdrawn a request's.
         Given a repository in which <case>
         When `model check` is run
    @@ -342,6 +347,42 @@ Feature: Design model check
           | a work directory .shop/work/i1 has the part p1.md with the kind capability-proposal and the status awaiting-answer | .shop/work/i1/p1.md       |
           | a request in .shop/work/requests/q1.md, of the form `work request` writes, has the status withdrawn        | .shop/work/requests/q1.md |
     
    +  @r123
    +  Scenario: an initiative may be `done` when its glossary-proposal is approved
    +    Pins that approved is a closed status for a glossary-proposal under a `done` initiative.
    +    Given a capability-change initiative with status `done`
    +    And under it a glossary-proposal with status approved
    +    When `model check` is run
    +    Then no violation names the initiative
    +
    +  @r124
    +  Scenario Outline: a malformed work directory or work file is a file problem
    +    Pins the shape each initiative and part file must have, that a missing initiative.md is charged to its directory, that a glossary-proposal is a part, and which requirements a work-item may accept before a scenario names them.
    +    Given a repository with a work directory .shop/work/i1 in which <case>
    +    When `model check` is run
    +    Then it <prints> a file problem naming <named>
    +
    +    Examples:
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
    +
       @r110
       Scenario Outline: a work-item not named w<n>.md, or two work-items with one id, is a file problem
         Pins that a work-item's file is named by its id and that no id is held by two work-items, in one initiative or across them.
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
    index 1d1faca2..dcaa1851 100644
    --- a/features/supervision.feature
    +++ b/features/supervision.feature
    @@ -1298,8 +1298,9 @@ Feature: Supervision
         When the person runs `work run i1`
         Then a session of analyzing-a-batch was started for i1 once `measure initiative` had written i1's measurement
         And i1's analysis record is not there
    -  @r77
    -  Scenario Outline: under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply>
    +  @r77 @deprecated
    +  Scenario Outline: under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply> (deprecated)
    +    Deprecated for: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply>
         Pins that a question is weighed against the person's words alone, apart from every other question, and answered only when those words cover it.
         Given i1 fulfils the request q1, which gives the delegation "<delegation>"
         And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py or scripts/queue.py own the log?" and no answer
    @@ -1315,8 +1316,9 @@ Feature: Supervision
           | Please get everything delivered. Do not stop to ask me questions or permission. | answers it                              | w1's question and p1's question each have the session's answer            |
           | Answer only the questions on the queue's tests; ask me everything else.          | leaves it for the person                | w1's question and p1's question have no answer, w1 and p1 awaiting-answer |
     
    -  @r77
    -  Scenario: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends
    +  @r77 @deprecated
    +  Scenario: under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends (deprecated)
    +    Deprecated for: removal
         Pins that two questions of one work-item are answered apart, in one `work run`, and that the run keeps every answer its sessions gave instead of losing one to the other.
         Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
         And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py own the log?" and "Is a title given twice in features/books.feature one book or two?", each with no answer
    @@ -1328,6 +1330,42 @@ Feature: Supervision
         And w1's answer to "Is a title given twice in features/books.feature one book or two?" is "One book.", naming the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
         And it exits successfully
     
    +  @r163
    +  Scenario Outline: under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply>
    +    Pins that a question is weighed against the person's words alone, apart from every other question, and answered only when those words cover it.
    +    Given spec/index.md's Glossary holds the term "ledger"
    +    And i1 fulfils the request q1, which gives the delegation "<delegation>"
    +    And i1's work-item w1 is awaiting-answer, its ## Questions section with "Does scripts/log.py or scripts/queue.py own the log?" and no answer
    +    And i1's capability-proposal p1 is awaiting-answer, its ## Questions section with "Is a title given twice in features/books.feature one book or two?" and no answer
    +    And each session given a question under the delegation <reply>, and every round ends and every worker gives DONE
    +    When the person runs `work run i1`
    +    Then w1's question was given to a session of its own, given the question, the delegation "<delegation>", scripts/log.py and scripts/queue.py, and nothing else
    +    And p1's question was given to a session of its own, given the question, the delegation "<delegation>", features/books.feature, and nothing else
    +    And <after>
    +
    +    Examples:
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
    +
    +    Examples:
    +      | named                         | question                                       |
    +      | the term "ledger"             | Does scripts/log.py write the ledger?          |
    +      | the glossary-proposal g1      | Does scripts/log.py wait for g1 to be applied? |
    +
       @r78
       Scenario: an answer given by a session started under a delegation is written naming that delegation
         Pins that the person can tell an answer given in their place from one they gave, and under which words of theirs it was given.
    @@ -1433,8 +1471,9 @@ Feature: Supervision
           | gives DONE with a change list naming thing |
           | ends at its turn limit                |
     
    -  @r92
    -  Scenario: an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability
    +  @r92 @deprecated
    +  Scenario: an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability (deprecated)
    +    Deprecated for: an integrate round that ends with a change list gives one drafted capability-proposal for each capability it names, with the requirement ids it adds, changes and removes on that capability
         Pins that the change list is split by capability, each proposal holding that capability's requirement ids and terms and nothing of another's.
         Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
         And the integrate round for i1 gives DONE with a change list that adds thing#r4 and the term "ledger", changes thing#r2 and removes thing#r3 on thing, and adds other#r1 on other
    @@ -1442,8 +1481,9 @@ Feature: Supervision
         When the person runs `work run i1`
         Then the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3, and one for other, its adds naming other#r1 and its changes and removes naming nothing
     
    -  @r92
    -  Scenario: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids
    +  @r92 @deprecated
    +  Scenario: the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated)
    +    Deprecated for: removal
         Pins that two initiatives changing one capability each get a capability-proposal of their own, never two proposals sharing one id.
         Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted
         And an initiative i2 under .shop/work/, proposed, that fulfils the request q2, whose line 1 has the line outcome accepted
    @@ -1463,6 +1503,15 @@ Feature: Supervision
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
       @r68
       Scenario: a drafted capability-proposal is given to a gate round whose brief asks for the gate as questions, each a decision with its readings and the recommended reading marked
         Pins that the gate comes back as decisions the person can answer one by one, with the reading to take already marked.
    @@ -1643,8 +1692,9 @@ Feature: Supervision
         Then a round of the kind integrate was started for i1, given thing#r4 and other#r1
         And the integrate round for i1 was not given thing#r1, thing#r2 or thing#r5
     
    -  @r104
    -  Scenario: the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes
    +  @r104 @deprecated
    +  Scenario: the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes (deprecated)
    +    Deprecated for: the gate round of a capability-proposal is asked only for the questions on the lines that proposal adds, changes or removes
         Pins that the gate of one capability-proposal raises no question on what another proposal, or the rest of the capability, holds.
         Given the capability thing holds thing#r1, thing#r2 and thing#r3
         And i1's capability-proposal p1 is drafted, its adds naming thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3
    @@ -1681,6 +1731,78 @@ Feature: Supervision
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
    @@ -1705,6 +1827,14 @@ Feature: Supervision
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
    diff --git a/scripts/supervise_brief.py b/scripts/supervise_brief.py
    index dd4bef1b..b6961870 100644
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
    +                lines += [supervise_glossary.text(self.dir)] if supervise_glossary.withheld(self.dir) else []     # r55
                 if stage == "formulate":     # r149: the output of a formulation whose answers change lines outside spec/
                     lines.append(NOTHING_FORMULATED)
                 if stage in ("gate", "apply"):     # r108: the kept drafts of the integrate round that wrote the proposal
    diff --git a/scripts/supervise_change.py b/scripts/supervise_change.py
    index c46f64ad..3f3e5409 100644
    --- a/scripts/supervise_change.py
    +++ b/scripts/supervise_change.py
    @@ -23,13 +23,15 @@ def entries(data):
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
    @@ -44,7 +46,7 @@ class Changes:
             the drafts of all of them count (an apply round's list)."""
             held = {p.stem for p in (self.root / "spec" / "capabilities").glob("*.md")}
             held |= {p.stem for p in stage.glob(("*/" if runs else "") + "drafts/round-*/spec/capabilities/*.md")}
    -        return [one["capability"] for one in found if one["capability"] not in held]
    +        return [one["capability"] for one in found if not one.get("glossary") and one["capability"] not in held]
     
         def kept_path(self, stage):
             """The integrate round's kept drafts directory with the highest round number, relative to the repository with a
    @@ -97,7 +99,7 @@ class Changes:
             ident = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("id:")), "")
             prefix = ident.split("/", 1)[1].rsplit("/", 1)[0] if "/" in ident else ""
             merged = {}
    -        for each in found:     # the entries that name one capability are one proposal's lists, in the order first named
    +        for each in (e for e in found if not e.get("glossary")):     # the entries that name one capability are one proposal's lists, in the order first named
                 one = merged.setdefault(each["capability"], {"capability": each["capability"], **{f: [] for f in FIELDS}})
                 for field in FIELDS:
                     one[field] += [i for i in each[field] if i not in one[field]]
    diff --git a/scripts/supervise_glossary.py b/scripts/supervise_glossary.py
    new file mode 100644
    index 00000000..e73db03a
    --- /dev/null
    +++ b/scripts/supervise_glossary.py
    @@ -0,0 +1,27 @@
    +"""The glossary-proposals of an initiative (spec-integration r55, design decision 0073): a term reaches spec/index.md only
    +once the person has approved its glossary-proposal, so an apply round's brief withholds the terms of every glossary-proposal
    +that is not `approved`. Standard library only."""
    +import workqueue
    +
    +FIELDS = ("adds", "changes", "removes")
    +
    +
    +def withheld(directory):
    +    """The terms (`term/<term>` ids, in the order found) of each glossary-proposal in the initiative's directory whose
    +    status is not `approved`."""
    +    terms = []
    +    for path in sorted(directory.glob("*.md")):
    +        data, _ = workqueue.frontmatter(path.read_text())
    +        if data.get("kind") != "glossary-proposal" or data.get("status") == "approved":
    +            continue
    +        terms += [i for f in FIELDS for i in data.get(f) or [] if i not in terms]
    +    return terms
    +
    +
    +def text(directory):
    +    """The line an apply round's brief gives about them; empty when no term is withheld."""
    +    terms = withheld(directory)
    +    if not terms:
    +        return ""
    +    return ("The person has not approved these terms of the initiative's glossary-proposals: %s. Apply none of them to "
    +            "spec/index.md, also where the drafts hold them." % ", ".join(terms))
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
    index 924c62ab..045ac6cb 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -3,8 +3,8 @@ id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
     title: Supervision
     narrator: the person who started `work run`
     group: service
    -rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140]
    +rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104]
     ---
     
     # Supervision
    @@ -43,16 +43,22 @@ from what using it shows.
     - [r96] **If** a round of the kind `integrate` that `work run` started ends without a change list, **then** `work run` shall exit with an error, naming the round.
     - [r84] **When** `work run` starts the round of the kind `integrate` of a `proposed` initiative, `work run` shall transition the initiative to `started`.
     - [r91] **When** a round of the kind `integrate` that `work run` started ends, `work run` shall keep the round's drafts on the initiative branch.
    -- [r92] **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability.
    +- [r159] **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids it adds, changes and removes on that capability.
    +- [r158] **When** a change list that `work run` reads names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
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
    +- [r160] **While** a glossary-proposal is `awaiting-answer`, `work run` shall start no round of the kind `apply` for it.
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
    index 6cb26c3c..6775356a 100644
    --- a/tests/scenarios/spec_integration_steps.py
    +++ b/tests/scenarios/spec_integration_steps.py
    @@ -6,7 +6,7 @@ import os
     import subprocess
     import sys
     
    -from pytest_bdd import given, then, when
    +from pytest_bdd import given, parsers, then, when
     
     from .conftest import INDEX, SCRIPTS, cap, full
     from .supervision_given import repository
    @@ -62,6 +62,70 @@ def approved_note(repo, plan):
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
    +    assert not (repo / ".shop/work/i1/glossary.md").exists()
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
     
