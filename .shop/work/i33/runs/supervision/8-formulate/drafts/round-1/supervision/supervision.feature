# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # [r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status.
  # added
  @r121
  Scenario Outline: a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now
    Pins that a branch review with nothing to ask the person counts as finding nothing to fix now, however it ended, so no fix is drafted and the initiative goes on to its measurement.
    Given i1's work-items w1 is green and w2 is withdrawn
    And every worker gives DONE, and the branch reviewer's result gives <outcome>, with no question
    When the person runs `work run i1`
    Then no work-item was drafted in i1 for the kept branch review
    And `work run` ran `measure initiative` on i1 after the branch review was kept

    Examples:
      | outcome       |
      | DONE          |
      | PARTIAL       |
      | BLOCKED       |
      | NEEDS_CONTEXT |

  # [r75] **When** every work-item of an initiative is `green` or `withdrawn` and at least one of them is `green` and its kept branch review lists nothing to fix now, `work run` shall run `measure initiative` on the initiative.
  # changed: at least one work-item `green` is now part of the condition
  @r75
  Scenario Outline: an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured>
    Pins that an initiative is measured once its work is done and at least one work-item delivered something, and not when every work-item was withdrawn.
    Given i1's work-items <work-items>
    And every worker gives DONE, and the branch reviewer's result lists nothing to fix now
    When the person runs `work run i1`
    Then `work run` <ran> on i1 after the branch review was kept

    Examples:
      | work-items                          | measured        | ran                         |
      | w1 is green and w2 is withdrawn     | is measured     | ran `measure initiative`    |
      | w1 is withdrawn and w2 is withdrawn | is not measured | ran no `measure initiative` |

  # [r105] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
  # changed: "at least one work-item that is `green`" is now part of the condition
  @r105
  Scenario Outline: an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>
    Pins that an initiative is set done only when at least one of its work-items is green, even with its branch review, measurement, analysis record and requests closed.
    Given i1 is started and its work-items <work-items>
    And i1's kept branch review lists nothing to fix now, and i1's measurement and analysis record are committed on the initiative branch
    And a request q2 kept in this context, whose asker is this context, that names i1 and is delivered
    And every worker gives DONE
    When the person runs `work run i1`
    Then i1 <status>

    Examples:
      | work-items                          | set             | status      |
      | w1 is green and w2 is withdrawn     | is set done     | is done     |
      | w1 is withdrawn and w2 is withdrawn | is not set done | is not done |
