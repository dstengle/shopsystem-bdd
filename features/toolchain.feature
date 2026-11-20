# generated from spec/capabilities/toolchain.md by features generate; do not edit
Feature: Toolchain
  Narrator: the person

  @g1 @r1
  Scenario: A probe with a Python interpreter gives that interpreter
    Given a Python interpreter p1
    When the person probes this toolchain with the Python interpreter p1
    Then the toolchain service returns the Python interpreter p1

  @g2 @r2
  Scenario: A probe finds the `.venv` interpreter first
    Given the `.venv/bin/python` Python interpreter exists
    When the person probes this toolchain without a Python interpreter
    Then the toolchain service returns `.venv/bin/python`

  @g3 @r3
  Scenario: A probe finds the `venv` interpreter when there is no `.venv` one
    Given the `venv/bin/python` Python interpreter exists
    And the `.venv/bin/python` Python interpreter does not exist
    When the person probes this toolchain without a Python interpreter
    Then the toolchain service returns `venv/bin/python`

  @g4 @r4
  Scenario: A probe finds the active virtualenv's interpreter when there is no local one
    Given the `$VIRTUAL_ENV/bin/python` Python interpreter exists
    And the `.venv/bin/python` Python interpreter does not exist
    And the `venv/bin/python` Python interpreter does not exist
    When the person probes this toolchain without a Python interpreter
    Then the toolchain service returns `$VIRTUAL_ENV/bin/python`

  @g5 @r5
  Scenario: A probe falls back to the interpreter that executes the tools
    Given the `.venv/bin/python` Python interpreter does not exist
    And the `venv/bin/python` Python interpreter does not exist
    And the `$VIRTUAL_ENV/bin/python` Python interpreter does not exist
    When the person probes this toolchain without a Python interpreter
    Then the toolchain service returns the Python interpreter p1
    And the Python interpreter p1 executes `scripts/tools`

  @g6 @r6
  Scenario: A probe does not give the `venv` interpreter beside a `.venv` one
    Given the `.venv/bin/python` Python interpreter exists
    And the `venv/bin/python` Python interpreter exists
    When the person probes this toolchain without a Python interpreter
    Then the toolchain service does not return `venv/bin/python`

  @g7 @r7
  Scenario: A probe with no missing analysis tool gives every analysis tool
    Given no analysis tool whose presence is `missing` exists
    And an analysis tool a1
    And an analysis tool a2
    When the person probes this toolchain
    Then the toolchain service returns the analysis tool a1
    And the toolchain service returns the analysis tool a2
    And the toolchain service completes this request

  @g8 @r8
  Scenario: A probe with a missing analysis tool fails naming it
    Given an analysis tool a1
    And the presence of the analysis tool a1 is `missing`
    When the person probes this toolchain
    Then the toolchain service fails this check
    And the toolchain service names the analysis tool a1

  @g9 @r9
  Scenario: A probe with the log gives one log line and every analysis tool
    Given a log line l1
    And a log line l2
    And an analysis tool a1
    And an analysis tool a2
    When the person probes this toolchain with the log
    Then the toolchain service returns one log line
    And the toolchain service returns the analysis tool a1
    And the toolchain service returns the analysis tool a2

  @g10 @r10
  Scenario: An install in a virtualenv installs every missing analysis tool and changes no dependency file
    Given the dependency file `requirements.txt` holds "pytest"
    And the environment of this Python interpreter is `virtualenv`
    And an analysis tool a1
    And the presence of the analysis tool a1 is `missing`
    And an analysis tool a2
    And the presence of the analysis tool a2 is `missing`
    And an analysis tool a3
    And the presence of the analysis tool a3 is `installed`
    When the person installs this toolchain
    Then the toolchain service installs the analysis tool a1
    And the toolchain service installs the analysis tool a2
    And the toolchain service does not install the analysis tool a3
    And the toolchain service does not change a dependency file

  @g11 @r11
  Scenario: An install installs the version of `ruff` the plugin pins
    Given the presence of `ruff` is `missing`
    And the environment of this Python interpreter is `virtualenv`
    When the person installs this toolchain
    Then the toolchain service installs the version v1
    And `ruff` has the version v1
    And this plugin pins the version v1

  @g12 @r12
  Scenario: An install outside a virtualenv is refused
    Given an analysis tool a1
    And the presence of the analysis tool a1 is `missing`
    And the environment of this Python interpreter is `system`
    When the person installs this toolchain
    Then the toolchain service refuses this request
    And the toolchain service names the analysis tool a1

  @g13 @r13
  Scenario: An install of an uninstallable analysis tool gives its pip command and is refused
    Given an analysis tool a1
    And the presence of the analysis tool a1 is `uninstallable`
    And the environment of this Python interpreter is `virtualenv`
    When the person installs this toolchain
    Then the toolchain service returns the pip command p1
    And the analysis tool a1 has the pip command p1
    And the toolchain service refuses this request
    And the toolchain service names the analysis tool a1

  @g14 @r14
  Scenario: A function is not traced while `coverage` is missing
    Given the presence of `coverage` is `missing`
    And a function f1
    When the person traces the function f1
    Then the code analysis service refuses this request
    And the code analysis service names `coverage`

  @g15 @r15
  Scenario: An identifier is not located while `jedi` is missing
    Given the presence of `jedi` is `missing`
    And an identifier i1
    When the person locates the identifier i1
    Then the code analysis service refuses this request
    And the code analysis service names `jedi`

  @g16 @r16
  Scenario: An install in a virtualenv installs a missing `gf-rgl`
    Given the presence of `gf-rgl` is `missing`
    And the environment of this Python interpreter is `virtualenv`
    When the person installs this toolchain
    Then the toolchain service installs `gf-rgl`

  @g17 @r17
  Scenario: A probe gives `gf-rgl`
    When the person probes this toolchain
    Then the toolchain service returns `gf-rgl`

  @g18 @r18
  Scenario: An install in a repository with no Python file installs `gf-rgl`
    Given no Python file exists
    And the presence of `gf-rgl` is `missing`
    And the environment of this Python interpreter is `virtualenv`
    When the person installs this toolchain
    Then the toolchain service installs `gf-rgl`
    And the toolchain service completes this request

  @g19 @r19
  Scenario: A probe in a repository with no Python file gives `gf-rgl`
    Given no Python file exists
    When the person probes this toolchain
    Then the toolchain service returns `gf-rgl`
    And the toolchain service completes this request
