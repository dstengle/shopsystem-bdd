# formulated from spec/capabilities/work-queue.md
Feature: Work queue
  Narrator: a person, session or script reading work-items or writing their transitions

  # r14 (changed): When `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item whose question a researcher, a planner or an implementer asked, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's and `ready` for an implementer's.
  # The existing scenario, kept until its replacement passes:
  @r14 @deprecated
  Scenario Outline: answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)
    Deprecated for: answer to a researcher's, a planner's or an implementer's question transitions the work-item to the status that stage started from
    Pins that an answer returns the work-item to the stage that asked, whichever stage that was.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by <asker>
    When the session runs `work answer w1 "Use the first reading"`
    Then .shop/work/i1/w1.md gives w1's status as <status>

    Examples:
      | asker              | status     |
      | a researcher       | drafted    |
      | a planner          | researched |
      | an implementer     | ready      |
      | a reviewer         | done       |

  # r14 (changed): When `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item whose question a researcher, a planner or an implementer asked, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's and `ready` for an implementer's.
  @r14
  Scenario Outline: answer to a researcher's, a planner's or an implementer's question transitions the work-item to the status that stage started from
    Pins that an answer returns the work-item to the stage that asked, for each of the three stages before review.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by <asker>
    When the session runs `work answer w1 "Use the first reading"`
    Then .shop/work/i1/w1.md gives w1's status as <status>
    And it exits successfully

    Examples:
      | asker          | status     |
      | a researcher   | drafted    |
      | a planner      | researched |
      | an implementer | ready      |

  # r26 (added): When `work answer <work-item> <answer>` is run, with the flag saying that the answer asks for a change, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `ready`.
  @r26
  Scenario: answer that asks for a change, to a reviewer's question, transitions the work-item to ready
    Pins that a person who wants the reviewed work changed sends the work-item back to implementation.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by a reviewer
    When the session runs `work answer w1 "Rename the flag"`, saying that the answer asks for a change
    Then .shop/work/i1/w1.md gives w1's status as ready
    And it exits successfully

  # r27 (added): When `work answer <work-item> <answer>` is run, with the flag saying that the answer accepts the work-item as it is, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `done`.
  @r27
  Scenario: answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item to done
    Pins that a person who accepts the reviewed work as it stands ends the work-item's review.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by a reviewer
    When the session runs `work answer w1 "Keep it as it is"`, saying that the answer accepts the work-item as it is
    Then .shop/work/i1/w1.md gives w1's status as done
    And it exits successfully

  # r28 (added): If `work answer <work-item> <answer>` is run without the flag saying whether the answer asks for a change or accepts the work-item as it is on an `awaiting-answer` work-item whose question a reviewer asked, then `work` shall exit with an error, saying that the answer must say which, and change nothing.
  @r28
  Scenario: answer to a reviewer's question that says neither whether it asks for a change nor whether it accepts the work-item is refused, and nothing changes
    Pins that an answer to a reviewer is never taken without saying which way it goes, and leaves the work-item awaiting its answer.
    Given an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer, its question asked by a reviewer
    When the session runs `work answer w1 "Use the first reading"`, saying neither that the answer asks for a change nor that it accepts the work-item as it is
    Then work exits with an error, saying that the answer must say whether it asks for a change or accepts the work-item as it is
    And .shop/work/i1/w1.md and .shop/work/i1/log.jsonl are as they were
