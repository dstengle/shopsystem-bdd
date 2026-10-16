# formulated from spec/capabilities/analysis-tools.md
Feature: Analysis tools
  Narrator: an agent researching or reviewing a project's code

  @r1
  Scenario Outline: the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one
    Pins the order in which tools picks its interpreter, and that probe says which one it picked and why.
    Given a Python project in the current directory
    And <setting>
    When the agent runs `tools probe <option>`
    Then tools prints the path of <interpreter>
    And it says the interpreter came from <source>

    Examples:
      | setting                                                                                                                                      | option                      | interpreter                                      | source                   |
      | the project has .venv/bin/python and venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python                              | --python /opt/py/bin/python | /opt/py/bin/python                               | --python                 |
      | the project has .venv/bin/python and venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python                              |                             | the .venv/bin/python under the current directory | the project's virtualenv |
      | the project has venv/bin/python and no .venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python                           |                             | the venv/bin/python under the current directory  | the project's virtualenv |
      | the project has neither .venv/bin/python nor venv/bin/python, and $VIRTUAL_ENV points at /opt/env, outside the project, which has bin/python |                             | /opt/env/bin/python                              | the project's virtualenv |
      | the project has neither .venv/bin/python nor venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has no bin/python                   |                             | the interpreter running the script               | neither                  |

  @r2
  Scenario: a project that is not a Python project has no known analysis tools
    Pins that tools names the gap in one line and fails rather than guessing at another language's tools.
    Given a project with no Python in it
    When the agent runs `tools probe`
    Then tools says in one line that no analysis tools are known for the project's language
    And it exits 1

  @r3
  Scenario: probe lists each tool, its version or that it is missing, and the interpreter
    Pins the probe's report and that one missing tool fails it.
    Given a Python project whose interpreter has every tool but vulture
    When the agent runs `tools probe`
    Then tools prints one line for each tool
    And each installed tool's line gives its name and version
    And vulture's line says it is missing and what it is for
    And the interpreter is printed after the tools
    And it exits 1

  @r4
  Scenario: probe with --log prints the one line to give plan log
    Pins that the log form is a single Probe line and nothing else.
    Given a Python project
    When the agent runs `tools probe --log`
    Then tools prints exactly one line, and it begins `Probe: tools -> `

  @r5
  Scenario: install puts each missing tool into the interpreter and leaves dependency files alone
    Pins that install changes the interpreter only, never the project's declared dependencies.
    Given a Python project with a pyproject.toml and a requirements.txt
    And its interpreter is a virtualenv missing jedi and vulture
    When the agent runs `tools install`
    Then jedi and vulture are installed into the interpreter with pip
    And pyproject.toml and requirements.txt are unchanged

  @r6
  Scenario: install refuses an interpreter that is not a virtualenv
    Pins that install never puts tools into an interpreter outside a virtualenv.
    Given a Python project whose interpreter is not a virtualenv and is missing jedi
    When the agent runs `tools install`
    Then the install is refused because the interpreter is not a virtualenv
    And jedi is still missing from the interpreter

  @r7
  Scenario: a tool still missing after install is reported with the failed command
    Pins what the agent is told when an install attempt does not take.
    Given a Python project whose interpreter is a virtualenv missing jedi
    And installing jedi with pip fails
    When the agent runs `tools install`
    Then tools prints jedi, what it is for and what the workflow does without it
    And it prints the command that failed with the end of its error
    And it exits 1

  @r8
  Scenario: map runs the suite once under coverage and keeps the map
    Pins that one run records which test executed which code, with the agent's pytest arguments honoured.
    Given a Python project with the tests test_total and test_discount
    When the agent runs `tools map -- -k test_total`
    Then the suite is run once under coverage with a context for each test
    And only test_total is run
    And the map is kept in `.superpowers/tools/coverage`

  @r9
  Scenario Outline: tests-of lists the tests that executed a target in the last map
    Pins the answer for each form of target, with the share of the map's tests and the map's commit.
    Given a map of 5 tests made at commit abc1234
    And test_total and test_checkout executed <target> and no other test did
    When the agent runs `tools tests-of <argument>`
    Then tools prints test_total and test_checkout, one a line
    And it says that is 2 of the map's 5 tests
    And it gives commit abc1234

    Examples:
      | target                           | argument                     |
      | the file src/cart.py             | src/cart.py                  |
      | the function total               | src/cart.py:total            |
      | the method Cart.total            | src/cart.py:Cart.total       |
      | lines 10 to 20 of src/cart.py    | src/cart.py:10-20            |

  @r10
  Scenario: tests-of with --by-file counts tests per test file
    Pins that --by-file groups the answer by test file in place of listing tests.
    Given a map in which two tests in tests/test_cart.py and one test in tests/test_checkout.py executed src/cart.py
    When the agent runs `tools tests-of --by-file src/cart.py`
    Then tools prints tests/test_cart.py with 2 and tests/test_checkout.py with 1
    And it prints no test names

  @r11
  Scenario Outline: tests-of fails when nothing executed the target or the function does not exist
    Pins that an empty answer and an unknown function both fail.
    Given a map has been made
    And <situation>
    When the agent runs `tools tests-of <argument>`
    Then it exits 1

    Examples:
      | situation                                             | argument            |
      | no test in the map executed the function unused       | src/cart.py:unused  |
      | src/cart.py has no function named missing             | src/cart.py:missing |

  @r12
  Scenario: tests-of without a map says to make one
    Pins that tests-of does not answer before a map exists.
    Given a Python project for which no map has been made
    When the agent runs `tools tests-of src/cart.py`
    Then the command is refused because no map has been made
    And it says to make one with `tools map`

  @r13
  Scenario: untested lists the functions no test executed
    Pins that untested reports, across every file given, the functions the last map shows no test ran.
    Given a map in which no test executed the function refund in src/cart.py or the function export in src/report.py
    And every other function in those files was executed by a test
    When the agent runs `tools untested src/cart.py src/report.py`
    Then tools prints refund and export
    And it prints no other function

  @r14
  Scenario: refs prints each reference as path:line, through imports and aliases, then one summary line
    Pins that a use under another file's import or an alias is still found, and that the summary keeps production and test files apart.
    Given a Python project that defines the function total in src/cart.py
    And src/checkout.py imports total and calls it
    And src/report.py imports total under the alias cart_total and calls cart_total
    And tests/test_cart.py imports total and calls it
    When the agent runs `tools refs total`
    Then tools prints each reference as `path:line`
    And the references printed include the calls in src/checkout.py, src/report.py and tests/test_cart.py
    And then it prints one summary line giving the number of references printed, 2 production files, 1 test file, and src/cart.py as where total is defined

  @r15
  Scenario: refs fails for a name the project does not define
    Pins that a name with no definition in the project fails.
    Given a Python project in which nothing is defined as `nowhere`
    When the agent runs `tools refs nowhere`
    Then it exits 1

  @r16
  Scenario Outline: check runs each tool under its own heading and fails when any reports
    Pins which tools check runs over the paths given, and that a report from any one fails it.
    Given a Python project with import contracts
    And <tool> reports a finding in src/cart.py and the other tools report nothing
    When the agent runs `tools check src/cart.py`
    Then tools prints a heading for ruff, for vulture and for import-linter, each over src/cart.py
    And <tool>'s finding is under <tool>'s heading
    And it exits 1

    Examples:
      | tool          |
      | ruff          |
      | vulture       |
      | import-linter |

  @r17
  Scenario: check names a missing tool under its heading
    Pins that a missing tool is reported, not silently skipped.
    Given a Python project whose interpreter is missing vulture
    When the agent runs `tools check src/cart.py`
    Then under the vulture heading tools says vulture is missing

  @r18
  Scenario: install outside a virtualenv explains each missing tool and installs nothing
    Pins what the agent is told about each missing tool when the interpreter cannot be installed into.
    Given a Python project whose interpreter is not a virtualenv and is missing jedi and vulture
    When the agent runs `tools install`
    Then nothing is installed into the interpreter
    And for jedi and for vulture tools prints the tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv
    And it exits 1

  @r19
  Scenario Outline: install with every tool present says so and succeeds
    Pins that nothing to install is success, virtualenv or not.
    Given a Python project whose interpreter <kind> and has every tool
    When the agent runs `tools install`
    Then tools says every tool is present
    And it exits 0

    Examples:
      | kind                  |
      | is a virtualenv       |
      | is not a virtualenv   |

  @r20
  Scenario: install says each tool it installed
    Pins that a successful install is reported per tool.
    Given a Python project whose interpreter is a virtualenv missing jedi
    And jedi installs with pip
    When the agent runs `tools install`
    Then tools prints that jedi is installed

  @r21
  Scenario Outline: an interpreter that does not run is refused
    Pins that probe, install and check stop at an interpreter that fails, and say why.
    Given a Python project
    And `--python` names an interpreter that fails when run
    When the agent runs `tools <command>`
    Then the command is refused because the interpreter does not run
    And it names the interpreter and the end of its error

    Examples:
      | command             |
      | probe               |
      | install             |
      | check src/cart.py   |

  @r22
  Scenario: the probe log line names every tool with its version or missing
    Pins the content of the Probe line.
    Given a Python project whose interpreter has every tool but vulture
    When the agent runs `tools probe --log`
    Then the line names each installed tool with its version
    And it names vulture as `missing`

  @r23
  Scenario Outline: map replaces the earlier map and succeeds whether or not the tests pass
    Pins that a failing suite still yields a map, and what map prints about it.
    Given a Python project with a map made at an earlier commit
    And the project is at commit def5678 and its suite <outcome>
    When the agent runs `tools map`
    Then the earlier map is replaced by one made at commit def5678
    And tools prints pytest's last line, where the map is and commit def5678
    And it exits 0

    Examples:
      | outcome         |
      | passes          |
      | has a failure   |

  @r24
  Scenario: map that makes no map is refused
    Pins that a run leaving no map is not reported as success.
    Given a Python project in which running the suite under coverage leaves no map
    When the agent runs `tools map`
    Then the command is refused because no map was made
    And it names the command it ran and the end of its output

  @r25
  Scenario Outline: untested prints each function with its place, the count and the commit
    Pins untested's report and that finding untested functions is not a failure.
    Given a map made at commit abc1234 in which no test executed <count> functions in src/cart.py
    When the agent runs `tools untested src/cart.py`
    Then tools prints each of those functions as `<path>:<line> <name>`
    And it says <count> functions no test executed and gives commit abc1234
    And it exits 0

    Examples:
      | count |
      | 0     |
      | 2     |

  @r26
  Scenario: untested without a map says to make one
    Pins that untested does not answer before a map exists.
    Given a Python project for which no map has been made
    When the agent runs `tools untested src/cart.py`
    Then the command is refused because no map has been made
    And it says to make one with `tools map`

  @r27
  Scenario Outline: without coverage tests-of and untested say to install it
    Pins that the map readers stop and point to install when coverage is missing.
    Given a Python project whose interpreter is missing coverage
    When the agent runs `tools <command>`
    Then the command is refused because coverage is missing from the interpreter
    And it says to run `tools install`

    Examples:
      | command                |
      | tests-of src/cart.py   |
      | untested src/cart.py   |

  @r28
  Scenario: without jedi refs says to install it
    Pins that refs stops and points to install when jedi is missing.
    Given a Python project whose interpreter is missing jedi
    When the agent runs `tools refs total`
    Then the command is refused because jedi is missing from the interpreter
    And it says to run `tools install`

  @r29
  Scenario: tests-of on a file that does not exist is refused
    Pins that an absent file is named, not treated as untested.
    Given a map has been made
    And the project has no file src/gone.py
    When the agent runs `tools tests-of src/gone.py`
    Then the command is refused because src/gone.py does not exist
    And it names src/gone.py

  @r30
  Scenario Outline: refs on a defined name gives its definition apart from its references
    Pins that the definition is named but not counted, and that any number of references is success.
    Given a Python project that defines the function total in src/cart.py and refers to it <count> times
    When the agent runs `tools refs total`
    Then tools names src/cart.py as where total is defined
    And the definition is not counted as a reference
    And <count> references are printed
    And it exits 0

    Examples:
      | count |
      | 0     |
      | 3     |

  @r31
  Scenario: check with --base checks the changed Python files that remain, in place of the paths given
    Pins which files --base selects: Python, changed since the base, not deleted.
    Given a Python project in git with base commit abc1234
    And since abc1234 src/cart.py and README.md have changed and src/old.py has been deleted
    When the agent runs `tools check --base abc1234 src/report.py`
    Then tools checks src/cart.py
    And it does not check README.md, src/old.py or src/report.py

  @r32
  Scenario: check with a base git cannot compare is refused with git's error
    Pins that a bad base stops the check and passes git's own reason on.
    Given a Python project in git with no ref named nosuchref
    When the agent runs `tools check --base nosuchref`
    Then the command is refused because git cannot compare the working tree with nosuchref
    And it prints git's error

  @r33
  Scenario: check with no file to check says so under ruff and vulture and does not fail for them
    Pins that an empty selection is not a finding.
    Given a Python project in git whose Python files are unchanged since base commit abc1234
    When the agent runs `tools check --base abc1234`
    Then under the ruff heading and under the vulture heading tools says there is nothing to check
    And neither ruff nor vulture makes it exit 1

  @r34
  Scenario: check without import contracts does not run import-linter
    Pins that import-linter is skipped, visibly, when the project states no contracts.
    Given a Python project that states no import contracts
    When the agent runs `tools check src/cart.py`
    Then under the import-linter heading tools says the project states no import contracts
    And import-linter is not run

  @r35
  Scenario: a tool that prints nothing is reported clean
    Pins that silence from a tool is shown as clean rather than as an empty heading.
    Given a Python project in which ruff prints nothing for src/cart.py
    When the agent runs `tools check src/cart.py`
    Then under the ruff heading tools says it is clean
