# generated from spec/capabilities/telemetry.md by features generate; do not edit
Feature: Telemetry
  Narrator: a session measuring a batch

  @g1 @r1
  Scenario: `measure batch` writes a merged batch's measurement
    Given a batch b1 that is `merged`
    When the person runs `measure batch` on the batch b1
    Then `measure` writes the measurement m1
    And the measurement m1 is of the batch b1
    And `measure` includes "wall time"
    And `measure` includes "session time"
    And `measure` includes "tokens"
    And `measure` includes "cost by role"

  @g2 @r2
  Scenario: The review's findings are counted by grade
    Given a pull request p1
    And a batch b1
    And the pull request p1 is of the batch b1
    And a review finding r1
    And the review finding r1 is on the pull request p1
    When the person runs `measure batch` on the batch b1
    Then `measure` includes the grade of the review finding r1

  @g3 @r3
  Scenario: A defect after the merge is traced to its item and batch
    Given an item i1 that is `delivered`
    And a batch b1
    And the item i1 is in the batch b1
    When the person runs `measure defect` on the item i1
    Then `measure` writes the defect d1
    And the defect d1 is of the item i1
    And the defect d1 is for the batch b1

  @g4 @r4
  Scenario: `measure compare` sets two batches side by side
    When the person runs `measure compare batch-2 batch-3`
    Then `measure` prints "batch-2"
    And `measure` prints "batch-3"
