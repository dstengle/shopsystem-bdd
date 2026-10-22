# formulated from spec/capabilities/work-queue.md
Feature: Work queue
  Narrator: a person, session or script reading work-items or writing their transitions

  @r1
  Scenario: add with --part-of, --under and --accepts writes a drafted work-item with the fields given
    Pins where add writes the work-item and that it holds what the command was given, as drafted.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then .shop/work/i1/w1.md is a drafted work-item w1
    And its part_of is capability-proposal/p1, its under is thing and its accepts is thing#r1

  @r2
  Scenario: add when the work-item's file already exists leaves the file as it was
    Pins that add never overwrites a work-item.
    Given an initiative i1 under .shop/work/ whose work-item w1 is ready
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then .shop/work/i1/w1.md is as it was

  @r3
  Scenario: show prints each work-item of every initiative with its status
    Pins that show reads every initiative under .shop/work/, and only their work-items.
    Given an initiative i1 under .shop/work/ whose work-items w1 is drafted and w2 is ready
    And an initiative i2 under .shop/work/ whose work-item w3 is claimed and whose capability-proposal p1 is merged
    When the session runs `work show`
    Then work prints w1 with drafted, w2 with ready and w3 with claimed
    And it prints nothing about p1

  @r4
  Scenario: a transition writes the new status into the work-item's file
    Pins that the work-item's file holds its status after a transition.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    When the script makes w1's transition to researched
    Then .shop/work/i1/w1.md gives w1's status as researched

  @r5
  Scenario: a transition appends a line to the initiative's log.jsonl with the time, the work-item, both statuses and who made it
    Pins what each transition writes, and that earlier lines stay.
    Given an initiative i1 under .shop/work/ whose work-item w1 is researched
    And .shop/work/i1/log.jsonl has one line, w1's transition from drafted to researched
    When the script makes w1's transition to planned
    Then .shop/work/i1/log.jsonl has two lines, the first as it was
    And its last line gives the time, w1, researched before, planned after, and the script as who made the transition

  @r6
  Scenario: a transition is refused when the work-item's status in its file is not the last status log.jsonl gives it
    Pins that a file and its log that disagree stop the transition, and the refusal names both.
    Given an initiative i1 under .shop/work/ whose work-item w1 is ready
    And .shop/work/i1/log.jsonl's last line for w1 is its transition to planned
    When the script makes w1's transition to claimed
    Then the transition is refused, naming .shop/work/i1/w1.md, ready and planned
    And .shop/work/i1/w1.md and .shop/work/i1/log.jsonl are as they were

  @r7
  Scenario: add when the work-item's file already exists is refused, saying so, with an error
    Pins that add on a work-item that exists is a request work cannot do, not a success.
    Given an initiative i1 under .shop/work/ whose work-item w1 is ready
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work says that the work-item w1 already exists
    And it exits with an error
    And nothing under the repository has changed

  @r7
  Scenario Outline: a command that cannot be done exits with an error, says why and changes nothing
    Pins that a missing file stops work with its reason, never a traceback, and leaves the files as they were.
    Given <setup>
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work says that <reason>
    And it exits with an error
    And nothing under the repository has changed

    Examples:
      | setup                                                   | reason                                             |
      | a repository with spec/index.md and no initiative i1    | the initiative i1 does not exist                   |
      | an initiative i1 under .shop/work/ and no spec/index.md | spec/index.md, which names the context, is missing |
      | an initiative i1 under .shop/work/ and a spec/index.md with no id | spec/index.md gives no bounded-context id |
      | an initiative i1 under .shop/work/ and a spec/index.md whose id is bounded-context | spec/index.md gives no bounded-context id |

  @r7
  Scenario: a transition of a work-item that does not exist is refused, saying why, and changes nothing
    Pins that a transition the library cannot make is refused with its reason rather than failing on a missing file.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the script makes w1's transition to researched
    Then the transition is refused, naming .shop/work/i1/w1.md
    And nothing under the repository has changed

  @r7
  Scenario Outline: add refuses a name or an initiative that is not one directory entry under .shop/work/, saying why, and changes nothing
    Pins that add writes only inside .shop/work/<initiative>/, whatever it is given.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the session runs `work add <initiative> <name> --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then work says that <reason>
    And it exits with an error
    And nothing under the repository has changed

    Examples:
      | initiative | name        | reason                                    |
      | i1         | ../../w1    | the name ../../w1 is not a file name      |
      | ../../spec | w1          | the initiative ../../spec is not a name   |

  @r7
  Scenario: add refuses a field value with a newline in it, saying why, and changes nothing
    Pins that a value given to add cannot write a second line, a status say, into the work-item.
    Given an initiative i1 under .shop/work/ with no work-item w1
    When the session runs `work add i1 w1 --part-of capability-proposal/p1 --under thing --accepts thing#r1` with a newline and `status: ready` in the --part-of value
    Then work says that the value of --part-of has a newline in it
    And it exits with an error
    And nothing under the repository has changed

  @r7
  Scenario: show refuses a file under an initiative that is not UTF-8 text, naming it
    Pins that show stops on a file it cannot read with its reason, never a traceback.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    And .shop/work/i1/w2.md is not UTF-8 text
    When the session runs `work show`
    Then work says that .shop/work/i1/w2.md is not UTF-8 text
    And it exits with an error

  @r7
  Scenario Outline: a transition of a work-item whose file <lacks> is refused, saying why, and changes nothing
    Pins that a transition writes a status only into a work-item whose frontmatter holds one, and logs nothing otherwise.
    Given an initiative i1 under .shop/work/ with a work-item w1 that <lacks>
    When the script makes w1's transition to researched
    Then the transition is refused, naming .shop/work/i1/w1.md
    And nothing under the repository has changed

    Examples:
      | lacks             |
      | has no status     |
      | has no frontmatter |

  @r7
  Scenario Outline: a transition whose log.jsonl <fault> is refused, saying why, and changes nothing
    Pins that a transition is all or nothing: the file and its log line are written together, or neither is.
    Given an initiative i1 under .shop/work/ whose work-item w1 is drafted
    And .shop/work/i1/log.jsonl <fault>
    When the script makes w1's transition to researched
    Then the transition is refused, naming <named>
    And nothing under the repository has changed

    Examples:
      | fault                        | named                              |
      | has a line that is not JSON  | line 2 of .shop/work/i1/log.jsonl  |
      | cannot be written            | .shop/work/i1/log.jsonl            |

  @r8
  Scenario Outline: retry returns a failed work-item to the status it had before the failed stage: failed from <from>
    Pins that `work retry` takes a work-item back to where its failed stage started, once the fault is remedied.
    Given an initiative i1 under .shop/work/ whose work-item w1 is failed
    And .shop/work/i1/log.jsonl gives w1's last transitions as <transitions>
    When the session runs `work retry w1`
    Then .shop/work/i1/w1.md gives w1's status as <status>

    Examples:
      | from       | transitions                                           | status     |
      | drafted    | to drafted, then from drafted to failed                | drafted    |
      | researched | to researched, then from researched to failed          | researched |
      | claimed    | to ready, then from ready to claimed, then to failed   | ready      |
      | done       | to done, then from done to failed                      | done       |
