  # r220: **If** the second run of a scenario that r219 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item.
  @r220
  Scenario: a scenario that fails again on its second run, alone, has both its runs in the question written for the work-item
    Pins that the person reading the work-item's question sees the scenario's failure in the run before the merge and in its second run, not one of them only.
    Given i1's work-item w1 is ready, accepting thing#r1
    And the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE
    And the work-item's scenario "it closes", tagged @r1, fails on the implementer's branch each time it is run
    When the person runs `work run i1`
    Then w1's ## Questions holds a question giving both runs of "it closes": its run with w1's scenarios and its second run, alone
