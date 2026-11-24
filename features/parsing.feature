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

  @g13 @r13
  Scenario: A requirement of a verb of two frames is read by one frame
    Given a frame f1
    And a verb v1
    And the verb v1 has the frame f1
    And a frame f2
    And the verb v1 has the frame f2
    And a frame f3
    And the verb v1 has the frame f3
    And a requirement r1
    And the requirement r1 uses the frame f3
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person parses the requirement r1
    Then the language service returns one logical form of the requirement r1
    And the language service completes this request

  @g14 @r14
  Scenario: A request on more than one thing is outside the language
    Given a plural object p1
    And a requirement r1
    And the requirement r1 has the plural object p1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g15 @r15
  Scenario: A requirement of two meanings is refused naming its ambiguous text
    Given a logical form l1
    And a requirement r1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1
    And the language service names the ambiguous text a1
    And the requirement r1 has the ambiguous text a1

  @g16 @r16
  Scenario: A requirement read by two frames of a verb is refused naming the two frames
    Given an ambiguous text a1
    And a requirement r1
    And the requirement r1 has the ambiguous text a1
    And a frame f1
    And a verb v1
    And the verb v1 has the frame f1
    And the ambiguous text a1 uses the frame f1
    And a frame f2
    And the verb v1 has the frame f2
    And the ambiguous text a1 uses the frame f2
    And a frame f3
    And the ambiguous text a1 uses the frame f3
    And a frame f4
    And the ambiguous text a1 uses the frame f4
    And a frame f5
    And the ambiguous text a1 does not use the frame f5
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the frame f3
    And the language service names the frame f4
    And the language service does not name the frame f5

  @g17 @r17
  Scenario: A request parameter's value that is another thing's value is parsed
    Given a requirement r1
    And the requirement r1 uses `param-of`
    When the person parses the requirement r1
    Then the language service completes this request

  @g18 @r18
  Scenario: The logical form keeps a value in use
    Given a requirement r1
    And the requirement r1 uses `param-of`
    And a value in use v1
    And a logical form l1
    When the person parses the requirement r1 with the logical form
    Then the language service returns the logical form l1
    And the logical form l1 holds the value in use v1

  @g19 @r19
  Scenario: A requirement that uses an item's term is parsed for the item
    Given a term t1
    And an item i1
    And the item i1 holds the term t1
    And a requirement r1
    And the requirement r1 uses the term t1
    When the person previews the requirement r1 for the item i1
    Then the language service completes this request

  @g20 @r20
  Scenario: The logical form of a requirement that uses an item's term is returned for the item
    Given a term t1
    And an item i1
    And the item i1 holds the term t1
    And a requirement r1
    And the requirement r1 uses the term t1
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person previews the requirement r1 for the item i1 with the logical form
    Then the language service returns one logical form of the requirement r1
    And the language service completes this request

  @g22 @r22
  Scenario: A requirement outside the language is refused for an item
    Given a requirement r1
    And the requirement r1 does not conform to the language reference
    And an item i1
    When the person previews the requirement r1 for the item i1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g23 @r23
  Scenario: A response that makes a request with its parameters is parsed
    Given a requirement r1
    And the requirement r1 uses `response-request`
    When the person parses the requirement r1
    Then the language service completes this request

  @g24 @r24
  Scenario: The logical form reads a response's request with its parameters
    Given a requirement r1
    And the requirement r1 uses `response-request`
    When the person parses the requirement r1 with the logical form
    Then the language service returns the logical form l1
    And the logical form l1 uses `request-params`
