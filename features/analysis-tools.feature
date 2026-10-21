# formulated from spec/capabilities/analysis-tools.md
Feature: Analysis tools
  Narrator: a session researching or reviewing a project's code

  @r1 @r3
  Scenario Outline: the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one
    Pins the order in which tools picks its interpreter, and that probe says which one it picked and why.
    Given a Python project in the current directory
    And <setting>
    When the session runs `tools probe <option>`
    Then tools prints the path of <interpreter>
    And it says the interpreter came from <source>

    Examples:
      | setting                                                                                                                                      | option                      | interpreter                                      | source                   |
      | the project has .venv/bin/python and venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python                              | --python /opt/py/bin/python | /opt/py/bin/python                               | --python                 |
      | the project has .venv/bin/python and venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python                              |                             | the .venv/bin/python under the current directory | the project's virtualenv |
      | the project has venv/bin/python and no .venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python                           |                             | the venv/bin/python under the current directory  | the project's virtualenv |
      | the project has neither .venv/bin/python nor venv/bin/python, and $VIRTUAL_ENV points at /opt/env, outside the project, which has bin/python |                             | /opt/env/bin/python                              | the project's virtualenv |
      | the project has neither .venv/bin/python nor venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has no bin/python                   |                             | the interpreter running the script               | neither                  |

  @r49
  Scenario: a project that is not a Python project has no known analysis tools
    Pins that tools names the gap in one line and fails rather than guessing at another language's tools.
    Given a project with no Python in it
    When the session runs `tools probe`
    Then tools says in one line that no analysis tools are known for its language
    And it exits 1

  @r3
  Scenario: probe lists each tool, its version or that it is missing, and the interpreter
    Pins the probe's output and that one missing tool fails it.
    Given a Python project whose interpreter has every tool but vulture
    When the session runs `tools probe`
    Then tools prints one line for each tool
    And each installed tool's line gives its name and version
    And vulture's line says it is missing and what it is for
    And the interpreter is printed after the tools
    And it exits 1

  @r4
  Scenario: probe with --log prints the one line for a researcher's notes
    Pins that the log form is a single Probe line and nothing else.
    Given a Python project
    When the session runs `tools probe --log`
    Then tools prints exactly one line, and it begins `Probe: tools -> `

  @r5
  Scenario: install puts each missing tool into the interpreter and leaves dependency files alone
    Pins that install changes the interpreter only, never the project's declared dependencies.
    Given a Python project with a pyproject.toml and a requirements.txt
    And its interpreter is a virtualenv missing jedi and vulture
    When the session runs `tools install`
    Then jedi and vulture are installed into the interpreter with pip
    And pyproject.toml and requirements.txt are unchanged

  @r6
  Scenario: install refuses an interpreter that is not a virtualenv
    Pins that install never puts tools into an interpreter outside a virtualenv.
    Given a Python project whose interpreter is not a virtualenv and is missing jedi
    When the session runs `tools install`
    Then the install is refused because the interpreter is not a virtualenv
    And jedi is still missing from the interpreter

  @r7
  Scenario: a tool still missing after install is printed with the failed command
    Pins what the session is told when an install attempt does not take.
    Given a Python project whose interpreter is a virtualenv missing jedi
    And installing jedi with pip fails
    When the session runs `tools install`
    Then tools prints jedi, what it is for and what the workflow does without it
    And it prints the command that failed with the end of its error
    And it exits 1

  @r8
  Scenario: map runs the suite once under coverage and keeps the map
    Pins that one map keeps which test executed which code, with the session's pytest arguments honoured.
    Given a Python project with the tests test_total and test_discount
    When the session runs `tools map -- -k test_total`
    Then the suite is run once under coverage with a context for each test
    And only test_total is run
    And the map is kept in `.shop/scratch/tools/coverage`

  @r9
  Scenario Outline: tests-of lists the tests that executed a target in the last map
    Pins the answer for each form of target, with the share of the map's tests and the map's commit.
    Given a map of 5 tests made at commit abc1234
    And test_total and test_checkout executed <target> and no other test did
    When the session runs `tools tests-of <argument>`
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
    When the session runs `tools tests-of --by-file src/cart.py`
    Then tools prints tests/test_cart.py with 2 and tests/test_checkout.py with 1
    And it prints no test names

  @r11
  Scenario Outline: tests-of fails when nothing executed the target or the function does not exist
    Pins that an empty answer and an unknown function both fail.
    Given a map has been made
    And <situation>
    When the session runs `tools tests-of <argument>`
    Then it exits 1

    Examples:
      | situation                                             | argument            |
      | no test in the map executed the function unused       | src/cart.py:unused  |
      | src/cart.py has no function named missing             | src/cart.py:missing |

  @r49
  Scenario: tests-of without a map says to make one
    Pins that tests-of does not answer before a map exists.
    Given a Python project for which no map has been made
    When the session runs `tools tests-of src/cart.py`
    Then the command is refused because no map has been made
    And it says to make one with `tools map`

  @r13
  Scenario: untested lists the functions no test executed
    Pins that untested prints, across every file given, the functions the last map shows no test ran.
    Given a map in which no test executed the function refund in src/cart.py or the function export in src/report.py
    And every other function in those files was executed by a test
    When the session runs `tools untested src/cart.py src/report.py`
    Then tools prints refund and export
    And it prints no other function

  @r14
  Scenario: refs prints each reference as path:line, through imports and aliases, then one summary line
    Pins that a use under another file's import or an alias is still found, and that the summary keeps production and test files apart.
    Given a Python project that defines the function total in src/cart.py
    And src/checkout.py imports total and calls it
    And src/report.py imports total under the alias cart_total and calls cart_total
    And tests/test_cart.py imports total and calls it
    When the session runs `tools refs total`
    Then tools prints each reference as `path:line`
    And the references printed include the calls in src/checkout.py, src/report.py and tests/test_cart.py
    And then it prints one summary line giving the number of references printed, 2 production files, 1 test file, and src/cart.py as where total is defined

  @r49
  Scenario: refs fails for a name the project does not define
    Pins that a name with no definition in the project fails.
    Given a Python project in which nothing is defined as `nowhere`
    When the session runs `tools refs nowhere`
    Then it exits 1
    And it says nothing in the project is defined as nowhere

  @r16
  Scenario Outline: `tools check` runs each tool under its own heading and fails when any finds something
    Pins which tools `tools check` runs, over what, and that a finding from any one fails it.
    Given a Python project with import contracts
    And <tool> prints a finding and the other tools print nothing
    When the session runs `tools check src/cart.py`
    Then tools prints a heading for ruff, for vulture and for import-linter
    And ruff and vulture are run over src/cart.py and import-linter over the project
    And <tool>'s finding is under <tool>'s heading
    And it exits 1

    Examples:
      | tool          |
      | ruff          |
      | vulture       |
      | import-linter |

  @r17
  Scenario: `tools check` names a missing tool under its heading
    Pins that a missing tool is named, not silently skipped.
    Given a Python project whose interpreter is missing vulture
    When the session runs `tools check src/cart.py`
    Then under the vulture heading tools says vulture is missing

  @r6
  Scenario: install outside a virtualenv explains each missing tool and installs nothing
    Pins what the session is told about each missing tool when the interpreter cannot be installed into.
    Given a Python project whose interpreter is not a virtualenv and is missing jedi and vulture
    When the session runs `tools install`
    Then nothing is installed into the interpreter
    And for jedi and for vulture tools prints the tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv
    And it exits 1

  @r5
  Scenario Outline: install with every tool present says so and succeeds
    Pins that nothing to install is success, virtualenv or not.
    Given a Python project whose interpreter <kind> and has every tool
    When the session runs `tools install`
    Then tools says every tool is present
    And it exits 0

    Examples:
      | kind                  |
      | is a virtualenv       |
      | is not a virtualenv   |

  @r5
  Scenario: install says each tool it installed
    Pins that a successful install is printed per tool.
    Given a Python project whose interpreter is a virtualenv missing jedi
    And jedi installs with pip
    When the session runs `tools install`
    Then tools prints that jedi is installed

  @r49
  Scenario Outline: an interpreter that does not start is refused
    Pins that probe, install and `tools check` stop at an interpreter that fails, and say why.
    Given a Python project
    And `--python` names an interpreter that fails when run
    When the session runs `tools <command>`
    Then the command is refused because the interpreter does not start
    And it names the interpreter and the end of its error

    Examples:
      | command             |
      | probe               |
      | install             |
      | check src/cart.py   |

  @r4
  Scenario: the probe log line names every tool with its version or missing
    Pins the content of the Probe line.
    Given a Python project whose interpreter has every tool but vulture
    When the session runs `tools probe --log`
    Then the line names each installed tool with its version
    And it names vulture as `missing`

  @r8
  Scenario Outline: map replaces the earlier map and succeeds whether or not the tests pass
    Pins that a failing suite still yields a map, and what map prints about it.
    Given a Python project with a map made at an earlier commit
    And the project is at commit def5678 and its suite <ending>
    When the session runs `tools map`
    Then the earlier map is replaced by one made at commit def5678
    And tools prints pytest's last line, where the map is and commit def5678
    And it exits 0

    Examples:
      | ending          |
      | passes          |
      | has a failure   |

  @r49
  Scenario: map that makes no map is refused
    Pins that a `tools map` leaving no map is not shown as success.
    Given a Python project in which running the suite under coverage leaves no map
    When the session runs `tools map`
    Then the command is refused because no map was made
    And it names the command it ran and the end of its output

  @r49
  Scenario: map that makes no map keeps the map made before
    Pins that a refused map changes nothing: the last map and its commit stay.
    Given a Python project with a map made at commit abc1234
    And running the suite under coverage now leaves no map
    When the session runs `tools map`
    Then it exits 1
    And the map made at commit abc1234 is as it was

  @r13
  Scenario Outline: untested prints each function with its place, the count and the commit
    Pins untested's output and that finding untested functions is not a failure.
    Given a map made at commit abc1234 in which no test executed <count> functions in src/cart.py
    When the session runs `tools untested src/cart.py`
    Then tools prints each of those functions as `<path>:<line> <name>`
    And it says <count> functions no test executed and gives commit abc1234
    And it exits 0

    Examples:
      | count |
      | 0     |
      | 2     |

  @r49
  Scenario: untested without a map says to make one
    Pins that untested does not answer before a map exists.
    Given a Python project for which no map has been made
    When the session runs `tools untested src/cart.py`
    Then the command is refused because no map has been made
    And it says to make one with `tools map`

  @r17
  Scenario Outline: without coverage tests-of and untested say to install it
    Pins that the map readers stop and point to install when coverage is missing.
    Given a Python project whose interpreter is missing coverage
    When the session runs `tools <command>`
    Then the command is refused because coverage is missing from the interpreter
    And it says to run `tools install`

    Examples:
      | command                |
      | tests-of src/cart.py   |
      | untested src/cart.py   |

  @r17
  Scenario: without jedi refs says to install it
    Pins that refs stops and points to install when jedi is missing.
    Given a Python project whose interpreter is missing jedi
    When the session runs `tools refs total`
    Then the command is refused because jedi is missing from the interpreter
    And it says to run `tools install`

  @r1 @r17
  Scenario: a .venv whose python links to the running interpreter is still the one used
    Pins that tools runs under the project's virtualenv, and so reads its packages, even when its python is a link to the interpreter running the script.
    Given a Python project whose .venv is a virtualenv made from the interpreter running the script, without jedi
    When the session runs `tools refs total`
    Then the command is refused because jedi is missing from the interpreter
    And it says to run `tools install`

  @r49
  Scenario: tests-of on a file that does not exist is refused
    Pins that an absent file is named, not treated as untested.
    Given a map has been made
    And the project has no file src/gone.py
    When the session runs `tools tests-of src/gone.py`
    Then the command is refused
    And it names src/gone.py

  @r49
  Scenario: untested on a file that does not exist is refused
    Pins that an absent file is named, not read as a file with no functions.
    Given a map has been made
    And the project has no file src/gone.py
    When the session runs `tools untested src/gone.py`
    Then the command is refused
    And it names src/gone.py

  @r14
  Scenario Outline: refs on a defined name gives its definition apart from its references
    Pins that the definition is named but not counted, and that any number of references is success.
    Given a Python project that defines the function total in src/cart.py and refers to it <count> times
    When the session runs `tools refs total`
    Then tools names src/cart.py as where total is defined
    And the definition is not counted as a reference
    And <count> references are printed
    And it exits 0

    Examples:
      | count |
      | 0     |
      | 3     |

  @r16
  Scenario: `tools check` with --base examines the changed Python files that remain, in place of the paths given
    Pins which files --base selects: Python, changed since the base, not deleted.
    Given a Python project in git with base commit abc1234
    And since abc1234 src/cart.py and README.md have changed and src/old.py has been deleted
    When the session runs `tools check --base abc1234 src/report.py`
    Then tools examines src/cart.py
    And it does not examine README.md, src/old.py or src/report.py

  @r49
  Scenario: `tools check` with a base git cannot compare is refused with git's error
    Pins that a bad base stops `tools check` and passes git's own reason on.
    Given a Python project in git with no ref named nosuchref
    When the session runs `tools check --base nosuchref`
    Then the command is refused because git cannot compare the working tree with nosuchref
    And it prints git's error

  @r16
  Scenario: `tools check` with no file to examine says so under ruff and vulture and does not fail for them
    Pins that an empty selection is not a finding.
    Given a Python project in git whose Python files are unchanged since base commit abc1234
    When the session runs `tools check --base abc1234`
    Then under the ruff heading and under the vulture heading tools says `nothing to check`
    And neither ruff nor vulture makes it exit 1

  @r16
  Scenario: `tools check` without import contracts does not run import-linter
    Pins that import-linter is skipped, visibly, when the project declares no contracts.
    Given a Python project that declares no import contracts
    When the session runs `tools check src/cart.py`
    Then under the import-linter heading tools says `the project states no import contracts`
    And import-linter is not run

  @r16
  Scenario: a tool that prints nothing is shown clean
    Pins that silence from a tool is shown as clean rather than as an empty heading.
    Given a Python project in which ruff prints nothing for src/cart.py
    When the session runs `tools check src/cart.py`
    Then under the ruff heading tools says it is clean

  @r50
  Scenario: size prints each tracked Python file over the limit in the working tree, with its line count
    Pins which files count as Python, that tests are included, that the working tree is counted, and that no other file is printed.
    Given a Python project in git
    And it tracks src/cart.py of 301 lines, tests/test_cart.py of 320 lines, src/total.py of 300 lines and README.md of 900 lines
    And it tracks bin/reprice, with no extension, a python shebang and 400 lines
    And it tracks src/report.py, committed at 200 lines and edited in the working tree to 350 lines
    And it has an untracked src/draft.py of 500 lines
    When the session runs `tools size`
    Then tools prints src/cart.py with 301 lines, tests/test_cart.py with 320 lines, bin/reprice with 400 lines and src/report.py with 350 lines
    And it prints no other file

  # [r51] **If** any tracked Python file is over the size limit, then `tools size` shall exit 1.
  @r51
  Scenario: size fails when one tracked Python file is over the limit
    Pins that a single file over the limit fails the command.
    Given a Python project in git
    And it tracks src/cart.py of 301 lines and src/total.py of 120 lines
    When the session runs `tools size`
    Then it exits 1

  # [r52] **Where** `tools size --limit <n>` is given, `tools size` shall use `<n>` lines as the size limit, and 300 lines otherwise.
  @r52
  Scenario Outline: size uses the limit --limit gives, and 300 lines without it
    Pins the limit at its edge: a file of exactly the limit is within it, one line more is over.
    Given a Python project in git
    And it tracks src/total.py of <within> lines and src/cart.py of <over> lines
    When the session runs `tools size <option>`
    Then tools prints src/cart.py with <over> lines
    And it does not print src/total.py

    Examples:
      | option      | within | over |
      | --limit 250 | 250    | 251  |
      |             | 300    | 301  |
