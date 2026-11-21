# generated from spec/capabilities/measurement.md by features generate; do not edit
Feature: Measurement
  Narrator: the person

  @g2 @r2
  Scenario: A batch measured keeps its review findings by grade
    Given a proposed change p1
    And a batch b1
    And the batch b1 has the proposed change p1
    And a review finding r1
    And the review finding r1 is on the proposed change p1
    And the grade of the review finding r1 is `Critical`
    And a review finding r2
    And the review finding r2 is on the proposed change p1
    And the grade of the review finding r2 is `Critical`
    And a review finding r3
    And the review finding r3 is on the proposed change p1
    And the grade of the review finding r3 is `Important`
    And a review finding r4
    And the review finding r4 is on the proposed change p1
    And the grade of the review finding r4 is `Important`
    And a review finding r5
    And the review finding r5 is on the proposed change p1
    And the grade of the review finding r5 is `Minor`
    And a review finding r6
    And the review finding r6 is on the proposed change p1
    And the grade of the review finding r6 is `Minor`
    When the person measures the batch b1
    Then the measurement service keeps the measurement m1
    And the batch b1 has the measurement m1
    And the measurement service returns the number of review findings on the proposed change p1 whose grade is `Critical`
    And the measurement service returns the number of review findings on the proposed change p1 whose grade is `Important`
    And the measurement service returns the number of review findings on the proposed change p1 whose grade is `Minor`

  @g3 @r3
  Scenario: A defect reported in a delivered item is kept for its batch
    Given an item i1
    And a batch b1
    And the batch b1 holds the item i1
    And the status of the item i1 is `delivered`
    And a defect d1
    When the person reports the defect d1 in the item i1
    Then the measurement service keeps the defect d2
    And the defect d2 is for the batch b1
    And the item i1 has the defect d2

  @g5 @r5
  Scenario: A measurement viewed gives the round trips of a stage row
    Given the measurement `m1` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
      """
    And a round trip r1
    And a stage row s1
    And the stage row s1 has the round trip r1
    And a measurement m1
    And the measurement m1 has the stage row s1
    And a total row t1
    And the measurement m1 has the total row t1
    And a round trip r2
    And the stage row s1 has the round trip r2
    And a round trip r3
    And the stage row s1 has the round trip r3
    And a stage row s2
    And the measurement m1 has the stage row s2
    And a stage row s3
    And the measurement m1 has the stage row s3
    And a stage row s4
    And the measurement m1 does not have the stage row s4
    When the person views the measurement m1
    Then the measurement service returns the number of round trips of the stage row s1
    And the measurement service returns the stage row s2
    And the measurement service returns the stage row s3
    And the measurement service does not return the stage row s4
    And the measurement service returns the total row t1

  @g6 @r6
  Scenario: A measurement viewed gives no round trip of a stage row that has none
    Given the measurement `m2` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
      """
    And a stage row s1
    And the stage row s1 has no round trip
    And a measurement m1
    And the measurement m1 has the stage row s1
    And a stage row s2
    And the measurement m1 has the stage row s2
    And a stage row s3
    And the measurement m1 has the stage row s3
    And a stage row s4
    And the measurement m1 does not have the stage row s4
    When the person views the measurement m1
    Then the measurement service returns the stage row s2
    And the measurement service returns the stage row s3
    And the measurement service does not return the stage row s4
    And the measurement service does not return a round trip

  @g7 @r7
  Scenario: A measurement viewed gives the tool uses, dispatches and compactions of a session row
    Given the measurement `m3` holds:
      """
      {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
      """
    And a session row s1
    And a measurement m1
    And the measurement m1 has the session row s1
    And a tool use t1
    And the session row s1 has the tool use t1
    And a tool use t2
    And the session row s1 has the tool use t2
    And a dispatch d1
    And the session row s1 has the dispatch d1
    And a dispatch d2
    And the session row s1 has the dispatch d2
    And a dispatch d3
    And the session row s1 does not have the dispatch d3
    And a compaction c1
    And the session row s1 has the compaction c1
    And a compaction c2
    And the session row s1 has the compaction c2
    When the person views the measurement m1
    Then the measurement service returns the number of tool uses of the session row s1
    And the measurement service returns the dispatch d1
    And the measurement service returns the dispatch d2
    And the measurement service does not return the dispatch d3
    And the measurement service returns the number of compactions of the session row s1

  @g9 @r9
  Scenario: A measurement compared gives its tool uses and compactions
    Given the measurement `m3` holds:
      """
      {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
      """
    And a session row s1
    And a measurement m1
    And the measurement m1 has the session row s1
    And a tool use t1
    And the measurement m1 holds the tool use t1
    And a tool use t2
    And the measurement m1 holds the tool use t2
    And a compaction c1
    And the measurement m1 holds the compaction c1
    And a compaction c2
    And the measurement m1 holds the compaction c2
    When the person compares the measurement m1
    Then the measurement service returns the number of tool uses in the measurement m1
    And the measurement service returns the number of compactions in the measurement m1

  @g10 @r10
  Scenario: A batch compared with another batch gives their measurements and a ratio
    Given a batch b1
    And a batch b2
    And a measurement m1
    And a measurement m2
    And a ratio r1
    When the person compares the batch b1 with the batch b2
    Then the measurement service returns the measurement m1
    And the measurement service returns the measurement m2
    And the measurement service returns the ratio r1

  @g11 @r11
  Scenario: A measurement compared with another measurement gives their total rows and a ratio
    Given the measurement `m1` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
      """
    And the measurement `m3` holds:
      """
      {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
      """
    And a measurement m1
    And a measurement m2
    And a total row t1
    And a total row t2
    And a ratio r1
    When the person compares the measurement m1 with the measurement m2
    Then the measurement service returns the total row t1
    And the measurement service returns the total row t2
    And the measurement service returns the ratio r1

  @g12 @r12
  Scenario: A merged batch measured keeps its time, tokens, cost, test runs and opening time
    Given a batch b1
    And the status of the batch b1 is `merged`
    And a wall time w1
    And the batch b1 has the wall time w1
    And a session time s1
    And the batch b1 has the session time s1
    And a token t1
    And the batch b1 has the token t1
    And a role r1
    And the batch b1 has the role r1
    And a role r2
    And the batch b1 has the role r2
    And a test run t2
    And the measurement m1 has the test run t2
    And a test run t3
    And the measurement m1 has the test run t3
    When the person measures the batch b1
    Then the measurement service keeps the measurement m1
    And the batch b1 has the measurement m1
    And the measurement service returns the wall time w1
    And the measurement service returns the session time s1
    And the measurement service returns the token t1
    And the measurement service returns the cost c1
    And the role r1 has the cost c1
    And the measurement service returns the cost c2
    And the role r2 has the cost c2
    And the measurement service returns the duration d1
    And the test run t2 has the duration d1
    And the measurement service returns the duration d2
    And the test run t3 has the duration d2
    And the measurement service returns the opening time o1
    And the measurement m1 has the opening time o1
