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
    And <file> is not empty and is not of a shape measure knows
    When the session runs <command>
    Then measure refuses, naming <file>
    And nothing is written

    Examples:
      | file kind    | file                                                  | command                                              |
      | session.json | the session.json of work-item cart-1's research stage | measure initiative i7-cart                           |
      | transcript   | the transcript sessions/s-9.jsonl                     | measure initiative i7-cart with --sessions sessions  |

  @r58
  Scenario Outline: a transcript line with <line break> inside a JSON string is read as one line
    A line break that JSON allows inside a string does not split the transcript's line, so its message is read whole and counted once.
    Given i7-cart's log.jsonl gives work-item cart-1's research stage a start and an end, run in the session s-1
    And the transcript of the session s-1 holds 3 assistant messages with 3 distinct request ids
    And the text of one of those messages holds <line break> inside its JSON string
    When the session runs measure initiative i7-cart
    Then measure exits successfully
    And the measurement gives the stage
      | work-item | stage    | session | round trips |
      | cart-1    | research | s-1     | 3           |

    Examples:
      | line break |
      | U+2028     |
      | U+2029     |
      | U+0085     |

  @r59
  Scenario Outline: a time ending in Z in <file> is read as a time in UTC
    A time ending in Z is the same moment wherever measure runs, so it lines up with a time given with its offset and is never taken for the local time.
    Given the session's local time zone is UTC+05:00
    And i7-cart's log.jsonl gives its first transition at <first> and its last at <last>
    And the directory sessions holds the transcript s-9, starting at <s-9 starts> and ending at 2026-10-22T09:00:00Z
    When the session runs measure initiative i7-cart with --sessions sessions
    Then measure exits successfully
    And the measurement gives the totals
      | time              |
      | 1 hour 45 minutes |
    And the measurement gives the session s-9

    Examples:
      | file         | first                     | last                      | s-9 starts                |
      | log.jsonl    | 2026-10-22T07:55:00Z      | 2026-10-22T11:40:00+02:00 | 2026-10-22T08:30:00+00:00 |
      | a transcript | 2026-10-22T09:55:00+02:00 | 2026-10-22T11:40:00+02:00 | 2026-10-22T08:30:00Z      |

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

  @r57
  Scenario: a stage whose session.json is empty is given without its session's figures, named as such
    An empty session.json does not stop the measurement: the stage is still given, with nothing taken from that file, and says why its figures are missing.
    Given i7-cart's log.jsonl gives work-item cart-1's research stage a start at 10:00 and an end at 10:12
    And that stage was run as the agent researcher
    And that stage's session.json is empty
    When the session runs measure initiative i7-cart
    Then the measurement gives the stage
      | work-item | stage    | agent      | took       |
      | cart-1    | research | researcher | 12 minutes |
    And the measurement gives no turns, output tokens, new input tokens, cache-read tokens or cost for the stage
    And the measurement names the stage as a stage whose session.json is empty

  @r41
  Scenario: each work-item is given with its transitions, its awaiting-answer and failed counts and the commits its merge brought in
    A work-item's path through its statuses is counted, and only the commits its own merge brought into the initiative branch are its.
    Given i7-cart's log.jsonl gives work-item cart-1 the transitions
      | from            | to              |
      | drafted         | researched      |
      | researched      | failed          |
      | failed          | researched      |
      | researched      | awaiting-answer |
      | awaiting-answer | planned         |
      | planned         | ready           |
      | ready           | claimed         |
      | claimed         | done            |
      | done            | green           |
    And cart-1's work-item branch has the commits c-1 and c-2, which its merge brought into the initiative branch
    And the commit c-3 was made on the initiative branch itself
    When the session runs measure initiative i7-cart
    Then the measurement gives cart-1 those 9 transitions
    And it gives cart-1 1 time to awaiting-answer and 1 time to failed
    And it gives cart-1 the commits c-1 and c-2
    And it does not give cart-1 the commit c-3

  @r42
  Scenario: the totals are over the stages' sessions, an unended stage included, and span the first transition to the last
    The initiative's totals add up its stages' sessions, turns and round trips included, count a stage that never ended, leave out sessions only --sessions found, and run from the first transition to the last.
    Given i7-cart's log.jsonl gives its first transition at 09:55 and its last at 11:40
    And it gives work-item cart-1's research stage a start and an end, run in the session s-1
    And it gives work-item cart-1's plan stage a start and no end, run in the session s-2
    And the stages' sessions took
      | session | turns | round trips | output tokens | new input tokens | cache-read tokens | cost |
      | s-1     | 14    | 31          | 3000          | 2000             | 50000             | 0.42 |
      | s-2     | 6     | 12          | 1000          | 500              | 20000             | 0.18 |
    And the transcript sessions/s-9.jsonl starts inside i7-cart's window with 20 turns, 45 round trips, 9000 output tokens, 4000 new input tokens and 80000 cache-read tokens
    When the session runs measure initiative i7-cart with --sessions sessions
    Then the measurement gives the totals
      | stages | sessions | turns | round trips | output tokens | new input tokens | cache-read tokens | cost | time              |
      | 2      | 2        | 20    | 43          | 4000          | 2500             | 70000             | 0.60 | 1 hour 45 minutes |

  @r43 @deprecated
  Scenario: --sessions gives the sessions that start inside the window and every session they dispatched (deprecated)
    Deprecated for: --sessions gives the sessions active inside the window, starting inside it or before it with a message inside it, and every session they dispatched
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

  @r43
  Scenario: --sessions gives the sessions active inside the window, starting inside it or before it with a message inside it, and every session they dispatched
    A session belongs to the initiative when it worked inside the window, whenever it started, and what it dispatched comes with it whenever that ran.
    Given i7-cart's log.jsonl gives its first transition at 09:55 and its last at 11:40
    And the directory sessions holds the transcripts
      | session | starts | messages at         | dispatched by | output tokens | new input tokens | cache-read tokens |
      | s-7     | 09:00  | 09:00, 09:20, 12:00 |               | 500           | 100              | 4000              |
      | s-8     | 09:30  | 09:30, 09:50, 10:05 |               | 700           | 300              | 9000              |
      | s-9     | 11:00  | 11:00, 12:30        |               | 9000          | 4000             | 80000             |
      | s-11    | 12:00  | 12:00, 12:20        | s-9           | 2500          | 1500             | 30000             |
      | s-10    | 11:50  | 11:50, 12:10        |               | 400           | 200              | 6000              |
      | s-12    | 12:05  | 12:05, 12:08        | s-10          | 300           | 100              | 2000              |
    When the session runs measure initiative i7-cart with --sessions sessions
    Then the measurement gives the sessions
      | session | output tokens | new input tokens | cache-read tokens |
      | s-8     | 700           | 300              | 9000              |
      | s-9     | 9000          | 4000             | 80000             |
      | s-11    | 2500          | 1500             | 30000             |
    And it gives none of s-7, s-10 or s-12

  @r60
  Scenario: each session --sessions gives is given with its round trips, tool uses by tool name, dispatches and compactions
    How much a session did is counted from its transcript: round trips, each tool's uses, the sessions it started and how often it was compacted.
    Given i7-cart's log.jsonl gives its first transition at 09:55 and its last at 11:40
    And the directory sessions holds the transcripts
      | session | starts | dispatched by |
      | s-9     | 10:00  |               |
      | s-11    | 10:30  | s-9           |
    And the transcript of the session s-9 holds 40 assistant messages with 31 distinct request ids
    And the transcript of the session s-9 holds the tool uses Read 5 times, Grep 3 times and Agent once
    And the transcript of the session s-9 holds 2 compactions
    And the transcript of the session s-11 holds 9 assistant messages with 8 distinct request ids
    And the transcript of the session s-11 holds the tool uses Read twice
    And the transcript of the session s-11 holds no compaction
    When the session runs measure initiative i7-cart with --sessions sessions
    Then the measurement gives the sessions
      | session | round trips | tool uses                | dispatched | compactions |
      | s-9     | 31          | Read 5, Grep 3, Agent 1  | s-11       | 2           |
      | s-11    | 8           | Read 2                   |            | 0           |

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

  @r61
  Scenario: show prints each session's round trips, tool uses by tool name, dispatches and compactions beside its tokens
    A reader of the printed sessions sees how much each session did next to what it cost in tokens.
    Given the measurement .shop/records/measurements/2026-10-24-i7-cart.md that measure wrote, giving the sessions
      | session | output tokens | new input tokens | cache-read tokens | round trips | tool uses               | dispatched | compactions |
      | s-9     | 9000          | 4000             | 80000             | 31          | Read 5, Grep 3, Agent 1 | s-11       | 2           |
      | s-11    | 2500          | 1500             | 30000             | 8           | Read 2                  |            | 0           |
    When the session runs measure show for it
    Then the printed sessions show
      | session | output tokens | new input tokens | cache-read tokens | round trips | tool uses               | dispatched | compactions |
      | s-9     | 9000          | 4000             | 80000             | 31          | Read 5, Grep 3, Agent 1 | s-11       | 2           |
      | s-11    | 2500          | 1500             | 30000             | 8           | Read 2                  |            | 0           |

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

  @r62
  Scenario: compare prints the totals over the sessions of round trips, tool uses and compactions side by side with the ratio of the second to the first
    Two initiatives' sessions can be read against each other: how many round trips, tool calls of any tool, and compactions each took, and how the second differs from the first.
    Given the measurement a for i6-pay that measure wrote, giving the sessions
      | session | round trips | tool uses      | compactions |
      | s-1     | 20          | Read 6, Grep 4 | 1           |
      | s-2     | 10          | Read 2         | 0           |
    And the measurement b for i7-cart that measure wrote, giving the sessions
      | session | round trips | tool uses               | compactions |
      | s-9     | 31          | Read 5, Grep 3, Agent 1 | 2           |
      | s-11    | 14          | Read 2, Edit 4          | 1           |
    When the session runs measure compare for a and b
    Then the totals over the sessions are printed side by side
      | total       | a  | b  | ratio |
      | round trips | 30 | 45 | 1.5   |
      | tool uses   | 12 | 15 | 1.25  |
      | compactions | 1  | 3  | 3     |

  @r53
  Scenario: each stage is given with its session's round trips
    A stage's round trips are the assistant messages with their own request ids in its session's transcript, counted apart from its turns.
    Given i7-cart's log.jsonl gives work-item cart-1's research stage a start and an end, run in the session s-1
    And the session s-1 took 14 turns
    And the transcript of the session s-1 holds 40 assistant messages with 31 distinct request ids
    When the session runs measure initiative i7-cart
    Then the measurement gives the stage
      | work-item | stage    | session | turns | round trips |
      | cart-1    | research | s-1     | 14    | 31          |

  @r55
  Scenario: a stage whose session has no transcript to be found is given without its round trips
    Without the transcript the round trips cannot be counted, and the stage is still measured.
    Given i7-cart's log.jsonl gives work-item cart-1's research stage a start and an end, run in the session s-1
    And the session s-1 took 14 turns
    And no transcript of the session s-1 can be found
    When the session runs measure initiative i7-cart
    Then the measurement gives the stage with 14 turns
    And the measurement gives no round trips for the stage

  @r54
  Scenario: show prints each stage's round trips beside its turns
    A reader of the printed stages sees both counts of a session's work side by side.
    Given the measurement .shop/records/measurements/2026-10-22-i7-cart.md that measure wrote, giving work-item cart-1's research stage 14 turns and 31 round trips
    When the session runs measure show for it
    Then the printed stage of cart-1's research shows
      | turns | round trips |
      | 14    | 31          |

  @r56
  Scenario: show prints the stages of a measurement that gives no round trips without them
    An older measurement is still readable; show leaves out what it does not hold.
    Given the measurement .shop/records/measurements/2026-10-22-i6-pay.md that measure wrote, giving no round trips
    When the session runs measure show for it
    Then the stages are printed
    And no round trips are printed
