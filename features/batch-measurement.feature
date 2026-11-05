# generated from spec/capabilities/batch-measurement.md by features generate; do not edit
Feature: Measurement of an initiative's deliveries
  Narrator: a session measuring an initiative's deliveries

  @g18 @r18
  Scenario: `measure show` prints a measurement's figures as tables, a stage's round trips beside its turns
    Given the measurement `m1` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
      """
    When the person runs `measure show m1.md`
    Then `measure` prints "stages"
    And `measure` prints "totals"
    And `measure` prints "round trips"

  @g19 @r19
  Scenario: `measure show` prints the stages of a measurement that gives no round trips without them
    Given the measurement `m2` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14}}
      """
    When the person runs `measure show m2.md`
    Then `measure` prints "stages"
    And `measure` does not print "round trips"

  @g20 @r20
  Scenario: `measure show` prints each session's round trips, tool uses, dispatches and compactions
    Given the measurement `m3` holds:
      """
      {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
      """
    When the person runs `measure show m3.md`
    Then `measure` prints "tool uses"
    And `measure` prints "dispatched"
    And `measure` prints "compactions"

  @g21 @r21
  Scenario: `measure compare` prints two measurements' totals side by side with the ratio of the second to the first
    Given the measurement `m1` holds:
      """
      {"stages": [{"work-item": "cart-1", "stage": "research", "agent": "researcher", "session": "s-1", "turns": 14, "round_trips": 7}], "work_items": [], "totals": {"stages": 1, "sessions": 1, "turns": 14, "round_trips": 7}}
      """
    And the measurement `m3` holds:
      """
      {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
      """
    When the person runs `measure compare m1.md m3.md`
    Then `measure` prints "ratio"

  @g22 @r22
  Scenario: `measure compare` prints the totals over the sessions side by side with their ratio
    Given the measurement `m3` holds:
      """
      {"stages": [], "work_items": [], "totals": {"stages": 0, "sessions": 0}, "sessions": [{"session": "s-9", "started": null, "dispatched_by": null, "output_tokens": 9000, "new_input_tokens": 4000, "cache_read_tokens": 80000, "round_trips": 6, "tool_uses": {"Bash": 2}, "dispatched": ["s-11"], "compactions": 1}]}
      """
    When the person runs `measure compare m3.md m3.md`
    Then `measure` prints "tool uses"
    And `measure` prints "compactions"
