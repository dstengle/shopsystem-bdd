# generated from spec/capabilities/consistency.md by features generate; do not edit
Feature: Consistency
  Narrator: the person

  @g1 @r1
  Scenario: `model explain` prints a requirement
    Given a requirement r1
    When the person explains the requirement r1
    Then the language service returns the requirement r1
    And the language service completes this request

  @g2 @r2
  Scenario: A pair that cannot be unified leaves the clash of two other requirements
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a code c2
    And the specification service does not unify the code c2
    And the requirement r1 uses the code c2
    And a requirement r2
    And the capability c1 has the requirement r2
    And the requirement r2 uses the code c2
    And a requirement r3
    And the capability c1 has the requirement r3
    And a requirement r4
    And the capability c1 has the requirement r4
    And an act a1
    And the requirement r4 forbids the act a1
    And the requirement r3 obliges the act a1
    When the person examines this specification
    Then the specification service returns the requirement r5
    And the specification service returns `L1`

  @g3 @r3
  Scenario: `model logic` finds no clash between only and a change of that kind
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `only`
    And a requirement r2
    And the capability c1 has the requirement r2
    And an act a1
    And the requirement r2 obliges the act a1
    And the requirement r1 allows the act a1
    When the person examines this specification
    Then the specification service completes this request

  @g4 @r4
  Scenario: `model logic` finds the clash of every and a forbidden print
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `every`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t1
    And the requirement r1 has the trigger t1
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g5 @r5
  Scenario: `model logic` reads an If line as taking precedence over a When line
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement r2
    And the capability c1 has the requirement r2
    And the requirement r1 overrides the requirement r2
    When the person examines this specification
    Then the specification service completes this request

  @g6 @r6
  Scenario: `model logic` pairs a universal condition with the lines it bears on
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an act a1
    And the requirement r1 obliges the act a1
    And a universal condition u1
    And the universal condition u1 forbids the act a1
    When the person examines this specification
    Then the specification service returns the universal condition u1

  @g7 @r7
  Scenario: `model logic` reports a requirement that other requirements entail
    Given a consequence c1
    And a requirement r1
    And the requirement r1 has the consequence c1
    And the requirement r1 adds no consequence
    When the person examines this specification
    Then the specification service returns `L8`

  @g8 @r8
  Scenario: `model logic` finds two counts that cannot both hold
    Given a count c2
    And a count c3
    And the count c2 contradicts the count c3
    And a capability c1
    And the capability c1 holds the count c2
    When the person examines this specification
    Then the specification service returns `L1`

  @g9 @r9
  Scenario: `model logic` finds a line that forbids what another permits
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement r2
    And the capability c1 has the requirement r2
    And an act a1
    And the requirement r2 permits the act a1
    And the requirement r1 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L7`

  @g10 @r10
  Scenario: `model logic` checks a capability in the new language
    Given a capability c1
    And the language of the capability c1 is `codified-2`
    When the person examines this specification
    Then the specification service completes this request

  @g11 @r11
  Scenario: `model explain` prints what a refusal entails and where it comes from
    Given a requirement r1
    And a refusal r2
    And the requirement r1 uses the refusal r2
    When the person explains the requirement r1
    Then the language service returns the universal condition u1
    And the language service returns the term t1

  @g12 @r12
  Scenario: `model explain` prints the If requirement that takes precedence
    Given a requirement r2
    And a requirement r1
    And the requirement r2 overrides the requirement r1
    When the person explains the requirement r1
    Then the language service returns the requirement r3
    And the requirement r3 uses the refusal r4

  @g13 @r13
  Scenario: `model explain` refuses an id that no capability holds
    Given a requirement id r1
    And no capability holds the requirement id r1
    When the person explains the requirement id r1
    Then the language service refuses this request
    And the language service names the requirement id r1

  @g14 @r14
  Scenario: `model logic` translates every requirement that conforms to the language reference
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 conforms to the language reference
    And a translation t1
    And the requirement r1 has the translation t1
    When the person examines this specification with the capability c1
    Then the specification service returns the translation t1

  @g15 @r15
  Scenario: `model logic` translates only over a relation in a response
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `only`
    And the requirement r1 uses `holds-relation`
    And a translation t1
    And the requirement r1 has the translation t1
    When the person examines this specification with the capability c1
    Then the specification service returns the translation t1

  @g16 @r16
  Scenario: `model logic` translates a count over a relation in a response
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `count`
    And the requirement r1 uses `holds-relation`
    And a translation t1
    And the requirement r1 has the translation t1
    When the person examines this specification with the capability c1
    Then the specification service returns the translation t1

  @g17 @r17
  Scenario: `model logic` names a requirement it has no translation of
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 has no translation
    When the person examines this specification with the capability c1
    Then the specification service returns the requirement r1
    And the specification service does not return `no findings`

  @g18 @r18
  Scenario: `model logic` reads `holds-exactly` as every and only
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t1
    And the requirement r1 has the trigger t1
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g19 @r19
  Scenario: `model logic` reads `is-in` as `holds-relation`
    Given a requirement r1
    And the requirement r1 uses `is-in`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    And the requirement r2 uses `holds-relation`
    When the person examines this specification
    Then the specification service returns `L1`

  @g20 @r20
  Scenario: `model logic` finds the clash of two lines under one comparison
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `value-compare`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t1
    And the requirement r1 has the trigger t1
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g21 @r21
  Scenario: `model logic` finds no clash between two lines whose comparisons contradict
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement r2
    And the capability c1 has the requirement r2
    And an act a1
    And the requirement r2 forbids the act a1
    And the requirement r1 obliges the act a1
    And a precondition p1
    And the requirement r2 has the precondition p1
    And a comparison c2
    And the precondition p1 has the comparison c2
    And a comparison c3
    And the comparison c2 contradicts the comparison c3
    When the person examines this specification
    Then the specification service completes this request

  @g22 @r22
  Scenario: `model logic` finds two contradicting orders
    Given an order o1
    And an order o2
    And the order o1 contradicts the order o2
    And a capability c1
    And the capability c1 holds the order o1
    When the person examines this specification
    Then the specification service returns `L1`

  @g23 @r23
  Scenario: `model logic` finds the clash of two lines under a comparison of two senses of one term
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a value order v1
    And the sense s1 has the value order v1
    And a sense s2
    And the term t1 has the sense s2
    And the sense s2 has the value order v1
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `value-compare`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t2
    And the requirement r1 has the trigger t2
    And the requirement r2 has the trigger t2
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g24 @r24
  Scenario: `model logic` reads `holds-exactly` whose restriction is a relative clause
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    And the requirement r1 uses `rc-object`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t1
    And the requirement r1 has the trigger t1
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g25 @r25
  Scenario: `model logic` reads `nothing` on a response's object
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `nothing`
    And the requirement r1 uses `rc-subject`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t1
    And the requirement r1 has the trigger t1
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g26 @r26
  Scenario: `model logic` translates every over a negated value in a precondition
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `every`
    And the precondition p1 uses `not-condition`
    And a translation t1
    And the requirement r1 has the translation t1
    When the person examines this specification with the capability c1
    Then the specification service returns the translation t1

  @g27 @r27
  Scenario: `model logic` finds no clash between an object that holds nothing and a forbidden object that holds a thing
    Given a requirement r1
    And the requirement r1 uses `nothing`
    And the requirement r1 uses `rc-subject`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    And the requirement r2 uses `holds-relation`
    When the person examines this specification
    Then the specification service completes this request

  @g28 @r28
  Scenario: `model logic` finds no clash between an object that holds no thing of a kind and a forbidden object that holds one
    Given a requirement r1
    And the requirement r1 uses `no-noun`
    And the requirement r1 uses `holds-relation`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    And the requirement r2 uses `holds-relation`
    When the person examines this specification
    Then the specification service completes this request

  @g29 @r29
  Scenario: `model logic` finds the clash of two objects that hold a thing
    Given a requirement r1
    And the requirement r1 uses `holds-relation`
    And the requirement r1 uses `rc-subject`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    And the requirement r2 uses `holds-relation`
    When the person examines this specification
    Then the specification service returns `L1`

  @g30 @r30
  Scenario: `model logic` reads `holds-exactly` whose restriction reaches a second thing
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    And the requirement r1 uses `of-relation`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the capability c1 has the requirement r2
    And a trigger t1
    And the requirement r1 has the trigger t1
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g31 @r31
  Scenario: `model logic` finds the clash of a forbidden object whose value is not one code with an obliged object of another value
    Given a requirement r1
    And the requirement r1 uses `not-relative`
    And a code c1
    And the requirement r1 uses the code c1
    And an act a1
    And the requirement r1 forbids the act a1
    And a requirement r2
    And the requirement r2 obliges the act a1
    And the requirement r2 uses `rc-whose`
    And the requirement r2 does not use the code c1
    When the person examines this specification
    Then the specification service returns `L1`

  @g32 @r32
  Scenario: `model logic` finds no clash of a forbidden object whose value is not one code with an obliged object of that value
    Given a requirement r1
    And the requirement r1 uses `not-relative`
    And a code c1
    And the requirement r1 uses the code c1
    And an act a1
    And the requirement r1 forbids the act a1
    And a requirement r2
    And the requirement r2 obliges the act a1
    And the requirement r2 uses `rc-whose`
    And the requirement r2 uses the code c1
    When the person examines this specification
    Then the specification service completes this request

  @g33 @r33
  Scenario: holds-exactly in a precondition
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `holds-exactly`
    And the precondition p1 uses `rc-subject`
    And a translation t1
    And the requirement r1 has the translation t1
    When the person examines this specification with the capability c1
    Then the specification service returns the translation t1

  @g34 @r34
  Scenario: `spec logic` reads a value in use and a code of the same value as one request
    Given a requirement r1
    And the requirement r1 uses `param-of`
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    And a trigger t1
    And the requirement r2 has the trigger t1
    When the person examines this specification
    Then the specification service returns `L1`

  @g35 @r35
  Scenario: Lines on two terms of one element clash as lines on one thing
    Given a term t1
    And an element e1
    And the term t1 means the element e1
    And a requirement r1
    And the requirement r1 uses the term t1
    And an act a1
    And the requirement r1 obliges the act a1
    And a term t2
    And the term t2 means the element e1
    And a requirement r2
    And the requirement r2 uses the term t2
    And the requirement r2 forbids the act a1
    When the person examines this specification
    Then the specification service returns `L1`

  @g36 @r36
  Scenario: spec logic translates a response that makes a request
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `response-request`
    And a translation t1
    And the requirement r1 has the translation t1
    When the person examines this specification with the capability c1
    Then the specification service returns the translation t1

  @g37 @r37
  Scenario: spec logic follows a response's request to the line that governs its operation
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And the requirement r1 uses `response-request`
    And an operation o1
    And the requirement r1 uses the operation o1
    And a requirement r2
    And the requirement r2 governs the operation o1
    And a consequence c1
    And the requirement r2 has the consequence c1
    And a requirement r3
    And the requirement r3 has the consequence c1
    And the requirement r3 has the trigger t1
    And a requirement r4
    And the requirement r4 governs the operation o1
    And a requirement r5
    And the requirement r5 governs the operation o1
    And a requirement r6
    And the requirement r6 does not govern the operation o1
    When the person examines this specification
    Then the specification service returns `L8`
    And the specification service returns the requirement r4
    And the specification service returns the requirement r5
    And the specification service does not return the requirement r6

  @g38 @r38
  Scenario: spec logic follows the consequence of a governing line to the line triggered on it
    Given a requirement r1
    And an operation o1
    And the requirement r1 governs the operation o1
    And a consequence c1
    And the requirement r1 has the consequence c1
    And a trigger t1
    And a requirement r2
    And the requirement r2 has the trigger t1
    And the trigger t1 uses the consequence c1
    And a consequence c2
    And the requirement r2 has the consequence c2
    And a requirement r3
    And the requirement r3 uses `response-request`
    And the requirement r3 uses the operation o1
    And a trigger t2
    And the requirement r3 has the trigger t2
    And a requirement r4
    And the requirement r4 has the consequence c2
    And the requirement r4 has the trigger t2
    When the person examines this specification
    Then the specification service returns `L8`

  @g39 @r39
  Scenario: spec logic reads a response's request with its parameters
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And an act a1
    And the requirement r1 obliges the act a1
    And the requirement r1 uses `response-request`
    And a code c1
    And the requirement r1 uses the code c1
    And a requirement r2
    And the requirement r2 has the trigger t1
    And the requirement r2 forbids the act a1
    And the requirement r2 does not use the code c1
    When the person examines this specification
    Then the specification service completes this request
