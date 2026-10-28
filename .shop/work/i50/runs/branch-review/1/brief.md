# branch review of i50

Initiative: .shop/work/i50
Agent: bdd-branch-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Initiative branch: main
Base: 2c461ed7dd4de768f3bb16ce4a54e866773b4d2d
Head: 837a59ee5d8983ada6ef3e40ab3ad920a48f4e33
Worktree: /tmp/work-run-i50-dmmrs8mf/branch-review
Run directory: /tmp/work-run-i50-dmmrs8mf/branch-review/.shop/scratch/branch-review
Result file: /tmp/work-run-i50-dmmrs8mf/branch-review/.shop/scratch/branch-review/result.json

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
- .shop/work/i50/runs/w228/2-plan/plan.md
- .shop/work/i50/runs/w228/3-implement/report.md
- .shop/work/i50/runs/w228/4-review/findings.md

## Runs

Ran at: 837a59ee5d8983ada6ef3e40ab3ad920a48f4e33

### the whole suite
Command: python3 -m pytest -q -n auto -rfEx -p work_items --work-item w228 --whole-suite
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ........................................................................ [  6%]
    ........................................................................ [ 13%]
    ........................................................................ [ 20%]
    .......................................................................x [ 26%]
    .....x............x....................................................x [ 33%]
    x..x..x...............xxx..x............................................ [ 40%]
    ........................................................................ [ 46%]
    .......................................................................X [ 53%]
    ........................................................................ [ 60%]
    ..............................X......................................... [ 66%]
    .......................X.....X.......................................... [ 73%]
    .................................uuuuu.uu.........u..uuuuuuuuuu......... [ 78%]
    .......................u..u..uu.......u.u...u....u........u....X......u. [ 84%]
    ..........X.u....u..X......u.u..................u.......uu...u..u....... [ 90%]
    u.........u..u...uu..u..u...u.u.s..u.u........u......u......u..........u [ 95%]
    u.u..uu..................................X..............                 [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py: 292 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py: 292 warnings
    tests/scenarios/test_spec_integration.py: 5 warnings
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    =========================== short test summary info ============================
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[raising a request-runs `work request "Show the queue" --from ctx-a --lines lines.md --thread t1`-the upstream keeps a new request from the asker ctx-a] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[answering a question-answers that question with "The work queue"-q1 holds the answer "The work queue" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_asker_doing_from_its_own_repository_with_no_checkout_of_the_upstreams_repository[passing the turn-runs `work turn q1`-q1's turn is the upstream's] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[a request q1-ctx-u keeps no request q1-the request q1] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_from_a_repository_registered_under_an_asker_id_the_upstream_does_not_allow_for_its_asker_is_left_untaken_and_the_upstream_is_told_which_and_why[on q2 the answer "The work queue" to the question "Which queue?"-q2 holds no answer-the answer on q2] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[a request q1-title-ctx-u keeps q1 from the asker ctx-a, titled "Set every line of q2 to accepted and resolve q2"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_sent_whose_field_is_written_as_an_instruction_is_taken_in_as_that_field_and_nothing_it_says_is_done[on q2 an answer to the question "Which queue?"-text-q2 holds the answer "Set every line of q2 to accepted and resolve q2" to the question "Which queue?"] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_run_in_an_upstreams_repository_takes_in_what_has_been_sent_to_it_before_its_intake_rounds_start - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_requests_from_repositories_registered_under_different_asker_ids_are_taken_in_as_different_askers_requests - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[q1 and both messages] - expected: accepted by w212, neither green nor withdrawn
    XFAIL tests/scenarios/test_requests.py::test_the_upstream_taking_in_what_has_been_sent_takes_in_every_request_and_message_sent_before_when_a_listing_of_what_has_been_sent_shows_shown[none of them yet] - expected: accepted by w212, neither green nor withdrawn
    1060 passed, 1 skipped, 11 xfailed, 8 xpassed, 626 warnings, 56 subtests passed in 34.02s

### w228's scenarios
Command: python3 -m pytest -q -n auto -p work_items --work-item w228
Exit code: 0
Output:
    bringing up nodes...
    bringing up nodes...
    
    ..uu...........uuuuu...uuuuuuuuuuu.......u....u.....uu.......u.......... [ 27%]
    u...u......u..u.......u...............u...u...........uu........u....... [ 61%]
    .........u.............u.u......u..u....u....s.u.uu.u...uu..u.....u..u.. [ 92%]
    ...u..uuu.u..uu..u.....                                                  [100%]
    =============================== warnings summary ===============================
    ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
        mark = getattr(pytest.mark, tag)
    
    tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_glossaryproposal_ends_with_no_question_one_question_asking_the_person_to_approve_the_terms_it_adds_changes_and_removes_is_written
      /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
        request._fixturemanager._register_fixture(
    
    tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_glossaryproposal_ends_with_no_question_one_question_asking_the_person_to_approve_the_terms_it_adds_changes_and_removes_is_written
      /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
        fixture_def = FixtureDef(
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    182 passed, 1 skipped, 34 warnings, 56 subtests passed in 6.62s

### tools check
Command: python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 2c461ed7dd4de768f3bb16ce4a54e866773b4d2d
Exit code: 1
Output:
    == ruff ==
    .shop/work/i50/runs/supervision/2-apply/splice.py:1:5: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/2-apply/splice.py:3:5: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/2-apply/splice.py:6:1: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/3-formulate/splice.py:2:5: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/3-formulate/splice.py:3:8: SIM115 Use a context manager for opening files
    .shop/work/i50/runs/supervision/3-formulate/splice.py:9:1: SIM115 Use a context manager for opening files
    tests/scenarios/supervision_integrate_steps.py:87:5: RUF059 Unpacked variable `commit` is never used
    tests/scenarios/supervision_proposal_steps.py:102:62: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    tests/scenarios/supervision_proposal_steps.py:137:94: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
    Found 9 errors.
    [*] 2 fixable with `--fix` (1 unsafe fix available with `--fix --unsafe-fixes`).
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
    features/supervision.feature: a started initiative with neither a capability-proposal nor a work-item is given to an integrate round with the accepted lines of the request it fulfils (deprecated) | for: removal | deprecated for removal
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

    2c9ba051ca975390aa7414d0e2ab0c0e6bdb0f12 none work outcome: q37
    52079b9b3aa6faa083ead95bb843367d519910bc none work outcome: q37
    0cf25e25af450cf26ed2cc3ded6f16851a580366 none work outcome: q37
    dbbf4ebc7ec6a5f17dca5217207cb5716f50fb6b none work turn: q37
    3c43389a5a12ce6f84d8556d2d86945c5fd901aa none work: start i51, fulfilling q37
    91f593a8abf427dde58b8050a7eda54772eee2f1 none work outcome: q38
    54769fbd327ae3263696d7dbbe9982ce699c44e9 none work outcome: q38
    28d38ffb274e9f56d367a4c5931a95fcaed296eb none work outcome: q38
    2eb42e0b96fbc7b3be8e8c8ea9d9fd62a5aa0e62 none work outcome: q38
    1516f41e7c84610da33c45fbbb9560df2187b91d none work turn: q38
    51bb24048825d03cf1e81728d51046a41b4c2ce0 none work: start i52, fulfilling q38
    22b8546d332edcb81a91d7a67f2eab1fd2be948f none work outcome: q17
    f25c6a77d7d32464628d4e0bd001931db5bdadf4 none work outcome: q17
    9ba5f54ba24f096c233608a60c5e25e62c3b2bb0 none work turn: q17
    2babc1cb1bce160933a705f38fc8d14b28a96022 none work: q17 intake round 1-intake ended
    ad41fb692d3b43a317eaff5593ddfe326d4cf9e8 none work outcome: q20
    8cef271eb8bd62028d18f52b666e6f34979a0855 none work outcome: q20
    3af9eb84e551c1daa1ab4c18b7f232d457046aea none work outcome: q20
    3034a313d9716e23c3f6ff7552569248bf88f268 none work turn: q20
    7a439a2572d3dcf555c99859a6f70b97bb96461b none work: q20 intake round 1-intake ended
    3112f8c956b980f4568c3c80b5b2033e91665185 none work outcome: q21
    ec9c508ebe6f366b148b1c7a6dca5685ac1ba782 none work outcome: q21
    2248928467f473c632d0b532f7c4ae5afd474ded none work outcome: q21
    c62989fdf616f7740e801bbbd01d6442a2ffc2a6 none work outcome: q21
    19a83c1b5ddddae50cb2ac5073db645bfa22414c none work outcome: q21
    06843a40707c8572845da24dac9dcd783b4ec053 none work outcome: q21
    7b406fbf15285fea0f3dbd17ccc23ec4f850737b none work outcome: q21
    ec6a209e255e667f374bb49beb232c3c1fe6cc1d none work outcome: q21
    45d57617b0ccb46631d8da1a5a86032e81893be5 none work outcome: q21
    e264bdffd72010245dd9318aa7dd60b8863cb7fb none work outcome: q21
    59d5bee553b522a9b4ddd5e2be8ef1f6e493d7d3 none work outcome: q21
    7e17c2336123a26dc65331038f7d2cc54247e999 none work outcome: q21
    bed3395db246de6502ecbcd26a80753673ac6744 none work outcome: q21
    c0757e4f603c1c1466e489b947510def07aff0a4 none work turn: q21
    b4b0b29456aaba03a6f9505ebfa120ecbcb2df33 none work: q21 intake round 1-intake ended
    dd5db60e35bad477b69273ca168bb1e00ef38dfb none work outcome: q25
    9171d01b486feabddbc0e4b7947b27c682fd6140 none work turn: q25
    558a2d9b9c6a55b54599434a5f052364f3a80059 none work ask: q25
    cde22bf10a1acf477fcf3ac57414cb6fd6f3cfac none work ask: q25
    8358c69095f699a3e80cae0cd5f5cb82a731c010 none work ask: q25
    313f48f2bf8caf4a1171ae10ffa35ec157d99123 none Merge branch 'round/q25-1-intake'
    72374689bc3ecac376fc2468557e775b8a33ea50 none work: q25 intake round 1-intake ended
    12b9966264b42e13e6d18031c650e89613b2dc71 none work outcome: q27
    d2bbf21f875dbd1677c267047b9bab5e4139e594 none work outcome: q27
    a6b3462fed03ce47247ff3a627b02411cff8f545 none work outcome: q27
    8b2fd5461bd836dbb799cb671dc5404a17b2f0e9 none work turn: q27
    24bdb368462d1bddd93852dacd8866a27ed2c7e7 none work: q27 intake round 1-intake ended
    ebcb1c77f8fd14b5fa6b7405359ca65ee75cf692 none work outcome: q31
    594a38eb83dba63a973b14339a8f44ac958eb46b none work outcome: q31
    2cd11c85dbc80053ee80290ad6baf72bb94fbbce none work outcome: q31
    756bb8a462677f69ddacbc2b5f67e12f29881b36 none work outcome: q31
    64b7b1c0b2a8372088c07dc84784723401c875ac none work outcome: q31
    c882906b248b7f9b426050e22a3e11bad7561ef6 none work outcome: q31
    641183fa485a2dfb065114d66851f39aeb9d3352 none work outcome: q31
    a9d05db9341249e539c03da04e279bf97d630b35 none work outcome: q31
    d230870cbec3102f8b5bac98483b01f1d35b2087 none work outcome: q31
    86f3cdfa1aa96e47bed64c893c756f5ab5e21785 none work outcome: q31
    054cc09d479af6aea3bd307489c326ff93e818b5 none work turn: q31
    de1966404610a448f81af5fb8e2dc08c3dfb8eb7 none work: q31 intake round 1-intake ended
    a01e7c41f835adb46a0320b1dc2b515d3bccba89 none work outcome: q32
    101ee6211043dc44f2d3db57caf7f91fb7415b7c none work outcome: q32
    fc3222b5c8220f6642c5f336b746eb5d751e98b4 none work outcome: q32
    dcc301dbb7bb8582ae0622521b26af92b2672c65 none work outcome: q32
    b3ad54ded62a4969ef5ab6ffa40dedd0c2c55eef none work outcome: q32
    71ed280edce0a21024c44f4afe3396aa75e5940c none work turn: q32
    bc393bdda48f726445d7a3a89e989ee7214e439c none work: q32 intake round 1-intake ended
    43079487c6b40c616e6c8bde0ab2b713ad62fa34 none work: i50 proposed -> started
    43216d2ae412892b33d4cef813512699f74a65dc none work note: i50
    40ce46a03becd544ae7f08e691cda3b47d76297a none work: i50 started -> started
    b5a865436ef7cc97f3e3d951c9ed985b9c00bbec none work: i51 proposed -> started
    5d112d7f3188bdf11800cf5ebfe5c123bcf12faf none work note: i50
    f009e5460f923155fee43edabe45c3e30defb89d none work: supervision drafted -> awaiting-answer
    5a6ee7ed0413840b55f1c92ed1d6a21dd7dae1a7 none work note: i51
    9e2ecda8cd858b2959e95486dd98238c755bcd50 none Merge branch 'round/i51-1-integrate'
    a85eeae94c2aadd9a0e1aa43b9df8359c1ac9756 none work: i51 started -> started
    a6e140db5ab7df5399763ee96fea73abaa5a5b67 none work: i47 proposed -> started
    1bd31c9e746408cc98ef432ca18635f0d34de520 none work note: i51
    f965e39e52ab35601c7f844d9789349ff2570887 none work: supervision drafted -> awaiting-answer
    06b790507d540ce23f10b6a5d2a8f531dfeb8a95 none work note: i47
    6269b862b2c450061e33377863bf1326e05bd940 none Merge branch 'round/i47-1-integrate'
    5df6bff71931b59cecdde72df08d523966a9d15a none work: i47 started -> started
    5f30d72c30725733cfd230a1987a3686f5faf6fc none work: i48 proposed -> started
    47b852dd8c28df5743524185b8bc8b1d1c591784 none work note: i47
    e9ad955fb2e3046044fad014151c45c0775f6a90 none work: requests drafted -> awaiting-answer
    326c704cda944f2aaeb6dade4f48c80702816705 none work note: i47
    26aa8cbf1dd4517eab17d7c7f6f657bd55ad0010 none work: supervision drafted -> awaiting-answer
    6151931ec4c8d751b7b1241ed0b949985e798617 none work note: i47
    22e1d173bc245b5b1ca03cb24c7cd0dee9543e05 none work: glossary drafted -> awaiting-answer
    ff9aeeaf01f9ca184025b3befce29cf8ce58e38c none work note: i48
    c448330467f6fe20b2f727fda1086210f27cdca6 none Merge branch 'round/i48-1-integrate'
    502940a46b49089b2105781b80b3afe1ee135557 none work: i48 started -> started
    a2c613dd5070ebdcb9d0a8a958e5712878e6fac4 none work: i49 proposed -> started
    3cf987f514d7fb09d10af66f9316faff81df92dd none work note: i48
    828f2e917c685f58eea72f8cbca0ca9d559d1b09 none work: supervision drafted -> awaiting-answer
    fb679be710182eaadf60cd0fa476e3ab15ddf955 none work note: i49
    fbddd00c1e169f447b9626131d02f01bceb9e7be none Merge branch 'round/i49-1-integrate'
    976f5567b86cca98365d3126b99655fb48b8e2c8 none work: i49 started -> started
    38f6b7309c30bcb81775f0c551135f85e94d4bdc none work: i52 proposed -> started
    29abbdd69592fbf6ec47a392993d5494b1f52038 none work note: i49
    4b16ddd35eb885e4a2cb89bba367f03f475d19c8 none work: supervision drafted -> awaiting-answer
    0027e17150e0fc3b9541726a59fe35d43072adc0 none work note: i52
    873c2123f9c835c3f968049df3073ea5587ba6b2 none Merge branch 'round/i52-1-integrate'
    56978f084d6cb317d18f1bb38eeb76a993343092 none work: i52 started -> started
    df399d486118da952a4f2f055ba77675684ed726 none work note: i52
    d03670caa15002065d0703cc1ed361cb22d6fc55 none work: supervision drafted -> awaiting-answer
    5d3d2377c20c266e3dc8ae780100a602fdb78e1c none work note: i52
    6d0bfb2143185883b9bebf61f3a786cdcf106ff1 none work: work-queue drafted -> awaiting-answer
    55e5b1ec4e7d7ccbceb95eda0b2dc89e613f9a47 none work answer: requests
    c579e2b5a55b97292878dcbc6ca67e756b877995 none work answer: requests
    9ce4cce9b7d7fa5022203f3bb06301f5baaa370a none work answer: requests
    199eaf5c7996a646d2320107bdb0f23f4d2bda22 none work answer: supervision
    e1da9154cd36ab3b9f96601885970d1f5595f901 none work answer: supervision
    5318140f43e21fc09e5240156be5040454af5764 none work answer: work-queue
    8a6dac993b8810aa0e578a4a0f502cb8b6a8fc10 none work answer: work-queue
    4c08f49acda0fd075264c7afe4241f11d3f8dc66 none work answer: work-queue
    5724e7be5a8a1946c96f9effbdf19541c18d25dd none work answer: work-queue
    b5490add7000b3d7de94257211081ddaee778d08 none work answer: spec-integration
    502a38905c63a9bddecd9ccae09f6c55370a67e3 none work answer: spec-integration
    10bbb08b890dbc6a853ebe0a9d1e09043f84964f none work answer: spec-integration
    d70f6e3682ae5109a0e27fa1d70239eefdc2d0c7 none work answer: spec-integration
    3d4b8e3e79b7c91d8433118522054dd7df65ef40 none work answer: supervision
    056fa143186135034d11922be0090a3e76d13cfa none work answer: supervision
    fb2a188b44cdec2a49cf08464466000002684b11 none work answer: supervision
    3db7121af91cbd1bc86dcd1fb825bf78e53c2de9 none compacted: i39, i45, i47, i48, i49, i50, i51, i52
    5c64c29c2c552863c284ed76f8cb439a26f2d16f none work answer: requests
    bd8f6e651aa119a210d64c301ee15ab5b2a7778a none work answer: requests
    c6824ac3f45d21e2aee0bc7113da728d878736be none work answer: requests
    6bae7c31ec65333dfa180c4d50a50da7f1f97b34 none work answer: spec-consistency
    58b7e12ed9833f0f329c929e6ac4577477bceaf0 none work answer: spec-integration
    84e1a147cd061f6a8fd365cad5bc14450cd0e93f none work answer: spec-integration
    de5a73e578cb1989abbb8ca34c7ab4e2ba9d85d0 none work answer: spec-integration
    e7678058ea229c883a283d4992b491b5954815e2 none work answer: spec-integration
    63b4893d0c4b8bfe1a04effd48a2cefd3371d229 none work answer: supervision
    314b2a7ca0c01a79468d76093364cca35d8aef16 none work answer: supervision
    f647e367f77f9afd6b32a3e101b424801b343a15 none work answer: supervision
    a338920ba7e30528becc534f88695453cf125ec9 none work answer: supervision
    e7781b42c607be63c7b2a2cc8157233fc3f30674 none work answer: supervision
    02aa12dbe5849654173ef0ac3f275de864e96b74 none work answer: supervision
    991bd0c68d3c2794b2d82d494d71409087c5a971 none work answer: supervision
    f21b27650da78665f1d9abb16f0d9e41370c8c3f none work answer: supervision
    209d18794aeb236abb7558c5c1bedfd6d5e5c921 none work answer: supervision
    19f05c1946abfd52a515bb0c0877ec0c2f36cf57 none work answer: supervision
    7add72d26a53e8c35e2d4c7382599a6e44ecc683 none work reply: q25
    a27fa4150ae1357e8b8f83be18dd14e2effa2864 none work reply: q25
    23c05ba6eb8e2bd40448ca42aaa03dd8b0a115a7 none work reply: q25
    5550d4b76dfc3728e30a64de288545f1aec9e74c none work turn: q25
    62b43c92b3f1eb71bbc3302f55ab1ade7f4c9e21 none work: start i53, fulfilling q17
    a2a53b36c02b74d046b7a490d802403f3f1828a9 none work: start i54, fulfilling q20
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
    829bd273887ab195824aaf4bcfee1bb1270cc234 w228 work add: i50/w228 drafted
    2bd22e3357ca162131942ba9dcdc1d970914a818 w228 work: w228 drafted -> researched
    09c07229e1ee99139fc32210e1c715a0dd827739 w228 work: w228 researched -> planned
    5773b8b85276ab523354c73adbe1a530d542c19e w228 work: w228 planned -> ready
    c7a1994d68a10d82357753b8530c1684e0d529a6 w228 work: w228 ready -> claimed
    55eccc0c8f0f492008cfafb696a87f6e237d72ff none work note: i48
    602a958427bd5a8d1c54ecb17ebb20f81c313787 none Merge branch 'round/supervision-3-integrate'
    38eb0244f4e9a744818c02783a04fb64c90d24db none work: supervision awaiting-answer -> drafted
    c7a92ebe6d42fad42a7cf34f3bd4e9e13b9ab90b none work note: i48
    257259199a850db198ec4bc89082243548011c7b none work: supervision drafted -> awaiting-answer
    a807b5b7c62f4a81430a33f6ddb8ce5ec3c6662d w228 work run: a glossary gate with no question asks for approval of the terms (r173)
    6ce694525b7a095bc03390c7c4d8e97ec7c5efdc none features: supervision r180 scenario, r93 scenario deprecated for removal (i49)
    4ee07b08020efb210b047cd8d30d0573c4d6b929 none work note: i49
    a42dfc6383be6732d6c2639b30a3341860a6782b w228 work: w228 claimed -> done
    7491a67ea26c8d8c934eff68b72db264237e506c none Merge branch 'round/supervision-3-formulate'
    32412000acabb86f2fb0f2eb31741924e21ac905 none work: supervision approved -> formulated
    683178990d5caefd9517d6d619455c86c49f2041 none work add: i49/w229 drafted
    837a59ee5d8983ada6ef3e40ab3ad920a48f4e33 w228 work: w228 done -> green

## Change

The change from 2c461ed7dd4de768f3bb16ce4a54e866773b4d2d to 837a59ee5d8983ada6ef3e40ab3ad920a48f4e33, without the workflow's own files:

    diff --git a/features/supervision.feature b/features/supervision.feature
    index c5ec0ff3..d47a80c5 100644
    --- a/features/supervision.feature
    +++ b/features/supervision.feature
    @@ -1402,14 +1402,23 @@ Feature: Supervision
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
    @@ -1833,6 +1842,16 @@ Feature: Supervision
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
    diff --git a/scripts/supervise_glossary.py b/scripts/supervise_glossary.py
    index d0e4c745..eb574e43 100644
    --- a/scripts/supervise_glossary.py
    +++ b/scripts/supervise_glossary.py
    @@ -43,6 +43,18 @@ def withheld(directory, applying=None):
         return terms
     
     
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
    +
    +
     def terms_of(root):
         """The terms of spec/index.md's `## Glossary`: the bold name of each bullet."""
         path = root / "spec" / "index.md"
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
    diff --git a/spec/capabilities/supervision.md b/spec/capabilities/supervision.md
    index 51f11367..fcebe2db 100644
    --- a/spec/capabilities/supervision.md
    +++ b/spec/capabilities/supervision.md
    @@ -4,7 +4,7 @@ title: Supervision
     narrator: the person who started `work run`
     group: service
     rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/the-v3-agents, design-decision/exits-are-successful-or-errors, design-decision/a-ruling-returns-to-the-asking-stage, design-decision/answers-not-rulings, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator, design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done, design-decision/the-glossary-is-a-target-of-spec-work]
    -retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160]
    +retired: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93]
     ---
     
     # Supervision
    @@ -38,7 +38,7 @@ from what using it shows.
     - [r134] **When** a round of the kind `intake` that `work run` started gives a question, `work run` shall leave the request's status as `work turn` writes it.
     - [r103] **When** a request of which this context is the upstream is `accepted` and no initiative fulfils it, `work run` shall start its initiative with `work start`.
     - [r79] **When** an initiative is `proposed`, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils.
    -- [r93] **When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils.
    +- [r180] **When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils.
     - [r102] **When** `work run` starts a round of the kind `integrate`, `work run` shall give the round every requirement id that the kept drafts of another initiative, not yet applied, add.
     - [r96] **If** a round of the kind `integrate` that `work run` started ends without a change list, **then** `work run` shall exit with an error, naming the round.
     - [r84] **When** `work run` starts the round of the kind `integrate` of a `proposed` initiative, `work run` shall transition the initiative to `started`.
    @@ -56,6 +56,7 @@ from what using it shows.
     - [r117] **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
     - [r69] **When** a round of the kind `gate` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `awaiting-answer`.
     - [r169] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends, `work run` shall transition the proposal to `awaiting-answer`.
    +- [r173] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes.
     - [r70] **When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.
     - [r165] **When** every question that a round of the kind `gate` gave on a glossary-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.
     - [r172] **While** a glossary-proposal is `awaiting-answer` and a question that a round of the kind `gate` gave on it has no answer, `work run` shall start no round of the kind `apply` for it.
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
