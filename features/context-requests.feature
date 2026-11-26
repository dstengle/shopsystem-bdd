# generated from spec/capabilities/context-requests.md by features generate; do not edit
Feature: Context requests
  Narrator: the person

  @g1 @r1
  Scenario: A counter-proposal passes the turn to the asker
    Given a request line r1
    And a context request c1
    And the context request c1 has the request line r1
    And a session s1
    When the session s1 settles the request line r1 with the line outcome `rewritten`
    Then the context requests service sets the line outcome of the request line r1 to `rewritten`
    And the context requests service keeps the request line r2
    And the context request c1 has the request line r2
    And the request line r2 counters the request line r1
    And the context requests service sets the side of the context request c1 to `asker`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g2 @r2
  Scenario: A refused request line keeps its reason
    Given a request line r1
    And a context request c1
    And the context request c1 has the request line r1
    And a session s1
    When the session s1 settles the request line r1 with the line outcome `refused`
    Then the context requests service sets the line outcome of the request line r1 to `refused`
    And the context requests service keeps the line reason l1
    And the request line r1 has the line reason l1
    And the context requests service keeps the context request c1

  @g3 @r3
  Scenario: A request line is not refused without a reason
    Given a session s1
    And a request line r1
    When the session s1 settles the request line r1 with the line outcome `refused` and without a line reason
    Then the context requests service refuses this request
    And the context requests service names the line reason l1
    And the request line r1 has the line reason l1

  @g4 @r4
  Scenario: A context request raised for another is kept
    Given a context request c1
    And a context request c2
    And the context request c1 is for the context request c2
    When the person raises the context request c1
    Then the context requests service keeps the context request c2

  @g5 @r5
  Scenario: A context request with neither an origin nor a thread is refused
    Given a context request c1
    When the person raises the context request c1 without an origin and a thread
    Then the context requests service refuses this request
    And the context requests service names the thread t1
    And the context request c1 has the thread t1

  @g6 @r6
  Scenario: A context request of an upstream entry with an origin and a thread is refused
    Given an upstream entry u1
    And this bounded context holds the upstream entry u1
    And a context request c1
    And a thread t1
    When the person raises the context request c1 with an origin and the thread t1
    Then the context requests service refuses this request
    And the context requests service names the origin

  @g7 @r7
  Scenario: A context request from a text that does not identify this bounded context is refused
    Given a text t1
    And the text t1 does not identify this bounded context
    And a context request c1
    When the person raises the context request c1 with the text t1
    Then the context requests service refuses this request
    And the context requests service names the text t1

  @g8 @r8
  Scenario: A request line accepted in an open context request is kept
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    When the person settles the request line r1 with the line outcome `accepted`
    Then the context requests service sets the line outcome of the request line r1 to `accepted`
    And the context requests service keeps the context request c1

  @g9 @r9
  Scenario: A request line is not settled while the context request awaits its asker
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    And a request line r1
    And the context request c1 holds the request line r1
    When the person settles the request line r1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g10 @r10
  Scenario: A request line of a context request not asked of this bounded context is not settled
    Given a context request c1
    And the status of the context request c1 is `open`
    And the context request c1 does not address this bounded context
    And a request line r1
    And the context request c1 holds the request line r1
    When the person settles the request line r1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g11 @r11
  Scenario: A question asked on an open context request is kept
    Given a context request c1
    And the status of the context request c1 is `open`
    And a question q1
    And the question q1 is on the context request c1
    When the person asks the question q1
    Then the context requests service keeps the question q1

  @g12 @r12
  Scenario: A reply to a context request this bounded context asked is kept
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    And the context request c1 originates from this bounded context
    When the person replies to the context request c1
    Then the context requests service keeps the answer a1

  @g13 @r13
  Scenario: A context request that is not accepted is not resolved
    Given a context request c1
    And the status of the context request c1 is not `accepted`
    When the person resolves the context request c1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g14 @r14
  Scenario: The context requests are given with their status and the observations no context request cites
    Given a context request c1
    And a context request c2
    And a context request c3
    And a context request c4
    And an observation o1
    And no context request cites the observation o1
    And an observation o2
    And no context request cites the observation o2
    When the person surveys this bounded context
    Then the context requests service returns the context request c1
    And the context requests service returns the context request c2
    And the context requests service returns the status of the context request c3
    And the context requests service returns the status of the context request c4
    And the context requests service returns the observation o1
    And the context requests service returns the observation o2

  @g15 @r15
  Scenario: A context request inspected gives its status and request lines
    Given a context request c1
    And a request line r1
    And the context request c1 holds the request line r1
    And a request line r2
    And the context request c1 holds the request line r2
    And a request line r3
    And the context request c1 does not hold the request line r3
    When the person inspects the context request c1
    Then the context requests service returns the status of the context request c1
    And the context requests service returns the request line r1
    And the context requests service returns the request line r2
    And the context requests service does not return the request line r3

  @g16 @r16
  Scenario: A context request raised is kept open with its thread
    Given a context request c1
    When the person raises the context request c1
    Then the context requests service keeps the context request c2
    And the status of the context request c2 is `open`
    And the context requests service keeps the thread t1
    And the context request c2 has the thread t1

  @g17 @r17
  Scenario: A context request to a bounded context with no channel is refused
    Given a bounded context b1
    And the bounded context b1 has no channel
    And a context request c1
    When the person raises the context request c1 with the bounded context b1
    Then the context requests service refuses this request
    And the context requests service names the bounded context b1

  @g18 @r18
  Scenario: An offer on an open context request awaits its asker
    Given a context request c1
    And the status of the context request c1 is `open`
    And a session s1
    When the session s1 offers on the context request c1
    Then the context requests service keeps the entry e1
    And the entry e1 is on the context request c1
    And the context requests service sets the status of the context request c1 to `awaiting-asker`

  @g20 @r20
  Scenario: Lines proposed to a context request are kept
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    When the person proposes to the context request c1
    Then the context requests service keeps the request line r1

  @g21 @r21
  Scenario: An entry not held is kept when the session catches up
    Given an entry e1
    And a context request c1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the context request c1 does not hold the entry e1
    And a session s1
    And a context request c2
    And a context request c3
    When the session s1 catches up
    Then the context requests service keeps the entry e1
    And the context requests service returns the context request c2
    And the context requests service returns the context request c3

  @g22 @r22
  Scenario: The asker's turn passed goes to the upstream
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service sets the status of the context request c1 to `awaiting-upstream`
    And the context requests service sets the side of the context request c1 to `upstream`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g23 @r23
  Scenario: The upstream's turn passed with a request line not settled goes to the asker
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is not `accepted`
    And the line outcome of the request line r1 is not `refused`
    And the line outcome of the request line r1 is not `withdrawn`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service sets the status of the context request c1 to `awaiting-asker`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g24 @r24
  Scenario: The upstream's turn passed with every request line settled and one accepted keeps the side (case 1)
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `accepted`
    And a request line r2
    And the context request c1 holds the request line r2
    And the line outcome of the request line r2 is `accepted`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service keeps the entry e1
    And the entry e1 is on the context request c1
    And the context requests service keeps the side of the context request c1

  @g24 @r24
  Scenario: The upstream's turn passed with every request line settled and one accepted keeps the side (case 2)
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `accepted`
    And a request line r2
    And the context request c1 holds the request line r2
    And the line outcome of the request line r2 is `refused`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service keeps the entry e1
    And the entry e1 is on the context request c1
    And the context requests service keeps the side of the context request c1

  @g24 @r24
  Scenario: The upstream's turn passed with every request line settled and one accepted keeps the side (case 3)
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `accepted`
    And a request line r2
    And the context request c1 holds the request line r2
    And the line outcome of the request line r2 is `withdrawn`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service keeps the entry e1
    And the entry e1 is on the context request c1
    And the context requests service keeps the side of the context request c1

  @g25 @r25
  Scenario: The upstream's turn passed with every request line refused refuses the context request
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `refused`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service sets the status of the context request c1 to `refused`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g26 @r26
  Scenario: A request line that does not conform to the requirement grammar is not accepted
    Given a requirement grammar r2
    And this bounded context has the requirement grammar r2
    And a request line r1
    And the request line r1 does not conform to the requirement grammar r2
    And a session s1
    When the session s1 settles the request line r1 with the line outcome `accepted`
    Then the context requests service refuses this request
    And the context requests service names the request line r1

  @g27 @r27
  Scenario: A context request accepted is kept as a shaped item (case 1)
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `accepted`
    And a request line r2
    And the context request c1 holds the request line r2
    And the line outcome of the request line r2 is `accepted`
    When the person accepts the context request c1
    Then the context requests service sets the status of the context request c1 to `accepted`
    And the context requests service keeps the item i1
    And the status of the item i1 is `shaped`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g27 @r27
  Scenario: A context request accepted is kept as a shaped item (case 2)
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `accepted`
    And a request line r2
    And the context request c1 holds the request line r2
    And the line outcome of the request line r2 is `refused`
    When the person accepts the context request c1
    Then the context requests service sets the status of the context request c1 to `accepted`
    And the context requests service keeps the item i1
    And the status of the item i1 is `shaped`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g27 @r27
  Scenario: A context request accepted is kept as a shaped item (case 3)
    Given a context request c1
    And the status of the context request c1 is `open`
    And a request line r1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is `accepted`
    And a request line r2
    And the context request c1 holds the request line r2
    And the line outcome of the request line r2 is `withdrawn`
    When the person accepts the context request c1
    Then the context requests service sets the status of the context request c1 to `accepted`
    And the context requests service keeps the item i1
    And the status of the item i1 is `shaped`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g28 @r28
  Scenario: A context request with a request line not settled is not accepted
    Given a request line r1
    And a context request c1
    And the context request c1 holds the request line r1
    And the line outcome of the request line r1 is not `accepted`
    And the line outcome of the request line r1 is not `refused`
    And the line outcome of the request line r1 is not `withdrawn`
    When the person accepts the context request c1
    Then the context requests service refuses this request
    And the context requests service names the request line r1

  @g30 @r30
  Scenario: No context request is raised while this repository rejects a change
    Given the store of this repository is `rejecting`
    And a context request c1
    When the person raises the context request c1
    Then the context requests service refuses this request
    And the context requests service names this repository
    And the context requests service does not keep a thread

  @g31 @r31
  Scenario: No turn is passed while this repository rejects a change
    Given the store of this repository is `rejecting`
    And a context request c1
    And the status of the context request c1 is `open`
    And a turn t1
    And the context request c1 has the turn t1
    And an entry e1
    And the entry e1 is on the context request c1
    When the person passes the turn t1
    Then the context requests service refuses this request
    And the context requests service names this repository
    And the context requests service does not keep the entry e1

  @g32 @r32
  Scenario: No context request is served while this repository rejects a change
    Given the store of this repository is `rejecting`
    And a context request c1
    And the status of the context request c1 is `awaiting-asker`
    And an entry e1
    And the entry e1 is on the context request c1
    When the person serves the context request c1
    Then the context requests service refuses this request
    And the context requests service names this repository
    And the context requests service does not keep the entry e1

  @g33 @r33
  Scenario: A context request asked of this bounded context is not replied to
    Given a context request c1
    And the context request c1 addresses this bounded context
    And the context request c1 does not originate from this bounded context
    When the person replies to the context request c1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g34 @r34
  Scenario: The asker's turn of a context request asked of this bounded context is not passed
    Given a context request c1
    And the context request c1 addresses this bounded context
    And the context request c1 does not originate from this bounded context
    And the status of the context request c1 is `awaiting-asker`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g35 @r35
  Scenario: The upstream's turn of an open context request this bounded context asked is not passed
    Given a context request c1
    And the context request c1 originates from this bounded context
    And the context request c1 does not address this bounded context
    And the status of the context request c1 is `open`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g36 @r36
  Scenario: The upstream's turn of a context request this bounded context asked is not passed
    Given a context request c1
    And the context request c1 originates from this bounded context
    And the context request c1 does not address this bounded context
    And the status of the context request c1 is `awaiting-upstream`
    And a turn t1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g37 @r37
  Scenario: An asker's entry holding an upstream's field is kept without the field
    Given an entry e1
    And a context request c1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the side of the entry e1 is `asker`
    And a field f1
    And the side of the field f1 is `upstream`
    And the entry e1 holds the field f1
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service keeps the entry e1
    And the context requests service does not keep the field f1

  @g38 @r38
  Scenario: An entry on a closed context request changes neither its status nor its side (case 1)
    Given a context request c1
    And the status of the context request c1 is `delivered`
    And an entry e1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service keeps the entry e1
    And the context requests service keeps the status of the context request c1
    And the context requests service keeps the side of the context request c1

  @g38 @r38
  Scenario: An entry on a closed context request changes neither its status nor its side (case 2)
    Given a context request c1
    And the status of the context request c1 is `refused`
    And an entry e1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service keeps the entry e1
    And the context requests service keeps the status of the context request c1
    And the context requests service keeps the side of the context request c1

  @g38 @r38
  Scenario: An entry on a closed context request changes neither its status nor its side (case 3)
    Given a context request c1
    And the status of the context request c1 is `withdrawn`
    And an entry e1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service keeps the entry e1
    And the context requests service keeps the status of the context request c1
    And the context requests service keeps the side of the context request c1

  @g39 @r39
  Scenario: A context request for another raised with an origin from an upstream entry is refused
    Given an upstream entry u1
    And this bounded context holds the upstream entry u1
    And a context request c1
    And a context request c2
    And the context request c1 is for the context request c2
    When the person raises the context request c1 with an origin
    Then the context requests service refuses this request
    And the context requests service names the origin

  @g40 @r40
  Scenario: An upstream's entry holding an asker's field is kept without the field
    Given an entry e1
    And a context request c1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the side of the entry e1 is `upstream`
    And a field f1
    And the side of the field f1 is `asker`
    And the entry e1 holds the field f1
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service keeps the entry e1
    And the context requests service does not keep the field f1

  @g41 @r41
  Scenario: A context request inspected gives the line reasons
    Given a request line r1
    And a context request c1
    And the context request c1 holds the request line r1
    And a line reason l1
    And the request line r1 has the line reason l1
    When the person inspects the context request c1
    Then the context requests service returns the line reason l1

  @g42 @r42
  Scenario: An offer gives the context request and its status
    Given a context request c1
    When the person offers on the context request c1
    Then the context requests service returns the context request c1
    And the context requests service returns the status of the context request c1

  @g43 @r43
  Scenario: A proposal gives the context request and its status
    Given a context request c1
    When the person proposes to the context request c1
    Then the context requests service returns the context request c1
    And the context requests service returns the status of the context request c1

  @g44 @r44
  Scenario: A reply gives the context request and its status
    Given a context request c1
    When the person replies to the context request c1
    Then the context requests service returns the context request c1
    And the context requests service returns the status of the context request c1

  @g45 @r45
  Scenario: A turn passed gives the context request and its status
    Given a turn t1
    And a context request c1
    And the context request c1 has the turn t1
    When the person passes the turn t1
    Then the context requests service returns the context request c1
    And the context requests service returns the status of the context request c1

  @g46 @r46
  Scenario: A context request raised with no sender originates from this bounded context
    Given a context request c1
    When the person raises the context request c1 without a text
    Then the context requests service keeps the context request c2
    And the context request c2 originates from this bounded context

  @g47 @r47
  Scenario: An offer of a capability holds every requirement of it
    Given a session s1
    And a context request c1
    And a capability c2
    And a requirement r1
    And the capability c2 has the requirement r1
    And a requirement r2
    And the capability c2 has the requirement r2
    And a requirement r3
    And the capability c2 does not have the requirement r3
    When the session s1 offers on the context request c1 with the capability c2
    Then the context requests service keeps the entry e1
    And the entry e1 holds the requirement r1
    And the entry e1 holds the requirement r2
    And the entry e1 does not hold the requirement r3

  @g48 @r48
  Scenario: An offer of a capability holds each term its requirements mention
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a term t1
    And the requirement r1 mentions the term t1
    And a session s1
    And a context request c2
    When the session s1 offers on the context request c2 with the capability c1
    Then the context requests service keeps the entry e1
    And the entry e1 holds the term t1

  @g49 @r49
  Scenario: An offer of a capability holds no given block of it
    Given a given block g1
    And a capability c1
    And the capability c1 holds the given block g1
    And a session s1
    And a context request c2
    When the session s1 offers on the context request c2 with the capability c1
    Then the context requests service keeps the entry e1
    And the entry e1 does not hold the given block g1

  @g50 @r50
  Scenario: An offer of a capability holds no term its requirements do not mention
    Given a term t1
    And this bounded context holds the term t1
    And a capability c1
    And no requirement of the capability c1 mentions the term t1
    And a session s1
    And a context request c2
    When the session s1 offers on the context request c2 with the capability c1
    Then the context requests service keeps the entry e1
    And the entry e1 does not hold the term t1

  @g51 @r51
  Scenario: A context request is not resolved while its channel rejects a change to its thread
    Given a context request c1
    And the status of the context request c1 is `accepted`
    And a channel c2
    And the availability of the channel c2 is `rejecting`
    And a thread t1
    And the thread t1 is on the channel c2
    And the context request c1 has the thread t1
    When the person resolves the context request c1
    Then the context requests service refuses this request
    And the context requests service names the thread t1

  @g52 @r52
  Scenario: A context request is not served while its channel rejects a change to its thread
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    And a channel c2
    And the availability of the channel c2 is `rejecting`
    And a thread t1
    And the thread t1 is on the channel c2
    And the context request c1 has the thread t1
    When the person serves the context request c1
    Then the context requests service refuses this request
    And the context requests service names the thread t1

  @g53 @r58
  Scenario: An accepted term proposal brings its term into the item
    Given a term proposal t1
    And the line outcome of the term proposal t1 is `accepted`
    And a context request c1
    And the context request c1 holds the term proposal t1
    And a term t2
    And the term proposal t1 concerns the term t2
    And a term t3
    And the term proposal t1 concerns the term t3
    And a term t4
    And the term proposal t1 does not concern the term t4
    When the person accepts the context request c1
    Then the context requests service keeps the item i1
    And the item i1 holds the term t2
    And the item i1 holds the term t3
    And the item i1 does not hold the term t4

  @g54 @r54
  Scenario: A request's issue is never left out of step with its record
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    When the person serves the context request c1
    Then the context requests service sets the status of the context request c1 to `delivered`
    And the context requests service keeps the resolution r1
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1
    And the context requests service sets the status of the thread t1 to `closed`
    And the context request c1 has the thread t1

  @g55 @r55
  Scenario: An accepted context request resolved is delivered and its thread closed
    Given a context request c1
    And the status of the context request c1 is `accepted`
    When the person resolves the context request c1
    Then the context requests service sets the status of the context request c1 to `delivered`
    And the context requests service keeps the resolution r1
    And the context requests service sets the side of the context request c1 to `asker`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1
    And the context requests service sets the status of the thread t1 to `closed`
    And the context request c1 has the thread t1

  @g56 @r56
  Scenario: A turn passed is posted though the channel does not provide its thread
    Given a context request c1
    And the status of the context request c1 is `awaiting-asker`
    And a thread t1
    And the context request c1 has the thread t1
    And a channel c2
    And the channel c2 does not provide the thread t1
    And a turn t2
    And the context request c1 has the turn t2
    When the person passes the turn t2
    Then the context requests service sets the status of the context request c1 to `awaiting-upstream`
    And the context requests service sets the side of the context request c1 to `upstream`
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c1

  @g57 @r57
  Scenario: A term proposal suggested is kept on its context request
    Given a term proposal t1
    And a context request c1
    When the person suggests the term proposal t1 for the context request c1
    Then the context requests service keeps the context request c2
    And the context request c2 holds the term proposal t1
    And the context requests service keeps the entry e1
    And the entry e1 is on the context request c2

  @g58 @r59
  Scenario: A term proposal out of the asker's turn is refused
    Given a context request c1
    And the status of the context request c1 is `awaiting-upstream`
    And a term proposal t1
    When the person suggests the term proposal t1 for the context request c1
    Then the context requests service refuses this request
    And the context requests service names the context request c1

  @g59 @r60
  Scenario: A term proposal out of the vocabulary-entry form is refused
    Given a term proposal t1
    And the term proposal t1 does not conform to the vocabulary-entry form
    When the person suggests the term proposal t1
    Then the context requests service refuses this request
    And the context requests service names the term proposal t1
