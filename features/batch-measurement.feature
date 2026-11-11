# generated from spec/capabilities/batch-measurement.md by features generate; do not edit
Feature: Measurement of an initiative's deliveries
  Narrator: a session measuring an initiative's deliveries

  @g23 @r23
  Scenario: `measure show` prints a measurement's stage rows, its total row and the number of round trips of a stage row
    Given the measurement `m1` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
      """
    And a round trip r1
    And a stage row s1
    And the stage row s1 has the round trip r1
    And a measurement m1
    And the measurement m1 has the stage row s1
    And a round trip r2
    And the stage row s1 has the round trip r2
    And a round trip r3
    And the stage row s1 has the round trip r3
    And a stage row s2
    And the measurement m1 has the stage row s2
    And a stage row s3
    And the measurement m1 has the stage row s3
    When the person runs `measure show` on the measurement m1
    Then `measure` prints the number of round trips of the stage row s1
    And `measure` prints the stage row s2
    And `measure` prints the stage row s3
    And the measurement m1 has the total row t1
    And `measure` prints the total row t1

  @g24 @r24
  Scenario: `measure show` prints the stage rows of a measurement whose stage row has no round trip without a round trip
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
    When the person runs `measure show` on the measurement m1
    Then `measure` prints the stage row s2
    And `measure` prints the stage row s3
    And `measure` does not print a round trip

  @g25 @r25
  Scenario: `measure show` prints each session row's tool uses, dispatches and compactions
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
    And a compaction c1
    And the session row s1 has the compaction c1
    And a compaction c2
    And the session row s1 has the compaction c2
    When the person runs `measure show` on the measurement m1
    Then `measure` prints the number of tool uses of the session row s1
    And `measure` prints the dispatch d1
    And `measure` prints the dispatch d2
    And `measure` prints the number of compactions of the session row s1

  @g26 @r26
  Scenario: `measure compare` prints the total rows of two measurements side by side with their ratio
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
    When the person runs `measure compare` on the measurement m1
    And the person runs `measure compare` on the measurement m2
    Then `measure` prints the total row t1
    And `measure` prints the total row t2
    And `measure` prints the ratio r1

  @g27 @r27
  Scenario: `measure compare` prints the totals over the session rows of a measurement
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
    When the person runs `measure compare` on the measurement m1
    Then `measure` prints the number of tool uses in the measurement m1
    And `measure` prints the number of compactions in the measurement m1
