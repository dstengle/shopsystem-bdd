  @r218
  Scenario: a change to .shop/work/ in the repository's own checkout, less another initiative's path run side by side, that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file
    Pins that `.shop/work/` in the main checkout, but for the parts of initiatives run beside it, is only what its last commit holds whenever a worker ends, and that a change there is a fault naming only the files of that part.
    Given i1's work-item w1 is drafted
    And an initiative i2 under .shop/work/ whose capability-proposal p2 is drafted
    And every round ends and every worker gives DONE, and while i1's researcher works another session changes .shop/work/i1/initiative.md and a session of i2 changes .shop/work/i2/initiative.md, both in the repository's own checkout without committing them
    When the person runs `work run`
    Then .shop/work/i1/initiative.md is as its last commit holds it
    And w1 is failed, naming .shop/work/i1/initiative.md
    And nothing recorded of w1 names .shop/work/i2/initiative.md
