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

  @g28 @r28
  Scenario: A request not of the form `work request` writes
    Given a request q1
    And the request q1 is misformed
    When the person runs `model check` on the request q1
    Then `model` exits with an error naming the request q1

  @g30 @r30
  Scenario: A scenario that names a requirement its capability does not have
    Given a scenario s1
    And the scenario s1 is misreferring
    When the person runs `model check` on the scenario s1
    Then `model` exits with an error naming the scenario s1

  @g36 @r36
  Scenario: A capability not named by its file
    Given a capability c1
    And the capability c1 is misnamed
    When the person runs `model check` on the capability c1
    Then `model` exits with an error naming the capability c1

  @g38 @r38
  Scenario: A feature file of no capability
    Given a feature f1
    And the feature f1 is misfiled
    When the person runs `model check` on the feature f1
    Then `model` exits with an error naming the feature f1

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

  @g54 @r54
  Scenario: `model rules` prints every rule
    When the person runs `model rules`
    Then `model` prints the rule r1
    And `model` exits successfully

  @g55 @r55
  Scenario: `model forms` lists every file form
    When the person runs `model forms`
    Then `model` prints the file form f1
    And `model` exits successfully

  @g56 @r56
  Scenario: `work record` writes and commits a record
    When the person runs `work record`
    Then `work` writes the record r1
    And `work` commits the record r1

  @g57 @r57
  Scenario: `work record` refuses an unattributed record
    Given a record r1
    And the record r1 is unattributed
    When the person runs `work record` on the record r1
    Then `work` exits with an error naming `--about`
    And `work` changes nothing

  @g58 @r58
  Scenario: `model parse` refuses a verb with no object
    Given a requirement r1
    And the requirement r1 is objectless
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g59 @r59
  Scenario: `model parse` refuses a verb with no recipient
    Given a requirement r1
    And the requirement r1 is recipientless
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g60 @r60
  Scenario: `model check` refuses a verb with no frame
    Given a term t1
    And the term t1 is frameless
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g61 @r61
  Scenario: `model check` refuses a condition that relates two kinds
    Given a term t1
    And the term t1 is relational
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g62 @r62
  Scenario: `model parse` parses a negated verb or relation
    Given a requirement r1
    And the requirement r1 is negating
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g63 @r63
  Scenario: `model parse` refuses a verb with a noun of the wrong kind
    Given a requirement r1
    And the requirement r1 is mistyped
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g64 @r64
  Scenario: `model parse` parses a verb between two kinds in a condition
    Given a requirement r1
    And the requirement r1 is verbal
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g65 @r65
  Scenario: `model parse` refuses a passive with no agent
    Given a requirement r1
    And the requirement r1 is agentless
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g66 @r66
  Scenario: `model parse` parses a trigger with a recipient
    Given a requirement r1
    And the requirement r1 is addressed
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g67 @r67
  Scenario: `model check` refuses a term with no part of speech
    Given a term t1
    And the term t1 is unlabelled
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1
