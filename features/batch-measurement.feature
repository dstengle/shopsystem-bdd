# generated from spec/capabilities/batch-measurement.md by features generate; do not edit
Feature: Measurement of an initiative's deliveries
  Narrator: a session measuring an initiative's deliveries

  @g1 @r1 @r2
  Scenario: `measure initiative` writes one measurement named by the day and the initiative
    Given an initiative log `i7-cart`
    When the person runs `measure initiative i7-cart`
    Then `measure` prints `.shop/records/measurements/2026-10-22-i7-cart.md`
    And `measure` exits successfully

  @g2 @r3
  Scenario: `measure initiative` refuses an initiative with no `log.jsonl`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming `log.jsonl`
    And `measure` changes nothing

  @g3 @r4
  Scenario: `measure initiative` refuses an initiative fulfilling a request the queue does not hold
    Given an initiative log `i7-cart`
    And a fulfilled request q1 that is `unheld`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the fulfilled request q1
    And `measure` changes nothing

  @g4 @r5
  Scenario: `measure initiative` refuses an initiative fulfilling a request with no asker
    Given an initiative log `i7-cart`
    And a fulfilled request q1 that is `askerless`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the fulfilled request q1
    And `measure` changes nothing

  @g5 @r6
  Scenario: `measure initiative` refuses an initiative fulfilling more than one request
    Given an initiative log `i7-cart`
    And a fulfilled request q1 that is `external`
    And a fulfilled request q2 that is `external`
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming "more than one request"
    And `measure` changes nothing

  @g6 @r7
  Scenario: `measure initiative` refuses a `session.json` of a shape it does not know, naming it
    Given an initiative log `i7-cart`
    And the session file `s-1` holds "not a session"
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the session file `s-1`
    And `measure` changes nothing

  @g7 @r8
  Scenario: `measure initiative --sessions` refuses a transcript of a shape it does not know, naming it
    Given an initiative log `i7-cart`
    And the transcript `sessions/s-9.jsonl` holds "this is not a transcript"
    When the person runs `measure initiative i7-cart --sessions sessions`
    Then `measure` exits with an error naming the transcript `sessions/s-9.jsonl`
    And `measure` changes nothing

  @g8 @r9 @r10
  Scenario: a line break inside a transcript's JSON string does not split its line
    Given an initiative log `i7-cart`
    And a transcript `u2028` that is `found`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "round_trips"
    And `measure` exits successfully

  @g9 @r11
  Scenario: a time ending in `Z` is read as a time in UTC
    Given an initiative log `zulu`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "1 hour 45 minutes"

  @g10 @r12
  Scenario: `measure initiative` does not write over a measurement without `--replace`
    Given an initiative log `i7-cart`
    And the measurement `2026-10-22-i7-cart` holds "an earlier measurement"
    When the person runs `measure initiative i7-cart`
    Then `measure` exits with an error naming the measurement `2026-10-22-i7-cart`
    And `measure` changes nothing

  @g11 @r13 @r14
  Scenario: `measure initiative --replace` writes over the measurement
    Given an initiative log `i7-cart`
    And the measurement `2026-10-22-i7-cart` holds "an earlier measurement"
    And `--replace` is given
    When the person runs `measure initiative i7-cart`
    Then `measure` prints `.shop/records/measurements/2026-10-22-i7-cart.md`
    And `measure` includes "12 minutes"

  @g12 @r15 @r16 @r17 @r18
  Scenario: each stage with a start and an end is given with how long it took and its session's figures
    Given a logged stage `cart-1` that is `ended`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "12 minutes"
    And `measure` includes "output_tokens"
    And `measure` includes "cache_read_tokens"
    And `measure` includes "cost"

  @g13 @r19 @r20
  Scenario: a stage with a start and no end is given without how long it took
    Given a logged stage `cart-1` that is `unended`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "turns"
    And `measure` does not include "took"

  @g14 @r21 @r22
  Scenario: a stage whose `session.json` is empty is given without its session's figures, named as such
    Given an initiative log `i7-cart`
    And a session file `s-1` that is `empty`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "session_json"
    And `measure` does not include "turns"

  @g15 @r23
  Scenario: each stage is given with its session's round trips
    Given an initiative log `i7-cart`
    And a transcript `s-1` that is `found`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "round_trips"

  @g16 @r24
  Scenario: a stage whose session has no transcript is given without its round trips
    Given an initiative log `i7-cart`
    And a transcript `s-1` that is `lost`
    When the person runs `measure initiative i7-cart`
    Then `measure` does not include "round_trips"

  @g17 @r25 @r26 @r27
  Scenario: each work-item is given with its transitions, its counts of `awaiting-answer` and `failed`, and its commits
    Given an initiative log `transitions`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "transitions"
    And `measure` includes "awaiting_answer"
    And `measure` includes "commits"

  @g18 @r28 @r29
  Scenario: the totals are over the stages' sessions and span the first transition to the last
    Given an initiative log `transitions`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "totals"
    And `measure` includes "time_seconds"

  @g19 @r30
  Scenario: the request an initiative fulfils is given as internal or external
    Given an initiative log `i7-cart`
    And a fulfilled request q1 that is `internal`
    When the person runs `measure initiative i7-cart`
    Then `measure` includes "internal"

  @g20 @r31
  Scenario: an initiative that fulfils no request is measured without an origin
    Given an initiative log `i7-cart`
    When the person runs `measure initiative i7-cart`
    Then `measure` does not include "origin"

  @g21 @r32 @r33 @r34
  Scenario: `--sessions` gives the sessions active inside the window, and the sessions they dispatched
    Given an initiative log `window`
    And a transcript `sessions`
    When the person runs `measure initiative i7-cart --sessions sessions`
    Then `measure` includes "s-9"
    And `measure` includes "s-11"
    And `measure` does not include "s-7"

  @g22 @r35 @r36
  Scenario: each session `--sessions` gives is given with its round trips, tool uses, dispatches and compactions
    Given an initiative log `window`
    And a transcript `sessions`
    When the person runs `measure initiative i7-cart --sessions sessions`
    Then `measure` includes "tool_uses"
    And `measure` includes "compactions"

  @g23 @r37 @r38
  Scenario: the measurement holds no prompt, reply or tool content
    Given an initiative log `secret`
    When the person runs `measure initiative i7-cart --sessions sessions`
    Then `measure` does not include "a secret reply"
    And `measure` does not include "a secret prompt"

  @g24 @r39
  Scenario: `measure show` prints a measurement's figures as tables, a stage's round trips beside its turns
    Given a measurement `m1`
    When the person runs `measure show m1.md`
    Then `measure` prints "stages", "totals" and "round trips"

  @g25 @r40
  Scenario: `measure show` prints the stages of a measurement that gives no round trips without them
    Given a measurement `m2`
    When the person runs `measure show m2.md`
    Then `measure` does not print "round trips"

  @g26 @r41
  Scenario: `measure show` prints each session's round trips, tool uses, dispatches and compactions
    Given a measurement `m3`
    When the person runs `measure show m3.md`
    Then `measure` prints "tool uses", "dispatched" and "compactions"

  @g27 @r42
  Scenario: `measure compare` prints two measurements' totals side by side with the ratio of the second to the first
    Given a measurement `m1`
    And a measurement `m3`
    When the person runs `measure compare m1.md m3.md`
    Then `measure` prints "ratio"

  @g28 @r43
  Scenario: `measure compare` prints the totals over the sessions side by side with their ratio
    Given a measurement `m3`
    When the person runs `measure compare m3.md m3.md`
    Then `measure` prints "tool uses" and "compactions"
