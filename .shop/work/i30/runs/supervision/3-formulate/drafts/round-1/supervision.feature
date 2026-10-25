# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # r117 (added): **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
  @r117
  Scenario: when the gate round `work run` started for a capability-proposal gives no question, one question asking for the approval of the proposal's lines as drafted is written under its ## Questions
    Pins that a gate with nothing to decide still reaches the person as a question to answer, so the proposal's lines are not taken as approved unasked.
    Given i1's capability-proposal p1 is drafted
    And the gate round's result gives no question, and every round ends
    When the person runs `work run i1`
    Then a round of the kind gate was started for p1
    And p1's ## Questions holds one question, asking for the approval of p1's lines as drafted

  # r110 (added): **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before `work run` exits.
  @r110
  Scenario: when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits
    Pins that fixing what a branch review found brings a new branch review in the same delivery, rather than leaving the fix unreviewed until the next `work run`.
    Given i1's work-items w1 is green, part of the capability-proposal p1, and w2 is withdrawn
    And every worker gives DONE, the first branch reviewer's result lists two findings to fix now, both concerning w1, in its findings.md, and the second lists nothing to fix now
    When the person runs `work run i1`
    Then one work-item was drafted in i1 for the two findings, and it is green
    And after that work-item turned green a second session of bdd-branch-reviewer was started, before `work run` exited

  # r19 (changed: a limit of 80 turns, was 40): **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns.
  @r19
  Scenario: a researcher is given the work-item's file set and accepted scenarios, and a limit of 80 turns
    Pins that the researcher starts from the work-item's file set and accepted scenarios, rather than searching the repository for it, and ends within a bounded number of turns.
    Given i1's work-item w1 is drafted, its file set scripts/thing.py and tests/test_thing.py
    And features/thing.feature has the scenario "it answers", tagged @r1, and the scenario "it waits", tagged @r2
    And every worker gives DONE
    When the person runs `work run i1`
    Then the researcher's brief gives scripts/thing.py and tests/test_thing.py as the work-item's file set
    And the researcher's brief names the accepted scenario "it answers" of features/thing.feature, and not "it waits"
    And the researcher was started with a limit of 80 turns
