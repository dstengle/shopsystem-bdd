---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-3
kind: work-item
part_of: capability-proposal/ids-model-check
status: withdrawn
under: design-model-check
accepts: [design-model-check#r110]
fileset: [scripts/model_work.py, tests/scenarios/design_model_check_problems.py, tests/scenarios/conftest.py, tests/scenarios/design_model_check_then.py]
---

# design-model-check-3

Readings settled by the coordinator under the person's delegation (formulation round f1): a work-item's id for r110 is the `w<n>` of its file name.

## Faults
- its researcher's session ended at its turn limit (error_max_turns, 26 turns, exit code 1); work run takes no outcome from it, whatever its result file says

## Questions
- `python3 -m pytest -q -n auto -rfEx -p work_items --work-item design-model-check-3 --whole-suite` failed on design-model-check-3's branch work/design-model-check-3:
  bringing up nodes...
  bringing up nodes...
  
  ........................................................................ [ 11%]
  ........................................................................ [ 22%]
  ..............F...............X......................................... [ 33%]
  .X............F..........X.X.......F..........................x.......Xx [ 44%]
  .x.x...............X............xx..xXxx..x........x....xx...x...Xx..... [ 55%]
  .x...................................................................... [ 66%]
  .................................................uuuuu...x...uuuuuuuuuuu [ 75%]
  ......X..X.uu.............X..............u...u........u......X.........u [ 85%]
  u.....uu....u.u........u.............uXu.u...suu..uu....uuuX.u.u...uu... [ 93%]
  .uuuu..u..uu...u.....u.u........X.X.X.............x.....                 [100%]
  =================================== FAILURES ===================================
  _ test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has no status-.shop/work/i1/p1.md] _
  [gw31] linux -- Python 3.11.15 /usr/local/bin/python3
  
  fixturefunc = <function file_problem_named at 0x742da9d82020>
  request = <FixtureRequest for <Function test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has no status-.shop/work/i1/p1.md]>>
  kwargs = {'named': '.shop/work/i1/p1.md', 'world': <scenarios.conftest.World object at 0x742da90c7b10>, 'context': {'result': C...y'], 'problems': ['.shop/work/i1/p1.md: no status', ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], ...}}}
  
      def call_fixture_func(
          fixturefunc: _FixtureFunc[FixtureValue], request: FixtureRequest, kwargs
      ) -> FixtureValue:
          if inspect.isgeneratorfunction(fixturefunc):
              fixturefunc = cast(Callable[..., Generator[FixtureValue]], fixturefunc)
              generator = fixturefunc(**kwargs)
              try:
                  fixture_result = next(generator)
              except StopIteration:
                  raise ValueError(f"{request.fixturename} did not yield a value") from None
              finalizer = functools.partial(_teardown_yield_fixture, fixturefunc, generator)
              request.addfinalizer(finalizer)
          else:
              fixturefunc = cast(Callable[..., FixtureValue], fixturefunc)
  >           fixture_result = fixturefunc(**kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^
  
  /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1005: 
  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
  
  world = <scenarios.conftest.World object at 0x742da90c7b10>
  context = {'result': CompletedProcess(args=['/usr/local/bin/python3', '/tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/des...ry'], 'problems': ['.shop/work/i1/p1.md: no status', ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], ...}}
  named = '.shop/work/i1/p1.md'
  
      @then(parsers.parse("it prints a file problem naming {named}"))
      def file_problem_named(world, context, named):
          data = found(world, context)
          if named.endswith(" and scripts/migrate"):  # r61: an old layout's path, named with the script that moves it
              path = named[: -len(" and scripts/migrate")]
              assert _problems_naming(data, path) == ["%s: the layout has no %s; run scripts/migrate" % (path, path)], data
              return
          named, _, absent = named.partition(", and not ")
          count = len(_problems_naming(data, named))
          if "mentions" in context:  # r28: and the requirement the work-item accepts
              count = len([p for p in _problems_naming(data, named) if context["mentions"] in p])
  >       assert count == 1, data
                 ^^^^^^^^^^
  E       AssertionError: {'violations': [['v10a', ['initiative/ex.com/prod/ctx/i1', 'observation/ex.com/prod/ctx/obs-1']], ['v_b1', ['work-item/ex.com/prod/ctx/p1']], ['v_k3', ['initiative/ex.com/prod/ctx/i1']]], 'warnings': [['w_unserved_cap', ['capability/ex.com/prod/ctx/thing']]], 'unresolved': ['.shop/work/i1/initiative.md: observation/ex.com/prod/ctx/obs-1 names nothing in this repository'], 'problems': ['.shop/work/i1/p1.md: no status', ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], 'labels': {'v10a': 'a source that is not an origin', 'v_k3': "a capability-change initiative's first part is not a capability-proposal", 'v_b1': 'a work-item is part of something other than a capability-proposal', 'w_unserved_cap': 'a capability serves no job'}}
  
  tests/scenarios/design_model_check_problems.py:167: AssertionError
  _ test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has a status not in its kind's lifecycle-.shop/work/i1/p1.md] _
  [gw31] linux -- Python 3.11.15 /usr/local/bin/python3
  
  fixturefunc = <function file_problem_named at 0x742da9d82020>
  request = <FixtureRequest for <Function test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has a status not in its kind's lifecycle-.shop/work/i1/p1.md]>>
  kwargs = {'named': '.shop/work/i1/p1.md', 'world': <scenarios.conftest.World object at 0x742da908f850>, 'context': {'result': C...led, green, planned, ready, researched, withdrawn", ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], ...}}}
  
      def call_fixture_func(
          fixturefunc: _FixtureFunc[FixtureValue], request: FixtureRequest, kwargs
      ) -> FixtureValue:
          if inspect.isgeneratorfunction(fixturefunc):
              fixturefunc = cast(Callable[..., Generator[FixtureValue]], fixturefunc)
              generator = fixturefunc(**kwargs)
              try:
                  fixture_result = next(generator)
              except StopIteration:
                  raise ValueError(f"{request.fixturename} did not yield a value") from None
              finalizer = functools.partial(_teardown_yield_fixture, fixturefunc, generator)
              request.addfinalizer(finalizer)
          else:
              fixturefunc = cast(Callable[..., FixtureValue], fixturefunc)
  >           fixture_result = fixturefunc(**kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^
  
  /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1005: 
  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
  
  world = <scenarios.conftest.World object at 0x742da908f850>
  context = {'result': CompletedProcess(args=['/usr/local/bin/python3', '/tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/des...iled, green, planned, ready, researched, withdrawn", ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], ...}}
  named = '.shop/work/i1/p1.md'
  
      @then(parsers.parse("it prints a file problem naming {named}"))
      def file_problem_named(world, context, named):
          data = found(world, context)
          if named.endswith(" and scripts/migrate"):  # r61: an old layout's path, named with the script that moves it
              path = named[: -len(" and scripts/migrate")]
              assert _problems_naming(data, path) == ["%s: the layout has no %s; run scripts/migrate" % (path, path)], data
              return
          named, _, absent = named.partition(", and not ")
          count = len(_problems_naming(data, named))
          if "mentions" in context:  # r28: and the requirement the work-item accepts
              count = len([p for p in _problems_naming(data, named) if context["mentions"] in p])
  >       assert count == 1, data
                 ^^^^^^^^^^
  E       AssertionError: {'violations': [['v10a', ['initiative/ex.com/prod/ctx/i1', 'observation/ex.com/prod/ctx/obs-1']], ['v_b1', ['work-item/ex.com/prod/ctx/p1']], ['v_k3', ['initiative/ex.com/prod/ctx/i1']]], 'warnings': [['w_unserved_cap', ['capability/ex.com/prod/ctx/thing']]], 'unresolved': ['.shop/work/i1/initiative.md: observation/ex.com/prod/ctx/obs-1 names nothing in this repository'], 'problems': [".shop/work/i1/p1.md: status 'loved' is not one of awaiting-ruling, claimed, done, drafted, failed, green, planned, ready, researched, withdrawn", ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], 'labels': {'v10a': 'a source that is not an origin', 'v_k3': "a capability-change initiative's first part is not a capability-proposal", 'v_b1': 'a work-item is part of something other than a capability-proposal', 'w_unserved_cap': 'a capability serves no job'}}
  
  tests/scenarios/design_model_check_problems.py:167: AssertionError
  _ test_a_node_whose_id_is_not_in_typefirst_form_is_a_file_problem[.shop/work/i1/p1.md-a work-item-capability-proposal/ex.com/prod/ctx/p1] _
  [gw11] linux -- Python 3.11.15 /usr/local/bin/python3
  
  fixturefunc = <function file_problem_named at 0x74478560e020>
  request = <FixtureRequest for <Function test_a_node_whose_id_is_not_in_typefirst_form_is_a_file_problem[.shop/work/i1/p1.md-a work-item-capability-proposal/ex.com/prod/ctx/p1]>>
  kwargs = {'named': '.shop/work/i1/p1.md', 'world': <scenarios.conftest.World object at 0x74478495a590>, 'context': {'result': C...d/ctx/p1' is not work-item/ex.com/prod/ctx/<name>", ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], ...}}}
  
      def call_fixture_func(
          fixturefunc: _FixtureFunc[FixtureValue], request: FixtureRequest, kwargs
      ) -> FixtureValue:
          if inspect.isgeneratorfunction(fixturefunc):
              fixturefunc = cast(Callable[..., Generator[FixtureValue]], fixturefunc)
              generator = fixturefunc(**kwargs)
              try:
                  fixture_result = next(generator)
              except StopIteration:
                  raise ValueError(f"{request.fixturename} did not yield a value") from None
              finalizer = functools.partial(_teardown_yield_fixture, fixturefunc, generator)
              request.addfinalizer(finalizer)
          else:
              fixturefunc = cast(Callable[..., FixtureValue], fixturefunc)
  >           fixture_result = fixturefunc(**kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^
  
  /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1005: 
  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
  
  world = <scenarios.conftest.World object at 0x74478495a590>
  context = {'result': CompletedProcess(args=['/usr/local/bin/python3', '/tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/des...od/ctx/p1' is not work-item/ex.com/prod/ctx/<name>", ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], ...}}
  named = '.shop/work/i1/p1.md'
  
      @then(parsers.parse("it prints a file problem naming {named}"))
      def file_problem_named(world, context, named):
          data = found(world, context)
          if named.endswith(" and scripts/migrate"):  # r61: an old layout's path, named with the script that moves it
              path = named[: -len(" and scripts/migrate")]
              assert _problems_naming(data, path) == ["%s: the layout has no %s; run scripts/migrate" % (path, path)], data
              return
          named, _, absent = named.partition(", and not ")
          count = len(_problems_naming(data, named))
          if "mentions" in context:  # r28: and the requirement the work-item accepts
              count = len([p for p in _problems_naming(data, named) if context["mentions"] in p])
  >       assert count == 1, data
                 ^^^^^^^^^^
  E       AssertionError: {'violations': [['v_b1', ['capability-proposal/ex.com/prod/ctx/p1']], ['v_e1', ['capability/ex.com/prod/ctx/thing#r1']], ['v_k3', ['initiative/ex.com/prod/ctx/i1']]], 'warnings': [['w_unserved_cap', ['capability/ex.com/prod/ctx/thing']]], 'unresolved': [], 'problems': [".shop/work/i1/p1.md: id 'capability-proposal/ex.com/prod/ctx/p1' is not work-item/ex.com/prod/ctx/<name>", ".shop/work/i1/p1.md: a work-item's file is named w<n>.md"], 'labels': {'v_k3': "a capability-change initiative's first part is not a capability-proposal", 'v_b1': 'a work-item is part of something other than a capability-proposal', 'v_e1': "a Behaviour line is not in one of EARS's patterns", 'w_unserved_cap': 'a capability serves no job'}}
  
  tests/scenarios/design_model_check_problems.py:167: AssertionError
  =============================== warnings summary ===============================
  ../../../home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: 32 warnings
    /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/plugin.py:137: PytestUnknownMarkWarning: Unknown pytest.mark.deprecated - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
      mark = getattr(pytest.mark, tag)
  
  tests/scenarios/test_supervision.py: 119 warnings
    /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
      request._fixturemanager._register_fixture(
  
  tests/scenarios/test_supervision.py: 119 warnings
    /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
      fixture_def = FixtureDef(
  
  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  =========================== short test summary info ============================
  FAILED tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has no status-.shop/work/i1/p1.md]
  FAILED tests/scenarios/test_design_model_check.py::test_a_malformed_work_directory_or_work_file_is_a_file_problem[the part p1.md has a status not in its kind's lifecycle-.shop/work/i1/p1.md]
  FAILED tests/scenarios/test_design_model_check.py::test_a_node_whose_id_is_not_in_typefirst_form_is_a_file_problem[.shop/work/i1/p1.md-a work-item-capability-proposal/ex.com/prod/ctx/p1]
  XFAIL tests/scenarios/test_migration_tools.py::test_command_on_a_repository_with_change_refuses_naming_it_exits_with_an_error_and_changes_no_file[migrate upgrade-a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md-a tracked README.md deleted since the last commit-README.md] - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_a_repository_with_shop_and_no_shoppluginversion_is_taken_to_be_on_0231 - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_migrate_upgrade_applies_the_pending_upgrade_step_records_the_plugins_version_and_commits_it_all_in_one_commit_naming_the_step - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_with_a_pending_upgrade_step_is_told_to_offer_the_upgrade_and_run_it_only_on_the_persons_yes - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_on_a_plugin_version_above_the_plugins_is_told_to_tell_the_person_to_update_the_plugin - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_on_the_plugins_version_is_told_nothing - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_the_upgrade_step_workitems_named_by_ids_numbers_every_workitem_from_1_by_its_initiatives_number_and_then_its_file_name - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_the_upgrade_step_workitems_named_by_ids_renames_a_workitems_file_and_stage_directories_and_rewrites_its_name_where_its_initiative_names_it - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_migrate_upgrade_with_no_pending_upgrade_step_says_so_exits_successfully_and_changes_nothing - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_a_session_starting_in_a_repository_without_shop_is_told_nothing - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_command_on_a_repository_with_change_refuses_naming_it_exits_with_an_error_and_changes_no_file[migrate run --context example.org/acme/shop-a repository on the old system with work/i1/w1.md-a tracked README.md changed since the last commit-README.md] - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_command_on_a_repository_with_change_refuses_naming_it_exits_with_an_error_and_changes_no_file[migrate run --context example.org/acme/shop-a repository on the old system with work/i1/w1.md-a tracked README.md deleted since the last commit-README.md] - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_command_on_a_repository_with_change_refuses_naming_it_exits_with_an_error_and_changes_no_file[migrate upgrade-a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md-a tracked README.md changed since the last commit-README.md] - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_command_on_a_repository_with_change_refuses_naming_it_exits_with_an_error_and_changes_no_file[migrate upgrade-a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md-an untracked notes/n2.md-notes/n2.md] - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_migrate_status_prints_the_repositorys_plugin_version_the_plugins_version_and_each_pending_upgrade_step_with_its_version_and_description - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_migration_tools.py::test_command_on_a_repository_with_change_refuses_naming_it_exits_with_an_error_and_changes_no_file[migrate run --context example.org/acme/shop-a repository on the old system with work/i1/w1.md-an untracked notes/n2.md-notes/n2.md] - expected: accepted by migration-tools-1, neither green nor withdrawn
  XFAIL tests/scenarios/test_work_queue.py::test_add_with_a_title_partof_under_and_accepts_writes_a_drafted_workitem_named_by_its_id_and_prints_the_id - expected: accepted by work-queue-5, neither green nor withdrawn
  XFAIL tests/scenarios/test_work_queue.py::test_add_numbers_the_new_workitem_one_above_the_highest_workitem_under_shopwork_in_any_initiative_and_any_status - expected: accepted by work-queue-5, neither green nor withdrawn
  3 failed, 613 passed, 1 skipped, 18 xfailed, 17 xpassed, 270 warnings, 52 subtests passed in 12.97s

Ruled by the coordinator under the person's delegation (2026-10-22) and finished by a direct bdd-implementer, merged in 7b4a237 (0.24.0): `work rule` is not yet there. Withdrawn from `work run` for that reason, its requirements built.
