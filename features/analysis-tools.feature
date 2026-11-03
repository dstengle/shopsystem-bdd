# generated from spec/capabilities/analysis-tools.md by features generate; do not edit
Feature: Analysis tools
  Narrator: a session researching or reviewing a project's code

  @g1 @r1
  Scenario: `--python` gives the Python interpreter
    Given `--python` is given
    And a Python interpreter `--python`
    When the person runs `tools probe`
    Then `tools` prints the Python interpreter `--python`

  @g2 @r2
  Scenario: `.venv/bin/python` is the Python interpreter when it exists
    Given a Python interpreter `.venv/bin/python`
    When the person runs `tools probe`
    Then `tools` prints the Python interpreter `.venv/bin/python`

  @g3 @r3
  Scenario: `venv/bin/python` is the Python interpreter when it exists and `.venv/bin/python` does not
    Given a Python interpreter `venv/bin/python`
    When the person runs `tools probe`
    Then `tools` prints the Python interpreter `venv/bin/python`

  @g4 @r4
  Scenario: `$VIRTUAL_ENV/bin/python` is the Python interpreter when there is no project virtualenv
    Given a Python interpreter `$VIRTUAL_ENV/bin/python`
    When the person runs `tools probe`
    Then `tools` prints the Python interpreter `$VIRTUAL_ENV/bin/python`

  @g5 @r5
  Scenario: the Python interpreter running the script is the Python interpreter when there is no other
    Given a Python interpreter `sys.executable`
    When the person runs `tools probe`
    Then `tools` prints the Python interpreter `sys.executable`

  @g6 @r6 @r7
  Scenario: `.venv/bin/python` comes before `venv/bin/python`
    Given a Python interpreter `venv/bin/python`
    And a Python interpreter `.venv/bin/python`
    And a Python interpreter `.venv/bin/python`
    And a Python interpreter `venv/bin/python`
    When the person runs `tools probe`
    Then `tools` prints the Python interpreter `.venv/bin/python`
    And `tools` does not print the Python interpreter `venv/bin/python`

  @g7 @r8 @r9
  Scenario: `tools probe` prints each analysis tool and the Python interpreter
    Given an analysis tool a1
    When the person runs `tools probe`
    Then `tools` prints the analysis tool a1 and the Python interpreter
    And `tools` exits successfully

  @g8 @r10
  Scenario: `tools probe` exits with an error naming a missing analysis tool
    Given an analysis tool `vulture` that is `missing`
    When the person runs `tools probe`
    Then `tools` exits with an error naming the analysis tool `vulture`

  @g9 @r11
  Scenario: `tools probe --log` prints one line for a researcher's notes
    Given an analysis tool a1
    When the person runs `tools probe --log`
    Then `tools` prints "Probe: tools ->" and the analysis tool a1

  @g10 @r12 @r13
  Scenario: `tools install` installs a missing analysis tool and changes no dependency file
    Given a Python interpreter `.venv/bin/python` that is `virtualenv`
    And the dependency file `requirements.txt` holds "pytest"
    And an analysis tool a1 that is `missing`
    And an analysis tool a2 that is `installed`
    When the person runs `tools install`
    Then `tools` installs the analysis tool a1
    And `tools` does not install the analysis tool a2
    And `tools` changes nothing

  @g11 @r14
  Scenario: `tools install` installs the one version of ruff the plugin pins
    Given an analysis tool `ruff` that is `missing`
    And a Python interpreter `.venv/bin/python` that is `virtualenv`
    When the person runs `tools install`
    Then `tools` installs `ruff==0.17.0`

  @g12 @r15 @r16
  Scenario: `tools install` installs nothing into a Python interpreter that is not a virtualenv
    Given an analysis tool `jedi` that is `missing`
    And a Python interpreter `.venv/bin/python` that is `system`
    When the person runs `tools install`
    Then `tools` does not install `jedi`
    And `tools` exits with an error naming the analysis tool `jedi`

  @g13 @r17 @r44
  Scenario: an analysis tool still missing after `tools install` is printed with the failed command
    Given an analysis tool `jedi` that is `uninstallable`
    And a Python interpreter `.venv/bin/python` that is `virtualenv`
    When the person runs `tools install`
    Then `tools` exits with an error naming the analysis tool `jedi`
    And `tools` prints `pip install`

  @g14 @r18 @r19
  Scenario: `tools map` writes the coverage map whether or not the tests pass
    Given a test `test_fails`
    When the person runs `tools map`
    Then `tools` replaces `.shop/scratch/tools/coverage`
    And `tools` exits successfully

  @g15 @r20
  Scenario: `tools map` replaces the coverage map made before
    Given a coverage map m1
    When the person runs `tools map`
    Then `tools` replaces the coverage map m1

  @g16 @r21
  Scenario: `tools map --json` prints the map commit and the number of tests
    Given `--json` is given
    When the person runs `tools map`
    Then `tools` prints the map commit and the number of tests

  @g17 @r22
  Scenario: `tools tests-of` prints each test that executed its target
    Given a coverage map m1
    And a test t1
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` prints the test t1, the number of tests and the map commit

  @g18 @r23
  Scenario: `tools tests-of --by-file` prints a count for each test file
    Given a coverage map m1
    And a Python file `tests/test_cart.py`
    And `--by-file` is given
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` prints the Python file `tests/test_cart.py` and the number of tests

  @g19 @r24 @r25
  Scenario: `tools tests-of` says that no test executed its target, and exits successfully
    Given a coverage map m1
    When the person runs `tools tests-of src/cart.py:refund`
    Then `tools` prints "no test of the map executed" and the map commit
    And `tools` exits successfully

  @g20 @r26
  Scenario: `tools tests-of --json` prints the tests, their number and the map commit
    Given a coverage map m1
    And `--json` is given
    And a test t1
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` prints the test t1, the number of tests and the map commit

  @g21 @r27
  Scenario: `tools tests-of` refuses a function its file does not have
    Given a coverage map m1
    When the person runs `tools tests-of src/cart.py:absent`
    Then `tools` exits with an error naming `src/cart.py:absent`
    And `tools` changes nothing

  @g22 @r28
  Scenario: `tools tests-of` refuses when there is no coverage map
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` exits with an error naming `tools map`
    And `tools` changes nothing

  @g23 @r29 @r30
  Scenario: `tools untested` prints each function no test executed
    Given a coverage map m1
    And a function `refund`
    When the person runs `tools untested src/cart.py`
    Then `tools` prints the function `refund`, the number of functions and the map commit
    And `tools` exits successfully

  @g24 @r31
  Scenario: `tools untested --json` prints the functions, their number and the map commit
    Given a coverage map m1
    And a function `refund`
    And `--json` is given
    When the person runs `tools untested src/cart.py`
    Then `tools` prints the function `refund`, the number of functions and the map commit

  @g25 @r32
  Scenario: `tools refs` prints each reference and a summary
    Given a reference `src/shop.py:4`
    When the person runs `tools refs total`
    Then `tools` prints the reference `src/shop.py:4` and the number of references

  @g26 @r33
  Scenario: `tools refs --json` prints the references and the summary
    Given a reference `src/shop.py:4`
    And `--json` is given
    When the person runs `tools refs total`
    Then `tools` prints the reference `src/shop.py:4` and the number of references

  @g27 @r34
  Scenario: `tools refs` refuses a name the project does not define
    When the person runs `tools refs nowhere`
    Then `tools` exits with an error naming `nowhere`
    And `tools` changes nothing

  @g28 @r35 @r36
  Scenario: `tools check` prints each finding under its tool's heading
    Given a finding `F401`
    When the person runs `tools check src`
    Then `tools` prints the finding `F401` and "== ruff =="
    And `tools` exits with an error naming the finding `F401`

  @g29 @r37
  Scenario: `tools check` names a missing analysis tool
    Given an analysis tool `vulture` that is `missing`
    When the person runs `tools check src`
    Then `tools` exits with an error naming the analysis tool `vulture`

  @g30 @r38 @r45
  Scenario: `tools tests-of` names a missing coverage as missing
    Given an analysis tool `coverage` that is `missing`
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` exits with an error naming the analysis tool `coverage`
    And `tools` prints `tools install`

  @g31 @r39 @r46
  Scenario: `tools refs` names a missing jedi as missing
    Given an analysis tool `jedi` that is `missing`
    When the person runs `tools refs total`
    Then `tools` exits with an error naming the analysis tool `jedi`
    And `tools` prints `tools install`

  @g32 @r40 @r41
  Scenario: `tools size` prints each tracked Python file over the limit and exits with an error
    Given the Python file `big.py` holds:
      """
      a = 1
      b = 2
      c = 3
      d = 4
      """
    When the person runs `tools size --limit 3`
    Then `tools` prints the Python file `big.py`
    And `tools` exits with an error naming the Python file `big.py`

  @g33 @r42
  Scenario: `tools size` counts a file with a `python` shebang as a Python file
    Given the Python file `bin/tool` holds:
      """
      #!/usr/bin/env python3
      a = 1
      b = 2
      c = 3
      """
    When the person runs `tools size --limit 3`
    Then `tools` exits with an error naming the Python file `bin/tool`

  @g34 @r43
  Scenario: `tools size` takes 300 lines as the limit when none is given
    Given the Python file `big.py` holds:
      """
      a = 1
      b = 2
      c = 3
      d = 4
      """
    When the person runs `tools size`
    Then `tools` exits successfully
