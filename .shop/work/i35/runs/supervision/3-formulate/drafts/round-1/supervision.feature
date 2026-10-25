  # [r73] When `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts.
  @r73
  Scenario: a work-item lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement it accepts
    Pins that a deprecated scenario is retired by the work-item that accepts its replacement's requirement, not by the one that accepts the requirement it was tagged with.
    Given i1's capability-proposal p1 is formulated, its changes naming thing#r2
    And features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it answers", tagged @r5
    And features/thing.feature has the scenario "it used to wait", tagged @deprecated and @r9, deprecated for "it waits"
    And features/thing.feature has the scenario "it used to answer", tagged @deprecated and @r2, deprecated for "it answers"
    And every worker gives DONE
    When the person runs `work run i1`
    Then the work-item drafted for p1 under thing lists "it used to wait" under its ## Retires, and neither "it used to answer", "it waits" nor "it answers"

  # [r73] When `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts.
  @r73
  Scenario: a work-item that accepts a range lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement in the range
    Pins that a range of requirements is read as each requirement in it when the deprecated scenarios a work-item retires are found through their replacements.
    Given i1's capability-proposal p1 is formulated, its changes naming thing#r3-r6
    And features/thing.feature has the scenario "it waits", tagged @r4, and the scenario "it answers", tagged @r8
    And features/thing.feature has the scenario "it used to wait", tagged @deprecated and @r9, deprecated for "it waits"
    And features/thing.feature has the scenario "it used to answer", tagged @deprecated and @r4, deprecated for "it answers"
    And every worker gives DONE
    When the person runs `work run i1`
    Then the work-item drafted for p1 under thing lists "it used to wait" under its ## Retires, and neither "it used to answer", "it waits" nor "it answers"

  # [r123] When every work-item of an initiative is `green` or `withdrawn` and a deprecated scenario's replacement's work-item, of any initiative, is `green`, `work run` shall draft one work-item, under the capability-proposal of the last-drafted work-item whose replacement it retires, that retires each deprecated scenario whose replacement's work-item is `green`.
  @r123
  Scenario: when every work-item is green or withdrawn, one work-item is drafted retiring each deprecated scenario whose replacement's work-item is green
    Pins that deprecated scenarios left behind once their replacements pass are retired by one work-item, under the proposal of the last-drafted work-item among those replacements', and that a scenario whose replacement is not yet green is left.
    Given i1's work-item w1 is green, part of the capability-proposal p1 and accepting thing#r2, and i1's work-item w2, drafted after w1, is green, part of the capability-proposal p2 and accepting other#r4
    And i1's work-item w3 is withdrawn
    And i2's work-item w4 is ready, accepting thing#r7
    And features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it closes", tagged @r7, and features/other.feature has the scenario "it answers", tagged @r4
    And features/thing.feature has the scenario "it used to wait", tagged @deprecated, deprecated for "it waits", and the scenario "it used to close", tagged @deprecated, deprecated for "it closes"
    And features/other.feature has the scenario "it used to answer", tagged @deprecated, deprecated for "it answers"
    And every worker gives DONE
    When the person runs `work run i1`
    Then one work-item was drafted in i1, part of p2, listing "it used to wait" and "it used to answer" under its ## Retires, and not "it used to close"

  # [r124] When every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft the work-item r123 names before it starts a branch review or runs `measure initiative`.
  @r124
  Scenario: the work-item retiring deprecated scenarios is drafted before the branch review starts and before measure initiative runs
    Pins that the retiring of deprecated scenarios is work of the initiative, drafted before its branch review and its measurement rather than after them.
    Given i1's work-item w1 is green, part of the capability-proposal p1 and accepting thing#r2, and w2 is withdrawn
    And features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it used to wait", tagged @deprecated, deprecated for "it waits"
    And every worker gives DONE, and the branch reviewer's result lists nothing to fix now
    When the person runs `work run i1`
    Then the work-item retiring "it used to wait" was drafted in i1 before `work run` started the branch review of i1
    And it was drafted before `work run` ran `measure initiative` on i1
