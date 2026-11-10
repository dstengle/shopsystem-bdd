# generated from spec/capabilities/requests.md by features generate; do not edit
Feature: Requests
  Narrator: a context taking in or raising a request

  @g59 @r59
  Scenario: `work request` writes the request it is raised for
    When the person runs `work request --raised-for` on the request r1
    Then the request r2 is raised for the request r1
    And `work` writes the request r2

  @g60 @r60
  Scenario: `work request` refuses a request with no origin
    Given this command has no origin
    When the person runs `work request`
    Then `work` refuses `work request`
    And `work` names the origin o1

  @g61 @r61
  Scenario: `work request` to an upstream refuses an observation beside a job-thread
    Given a upstream entry u1
    And this bounded context holds the upstream entry u1
    When the person runs `work request --source` with `--thread`
    Then `work` refuses `work request --source`
    And `work` names `--source`

  @g62 @r62
  Scenario: A repository raises requests only as itself
    Given a text t1
    And the text t1 does not identify this bounded context
    When the person runs `work request --from` on the text t1
    Then `work` refuses `work request --from`
    And `work` names the text t1

  @g63 @r63
  Scenario: `work outcome` writes a line outcome in the upstream's turn
    Given a request r1
    And the request r1 is `open`
    When the person runs `work outcome` on the request r1
    Then the request line r2 is proposed in the request r1
    And `work` assigns the line outcome of the request line r2
    And `work` commits the request r1

  @g64 @r64
  Scenario: A side writes nothing in the other side's turn
    Given a request r1
    And the request r1 is `awaiting-asker`
    When the person runs `work outcome` on the request r1
    Then `work` refuses `work outcome`
    And `work` names the request r1

  @g65 @r65
  Scenario: The asker's repository does not write the upstream's part
    Given a request r1
    And the request r1 is `open`
    And the request r1 does not address this bounded context
    When the person runs `work outcome` on the request r1
    Then `work` refuses `work outcome`
    And `work` names the request r1

  @g66 @r66
  Scenario: `work ask` writes the upstream's question
    Given a request r1
    And the request r1 is `open`
    When the person runs `work ask` on the request r1
    Then `work` writes the question q1
    And `work` commits the request r1

  @g67 @r67
  Scenario: `work reply` writes the asker's answer
    Given a request r1
    And the request r1 is `awaiting-asker`
    And the request r1 originates from this bounded context
    When the person runs `work reply` on the request r1
    Then `work` writes the answer a1
    And `work` commits the request r1

  @g68 @r68
  Scenario: `work resolve` refuses a request that is not accepted
    Given a request r1
    And the request r1 is not `accepted`
    When the person runs `work resolve` on the request r1
    Then `work` refuses `work resolve`
    And `work` names the status of the request r1

  @g69 @r69
  Scenario: `work list` prints every request with its status and every observation no node cites
    Given a request r1
    And a request r2
    And a request r3
    And a request r4
    And an observation o1
    And a citation c1
    And the observation o1 lacks the citation c1
    And an observation o2
    And a citation c2
    And the observation o2 lacks the citation c2
    When the person runs `work list`
    Then `work` prints the request r1
    And `work` prints the request r2
    And `work` prints the status of the request r3
    And `work` prints the status of the request r4
    And `work` prints the observation o1
    And `work` prints the observation o2

  @g70 @r70
  Scenario: `work show` on a request prints its status and its lines
    Given a request line r2
    And the request line r2 is proposed in the request r1
    And a request line r3
    And the request line r3 is proposed in the request r1
    When the person runs `work show` on the request r1
    Then `work` prints the status of the request r1
    And `work` prints the request line r2
    And `work` prints the request line r3

  @g71 @r71
  Scenario: `work request` opens the request's issue
    When the person runs `work request`
    Then `work` posts the issue i1
    And the request r1 is `open`
    And `work` writes the request r1
    And `work` commits the request r1

  @g72 @r72
  Scenario: `work request` refuses an upstream with no GitHub repository
    Given a bounded context b1
    And the bounded context b1 has no host
    When the person runs `work request` on the bounded context b1
    Then `work` refuses `work request`
    And `work` names the bounded context b1

  @g73 @r73
  Scenario: `work offer` answers an ask with what may serve it
    Given a request r1
    And the request r1 is `open`
    When the session s1 runs `work offer` on the request r1
    Then `work` posts the comment c1
    And `work` sets the status of the request r1 to `awaiting-asker`
    And `work` commits the request r1

  @g74 @r74
  Scenario: `work fits` ends a request an offer serves
    Given a request r1
    And the request r1 is `awaiting-asker`
    When the person runs `work fits` on the request r1
    Then `work` sets the status of the request r1 to `delivered`
    And `work` writes the resolution r2
    And `work` posts the comment c1
    And the request r1 has the issue i1
    And `work` closes the issue i1
    And `work` commits the request r1

  @g75 @r75
  Scenario: `work propose` writes the asker's lines
    Given a request r1
    And the request r1 is `awaiting-asker`
    When the person runs `work propose` on the request r1
    Then `work` writes the request line r2
    And `work` commits the request r1

  @g76 @r76
  Scenario: `work sync` records what the other side posted
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And a field block f1
    And the comment c1 has the field block f1
    And the request r1 lacks the comment c1
    And a request r2
    And a request r3
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` prints the request r2
    And `work` prints the request r3

  @g77 @r77
  Scenario: `work sync` acts on no comment it cannot read
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And the comment c1 has no field block
    When the session s1 runs `work sync`
    Then `work` prints the comment c1
    And `work` does not write the comment c1

  @g78 @r78
  Scenario: `work turn` posts the asker's turn
    Given a request r1
    And the request r1 is `awaiting-asker`
    When the person runs `work turn` on the request r1
    Then `work` sets the status of the request r1 to `awaiting-upstream`
    And `work` sets the side of the request r1 to `upstream`
    And `work` posts the comment c1

  @g79 @r79
  Scenario: The upstream's turn ends with a line not settled, posted
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is not `accepted`
    And the request line r2 is not `refused`
    And the request line r2 is not `withdrawn`
    When the person runs `work turn` on the request r1
    Then `work` sets the status of the request r1 to `awaiting-asker`
    And `work` posts the comment c1

  @g80 @r80
  Scenario: The upstream's turn ends with every line settled and one accepted, posted for the person to accept
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And no request line blocks the request r1
    When the person runs `work turn` on the request r1
    Then `work` posts the comment c1
    And `work` keeps the side of the request r1

  @g81 @r81
  Scenario: The upstream's turn ends with every line refused, and the issue closed
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `refused`
    When the person runs `work turn` on the request r1
    Then `work` sets the status of the request r1 to `refused`
    And `work` posts the comment c1
    And the request r1 has the issue i1
    And `work` closes the issue i1

  @g82 @r82
  Scenario: A line that does not parse is not accepted
    Given a request line r1
    And the request line r1 has no logical form
    When the session s1 runs `work outcome accepted` on the request line r1
    Then `work` refuses `work outcome accepted`
    And `work` names the request line r1

  @g83 @r83
  Scenario: `work accept` accepts a request and writes its item
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And no request line blocks the request r1
    When the person runs `work accept` on the request r1
    Then `work` sets the status of the request r1 to `accepted`
    And the item i1 is `shaped`
    And `work` writes the item i1
    And `work` posts the comment c1
    And `work` commits the request r1

  @g84 @r84
  Scenario: `work accept` refuses a request with a line not settled
    Given a request line r1
    And a request r2
    And the request line r1 blocks the request r2
    When the person runs `work accept` on the request r2
    Then `work` refuses `work accept`
    And `work` names the request line r1

  @g85 @r85
  Scenario: `work resolve` posts the resolution and closes the issue
    Given a request r1
    And the request r1 is `accepted`
    When the person runs `work resolve` on the request r1
    Then `work` sets the status of the request r1 to `delivered`
    And `work` writes the resolution r2
    And `work` sets the side of the request r1 to `asker`
    And `work` posts the comment c1
    And the request r1 has the issue i1
    And `work` closes the issue i1
    And `work` commits the request r1

  @g86 @r86
  Scenario: `work watch` wakes on a readable comment the request does not hold
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And a field block f1
    And the comment c1 has the field block f1
    And the request r1 does not hold the comment c1
    When the session s1 runs `work watch`
    Then `work` prints the comment c1
    And `work` exits successfully
    And `work` does not write the comment c1

  @g87 @r87
  Scenario: `work watch` wakes on a new ask
    Given an issue i1
    And no request has the issue i1
    And a host h1
    And the host h1 holds the issue i1
    And this bounded context has the host h1
    When the session s1 runs `work watch`
    Then `work` prints the issue i1
    And `work` exits successfully

  @g88 @r88
  Scenario: `work request` opens no issue when its record is not committed
    Given a commit c1
    And this repository rejects the commit c1
    When the person runs `work request`
    Then `work` refuses `work request`
    And `work` names this repository
    And `work` does not post an issue

  @g89 @r89
  Scenario: `work turn` posts nothing when its record is not committed
    Given a commit c1
    And this repository rejects the commit c1
    And a request r1
    And the request r1 is `open`
    When the person runs `work turn` on the request r1
    Then `work` refuses `work turn`
    And `work` names this repository
    And `work` does not post a comment
    And `work` does not close an issue

  @g90 @r90
  Scenario: `work fits` posts nothing when its record is not committed
    Given a commit c1
    And this repository rejects the commit c1
    And a request r1
    And the request r1 is `awaiting-asker`
    When the person runs `work fits` on the request r1
    Then `work` refuses `work fits`
    And `work` names this repository
    And `work` does not post a comment
    And `work` does not close an issue

  @g91 @r91
  Scenario: `work reply` refuses a request this context received
    Given a request r1
    And the request r1 addresses this bounded context
    And the request r1 does not originate from this bounded context
    When the person runs `work reply` on the request r1
    Then `work` refuses `work reply`
    And `work` names the request r1

  @g92 @r92
  Scenario: The upstream's `work turn` refuses the asker's turn
    Given a request r1
    And the request r1 addresses this bounded context
    And the request r1 does not originate from this bounded context
    And the request r1 is `awaiting-asker`
    When the person runs `work turn` on the request r1
    Then `work` refuses `work turn`
    And `work` names the request r1

  @g93 @r93
  Scenario: The asker's `work turn` refuses the upstream's turn
    Given a request r1
    And the request r1 originates from this bounded context
    And the request r1 does not address this bounded context
    And the request r1 is `open`
    When the person runs `work turn` on the request r1
    Then `work` refuses `work turn`
    And `work` names the request r1

  @g94 @r94
  Scenario: The asker's `work turn` refuses a turn it has passed
    Given a request r1
    And the request r1 originates from this bounded context
    And the request r1 does not address this bounded context
    And the request r1 is `awaiting-upstream`
    When the person runs `work turn` on the request r1
    Then `work` refuses `work turn`
    And `work` names the request r1

  @g95 @r95
  Scenario: `work sync` writes no entry of the other side's part
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And a foreign entry f2
    And a field block f1
    And the field block f1 holds the foreign entry f2
    And the comment c1 has the field block f1
    And the request r1 does not hold the comment c1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` does not write the foreign entry f2

  @g96 @r96
  Scenario: `work sync` reopens no closed request (case 1)
    Given a request r1
    And the request r1 is `delivered`
    When the session s1 runs `work sync`
    Then `work` keeps the status of the request r1
    And `work` keeps the side of the request r1

  @g96 @r96
  Scenario: `work sync` reopens no closed request (case 2)
    Given a request r1
    And the request r1 is `refused`
    When the session s1 runs `work sync`
    Then `work` keeps the status of the request r1
    And `work` keeps the side of the request r1

  @g96 @r96
  Scenario: `work sync` reopens no closed request (case 3)
    Given a request r1
    And the request r1 is `withdrawn`
    When the session s1 runs `work sync`
    Then `work` keeps the status of the request r1
    And `work` keeps the side of the request r1

  @g97 @r97
  Scenario: The SessionStart hook names a sent request awaiting the upstream
    Given a request r1
    And the request r1 originates from this bounded context
    And the request r1 does not address this bounded context
    And the request r1 is `awaiting-upstream`
    When the SessionStart hook runs `work watch --hook`
    Then `work` prints the request r1

  @g98 @r98
  Scenario: The SessionStart hook names a received request awaiting the asker
    Given a request r1
    And the request r1 addresses this bounded context
    And the request r1 does not originate from this bounded context
    And the request r1 is `awaiting-asker`
    When the SessionStart hook runs `work watch --hook`
    Then `work` prints the request r1

  @g99 @r99
  Scenario: The SessionStart hook is silent with every request closed
    Given no request is `open`
    And no request is `awaiting-asker`
    And no request is `awaiting-upstream`
    And no request is `accepted`
    When the SessionStart hook runs `work watch --hook`
    Then `work` exits successfully
    And `work` does not print a request

  @g100 @r100
  Scenario: `work watch --forward` wakes on a readable comment the request does not hold
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And a field block f1
    And the comment c1 has the field block f1
    And the request r1 does not hold the comment c1
    When the session s1 runs `work watch --forward`
    Then `work` prints the comment c1
    And `work` exits successfully
    And `work` does not write the comment c1

  @g101 @r101
  Scenario: `work watch --forward` wakes on a new ask
    Given an issue i1
    And no request has the issue i1
    And a host h1
    And the host h1 holds the issue i1
    And this bounded context has the host h1
    When the session s1 runs `work watch --forward`
    Then `work` prints the issue i1
    And `work` exits successfully

  @g102 @r102
  Scenario: `work request` to an upstream refuses an observation beside a request it is raised for
    Given a upstream entry u1
    And this bounded context holds the upstream entry u1
    When the person runs `work request --source` with `--raised-for`
    Then `work` refuses `work request --source`
    And `work` names `--source`
