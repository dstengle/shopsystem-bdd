# generated from spec/capabilities/requests.md by features generate; do not edit
Feature: Requests
  Narrator: a context taking in or raising a request

  @g59 @r59
  Scenario: `work request` writes the request it is raised for
    Given a request r1
    When the person runs `work request` with the `--raised-for` option set to the request r1
    Then the request r2 is raised for the request r1
    And `work` writes the request r2

  @g60 @r60
  Scenario: `work request` refuses a request with no origin
    When the person runs `work request` without the `--source` , `--thread` and `--raised-for` options
    Then `work` refuses `work request`
    And `work` names the `--thread` option

  @g61 @r61
  Scenario: `work request` to an upstream refuses an observation beside a job-thread
    Given an upstream entry u1
    And this bounded context holds the upstream entry u1
    When the person runs `work request` with the `--source` and `--thread` options
    Then `work` refuses `work request`
    And `work` names the `--source` option

  @g62 @r62
  Scenario: A repository raises requests only as itself
    Given a text t1
    And the text t1 does not identify this bounded context
    When the person runs `work request` with the `--from` option set to the text t1
    Then `work` refuses `work request`
    And `work` names the text t1

  @g63 @r63
  Scenario: `work outcome` writes a line outcome in the upstream's turn
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    When the person runs `work outcome accepted` on the request line r2
    Then `work` sets the line outcome of the request line r2 to `accepted`
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
  Scenario: `work list` prints every request with its status and every observation no request or initiative cites
    Given a request r1
    And a request r2
    And a request r3
    And a request r4
    And an observation o1
    And no request cites the observation o1
    And no initiative cites the observation o1
    And an observation o2
    And no request cites the observation o2
    And no initiative cites the observation o2
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
    And the bounded context b1 has no GitHub repository
    When the person runs `work request` with the `--to` option set to the bounded context b1
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
    And the comment c1 conforms to the comment form
    And the request r1 does not hold the comment c1
    And a request r2
    And a request r3
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` prints the request r2
    And `work` prints the request r3

  @g77 @r77
  Scenario: `work sync` acts on no comment that does not conform to the comment form
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And the comment c1 does not conform to the comment form
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
  Scenario: The upstream's turn ends with a line that has no outcome, posted
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
  Scenario: The upstream's turn ends with every line accepted, refused or withdrawn and one accepted, posted for the person to accept (case 1)
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `accepted`
    When the person runs `work turn` on the request r1
    Then `work` posts the comment c1
    And `work` keeps the side of the request r1

  @g80 @r80
  Scenario: The upstream's turn ends with every line accepted, refused or withdrawn and one accepted, posted for the person to accept (case 2)
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `refused`
    When the person runs `work turn` on the request r1
    Then `work` posts the comment c1
    And `work` keeps the side of the request r1

  @g80 @r80
  Scenario: The upstream's turn ends with every line accepted, refused or withdrawn and one accepted, posted for the person to accept (case 3)
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `withdrawn`
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
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `refused`
    When the person runs `work turn` on the request r1
    Then `work` sets the status of the request r1 to `refused`
    And `work` posts the comment c1
    And the request r1 has the issue i1
    And `work` closes the issue i1

  @g82 @r82
  Scenario: A line that does not parse is not accepted
    Given a requirement grammar r2
    And this bounded context has the requirement grammar r2
    And a request line r1
    And the request line r1 does not conform to the requirement grammar r2
    When the session s1 runs `work outcome accepted` on the request line r1
    Then `work` refuses `work outcome accepted`
    And `work` names the request line r1

  @g83 @r83
  Scenario: `work accept` accepts a request and writes its item (case 1)
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `accepted`
    When the person runs `work accept` on the request r1
    Then `work` sets the status of the request r1 to `accepted`
    And the item i1 is `shaped`
    And `work` writes the item i1
    And `work` posts the comment c1
    And `work` commits the request r1

  @g83 @r83
  Scenario: `work accept` accepts a request and writes its item (case 2)
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `refused`
    When the person runs `work accept` on the request r1
    Then `work` sets the status of the request r1 to `accepted`
    And the item i1 is `shaped`
    And `work` writes the item i1
    And `work` posts the comment c1
    And `work` commits the request r1

  @g83 @r83
  Scenario: `work accept` accepts a request and writes its item (case 3)
    Given a request r1
    And the request r1 is `open`
    And a request line r2
    And the request line r2 is proposed in the request r1
    And the request line r2 is `accepted`
    And a request line r3
    And the request line r3 is proposed in the request r1
    And the request line r3 is `withdrawn`
    When the person runs `work accept` on the request r1
    Then `work` sets the status of the request r1 to `accepted`
    And the item i1 is `shaped`
    And `work` writes the item i1
    And `work` posts the comment c1
    And `work` commits the request r1

  @g84 @r84
  Scenario: `work accept` refuses a request with a line that has no outcome
    Given a request line r1
    And a request r2
    And the request line r1 is proposed in the request r2
    And the request line r1 is not `accepted`
    And the request line r1 is not `refused`
    And the request line r1 is not `withdrawn`
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
  Scenario: `work watch` wakes on a comment that conforms to the comment form and that the request does not hold
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the request r1 does not hold the comment c1
    When the session s1 runs `work watch`
    Then `work` prints the comment c1
    And `work` exits successfully
    And `work` does not write the comment c1

  @g87 @r87
  Scenario: `work watch` wakes on a new ask
    Given a GitHub repository g1
    And this bounded context has the GitHub repository g1
    And an issue i1
    And the GitHub repository g1 holds the issue i1
    And the issue i1 is `open`
    And the issue i1 conforms to the comment form
    And no request has the issue i1
    When the session s1 runs `work watch`
    Then `work` prints the issue i1
    And `work` exits successfully

  @g88 @r88
  Scenario: `work request` opens no issue when its record is not committed
    Given this repository rejects this commit
    When the person runs `work request`
    Then `work` refuses `work request`
    And `work` names this repository
    And `work` does not post an issue

  @g89 @r89
  Scenario: `work turn` posts nothing when its record is not committed
    Given this repository rejects this commit
    And a request r1
    And the request r1 is `open`
    When the person runs `work turn` on the request r1
    Then `work` refuses `work turn`
    And `work` names this repository
    And `work` does not post a comment
    And the request r1 has the issue i1
    And `work` does not close the issue i1

  @g90 @r90
  Scenario: `work fits` posts nothing when its record is not committed
    Given this repository rejects this commit
    And a request r1
    And the request r1 is `awaiting-asker`
    When the person runs `work fits` on the request r1
    Then `work` refuses `work fits`
    And `work` names this repository
    And `work` does not post a comment
    And the request r1 has the issue i1
    And `work` does not close the issue i1

  @g91 @r91
  Scenario: `work reply` refuses a request this bounded context is asked
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
  Scenario: `work sync` writes no entry of the upstream's part that the asker posted
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the comment c1 is `asker`
    And an entry e1
    And the entry e1 is `upstream`
    And the comment c1 holds the entry e1
    And the request r1 does not hold the comment c1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` does not write the entry e1

  @g96 @r96
  Scenario: `work sync` reopens no request that is `delivered`, `refused` or `withdrawn` (case 1)
    Given a request r1
    And the request r1 is `delivered`
    And a comment c1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the request r1 does not hold the comment c1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` keeps the status of the request r1
    And `work` keeps the side of the request r1

  @g96 @r96
  Scenario: `work sync` reopens no request that is `delivered`, `refused` or `withdrawn` (case 2)
    Given a request r1
    And the request r1 is `refused`
    And a comment c1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the request r1 does not hold the comment c1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` keeps the status of the request r1
    And `work` keeps the side of the request r1

  @g96 @r96
  Scenario: `work sync` reopens no request that is `delivered`, `refused` or `withdrawn` (case 3)
    Given a request r1
    And the request r1 is `withdrawn`
    And a comment c1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the request r1 does not hold the comment c1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` keeps the status of the request r1
    And `work` keeps the side of the request r1

  @g97 @r97
  Scenario: The SessionStart hook names a request awaiting the upstream that this bounded context asked
    Given a request r1
    And the request r1 originates from this bounded context
    And the request r1 does not address this bounded context
    And the request r1 is `awaiting-upstream`
    When the SessionStart hook runs `work watch` with the `--hook` option
    Then `work` prints the request r1

  @g98 @r98
  Scenario: The SessionStart hook names a request awaiting the asker that this bounded context is asked
    Given a request r1
    And the request r1 addresses this bounded context
    And the request r1 does not originate from this bounded context
    And the request r1 is `awaiting-asker`
    When the SessionStart hook runs `work watch` with the `--hook` option
    Then `work` prints the request r1

  @g99 @r99
  Scenario: The SessionStart hook is silent with no request waiting on the other side
    Given no request originates from this bounded context
    And no request addresses this bounded context
    When the SessionStart hook runs `work watch` with the `--hook` option
    Then `work` exits successfully
    And `work` does not print a request

  @g100 @r100
  Scenario: `work watch --forward` wakes on a comment that conforms to the comment form and that the request does not hold
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the request r1 does not hold the comment c1
    When the session s1 runs `work watch` with the `--forward` option
    Then `work` prints the comment c1
    And `work` exits successfully
    And `work` does not write the comment c1

  @g101 @r101
  Scenario: `work watch --forward` wakes on a new ask
    Given a GitHub repository g1
    And this bounded context has the GitHub repository g1
    And an issue i1
    And the GitHub repository g1 holds the issue i1
    And the issue i1 is `open`
    And the issue i1 conforms to the comment form
    And no request has the issue i1
    When the session s1 runs `work watch` with the `--forward` option
    Then `work` prints the issue i1
    And `work` exits successfully

  @g102 @r102
  Scenario: `work request` to an upstream refuses an observation beside a request it is raised for
    Given an upstream entry u1
    And this bounded context holds the upstream entry u1
    When the person runs `work request` with the `--source` and `--raised-for` options
    Then `work` refuses `work request`
    And `work` names the `--source` option

  @g103 @r103
  Scenario: `work sync` writes no entry of the asker's part that the upstream posted
    Given a comment c1
    And a request r1
    And the comment c1 is on the request r1
    And the comment c1 conforms to the comment form
    And the comment c1 is `upstream`
    And an entry e1
    And the entry e1 is `asker`
    And the comment c1 holds the entry e1
    And the request r1 does not hold the comment c1
    When the session s1 runs `work sync`
    Then `work` writes the comment c1
    And `work` does not write the entry e1
