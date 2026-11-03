# generated from spec/capabilities/work-queue.md by features generate; do not edit
Feature: Work queue
  Narrator: a person, session or script reading work-items or writing their transitions

  @g1 @r1 @r2
  Scenario: `work add` drafts a work-item
    Given an initiative i1 that is `started`
    When the person runs `work add` on the initiative i1
    Then `work` writes a work-item that is `drafted`
    And `work` commits a work-item

  @g2 @r3
  Scenario: `work add` refuses an initiative that is not open
    Given an initiative i1 that is `done`
    When the person runs `work add` on the initiative i1
    Then `work` exits with an error naming the status of the initiative i1
    And `work` changes nothing

  @g3 @r4 @r5
  Scenario: `work start` begins an initiative for an accepted request
    Given a request q1 that is `accepted`
    When the person runs `work start` on the request q1
    Then `work` writes an initiative that is `proposed`
    And `work` commits an initiative

  @g4 @r6
  Scenario: `work start` refuses a request that is not accepted
    Given a request q1 that is `open`
    When the person runs `work start` on the request q1
    Then `work` exits with an error naming the request q1
    And `work` changes nothing

  @g5 @r7
  Scenario: An initiative whose work is closed becomes done
    Given a work-item w2 that is `green`
    And an initiative i1
    And a work-item w1 that is `ready`
    When the person runs `work withdraw` on the work-item w1
    Then the initiative i1 is `done`

  @g6 @r8
  Scenario: An initiative whose every work-item is withdrawn stays as it is
    Given an initiative i1 that is `started`
    And a work-item w1 that is `ready`
    When the person runs `work withdraw` on the work-item w1
    Then the initiative i1 is not `done`

  @g7 @r9
  Scenario: An open capability-proposal keeps its initiative started
    Given an initiative i1 that is `started`
    And a work-item w2 that is `green`
    And a capability-proposal p1 that is `drafted`
    And a work-item w1 that is `ready`
    When the person runs `work withdraw` on the work-item w1
    Then the initiative i1 is not `done`

  @g8 @r10 @r11
  Scenario: `work list` prints every node with its status
    Given an initiative i1
    And a work-item w1
    When the person runs `work list`
    Then `work` prints the initiative i1 and the status of the initiative i1
    And `work` prints the work-item w1 and the status of the work-item w1

  @g9 @r12
  Scenario: `work list --json` prints one JSON object
    Given `--json` is given
    When the person runs `work list`
    Then `work` prints one JSON object

  @g10 @r13
  Scenario: `work show` on an initiative prints where it stands
    Given an initiative i1
    And a work-item w1
    And the work-item w1 is kept in the initiative i1
    When the person runs `work show` on the initiative i1
    Then `work` prints the status of the initiative i1 and the work-item w1

  @g11 @r14
  Scenario: `work show` on a work-item prints its status
    Given a work-item w1
    When the person runs `work show` on the work-item w1
    Then `work` prints the status of the work-item w1

  @g12 @r15
  Scenario: `work show --json` prints one JSON object
    Given `--json` is given
    And an initiative i1
    When the person runs `work show` on the initiative i1
    Then `work` prints one JSON object

  @g13 @r16 @r17
  Scenario: `work note` appends a note to the ledger
    Given an initiative i1
    When the person runs `work note` on the initiative i1
    Then `work` writes the ledger of the initiative i1
    And `work` commits the ledger of the initiative i1

  @g14 @r18
  Scenario: `work note` refuses a note of more than one line
    Given a note n1 that is `multi-line`
    And an initiative i1
    When the person runs `work note` on the initiative i1
    Then `work` exits with an error naming the note n1
    And `work` changes nothing

  @g15 @r19 @r20 @r21
  Scenario: `work withdraw` withdraws a work-item that is not claimed or green
    Given a work-item w1 that is `ready`
    When the person runs `work withdraw` on the work-item w1
    Then the work-item w1 is `withdrawn`
    And `work` writes a transition
    And `work` commits the work-item w1

  @g16 @r22
  Scenario: `work withdraw` refuses a green work-item
    Given a work-item w1 that is `green`
    When the person runs `work withdraw` on the work-item w1
    Then `work` exits with an error naming the status of the work-item w1
    And `work` changes nothing

  @g17 @r23
  Scenario: A transition the log does not agree with is refused
    Given a work-item w1 that is `ready`
    And the work-item w1 is out of step
    When the person runs `work withdraw` on the work-item w1
    Then `work` exits with an error naming the work-item w1
    And `work` changes nothing

  @g18 @r24
  Scenario: `work retry` returns a failed work-item
    Given a work-item w1 that is `failed`
    When the person runs `work retry` on the work-item w1
    Then the work-item w1 is `claimed`

  @g19 @r25 @r26
  Scenario: `work answer` writes an answer
    Given a capability-proposal p1 that is `awaiting-answer`
    When the person runs `work answer` on the capability-proposal p1
    Then `work` writes an answer
    And `work` commits the capability-proposal p1

  @g20 @r27 @r28
  Scenario: `work answer` returns a work-item to the research stage that asked
    Given a question q1 that is `research`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then the work-item w1 is `drafted`
    And `work` writes an answer

  @g21 @r29
  Scenario: An answer to a reviewer's question that asks for a change
    Given a question q1 that is `review`
    And an answer a1 that is `--change`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then the work-item w1 is `ready`

  @g22 @r30
  Scenario: An answer to a reviewer's question that accepts the work-item
    Given a question q1 that is `review`
    And an answer a1 that is `--accept`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then the work-item w1 is `done`

  @g23 @r31
  Scenario: An answer to a reviewer's question must say which
    Given a question q1 that is `review`
    And an answer a1 that is `unflagged`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then `work` exits with an error naming the flag of the answer a1
    And `work` changes nothing

  @g24 @r32
  Scenario: `work answer` refuses an answer of more than one line
    Given an answer a1 that is `multi-line`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then `work` exits with an error naming the answer a1
    And `work` changes nothing

  @g25 @r33
  Scenario: `work answer` returns a work-item to the plan stage that asked
    Given a question q1 that is `plan`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then the work-item w1 is `researched`

  @g26 @r34
  Scenario: `work answer` returns a work-item to the implement stage that asked
    Given a question q1 that is `implement`
    And a work-item w1 that is `awaiting-answer`
    When the person runs `work answer` on the work-item w1
    Then the work-item w1 is `ready`
