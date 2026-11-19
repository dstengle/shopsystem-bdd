# generated from spec/capabilities/checking.md by features generate; do not edit
Feature: Checking
  Narrator: the person

  @g1 @r1
  Scenario: `model rules` prints every rule
    Given a rule r1
    And a rule r2
    When the person consults this rule catalogue
    Then the specification service returns the rule r1
    And the specification service returns the rule r2
    And the specification service completes this request

  @g2 @r2
  Scenario: `model forms` lists every file form
    Given a file form f1
    And a file form f2
    When the person inventories this specification
    Then the specification service returns the file form f1
    And the specification service returns the file form f2
    And the specification service completes this request

  @g3 @r3
  Scenario: the check exits successfully when nothing violates a rule
    Given no thing violates a rule
    When the person validates this specification
    Then the specification service returns `0 violations`
    And the specification service completes this request

  @g18 @r18
  Scenario: A request not of the form `work request` writes
    Given a request r1
    And the request r1 does not conform to the request form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the request r1

  @g19 @r19
  Scenario: A scenario that names a requirement its capability does not have
    Given a capability c1
    And a scenario s1
    And the scenario s1 has the capability c1
    And a requirement id r1
    And the capability c1 does not hold the requirement id r1
    And the scenario s1 refers to the requirement id r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the scenario s1

  @g20 @r20
  Scenario: A capability with no capability id
    Given a capability c1
    And the capability c1 does not conform to the capability id form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the capability c1

  @g21 @r21
  Scenario: A capability with no Behaviour section
    Given a capability c1
    And the capability c1 has no section
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the capability c1

  @g22 @r22
  Scenario: A feature file of no capability
    Given a feature f1
    And the feature f1 does not conform to the feature form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the feature f1

  @g23 @r23
  Scenario: A glossary bullet in no form of a term entry
    Given a term t1
    And the term t1 does not conform to the entry form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

  @g24 @r24
  Scenario: A repository not on the final layout
    Given this bounded context does not conform to the final layout
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `scripts/migrate`

  @g26 @r26
  Scenario: A context with no job has no unserved capability
    Given this bounded context has no job
    And a capability c1
    And the capability c1 violates `w_unserved_cap`
    When the person validates this specification
    Then the specification service does not return the capability c1

  @g27 @r27
  Scenario: the check tries again under an interpreter that has clingo
    Given this interpreter does not import `clingo`
    And an interpreter i1
    And the interpreter i1 imports `clingo`
    When the person validates this specification
    Then the specification service returns `0 violations`

  @g28 @r28
  Scenario: No interpreter has clingo
    Given no interpreter imports `clingo`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names this interpreter

  @g29 @r29
  Scenario: `model facts` prints the facts
    Given a fact f1
    And this bounded context has the fact f1
    And a fact f2
    And this bounded context has the fact f2
    And a fact f3
    And this bounded context does not have the fact f3
    When the person translates this specification
    Then the specification service returns the fact f1
    And the specification service returns the fact f2
    And the specification service does not return the fact f3

  @g30 @r30
  Scenario: the check refuses a verb with no frame
    Given a verb v1
    And the verb v1 has no frame
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the verb v1

  @g32 @r32
  Scenario: the check refuses a term with no part of speech
    Given a term t1
    And the term t1 has no part of speech
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

  @g33 @r33
  Scenario: the check reads a frame with a preposition
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a preposition p1
    And the frame f1 has the preposition p1
    When the person validates this specification
    Then the specification service completes this request

  @g35 @r35
  Scenario: `model rules --write` writes the rule catalogue
    When the person renews this rule catalogue
    Then the specification service keeps the rule catalogue r1
    And the specification service completes this request

  @g36 @r36
  Scenario: `model rules --check` refuses a catalogue that lacks a catalogue entry
    Given a catalogue entry c1
    And a rule catalogue r2
    And the rule catalogue r2 does not hold the catalogue entry c1
    And a rule r1
    And the rule r1 has the catalogue entry c1
    When the person renews the rule catalogue r2 with the audit
    Then the specification service fails this check
    And the specification service names the rule catalogue r2
    And the specification service does not change a file

  @g38 @r38
  Scenario: the check passes a verb with two frames
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a frame f2
    And the term t1 has the frame f2
    When the person validates this specification
    Then the specification service completes this request

  @g39 @r39
  Scenario: the check passes a verb with two senses told apart by kinds
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a sense s2
    And the term t1 has the sense s2
    When the person validates this specification
    Then the specification service completes this request

  @g41 @r41
  Scenario: `model lexicon` shows the terms of the imported packs
    Given a pack p1
    And this bounded context imports the pack p1
    And a term t1
    And the pack p1 has the term t1
    And a term t2
    And the pack p1 has the term t2
    And a term t3
    And the pack p1 does not have the term t3
    When the person looks up the pack p1
    Then the language service returns the term t1
    And the language service returns the term t2
    And the language service does not return the term t3
    And the language service completes this request

  @g44 @r44
  Scenario: the check passes a term marked Redefines:
    Given a term t1
    And a pack p1
    And the term t1 redefines the pack p1
    When the person validates this specification
    Then the specification service completes this request

  @g46 @r46
  Scenario: the check refuses a capability in the old language, naming `migrate upgrade`
    Given a capability c1
    And the language of the capability c1 is `codified-1`
    When the person validates this specification with the capability c1
    Then the specification service refuses this request
    And the specification service names the capability c1

  @g47 @r47
  Scenario: `model forms --check` refuses a file form written by hand
    Given a file form f1
    And the writer of the file form f1 is `hand`
    When the person inventories this specification with the audit
    Then the specification service fails this check
    And the specification service names the file form f1

  @g48 @r48
  Scenario: Each operation of an adapter contract is given the requirements that govern it
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the requirement r1 governs the operation o1
    And an operation o2
    And an adapter contract a2
    When the person annotates the adapter contract a1
    Then the operation o2 holds the requirement r1
    And the specification service keeps the adapter contract a2
    And the adapter contract a2 holds the operation o2
    And the specification service completes this request

  @g49 @r49
  Scenario: An operation missing a requirement that governs it fails the check
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the requirement r1 governs the operation o1
    And the operation o1 does not hold the requirement r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the operation o1
    And the specification service names the requirement r1

  @g50 @r50
  Scenario: An operation holding a requirement that no longer governs it fails the check
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the operation o1 holds the requirement r1
    And the requirement r1 does not govern the operation o1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the operation o1
    And the specification service names the requirement r1

  @g51 @r51
  Scenario: A stale adapter contract fails the audit
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the requirement r1 governs the operation o1
    And the operation o1 does not hold the requirement r1
    When the person annotates the adapter contract a1 with the audit
    Then the specification service fails this check
    And the specification service names the adapter contract a1
    And the specification service does not change a file

  @g52 @r52
  Scenario: A violation of a rule fails the check under the rule's code
    Given a rule r1
    And the severity of the rule r1 is `error`
    And a capability c1
    And the capability c1 violates the rule r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the rule r1

  @g53 @r53
  Scenario: A warning is named and the check passes
    Given a rule r1
    And the severity of the rule r1 is `warning`
    And a capability c1
    And the capability c1 violates the rule r1
    And no rule whose severity is `error` exists
    When the person validates this specification
    Then the specification service names the rule r1
    And the specification service completes this request

  @g54 @r54
  Scenario: A requirement that uses a rule the rule catalogue does not define fails the check
    Given a rule r2
    And the rule r2 has no catalogue entry
    And a requirement r1
    And the requirement r1 uses the rule r2
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the rule r2

  @g55 @r55
  Scenario: A catalogue entry with no purpose fails the check
    Given a catalogue entry c1
    And the catalogue entry c1 has no purpose
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the catalogue entry c1

  @g56 @r56
  Scenario: A catalogue entry that names no item fails the check
    Given a catalogue entry c1
    And the catalogue entry c1 mentions no item
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the catalogue entry c1

  @g57 @r57
  Scenario: A catalogue entry that names an undelivered item fails the check
    Given an item i1
    And the status of the item i1 is not `delivered`
    And a catalogue entry c1
    And the catalogue entry c1 mentions the item i1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the catalogue entry c1
    And the specification service names the item i1
