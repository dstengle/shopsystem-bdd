# generated from spec/capabilities/telemetry.md by features generate; do not edit
Feature: Telemetry
  Narrator: a session measuring a batch

  @g5 @r5
  Scenario: `measure batch` writes a merged batch's measurement with its wall time, session time, tokens and cost by role
    Given a batch b1
    And the batch b1 is `merged`
    And a role r1
    And the batch b1 has the role r1
    And a role r2
    And the batch b1 has the role r2
    When the person runs `measure batch` on the batch b1
    Then the batch b1 has the measurement m1
    And the batch b1 has the wall time w1
    And the measurement m1 includes the wall time w1
    And the batch b1 has the session time s1
    And the measurement m1 includes the session time s1
    And the batch b1 has the token t1
    And the measurement m1 includes the token t1
    And the role r1 has the cost c1
    And the measurement m1 includes the cost c1
    And the role r2 has the cost c2
    And the measurement m1 includes the cost c2
    And `measure` writes the measurement m1

  @g6 @r6
  Scenario: The measurement of a batch counts the review findings on its pull request by grade
    Given a pull request p1
    And a batch b1
    And the batch b1 has the pull request p1
    And a review finding r1
    And the review finding r1 is on the pull request p1
    And the review finding r1 is `Critical`
    And a review finding r2
    And the review finding r2 is on the pull request p1
    And the review finding r2 is `Critical`
    And a review finding r3
    And the review finding r3 is on the pull request p1
    And the review finding r3 is `Important`
    And a review finding r4
    And the review finding r4 is on the pull request p1
    And the review finding r4 is `Important`
    And a review finding r5
    And the review finding r5 is on the pull request p1
    And the review finding r5 is `Minor`
    And a review finding r6
    And the review finding r6 is on the pull request p1
    And the review finding r6 is `Minor`
    When the person runs `measure batch` on the batch b1
    Then the batch b1 has the measurement m1
    And the measurement m1 includes the number of review findings on the pull request p1 whose grade is `Critical`
    And the measurement m1 includes the number of review findings on the pull request p1 whose grade is `Important`
    And the measurement m1 includes the number of review findings on the pull request p1 whose grade is `Minor`
    And `measure` writes the measurement m1

  @g7 @r7
  Scenario: A defect after the merge is traced to its item and batch
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the item i1 is `delivered`
    When the person runs `measure defect` on the item i1
    Then the defect d1 is for the batch b1
    And the item i1 has the defect d1
    And `measure` writes the defect d1

  @g8 @r8
  Scenario: `measure compare` sets the measurements of two batches side by side with their ratio
    When the person runs `measure compare` on the batch b1
    And the person runs `measure compare` on the batch b2
    Then `measure` prints the measurement m1
    And `measure` prints the measurement m2
    And `measure` prints the ratio r1
