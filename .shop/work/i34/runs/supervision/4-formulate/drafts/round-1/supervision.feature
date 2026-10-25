# formulated from spec/capabilities/supervision.md
# New scenarios only; place directly after the @r43 outline.

  # [r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.
  @r122
  Scenario Outline: when the whole suite is run <run>, a failing scenario whose requirement a capability-proposal that is <status> adds or changes is counted as <counted>
    Pins that every whole-suite run for a work-item expects the failures of requirements a capability-proposal has yet to formulate, and not those of one formulated or withdrawn.
    Given i1's work-item w1 is ready, accepting thing#r1
    And features/thing.feature has the scenario "it waits", tagged @r2, which fails
    And i1's capability-proposal p1 is <status>, <naming>
    And every worker gives DONE, the implementer committing feature.txt
    When the person runs `work run i1`
    Then the whole suite `work run` ran <run> counted "it waits" as <counted>

    Examples:
      | run                                                         | status          | naming                       | counted      |
      | in the implementer's worktree before the implementer started | drafted         | its adds naming thing#r2     | expected     |
      | in the implementer's worktree before the implementer started | approved        | its changes naming thing#r2  | expected     |
      | in the implementer's worktree before the implementer started | formulated      | its adds naming thing#r2     | not expected |
      | in the implementer's worktree before the implementer started | withdrawn       | its changes naming thing#r2  | not expected |
      | in the implementer's worktree before the implementer started | drafted         | its adds naming thing#r3     | not expected |
      | before w1's merge                                           | awaiting-answer | its adds naming thing#r2     | expected     |
      | before w1's merge                                           | merged          | its changes naming thing#r2  | expected     |
      | before w1's merge                                           | formulated      | its changes naming thing#r2  | not expected |
      | before w1's merge                                           | withdrawn       | its adds naming thing#r2     | not expected |
      | before w1's merge                                           | approved        | its changes naming thing#r3  | not expected |
