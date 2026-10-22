# formulated from spec/capabilities/batch-measurement.md
Feature: Batch measurement
  Narrator: a session measuring a closed batch

  @r39
  Scenario: measuring an initiative writes one measurement named by today's date and the initiative
    One run writes one measurement, in the measurements directory, under the day it ran and the initiative's name.
    Given today is 2026-10-22
    And the initiative i7-cart has a log.jsonl
    When the session runs measure initiative i7-cart
    Then one measurement is written for i7-cart
    And it is at .shop/records/measurements/2026-10-22-i7-cart.md

  @r46
  Scenario: an initiative with no log.jsonl is refused
    Without the log of what work run did there is nothing to measure.
    Given the initiative i7-cart has no log.jsonl
    When the session runs measure initiative i7-cart
    Then measure initiative refuses because the initiative has no log.jsonl
    And nothing is written

  @r47
  Scenario Outline: a <file kind> of a shape measure does not know is refused, naming it
    Measure does not guess at a session it cannot read; it says which file stopped it.
    Given the initiative i7-cart has a log.jsonl
    And <file> is not of a shape measure knows
    When the session runs <command>
    Then measure refuses, naming <file>
    And nothing is written

    Examples:
      | file kind    | file                                                  | command                                              |
      | session.json | the session.json of work-item cart-1's research stage | measure initiative i7-cart                           |
      | transcript   | the transcript sessions/s-9.jsonl                     | measure initiative i7-cart with --sessions sessions  |

  @r48
  Scenario: an existing measurement is not written over without --replace
    A measurement already written survives a second run unless replacing it is asked for.
    Given the measurement .shop/records/measurements/2026-10-22-i7-cart.md exists
    When the session runs measure initiative i7-cart with no --replace
    Then measure initiative refuses because the measurement exists
    And the measurement is as it was

  @r52
  Scenario: with --replace an existing measurement is written over
    Asking to replace lets a fresh measurement take the place of the one already there.
    Given the measurement .shop/records/measurements/2026-10-22-i7-cart.md exists, giving 3 stages
    And i7-cart's log.jsonl now gives 4 stages with a start and an end
    When the session runs measure initiative i7-cart with --replace
    Then the measurement .shop/records/measurements/2026-10-22-i7-cart.md is written over
    And it gives 4 stages

  @r50
  Scenario: a refusal exits with an error
    Whatever measure refuses, the session running it sees a failed command.
    Given the initiative i7-cart has no log.jsonl
    When the session runs measure initiative i7-cart
    Then measure exits with an error

  @r40
  Scenario: each stage with a start and an end is given with its session's figures
    A finished stage is measured by who ran it, in which session, for how long and at what cost.
    Given i7-cart's log.jsonl gives work-item cart-1's research stage a start at 10:00 and an end at 10:12
    And that stage was run as the agent researcher in the session s-1
    And the session s-1 took 14 turns, 3000 output tokens, 2000 new input tokens and 50000 cache-read tokens, costing 0.42
    When the session runs measure initiative i7-cart
    Then the measurement gives the stage
      | work-item | stage    | agent      | session | took       | turns | output tokens | new input tokens | cache-read tokens | cost |
      | cart-1    | research | researcher | s-1     | 12 minutes | 14    | 3000          | 2000             | 50000             | 0.42 |

  @r51
  Scenario: a stage with a start and no end is given with its session's figures but not how long it took
    A stage that never ended is still measured, with everything a finished stage gives except its time.
    Given i7-cart's log.jsonl gives work-item cart-1's plan stage a start at 10:20 and no end
    And that stage was run as the agent planner in the session s-2
    And the session s-2 took 6 turns, 1000 output tokens, 500 new input tokens and 20000 cache-read tokens, costing 0.18
    When the session runs measure initiative i7-cart
    Then the measurement gives the stage
      | work-item | stage | agent   | session | turns | output tokens | new input tokens | cache-read tokens | cost |
      | cart-1    | plan  | planner | s-2     | 6     | 1000          | 500              | 20000             | 0.18 |
    And the measurement gives no time for how long the stage took

  @r41
  Scenario: each work-item is given with its transitions, its awaiting-ruling and failed counts and the commits its merge brought in
    A work-item's path through its statuses is counted, and only the commits its own merge brought into the initiative branch are its.
    Given i7-cart's log.jsonl gives work-item cart-1 the transitions
      | from            | to              |
      | drafted         | researched      |
      | researched      | failed          |
      | failed          | researched      |
      | researched      | awaiting-ruling |
      | awaiting-ruling | planned         |
      | planned         | ready           |
      | ready           | claimed         |
      | claimed         | done            |
      | done            | green           |
    And cart-1's work-item branch has the commits c-1 and c-2, which its merge brought into the initiative branch
    And the commit c-3 was made on the initiative branch itself
    When the session runs measure initiative i7-cart
    Then the measurement gives cart-1 those 9 transitions
    And it gives cart-1 1 time to awaiting-ruling and 1 time to failed
    And it gives cart-1 the commits c-1 and c-2
    And it does not give cart-1 the commit c-3

  @r42
  Scenario: the totals are over the stages' sessions, an unended stage included, and span the first transition to the last
    The initiative's totals add up its stages' sessions, count a stage that never ended, leave out sessions only --sessions found, and run from the first transition to the last.
    Given i7-cart's log.jsonl gives its first transition at 09:55 and its last at 11:40
    And it gives work-item cart-1's research stage a start and an end, run in the session s-1
    And it gives work-item cart-1's plan stage a start and no end, run in the session s-2
    And the stages' sessions took
      | session | output tokens | new input tokens | cache-read tokens | cost |
      | s-1     | 3000          | 2000             | 50000             | 0.42 |
      | s-2     | 1000          | 500              | 20000             | 0.18 |
    And the transcript sessions/s-9.jsonl starts inside i7-cart's window with 9000 output tokens, 4000 new input tokens and 80000 cache-read tokens
    When the session runs measure initiative i7-cart with --sessions sessions
    Then the measurement gives the totals
      | stages | sessions | output tokens | new input tokens | cache-read tokens | cost | time              |
      | 2      | 2        | 4000          | 2500             | 70000             | 0.60 | 1 hour 45 minutes |

  @r43
  Scenario: --sessions gives the sessions that start inside the window and every session they dispatched
    A session belongs to the initiative by when it started, and what it dispatched comes with it whenever that ran.
    Given i7-cart's log.jsonl gives its first transition at 09:55 and its last at 11:40
    And the directory sessions holds the transcripts
      | session | starts | ends  | dispatched by | output tokens | new input tokens | cache-read tokens |
      | s-8     | 09:30  | 10:10 |               | 700           | 300              | 9000              |
      | s-9     | 11:00  | 12:30 |               | 9000          | 4000             | 80000             |
      | s-11    | 12:00  | 12:20 | s-9           | 2500          | 1500             | 30000             |
      | s-10    | 11:50  | 12:10 |               | 400           | 200              | 6000              |
    When the session runs measure initiative i7-cart with --sessions sessions
    Then the measurement gives the sessions
      | session | output tokens | new input tokens | cache-read tokens |
      | s-9     | 9000          | 4000             | 80000             |
      | s-11    | 2500          | 1500             | 30000             |
    And it gives neither s-8 nor s-10


  @r49
  Scenario: the measurement holds no prompt, reply or tool content
    What the sessions said and did is counted, never copied into the measurement.
    Given work-item cart-1's research stage, whose session's reply reads "the cart rounds down"
    And the transcript sessions/s-9.jsonl, starting and ending inside i7-cart's window, whose prompt reads "measure the cart" and whose tool call reads "grep rounding"
    When the session runs measure initiative i7-cart with --sessions sessions
    Then the measurement holds none of "the cart rounds down", "measure the cart" or "grep rounding"

  @r44
  Scenario: show prints a measurement's figures as tables
    A measurement can be read without opening the record.
    Given the measurement .shop/records/measurements/2026-10-22-i7-cart.md that measure wrote
    When the session runs measure show for it
    Then the measurement's figures are printed as tables

  @r45
  Scenario: compare prints two measurements' totals side by side with the ratio of the second to the first
    Two initiatives' deliveries can be read against each other, with how the second differs from the first.
    Given the measurement a for i6-pay, whose totals are 4 stages, 100000 output tokens and a cost of 2.00
    And the measurement b for i7-cart, whose totals are 6 stages, 150000 output tokens and a cost of 3.00
    When the session runs measure compare for a and b
    Then the totals are printed side by side
      | total         | a      | b      | ratio |
      | stages        | 4      | 6      | 1.5   |
      | output tokens | 100000 | 150000 | 1.5   |
      | cost          | 2.00   | 3.00   | 1.5   |
