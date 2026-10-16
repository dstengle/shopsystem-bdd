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

  @r8
  Scenario Outline: a status plan does not know is refused
    Pins that only planned, in progress and green, each with an optional note, or blocked with its reason, can be set.
    Given a valid plan whose slice 2 has Status planned
    When the agent runs `plan status 2 "<status>"`
    Then the command is rejected because <status> is not a status a slice may have
    And the plan file is unchanged

    Examples:
      | status        |
      | done          |
      | done: merged  |
      | blocked       |

  @r9
  Scenario: setting the status of a slice the plan does not have is refused
    The status command needs a slice that exists.
    Given a valid plan with slices 1 and 2
    When the agent runs `plan status 7 green`
    Then the command is rejected because the plan has no slice 7

  @r10
  Scenario Outline: an added slice goes in number order with Status planned
    Pins where a new slice lands among dotted numbers, compared part by part as whole numbers.
    Given a valid plan with slices <slices before>, in that order
    When the agent runs `plan add-slice <number> "Checkout"`
    Then the plan's slices are <slices after>, in that order
    And slice <number> has Status planned

    Examples:
      | slices before | number | slices after         |
      | 1, 2.9 and 3  | 2.10   | 1, 2.9, 2.10 and 3   |
      | 1.1 and 2     | 1      | 1, 1.1 and 2         |
      | 1 and 3       | 2      | 1, 2 and 3           |

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

  @r23
  Scenario: archiving writes the green slices and the Log beside the plan and removes those slices
    Pins the archive file's name and place, what goes into it, and that the archived slices leave the plan.
    Given a valid plan docs/superpowers/plans/foo-slices.md with slice 1 green, slice 2 planned and slice 3 green
    And its Log holds three entries
    When the agent runs `plan archive batch-1`
    Then docs/superpowers/plans/archive/foo-slices-batch-1.md holds slices 1 and 3 and not slice 2
    And it holds the three entries the Log held
    And the plan holds slice 2 and not slices 1 or 3

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
