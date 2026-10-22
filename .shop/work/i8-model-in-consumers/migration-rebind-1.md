---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migration-rebind-1
kind: work-item
part_of: capability-proposal/one-requirement-migration-tools
status: withdrawn
wkind: capability
under: migration-tools
accepts: [migration-tools#r1, migration-tools#r2, migration-tools#r4, migration-tools#r5]
fileset: [tests/scenarios/migration_safety_steps.py]
---

# migration-tools r1-r5: the reformulated scenarios bound

Goes green: the scenarios of the lines it accepts, as the blind formulator rewrote features/migration-tools.feature
for 0.22.0 (one requirement per scenario, exits in words), their step definitions following.

## Questions
- `python3 -m pytest -q -n auto -rfEx -p work_items --work-item migration-rebind-1 --whole-suite` failed on migration-rebind-1's branch work/migration-rebind-1:
  bringing up nodes...
  bringing up nodes...
  
  ........................................................................ [ 11%]
  ........................................................................ [ 23%]
  ........................................................................ [ 34%]
  ...................FF...............F......F.......F..F.........F.F..F.. [ 46%]
  ........F......FF.F.F.........F.......X...F.......X.........X........... [ 58%]
  ....X...............X.X......X........X............X.....X.............. [ 69%]
  ........uuuuu....uu...X.........uu....u....u...u..u...u...u......u..u... [ 78%]
  .u..X.uuuuu..u..u.uXuuuu.u.......u..uuu..u.u...X.u..u..u..u....uu....... [ 86%]
  uu.....................u..u...u...uuuu.u..u...u.u......u.uuuuuuuuu.....u [ 94%]
  ...u.uuu..u.u.u.s..uu..uu..u.uu...u.u.....XX...........                  [100%]
  =================================== FAILURES ===================================
  _ test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a` and `## decision/b`-decisions/0008-b.md, which is relocated to spec/decisions/0008-b.md-0008-b.md-`## decision/b`] _
  [gw27] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 140 in scenario "`migrate run` whose ledger entry's decision file would land on decisions/0008-b.md, which is relocated to spec/decisions/0008-b.md names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a`-decisions/0007-a.md, which is relocated to spec/decisions/0007-a.md-0007-a.md-`## decision/0007-a`] _
  [gw25] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 140 in scenario "`migrate run` whose ledger entry's decision file would land on decisions/0007-a.md, which is relocated to spec/decisions/0007-a.md names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a`-a tracked spec/decisions/0007-a.md-0007-a.md-`## decision/0007-a`] _
  [gw25] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 140 in scenario "`migrate run` whose ledger entry's decision file would land on a tracked spec/decisions/0007-a.md names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_that_finds_found_in_specdecisionsmd_names_it_exits_with_an_error_and_changes_no_file_the_ledger_included[before it the text "Notes on the ledger."-the ledger text "Notes on the ledger." outside its entries] _
  [gw6] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 126 in scenario "`migrate run` that finds before it the text "Notes on the ledger." in spec/decisions.md names it, exits with an error and changes no file, the ledger included" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_that_would_relocate_a_file_onto_an_untracked_file_names_the_relocation_exits_with_an_error_and_changes_no_file _
  [gw1] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 234 in scenario "`migrate run` that would relocate a file onto an untracked file names the relocation, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_outside_a_git_repository_says_so_exits_with_an_error_and_changes_no_file _
  [gw28] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 407 in scenario "`migrate run` outside a git repository says so, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a`-an untracked spec/decisions/0007-a.md-0007-a.md-`## decision/0007-a`] _
  [gw25] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 140 in scenario "`migrate run` whose ledger entry's decision file would land on an untracked spec/decisions/0007-a.md names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_that_finds_found_in_specdecisionsmd_names_it_exits_with_an_error_and_changes_no_file_the_ledger_included[after it the heading `## decision/0007-a`-the ledger entry `## decision/0007-a`, which is there twice] _
  [gw6] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 126 in scenario "`migrate run` that finds after it the heading `## decision/0007-a` in spec/decisions.md names it, exits with an error and changes no file, the ledger included" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[one decision-decision/0003-b (for artifacts)-design-decision/example.org/acme/shop/b] _
  [gw21] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "its by has the qualifier "(for artifacts)"". Line 88 in scenario "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, one decision" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_adds_every_file_it_wrote_or_relocated_to_git_and_writes_specdecisionsindexmd _
  [gw15] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "spec/decisions/index.md is what `model decisions` would write". Line 329 in scenario "`migrate run` adds every file it wrote or relocated to git and writes spec/decisions/index.md" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[two decisions, the first qualified-decision/0003-b (for artifacts), decision/0004-c-design-decision/example.org/acme/shop/b and design-decision/example.org/acme/shop/c] _
  [gw21] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "its by has the qualifier "(for artifacts)"". Line 88 in scenario "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, two decisions, the first qualified" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_that_cannot_make_two_of_its_changes_names_both_exits_with_an_error_and_changes_no_file _
  [gw17] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 225 in scenario "`migrate run` that cannot make two of its changes names both, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_that_would_what_names_it_exits_with_an_error_and_changes_no_file[give a plan that is a symbolic link its id-docs/superpowers/plans/p1.md, a tracked symbolic link to a file outside the repository-change docs/superpowers/plans/p1.md: it is a symbolic link] _
  [gw19] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 392 in scenario "`migrate run` that would give a plan that is a symbolic link its id names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_gives_a_decision_file_whose_id_is_decisionnnnnname_the_typefirst_id _
  [gw14] linux -- Python 3.11.15 /usr/local/bin/python3
  
  fixturefunc = <function _ at 0x794519ebb740>
  request = <FixtureRequest for <Function test_migrate_run_gives_a_decision_file_whose_id_is_decisionnnnnname_the_typefirst_id>>
  kwargs = {'rel': 'spec/decisions/0001-x.md', 'ident': 'design-decision/example.org/acme/shop/x', 'old': <scenarios.migration_old.Old object at 0x79451957a250>}
  
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
  tests/scenarios/migration_spec_steps.py:27: in _
      data, _ = front(old, rel)
                ^^^^^^^^^^^^^^^
  tests/scenarios/migration_old.py:64: in front
      data, body = load_model().frontmatter(old.read(rel))
                                            ^^^^^^^^^^^^^
  tests/scenarios/migration_old.py:44: in read
      return (self.root / rel).read_text()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  /usr/local/lib/python3.11/pathlib.py:1058: in read_text
      with self.open(mode='r', encoding=encoding, errors=errors) as f:
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
  
  self = PosixPath('/tmp/pytest-of-vscode/pytest-10546/popen-gw14/test_migrate_run_gives_a_decis0/spec/decisions/0001-x.md')
  mode = 'r', buffering = -1, encoding = 'locale', errors = None, newline = None
  
      def open(self, mode='r', buffering=-1, encoding=None,
               errors=None, newline=None):
          """
          Open the file pointed by this path and return a file object, as
          the built-in open() function does.
          """
          if "b" not in mode:
              encoding = io.text_encoding(encoding)
  >       return io.open(self, mode, buffering, encoding, errors, newline)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  E       FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-vscode/pytest-10546/popen-gw14/test_migrate_run_gives_a_decis0/spec/decisions/0001-x.md'
  
  /usr/local/lib/python3.11/pathlib.py:1044: FileNotFoundError
  _ test_migrate_run_that_would_what_names_it_exits_with_an_error_and_changes_no_file[write spec/decisions/index.md over an ignored file-an ignored spec/decisions/index.md-write spec/decisions/index.md] _
  [gw19] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 392 in scenario "`migrate run` that would write spec/decisions/index.md over an ignored file names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  _ test_migrate_run_that_would_what_names_it_exits_with_an_error_and_changes_no_file[move a file under an ignored file-an ignored file .shop-move work/i1/w1.md to .shop/work/i1/w1.md: .shop is not a directory] _
  [gw19] linux -- Python 3.11.15 /usr/local/bin/python3
  
  E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "it exits with an error". Line 392 in scenario "`migrate run` that would move a file under an ignored file names it, exits with an error and changes no file" in the feature "/tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1/features/migration-tools.feature"
  All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
  =============================== warnings summary ===============================
  tests/scenarios/test_supervision.py: 101 warnings
    /home/vscode/.local/lib/python3.11/site-packages/pytest_bdd/compat.py:28: PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated. Pass node instead for fixture scoping.
      request._fixturemanager._register_fixture(
  
  tests/scenarios/test_supervision.py: 101 warnings
    /home/vscode/.local/lib/python3.11/site-packages/_pytest/fixtures.py:1986: PytestRemovedIn10Warning: Passing baseid to FixtureDef is deprecated. Pass node instead for fixture scoping.
      fixture_def = FixtureDef(
  
  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  =========================== short test summary info ============================
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a` and `## decision/b`-decisions/0008-b.md, which is relocated to spec/decisions/0008-b.md-0008-b.md-`## decision/b`]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a`-decisions/0007-a.md, which is relocated to spec/decisions/0007-a.md-0007-a.md-`## decision/0007-a`]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a`-a tracked spec/decisions/0007-a.md-0007-a.md-`## decision/0007-a`]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_finds_found_in_specdecisionsmd_names_it_exits_with_an_error_and_changes_no_file_the_ledger_included[before it the text "Notes on the ledger."-the ledger text "Notes on the ledger." outside its entries]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_would_relocate_a_file_onto_an_untracked_file_names_the_relocation_exits_with_an_error_and_changes_no_file
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_outside_a_git_repository_says_so_exits_with_an_error_and_changes_no_file
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_whose_ledger_entrys_decision_file_would_land_on_there_names_it_exits_with_an_error_and_changes_no_file[`## decision/0007-a`-an untracked spec/decisions/0007-a.md-0007-a.md-`## decision/0007-a`]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_finds_found_in_specdecisionsmd_names_it_exits_with_an_error_and_changes_no_file_the_ledger_included[after it the heading `## decision/0007-a`-the ledger entry `## decision/0007-a`, which is there twice]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[one decision-decision/0003-b (for artifacts)-design-decision/example.org/acme/shop/b]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_adds_every_file_it_wrote_or_relocated_to_git_and_writes_specdecisionsindexmd
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_writes_a_qualified_supersedes_as_the_decisions_ids_alone_the_qualifier_going_to_by_case[two decisions, the first qualified-decision/0003-b (for artifacts), decision/0004-c-design-decision/example.org/acme/shop/b and design-decision/example.org/acme/shop/c]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_cannot_make_two_of_its_changes_names_both_exits_with_an_error_and_changes_no_file
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_would_what_names_it_exits_with_an_error_and_changes_no_file[give a plan that is a symbolic link its id-docs/superpowers/plans/p1.md, a tracked symbolic link to a file outside the repository-change docs/superpowers/plans/p1.md: it is a symbolic link]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_gives_a_decision_file_whose_id_is_decisionnnnnname_the_typefirst_id
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_would_what_names_it_exits_with_an_error_and_changes_no_file[write spec/decisions/index.md over an ignored file-an ignored spec/decisions/index.md-write spec/decisions/index.md]
  FAILED tests/scenarios/test_migration_tools.py::test_migrate_run_that_would_what_names_it_exits_with_an_error_and_changes_no_file[move a file under an ignored file-an ignored file .shop-move work/i1/w1.md to .shop/work/i1/w1.md: .shop is not a directory]
  16 failed, 587 passed, 1 skipped, 16 xpassed, 202 warnings, 83 subtests passed in 11.66s

Withdrawn 2026-10-22 by the person: no more time on migration code; shopsystem-knowledge is the only repository left to migrate, and what `migrate` does not do there the migrating agent fixes by hand.
