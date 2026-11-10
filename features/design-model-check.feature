# generated from spec/capabilities/design-model-check.md by features generate; do not edit
Feature: Design model check
  Narrator: a person or session verifying a repository against the design model

  @g50 @r50
  Scenario: `model decisions` writes the decisions index
    When the person runs `model decisions`
    Then `model` writes the decisions index d1

  @g54 @r54
  Scenario: `model rules` prints every rule
    Given a rule r1
    And a rule r2
    When the person runs `model rules`
    Then `model` prints the rule r1
    And `model` prints the rule r2
    And `model` exits successfully

  @g55 @r55
  Scenario: `model forms` lists every file form
    Given a file form f1
    And a file form f2
    When the person runs `model forms`
    Then `model` prints the file form f1
    And `model` prints the file form f2
    And `model` exits successfully

  @g56 @r56
  Scenario: `work record` writes and commits a record
    When the person runs `work record`
    Then `work` writes the record r1
    And `work` commits the record r1

  @g156 @r156
  Scenario: `model explain` prints a requirement
    When the person runs `model explain` on the requirement r1
    Then `model` prints the requirement r1
    And `model` exits successfully

  @g174 @r174
  Scenario: `model check` exits successfully when nothing violates a rule
    Given this bounded context conforms to the design model
    When the person runs `model check`
    Then `model` does not print a violation
    And `model` exits successfully

  @g175 @r175
  Scenario: `model check` prints a violation under its rule's code
    Given a capability c1
    And the capability c1 violates `v15a`
    When the person runs `model check`
    Then `model` exits with an error naming `v15a`

  @g176 @r176
  Scenario: Two requirements with one id
    Given a capability c1
    And the capability c1 violates `v15b`
    When the person runs `model check`
    Then `model` exits with an error naming `v15b`

  @g177 @r177
  Scenario: A retired id used again
    Given a capability c1
    And the capability c1 violates `v15c`
    When the person runs `model check`
    Then `model` exits with an error naming `v15c`

  @g178 @r178
  Scenario: A group with more than one statement
    Given a requirement group r1
    And the requirement group r1 violates `v15l`
    When the person runs `model check`
    Then `model` exits with an error naming `v15l`

  @g179 @r179
  Scenario: Two groups of a capability that share their features, condition and trigger
    Given a requirement group r1
    And the requirement group r1 violates `v15n`
    When the person runs `model check`
    Then `model` exits with an error naming `v15n`

  @g180 @r180
  Scenario: A given line that is not example data
    Given a requirement group r1
    And the requirement group r1 violates `v15m`
    When the person runs `model check`
    Then `model` exits with an error naming `v15m`

  @g181 @r181
  Scenario: A requirement with no scenario
    Given a requirement group r1
    And the requirement group r1 violates `v_s3`
    When the person runs `model check`
    Then `model` exits with an error naming `v_s3`

  @g182 @r182
  Scenario: A scenario that names more than one requirement
    Given a scenario s1
    And the scenario s1 violates `v_s2`
    When the person runs `model check`
    Then `model` exits with an error naming `v_s2`

  @g183 @r183
  Scenario: A request with no origin
    Given a request r1
    And the request r1 violates `v17`
    When the person runs `model check`
    Then `model` exits with an error naming `v17`

  @g184 @r184
  Scenario: A delivered request resolved by no requirement of the spec
    Given a request r1
    And the request r1 violates `v3`
    When the person runs `model check`
    Then `model` exits with an error naming `v3`

  @g185 @r185
  Scenario: A requirement that uses an avoided word
    Given a requirement r1
    And the requirement r1 violates `v_t1`
    When the person runs `model check`
    Then `model` exits with an error naming `v_t1`

  @g186 @r186
  Scenario: Two glossary entries with one term
    Given a term t1
    And the term t1 violates `v_t2`
    When the person runs `model check`
    Then `model` exits with an error naming `v_t2`

  @g187 @r187
  Scenario: An avoided word that is a term
    Given a term t1
    And the term t1 violates `v_t3`
    When the person runs `model check`
    Then `model` exits with an error naming `v_t3`

  @g188 @r188
  Scenario: A requirement that does not parse
    Given a requirement r1
    And the requirement r1 violates `v_p1`
    When the person runs `model check`
    Then `model` exits with an error naming `v_p1`

  @g189 @r189
  Scenario: A request not of the form `work request` writes
    Given a request r1
    And the request r1 does not conform to the request form
    When the person runs `model check`
    Then `model` exits with an error naming the request r1

  @g190 @r190
  Scenario: A scenario that names a requirement its capability does not have
    Given a capability c1
    And a scenario s1
    And the scenario s1 has the capability c1
    And a requirement id r1
    And the capability c1 does not hold the requirement id r1
    And the scenario s1 refers to the requirement id r1
    When the person runs `model check`
    Then `model` exits with an error naming the scenario s1

  @g191 @r191
  Scenario: A capability with no capability id
    Given a capability c1
    And the capability c1 does not conform to the capability id form
    When the person runs `model check`
    Then `model` exits with an error naming the capability c1

  @g192 @r192
  Scenario: A capability with no Behaviour section
    Given a capability c1
    And the capability c1 does not conform to the capability section form
    When the person runs `model check`
    Then `model` exits with an error naming the capability c1

  @g193 @r193
  Scenario: A feature file of no capability
    Given a feature f1
    And the feature f1 does not conform to the feature form
    When the person runs `model check`
    Then `model` exits with an error naming the feature f1

  @g194 @r194
  Scenario: A decision with no id or no Decision section
    Given a design-decision d1
    And the design-decision d1 does not conform to the decision form
    When the person runs `model check`
    Then `model` exits with an error naming the design-decision d1

  @g195 @r195
  Scenario: A glossary bullet in no form of a term entry
    Given a term t1
    And the term t1 does not conform to the entry form
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g196 @r196
  Scenario: A repository not on the final layout
    Given this bounded context does not conform to the final layout
    When the person runs `model check`
    Then `model` exits with an error naming `scripts/migrate`

  @g197 @r197
  Scenario: A warning leaves the exit as it is
    Given an observation o1
    And the observation o1 violates `w_uncited_obs`
    When the person runs `model check`
    Then `model` prints `w_uncited_obs`
    And `model` exits successfully

  @g198 @r198
  Scenario: A context with no job has no unserved capability
    Given this bounded context has no job
    When the person runs `model check`
    Then `model` does not print `w_unserved_cap`

  @g199 @r199
  Scenario: `model check` tries again under an interpreter that has clingo
    Given an interpreter i1
    And the interpreter i1 does not import `clingo`
    And `model check` has the interpreter i1
    When the person runs `model check`
    Then the interpreter i2 imports `clingo`
    And `model` uses the interpreter i2

  @g200 @r200
  Scenario: No interpreter has clingo
    Given no interpreter imports `clingo`
    When the person runs `model check`
    Then `model` refuses `model check`
    And `model` names `pip install clingo`

  @g201 @r201
  Scenario: `model facts` prints the facts
    Given a fact f1
    And this bounded context has the fact f1
    And a fact f2
    And this bounded context has the fact f2
    When the person runs `model facts`
    Then `model` prints the fact f1
    And `model` prints the fact f2

  @g202 @r202
  Scenario: `model decisions --check` refuses an index that lacks an index entry
    Given an index entry i1
    And a decisions index d2
    And the decisions index d2 does not hold the index entry i1
    And a design-decision d1
    And the design-decision d1 has the index entry i1
    When the person runs `model decisions --check`
    Then `model` exits with an error naming the decisions index d2
    # entailed: U11 through the definition of refuse

  @g203 @r203
  Scenario: `model decisions --check` passes a current index
    Given no decisions index lacks an index entry
    When the person runs `model decisions --check`
    Then `model` exits successfully

  @g204 @r204
  Scenario: `work record` refuses an `--about` that identifies nothing
    Given a text t1
    And the text t1 does not conform to the node id form
    When the person runs `work record --about` on the text t1
    Then `work` refuses `work record --about`
    And `work` names `--about`

  @g205 @r205
  Scenario: `model parse` refuses a verb with no object
    Given an object o1
    And a term t1
    And the term t1 has the object o1
    And a requirement r1
    And the requirement r1 omits the object o1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the term t1

  @g206 @r206
  Scenario: `model parse` refuses a verb with no recipient
    Given a recipient r2
    And a term t1
    And the term t1 has the recipient r2
    And a requirement r1
    And the requirement r1 omits the recipient r2
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the term t1

  @g207 @r207
  Scenario: `model check` refuses a verb with no frame
    Given a term t1
    And the term t1 violates `v_t11`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g208 @r208
  Scenario: `model check` refuses a condition that relates two kinds
    Given a term t1
    And the term t1 violates `v_t12`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g209 @r209
  Scenario: `model parse` parses a negated verb or relation
    Given a requirement r1
    And a negation n1
    And the requirement r1 uses the negation n1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g210 @r210
  Scenario: `model parse` refuses a verb with a noun of the wrong kind
    Given a noun phrase n1
    And a term t1
    And the noun phrase n1 mismatches the term t1
    And a requirement r1
    And the requirement r1 uses the noun phrase n1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the term t1

  @g211 @r211
  Scenario: `model parse` parses a verb between two kinds in a condition
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a term t1
    And the term t1 is `state`
    And the precondition p1 uses the term t1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g212 @r212
  Scenario: `model parse` refuses a passive with no agent
    Given a passive form p1
    And the passive form p1 has no by-phrase
    And a requirement r1
    And the requirement r1 uses the passive form p1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the passive form p1

  @g213 @r213
  Scenario: `model parse` parses a trigger with a recipient
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And a recipient r2
    And the trigger t1 uses the recipient r2
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g214 @r214
  Scenario: `model check` refuses a term with no part of speech
    Given a term t1
    And the term t1 violates `v_t4`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g215 @r215
  Scenario: `model check` reads a frame with a preposition
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a preposition p1
    And the frame f1 has the preposition p1
    When the person runs `model check`
    Then `model` exits successfully

  @g216 @r216
  Scenario: `model parse` parses a verb whose frame has a preposition
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a preposition p1
    And the frame f1 has the preposition p1
    And a requirement r1
    And the requirement r1 uses the term t1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g217 @r217
  Scenario: `model check` refuses a frame that does not read
    Given a term t1
    And the term t1 violates `v_t13`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g218 @r218
  Scenario: A pair that cannot be unified sets only itself aside
    Given a unification failure u1
    And a capability c1
    And the capability c1 holds the unification failure u1
    And a clash c2
    And the capability c1 holds the clash c2
    When the person runs `model logic`
    Then `model` prints the clash c2
    And `model` prints `L1`

  @g219 @r219
  Scenario: `model rules --write` writes the rule catalogue
    When the person runs `model rules --write`
    Then `model` writes the rule catalogue r1
    And `model` exits successfully

  @g220 @r220
  Scenario: `model rules --check` refuses a catalogue that lacks a catalogue entry
    Given a catalogue entry c1
    And a rule catalogue r2
    And the rule catalogue r2 does not hold the catalogue entry c1
    And a rule r1
    And the rule r1 has the catalogue entry c1
    When the person runs `model rules --check`
    Then `model` exits with an error naming the rule catalogue r2
    # entailed: U11 through the definition of refuse

  @g221 @r221
  Scenario: `model check` refuses a verb with no aspect
    Given a term t1
    And the term t1 violates `v_t14`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g222 @r222
  Scenario: `model check` passes a verb with two frames
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a frame f2
    And the term t1 has the frame f2
    When the person runs `model check`
    Then `model` exits successfully

  @g223 @r223
  Scenario: `model check` passes a verb with two senses told apart by kinds
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a sense s2
    And the term t1 has the sense s2
    When the person runs `model check`
    Then `model` exits successfully

  @g224 @r224
  Scenario: `model check` refuses two senses that overlap
    Given a term t1
    And the term t1 violates `v_t15`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g225 @r225
  Scenario: `model lexicon` shows the terms of the imported packs
    Given a pack p1
    And this bounded context imports the pack p1
    And a term t1
    And the pack p1 has the term t1
    And a term t2
    And the pack p1 has the term t2
    When the person runs `model lexicon`
    Then `model` prints the term t1
    And `model` prints the term t2
    And `model` exits successfully

  @g226 @r226
  Scenario: `model check` refuses an import of no pack
    Given a pack p1
    And the pack p1 violates `v_t17`
    And this bounded context imports the pack p1
    When the person runs `model check`
    Then `model` exits with an error naming the pack p1

  @g227 @r227
  Scenario: `model check` refuses a pack's term redefined without Redefines:
    Given a term t1
    And the term t1 violates `v_t16`
    When the person runs `model check`
    Then `model` exits with an error naming the term t1

  @g228 @r228
  Scenario: `model check` passes a term marked Redefines:
    Given a term t1
    And a pack p1
    And the term t1 redefines the pack p1
    When the person runs `model check`
    Then `model` exits successfully

  @g229 @r229
  Scenario: `model parse` passes a plural subject whose verb agrees
    Given a requirement r1
    And a plural subject p1
    And the requirement r1 uses the plural subject p1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g230 @r230
  Scenario: `model parse` refuses a verb that does not agree with its subject
    Given a subject s1
    And a term t1
    And the term t1 has the subject s1
    And the term t1 disagrees with the subject s1
    And a requirement r1
    And the requirement r1 uses the term t1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the term t1

  @g231 @r231
  Scenario: `model parse` refuses a verb of the wrong aspect for its clause (case 1)
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a term t1
    And the term t1 is `action`
    And the precondition p1 uses the term t1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the requirement r1

  @g231 @r231
  Scenario: `model parse` refuses a verb of the wrong aspect for its clause (case 2)
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And a term t2
    And the term t2 is `state`
    And the trigger t1 uses the term t2
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the requirement r1

  @g232 @r232
  Scenario: `model parse` passes a trigger that runs a command with an option
    Given a trigger t1
    And a requirement r1
    And the requirement r1 has the trigger t1
    And an option o1
    And the trigger t1 uses the option o1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g233 @r233
  Scenario: `model parse` passes of and its over a relation row or an attribute
    Given a requirement r1
    And a genitive g1
    And the requirement r1 uses the genitive g1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g234 @r234
  Scenario: `model parse` passes no before a subject or an object
    Given a requirement r1
    And a negative quantifier n1
    And the requirement r1 uses the negative quantifier n1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g235 @r235
  Scenario: `model parse` passes a derived compound noun
    Given a requirement r1
    And a compound noun c1
    And the requirement r1 uses the compound noun c1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g236 @r236
  Scenario: `model parse` passes only before an object
    Given a requirement r1
    And a restriction r2
    And the requirement r1 uses the restriction r2
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g237 @r237
  Scenario: `model parse` passes a relative clause on a verb's frame
    Given a requirement r1
    And a relative clause r2
    And the requirement r1 uses the relative clause r2
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g238 @r238
  Scenario: `model parse` passes whose over a relation row or an attribute
    Given a requirement r1
    And a whose clause w1
    And the requirement r1 uses the whose clause w1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g239 @r239
  Scenario: `model parse` refuses a requirement with two meanings
    Given a logical form l1
    And a requirement r1
    And the requirement r1 has the logical form l1
    And a logical form l2
    And the requirement r1 has the logical form l2
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the requirement r1

  @g240 @r240
  Scenario: `model parse --form` prints a requirement's logical form
    When the person runs `model parse --form` on the requirement r1
    Then the requirement r1 has the logical form l1
    And `model` prints the logical form l1
    And `model` exits successfully

  @g241 @r241
  Scenario: `model parse` passes this before a kind whose entry has This:
    Given a requirement r1
    And a demonstrative d1
    And the requirement r1 uses the demonstrative d1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g242 @r242
  Scenario: `model parse` refuses the with no antecedent
    Given a definite noun phrase d1
    And the definite noun phrase d1 has no antecedent
    And a requirement r1
    And the requirement r1 uses the definite noun phrase d1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the definite noun phrase d1

  @g243 @r243
  Scenario: `model parse` refuses a negated indefinite in a While clause
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a negated indefinite n1
    And the precondition p1 uses the negated indefinite n1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the negated indefinite n1

  @g244 @r244
  Scenario: `model parse` refuses a requirement with no trigger and neither always nor never
    Given a requirement r1
    And the requirement r1 has no trigger
    And the requirement r1 uses no modal adverb
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the requirement r1

  @g245 @r245
  Scenario: `model parse` refuses a fragment with the terms that may follow
    When the person runs `model parse` on the fragment f1
    Then `model` refuses `model parse`
    And `model` names the fragment f1
    And `model` prints the term t1

  @g246 @r246
  Scenario: `model check` warns of example data in a line
    Given a requirement r1
    And the requirement r1 violates `w_example`
    When the person runs `model check`
    Then `model` prints the requirement r1

  @g247 @r247
  Scenario: `model logic` finds no clash between only and a change of that kind
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a restriction r2
    And the requirement r1 uses the restriction r2
    And a requirement r3
    And the capability c1 has the requirement r3
    And an act a1
    And the restriction r2 allows the act a1
    And the requirement r3 uses the act a1
    When the person runs `model logic`
    Then `model` exits successfully

  @g248 @r248
  Scenario: `model logic` finds the clash of every and a forbidden print
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a universal quantifier u1
    And the requirement r1 uses the universal quantifier u1
    And a requirement r2
    And the capability c1 has the requirement r2
    And an act a1
    And the universal quantifier u1 obliges the act a1
    And the requirement r2 forbids the act a1
    When the person runs `model logic`
    Then `model` prints `L1`

  @g249 @r249
  Scenario: `model logic` reads an If line as taking precedence over a When line
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement r2
    And the capability c1 has the requirement r2
    And the requirement r1 overrides the requirement r2
    When the person runs `model logic`
    Then `model` exits successfully

  @g250 @r250
  Scenario: `model logic` pairs a universal condition with the lines it bears on
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And an act a1
    And the requirement r1 obliges the act a1
    And a universal condition u1
    And the universal condition u1 forbids the act a1
    When the person runs `model logic`
    Then `model` prints the universal condition u1

  @g251 @r251
  Scenario: `model logic` reports a requirement that other requirements entail
    Given a consequence c1
    And a requirement r1
    And the requirement r1 has the consequence c1
    And the requirement r1 adds no consequence
    When the person runs `model logic`
    Then `model` prints `L8`

  @g252 @r252
  Scenario: `model parse` reads a count
    Given a requirement r1
    And a count c1
    And the requirement r1 uses the count c1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g253 @r253
  Scenario: `model logic` finds two counts that cannot both hold
    Given a count c2
    And a count c3
    And the count c2 contradicts the count c3
    And a capability c1
    And the capability c1 holds the count c2
    When the person runs `model logic`
    Then `model` prints `L1`

  @g254 @r254
  Scenario: `model parse` reads a comparison of moments
    Given a requirement r1
    And a comparison c1
    And the requirement r1 uses the comparison c1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g255 @r255
  Scenario: `model parse` reads the clock as a trigger
    Given a requirement r1
    And a clock trigger c1
    And the requirement r1 uses the clock trigger c1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g256 @r256
  Scenario: `model parse` reads the perfect as history
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a perfect p2
    And the precondition p1 uses the perfect p2
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g257 @r257
  Scenario: `model parse` refuses a duration with no unit
    Given a number n1
    And the number n1 has no unit
    And a requirement r1
    And the requirement r1 uses the number n1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the requirement r1

  @g258 @r258
  Scenario: `model parse` reads a permission
    Given a requirement r1
    And a permission p1
    And the requirement r1 uses the permission p1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g259 @r259
  Scenario: `model parse` reads always and never with no trigger
    Given a requirement r1
    And a modal adverb m1
    And the requirement r1 uses the modal adverb m1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g260 @r260
  Scenario: `model logic` finds a line that forbids what another permits
    Given a requirement r1
    And a capability c1
    And the capability c1 has the requirement r1
    And a requirement r2
    And the capability c1 has the requirement r2
    And an act a1
    And the requirement r2 permits the act a1
    And the requirement r1 forbids the act a1
    When the person runs `model logic`
    Then `model` prints `L7`

  @g261 @r261
  Scenario: `model logic` checks a capability in the new language
    Given a capability c1
    And the capability c1 is `codified-2`
    When the person runs `model logic`
    Then `model` exits successfully

  @g262 @r262
  Scenario: `model explain` prints what a refusal entails and where it comes from
    Given a requirement r1
    And a refusal r2
    And the requirement r1 uses the refusal r2
    When the person runs `model explain` on the requirement r1
    Then `model` prints the universal condition u1
    And `model` prints the term t1

  @g263 @r263
  Scenario: `model explain` prints the If requirement that takes precedence
    Given a requirement r2
    And a requirement r1
    And the requirement r2 overrides the requirement r1
    When the person runs `model explain` on the requirement r1
    Then the requirement r4 uses the refusal r3
    And `model` prints the requirement r4

  @g264 @r264
  Scenario: `model explain` refuses an id that no capability holds
    Given a requirement id r1
    And no capability holds the requirement id r1
    When the person runs `model explain` on the requirement id r1
    Then `model` refuses `model explain`
    And `model` names the requirement id r1

  @g265 @r265
  Scenario: `model check` reads a frame with a recipient behind a preposition other than to
    Given an oblique recipient o1
    And a term t1
    And the term t1 has the oblique recipient o1
    When the person runs `model check`
    Then `model` exits successfully

  @g266 @r266
  Scenario: `model parse` reads a codified-1 line in a verb's later sense
    Given a capability c1
    And the capability c1 is `codified-1`
    And a requirement r1
    And the capability c1 has the requirement r1
    And a later sense l1
    And the requirement r1 uses the later sense l1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g267 @r267
  Scenario: `model parse` refuses a definite that only the noun phrase it modifies gives
    Given a self-reference s1
    And the self-reference s1 has no antecedent
    And a requirement r1
    And the requirement r1 uses the self-reference s1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the self-reference s1

  @g268 @r268
  Scenario: `model logic` reads a state verb that takes no object
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a term t1
    And the term t1 has no object
    And the precondition p1 uses the term t1
    When the person runs `model logic` on the requirement r1
    Then `model` exits successfully

  @g269 @r269
  Scenario: `model parse --form` reads "the K of X" in a relative clause on a K as its own referent
    Given a requirement r1
    And an inner genitive i1
    And the requirement r1 uses the inner genitive i1
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the relation reading r2
    And `model` exits successfully

  @g270 @r270
  Scenario: `model parse --form` reads "the K of every Y" inside the box of every Y
    Given a requirement r1
    And a distributive genitive d1
    And the requirement r1 uses the distributive genitive d1
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the distributed reading d2
    And `model` exits successfully

  @g271 @r271
  Scenario: `model parse --form` binds "the K" to a referent outside a no, not, every or only box
    Given a requirement r1
    And a boxed noun phrase b1
    And the requirement r1 uses the boxed noun phrase b1
    And an antecedent a1
    And a definite noun phrase d1
    And the definite noun phrase d1 has the antecedent a1
    And the requirement r1 uses the definite noun phrase d1
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints the accessible reading a2
    And `model` exits successfully

  @g272 @r272
  Scenario: `model parse` refuses "the K" that only a referent inside a no, not, every or only box gives
    Given a requirement r1
    And a boxed noun phrase b1
    And the requirement r1 uses the boxed noun phrase b1
    And a definite noun phrase d1
    And the definite noun phrase d1 has no antecedent
    And the requirement r1 uses the definite noun phrase d1
    When the person runs `model parse` on the requirement r1
    Then `model` refuses `model parse`
    And `model` names the definite noun phrase d1

  @g273 @r273
  Scenario: `model parse` reads a response that sets an attribute to a value
    Given a requirement r1
    And an assignment a1
    And the requirement r1 uses the assignment a1
    When the person runs `model parse` on the requirement r1
    Then `model` exits successfully

  @g274 @r274
  Scenario: `model parse --form` reads setting an attribute as a change of its value
    Given a requirement r1
    And an assignment a1
    And the requirement r1 uses the assignment a1
    When the person runs `model parse --form` on the requirement r1
    Then `model` prints `initiates`

  @g275 @r275
  Scenario: `model logic` finds no clash in a response that sets an attribute
    Given a requirement r1
    And an assignment a1
    And the requirement r1 uses the assignment a1
    When the person runs `model logic` on the requirement r1
    Then `model` exits successfully

  @g276 @r276
  Scenario: `model logic` reads every in a While clause
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a universal quantifier u1
    And the precondition p1 uses the universal quantifier u1
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    When the person runs `model logic`
    Then `model` prints `L1`

  @g277 @r277
  Scenario: `model logic` reads a count in a While clause
    Given a precondition p1
    And a requirement r1
    And the requirement r1 has the precondition p1
    And a count c1
    And the precondition p1 uses the count c1
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    When the person runs `model logic`
    Then `model` prints `L1`

  @g278 @r278
  Scenario: `model logic` reads a negated restriction on an object
    Given a requirement r1
    And a negated modifier n1
    And the requirement r1 uses the negated modifier n1
    And an act a1
    And the requirement r1 obliges the act a1
    And a requirement r2
    And the requirement r2 forbids the act a1
    When the person runs `model logic`
    Then `model` prints `L1`
