---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-script-capabilities-drafts-round-1
kind: initiative-archive
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools, capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement, capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check, capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools, bounded-context/missingmass.io/shopsystem/shopsystem-bdd]
date: 2026-10-16
---

# Script capabilities formulation, round 1: feature drafts (superseded)

The feature-formulator's round-1 feature drafts of 2026-10-16 for analysis-tools, batch-measurement, design-model-check (new scenarios r19-r45 only), feature-file-tools and slice-plan-tool (since removed from the spec). Superseded: the committed feature files were applied from these and round 2's drafts. The replies are in review-findings/2026-10-16-script-capabilities-formulation-round-1.

Archived from git-ignored scratch; each file's text as it was.

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/analysis-tools.feature`

~~~~~~
# formulated from spec/capabilities/analysis-tools.md
Feature: Analysis tools
  Narrator: an agent researching or reviewing a project's code

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
    Then tools prints one line for each tool with what it is for
    And each installed tool's line gives its version
    And vulture's line says it is missing
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
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/batch-measurement.feature`

~~~~~~
# formulated from spec/capabilities/batch-measurement.md
Feature: Batch measurement
  Narrator: a session measuring a closed batch

  @r1
  Scenario: an archive file's batch runs from the archive commit before it to its own
    A named archive file's batch starts where the previous archive file was added and ends where its own was.
    Given archive file 2026-09-01-slices.md was added by commit A
    And archive file 2026-09-15-slices.md was added by a later commit B
    When the session runs measure batch for 2026-09-15-slices.md
    Then one facts file is written for the batch
    And the batch's window runs from commit A to commit B

  @r2
  Scenario: without an archive file the open batch is measured from the last archive commit to now
    With no archive file, the batch is the work since the last archive, read against the living plan.
    Given the last archive file was added by commit B
    And the repository holds one living plan
    When the session runs measure batch with no archive file
    Then the batch's window runs from commit B to now
    And the slices are read from the living plan

  @r3
  Scenario Outline: a given --<option> replaces that end of the batch
    Either end of the batch can be set by hand, as a commit or as an ISO time.
    Given archive file 2026-09-15-slices.md whose batch runs from commit A to commit B
    When the session runs measure batch for 2026-09-15-slices.md with --<option> <value>
    Then the batch's <end> is <value>

    Examples:
      | option | value                | end   |
      | from   | commit C             | start |
      | from   | 2026-09-05T09:00:00Z | start |
      | to     | commit D             | end   |
      | to     | 2026-09-14T18:00:00Z | end   |

  @r4
  Scenario: without --out the facts go under measurements in the archive file's name
    The default place for an archive batch's facts follows the archive file's name.
    Given archive file 2026-09-15-slices.md with dispatches inside its batch
    When the session runs measure batch for 2026-09-15-slices.md with no --out
    Then the facts are written to docs/superpowers/measurements/2026-09-15-slices.md.json

  @r5
  Scenario: an archive file no commit added is refused
    A batch cannot be bounded by an archive file git has no record of adding.
    Given a file 2026-10-01-slices.md that no commit added
    When the session runs measure batch for 2026-10-01-slices.md
    Then measure batch refuses because the archive file was not added by any commit
    And the refusal names 2026-10-01-slices.md

  @r6
  Scenario: a transcript of an unknown shape is refused and no facts are written
    Measure does not guess at transcripts it does not recognise.
    Given a batch with a transcript that lacks a field measure knows transcripts to have
    When the session runs measure batch for the batch
    Then measure batch refuses because the transcript's shape is not known
    And the refusal names the transcript and what was missing
    And no facts file is written

  @r7
  Scenario: an existing facts file is not written over without --replace
    A facts file already written survives a second run unless replacing is asked for.
    Given the batch's facts file already exists
    When the session runs measure batch for the batch with no --replace
    Then measure batch refuses because the facts file exists
    And the facts file is as it was

  @r8
  Scenario: a batch with no dispatch inside it is refused
    A batch in which nothing was dispatched has nothing to measure.
    Given a batch inside whose window no dispatch started
    When the session runs measure batch for the batch
    Then measure batch refuses because no dispatch was found inside the batch
    And the refusal names the window it searched
    And nothing is written

  @r9
  Scenario Outline: a subagent transcript is a dispatch only when it starts inside the batch
    Whether a subagent belongs to the batch is decided by when it started.
    Given a batch running from commit A to commit B
    And a subagent transcript that starts <when> the batch
    When the session runs measure batch for the batch
    Then the transcript <counted> as a dispatch

    Examples:
      | when   | counted       |
      | inside | is counted    |
      | before | is not counted |
      | after  | is not counted |

  @r11
  Scenario: a dispatching session's own requests are the controller's
    The session that dispatched inside the batch has its own requests there counted to the controller.
    Given a session that dispatched a subagent inside the batch
    And made requests of its own inside the batch
    When the session runs measure batch for the batch
    Then the facts count that session's requests inside the batch as the controller's

  @r12
  Scenario Outline: a dispatch is attributed by its description, then its prompt, else unattributed
    Attribution tries the description first and the prompt second, and admits when neither tells.
    Given a dispatch whose description <description> and whose prompt <prompt>
    When the session runs measure batch for the batch
    Then the facts attribute the dispatch to <attributed>

    Examples:
      | description         | prompt                  | attributed  |
      | names slice 2       | names slice 3           | slice 2     |
      | names batch work    | names slice 3           | batch work  |
      | names no slice      | names slice 3           | slice 3     |
      | names no slice      | names no task or slice  | unattributed |

  @r13
  Scenario: a reviewer's findings are counted as it wrote them
    Critical and Important findings are its lines so marked, and Minor is the count it states.
    Given a reviewer's reply with 2 lines beginning Critical and 1 line beginning Important
    And the reply states a count of 4 Minor
    When the session runs measure batch for the batch
    Then the facts count the reviewer's findings as 2 Critical, 1 Important and 4 Minor

  @r14
  Scenario: a commit goes to the implementer running when it was made
    Each commit is credited to the implementer at work at the time and its files are sorted into kinds.
    Given an implementer dispatch running from 10:00 to 10:30
    And a commit made at 10:15 that touched three files
    When the session runs measure batch for the batch
    Then the facts give the commit to that implementer
    And each of its three files is counted as production, test or other

  @r15
  Scenario Outline: each slice's Lands line sits beside the files its dispatches touched
    What a slice said it would land is set against what its dispatches actually touched.
    Given a <batch> whose <source> gives slice 1 the Lands line "src/cart.py"
    And slice 1's dispatches touched src/cart.py and tests/test_cart.py
    When the session runs measure batch for the <batch>
    Then the facts give slice 1 the Lands line "src/cart.py" beside src/cart.py and tests/test_cart.py

    Examples:
      | batch         | source       |
      | archive batch | archive file |
      | open batch    | living plan  |

  @r16
  Scenario: the facts give the plan's tasks at both ends, its hand-backs and suite record
    The batch plan's task list is taken when the plan was added and again at the batch's end.
    Given a batch plan that held 5 tasks when it was added and 7 tasks at the batch's end
    And the plan has two hand-back entries and a suite record
    When the session runs measure batch for the batch
    Then the facts give the 5 tasks held when it was added and the 7 held at the end
    And the facts give both hand-back entries and the suite record

  @r17
  Scenario: the facts hold no prompt, reply or tool content
    What the agents said and did is measured, never copied into the facts.
    Given a batch whose dispatches have prompts, replies and tool calls
    When the session runs measure batch for the batch
    Then the facts hold none of the prompts', replies' or tools' content

  @r18
  Scenario: show prints a facts file as tables
    A facts file can be read without opening the JSON.
    Given a facts file measure wrote
    When the session runs measure show for the file
    Then the facts are printed as tables

  @r19
  Scenario: compare prints two facts files side by side
    Two batches can be read against each other.
    Given two facts files measure wrote
    When the session runs measure compare for the two files
    Then the two files' facts are printed side by side

  @r20
  Scenario: show refuses a file measure did not write as facts
    Show reads only facts files of measure's own making.
    Given a JSON file that is not a facts file measure wrote
    When the session runs measure show for the file
    Then measure refuses because the file is not a facts file measure wrote
    And the refusal names the file

  @r21
  Scenario Outline: the open batch needs --plan when the living plan cannot be found
    Without one slices plan in the repository, measure asks for the living plan to be named.
    Given a repository holding <plans> docs/superpowers/plans/*-slices.md files
    When the session runs measure batch with no archive file and no --plan
    Then measure batch refuses because the living plan cannot be found
    And the refusal says to name the living plan with --plan

    Examples:
      | plans |
      | no    |
      | two   |

  @r22
  Scenario Outline: a batch with no archive before it needs --from
    When nothing marks where the batch began, measure asks for the start.
    Given <batch> with no archive file added before the batch's end
    When the session runs measure batch for it with no --from
    Then measure batch refuses because the batch has no start
    And the refusal says to give the batch's start with --from

    Examples:
      | batch                                           |
      | the open batch of a repository                  |
      | the batch of the first archive file a commit added |

  @r23
  Scenario Outline: a --<option> that is neither a commit nor an ISO time is refused
    An end of the batch must be something measure can place in time.
    Given a repository with no commit named "last-tuesday"
    When the session runs measure batch with --<option> last-tuesday
    Then measure batch refuses because the value is neither a commit nor an ISO time
    And the refusal names last-tuesday

    Examples:
      | option |
      | from   |
      | to     |

  @r24
  Scenario Outline: git's failures are refused with git's error
    When git cannot answer, measure passes on what git said.
    Given <situation>
    When the session runs measure batch
    Then measure refuses with git's error

    Examples:
      | situation                                                   |
      | --repo names a directory that is not inside a git repository |
      | the current directory is not inside a git repository and no --repo is given |
      | a git command measure batch runs fails                      |

  @r25
  Scenario Outline: the open batch is named by --name, default open
    The open batch's name, and so its default facts file, can be chosen.
    Given an open batch with dispatches inside it
    When the session runs measure batch with no archive file, <name option> and no --out
    Then the batch is named <name>
    And the facts are written to docs/superpowers/measurements/<name>.json

    Examples:
      | name option     | name       |
      | no --name       | open       |
      | --name trial-3  | trial-3    |

  @r26
  Scenario Outline: the open batch starts at the last commit that added a file under the archive directory
    The archive directory that marks batch boundaries defaults to the plans archive and can be changed.
    Given the last commit adding a file under <directory> is commit <commit>
    When the session runs measure batch with no archive file and <archive option>
    Then the batch starts at commit <commit>

    Examples:
      | archive option            | directory                     | commit |
      | no --archive-dir          | docs/superpowers/plans/archive | A      |
      | --archive-dir old/plans   | old/plans                     | B      |

  @r27
  Scenario Outline: the facts hold the slices the batch planned and the slices dispatches were attributed to
    An archive batch keeps all its planned slices; the open batch only those that saw work.
    Given a <batch> whose <source> holds slices 1 and 2
    And the only dispatches are attributed to slice 2 and slice 3
    When the session runs measure batch for the <batch>
    Then the facts hold slices <slices>

    Examples:
      | batch         | source       | slices     |
      | archive batch | archive file | 1, 2 and 3 |
      | open batch    | living plan  | 2 and 3    |

  @r28
  Scenario: a commit made while two implementers ran is counted as ambiguous
    Credit for a commit is flagged as uncertain when more than one implementer could have made it.
    Given two implementer dispatches both running at 10:15
    And a commit made at 10:15
    When the session runs measure batch for the batch
    Then the facts count the commit as ambiguous

  @r29
  Scenario Outline: tasks are left uncounted with a note when the batch plan cannot be had
    Without a batch plan to read, the facts say why tasks are missing instead of counting none.
    Given <situation>
    When the session runs measure batch for the batch
    Then the facts leave tasks uncounted
    And the facts hold a note saying why
    And measure batch writes the note on stderr

    Examples:
      | situation                                                   |
      | no dispatch names a ledger and no --tasks is given          |
      | the batch plan is in no commit                              |

  @r30
  Scenario: a written batch is reported in one line
    After writing, the session learns where the facts went and what they cover.
    Given a batch with 6 dispatches across 2 slices
    When the session runs measure batch for the batch
    Then measure batch prints one line naming the facts file, 6 dispatches, 2 slices and the window

  @r31
  Scenario Outline: a reply closing <status> is counted as not done
    The closing status a reply states is kept, and the stuck ones are counted as not done.
    Given a dispatch whose reply closes with status <status>
    When the session runs measure batch for the batch
    Then the facts give the dispatch the closing status <status>
    And the facts count the dispatch as not done

    Examples:
      | status        |
      | BLOCKED       |
      | PARTIAL       |
      | NEEDS_CONTEXT |

  @r32
  Scenario: the facts record the versions the transcripts name and the window
    The facts say what plugin and harness ran, and when the batch was.
    Given archive file 2026-09-15-slices.md whose batch runs from commit A to commit B
    And its transcripts name plugin version 0.18.0 and harness version 2.1.4
    When the session runs measure batch for 2026-09-15-slices.md
    Then the facts record plugin version 0.18.0 and harness version 2.1.4
    And the facts record the window as the times of commits A and B and as commits A and B

  @r33
  Scenario Outline: a batch starting at a commit gives the files and lines changed to its end
    The size of the change is taken from the batch's start commit to its end commit, or HEAD.
    Given a batch starting at commit A and ending <end>
    When the session runs measure batch for the batch
    Then the facts give the files and lines changed from commit A to <to>

    Examples:
      | end                       | to       |
      | at commit B               | commit B |
      | at 2026-09-14T18:00:00Z   | HEAD     |
      | now                       | HEAD     |

  @r35
  Scenario: show prints the header, the tables, the exceptions, the hand-backs and the notes
    Show lays a facts file out in a fixed order.
    Given a facts file measure wrote, with a dispatch not done, a dispatch not attributed, a hand-back and a note
    When the session runs measure show for the file
    Then it prints the repository, batch, window, plugin and harness versions and suite record
    And then the summary, roles and slices tables
    And then the dispatch not done and the dispatch not attributed
    And then the hand-back and the note

  @r36
  Scenario: compare prints both files' figures with the ratio of the second to the first
    Compare sets each summary figure and each slice's costs side by side, with how the second batch differs.
    Given facts file a for batch 2026-09-01 on plugin version 0.17.0 with slice 1
    And facts file b for batch 2026-09-15 on plugin version 0.18.0 with slice 1
    When the session runs measure compare for a and b
    Then each file is headed by its batch and plugin versions
    And each summary figure of both files is printed with the ratio of b's to a's
    And slice 1's output, new input, cache read and agent minutes of both files are printed with the ratio of b's to a's

  @r37
  Scenario Outline: a file measure cannot read as its facts is refused
    Compare reads only measure's own facts files, and neither command reads a file that is not JSON.
    Given a file that <file>
    When the session runs measure <command> with the file
    Then measure refuses because the file <reason>
    And the refusal names the file

    Examples:
      | command | file                                              | reason                                |
      | compare | is JSON but not a facts file measure wrote        | is not a facts file measure wrote     |
      | show    | cannot be read as JSON                            | cannot be read as JSON                |
      | compare | cannot be read as JSON                            | cannot be read as JSON                |

  @r38
  Scenario: a refusal says why on stderr and exits 1
    Every refusal is explained on stderr and ends with exit status 1.
    Given the batch's facts file already exists
    When the session runs measure batch for the batch with no --replace
    Then measure refuses and says why on stderr
    And it exits 1
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/design-model-check.feature`

~~~~~~
  # [r19] `model` reads, under `--root` (default the current directory), `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, `decisions/*.md`, `work/<initiative>/*.md`, `records/observations.md` and any other Markdown under `records/` whose frontmatter has an `id`.
  @r19
  Scenario Outline: model reads the repository's files under its root
    Pins which files of a repository model reads, and that the root is the current directory unless --root names one.
    Given a repository in a directory holding <file>
    When model facts is run <how>
    Then the facts printed <outcome> what <file> holds

    Examples:
      | file                               | how                                   | outcome         |
      | spec/index.md                      | with --root naming that directory     | include         |
      | spec/capabilities/thing.md         | with --root naming that directory     | include         |
      | features/sub/thing.feature         | with --root naming that directory     | include         |
      | decisions/0001-one.md              | with --root naming that directory     | include         |
      | work/i1/p1.md                      | with --root naming that directory     | include         |
      | records/observations.md            | with --root naming that directory     | include         |
      | records/review/f1.md with an id    | with --root naming that directory     | include         |
      | records/review/f2.md with no id    | with --root naming that directory     | do not include  |
      | spec/capabilities/thing.md         | from that directory with no --root    | include         |

  # [r20] A scenario names a requirement by a tag `@r<n>`, its own or its feature's, in the feature file its capability is `formulated_as`, or `features/<capability name>.feature` when it gives none.
  @r20
  Scenario Outline: a scenario names a requirement by its tag in its capability's feature file
    Pins where an @r<n> tag may sit, and which feature file a capability's scenarios are read from.
    Given a capability thing with requirement r2, <formulated as>
    And a scenario in <feature file> with the tag @r2 <placed>
    When model check is run
    Then the requirement thing#r2 is <reported> under v_s3

    Examples:
      | formulated as                                  | feature file              | placed                  | reported |
      | formulated_as features/thing.feature           | features/thing.feature    | on the scenario         | not      |
      | formulated_as features/thing.feature           | features/thing.feature    | on its feature          | not      |
      | giving no formulated_as                        | features/thing.feature    | on the scenario         | not      |
      | formulated_as features/sub/thing-flow.feature  | features/sub/thing-flow.feature | on the scenario   | not      |
      | formulated_as features/sub/thing-flow.feature  | features/other.feature    | on the scenario         | still    |

  # [r21] A reference written `<name>#r<n>` is read as a requirement of the capability `<name>` in the bounded context.
  @r21
  Scenario: a reference written name#r<n> is that capability's requirement
    Pins that the part before # is the capability's name in this bounded context and the part after it the requirement's id.
    Given a capability thing with requirement r2
    And a capability-proposal that adds thing#r2
    When model why is run for thing#r2
    Then it prints thing's requirement r2 and the proposal as adding it

  # [r22] **If** a list names a reference that is not `<capability>#r<n>` or `<capability>#behaviour/r<n>`, or a range `#r<a>-r<b>` with a greater than b, `model check` reports it as unresolved.
  @r22
  Scenario Outline: a reference in neither requirement form, or a reversed range, is unresolved
    Pins the forms a requirement reference in a list may take.
    Given a capability thing with requirements r1 to r3
    And a capability-proposal whose list names <reference>
    When model check is run
    Then <reference> is reported as unresolved

    Examples:
      | reference      |
      | thing          |
      | thing#2        |
      | thing#line2    |
      | thing#r3-r1    |

  # [r24] **If** a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by` or `depends_on` names nothing, or nothing of the kind it needs, in the repository, `model check` reports it as unresolved.
  @r24
  Scenario Outline: a frontmatter reference to nothing, or to the wrong kind, is unresolved
    Pins that each named frontmatter reference must reach a node of the kind it needs.
    Given a file whose <field> names <target>
    When model check is run
    Then that <field> is reported as unresolved

    Examples:
      | field      | target                                   |
      | supersedes | an id nothing in the repository has      |
      | source     | an id nothing in the repository has      |
      | part_of    | an id nothing in the repository has      |
      | argues     | an id nothing in the repository has      |
      | under      | an id nothing in the repository has      |
      | for        | an id nothing in the repository has      |
      | blocked_by | an id nothing in the repository has      |
      | depends_on | an id nothing in the repository has      |
      | argues     | a decision, where a capability is needed |

  # [r25] **If** `spec/index.md` is missing or has no `id`, a capability's `id` is not `<context>/<file name>`, a capability has no `## Behaviour` section, or its `retired` lists an entry not written `r<n>`, `model check` reports a file problem naming the file.
  @r25
  Scenario Outline: a malformed index or capability file is a file problem
    Pins the shape spec/index.md and each capability file must have to be read.
    Given a bounded context with id acme/shop/cart in which <case>
    When model check is run
    Then it reports a file problem naming <file>

    Examples:
      | case                                                       | file                       |
      | spec/index.md is missing                                   | spec/index.md              |
      | spec/index.md has no id                                    | spec/index.md              |
      | spec/capabilities/thing.md has the id acme/shop/cart/other | spec/capabilities/thing.md |
      | spec/capabilities/thing.md has no ## Behaviour section     | spec/capabilities/thing.md |
      | spec/capabilities/thing.md lists retired: [3]              | spec/capabilities/thing.md |

  # [r28] **If** a work-item accepts a requirement no scenario names yet, `model check` reports a file problem naming the work-item's file.
  @r28
  Scenario: a work-item accepting a requirement no scenario names is a file problem
    Pins that a work-item may accept only requirements a scenario already names.
    Given a capability thing with requirement r2 that no scenario names
    And a work-item in work/i1/w1.md that accepts thing#r2
    When model check is run
    Then it reports a file problem naming work/i1/w1.md

  # [r29] **If** a decision has no `id`, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds, `model check` reports a file problem.
  @r29
  Scenario Outline: a malformed decision, record or frontmatter is a file problem
    Pins the frontmatter faults in decisions, records and shared ids that model check refuses.
    Given a repository in which <case>
    When model check is run
    Then it reports a file problem

    Examples:
      | case                                                         |
      | a decision under decisions/ has no id                        |
      | a record under records/ with an id has the kind banana       |
      | a frontmatter value is written as a folded block, with >     |
      | a frontmatter value is written as a literal block, with \|   |
      | a decision and an observation have the same id               |

  # [r30] **If** `model check` finds a file problem, it prints each and exits 1.
  @r30
  Scenario: file problems are each printed and fail the check
    Pins that every file problem is shown and that any one of them fails the check.
    Given a repository with two capabilities that each have no ## Behaviour section
    When model check is run
    Then it prints a file problem for each of the two capabilities
    And it exits 1

  # [r31] **When** `model check` ends without `--json`, it prints the counts of violations, warnings, unresolved references and file problems.
  @r31
  Scenario: the check ends with the four counts
    Pins the summary every plain-text check ends with.
    Given a repository with one violation, one warning, one unresolved reference and one file problem
    When model check is run without --json
    Then it prints 1 violation, 1 warning, 1 unresolved reference and 1 file problem

  # [r32] **Where** `--limit <n>` is given, default 10, `model check` prints at most n rows of each violated relation and how many more there are.
  @r32
  Scenario Outline: rows of a violated relation are limited, saying how many more there are
    Pins the row limit per violated relation, given or by default.
    Given a repository with <rows> requirements no scenario names
    When model check is run <limit>
    Then it prints <shown> rows under v_s3
    And it says there are <more> more

    Examples:
      | rows | limit           | shown | more |
      | 5    | with --limit 2  | 2     | 3    |
      | 12   | with no --limit | 10    | 2    |

  # [r33] **Where** `--json` is given, `model check` prints the violations, warnings, unresolved references and file problems as one JSON object, with the same exit status.
  @r33
  Scenario Outline: with --json the check's findings are one JSON object
    Pins the machine-readable output and that it does not change the exit status.
    Given a repository <state>
    When model check is run with --json
    Then it prints one JSON object holding the violations, warnings, unresolved references and file problems
    And it exits <status>

    Examples:
      | state                                  | status |
      | the grammar accepts                    | 0      |
      | with a requirement no scenario names   | 1      |

  # [r34] **If** an initiative that is not a capability-change has more than one part directly under it, `model check` reports it under v_k5, while a capability-change initiative may hold several capability-proposals.
  @r34
  Scenario Outline: only a capability-change initiative may hold several parts directly
    Pins that an initiative holds one part directly, except a capability-change holding capability-proposals.
    Given <initiative> with <parts> directly under it
    When model check is run
    Then the initiative is <reported> under v_k5

    Examples:
      | initiative                                   | parts                    | reported |
      | an initiative that is not a capability-change | two parts                | reported |
      | a capability-change initiative               | two capability-proposals | not reported |

  # [r35] **If** a capability-proposal argues more than one capability, `model check` reports it under v_k6.
  @r35
  Scenario: a proposal arguing two capabilities is refused
    Pins that a capability-proposal argues one capability.
    Given capabilities thing and other
    And a capability-proposal that argues both thing and other
    When model check is run
    Then the output names v_k6 with the proposal

  # [r36] A capability-proposal at `formulated` counts as closed when `model check` decides whether an initiative may be done.
  @r36
  Scenario: an initiative may be done when its proposal is formulated
    Pins that formulated is a closed status for a capability-proposal under a done initiative.
    Given a capability-change initiative with status done
    And under it a capability-proposal with status formulated, whose requirements scenarios name
    When model check is run
    Then no violation names the initiative

  # [r37] **When** `model decisions --check` finds `spec/decisions.md` is what `model decisions` would write, it says the file is current and exits 0.
  @r37
  Scenario: a current decisions index passes the check
    Pins the passing outcome of the decisions index check.
    Given a spec/decisions.md that is what model decisions writes
    When model decisions --check is run
    Then it says the file is current
    And it exits 0

  # [r38] **When** `model decisions` is run, it prints the file it wrote, and a decision file with no `id` is left out of the index.
  @r38
  Scenario: writing the decisions index names the file and leaves out decisions with no id
    Pins what writing the index reports and that only decisions with an id are indexed.
    Given two decisions under decisions/, one of them with no id
    When model decisions is run
    Then it prints spec/decisions.md as the file it wrote
    And spec/decisions.md lists the decision with an id and not the one without

  # [r39] **If** `model why` is given an argument that is not a requirement reference, it says why and exits 2.
  @r39
  Scenario: why refuses an argument that is not a requirement reference
    Pins that model why takes only a requirement reference.
    Given a capability thing
    When model why is run for thing
    Then it is refused because thing is not a requirement reference
    And it exits 2

  # [r40] **If** no capability has the requirement `model why` names, it says so in place of the requirement's text and still lists the proposals that name it.
  @r40
  Scenario: why on a requirement no capability has still lists its proposals
    Pins that a missing requirement does not hide the proposals that name it.
    Given a capability thing with no requirement r9
    And a capability-proposal that changes thing#r9
    When model why is run for thing#r9
    Then it says no capability has thing#r9 where the requirement's text would be
    And it lists the proposal

  # [r42] A reference written `<capability>#behaviour/r<n>`, the requirement as a part in shopsystem-knowledge's IRI form, names the same requirement as `<capability>#r<n>`.
  @r42
  Scenario: the behaviour/ form of a reference names the same requirement
    Pins that #behaviour/r<n> and #r<n> are one requirement.
    Given a capability thing with requirement r2
    And a capability-proposal that adds thing#behaviour/r2
    When model why is run for thing#r2
    Then it prints the proposal as adding it

  # [r43] **Where** the bounded context's id is a path such as `<owner>/<product>/<context name>`, a capability written `<context name>/<name>` is read as `<context id>/<name>`, and the context name alone as the bounded context.
  @r43
  Scenario Outline: a path-shaped context id may be written by its context name
    Pins the short forms of a capability and of the bounded context when the context's id is a path.
    Given a bounded context with id acme/shop/cart and a capability thing
    And <reference>
    When model check is run
    Then <written> is read as <read> and is not reported as unresolved

    Examples:
      | reference                                                  | written    | read                  |
      | a capability-proposal that argues cart/thing               | cart/thing | acme/shop/cart/thing  |
      | a reference to the bounded context written cart            | cart       | the bounded context   |

  # [r44] A scenario tagged `@holding` is not read as an acceptance-scenario, whatever `@r<n>` tag it carries.
  @r44
  Scenario: a held scenario names no requirement
    Pins that a scenario tagged @holding does not count as a requirement's acceptance-scenario.
    Given a capability thing with requirement r2
    And its only scenario tagged @r2 is also tagged @holding
    When model check is run
    Then the requirement thing#r2 is reported under v_s3

  # [r45] **Where** a repository has no `decisions/` directory, `model` reads each `## decision/<slug>` heading of `spec/decisions.md` as a design-decision.
  @r45
  Scenario: without a decisions directory the index's headings are the decisions
    Pins where decisions come from in a repository that keeps them only in spec/decisions.md.
    Given a repository with no decisions/ directory
    And a spec/decisions.md with the heading ## decision/one
    And a capability that rests on decision/one
    When model check is run
    Then decision/one is not reported as unresolved
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/feature-file-tools.feature`

~~~~~~
# formulated from spec/capabilities/feature-file-tools.md
Feature: Feature file tools
  Narrator: an agent or session editing feature files

  @r1
  Scenario: every feature file under the directory is read, and docstring text is not
    A feature file in a nested directory under the default features directory is read, and a tag or scenario written inside a docstring is not.
    Given a feature file features/cart/nested.feature with a scenario "Nested" tagged @slice-1
    And the scenario "Nested" has a docstring holding the lines "@slice-1" and "Scenario: Phantom"
    When the agent runs features list --tag slice-1 without --dir
    Then the output lists features/cart/nested.feature with "Nested"
    And the output does not list "Phantom"

  @r2
  Scenario: a feature file with a Rule block is refused
    A Rule block is not read as part of the feature; the command refuses and says which file holds it.
    Given a feature file features/rules.feature that holds a Rule: block
    When the agent runs features list --title Cart
    Then the command is rejected because the feature file holds a Rule: block
    And the refusal names features/rules.feature

  @r5
  Scenario: listing by tag includes the feature's and the Examples' tags
    A scenario holds a tag when it carries it itself, when its feature carries it, or when its Examples table carries it.
    Given a feature file features/cart.feature tagged @cart
    And it has a scenario "Plain" with no tags of its own
    And it has a scenario "Own tag" tagged @checkout
    And it has a Scenario Outline "Outlined" whose one Examples table is tagged @checkout and has one row
    And another feature file features/stock.feature tagged @checkout has a scenario "Elsewhere"
    And a feature file features/misc.feature has a scenario "Untagged" with no tags
    When the agent runs features list --tag checkout
    Then the output lists features/cart.feature with "Own tag"
    And the output lists features/cart.feature with "Outlined"
    And the output lists features/stock.feature with "Elsewhere"
    And the output does not list "Plain" or "Untagged"

  @r6
  Scenario: listing by title finds every scenario whose title contains the text
    A title matches when the text appears anywhere in it, not only when it equals it.
    Given a feature file features/cart.feature with scenarios "Apply a code", "Code expired" and "Empty cart"
    When the agent runs features list --title "ode"
    Then the output lists features/cart.feature with "Apply a code"
    And the output lists features/cart.feature with "Code expired"
    And the output does not list "Empty cart"

  @r7
  Scenario: listing that matches nothing prints nothing and fails
    An empty result is not a success.
    Given a feature file features/cart.feature with no scenario tagged @slice-9
    When the agent runs features list --tag slice-9
    Then nothing is printed
    And it exits 1

  @r8
  Scenario: retagging replaces the first slice tag and drops the others
    A scenario ends with exactly one slice tag, in the place of its first, and keeps every other tag and line.
    Given a feature file features/cart.feature whose only scenario "Apply a code" has the tag line "@wip @slice-1 @slice-2 @r3"
    When the agent runs features tag "Apply a code" slice-4
    Then the scenario's tag line is "@wip @slice-4 @r3"
    And every other line of features/cart.feature is unchanged

  @r9
  Scenario Outline: a scenario without a slice tag gets one
    The new slice tag joins the scenario's last tag line, or stands on a tag line of its own when the scenario has none.
    Given a feature file features/cart.feature whose only scenario "Apply a code" has the tag lines <tag lines before>
    When the agent runs features tag "Apply a code" slice-2
    Then the scenario's tag lines are <tag lines after>

    Examples:
      | tag lines before  | tag lines after               |
      | "@wip"            | "@wip @slice-2"               |
      | "@wip" then "@r1" | "@wip" then "@r1 @slice-2"    |
      | none              | "@slice-2" above the scenario |

  @r10
  Scenario Outline: retagging a title that is not in exactly one file is refused
    The title must pick out one file; otherwise nothing is changed and every file holding it is named.
    Given the title "Apply a code" is held by <files holding it>
    When the agent runs features tag "Apply a code" slice-2
    Then the command is rejected because the title is not held by exactly one file
    And the refusal names <files named>
    And no file is changed

    Examples:
      | files holding it                               | files named                                    |
      | no feature file                                | no file                                        |
      | features/cart.feature and features/old.feature | features/cart.feature and features/old.feature |

  @r11
  Scenario: retagging with a tag that is neither a slice nor a requirement tag is bad usage
    Only slice-<n>, slice-<n>.<m> and r<n> are tags features tag accepts.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the agent runs features tag "Apply a code" wip
    Then the command is rejected as bad usage because the tag is not written slice-<n>, slice-<n>.<m> or r<n>
    And no file is changed

  @r12
  Scenario: moving a scenario takes its block to the end of the destination
    The block leaves its source file and arrives unchanged after everything already in the destination.
    Given a feature file features/old.feature with scenarios "Apply a code" and "Empty cart"
    And a feature file features/cart.feature whose last scenario is "Checkout"
    When the agent runs features move "Apply a code" --to features/cart.feature
    Then features/old.feature holds "Empty cart" and not "Apply a code"
    And the block of "Apply a code" follows "Checkout" at the end of features/cart.feature, unchanged

  @r13
  Scenario: moving with the Background inlined puts its steps first
    A moved scenario keeps the steps its source Background gave it.
    Given a feature file features/old.feature whose Background has the step "Given the date is 2026-10-16"
    And its scenario "Apply a code" has first step "Given a cart holding product Mug at price 8.00"
    And a feature file features/cart.feature
    When the agent runs features move "Apply a code" --to features/cart.feature --inline-background
    Then the moved "Apply a code" has the steps "Given the date is 2026-10-16" then "Given a cart holding product Mug at price 8.00"

  @r15
  Scenario: moving to a destination that does not exist is refused
    A move never creates a file.
    Given a feature file features/old.feature with a scenario "Apply a code"
    And no file features/missing.feature
    When the agent runs features move "Apply a code" --to features/missing.feature
    Then the command is rejected because the destination does not exist
    And no file is changed

  @r16
  Scenario: two trees alike scenario by scenario pass the move check
    Scenarios may sit in other files, but alike by title in tags, description and steps they all match.
    Given a tree old/ with "Apply a code" and "Empty cart" in old/cart.feature
    And a tree features/ with "Apply a code" in features/codes.feature and "Empty cart" in features/cart.feature, each alike in effective tags, description, Background and own steps
    When the agent runs features verify-moved --from old
    Then it prints that 2 scenarios match
    And it exits 0

  @r17
  Scenario Outline: a scenario that changed in the move is named with what changed
    The check names which of effective tags, description or steps differ.
    Given trees old/ and features/ that both hold "Apply a code"
    And the two copies of "Apply a code" differ in their <part>
    When the agent runs features verify-moved --from old
    Then it names "Apply a code" with its <part> as changed
    And it exits 1

    Examples:
      | part           |
      | effective tags |
      | description    |
      | steps          |

  @r18
  Scenario Outline: a title held twice in either tree is a duplicate
    Scenarios are matched by title, so a title held twice cannot be matched.
    Given trees old/ and features/ that both hold "Apply a code"
    And <tree> holds a second scenario titled "Apply a code"
    When the agent runs features verify-moved --from old
    Then it names "Apply a code" as a duplicate
    And it exits 1

    Examples:
      | tree      |
      | old/      |
      | features/ |

  @r19
  Scenario Outline: holding a scenario marks it held and records what for
    A held scenario carries @holding, a "(held)" title and a line naming what it is held for, and nothing else in it changes.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    And <replacement>
    When the agent runs features hold "Apply a code" <option>
    Then the scenario carries the tag @holding
    And its title is "Apply a code (held)"
    And it has a description line naming <held for> as what it is held for
    And nothing else in the scenario is changed

    Examples:
      | replacement                          | option                  | held for        |
      | a scenario "Apply a voucher" exists  | --for "Apply a voucher" | Apply a voucher |
      | no scenario "Apply a voucher" exists | --for "Apply a voucher" | Apply a voucher |
      | no replacement is planned            | --for-removal           | removal         |

  @r20
  Scenario: holding a scenario already held is refused
    A scenario is held once.
    Given a feature file features/cart.feature with a scenario "Apply a code (held)" tagged @holding
    When the agent runs features hold "Apply a code (held)" --for "Apply a voucher"
    Then the command is rejected because the scenario is already held

  @r21
  Scenario Outline: the holding list shows each held scenario and what will retire it
    For each held scenario the list says what it is held for and how its replacement stands.
    Given a feature file features/cart.feature with a held scenario "Apply a code (held)" held for <held for>
    And <replacement>
    When the agent runs features holding
    Then the list shows "Apply a code (held)" held for <held for>, with <shown>

    Examples:
      | held for          | replacement                                  | shown                                            |
      | "Apply a voucher" | a scenario "Apply a voucher" tagged @slice-3 | the slice tag slice-3                            |
      | "Apply a voucher" | no scenario titled "Apply a voucher"         | that no scenario has the title "Apply a voucher" |
      | removal           | no replacement                               | that the slice removing the behaviour retires it |

  @r22
  Scenario: the holding list says when nothing is held
    An empty holding list is stated, not left blank.
    Given feature files in which no scenario is tagged @holding
    When the agent runs features holding
    Then it says that none is held

  @r23
  Scenario: retiring a held scenario removes its block
    Only the held scenario's block goes; the rest of the file stays as it was.
    Given a feature file features/cart.feature with a scenario "Empty cart" and a scenario "Apply a code (held)" tagged @holding
    When the agent runs features retire "Apply a code (held)"
    Then features/cart.feature no longer holds "Apply a code (held)"
    And the rest of features/cart.feature is as it was

  @r24
  Scenario: retiring a scenario that is not held is refused
    Only a held scenario can be retired.
    Given a feature file features/cart.feature with a scenario "Apply a code" not tagged @holding
    When the agent runs features retire "Apply a code"
    Then the command is rejected because the scenario is not held
    And features/cart.feature is as it was

  @r25
  Scenario Outline: a binding that names no scenario is reported
    A binding fails when no feature file has its title, or when the feature it names does not have it.
    Given a test module tests/test_cart.py whose line 12 binds the title "Apply a code" in the feature cart.feature
    And <where the title is>
    When the agent runs features bindings without --tests
    Then it reports tests/test_cart.py, line 12, the title "Apply a code" and the feature cart.feature
    And it exits 1

    Examples:
      | where the title is                                       |
      | no feature file has the title "Apply a code"             |
      | only features/codes.feature has the title "Apply a code" |

  @r26
  Scenario: bindings that all name a scenario pass
    The check says so when every binding is good.
    Given a test module tests/test_cart.py binding "Apply a code" in cart.feature
    And features/cart.feature has the scenario "Apply a code"
    When the agent runs features bindings
    Then it says that every binding names a scenario
    And it exits 0

  @r27
  Scenario: a test module that does not parse is refused
    Bindings cannot be read from a module that does not parse, and the module is named.
    Given a test module tests/test_broken.py that does not parse
    When the agent runs features bindings
    Then the command is rejected because the test module does not parse
    And the refusal names tests/test_broken.py

  @r28
  Scenario Outline: rebinding rewrites each binding of the old title and counts them
    Only the title in the binding calls changes, and the count is printed even when it is zero.
    Given a feature file features/cart.feature with a scenario "Apply a voucher"
    And test modules with <bindings> binding calls naming "Apply a code"
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then each of those binding calls names "Apply a voucher"
    And nothing else in the test modules is changed
    And it prints that <bindings> bindings were rebound

    Examples:
      | bindings |
      | 2        |
      | 0        |

  @r29
  Scenario: rebinding to a title no scenario has is refused
    A binding is never pointed at a scenario that does not exist.
    Given a test module binding "Apply a code"
    And no feature file has a scenario "Apply a voucher"
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then the command is rejected because no scenario has the new title
    And no test module is changed

  @r30
  Scenario: the plugin is written into the directory with its registration line
    The plugin file arrives in the directory, and the line to register it in the conftest.py there is printed.
    Given a directory tests/
    When the agent runs features plugin tests
    Then tests/slice_expectations.py is written
    And it prints the line that registers it in tests/conftest.py

  @r31
  Scenario Outline: a test of a planned or blocked slice is expected to fail
    A waiting slice's failing test is reported as expected, and its passing test fails the run.
    Given slice_expectations.py is registered
    And one living plan in which slice-2 is <status>
    And a test tagged @slice-2 that <result>
    When the agent runs pytest
    Then the test is reported as <reported as>
    And the run <run outcome>
    And the run reports 1 test of slice-2 expected to fail

    Examples:
      | status  | result | reported as                    | run outcome |
      | planned | fails  | an expected failure            | passes      |
      | planned | passes | a pass that should have failed | fails       |
      | blocked | fails  | an expected failure            | passes      |
      | blocked | passes | a pass that should have failed | fails       |

  @r32
  Scenario Outline: a test of a slice under way, done or gone from the plan runs as it is
    Only waiting slices are expected to fail.
    Given slice_expectations.py is registered
    And one living plan in which slice-2 is <standing>
    And a test tagged @slice-2 that passes
    When the agent runs pytest
    Then the test passes
    And the run passes

    Examples:
      | standing         |
      | in progress      |
      | green            |
      | no longer listed |

  @r33
  Scenario: naming a slice runs its tests as they are
    A planned slice's tests can be run without being expected to fail.
    Given slice_expectations.py is registered
    And one living plan in which slice-2 is planned
    And a test tagged @slice-2 that passes
    When the agent runs pytest --slice 2
    Then the test passes
    And the run passes

  @r34
  Scenario Outline: with no one living plan no test is expected to fail
    Without a single plan to read, every test runs as it is and the run says so.
    Given slice_expectations.py is registered
    And <plans>
    And a test tagged @slice-2 that passes
    When the agent runs pytest
    Then the test passes
    And the run says no test is expected to fail

    Examples:
      | plans            |
      | no living plan   |
      | two living plans |

  @r35
  Scenario: moving a title no file holds is refused
    A move, hold or retire needs the title in exactly one file; here it is in none.
    Given no feature file holds the title "Apply a code"
    When the agent runs features move "Apply a code" --to features/cart.feature
    Then the command is rejected because no file holds the title
    And no file is changed

  @r35
  Scenario: moving a title several files hold is refused
    A move, hold or retire needs the title in exactly one file; here it is in several, and each is named.
    Given features/cart.feature and features/old.feature both hold the title "Apply a code"
    When the agent runs features move "Apply a code" --to features/codes.feature
    Then the command is rejected because several files hold the title
    And the refusal names features/cart.feature and features/old.feature
    And no file is changed

  @r36
  Scenario: moving a scenario to its own file is refused
    A move must take the scenario somewhere else.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the agent runs features move "Apply a code" --to features/cart.feature
    Then the command is rejected because the destination is the scenario's own file
    And no file is changed

  @r37
  Scenario Outline: a title in only one tree is missing or added
    Every title must be in both trees; one in only the source is missing, one in only the other is added.
    Given trees old/ and features/
    And the title "Apply a code" is only in <tree>
    When the agent runs features verify-moved --from old
    Then it names "Apply a code" as <named as>
    And it exits 1

    Examples:
      | tree      | named as |
      | old/      | missing  |
      | features/ | added    |

  @r38
  Scenario Outline: a tag is found with or without its leading @
    The leading @ is optional when listing by tag.
    Given a feature file features/cart.feature with a scenario "Apply a code" tagged @slice-2
    When the agent runs features list --tag <tag>
    Then the output lists features/cart.feature with "Apply a code"

    Examples:
      | tag      |
      | @slice-2 |
      | slice-2  |

  @r39
  Scenario: holding a scenario prints its file and new title
    The agent sees where the held scenario is and what it is now called.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the agent runs features hold "Apply a code" --for-removal
    Then it prints features/cart.feature and "Apply a code (held)"

  @r40
  Scenario Outline: the holding list flags a held scenario it cannot place
    A held scenario with nothing to say what it is held for, or whose replacement has no slice tag, is flagged on its own line.
    Given a feature file features/cart.feature with a scenario "Apply a code (held)" tagged @holding
    And <condition>
    When the agent runs features holding
    Then the line for "Apply a code (held)" says <said>

    Examples:
      | condition                                                                | said                                      |
      | the scenario has no Held for: line                                       | that it has no Held for: line             |
      | it is held for "Apply a voucher", and "Apply a voucher" has no slice tag | that the replacement carries no slice tag |

  @r41
  Scenario: rebinding to a title several feature files hold is refused
    The new title must pick out one scenario.
    Given a test module binding "Apply a code"
    And features/cart.feature and features/codes.feature both hold a scenario "Apply a voucher"
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then the command is rejected because several feature files hold the new title
    And no test module is changed

  @r42
  Scenario: rebinding a title written over several lines is refused
    A binding whose title string spans lines is not rewritten, and the module and line are named.
    Given a feature file with a scenario "Apply a voucher"
    And a test module tests/test_cart.py whose binding call at line 20 names "Apply a code" in a string written over several lines
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then the command is rejected because the binding's title is written over several lines
    And the refusal names tests/test_cart.py and line 20
    And no test module is changed

  @r43
  Scenario: writing the plugin to a path that is not a directory is refused
    The plugin is written only into a directory.
    Given a file tests/notes.txt
    When the agent runs features plugin tests/notes.txt
    Then the command is rejected because the path is not a directory
    And nothing is written

  @r44
  Scenario: writing the plugin replaces an existing one and reads no feature file
    The plugin is written whatever is already there, and the feature files play no part.
    Given a directory tests/ holding an older slice_expectations.py
    And a feature file features/rules.feature that holds a Rule: block
    When the agent runs features plugin tests
    Then tests/slice_expectations.py is replaced by the plugin
    And the command is not refused

  @r45
  Scenario: the registration line for a package imports relatively
    In a package directory the plugin is imported relative to the package.
    Given a directory tests/ holding an __init__.py
    When the agent runs features plugin tests
    Then the line it prints imports slice_expectations relative to the package

  @r46
  Scenario: a refusal says why on stderr and fails
    Whatever is refused, the reason goes to stderr and the command fails.
    Given a feature file features/cart.feature with a scenario "Apply a code" not tagged @holding
    When the agent runs features retire "Apply a code"
    Then the reason for the refusal is written to stderr
    And it exits 1

  @r47
  Scenario Outline: the living plan is the one slice_plan names, or else the one plan file
    The ini value slice_plan wins; otherwise the single slices plan under docs/superpowers/plans is read, and none or several give no plan.
    Given slice_expectations.py is registered
    And <slice_plan>
    And <plan files> under docs/superpowers/plans in pytest's root directory
    When the agent runs pytest
    Then the living plan read is <plan read>

    Examples:
      | slice_plan                                                    | plan files                    | plan read                                   |
      | the ini value slice_plan names plans/current.md, which exists | one file 2026-10-01-slices.md | plans/current.md                            |
      | no ini value slice_plan                                       | one file 2026-10-01-slices.md | docs/superpowers/plans/2026-10-01-slices.md |
      | no ini value slice_plan                                       | no -slices.md file            | none                                        |
      | no ini value slice_plan                                       | two -slices.md files          | none                                        |

  @r48
  Scenario: naming several slices runs each one's tests as they are
    Each --slice adds a slice, written with or without its slice- prefix.
    Given slice_expectations.py is registered
    And one living plan in which slice-2 and slice-3 are planned
    And a passing test tagged @slice-2 and a passing test tagged @slice-3
    When the agent runs pytest --slice 2 --slice slice-3
    Then both tests pass
    And the run passes

  @r49
  Scenario Outline: the run's header names the living plan or says there is none
    The run shows which plan it read, relative to the root directory.
    Given slice_expectations.py is registered
    And <plans>
    When the agent runs pytest
    Then the run's header <header>

    Examples:
      | plans                                                       | header                                            |
      | one living plan docs/superpowers/plans/2026-10-01-slices.md | names docs/superpowers/plans/2026-10-01-slices.md |
      | no living plan                                              | says no one living plan was found                 |

  @r50
  Scenario: a slice_plan naming a missing file expects nothing to fail
    A plan file that is not there gives no expected failures, and the header shows which file was looked for.
    Given slice_expectations.py is registered
    And the ini value slice_plan names plans/missing.md, which does not exist
    And a test tagged @slice-2 that passes
    When the agent runs pytest
    Then the test passes
    And the run's header names plans/missing.md

  @r51
  Scenario: tagging with a requirement id makes it the scenario's one requirement tag
    A scenario ends with one @r<n> tag, the new one, and keeps every other tag and line.
    Given a feature file features/cart.feature whose only scenario "Apply a code" has the tags @wip, @slice-2, @r1 and @r4
    When the agent runs features tag "Apply a code" r7
    Then the scenario's tags are @wip, @slice-2 and @r7
    And every other line of features/cart.feature is unchanged
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/slice-plan-tool.feature`

~~~~~~
# formulated from spec/capabilities/slice-plan-tool.md
Feature: Slice plan tool
  Narrator: an agent or session editing a living slice plan

  Background:
    Given today is 2026-10-16

  @r1
  Scenario: an invalid plan refuses every command and names every problem
    Plan refuses to work on a plan that is already broken, lists all of what is wrong, and does not touch it.
    Given a plan whose sections are out of order and one of whose slices has no Status line
    When the agent runs `plan log "started batch"`
    Then the command is rejected because the plan is not valid
    And the refusal names both the section order and the slice missing its Status
    And the plan file is unchanged

  @r2
  Scenario: an edit that would break the plan is refused with every problem named
    An edit that would leave the plan invalid is not made, and every problem it would cause is listed.
    Given a valid plan that has a slice 3
    When the agent runs `plan add-slice 3 "Checkout"` giving the slice the one of Scenarios and Check its Kind does not take
    Then the command is rejected because the edit would make the plan invalid
    And the refusal names both the repeated slice number and the wrong one of Scenarios and Check
    And the plan file is unchanged

  @r3
  Scenario: checking a valid plan says ok
    A valid plan passes the check.
    Given a valid plan
    When the agent runs `plan check`
    Then plan says the plan is ok
    And it exits 0

  @r4
  Scenario: a section plan does not know survives an edit untouched
    Sections plan has no rules for are carried through edits exactly as written.
    Given a valid plan with a section "Notes" that plan does not know
    When the agent runs `plan log "started batch"`
    Then the "Notes" section is byte for byte as it was

  @r5
  Scenario Outline: log and backlog entries are appended with a date
    A new Log or Backlog entry goes at the end of its section, dated by --date or today.
    Given a valid plan with a <section> section holding one entry
    When the agent runs `plan <command> "check the totals"` <date option>
    Then the last entry of the <section> section is "- <date> check the totals"

    Examples:
      | command | section | date option         | date       |
      | log     | Log     |                     | 2026-10-16 |
      | log     | Log     | --date 2026-10-01   | 2026-10-01 |
      | backlog | Backlog |                     | 2026-10-16 |
      | backlog | Backlog | --date 2026-10-01   | 2026-10-01 |

  @r6
  Scenario Outline: a missing Log or Backlog section is created where it belongs
    When a command needs a section that is absent, plan adds it at its place among the other sections.
    Given a valid plan with no <section> section, whose other sections are <present sections>
    When the agent runs `plan <command> "check the totals"`
    Then the plan's sections are <sections after>, in that order

    Examples:
      | section | present sections                       | command | sections after                                   |
      | Backlog | Satisfied by existing behaviour, Log   | backlog | Satisfied by existing behaviour, Backlog, Log    |
      | Log     | Satisfied by existing behaviour, Backlog | log   | Satisfied by existing behaviour, Backlog, Log    |

  @r7
  Scenario: setting a slice's status changes only that status
    The status command touches nothing but the named slice's Status.
    Given a valid plan whose slice 2 has Status planned
    When the agent runs `plan status 2 "in progress"`
    Then slice 2's Status is in progress
    And every other line of the plan is as it was

  @r9
  Scenario: setting the status of a slice the plan does not have is refused
    The status command needs a slice that exists.
    Given a valid plan with slices 1 and 2
    When the agent runs `plan status 7 green`
    Then the command is rejected because the plan has no slice 7

  @r11
  Scenario Outline: adding a slice that does not fit is refused
    A new slice must carry the right one of Scenarios and Check for its Kind and a number not yet used.
    Given a valid plan with slices 1 and 2
    When the agent runs `plan add-slice <number> "Checkout"` <given>
    Then the command is rejected because <reason>
    And the plan file is unchanged

    Examples:
      | number | given                                                      | reason                                                  |
      | 3      | giving the one of Scenarios and Check its Kind does not take | the slice has the wrong one of Scenarios and Check for its Kind |
      | 2      | giving the one of Scenarios and Check its Kind takes        | the plan already has a slice 2                          |

  @r12
  Scenario Outline: adding a slice with or without a Lands line
    Without --lands the slice is written with a hint about its missing Lands line; with --lands the line is written quietly.
    Given a valid plan with slices 1 and 2
    When the agent runs `plan add-slice 3 "Checkout"` <lands option>
    Then slice 3 is in the plan <lands line>
    And stderr <stderr>

    Examples:
      | lands option                     | lands line                                     | stderr                                                    |
      |                                  | with no Lands line                             | says slice 3 has no Lands line and how to set it          |
      | --lands "3 production, 1 test"   | with the Lands line "3 production, 1 test"     | is empty                                                  |

  @r13
  Scenario Outline: a slice over the module budget is refused whatever the command
    A Lands line counting too many production or test modules stops any command, naming the slice, its Lands and the budget.
    Given a plan whose slice 2 has the Lands line "- Lands: <production> production, <test> test"
    When the agent runs `plan log "started batch"`
    Then the command is rejected because slice 2 is over the budget of 8 production and 4 test modules
    And the refusal names slice 2, its Lands and the budget
    And the plan file is unchanged

    Examples:
      | production | test |
      | 9          | 1    |
      | 3          | 5    |

  @r14
  Scenario Outline: a slice with a badly written or repeated Lands line is refused
    A slice may have at most one Lands line, and only in the one written form.
    Given a plan whose slice 2 has <lands lines>
    When the agent runs `plan check`
    Then the command is rejected because slice 2's Lands line is not valid
    And the refusal names slice 2

    Examples:
      | lands lines                                                         |
      | two Lands lines "- Lands: 2 production, 1 test" and "- Lands: 3 production, 1 test" |
      | the one Lands line "- Lands: 2 prod, 1 tests"                       |

  @r15
  Scenario: a slice without a Lands line is valid
    Lacking a Lands line is not a problem with the plan.
    Given an otherwise valid plan whose slice 2 has no Lands line
    When the agent runs `plan check`
    Then plan says the plan is ok

  @r16
  Scenario Outline: setting a slice's Lands line replaces any it had
    The lands command leaves the slice with exactly the Lands line it was given.
    Given a valid plan whose slice 2 has <before>
    When the agent runs `plan lands 2 "3 production, 2 test"`
    Then slice 2 has one Lands line, "- Lands: 3 production, 2 test"

    Examples:
      | before                                     |
      | no Lands line                              |
      | the Lands line "- Lands: 1 production, 1 test" |

  @r17
  Scenario: showing open slices lists every slice that is not green
    The open view gives each unfinished slice with its name and status.
    Given a valid plan with slice 1 "Cart" green, slice 2 "Checkout" in progress and slice 3 "Refunds" planned
    When the agent runs `plan show --open`
    Then plan prints "Checkout" with in progress and "Refunds" with planned
    And it does not print "Cart"

  @r18
  Scenario: showing requests lists the Log's REQUEST entries
    The requests view gives the Log's REQUEST entries and no others.
    Given a valid plan whose Log holds two REQUEST entries and one other entry
    When the agent runs `plan show --requests`
    Then plan prints the two REQUEST entries
    And it does not print the other entry

  @r19
  Scenario: showing the last suite record gives the Log's last Suite entry
    Of several suite records in the Log, only the latest is shown.
    Given a valid plan whose Log holds two `Suite:` entries
    When the agent runs `plan show --last-suite`
    Then plan prints the later `Suite:` entry
    And it does not print the earlier one

  @r20
  Scenario Outline: the current flag says whether the last suite record still holds
    The suite record holds while nothing outside the plans directory has changed since its commit.
    Given a valid plan whose last `Suite:` entry names a commit the repository has
    And since that commit <change>
    When the agent runs `plan show --last-suite --current`
    Then plan prints the record, then <verdict>
    And it exits <status>

    Examples:
      | change                                                      | verdict                   | status |
      | only a file under docs/superpowers/plans/ has changed       | `current`                 | 0      |
      | a file outside docs/superpowers/plans/ has changed          | `stale:` with the reason  | 1      |

  @r21
  Scenario: a suite record naming an unknown commit is stale
    A record whose commit the repository does not have cannot hold.
    Given a valid plan whose last `Suite:` entry names a commit the repository does not have
    When the agent runs `plan show --last-suite --current`
    Then plan says the record is stale because of that commit
    And it exits 1

  @r22
  Scenario: the current flag without last-suite is bad usage
    --current only means something alongside --last-suite.
    Given a valid plan
    When the agent runs `plan show --current`
    Then the command is rejected as bad usage
    And it exits 2

  @r24
  Scenario: archiving leaves the Log holding what is still owed and the suite record
    After archiving, the Log keeps open requests and questions, a line pointing to the archive, and the last suite record.
    Given a valid plan with a green slice and a Log holding a REQUEST, a RE-FORMULATE and a QUESTION FOR THE SPEC: entry, each with continuation lines, two `Suite:` entries and other entries
    When the agent runs `plan archive batch-1`
    Then the Log holds only the REQUEST, RE-FORMULATE and QUESTION FOR THE SPEC: entries with their continuation lines, one line naming the archive and the later `Suite:` entry, and that `Suite:` entry
    And `plan show --last-suite --current` finds that `Suite:` entry

  @r25
  Scenario Outline: archiving is refused when the archive exists or nothing is green
    An archive is never overwritten, and an archive with no green slice is never made.
    Given a valid plan <state>
    When the agent runs `plan archive batch-1`
    Then the command is rejected because <reason>

    Examples:
      | state                                                          | reason                     |
      | with a green slice, whose archive for batch-1 already exists   | the archive file exists    |
      | with no green slice                                            | no slice is green          |

  @r26
  Scenario Outline: plan works on the named file or the one plan in the current directory
    The plan is the --file argument when given, otherwise the single slices plan found under the current directory.
    Given the current directory holds the one plan docs/superpowers/plans/2026-10-01-cart-slices.md
    And there is another plan at other/2026-10-02-refunds-slices.md
    When the agent runs `plan log "started batch"` <file option>
    Then the entry is appended to <plan>

    Examples:
      | file option                                  | plan                                             |
      |                                              | docs/superpowers/plans/2026-10-01-cart-slices.md |
      | --file other/2026-10-02-refunds-slices.md    | other/2026-10-02-refunds-slices.md               |

  @r27
  Scenario Outline: without --file, no plan or several plans is refused
    When plan cannot tell which plan is meant, it says how many it found and to name one with --file.
    Given the current directory holds <count> files matching docs/superpowers/plans/*-slices.md
    When the agent runs `plan check` without --file
    Then the command is rejected because it found <count> plans
    And the refusal says to name the plan with --file

    Examples:
      | count |
      | 0     |
      | 2     |

  @r28
  Scenario: a plan file that cannot be read is refused
    An unreadable plan stops the command, and the refusal says which file.
    Given --file names a plan file that cannot be read
    When the agent runs `plan check` with that --file
    Then the command is rejected because the plan file cannot be read
    And the refusal names the file

  @r29
  Scenario Outline: showing the backlog prints each entry with its continuation lines
    The backlog view gives every Backlog entry in full, and nothing at all when there is none.
    Given a valid plan <backlog>
    When the agent runs `plan show --backlog`
    Then plan prints <output>

    Examples:
      | backlog                                                         | output                                            |
      | whose Backlog holds two entries, one with continuation lines    | both entries, the one with its continuation lines |
      | whose Backlog is empty                                          | nothing                                           |
      | with no Backlog section                                         | nothing                                           |

  @r30
  Scenario Outline: showing requests or the last suite record keeps continuation lines
    Entries in these views are printed whole, continuation lines included.
    Given a valid plan whose Log holds a REQUEST entry and a `Suite:` entry, each with continuation lines
    When the agent runs `plan show <option>`
    Then plan prints the <entry> with its continuation lines

    Examples:
      | option       | entry           |
      | --requests   | REQUEST entry   |
      | --last-suite | `Suite:` entry  |

  @r31
  Scenario Outline: a Log with no suite record
    With no Suite entry, the plain view is empty and the current check is refused.
    Given a valid plan whose Log has no `Suite:` entry
    When the agent runs `plan show <options>`
    Then <outcome>

    Examples:
      | options                  | outcome                                                          |
      | --last-suite             | plan prints nothing and exits 0                                  |
      | --last-suite --current   | the command is rejected because there is no suite record         |

  @r32
  Scenario: a suite record naming no commit is stale
    A record without a commit cannot be checked against the repository, so it does not hold.
    Given a valid plan whose last `Suite:` entry names no commit
    When the agent runs `plan show --last-suite --current`
    Then plan says the record is stale because it names no commit
    And it exits 1

  @r33
  Scenario: the stale reason counts and names every changed file
    Changed files outside the plans directory, committed or not, are all counted and listed.
    Given a valid plan whose last `Suite:` entry names a commit the repository has
    And since that commit src/cart.py has been changed and committed and src/checkout.py has been changed and not committed
    When the agent runs `plan show --last-suite --current`
    Then the stale reason gives 2 files and names src/cart.py and src/checkout.py

  @r34
  Scenario: setting the Lands line of a slice the plan does not have is refused
    The lands command needs a slice that exists, and the plan is left alone.
    Given a valid plan with slices 1 and 2
    When the agent runs `plan lands 7 "2 production, 1 test"`
    Then the command is rejected because the plan has no slice 7
    And the plan file is unchanged

  @r35
  Scenario Outline: a green status with a note counts as green
    Only the word before the Status's colon decides whether a slice is green.
    Given a valid plan whose slice 1 "Cart" has Status "green: merged early" and slice 2 "Checkout" is planned
    When the agent runs `plan <command>`
    Then <outcome>

    Examples:
      | command          | outcome                                                  |
      | show --open      | plan prints "Checkout" and does not print "Cart"         |
      | archive batch-1  | slice 1 is written to the archive and removed from the plan |

  @r36
  Scenario: archiving creates the archive directory and starts the file with the plan's title
    A missing archive directory is no obstacle, and every archive opens with the plan's title.
    Given a valid plan titled "Cart slices" with a green slice and no archive/ directory beside it
    When the agent runs `plan archive batch-1`
    Then an archive/ directory exists beside the plan
    And the archive file in it begins with the title "Cart slices"

  @r37
  Scenario Outline: the Log's archive line carries the given date or today's
    The line recording the archive is dated by --date when given.
    Given a valid plan with a green slice
    When the agent runs `plan archive batch-1` <date option>
    Then the Log's line naming the archive carries <date>

    Examples:
      | date option        | date       |
      |                    | 2026-10-16 |
      | --date 2026-10-01  | 2026-10-01 |

  @r38
  Scenario: a refused command says why on stderr and exits 1
    Every refusal explains itself on stderr and fails with status 1.
    Given a valid plan with slices 1 and 2
    When the agent runs `plan status 7 green`
    Then stderr says why the command was refused
    And it exits 1
~~~~~~
