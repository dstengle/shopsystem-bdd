# formulated from spec/capabilities/work-queue.md
Feature: Work queue
  Narrator: a person, session or script reading work-items or writing their transitions

  # r32: **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.
  @r32
  Scenario Outline: add given an initiative that is <status> is refused, naming its status, and changes nothing
    Pins that an initiative that has ended takes no new work-item, whichever way it ended.
    Given an initiative i1 under .shop/work/ that is <status>, whose work-item w1 is green
    When the session runs `work add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1`
    Then the add is refused because i1 is <status>, naming <status>
    And nothing under the repository has changed

    Examples:
      | status    |
      | done      |
      | abandoned |

  # r23: **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
  @r23
  Scenario Outline: a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done
    Pins that the command that completes an initiative's work ends the initiative when one of its work-items is green, and that only requests this context asked and keeps, naming the initiative, can hold it open.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready
    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    And <request>
    When the session runs `work withdraw w2`
    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    And .shop/work/i1/initiative.md gives i1's status as done
    And it exits successfully

    Examples:
      | request                                                                                     |
      | no request kept in this context names i1                                                    |
      | a request q1 kept in this context, whose asker is this context, names i1 and is delivered   |
      | a request q1 kept in this context, whose asker is another context, names i1 and is accepted |
      | a request q1 kept in this context, whose asker is this context, names i2 and is accepted    |

  # r31: **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.
  @r31
  Scenario: withdraw that leaves every work-item of an initiative withdrawn leaves the initiative's status as it is
    Pins that an initiative none of whose work was delivered is not ended by withdrawing the last of it, even with no request holding it open.
    Given an initiative i1 under .shop/work/ that is started, whose work-item w1 is withdrawn and whose work-item w2 is ready
    And .shop/work/i1/log.jsonl's last line for w2 is its transition to ready
    And no request kept in this context names i1
    When the session runs `work withdraw w2`
    Then .shop/work/i1/w2.md gives w2's status as withdrawn
    And .shop/work/i1/initiative.md gives i1's status as started
    And it exits successfully
