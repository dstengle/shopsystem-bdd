# generated from spec/capabilities/parsing.md by features generate; do not edit
Feature: Parsing
  Narrator: the person

  @g1 @r1
  Scenario: A requirement in the language is parsed
    Given a requirement r1
    And the requirement r1 conforms to the language reference
    When the person parses the requirement r1
    Then the language service completes this request

  @g2 @r2
  Scenario: The logical form of a requirement is returned
    Given a requirement r1
    And the requirement r1 conforms to the language reference
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person parses the requirement r1 with the logical form
    Then the language service returns one logical form of the requirement r1
    And the language service completes this request

  @g3 @r3
  Scenario: A requirement outside the language is refused
    Given a requirement r1
    And the requirement r1 does not conform to the language reference
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g4 @r4
  Scenario: A requirement of two meanings is refused
    Given a logical form l1
    And a requirement r1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g5 @r5
  Scenario: A requirement that breaks a reading rule is refused
    Given a requirement r1
    And a reading rule r2
    And the requirement r1 violates the reading rule r2
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the reading rule r2

  @g6 @r6
  Scenario: A construct the construct catalogue does not define is refused
    Given a construct c1
    And the construct c1 has no catalogue entry
    And a requirement r1
    And the requirement r1 uses the construct c1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the construct c1

  @g7 @r7
  Scenario: A fragment is refused with the terms that may follow
    Given a fragment f1
    When the person parses the fragment f1
    Then the language service refuses this request
    And the language service names the fragment f1
    And the language service returns the term t1

  @g8 @r8
  Scenario: The corpus's logical form of a requirement is returned
    Given a logical form l1
    And a requirement r1
    And the requirement r1 has the logical form l1
    And this corpus holds the logical form l1
    When the person parses the requirement r1 with the logical form
    Then the language service returns the logical form l1

  @g9 @r9
  Scenario: A kept parse is returned
    Given a parse p2
    And a requirement r1
    And the requirement r1 has the parse p2
    And a parse cache p1
    And the parse cache p1 holds the parse p2
    When the person parses the requirement r1
    Then the language service returns the parse p2
    And the language service does not keep a compiled grammar
    And the language service completes this request

  @g10 @r10
  Scenario: A new parse is kept
    Given a parse p1
    And no parse cache holds the parse p1
    And a requirement r1
    And the requirement r1 has the parse p1
    When the person parses the requirement r1
    Then the language service keeps the parse cache p2
    And the language service completes this request

  @g11 @r11
  Scenario: An unchanged grammar is not compiled again
    Given a parse p1
    And no parse cache holds the parse p1
    And a requirement r1
    And the requirement r1 has the parse p1
    And a compiled grammar c1
    And the requirement r1 has the compiled grammar c1
    And the compiled grammar c1 exists
    When the person parses the requirement r1
    Then the language service does not keep a compiled grammar
    And the language service completes this request

  @g12 @r12
  Scenario: The logical form puts an order after a collection on its members
    Given a requirement r1
    And the requirement r1 uses `order-by`
    When the person parses the requirement r1 with the logical form
    Then the collection c1 has the member m1
    And the member m1 has the order o1
    And the language service returns the logical form l1
    And the logical form l1 uses the order o1
