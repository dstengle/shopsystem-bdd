# generated from spec/capabilities/batch-measurement.md by features generate; do not edit
Feature: Measurement of an initiative's deliveries
  Narrator: a session measuring an initiative's deliveries

  @g1 @r1
  Scenario: `measure initiative` writes one measurement named by the day and the initiative, each ended stage with how long it took and its session's figures
    Given a logged stage l1 that is `ended`
    When the person runs `measure initiative i7-cart`
    Then `measure` prints `.shop/records/measurements/2026-10-22-i7-cart.md`
    And `measure` includes "12 minutes"
    And `measure` includes "output_tokens"
    And `measure` includes "cache_read_tokens"
    And `measure` includes "cost"
    And `measure` exits successfully

  @g2 @r2
  Scenario: `measure initiative` refuses an initiative with no `log.jsonl`
    Given an initiative log i1
    And the initiative log i1 is unwritten
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming `log.jsonl`
    And `measure` changes nothing

  @g3 @r3
  Scenario: `measure initiative` refuses an initiative fulfilling a request the queue does not hold
    Given a fulfilled request f1 that is `unheld`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the fulfilled request f1
    And `measure` changes nothing

  @g4 @r4
  Scenario: `measure initiative` refuses an initiative fulfilling a request with no asker
    Given a fulfilled request f1 that is `askerless`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the fulfilled request f1
    And `measure` changes nothing

  @g5 @r5
  Scenario: `measure initiative` refuses an initiative fulfilling more than one request
    Given an initiative log i1
    And the initiative log i1 is overfulfilling
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming "more than one request"
    And `measure` changes nothing

  @g6 @r6
  Scenario: `measure initiative` refuses a `session.json` of a shape it does not know, naming it
    Given a session file s1 that is `garbled`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the session file s1
    And `measure` changes nothing

  @g7 @r7
  Scenario: `measure initiative --sessions` refuses a transcript of a shape it does not know, naming it
    Given a transcript t1 that is `unreadable`
    When the person runs `measure initiative i7-cart --sessions sessions`
    Then `measure` exits with an error naming the transcript t1
    And `measure` changes nothing

  @g8 @r8
  Scenario: each stage is given with its session's round trips, a line break inside a transcript's JSON string not splitting its line
    Given a transcript t1 that is `found`
    And a logged stage l1
    And the logged stage l1 has the transcript t1
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "round_trips" for the logged stage l1
    And `measure` exits successfully

  @g9 @r9
  Scenario: each work-item is given with its transitions, its counts of `awaiting-answer` and `failed`, and its commits, and the totals span the first transition to the last, a time ending in `Z` read as a time in UTC
    Given the initiative log `i7-cart` holds:
      """
      {"time": "2026-10-22T07:55:00Z", "work-item": "cart-1", "before": "drafted", "after": "researched"}
      {"time": "2026-10-22T08:30:00Z", "work-item": "cart-1", "before": "researched", "after": "awaiting-answer"}
      {"time": "2026-10-22T11:40:00+02:00", "work-item": "cart-1", "before": "awaiting-answer", "after": "researched"}
      """
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "transitions"
    And `measure` includes "awaiting_answer"
    And `measure` includes "commits"
    And `measure` includes "totals"
    And `measure` includes "time_seconds"
    And `measure` includes "1 hour 45 minutes"

  @g10 @r10
  Scenario: `measure initiative` does not write over a measurement without `--replace`
    Given a measurement m1
    And the measurement m1 is present
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the measurement m1
    And `measure` changes nothing

  @g11 @r11
  Scenario: `measure initiative --replace` writes over the measurement
    Given a measurement m1
    And the measurement m1 is present
    When the person runs `measure initiative i7-cart --replace`
    Then `measure` prints `.shop/records/measurements/2026-10-22-i7-cart.md`
    And `measure` includes "12 minutes"

  @g12 @r12
  Scenario: a stage with a start and no end is given without how long it took
    Given a logged stage l1 that is `unended`
    And a session file s1 that is `filled`
    And the logged stage l1 has the session file s1
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "turns" for the logged stage l1
    And `measure` does not include "took" for the logged stage l1

  @g13 @r13
  Scenario: a stage whose `session.json` is empty is given without its session's figures, named as such
    Given a session file s1 that is `empty`
    And a logged stage l1
    And the logged stage l1 has the session file s1
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "session_json" for the logged stage l1
    And `measure` does not include "turns" for the logged stage l1

  @g14 @r14
  Scenario: a stage whose session has no transcript is given without its round trips
    Given a transcript t1 that is `lost`
    And a logged stage l1
    And the logged stage l1 has the transcript t1
    When the person runs `measure initiative i7-cart`
    Then `measure` does not include "round_trips" for the logged stage l1

  @g15 @r15
  Scenario: the request an initiative fulfils is given as internal or external
    Given a fulfilled request f1 that is `internal`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "internal"

  @g16 @r16
  Scenario: an initiative that fulfils no request is measured without an origin
    Given an initiative log i1
    And the initiative log i1 is requestless
    When the person runs `measure initiative i7-cart`
    Then `measure` does not include "origin"

  @g17 @r17
  Scenario: `--sessions` gives the sessions active inside the window and the sessions they dispatched, each with its round trips, tool uses, dispatches and compactions, and no prompt, reply or tool content
    Given the initiative log `i7-cart` holds:
      """
      {"time": "2026-10-22T09:55:00+00:00", "work-item": "cart-1", "before": "drafted", "after": "researched"}
      {"time": "2026-10-22T10:00:00+00:00", "event": "start", "work-item": "cart-1", "stage": "research", "session": "s-1"}
      {"time": "2026-10-22T10:12:00+00:00", "event": "end", "work-item": "cart-1", "stage": "research", "session": "s-1"}
      {"time": "2026-10-22T11:40:00+00:00", "work-item": "cart-1", "before": "researched", "after": "planned"}
      """
    When the person runs `measure initiative i7-cart --sessions sessions`
    Then `measure` includes "s-9"
    And `measure` includes "s-11"
    And `measure` includes "tool_uses"
    And `measure` includes "compactions"
    And `measure` does not include "s-7"
    And `measure` does not include "a secret reply"
    And `measure` does not include "a secret prompt"

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
