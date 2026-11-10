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

  @g68 @r68
  Scenario: `model check` reads a prepositional verb's frame
    Given a term t1
    And the term t1 is prepositional
    When the person runs `model check` on the term t1
    Then `model` exits successfully

  @g69 @r69
  Scenario: `model parse` parses a prepositional verb with its preposition
    Given a requirement r1
    And the requirement r1 is prepositioned
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g70 @r70
  Scenario: `model check` refuses a frame that does not read
    Given a term t1
    And the term t1 is misframed
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g71 @r71
  Scenario: A pair that cannot be unified sets only itself aside
    Given a capability c1
    And the capability c1 is unpairable
    When the person runs `model logic` on the capability c1
    Then `model` prints the requirement r1
    And `model` prints "L1"

  @g74 @r74
  Scenario: `model rules --write` writes the rule catalogue
    When the person runs `model rules --write`
    Then `model` writes the rule catalogue r1
    And `model` exits successfully

  @g75 @r75
  Scenario: `model rules --check` refuses a stale rule catalogue
    Given a rule catalogue r1
    And the rule catalogue r1 is stale
    When the person runs `model rules --check` on the rule catalogue r1
    Then `model` exits with an error naming the rule catalogue r1
    And `model` changes nothing

  @g76 @r76
  Scenario: `model check` refuses a verb with no aspect
    Given a term t1
    And the term t1 is aspectless
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g77 @r77
  Scenario: `model check` passes a verb with two frames
    Given a term t1
    And the term t1 is multiframed
    When the person runs `model check` on the term t1
    Then `model` exits successfully

  @g78 @r78
  Scenario: `model check` passes a verb with two senses told apart by kinds
    Given a term t1
    And the term t1 is polysemous
    When the person runs `model check` on the term t1
    Then `model` exits successfully

  @g79 @r79
  Scenario: `model check` refuses two senses that overlap
    Given a term t1
    And the term t1 is overlapping
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g80 @r80
  Scenario: `model lexicon` shows the terms of the imported packs
    Given a bounded context b1
    And the bounded context b1 is importing
    When the person runs `model lexicon` on the bounded context b1
    Then `model` prints the term t1
    And `model` exits successfully

  @g81 @r81
  Scenario: `model check` refuses an import of no pack
    Given a bounded context b1
    And the bounded context b1 is misimporting
    When the person runs `model check` on the bounded context b1
    Then `model` exits with an error naming the pack p1

  @g82 @r82
  Scenario: `model check` refuses a pack's term redefined without Redefines:
    Given a term t1
    And the term t1 is unmarked
    When the person runs `model check` on the term t1
    Then `model` exits with an error naming the term t1

  @g83 @r83
  Scenario: `model check` passes a term marked Redefines:
    Given a term t1
    And the term t1 is redefining
    When the person runs `model check` on the term t1
    Then `model` exits successfully

  @g84 @r84
  Scenario: `model parse` passes a plural subject whose verb agrees
    Given a requirement r1
    And the requirement r1 is plural
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g85 @r85
  Scenario: `model parse` refuses a verb that does not agree with its subject
    Given a requirement r1
    And the requirement r1 is disagreeing
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g86 @r86
  Scenario: `model parse` refuses a verb of the wrong aspect for its clause
    Given a requirement r1
    And the requirement r1 is misaspected
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g87 @r87
  Scenario: `model parse` passes a trigger that runs a command with an option
    Given a requirement r1
    And the requirement r1 is optioned
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g88 @r88
  Scenario: `model parse` passes of and its over a relation row or an attribute
    Given a requirement r1
    And the requirement r1 is genitive
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g89 @r89
  Scenario: `model parse` passes no before a subject or an object
    Given a requirement r1
    And the requirement r1 is denying
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g90 @r90
  Scenario: `model parse` passes a derived compound noun
    Given a requirement r1
    And the requirement r1 is compound
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g91 @r91
  Scenario: `model parse` passes only before an object
    Given a requirement r1
    And the requirement r1 is restrictive
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g92 @r92
  Scenario: `model parse` passes a relative clause on a verb's frame
    Given a requirement r1
    And the requirement r1 is relative
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g93 @r93
  Scenario: `model parse` passes whose over a relation row or an attribute
    Given a requirement r1
    And the requirement r1 is possessive
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g94 @r94
  Scenario: `model parse` refuses a requirement with two meanings
    Given a requirement r1
    And the requirement r1 is ambiguous
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the requirement r1

  @g95 @r95
  Scenario: `model parse --form` prints a requirement's logical form
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the logical form l1
    And `model` exits successfully

  @g96 @r96
  Scenario: `model parse` passes this before a kind whose entry has This:
    Given a requirement r1
    And the requirement r1 is indexical
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g97 @r97
  Scenario: `model parse` refuses the with no antecedent
    Given a requirement r1
    And the requirement r1 is antecedentless
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g98 @r98
  Scenario: `model parse` refuses a negated indefinite in a While clause
    Given a requirement r1
    And the requirement r1 is unquantified
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g99 @r99
  Scenario: `model parse` refuses a requirement with no trigger and neither always nor never
    Given a requirement r1
    And the requirement r1 is triggerless
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the requirement r1

  @g100 @r100
  Scenario: `model parse` refuses an unfinished requirement with the terms that may follow
    Given a requirement r1
    And the requirement r1 is unfinished
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the requirement r1
    And `model` prints the term t1

  @g101 @r101
  Scenario: `model check` warns of example data in a line
    Given a requirement r1
    And the requirement r1 is exemplified
    When the person runs `model check` on the requirement r1
    Then `model` prints the requirement r1

  @g131 @r131
  Scenario: `model logic` finds no clash between only and a change of that kind
    Given a capability c1
    And the capability c1 is restricting
    When the person runs `model logic` on the capability c1
    Then `model` does not print "L1"

  @g132 @r132
  Scenario: `model logic` finds the clash of every and a forbidden print
    Given a capability c1
    And the capability c1 is exhaustive
    When the person runs `model logic` on the capability c1
    Then `model` prints "L1"

  @g133 @r133
  Scenario: `model logic` reads an If line as taking precedence over a When line
    Given a capability c1
    And the capability c1 is overriding
    When the person runs `model logic` on the capability c1
    Then `model` does not print "L1"

  @g134 @r134
  Scenario: `model logic` pairs a universal condition with the lines it bears on
    Given a capability c1
    And the capability c1 is contravening
    When the person runs `model logic` on the capability c1
    Then `model` prints the universal condition u1

  @g135 @r135
  Scenario: `model logic` reports a requirement that other requirements entail
    Given a requirement r1
    And the requirement r1 is restating
    When the person runs `model logic` on the requirement r1
    Then `model` prints "L8"

  @g136 @r136
  Scenario: `model parse` reads a count
    Given a requirement r1
    And the requirement r1 is counted
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g137 @r137
  Scenario: `model logic` finds two counts that cannot both hold
    Given a capability c1
    And the capability c1 is overcounted
    When the person runs `model logic` on the capability c1
    Then `model` prints "L1"

  @g138 @r138
  Scenario: `model parse` reads a comparison of moments
    Given a requirement r1
    And the requirement r1 is timed
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g139 @r139
  Scenario: `model parse` reads the clock as a trigger
    Given a requirement r1
    And the requirement r1 is clocked
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g140 @r140
  Scenario: `model parse` reads the perfect as history
    Given a requirement r1
    And the requirement r1 is historical
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g141 @r141
  Scenario: `model parse` refuses a duration with no unit
    Given a requirement r1
    And the requirement r1 is unitless
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the requirement r1

  @g142 @r142
  Scenario: `model parse` reads a permission
    Given a requirement r1
    And the requirement r1 is permissive
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g143 @r143
  Scenario: `model parse` reads always and never with no trigger
    Given a requirement r1
    And the requirement r1 is invariant
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g144 @r144
  Scenario: `model logic` finds a line that forbids what another permits
    Given a capability c1
    And the capability c1 is forbidding
    When the person runs `model logic` on the capability c1
    Then `model` prints "L7"

  @g145 @r145
  Scenario: `model logic` checks a capability in the new language
    Given a capability c1
    And the capability c1 is recodified
    When the person runs `model logic` on the capability c1
    Then `model` exits successfully

  @g156 @r156
  Scenario: `model explain` prints a requirement
    When the person runs `model explain` on the requirement r1
    Then `model` prints the requirement r1
    And `model` exits successfully

  @g157 @r157
  Scenario: `model explain` prints what a refusal entails and where it comes from
    Given a requirement r1
    And the requirement r1 is refusing
    When the person runs `model explain` on the requirement r1
    Then `model` prints the universal condition u1
    And `model` prints the term t1

  @g158 @r158
  Scenario: `model explain` prints the If requirement that takes precedence
    Given a requirement r1
    And the requirement r1 is overridden
    When the person runs `model explain` on the requirement r1
    Then `model` prints the requirement r2
    And the requirement r2 is refusing

  @g159 @r159
  Scenario: `model explain` refuses an id that no capability holds
    Given a requirement r1
    And the requirement r1 is nonexistent
    When the person runs `model explain` on the requirement r1
    Then `model` exits with an error naming the requirement r1
    And `model` changes nothing

  @g160 @r160
  Scenario: `model check` reads a frame with a kind behind a preposition after its object
    Given a term t1
    And the term t1 is oblique
    When the person runs `model check` on the term t1
    Then `model` exits successfully

  @g161 @r161
  Scenario: `model parse` reads a codified-1 line in a verb's later sense
    Given a requirement r1
    And the requirement r1 is later-sensed
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g162 @r162
  Scenario: `model parse` refuses a definite that only the noun phrase it modifies gives
    Given a requirement r1
    And the requirement r1 is self-embedding
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g163 @r163
  Scenario: `model logic` reads a state verb that takes no object
    Given a requirement r1
    And the requirement r1 is intransitive
    When the person runs `model logic` on the requirement r1
    Then `model` exits successfully

  @g164 @r164
  Scenario: `model parse --form` reads "the K of X" in a relative clause on a K as its own referent
    Given a requirement r1
    And the requirement r1 is self-relating
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the relation reading r2
    And `model` exits successfully

  @g165 @r165
  Scenario: `model parse --form` reads "the K of every Y" inside the box of every Y
    Given a requirement r1
    And the requirement r1 is distributive
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the distributed reading d1
    And `model` exits successfully

  @g166 @r166
  Scenario: `model parse --form` binds "the K" to a referent outside a no, not, every or only box
    Given a requirement r1
    And the requirement r1 is shadowed
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the accessible reading a1
    And `model` exits successfully

  @g167 @r167
  Scenario: `model parse` refuses "the K" that only a referent inside a no, not, every or only box gives
    Given a requirement r1
    And the requirement r1 is unreachable
    When the person runs `model parse` on the requirement r1
    Then `model` exits with an error naming the term t1

  @g168 @r168
  Scenario: `model parse` reads a response that sets an attribute to a value
    Given a requirement r1
    And the requirement r1 is setting
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g169 @r169
  Scenario: `model parse --form` reads setting an attribute as a change of its value
    Given a requirement r1
    And the requirement r1 is setting
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints "initiates"

  @g170 @r170
  Scenario: `model logic` finds no clash in a response that sets an attribute
    Given a requirement r1
    And the requirement r1 is setting
    When the person runs `model logic` on the requirement r1
    Then `model` exits successfully

  @g171 @r171
  Scenario: `model logic` reads every in a While clause
    Given a capability c1
    And the capability c1 is quantifying
    When the person runs `model logic` on the capability c1
    Then `model` prints "L1"

  @g172 @r172
  Scenario: `model logic` reads a count in a While clause
    Given a capability c1
    And the capability c1 is thresholded
    When the person runs `model logic` on the capability c1
    Then `model` prints "L1"

  @g173 @r173
  Scenario: `model logic` reads a negated restriction on an object
    Given a capability c1
    And the capability c1 is excepting
    When the person runs `model logic` on the capability c1
    Then `model` prints "L1"
