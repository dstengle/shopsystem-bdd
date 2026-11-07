# generated from spec/capabilities/requests.md by features generate; do not edit
Feature: Requests
  Narrator: a context taking in or raising a request

  @g2 @r2
  Scenario: `work request` writes the request it is raised for
    Given `--raised-for` is given
    When the person runs `work request` on the request q1
    Then `work` writes the request q2
    And the request q2 is raised for the request q1

  @g6 @r6
  Scenario: An internal request names an origin
    Given a command c1
    And the command c1 is originless
    When the person runs `work request`
    Then `work` exits with an error naming the origin o1
    And `work` changes nothing

  @g7 @r7
  Scenario: A request to an upstream cites no observation
    Given a bounded context b1
    And the bounded context b1 is downstream
    And a command c1
    And the command c1 is sourced
    When the person runs `work request`
    Then `work` exits with an error naming the origin o1
    And `work` changes nothing

  @g8 @r8
  Scenario: A request to an upstream names the request it is raised for or a job-thread
    Given a bounded context b1
    And the bounded context b1 is downstream
    And a command c1
    And the command c1 is originless
    When the person runs `work request`
    Then `work` exits with an error naming the origin o1
    And `work` changes nothing

  @g9 @r9
  Scenario: A repository raises requests only as itself
    Given a command c1
    And the command c1 is foreign
    When the person runs `work request`
    Then `work` exits with an error naming the bounded context b1
    And `work` changes nothing

  @g14 @r14
  Scenario: `work outcome` writes a line outcome in the upstream's turn
    Given a request q1 that is `open`
    When the person runs `work outcome` on the request q1
    Then `work` writes a line outcome
    And `work` commits the request q1

  @g15 @r15
  Scenario: A side writes nothing in the other side's turn
    Given a request q1 that is `awaiting-asker`
    When the person runs `work outcome` on the request q1
    Then `work` exits with an error naming the request q1
    And `work` changes nothing

  @g16 @r16
  Scenario: The asker's repository does not write the upstream's part
    Given a bounded context b1
    And the bounded context b1 is downstream
    And a request q1 that is `open`
    When the person runs `work outcome` on the request q1
    Then `work` exits with an error naming the request q1
    And `work` changes nothing

  @g17 @r17
  Scenario: `work ask` writes the upstream's question
    Given a request q1 that is `open`
    When the person runs `work ask` on the request q1
    Then `work` writes the question q2
    And `work` commits the request q1

  @g18 @r18
  Scenario: `work reply` writes the asker's answer
    Given a request q1 that is `awaiting-asker`
    When the person runs `work reply` on the request q1
    Then `work` writes the answer a1
    And `work` commits the request q1

  @g24 @r24
  Scenario: `work resolve` refuses a request that is not accepted
    Given a request q1
    And the request q1 is not `accepted`
    When the person runs `work resolve` on the request q1
    Then `work` exits with an error naming the status of the request q1
    And `work` changes nothing

  @g25 @r25
  Scenario: `work list` prints every request with its status and every observation no node cites
    Given an observation o1
    And the observation o1 is uncited
    And an observation o2
    And the observation o2 is not uncited
    When the person runs `work list`
    Then `work` prints the request q1
    And `work` prints the status of the request q1
    And `work` prints the observation o1
    And `work` does not print the observation o2

  @g26 @r26
  Scenario: `work show` on a request prints its status and its lines
    Given a request line r1
    And a request q1
    And the request line r1 is proposed in the request q1
    When the person runs `work show` on the request q1
    Then `work` prints the status of the request q1
    And `work` prints the request line r1

  @g27 @r27
  Scenario: `work request` opens the request's issue
    When the person runs `work request`
    Then `work` posts the issue i1
    And `work` writes the request q1
    And the request q1 is `open`
    And `work` commits the request q1

  @g28 @r28
  Scenario: `work request` refuses an upstream with no GitHub repository
    Given a bounded context b1
    And the bounded context b1 is unhosted
    When the person runs `work request`
    Then `work` exits with an error naming the bounded context b1
    And `work` changes nothing

  @g29 @r29
  Scenario: `work offer` answers an ask with what may serve it
    Given a request q1 that is `open`
    When the session s1 runs `work offer` on the request q1
    Then `work` posts the comment c1
    And the request q1 is `awaiting-asker`
    And `work` commits the request q1

  @g30 @r30
  Scenario: `work fits` ends a request an offer serves
    Given a request q1 that is `awaiting-asker`
    When the person runs `work fits` on the request q1
    Then the request q1 is `delivered`
    And `work` writes the resolution r1
    And `work` posts the comment c1
    And `work` closes the issue i1
    And `work` commits the request q1

  @g31 @r31
  Scenario: `work propose` writes the asker's lines
    Given a request q1 that is `awaiting-asker`
    When the person runs `work propose` on the request q1
    Then `work` writes the request line r1
    And `work` commits the request q1

  @g32 @r32
  Scenario: `work sync` records what the other side posted
    Given a comment c1
    And the comment c1 is unrecorded
    And a comment c2
    And the comment c2 is not unrecorded
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` prints the request q1
    And `work` does not write the comment c2

  @g33 @r33
  Scenario: `work sync` acts on no comment it cannot read
    Given a comment c1
    And the comment c1 is unreadable
    When the session s1 runs `work sync`
    Then `work` prints the comment c1
    And `work` does not write the comment c1

  @g34 @r34
  Scenario: `work turn` posts the asker's turn
    Given a request q1 that is `awaiting-asker`
    When the person runs `work turn` on the request q1
    Then the request q1 is `awaiting-upstream`
    And `work` changes the side of the request q1
    And `work` posts the comment c1

  @g35 @r35
  Scenario: The upstream's turn ends with a line not settled, posted
    Given a request q1 that is `open`
    And a request line r1
    And the request line r1 is proposed in the request q1
    And the request line r1 is not settled
    When the person runs `work turn` on the request q1
    Then the request q1 is `awaiting-asker`
    And `work` posts the comment c1

  @g36 @r36
  Scenario: The upstream's turn ends with every line settled and one accepted, posted for the person to accept
    Given a request q1 that is `open`
    And a request line r1
    And the request line r1 is proposed in the request q1
    And the request line r1 is `accepted`
    When the person runs `work turn` on the request q1
    Then `work` posts the comment c1
    And `work` does not change the side of the request q1

  @g37 @r37
  Scenario: The upstream's turn ends with every line refused, and the issue closed
    Given a request q1 that is `open`
    And a request line r1
    And the request line r1 is proposed in the request q1
    And the request line r1 is `refused`
    When the person runs `work turn` on the request q1
    Then the request q1 is `refused`
    And `work` posts the comment c1
    And `work` closes the issue i1

  @g38 @r38
  Scenario: A line that does not parse is not accepted
    Given a request line r1
    And the request line r1 is unparsed
    When the session s1 runs `work outcome accepted` on the request line r1
    Then `work` exits with an error naming the request line r1
    And `work` changes nothing

  @g39 @r39
  Scenario: `work accept` accepts a request and writes its item
    Given a request q1 that is `open`
    And a request line r1
    And the request line r1 is proposed in the request q1
    And the request line r1 is `accepted`
    When the person runs `work accept` on the request q1
    Then the request q1 is `accepted`
    And `work` writes the item i1
    And the item i1 is `shaped`
    And `work` posts the comment c1
    And `work` commits the request q1

  @g40 @r40
  Scenario: `work accept` refuses a request with a line not settled
    Given a request line r1
    And a request q1
    And the request line r1 is proposed in the request q1
    And the request line r1 is not settled
    When the person runs `work accept` on the request q1
    Then `work` exits with an error naming the request line r1
    And `work` changes nothing

  @g41 @r41
  Scenario: `work resolve` posts the resolution and closes the issue
    Given a request q1 that is `accepted`
    When the person runs `work resolve` on the request q1
    Then the request q1 is `delivered`
    And `work` writes the resolution r1
    And `work` changes the side of the request q1
    And `work` posts the comment c1
    And `work` closes the issue i1
    And `work` commits the request q1

  @g43 @r43
  Scenario: `work watch` wakes on a new ask
    Given an issue i1
    And the issue i1 is untaken
    When the session s1 runs `work watch`
    Then `work` prints the issue i1
    And `work` exits successfully

  @g44 @r44
  Scenario: `work watch` wakes on a readable comment the request does not hold
    Given a comment c1
    And the comment c1 is unrecorded
    And the comment c1 is not unreadable
    When the session s1 runs `work watch`
    Then `work` prints the comment c1
    And `work` exits successfully
    And `work` does not write the comment c1

  @g45 @r45
  Scenario: `work request` opens no issue when its record is not committed
    Given a repository r1
    And the repository r1 is uncommittable
    When the person runs `work request`
    Then `work` does not post the issue i1

  @g46 @r46
  Scenario: `work turn` posts nothing when its record is not committed
    Given a repository r1
    And the repository r1 is uncommittable
    And a request q1 that is `open`
    When the person runs `work turn` on the request q1
    Then `work` does not post the comment c1
    And `work` does not close the issue i1

  @g47 @r47
  Scenario: `work fits` posts nothing when its record is not committed
    Given a repository r1
    And the repository r1 is uncommittable
    And a request q1 that is `awaiting-asker`
    When the person runs `work fits` on the request q1
    Then `work` does not post the comment c1
    And `work` does not close the issue i1

  @g48 @r48
  Scenario: The asker's `work turn` refuses a turn it has passed
    Given a request q1
    And the request q1 is sent
    And the request q1 is `awaiting-upstream`
    When the person runs `work turn` on the request q1
    Then `work` exits with an error naming the request q1

  @g49 @r49
  Scenario: `work reply` refuses a request this context received
    Given a request q1
    And the request q1 is received
    When the person runs `work reply` on the request q1
    Then `work` exits with an error naming the request q1

  @g50 @r50
  Scenario: The upstream's `work turn` refuses the asker's turn
    Given a request q1
    And the request q1 is received
    And the request q1 is `awaiting-asker`
    When the person runs `work turn` on the request q1
    Then `work` exits with an error naming the request q1

  @g51 @r51
  Scenario: The asker's `work turn` refuses the upstream's turn
    Given a request q1
    And the request q1 is sent
    And the request q1 is `open`
    When the person runs `work turn` on the request q1
    Then `work` exits with an error naming the request q1

  @g52 @r52
  Scenario: `work sync` writes no entry of the other side's part
    Given a comment c1
    And the comment c1 is unrecorded
    And a foreign entry f1
    And the comment c1 holds the foreign entry f1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` does not write the foreign entry f1

  @g53 @r53
  Scenario: `work sync` reopens no closed request
    Given a request q1
    And the request q1 is closed
    And a comment c1
    And the comment c1 is on the request q1
    And the comment c1 is unrecorded
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` does not change the status of the request q1
    And `work` does not change the side of the request q1

  @g54 @r54
  Scenario: The SessionStart hook names a sent request awaiting the upstream
    Given a request q1
    And the request q1 is sent
    And the request q1 is `awaiting-upstream`
    When the SessionStart hook runs `work watch --hook`
    Then `work` prints the request q1

  @g55 @r55
  Scenario: The SessionStart hook names a received request awaiting the asker
    Given a request q1
    And the request q1 is received
    And the request q1 is `awaiting-asker`
    When the SessionStart hook runs `work watch --hook`
    Then `work` prints the request q1

  @g56 @r56
  Scenario: The SessionStart hook is silent with every request closed
    When the SessionStart hook runs `work watch --hook`
    Then `work` exits successfully
    And `work` does not print the request q1

  @g57 @r57
  Scenario: `work watch --forward` wakes on a readable comment the request does not hold
    Given a comment c1
    And the comment c1 is unrecorded
    And the comment c1 is not unreadable
    When the session s1 runs `work watch --forward`
    Then `work` prints the comment c1
    And `work` exits successfully
    And `work` does not write the comment c1

  @g58 @r58
  Scenario: `work watch --forward` wakes on a new ask
    Given an issue i1
    And the issue i1 is untaken
    When the session s1 runs `work watch --forward`
    Then `work` prints the issue i1
    And `work` exits successfully
