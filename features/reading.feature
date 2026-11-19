# generated from spec/capabilities/reading.md by features generate; do not edit
Feature: Reading
  Narrator: the person

  @g1 @r1
  Scenario: `model parse` refuses a verb with no object
    Given an object o1
    And a term t1
    And the term t1 has the object o1
    And a requirement r1
    And the requirement r1 omits the object o1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g2 @r2
  Scenario: `model parse` refuses a verb with no recipient
    Given a recipient r2
    And a term t1
    And the term t1 has the recipient r2
    And a requirement r1
    And the requirement r1 omits the recipient r2
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g3 @r3
  Scenario: `model parse` parses a negated verb or relation
    Given a requirement r1
    And the requirement r1 uses `not-condition`
    When the person parses the requirement r1
    Then the language service completes this request

  @g4 @r4
  Scenario: `model parse` refuses a verb with a noun of the wrong kind
    Given a noun phrase n1
    And a term t1
    And the term t1 has the noun phrase n1
    And no frame takes the noun phrase n1
    And a requirement r1
    And the requirement r1 uses the noun phrase n1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g5 @r5
  Scenario: `model parse` parses a verb between two kinds in a condition
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a term t1
    And the aspect of the term t1 is `state`
    And the precondition p1 uses the term t1
    When the person parses the requirement r1
    Then the language service completes this request

  @g6 @r6
  Scenario: `model parse` refuses a passive with no agent
    Given a passive form p1
    And the passive form p1 has no by-phrase
    And a requirement r1
    And the requirement r1 uses the passive form p1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the passive form p1

  @g7 @r7
  Scenario: `model parse` parses a trigger with a recipient
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And a recipient r2
    And the trigger t1 uses the recipient r2
    When the person parses the requirement r1
    Then the language service completes this request

  @g8 @r8
  Scenario: `model parse` parses a verb whose frame has a preposition
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a preposition p1
    And the frame f1 has the preposition p1
    And a requirement r1
    And the requirement r1 uses the term t1
    When the person parses the requirement r1
    Then the language service completes this request

  @g9 @r9
  Scenario: `model parse` passes a plural subject whose verb agrees
    Given a requirement r1
    And the requirement r1 uses `bare-plural`
    When the person parses the requirement r1
    Then the language service completes this request

  @g10 @r10
  Scenario: `model parse` refuses a verb that does not agree with its subject
    Given a subject s1
    And a term t1
    And the term t1 has the subject s1
    And the term t1 does not agree with the subject s1
    And a requirement r1
    And the requirement r1 uses the term t1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g11 @r11
  Scenario: `model parse` refuses an action verb in a While clause
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a term t1
    And the aspect of the term t1 is `action`
    And the precondition p1 uses the term t1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g12 @r12
  Scenario: `model parse` passes a trigger that runs a command with an option
    Given a requirement r1
    And the requirement r1 uses `request-params`
    When the person parses the requirement r1
    Then the language service completes this request

  @g13 @r13
  Scenario: `model parse` passes of and its over a relation row or an attribute
    Given a requirement r1
    And the requirement r1 uses `of-relation`
    When the person parses the requirement r1
    Then the language service completes this request

  @g14 @r14
  Scenario: `model parse` passes no before a subject or an object
    Given a requirement r1
    And the requirement r1 uses `no-noun`
    When the person parses the requirement r1
    Then the language service completes this request

  @g15 @r15
  Scenario: `model parse` passes a derived compound noun
    Given a requirement r1
    And the requirement r1 uses `compound`
    When the person parses the requirement r1
    Then the language service completes this request

  @g16 @r16
  Scenario: `model parse` passes only before an object
    Given a requirement r1
    And the requirement r1 uses `only`
    When the person parses the requirement r1
    Then the language service completes this request

  @g17 @r17
  Scenario: `model parse` passes a relative clause on a verb's frame
    Given a requirement r1
    And the requirement r1 uses `rc-object`
    When the person parses the requirement r1
    Then the language service completes this request

  @g18 @r18
  Scenario: `model parse` passes whose over a relation row or an attribute
    Given a requirement r1
    And the requirement r1 uses `rc-whose`
    When the person parses the requirement r1
    Then the language service completes this request

  @g19 @r19
  Scenario: `model parse` refuses a requirement with two meanings
    Given a logical form l1
    And a requirement r1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g20 @r20
  Scenario: `model parse --form` prints the one logical form of a requirement that conforms to the language reference
    Given a requirement r1
    And the requirement r1 conforms to the language reference
    And a logical form l1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person parses the requirement r1 with the logical form
    Then the language service returns one logical form of the requirement r1
    And the language service completes this request

  @g21 @r21
  Scenario: `model parse` passes this before a kind whose entry has This:
    Given a requirement r1
    And the requirement r1 uses `this`
    When the person parses the requirement r1
    Then the language service completes this request

  @g22 @r22
  Scenario: `model parse` refuses the with no antecedent
    Given a definite noun phrase d1
    And the definite noun phrase d1 has no antecedent
    And a requirement r1
    And the requirement r1 uses the definite noun phrase d1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the definite noun phrase d1

  @g23 @r23
  Scenario: `model parse` refuses a negated indefinite in a While clause
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a negated indefinite n1
    And the precondition p1 uses the negated indefinite n1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the negated indefinite n1

  @g24 @r24
  Scenario: `model parse` refuses a requirement with no trigger and neither always nor never
    Given a requirement r1
    And the requirement r1 has no trigger
    And the requirement r1 does not use `always-never`
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g25 @r25
  Scenario: `model parse` refuses a fragment with the terms that may follow
    Given a fragment f1
    When the person parses the fragment f1
    Then the language service refuses this request
    And the language service names the fragment f1
    And the language service returns the term t1

  @g26 @r26
  Scenario: `model parse` reads a count
    Given a requirement r1
    And the requirement r1 uses `count`
    When the person parses the requirement r1
    Then the language service completes this request

  @g27 @r27
  Scenario: `model parse` reads a comparison of moments
    Given a requirement r1
    And the requirement r1 uses `moment-compare`
    When the person parses the requirement r1
    Then the language service completes this request

  @g28 @r28
  Scenario: `model parse` reads the clock as a trigger
    Given a requirement r1
    And a clock trigger c1
    And the requirement r1 uses the clock trigger c1
    When the person parses the requirement r1
    Then the language service completes this request

  @g29 @r29
  Scenario: `model parse` reads the perfect as history
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a perfect p2
    And the precondition p1 uses the perfect p2
    When the person parses the requirement r1
    Then the language service completes this request

  @g30 @r30
  Scenario: `model parse` refuses a duration with no unit
    Given a number n1
    And the number n1 has no unit
    And a requirement r1
    And the requirement r1 uses the number n1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g31 @r31
  Scenario: `model parse` reads a permission
    Given a requirement r1
    And the requirement r1 uses `may`
    When the person parses the requirement r1
    Then the language service completes this request

  @g32 @r32
  Scenario: `model parse` reads always and never with no trigger
    Given a requirement r1
    And the requirement r1 uses `always-never`
    When the person parses the requirement r1
    Then the language service completes this request

  @g33 @r33
  Scenario: `model parse` refuses a requirement that does not conform to the language reference
    Given a requirement r1
    And the requirement r1 does not conform to the language reference
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g34 @r34
  Scenario: `model parse --form` prints the logical form the corpus holds
    Given a logical form l1
    And a requirement r1
    And the requirement r1 has the logical form l1
    And this corpus holds the logical form l1
    When the person parses the requirement r1 with the logical form
    Then the language service returns the logical form l1

  @g35 @r35
  Scenario: `model parse` reads a requirement from the parse cache that holds its parse
    Given a parse p2
    And a requirement r1
    And the requirement r1 has the parse p2
    And a parse cache p1
    And the parse cache p1 holds the parse p2
    When the person parses the requirement r1
    Then the language service returns the parse p2
    And the language service does not keep a compiled grammar
    And the language service completes this request

  @g36 @r36
  Scenario: `model parse` parses a requirement whose parse no parse cache holds and keeps it
    Given a parse p1
    And no parse cache holds the parse p1
    And a requirement r1
    And the requirement r1 has the parse p1
    When the person parses the requirement r1
    Then the language service keeps the parse cache p2
    And the language service completes this request

  @g37 @r37
  Scenario: `model parse` reuses the compiled grammar of unchanged sources
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

  @g38 @r38
  Scenario: `model parse` refuses a state verb in a trigger
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And a term t2
    And the aspect of the term t2 is `state`
    And the trigger t1 uses the term t2
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the requirement r1

  @g39 @r39
  Scenario: `model parse` reads `holds-exactly`
    Given a requirement r1
    And the requirement r1 uses `holds-exactly`
    When the person parses the requirement r1
    Then the language service completes this request

  @g40 @r40
  Scenario: `model parse` reads `nothing` in a precondition
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `nothing`
    When the person parses the requirement r1
    Then the language service completes this request

  @g41 @r41
  Scenario: `model parse` reads `is-in`
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `is-in`
    When the person parses the requirement r1
    Then the language service completes this request

  @g42 @r42
  Scenario: `model parse` reads one thing's value compared with another's
    Given a requirement r1
    And the requirement r1 uses `value-compare`
    When the person parses the requirement r1
    Then the language service completes this request

  @g43 @r43
  Scenario: `model parse` reads one thing's value said to be the same as another's
    Given a requirement r1
    And the requirement r1 uses `value-same`
    When the person parses the requirement r1
    Then the language service completes this request

  @g44 @r44
  Scenario: `model parse` refuses a comparison of an attribute that has no order
    Given a term t1
    And the term t1 has no value order
    And a requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `value-compare`
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g45 @r45
  Scenario: `model parse` reads an order on a collection
    Given a requirement r1
    And the requirement r1 uses `order-by`
    When the person parses the requirement r1
    Then the language service completes this request

  @g46 @r46
  Scenario: `model parse` reads an order on a printed every
    Given a requirement r1
    And the requirement r1 uses `order-by-every`
    When the person parses the requirement r1
    Then the language service completes this request

  @g47 @r47
  Scenario: `model parse --form` prints an order as one atom
    Given a requirement r1
    And an order o1
    And the requirement r1 uses the order o1
    When the person parses the requirement r1 with the logical form
    Then the language service returns the order o1
    And the language service completes this request

  @g48 @r48
  Scenario: `model parse` refuses an order on an attribute whose values have no order
    Given a term t1
    And the term t1 has no value order
    And an order o1
    And the order o1 is on the term t1
    And a requirement r1
    And the requirement r1 uses the order o1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g49 @r49
  Scenario: `model parse` refuses an order in a precondition
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And an order o1
    And the precondition p1 uses the order o1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the order o1

  @g50 @r50
  Scenario: `model parse` refuses an order in a trigger
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And an order o1
    And the trigger t1 uses the order o1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the order o1

  @g51 @r51
  Scenario: `model parse` refuses an order in a forbidden act
    Given an order o1
    And an act a1
    And the act a1 holds the order o1
    And a requirement r1
    And the requirement r1 forbids the act a1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the order o1

  @g52 @r52
  Scenario: `model parse` reads a comparison of two senses of one term with one value order
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a value order v1
    And the sense s1 has the value order v1
    And a sense s2
    And the term t1 has the sense s2
    And the sense s2 has the value order v1
    And a requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `value-compare`
    When the person parses the requirement r1
    Then the language service completes this request

  @g53 @r53
  Scenario: `model parse` reads two senses of one term with one value order said to be the same
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a value order v1
    And the sense s1 has the value order v1
    And a sense s2
    And the term t1 has the sense s2
    And the sense s2 has the value order v1
    And a requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `value-same`
    When the person parses the requirement r1
    Then the language service completes this request

  @g54 @r54
  Scenario: `model parse` refuses a comparison of two senses of one term with different value orders
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a value order v1
    And the sense s1 has the value order v1
    And a sense s2
    And the term t1 has the sense s2
    And a value order v2
    And the sense s2 has the value order v2
    And a requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `value-compare`
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g55 @r55
  Scenario: `model parse` refuses two senses of one term with different value orders said to be the same
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a value order v1
    And the sense s1 has the value order v1
    And a sense s2
    And the term t1 has the sense s2
    And a value order v2
    And the sense s2 has the value order v2
    And a requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `value-same`
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1

  @g56 @r56
  Scenario: `model parse` reads an order on every K that a verb whose frames name its kind takes
    Given a requirement r1
    And the requirement r1 uses `order-by-every`
    And no frame takes `thing`
    And a verb v1
    And the requirement r1 uses the verb v1
    When the person parses the requirement r1
    Then the language service completes this request

  @g57 @r57
  Scenario: `model parse` reads an order after every K in a collection one way
    Given a requirement r1
    And the requirement r1 uses `order-by-every`
    And the requirement r1 uses `of-relation`
    When the person parses the requirement r1
    Then the language service completes this request

  @g58 @r58
  Scenario: `model parse` refuses a state verb in a response as the response's
    Given a response r2
    And a requirement r1
    And the requirement r1 has the response r2
    And a term t1
    And the aspect of the term t1 is `state`
    And the response r2 uses the term t1
    When the person parses the requirement r1
    Then the language service refuses this request
    And the language service names the term t1
    And the language service names the response r2
    And the language service does not name the trigger t2
    And the requirement r1 has the trigger t2

  @g59 @r59
  Scenario: `model parse` reads an order that a closing comma ends before the recipient
    Given a requirement r1
    And the requirement r1 uses `order-by`
    And a closing comma c1
    And the requirement r1 uses the closing comma c1
    When the person parses the requirement r1
    Then the language service completes this request

  @g60 @r60
  Scenario: `model parse` reads an order on every K that a closing comma ends before the recipient
    Given a requirement r1
    And the requirement r1 uses `order-by-every`
    And a closing comma c1
    And the requirement r1 uses the closing comma c1
    When the person parses the requirement r1
    Then the language service completes this request

  @g61 @r61
  Scenario: `model parse` still reads an order before the recipient with no closing comma
    Given a requirement r1
    And the requirement r1 uses `order-by`
    And a recipient r2
    And the requirement r1 uses the recipient r2
    And the requirement r1 uses no closing comma
    When the person parses the requirement r1
    Then the language service completes this request
