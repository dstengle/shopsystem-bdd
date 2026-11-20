# generated from spec/capabilities/scenarios.md by features generate; do not edit
Feature: Scenarios
  Narrator: the person

  @g1 @r1
  Scenario: `features generate --check` names a feature with a scenario that no requirement group of its capability has
    Given the capability `shelf` holds:
      """
      ---
      id: capability/ex.com/prod/ctx/shelf
      title: shelf
      narrator: a client
      group: service
      language: codified-2
      rests_on: []
      retired: []
      ---
      # shelf
      ## Purpose
      Something.
      ## Terms
      - **book** (noun): a thing.
      ## Behaviour
      ## Not yet
      ## Dropped
      """
    And the feature file `features/shelf.feature` holds:
      """
      Feature: Shelf
        Scenario: Edited by hand
          Given a step
      """
    And a feature f1
    And a capability c1
    And the capability c1 has the feature f1
    And a scenario s1
    And no requirement group has the scenario s1
    And the feature f1 has the scenario s1
    When the person generates the feature f1 with the audit
    Then the scenarios service fails this check
    And the scenarios service names the feature f1
    And the scenarios service does not change a file

  @g2 @r2
  Scenario: `features vocab --check` names a step with no handler and its feature
    Given the capability `shelf` holds:
      """
      ---
      id: capability/ex.com/prod/ctx/shelf
      title: shelf
      narrator: a client
      group: service
      language: codified-2
      rests_on: []
      retired: []
      ---
      # shelf
      ## Purpose
      Something.
      ## Terms
      - **book** (noun): a thing.
      ## Behaviour
      ## Not yet
      ## Dropped
      """
    And the feature file `features/shelf.feature` holds:
      """
      # generated from spec/capabilities/shelf.md by features generate; do not edit
      Feature: shelf
        Narrator: a client
        @g1 @r1
        Scenario: Lending
          When the person lends a book
      """
    And a step s1
    And a feature f1
    And the feature f1 has the step s1
    And the step s1 has no handler
    When the person audits the feature f1
    Then the scenarios service fails this check
    And the scenarios service names the step s1
    And the scenarios service names the feature f1
    And the scenarios service does not change a file

  @g3 @r3
  Scenario: generation writes a scenario of every requirement group of a capability in the language reference
    Given a capability c1
    And the language of the capability c1 is `codified-2`
    And a requirement r1
    And the capability c1 has the requirement r1
    And the requirement r1 conforms to the language reference
    And a requirement r2
    And the capability c1 has the requirement r2
    And the requirement r2 uses `shall`
    And a feature f1
    And the capability c1 has the feature f1
    And a requirement group r3
    And the capability c1 has the requirement group r3
    And a requirement group r4
    And the capability c1 has the requirement group r4
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r3 has the scenario s1
    And the scenarios service keeps the scenario s2
    And the requirement group r4 has the scenario s2

  @g4 @r4
  Scenario: generation leaves out a step that a universal condition entails
    Given a capability c1
    And the language of the capability c1 is `codified-2`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And a universal condition u1
    And the universal condition u1 entails the step s1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1

  @g5 @r5
  Scenario: generation writes the feature of a codified service capability
    Given the capability `shelf` holds:
      """
      ---
      id: capability/ex.com/prod/ctx/shelf
      title: shelf
      narrator: a client
      group: service
      language: codified-2
      rests_on: []
      retired: []
      ---
      # shelf
      ## Purpose
      Something.
      ## Terms
      - **book** (noun): a thing.
      ## Behaviour
      ## Not yet
      ## Dropped
      """
    And a capability c1
    And the group of the capability c1 is `service`
    And the language of the capability c1 is `codified-2`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the feature f1
    And the scenarios service returns the feature f1

  @g6 @r6
  Scenario: generation writes what a requirement says of a referent after the act that brings it in
    Given the capability `shelf` holds:
      """
      ---
      id: capability/ex.com/prod/ctx/shelf
      title: shelf
      narrator: a client
      group: service
      language: codified-2
      rests_on: []
      retired: []
      ---
      # shelf
      ## Purpose
      Something.
      ## Terms
      - **book** (noun): a thing. Kind of: thing.
      - **status** (attribute of book): where a book is. Values (adjective): `shelved`, `lent`.
      - **lend** (verb, action): a client gives a book to a reader. Forms: lends, lent. Frame: client lends book.
      ## Behaviour
      ### [g1] Lending
      - [r1] When the person runs `shelf add`, `shelf` shall write a book whose status is `shelved` and print the book.
      ## Not yet
      ## Dropped
      """
    And a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an act a1
    And the requirement r1 has the act a1
    And a referent r2
    And the act a1 brings in the referent r2
    And a feature f1
    And the capability c1 has the feature f1
    And a description d2
    And the referent r2 has the description d2
    And the description d2 precedes the act a1
    When the person generates the feature f1
    Then the scenarios service keeps the description d1
    And the referent r2 has the description d1
    And the description d1 follows the act a1
    And the scenarios service does not keep the description d2

  @g7 @r7
  Scenario: generation writes only over a relation in a response
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `only`
    And the requirement r1 uses `holds-relation`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the scenario s1 uses `only`

  @g8 @r8
  Scenario: generation writes a count over a relation in a response
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `count`
    And the requirement r1 uses `holds-relation`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the scenario s1 uses `count`

  @g9 @r9
  Scenario: generation writes a counter-example of every
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `every`
    And a restriction r3
    And the requirement r1 has the restriction r3
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2

  @g10 @r10
  Scenario: generation writes a counter-example of only and asserts no act that only allows
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `only`
    And a restriction r3
    And the requirement r1 has the restriction r3
    And a feature f1
    And the capability c1 has the feature f1
    And a step s2
    And an act a1
    And the requirement r1 allows the act a1
    And the step s2 asserts the act a1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2
    And the scenarios service does not keep the step s2

  @g11 @r11
  Scenario: generation writes a counter-example of an upper bound
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And an upper bound u1
    And the requirement r1 has the upper bound u1
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2

  @g12 @r12
  Scenario: generation writes Givens that satisfy a precondition that uses every
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `every`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 satisfies the precondition p1

  @g13 @r13
  Scenario: generation gives a count in a precondition at its boundary
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And a count c2
    And the precondition p1 holds the count c2
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the count c2 has the boundary b1
    And the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the boundary b1

  @g15 @r15
  Scenario: generation writes the member a collection must not hold
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `not-condition`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g16 @r16
  Scenario: generation writes `nothing` in a precondition
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `nothing`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `nothing`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g17 @r17
  Scenario: generation writes an order's Then and Givens that can fail it
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And an order o1
    And the requirement r1 uses the order o1
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the scenario s1 has the order counter-example o2

  @g18 @r18
  Scenario: generation writes the scenario of `order-by` on a term of two senses
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a sense s2
    And the term t1 has the sense s2
    And a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `order-by`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s3
    And the requirement group r2 has the scenario s3
    And the scenario s3 has the order counter-example o1

  @g19 @r19
  Scenario: generation writes the scenario of `order-by-every` on a term of two senses
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a sense s2
    And the term t1 has the sense s2
    And a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses the term t1
    And the requirement r1 uses `order-by-every`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s3
    And the requirement group r2 has the scenario s3
    And the scenario s3 has the order counter-example o1

  @g20 @r20
  Scenario: generation writes the member outside a relative clause's restriction
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    And the requirement r1 uses `rc-object`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `not-condition`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g21 @r21
  Scenario: generation writes `nothing` on a response's object
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `nothing`
    And the requirement r1 uses `rc-subject`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `nothing`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g22 @r22
  Scenario: generation writes the scenario of `order-by` on the object of a verb whose frames name its kind
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `order-by`
    And no frame takes `thing`
    And a verb v1
    And the requirement r1 uses the verb v1
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the order counter-example o1

  @g23 @r23
  Scenario: generation writes the Then of a response's object that holds no K
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `no-noun`
    And the requirement r1 uses `holds-relation`
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 does not use `no-noun`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2

  @g24 @r24
  Scenario: generation satisfies every over a negated value in a precondition
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `every`
    And the precondition p1 uses `not-condition`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 satisfies the precondition p1

  @g25 @r25
  Scenario: generation writes the scenario of `order-by-every` on the object of a verb whose frames name its kind
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `order-by-every`
    And no frame takes `thing`
    And a verb v1
    And the requirement r1 uses the verb v1
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the order counter-example o1

  @g28 @r28
  Scenario: generation writes the scenario of `order-by-every` on every K in a collection
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `order-by-every`
    And the requirement r1 uses `of-relation`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the order counter-example o1

  @g29 @r29
  Scenario: generation writes a counter-example of a count over a relation in a response
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `count`
    And the requirement r1 uses `holds-relation`
    And an upper bound u1
    And the requirement r1 has the upper bound u1
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the scenario s1
    And the requirement group r2 has the scenario s1
    And the scenario s1 has the counter-example c2

  @g30 @r30
  Scenario: generation writes the member outside a restriction that reaches a second thing
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And the requirement r1 uses `holds-exactly`
    And the requirement r1 uses `of-relation`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `not-condition`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g31 @r31
  Scenario: holds-exactly in a precondition
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `holds-exactly`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `not-condition`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g32 @r32
  Scenario: holds-exactly with a subject relative clause in a precondition
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 uses `holds-exactly`
    And the precondition p1 uses `rc-subject`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the step s1 uses `not-condition`
    And the scenarios service keeps the scenario s2
    And the scenario s2 has the step s1

  @g36 @r36
  Scenario: generation gives a value in use to a given step and to the when step
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `param-of`
    And a feature f1
    And the capability c1 has the feature f1
    When the person generates the feature f1
    Then the scenarios service keeps the given step g1
    And the given step g1 mentions the code c2
    And the scenarios service keeps the when step w1
    And the when step w1 mentions the code c2

  @g37 @r37
  Scenario: generation introduces the thing an operation makes in the when step
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And an operation o1
    And a referent r3
    And the operation o1 makes the referent r3
    And the requirement r1 governs the operation o1
    And a feature f1
    And the capability c1 has the feature f1
    And a given step g1
    And the given step g1 introduces the instance i1
    When the person generates the feature f1
    Then the scenarios service keeps the when step w1
    And the scenarios service does not keep the given step g1
    And the referent r3 has the instance i1
    And the when step w1 introduces the instance i1

  @g38 @r38
  Scenario: generation introduces each instance of two Ks
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `two`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And no when step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1

  @g39 @r39
  Scenario: generation introduces the thing a printed thing holds
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `holds-relation`
    And the requirement r1 uses `rc-subject`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And no when step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1

  @g40 @r40
  Scenario: generation introduces each instance of an order
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `order-by`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And no when step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1

  @g41 @r41
  Scenario: generation introduces the thing a response names by its owner
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `of-relation`
    And a precondition p1
    And the requirement r1 has the precondition p1
    And the precondition p1 does not use `of-relation`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And no when step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1

  @g42 @r42
  Scenario: generation introduces the thing a response names by an indexical owner
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `of-relation`
    And the requirement r1 uses `this`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And no when step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1

  @g43 @r43
  Scenario: generation introduces the thing a response names by a While part's owner
    Given a requirement group r2
    And a capability c1
    And the capability c1 has the requirement group r2
    And a requirement r1
    And the requirement group r2 has the requirement r1
    And the requirement r1 uses `of-relation`
    And the requirement r1 uses `while`
    And a feature f1
    And the capability c1 has the feature f1
    And a step s1
    And an instance i1
    And no given step introduces the instance i1
    And no when step introduces the instance i1
    And the step s1 mentions the instance i1
    When the person generates the feature f1
    Then the scenarios service does not keep the step s1
