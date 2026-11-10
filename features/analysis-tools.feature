# generated from spec/capabilities/analysis-tools.md by features generate; do not edit
Feature: Analysis tools
  Narrator: a session researching or reviewing a project's code

  @g7 @r7
  Scenario: `tools probe` prints each analysis tool and the Python interpreter
    Given no analysis tool is `missing`
    And an analysis tool a1
    And an analysis tool a2
    When the person runs `tools probe`
    Then `tools` prints the analysis tool a1
    And `tools` prints the analysis tool a2
    And `tools` exits successfully

  @g8 @r8
  Scenario: `tools probe` exits with an error naming a missing analysis tool
    Given an analysis tool a1
    And the analysis tool a1 is `missing`
    When the person runs `tools probe`
    Then `tools` exits with an error naming the analysis tool a1

  @g36 @r36
  Scenario: `tools probe --python` prints the Python interpreter it is given
    Given a Python interpreter p1
    When the person runs `tools probe` with the `--python` option set to the Python interpreter p1
    Then `tools` prints the Python interpreter p1

  @g37 @r37
  Scenario: `.venv/bin/python` is the Python interpreter when it exists
    Given the `.venv/bin/python` Python interpreter exists
    When the person runs `tools probe` without the `--python` option
    Then `tools` prints `.venv/bin/python`

  @g38 @r38
  Scenario: `venv/bin/python` is the Python interpreter when it exists and `.venv/bin/python` does not
    Given the `venv/bin/python` Python interpreter exists
    And the `.venv/bin/python` Python interpreter does not exist
    When the person runs `tools probe` without the `--python` option
    Then `tools` prints `venv/bin/python`

  @g39 @r39
  Scenario: `$VIRTUAL_ENV/bin/python` is the Python interpreter when there is no project virtualenv
    Given the `$VIRTUAL_ENV/bin/python` Python interpreter exists
    And the `.venv/bin/python` Python interpreter does not exist
    And the `venv/bin/python` Python interpreter does not exist
    When the person runs `tools probe` without the `--python` option
    Then `tools` prints `$VIRTUAL_ENV/bin/python`

  @g40 @r40
  Scenario: the Python interpreter that executes `scripts/tools` is the Python interpreter when there is no other
    Given the `.venv/bin/python` Python interpreter does not exist
    And the `venv/bin/python` Python interpreter does not exist
    And the `$VIRTUAL_ENV/bin/python` Python interpreter does not exist
    When the person runs `tools probe` without the `--python` option
    Then the Python interpreter p1 executes `scripts/tools`
    And `tools` prints the Python interpreter p1

  @g41 @r41
  Scenario: `.venv/bin/python` comes before `venv/bin/python`
    Given the `.venv/bin/python` Python interpreter exists
    And the `venv/bin/python` Python interpreter exists
    When the person runs `tools probe` without the `--python` option
    Then `tools` does not print `venv/bin/python`

  @g42 @r42
  Scenario: `tools probe --log` prints one log line for a researcher's notes
    Given a log line l1
    And an analysis tool a1
    And an analysis tool a2
    When the person runs `tools probe` with the `--log` option
    Then `tools` prints the log line l1
    And `tools` prints the analysis tool a1
    And `tools` prints the analysis tool a2

  @g43 @r43
  Scenario: `tools install` installs a missing analysis tool and changes no dependency file
    Given the dependency file `requirements.txt` holds "pytest"
    And this Python interpreter is `virtualenv`
    And an analysis tool a1
    And the analysis tool a1 is `missing`
    And an analysis tool a2
    And the analysis tool a2 is `missing`
    When the person runs `tools install`
    Then `tools` installs the analysis tool a1
    And `tools` installs the analysis tool a2
    And `tools` does not change a dependency file

  @g44 @r44
  Scenario: `tools install` installs the one version of `ruff` the plugin pins
    Given `ruff` is `missing`
    And this Python interpreter is `virtualenv`
    When the person runs `tools install`
    Then `ruff` has the version v1
    And the plugin pins the version v1
    And `tools` installs the version v1

  @g45 @r45
  Scenario: `tools install` refuses to install into a Python interpreter that is not a virtualenv
    Given an analysis tool a1
    And the analysis tool a1 is `missing`
    And this Python interpreter is `system`
    When the person runs `tools install`
    Then `tools` refuses `tools install`
    And `tools` names the analysis tool a1

  @g46 @r46
  Scenario: an analysis tool still missing after `tools install` is printed with its pip command
    Given an analysis tool a1
    And the analysis tool a1 is `uninstallable`
    And this Python interpreter is `virtualenv`
    When the person runs `tools install`
    Then the analysis tool a1 has the pip command p1
    And `tools` prints the pip command p1
    And `tools` exits with an error naming the analysis tool a1

  @g47 @r47
  Scenario: `tools map` makes the coverage map whether or not the tests pass
    Given a test t1
    And the test t1 fails
    When the person runs `tools map`
    Then `tools` makes the coverage map c1
    And `tools` exits successfully

  @g48 @r48
  Scenario: `tools map` replaces the coverage map made before
    Given a coverage map c1
    And the coverage map c1 exists
    When the person runs `tools map`
    Then `tools` replaces the coverage map c1

  @g49 @r49
  Scenario: `tools map --json` prints the commit of the coverage map and the number of its tests
    Given a test t1
    And the coverage map c1 holds the test t1
    And a test t2
    And the coverage map c1 holds the test t2
    When the person runs `tools map` with the `--json` option
    Then `tools` makes the coverage map c1
    And the coverage map c1 has the commit c2
    And `tools` prints the commit c2
    And `tools` prints the number of tests in the coverage map c1

  @g50 @r50
  Scenario: `tools tests-of` prints each test that executed its function
    Given a coverage map c1
    And the coverage map c1 exists
    And a test t1
    And the test t1 executes the function f1
    And a test t2
    And the test t2 executes the function f1
    And a test t3
    And the test t3 executes the function f1
    And a test t4
    And the test t4 executes the function f1
    When the person runs `tools tests-of` on the function f1
    Then `tools` prints the test t1
    And `tools` prints the test t2
    And `tools` prints the number of tests that execute the function f1
    And the coverage map c1 has the commit c2
    And `tools` prints the commit c2

  @g51 @r51
  Scenario: `tools tests-of --by-file` prints each Python file that holds a test that executed the function
    Given a coverage map c1
    And the coverage map c1 exists
    And a Python file p1
    And a test t1
    And the test t1 executes the function f1
    And the Python file p1 holds the test t1
    And a Python file p2
    And a test t2
    And the test t2 executes the function f1
    And the Python file p2 holds the test t2
    When the person runs `tools tests-of` with the `--by-file` option on the function f1
    Then `tools` prints the Python file p1
    And `tools` prints the Python file p2

  @g52 @r52
  Scenario: `tools tests-of` says that no test executed its function, and exits successfully
    Given a coverage map c1
    And the coverage map c1 exists
    And a function f1
    And no test executes the function f1
    When the person runs `tools tests-of` on the function f1
    Then the coverage map c1 has the commit c2
    And `tools` prints the commit c2
    And `tools` exits successfully

  @g53 @r53
  Scenario: `tools tests-of --json` prints the tests, their number and the commit of the coverage map
    Given a coverage map c1
    And the coverage map c1 exists
    And a test t1
    And the test t1 executes the function f1
    And a test t2
    And the test t2 executes the function f1
    And a test t3
    And the test t3 executes the function f1
    And a test t4
    And the test t4 executes the function f1
    When the person runs `tools tests-of` with the `--json` option on the function f1
    Then `tools` prints the test t1
    And `tools` prints the test t2
    And `tools` prints the number of tests that execute the function f1
    And the coverage map c1 has the commit c2
    And `tools` prints the commit c2

  @g54 @r54
  Scenario: `tools tests-of` refuses a function its file does not define
    Given a coverage map c1
    And the coverage map c1 exists
    And an identifier i1
    And no Python file defines the identifier i1
    When the person runs `tools tests-of` on the identifier i1
    Then `tools` refuses `tools tests-of`
    And `tools` names the identifier i1

  @g55 @r55
  Scenario: `tools tests-of` refuses when there is no coverage map
    Given no coverage map exists
    When the person runs `tools tests-of` on the function f1
    Then `tools` refuses `tools tests-of`
    And `tools` names `tools map`

  @g56 @r56
  Scenario: `tools untested` prints each function of a Python file that no test executed
    Given a coverage map c1
    And the coverage map c1 exists
    And a function f1
    And the Python file p1 has the function f1
    And no test executes the function f1
    And a function f2
    And the Python file p1 has the function f2
    And no test executes the function f2
    When the person runs `tools untested` on the Python file p1
    Then `tools` prints the function f1
    And `tools` prints the function f2
    And the coverage map c1 has the commit c2
    And `tools` prints the commit c2
    And `tools` exits successfully

  @g57 @r57
  Scenario: `tools untested --json` prints the functions, their number and the commit of the coverage map
    Given a coverage map c1
    And the coverage map c1 exists
    And a function f1
    And the Python file p1 has the function f1
    And no test executes the function f1
    And a function f2
    And the Python file p1 has the function f2
    And no test executes the function f2
    When the person runs `tools untested` with the `--json` option on the Python file p1
    Then `tools` prints the function f1
    And `tools` prints the function f2
    And the coverage map c1 has the commit c2
    And `tools` prints the commit c2

  @g58 @r58
  Scenario: `tools refs` prints each reference to an identifier and their number
    Given a Python file p1
    And an identifier i1
    And the Python file p1 defines the identifier i1
    And a reference r1
    And the reference r1 is to the identifier i1
    And a reference r2
    And the reference r2 is to the identifier i1
    And a reference r3
    And the reference r3 is to the identifier i1
    And a reference r4
    And the reference r4 is to the identifier i1
    When the person runs `tools refs` on the identifier i1
    Then `tools` prints the reference r1
    And `tools` prints the reference r2
    And `tools` prints the number of references to the identifier i1
    And `tools` exits successfully

  @g59 @r59
  Scenario: `tools refs` refuses an identifier the project does not define
    Given an identifier i1
    And no Python file defines the identifier i1
    When the person runs `tools refs` on the identifier i1
    Then `tools` refuses `tools refs`
    And `tools` names the identifier i1

  @g60 @r60
  Scenario: `tools check` prints each finding under its analysis tool's heading
    Given a finding f2
    And an analysis tool a1
    And the analysis tool a1 has the finding f2
    And a file f1
    And the file f1 holds the finding f2
    When the person runs `tools check` on the file f1
    Then the analysis tool a1 has the heading h1
    And `tools` prints the heading h1
    And `tools` prints the finding f2
    And `tools` exits with an error naming the finding f2

  @g61 @r61
  Scenario: `tools check` names a missing analysis tool
    Given `vulture` is `missing`
    When the person runs `tools check`
    Then `tools` exits with an error naming `vulture`

  @g62 @r62
  Scenario: `tools tests-of` refuses when `coverage` is missing, naming `tools install`
    Given `coverage` is `missing`
    When the person runs `tools tests-of` on the function f1
    Then `tools` refuses `tools tests-of`
    And `tools` names `coverage`
    And `tools` names `tools install`

  @g63 @r63
  Scenario: `tools refs` refuses when `jedi` is missing, naming `tools install`
    Given `jedi` is `missing`
    When the person runs `tools refs` on the identifier i1
    Then `tools` refuses `tools refs`
    And `tools` names `jedi`
    And `tools` names `tools install`

  @g64 @r64
  Scenario: `tools size --limit` prints each Python file over the size limit, and exits with an error
    Given a Python file p1
    And a size limit s1
    And the Python file p1 exceeds the size limit s1
    When the person runs `tools size` with the `--limit` option set to the size limit s1
    Then `tools` prints the Python file p1
    And `tools` exits with an error naming the Python file p1

  @g65 @r65
  Scenario: `tools size` takes 300 lines as the size limit when `--limit` gives none
    Given no Python file exceeds `300`
    When the person runs `tools size` without the `--limit` option
    Then `tools` exits successfully

  @g66 @r66
  Scenario: `tools install` installs the RGL
    Given `gf-rgl` is `missing`
    And this Python interpreter is `virtualenv`
    When the person runs `tools install`
    Then `tools` installs `gf-rgl`

  @g67 @r67
  Scenario: `tools probe` reports the RGL
    When the person runs `tools probe`
    Then `tools` prints `gf-rgl`

  @g68 @r68
  Scenario: `tools refs --json` prints the references to an identifier and their number
    Given a Python file p1
    And an identifier i1
    And the Python file p1 defines the identifier i1
    And a reference r1
    And the reference r1 is to the identifier i1
    And a reference r2
    And the reference r2 is to the identifier i1
    And a reference r3
    And the reference r3 is to the identifier i1
    And a reference r4
    And the reference r4 is to the identifier i1
    When the person runs `tools refs` with the `--json` option on the identifier i1
    Then `tools` prints the reference r1
    And `tools` prints the reference r2
    And `tools` prints the number of references to the identifier i1
