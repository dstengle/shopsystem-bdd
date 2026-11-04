# generated from spec/capabilities/design-model-check.md by features generate; do not edit
Feature: Design model check
  Narrator: a person or session verifying a repository against the design model

  @g1 @r1
  Scenario: `model check` exits successfully on a sound context
    Given a bounded context b1
    And the bounded context b1 is sound
    When the person runs `model check` on the bounded context b1
    Then `model` prints "0 violations"
    And `model` exits successfully

  @g2 @r2
  Scenario: `model check` prints a violation under its rule's code
    Given a capability c1
    And the capability c1 is unnumbered
    When the person runs `model check` on the capability c1
    Then `model` exits with an error naming `v15a`

  @g3 @r3
  Scenario: Two requirements with one id
    Given a capability c1
    And the capability c1 is renumbered
    When the person runs `model check` on the capability c1
    Then `model` exits with an error naming `v15b`

  @g4 @r4
  Scenario: A retired id used again
    Given a capability c1
    And the capability c1 is reusing
    When the person runs `model check` on the capability c1
    Then `model` exits with an error naming `v15c`

  @g5 @r5
  Scenario: A group with more than one statement
    Given a requirement group r1
    And the requirement group r1 is compound
    When the person runs `model check` on the requirement group r1
    Then `model` exits with an error naming `v15l`

  @g6 @r6
  Scenario: Two groups of a capability that share their features, condition and trigger
    Given a requirement group r1
    And the requirement group r1 is repeating
    When the person runs `model check` on the requirement group r1
    Then `model` exits with an error naming `v15n`

  @g7 @r7
  Scenario: A given line that is not example data
    Given a requirement group r1
    And the requirement group r1 is unexampled
    When the person runs `model check` on the requirement group r1
    Then `model` exits with an error naming `v15m`

  @g8 @r8
  Scenario: A proposal that changes a requirement no capability has
    Given a capability-proposal p1
    And the capability-proposal p1 is reaching
    When the person runs `model check` on the capability-proposal p1
    Then `model` exits with an error naming `v15e`

  @g9 @r9
  Scenario: A formulated proposal that leaves a requirement with no scenario
    Given a capability-proposal p1
    And the capability-proposal p1 is unformulated
    When the person runs `model check` on the capability-proposal p1
    Then `model` exits with an error naming `v15f`

  @g10 @r10
  Scenario: A requirement with no scenario
    Given a requirement r1
    And the requirement r1 is untested
    When the person runs `model check` on the requirement r1
    Then `model` exits with an error naming `v_s3`

  @g11 @r11
  Scenario: A scenario that names more than one requirement
    Given a scenario s1
    And the scenario s1 is overtagged
    When the person runs `model check` on the scenario s1
    Then `model` exits with an error naming `v_s2`

  @g12 @r12
  Scenario: A part with no part_of
    Given a work-item w1
    And the work-item w1 is parentless
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming `v9a`

  @g13 @r13
  Scenario: An initiative with more than one first part
    Given an initiative i1 that is `started`
    And the initiative i1 is crowded
    When the person runs `model check` on the initiative i1
    Then `model` exits with an error naming `v_k5`

  @g14 @r14
  Scenario: A capability-proposal that argues more than one capability
    Given a capability-proposal p1
    And the capability-proposal p1 is plural
    When the person runs `model check` on the capability-proposal p1
    Then `model` exits with an error naming `v_k6`

  @g15 @r15
  Scenario: An abandoned initiative with an open part
    Given an initiative i1 that is `abandoned`
    And a work-item w1
    And the work-item w1 is open
    When the person runs `model check`
    Then `model` exits with an error naming `v_d5`

  @g16 @r16
  Scenario: An initiative that fulfils no request
    Given an initiative i1 that is `started`
    And the initiative i1 is unrequested
    When the person runs `model check` on the initiative i1
    Then `model` exits with an error naming `v16a`

  @g17 @r17
  Scenario: A done initiative with a request of its own not delivered
    Given an initiative i1 that is `done`
    And the initiative i1 is unwaiting
    When the person runs `model check` on the initiative i1
    Then `model` exits with an error naming `v_d1`

  @g18 @r18
  Scenario: A delivered request whose initiative is not done
    Given a request q1 that is `delivered`
    And an initiative i1
    And the initiative i1 fulfils the request q1
    And the initiative i1 is `started`
    When the person runs `model check`
    Then `model` exits with an error naming `v_d3`

  @g19 @r19
  Scenario: A request with no origin
    Given a request q1
    And the request q1 is unanchored
    When the person runs `model check` on the request q1
    Then `model` exits with an error naming `v17`

  @g20 @r20
  Scenario: A delivered request resolved by no requirement of the spec
    Given a request q1
    And the request q1 is misresolved
    When the person runs `model check` on the request q1
    Then `model` exits with an error naming `v3`

  @g21 @r21
  Scenario: An id with another context's path
    Given a work-item w1
    And the work-item w1 is alien
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming `v18d`

  @g22 @r22
  Scenario: A requirement that uses an avoided word
    Given a requirement r1
    And the requirement r1 is avoiding
    When the person runs `model check` on the requirement r1
    Then `model` exits with an error naming `v_t1`

  @g23 @r23
  Scenario: Two glossary entries with one term
    Given a term t1
    And the term t1 is duplicated
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming `v_t2`

  @g24 @r24
  Scenario: An avoided word that is a term
    Given a term t1
    And the term t1 is selfavoiding
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming `v_t3`

  @g25 @r25
  Scenario: A requirement that does not parse
    Given a requirement r1
    And the requirement r1 is unparsed
    When the person runs `model check` on the requirement r1
    Then `model` exits with an error naming `v_p1`

  @g26 @r26
  Scenario: A work-item with no acceptance and no check
    Given a work-item w1
    And the work-item w1 is uncommitted
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming `v_w4`

  @g27 @r27
  Scenario: A work-item file not named by its id
    Given a work-item w1
    And the work-item w1 is misnumbered
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming the work-item w1

  @g28 @r28
  Scenario: A request not of the form `work request` writes
    Given a request q1
    And the request q1 is misformed
    When the person runs `model check` on the request q1
    Then `model` exits with an error naming the request q1

  @g29 @r29
  Scenario: An initiative of a job's kind
    Given an initiative i1 that is `started`
    And the initiative i1 is jobbed
    When the person runs `model check` on the initiative i1
    Then `model` exits with an error naming the initiative i1

  @g30 @r30
  Scenario: A scenario that names a requirement its capability does not have
    Given a scenario s1
    And the scenario s1 is misreferring
    When the person runs `model check` on the scenario s1
    Then `model` exits with an error naming the scenario s1

  @g31 @r31
  Scenario: A reference not written as a requirement id
    Given a work-item w1
    And the work-item w1 is misreferenced
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming the work-item w1

  @g32 @r32
  Scenario: A proposal that adds an id its capability does not have
    Given a capability-proposal p1
    And the capability-proposal p1 is dangling
    When the person runs `model check` on the capability-proposal p1
    Then `model` exits with an error naming the capability-proposal p1

  @g33 @r33
  Scenario: A field that names nothing
    Given a work-item w1
    And the work-item w1 is unresolving
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming the work-item w1

  @g34 @r34
  Scenario: A capability-proposal that names a term the glossary does not have
    Given a capability-proposal p1
    And the capability-proposal p1 is termless
    When the person runs `model check` on the capability-proposal p1
    Then `model` exits with an error naming the capability-proposal p1

  @g35 @r35
  Scenario: A glossary-proposal that names a term the glossary does not have
    Given a glossary-proposal p1
    And the glossary-proposal p1 is termless
    When the person runs `model check` on the glossary-proposal p1
    Then `model` exits with an error naming the glossary-proposal p1

  @g36 @r36
  Scenario: A capability not named by its file
    Given a capability c1
    And the capability c1 is misnamed
    When the person runs `model check` on the capability c1
    Then `model` exits with an error naming the capability c1

  @g37 @r37
  Scenario: A node whose id is not of its kind
    Given a work-item w1
    And the work-item w1 is misidentified
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming the work-item w1

  @g38 @r38
  Scenario: A feature file of no capability
    Given a feature f1
    And the feature f1 is misfiled
    When the person runs `model check` on the feature f1
    Then `model` exits with an error naming the feature f1

  @g39 @r39
  Scenario: A work directory with no initiative
    Given a work-item w1
    And the work-item w1 is homeless
    When the person runs `model check` on the work-item w1
    Then `model` exits with an error naming the work-item w1

  @g40 @r40
  Scenario: A decision with no id or no Decision section
    Given a design-decision d1
    And the design-decision d1 is headless
    When the person runs `model check` on the design-decision d1
    Then `model` exits with an error naming the design-decision d1

  @g41 @r41
  Scenario: A glossary bullet in no form of a term entry
    Given a term t1
    And the term t1 is malformed
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g42 @r42
  Scenario: A repository not on the final layout
    Given a bounded context b1
    And the bounded context b1 is unmigrated
    When the person runs `model check` on the bounded context b1
    Then `model` exits with an error naming `scripts/migrate`

  @g43 @r43
  Scenario: A warning leaves the exit as it is
    Given an observation o1
    And the observation o1 is uncited
    When the person runs `model check` on the observation o1
    Then `model` prints `w_uncited_obs`
    And `model` exits successfully

  @g44 @r44
  Scenario: A context with no job has no unserved capability
    When the person runs `model check`
    Then `model` does not print `w_unserved_cap`

  @g45 @r45
  Scenario: A formulated capability-proposal is closed for a done initiative
    Given an initiative i1 that is `done`
    And a capability-proposal p1
    And the capability-proposal p1 is part of the initiative i1
    And the capability-proposal p1 is `formulated`
    When the person runs `model check`
    Then `model` does not print `v_d1`

  @g46 @r46
  Scenario: An approved glossary-proposal is closed for a done initiative
    Given an initiative i1 that is `done`
    And a glossary-proposal p1
    And the glossary-proposal p1 is part of the initiative i1
    And the glossary-proposal p1 is `approved`
    When the person runs `model check`
    Then `model` does not print `v_d1`

  @g47 @r47
  Scenario: `model check` tries again under an interpreter that has clingo
    Given an interpreter i1
    And the interpreter i1 is clingoless
    When the person runs `model check`
    Then `model` prints "0 violations"

  @g48 @r48
  Scenario: No interpreter has clingo
    Given an interpreter i1
    And the interpreter i1 is unfound
    When the person runs `model check`
    Then `model` exits with an error naming "pip install clingo"

  @g49 @r49
  Scenario: `model facts` prints the facts
    When the person runs `model facts`
    Then `model` prints the fact f1

  @g50 @r50
  Scenario: `model decisions` writes the decisions index
    When the person runs `model decisions`
    Then `model` writes the decisions index d1

  @g51 @r51
  Scenario: `model decisions --check` refuses a stale index
    Given `--check` is given
    And a decisions index d1
    And the decisions index d1 is stale
    When the person runs `model decisions` on the decisions index d1
    Then `model` exits with an error naming the decisions index d1
    And `model` changes nothing

  @g52 @r52
  Scenario: `model decisions --check` passes a current index
    Given `--check` is given
    When the person runs `model decisions` on the decisions index d1
    Then `model` exits successfully

  @g53 @r53
  Scenario: `model why` traces a requirement to the proposals that add it
    Given a capability-proposal p1
    And a requirement r1
    And the capability-proposal p1 adds the requirement r1
    When the person runs `model why` on the requirement r1
    Then `model` prints the requirement r1
    And `model` prints the capability-proposal p1
    And `model` exits successfully

  @g54 @r54
  Scenario: `model rules` prints every rule
    When the person runs `model rules`
    Then `model` prints the rule r1
    And `model` exits successfully
