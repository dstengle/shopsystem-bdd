# generated from spec/capabilities/request-watch.md by features generate; do not edit
Feature: Request watch
  Narrator: a session

  @g1 @r1
  Scenario: A watch tells of an entry not held
    Given an entry e1
    And a context request c1
    And the entry e1 is on the context request c1
    And the entry e1 conforms to the entry form
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 watches this bounded context
    Then the context requests service notifies the session s1 of the entry e1
    And the context requests service completes this request
    And the context requests service does not keep the entry e1

  @g2 @r2
  Scenario: A watch tells of an open thread that no context request has
    Given a channel c1
    And this bounded context has the channel c1
    And a thread t1
    And the thread t1 is on the channel c1
    And the status of the thread t1 is `open`
    And the thread t1 conforms to the entry form
    And no context request has the thread t1
    And a session s1
    When the session s1 watches this bounded context
    Then the context requests service notifies the session s1 of the thread t1
    And the context requests service completes this request

  @g3 @r3
  Scenario: A session that starts is told of a context request awaiting its upstream
    Given a context request c1
    And the context request c1 originates from this bounded context
    And the context request c1 does not address this bounded context
    And the status of the context request c1 is `awaiting-upstream`
    And a session s1
    When the session s1 starts
    Then the context requests service notifies the session s1 of the context request c1

  @g4 @r4
  Scenario: A session that starts is told of a context request awaiting this bounded context's asker
    Given a context request c1
    And the context request c1 addresses this bounded context
    And the context request c1 does not originate from this bounded context
    And the status of the context request c1 is `awaiting-asker`
    And a session s1
    When the session s1 starts
    Then the context requests service notifies the session s1 of the context request c1

  @g5 @r5
  Scenario: A session that starts is told nothing when no context request waits
    Given no context request originates from this bounded context
    And no context request addresses this bounded context
    And a session s1
    When the session s1 starts
    Then the context requests service does not notify the session s1 of a context request

  @g6 @r6
  Scenario: An unreadable entry is told once and kept
    Given an entry e1
    And a context request c1
    And the entry e1 is on the context request c1
    And the entry e1 does not conform to the entry form
    And the context request c1 does not hold the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service notifies the session s1 of the entry e1
    And the context requests service keeps the entry e1
    And the context requests service keeps the status of the context request c1

  @g7 @r7
  Scenario: An unreadable entry held is not told again
    Given an entry e1
    And a context request c1
    And the entry e1 is on the context request c1
    And the entry e1 does not conform to the entry form
    And the context request c1 holds the entry e1
    And a session s1
    When the session s1 catches up
    Then the context requests service does not notify the session s1 of the entry e1
