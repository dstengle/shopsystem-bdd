---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migration-rebind-2
kind: work-item
part_of: capability-proposal/one-requirement-migration-tools
status: withdrawn
wkind: capability
under: migration-tools
accepts: [migration-tools#r6, migration-tools#r7, migration-tools#r8, migration-tools#r9]
fileset: [tests/scenarios/test_migration_tools.py, tests/scenarios/migration_safety_steps.py]
---

# migration-tools r6-r9: the reformulated scenarios bound

Goes green: the scenarios of the lines it accepts, as the blind formulator rewrote features/migration-tools.feature
for 0.22.0 (one requirement per scenario, exits in words), their step definitions following.

## Questions
- `python3 -m pytest -q -n auto -rfEx -p work_items --work-item migration-rebind-2 --whole-suite` failed on migration-rebind-2's branch work/migration-rebind-2:
  bringing up nodes...
  bringing up nodes...
  
  ........................................................................ [ 11%]
  ........................................................................ [ 23%]
  ........................................................................ [ 34%]
  ....F..................................................................F [ 46%]
  .F.....F.............................X...........X.....................X [ 58%]
  ...............X.....XX.......X.....X..X..X...........uuuuu...uuuuuuuuuu [ 67%]
  ...............................X..u.....u....u........u....u..u....u.u.X [ 77%]
  .u.uu.......u.u.u.X..uu.uu.u..u..uu...u.u...u..u..u..X....uu.......uu..u [ 85%]
  ...u..u.u.u..u....u......uuu.........uu..u............uuuu...........u.. [ 94%]
  ..uus.u..uuu.uu..uuuuu..u.uu..u.u....u...X.X...........                  [100%]
  =================================== FAILURES ===================================
  _ test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[two decisions, the first qualified-decision/0003-b (for artifacts), decision/0004-c-design-decision/example.org/acme/shop/b and design-decision/example.org/acme/shop/c] _
  [gw13] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "its by has the qualifier "(for artifacts)"". Line 88 in scenario "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, two decisions, the first qualified" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[one decision-decision/0003-b (for artifacts)-design-decision/example.org/acme/shop/b] _
  [gw26] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "its by has the qualifier "(for artifacts)"". Line 88 in scenario "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, one decision" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_adds_every_file_it_wrote_or_relocated_to_git_and_writes_specdecisionsindexmd _
  [gw21] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "spec/decisions/index.md is what `model decisions` would write". Line 329 in scenario "`migrate run` adds every file it wrote or relocated to git and writes spec/decisions/index.md" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_gives_specindexmd_whose_id_is_boundedcontextshop_the_id_boundedcontextpath _
  [gw30] linux -- Python 3.11.15 /usr/local/bin/python3
  
  fixturefunc = <function _ at 0x7a8fbc80b740>
  request = <FixtureRequest for <Function test_migrate_run_gives_specindexmd_whose_id_is_boundedcontextshop_the_id_boundedcontextpath>>
  kwargs = {'rel': 'spec/index.md', 'ident': 'bounded-context/example.org/acme/shop', 'old': <scenarios.migration_old.Old object at 0x7a8fbc118190>}
  
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
  
  old = <scenarios.migration_old.Old object at 0x7a8fbc118190>
  rel = 'spec/index.md', ident = 'bounded-context/example.org/acme/shop'
  
      @then(parsers.parse("{rel} gives the id {ident}"))
      def _(old, rel, ident):
          data, _ = front(old, rel)
  >       assert data.get("id") == ident
                 ^^^^^^^^^^^^^^^^^^^^^^^
  E       AssertionError
  
  tests/scenarios/migration_spec_steps.py:28: AssertionError
  =============================== warnings summary ===============================
  tests/scenarios/test_supervision.py: 101 warnings
    /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
      request._fixturemanager._register_fixture(
  
  tests/scenarios/test_supervision.py: 101 warnings
    /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
      fixture_def = FixtureDef(
  
  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  =========================== short test summary info ============================
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[two decisions, the first qualified-decision/0003-b (for artifacts), decision/0004-c-design-decision/example.org/acme/shop/b and design-decision/example.org/acme/shop/c]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[one decision-decision/0003-b (for artifacts)-design-decision/example.org/acme/shop/b]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_adds_every_file_it_wrote_or_relocated_to_git_and_writes_specdecisionsindexmd
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_gives_specindexmd_whose_id_is_boundedcontextshop_the_id_boundedcontextpath
  4 failed, 599 passed, 1 skipped, 16 xpassed, 202 warnings, 83 subtests passed in 11.98s

Withdrawn 2026-10-22 by the person: no more time on migration code; shopsystem-knowledge is the only repository left to migrate, and what `migrate` does not do there the migrating agent fixes by hand.
