# generated from spec/capabilities/requests.md by features generate; do not edit
Feature: Requests
  Narrator: a context taking in or raising a request

  @g1 @r1 @r2
  Scenario: `work request` takes in an open request
    When the person runs `work request`
    Then `work` writes a request that is `open`
    And `work` commits a request

  @g2 @r3
  Scenario: `work request` writes the request it is raised for
    Given `--raised-for` is given
    And a request q1
    When the person runs `work request` on the request q1
    Then `work` writes a request raised for the request q1

  @g3 @r4
  Scenario: `work request` writes a delegation it is given
    Given `--delegation` is given
    When the person runs `work request`
    Then `work` writes a delegation

  @g4 @r5
  Scenario: `work request` refuses an empty delegation
    Given a delegation d1 that is `empty`
    When the person runs `work request`
    Then `work` exits with an error naming the delegation d1
    And `work` changes nothing

  @g5 @r6
  Scenario: `work request` refuses a line that does not parse
    Given a request line r1
    And the request line r1 is unparsed
    When the person runs `work request`
    Then `work` exits with an error naming the request line r1
    And `work` changes nothing

  @g6 @r7
  Scenario: An internal request names an origin
    Given a command c1
    And the command c1 is originless
    When the person runs `work request`
    Then `work` exits with an error naming an origin
    And `work` changes nothing

  @g7 @r8
  Scenario: A request to an upstream cites no observation
    Given a bounded context b1
    And the bounded context b1 is downstream
    And a command c1
    And the command c1 is sourced
    When the person runs `work request`
    Then `work` exits with an error naming an origin
    And `work` changes nothing

  @g8 @r9
  Scenario: A request to an upstream names the request it is raised for or a job-thread
    Given a bounded context b1
    And the bounded context b1 is downstream
    And a command c1
    And the command c1 is originless
    When the person runs `work request`
    Then `work` exits with an error naming an origin
    And `work` changes nothing

  @g9 @r10
  Scenario: A repository raises requests only as itself
    Given a command c1
    And the command c1 is foreign
    When the person runs `work request`
    Then `work` exits with an error naming a bounded context
    And `work` changes nothing

  @g10 @r11 @r12 @r13 @r14
  Scenario: `work delegate` writes a delegation in place of any
    Given a request q1 that is `open`
    When the person runs `work delegate` on the request q1
    Then `work` writes a delegation
    And `work` commits the request q1
    And `work` does not change the status of the request q1
    And `work` does not change the side of the request q1

  @g11 @r15
  Scenario: `work delegate` writes a delegation in the asker's turn
    Given a request q1 that is `awaiting-asker`
    When the person runs `work delegate` on the request q1
    Then `work` writes a delegation

  @g12 @r16
  Scenario: `work delegate` refuses an empty delegation
    Given a delegation d1 that is `empty`
    And a request q1 that is `open`
    When the person runs `work delegate` on the request q1
    Then `work` exits with an error naming the delegation d1
    And `work` changes nothing

  @g13 @r17
  Scenario: `work delegate` refuses a closed request
    Given a request q1 that is `delivered`
    When the person runs `work delegate` on the request q1
    Then `work` exits with an error naming the status of the request q1
    And `work` changes nothing

  @g14 @r18 @r19
  Scenario: `work outcome` writes a line outcome in the upstream's turn
    Given a request q1 that is `open`
    When the person runs `work outcome` on the request q1
    Then `work` writes a line outcome
    And `work` commits the request q1

  @g15 @r20
  Scenario: A side writes nothing in the other side's turn
    Given a request q1 that is `awaiting-asker`
    When the person runs `work outcome` on the request q1
    Then `work` exits with an error naming the request q1
    And `work` changes nothing

  @g16 @r21
  Scenario: The asker's repository does not write the upstream's part
    Given a bounded context b1
    And the bounded context b1 is downstream
    And a request q1 that is `open`
    When the person runs `work outcome` on the request q1
    Then `work` exits with an error naming the request q1
    And `work` changes nothing

  @g17 @r22 @r23
  Scenario: `work ask` writes the upstream's question
    Given a request q1 that is `open`
    When the person runs `work ask` on the request q1
    Then `work` writes a question
    And `work` commits the request q1

  @g18 @r24 @r25
  Scenario: `work reply` writes the asker's answer
    Given a request q1 that is `awaiting-asker`
    When the person runs `work reply` on the request q1
    Then `work` writes an answer
    And `work` commits the request q1

  @g19 @r26 @r27
  Scenario: `work turn` passes the asker's turn to the upstream
    Given a request q1 that is `awaiting-asker`
    When the person runs `work turn` on the request q1
    Then the request q1 is `awaiting-upstream`
    And `work` changes the side of the request q1

  @g20 @r28
  Scenario: The upstream's turn ends with a line not settled
    Given a request line r1 that is `rewritten`
    And a request q1 that is `open`
    When the person runs `work turn` on the request q1
    Then the request q1 is `awaiting-asker`

  @g21 @r29 @r30
  Scenario: The upstream's turn ends with every line settled and one accepted
    Given a request line r1 that is `accepted`
    And a request q1 that is `open`
    When the person runs `work turn` on the request q1
    Then the request q1 is `accepted`
    And `work` does not change the side of the request q1

  @g22 @r31
  Scenario: The upstream's turn ends with every line refused
    Given a request line r1 that is `refused`
    And a request q1 that is `open`
    When the person runs `work turn` on the request q1
    Then the request q1 is `refused`

  @g23 @r32 @r33 @r34 @r35
  Scenario: `work resolve` delivers an accepted request
    Given a request q1 that is `accepted`
    When the person runs `work resolve` on the request q1
    Then the request q1 is `delivered`
    And `work` writes a resolution
    And `work` changes the side of the request q1
    And `work` commits the request q1

  @g24 @r36
  Scenario: `work resolve` refuses a request that is not accepted
    Given a request q1 that is `open`
    When the person runs `work resolve` on the request q1
    Then `work` exits with an error naming the status of the request q1
    And `work` changes nothing

  @g25 @r37
  Scenario: `work list` prints every request with its status
    Given a request q1
    When the person runs `work list`
    Then `work` prints the request q1 and the status of the request q1

  @g26 @r38
  Scenario: `work list` prints every observation no node cites
    Given an observation o1
    When the person runs `work list`
    Then `work` prints the observation o1

  @g27 @r39
  Scenario: `work show` on a request prints its status and its lines
    Given a request q1
    And a request line r1
    And the request line r1 is proposed in the request q1
    When the person runs `work show` on the request q1
    Then `work` prints the status of the request q1 and the request line r1
