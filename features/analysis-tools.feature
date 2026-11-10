# generated from spec/capabilities/analysis-tools.md by features generate; do not edit
Feature: Analysis tools
  Narrator: a session researching or reviewing a project's code

  @g1 @r1
  Scenario: `--python` gives the Python interpreter
    Given `--python` is given
    When the person runs `tools probe`
    Then `tools` prints `--python`

  @g2 @r2
  Scenario: `.venv/bin/python` is the Python interpreter when it exists
    Given the Python interpreter `.venv/bin/python` is present
    When the person runs `tools probe`
    Then `tools` prints `.venv/bin/python`

  @g3 @r3
  Scenario: `venv/bin/python` is the Python interpreter when it exists and `.venv/bin/python` does not
    Given the Python interpreter `venv/bin/python` is present
    And the Python interpreter `.venv/bin/python` is not present
    When the person runs `tools probe`
    Then `tools` prints `venv/bin/python`

  @g4 @r4
  Scenario: `$VIRTUAL_ENV/bin/python` is the Python interpreter when there is no project virtualenv
    Given the Python interpreter `$VIRTUAL_ENV/bin/python` is present
    And the Python interpreter `.venv/bin/python` is not present
    And the Python interpreter `venv/bin/python` is not present
    When the person runs `tools probe`
    Then `tools` prints `$VIRTUAL_ENV/bin/python`

  @g5 @r5
  Scenario: the Python interpreter running the script is the Python interpreter when there is no other
    Given the Python interpreter `.venv/bin/python` is not present
    And the Python interpreter `venv/bin/python` is not present
    And the Python interpreter `$VIRTUAL_ENV/bin/python` is not present
    When the person runs `tools probe`
    Then `tools` prints `sys.executable`

  @g6 @r6
  Scenario: `.venv/bin/python` comes before `venv/bin/python`
    Given the Python interpreter `.venv/bin/python` is present
    And the Python interpreter `venv/bin/python` is present
    When the person runs `tools probe`
    Then `tools` prints `.venv/bin/python`
    And `tools` does not print `venv/bin/python`

  @g7 @r7
  Scenario: `tools probe` prints each analysis tool and the Python interpreter
    When the person runs `tools probe`
    Then `tools` prints the analysis tool a1
    And `tools` exits successfully

  @g8 @r8
  Scenario: `tools probe` exits with an error naming a missing analysis tool
    Given an analysis tool a1 that is `missing`
    When the person runs `tools probe`
    Then `tools` exits with an error naming the analysis tool a1

  @g9 @r9
  Scenario: `tools probe --log` prints one line for a researcher's notes
    When the person runs `tools probe --log`
    Then `tools` prints "Probe: tools ->"
    And `tools` prints the analysis tool a1

  @g10 @r10
  Scenario: `tools install` installs a missing analysis tool and changes no dependency file
    Given the dependency file `requirements.txt` holds "pytest"
    And the Python interpreter `.venv/bin/python` is `virtualenv`
    And an analysis tool a1 that is `missing`
    And an analysis tool a2 that is `installed`
    When the person runs `tools install`
    Then `tools` installs the analysis tool a1
    And `tools` changes nothing
    And `tools` does not install the analysis tool a2

  @g11 @r11
  Scenario: `tools install` installs the one version of ruff the plugin pins
    Given the analysis tool `ruff` is `missing`
    And the Python interpreter `.venv/bin/python` is `virtualenv`
    When the person runs `tools install`
    Then `tools` installs `ruff==0.17.0`

  @g12 @r12
  Scenario: `tools install` installs nothing into a Python interpreter that is not a virtualenv
    Given an analysis tool a1 that is `missing`
    And the Python interpreter `.venv/bin/python` is `system`
    When the person runs `tools install`
    Then `tools` does not install the analysis tool a1
    And `tools` exits with an error naming the analysis tool a1

  @g13 @r13
  Scenario: an analysis tool still missing after `tools install` is printed with the failed command
    Given an analysis tool a1 that is `uninstallable`
    And the Python interpreter `.venv/bin/python` is `virtualenv`
    When the person runs `tools install`
    Then `tools` prints `pip install`
    And `tools` exits with an error naming the analysis tool a1

  @g14 @r14
  Scenario: `tools map` writes the coverage map whether or not the tests pass
    Given a test t1
    And the test t1 is failing
    When the person runs `tools map`
    Then `tools` replaces the coverage map c1
    And `tools` exits successfully

  @g15 @r15
  Scenario: `tools map` replaces the coverage map made before
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools map`
    Then `tools` replaces the coverage map c1

  @g16 @r16
  Scenario: `tools map --json` prints the map commit and the number of tests
    Given `--json` is given
    When the person runs `tools map`
    Then `tools` prints the map commit m1
    And `tools` prints the number of tests

  @g17 @r17
  Scenario: `tools tests-of` prints each test that executed its target
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` prints the test t1
    And `tools` prints the number of tests
    And `tools` prints the map commit m1

  @g18 @r18
  Scenario: `tools tests-of --by-file` prints a count for each test file
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools tests-of src/cart.py:total --by-file`
    Then `tools` prints `tests/test_cart.py`
    And `tools` prints the number of tests

  @g19 @r19
  Scenario: `tools tests-of` says that no test executed its target, and exits successfully
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools tests-of src/cart.py:refund`
    Then `tools` prints "no test of the map executed"
    And `tools` prints the map commit m1
    And `tools` exits successfully

  @g20 @r20
  Scenario: `tools tests-of --json` prints the tests, their number and the map commit
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools tests-of src/cart.py:total --json`
    Then `tools` prints the test t1
    And `tools` prints the number of tests
    And `tools` prints the map commit m1

  @g21 @r21
  Scenario: `tools tests-of` refuses a function its file does not have
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools tests-of src/cart.py:absent`
    Then `tools` exits with an error naming `src/cart.py:absent`
    And `tools` changes nothing

  @g22 @r22
  Scenario: `tools tests-of` refuses when there is no coverage map
    Given a coverage map c1
    And the coverage map c1 is not present
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` exits with an error naming `tools map`
    And `tools` changes nothing

  @g23 @r23
  Scenario: `tools untested` prints each function no test executed
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools untested src/cart.py`
    Then `tools` prints `refund`
    And `tools` prints the number of functions
    And `tools` prints the map commit m1
    And `tools` exits successfully

  @g24 @r24
  Scenario: `tools untested --json` prints the functions, their number and the map commit
    Given a coverage map c1
    And the coverage map c1 is present
    When the person runs `tools untested src/cart.py --json`
    Then `tools` prints `refund`
    And `tools` prints the number of functions
    And `tools` prints the map commit m1

  @g25 @r25
  Scenario: `tools refs` prints each reference and a summary
    Given the Python file `src/shop.py` holds:
      """
      from cart import total
      print(total([1]))
      """
    When the person runs `tools refs total`
    Then `tools` prints `src/shop.py:2`
    And `tools` prints the number of references

  @g26 @r26
  Scenario: `tools refs --json` prints the references and the summary
    Given the Python file `src/shop.py` holds:
      """
      from cart import total
      print(total([1]))
      """
    And `--json` is given
    When the person runs `tools refs total`
    Then `tools` prints `src/shop.py:2`
    And `tools` prints the number of references

  @g27 @r27
  Scenario: `tools refs` refuses a name the project does not define
    When the person runs `tools refs nowhere`
    Then `tools` exits with an error naming `nowhere`
    And `tools` changes nothing

  @g28 @r28
  Scenario: `tools check` prints each finding under its tool's heading
    When the person runs `tools check src`
    Then `tools` prints `F401`
    And `tools` prints "== ruff =="
    And `tools` exits with an error naming `F401`

  @g29 @r29
  Scenario: `tools check` names a missing analysis tool
    Given the analysis tool `vulture` is `missing`
    When the person runs `tools check src`
    Then `tools` exits with an error naming `vulture`

  @g30 @r30
  Scenario: `tools tests-of` names a missing coverage as missing
    Given the analysis tool `coverage` is `missing`
    When the person runs `tools tests-of src/cart.py:total`
    Then `tools` prints `tools install`
    And `tools` exits with an error naming `coverage`

  @g31 @r31
  Scenario: `tools refs` names a missing jedi as missing
    Given the analysis tool `jedi` is `missing`
    When the person runs `tools refs total`
    Then `tools` prints `tools install`
    And `tools` exits with an error naming `jedi`

  @g32 @r32
  Scenario: `tools size` prints each tracked Python file over the limit, a `python` shebang included, and exits with an error
    Given the Python file `big.py` holds:
      """
      a = 1
      b = 2
      c = 3
      d = 4
      """
    And the Python file `bin/tool` holds:
      """
      #!/usr/bin/env python3
      a = 1
      b = 2
      c = 3
      """
    When the person runs `tools size --limit 3`
    Then `tools` prints `big.py`
    And `tools` prints `bin/tool`
    And `tools` exits with an error naming `bin/tool`

  @g33 @r33
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

  @g34 @r34
  Scenario: `tools install` installs the RGL
    Given the analysis tool `gf-rgl` is `missing`
    And the Python interpreter `.venv/bin/python` is `virtualenv`
    When the person runs `tools install`
    Then `tools` installs `gf-rgl`

  @g35 @r35
  Scenario: `tools probe` reports the RGL
    When the person runs `tools probe`
    Then `tools` prints `gf-rgl`
