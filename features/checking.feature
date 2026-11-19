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

  @g4 @r4
  Scenario: the check prints a violation under its rule's code
    Given a capability c1
    And the capability c1 violates `v15a`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v15a`

  @g5 @r5
  Scenario: Two requirements with one id
    Given a capability c1
    And the capability c1 violates `v15b`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v15b`

  @g6 @r6
  Scenario: A retired id used again
    Given a capability c1
    And the capability c1 violates `v15c`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v15c`

  @g7 @r7
  Scenario: A group with more than one statement
    Given a requirement group r1
    And the requirement group r1 violates `v15l`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v15l`

  @g8 @r8
  Scenario: Two groups of a capability that share their features, condition and trigger
    Given a requirement group r1
    And the requirement group r1 violates `v15n`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v15n`

  @g9 @r9
  Scenario: A given line that is not example data
    Given a requirement group r1
    And the requirement group r1 violates `v15m`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v15m`

  @g10 @r10
  Scenario: A requirement with no scenario
    Given a requirement group r1
    And the requirement group r1 violates `v_s3`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_s3`

  @g11 @r11
  Scenario: A scenario that names more than one requirement
    Given a scenario s1
    And the scenario s1 violates `v_s2`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_s2`

  @g12 @r12
  Scenario: A request with no origin
    Given a request r1
    And the request r1 violates `v17`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v17`

  @g13 @r13
  Scenario: A delivered request resolved by no requirement of the spec
    Given a request r1
    And the request r1 violates `v3`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v3`

  @g14 @r14
  Scenario: A requirement that uses an avoided word
    Given a requirement r1
    And the requirement r1 violates `v_t1`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_t1`

  @g15 @r15
  Scenario: Two glossary entries with one term
    Given a term t1
    And the term t1 violates `v_t2`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_t2`

  @g16 @r16
  Scenario: An avoided word that is a term
    Given a term t1
    And the term t1 violates `v_t3`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_t3`

  @g17 @r17
  Scenario: A requirement that does not parse
    Given a requirement r1
    And the requirement r1 violates `v_p1`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `v_p1`

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

  @g25 @r25
  Scenario: A warning leaves the exit as it is
    Given an observation o1
    And the observation o1 violates `w_uncited_obs`
    When the person validates this specification
    Then the specification service returns `w_uncited_obs`
    And the specification service completes this request

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

  @g31 @r31
  Scenario: the check refuses a condition that relates two kinds
    Given a term t1
    And the term t1 violates `v_t12`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

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

  @g34 @r34
  Scenario: the check refuses a frame that does not read
    Given a term t1
    And the term t1 violates `v_t13`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

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

  @g37 @r37
  Scenario: the check refuses a verb with no aspect
    Given a term t1
    And the term t1 violates `v_t14`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

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

  @g40 @r40
  Scenario: the check refuses two senses that overlap
    Given a term t1
    And the term t1 violates `v_t15`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

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

  @g42 @r42
  Scenario: the check refuses an import of no pack
    Given a pack p1
    And the pack p1 violates `v_t17`
    And this bounded context imports the pack p1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the pack p1

  @g43 @r43
  Scenario: the check refuses a pack's term redefined without Redefines:
    Given a term t1
    And the term t1 violates `v_t16`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

  @g44 @r44
  Scenario: the check passes a term marked Redefines:
    Given a term t1
    And a pack p1
    And the term t1 redefines the pack p1
    When the person validates this specification
    Then the specification service completes this request

  @g45 @r45
  Scenario: the check warns of example data in a line
    Given a requirement r1
    And the requirement r1 violates `w_example`
    When the person validates this specification
    Then the specification service returns the requirement r1

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
