# formulated from spec/capabilities/design-model-check.md
Feature: Design model check
  Narrator: a person or session verifying a repository against the design model

  @r1
  Scenario: a repository the grammar accepts passes
    Given a bounded context with one capability whose requirement r1 has a scenario tagged @r1
    When `model check` is run
    Then it says it found no violation, unresolved reference or file problem
    And it exits successfully

  @r2
  Scenario: violations are printed by their grammar name and make `model check` exit with an error
    Given a bounded context with a requirement no scenario names
    When `model check` is run
    Then the output names v_s3 with its plain label and the requirement's id
    And it exits with an error

  @r3
  Scenario: a requirement bullet without an id is refused
    Given a capability whose Behaviour has a bullet with no [r<n>]
    When `model check` is run
    Then the output names v15a

  @r4
  Scenario: two requirements with one id are refused
    Given a capability whose Behaviour has two bullets marked [r1]
    When `model check` is run
    Then the output names v15b

  @r5
  Scenario: a retired id used again is refused
    Given a capability that lists r1 as retired and has a requirement [r1]
    When `model check` is run
    Then the output names v15c

  @r6
  Scenario: a proposal changing a requirement no capability has is refused
    Given a capability-proposal that changes r9 of a capability with no r9
    When `model check` is run
    Then the output names v15e with the proposal and the requirement

  @r7
  Scenario: a proposal formulated before its requirement has a scenario is refused
    Given a capability-proposal with status formulated that adds a requirement no scenario names
    When `model check` is run
    Then the output names v15f with the proposal

  @r8
  Scenario: a guarantees capability needs no scenarios
    Given a capability in the guarantees group whose requirements no scenario names
    When `model check` is run
    Then the output does not name v_s3

  @r9
  Scenario: references that name nothing are printed
    Given a scenario tagged @r7 in a capability with no r7, and a capability resting on a decision that does not exist
    When `model check` is run
    Then each is printed as unresolved

  @r10
  Scenario: a part that reaches no initiative is refused
    Given a work-item whose part_of names nothing
    When `model check` is run
    Then the output names v9c with the work-item

  @r11
  Scenario: warnings are counted and do not change whether `model check` exits successfully
    Given a bounded context the grammar accepts, with an observation no initiative cites
    When `model check` is run
    Then the output gives w_uncited_obs with its plain label and its count
    And it exits successfully

  @r111
  Scenario: a bounded context with no job gets no unserved-capability warning
    Pins that a capability is not warned about as serving no job when the bounded context has no job for it to serve.
    Given a bounded context with one capability and no job
    When `model check` is run
    Then the output does not give w_unserved_cap

  @r12
  Scenario: without clingo `model check` says how to install it
    Given an interpreter without the clingo package
    When `model check` is run
    Then it names clingo and the pip command that installs it
    And it exits with an error

  @r13
  Scenario: facts are printed in clingo's syntax
    Given a bounded context with one capability
    When `model facts` is run
    Then each line is one fact, such as a node fact for the capability

  @r14
  Scenario: the decisions index lists every decision
    Given two decisions under spec/decisions/, one superseding the other
    When `model decisions` is run
    Then spec/decisions/index.md has a row for each with its summary, status and what it supersedes, linked to its file

  @r15
  Scenario: a stale decisions index is printed as not current and left alone
    Given a spec/decisions/index.md that differs from what `model decisions` writes
    When `model decisions --check` is run
    Then it says the file is not current, exits with an error, and the file is unchanged

  @r16
  Scenario: why traces a requirement to its initiative's sources
    Given an initiative citing an observation, with a capability-proposal that adds r1
    When `model why` is run for that requirement
    Then it prints the requirement, the proposal, the initiative and the observation

  @r17
  Scenario: why with no proposal says so and succeeds
    Pins that a requirement nothing has added or changed is an answer, not a failure.
    Given a requirement no capability-proposal adds or changes
    When `model why` is run for it
    Then it says no capability-proposal adds or changes it
    And it exits successfully

  @r18
  Scenario: a range of ids stands for each id in it
    Given a capability-proposal that adds thing#r1-r3
    When `model why` is run for thing#r2
    Then it prints the proposal as adding it

  @r19 @deprecated
  Scenario Outline: model reads the repository's files under its root (deprecated)
    Deprecated for: model reads the repository's files under its root
    Pins which files of a repository model reads, and that the root is the current directory unless --root names one.
    Given a repository in a directory that has <file>
    When `model facts` is run <how>
    Then the facts printed <facts> what <file> contains

    Examples:
      | file                               | how                                   | facts           |
      | spec/index.md                      | with --root naming that directory     | include         |
      | spec/capabilities/thing.md         | with --root naming that directory     | include         |
      | features/sub/thing.feature         | with --root naming that directory     | include         |
      | spec/decisions/0001-one.md         | with --root naming that directory     | include         |
      | spec/decisions/index.md            | with --root naming that directory     | do not include  |
      | .shop/work/i1/initiative.md        | with --root naming that directory     | include         |
      | .shop/records/observations.md      | with --root naming that directory     | include         |
      | .shop/records/review/f1.md with an id | with --root naming that directory  | include         |
      | .shop/records/review/f2.md with no id | with --root naming that directory  | do not include  |
      | decisions/0001-one.md              | with --root naming that directory     | do not include  |
      | work/i1/initiative.md              | with --root naming that directory     | do not include  |
      | records/observations.md            | with --root naming that directory     | do not include  |
      | spec/capabilities/thing.md         | from that directory with no --root    | include         |

  @r19
  Scenario Outline: model reads the repository's files under its root
    Pins which files of a repository model reads, and that the root is the current directory unless --root names one.
    Given a repository in a directory that has <file>
    When `model facts` is run <how>
    Then the facts printed <facts> what <file> contains

    Examples:
      | file                               | how                                   | facts           |
      | spec/index.md                      | with --root naming that directory     | include         |
      | spec/capabilities/thing.md         | with --root naming that directory     | include         |
      | features/sub/thing.feature         | with --root naming that directory     | include         |
      | spec/decisions/0001-one.md         | with --root naming that directory     | include         |
      | spec/decisions/index.md            | with --root naming that directory     | do not include  |
      | .shop/work/i1/initiative.md        | with --root naming that directory     | include         |
      | .shop/work/requests/q1.md          | with --root naming that directory     | include         |
      | .shop/records/observations.md      | with --root naming that directory     | include         |
      | .shop/records/review/f1.md with an id | with --root naming that directory  | include         |
      | .shop/records/review/f2.md with no id | with --root naming that directory  | do not include  |
      | decisions/0001-one.md              | with --root naming that directory     | do not include  |
      | work/i1/initiative.md              | with --root naming that directory     | do not include  |
      | records/observations.md            | with --root naming that directory     | do not include  |
      | spec/capabilities/thing.md         | from that directory with no --root    | include         |

  @r20
  Scenario Outline: a scenario names a requirement by its tag in its capability's feature file
    Pins where an @r<n> tag may sit, and which feature file a capability's scenarios are read from.
    Given a capability thing with requirement r2
    And a scenario in <feature file> with the tag @r2 <placed>
    When `model check` is run
    Then the requirement thing#r2 is <printed> under v_s3

    Examples:
      | feature file               | placed          | printed |
      | features/thing.feature     | on the scenario | not      |
      | features/thing.feature     | on its feature  | not      |
      | features/sub/thing.feature | on the scenario | still    |
      | features/other.feature     | on the scenario | still    |

  @r21
  Scenario: a reference written name#r<n> is that capability's requirement
    Pins that the part before # is the capability's name in this bounded context and the part after it the requirement's id.
    Given a bounded context with id bounded-context/ex.com/prod/ctx and a capability thing with requirement r2
    And a capability-proposal that adds thing#r2
    When `model why` is run for capability/thing#r2
    Then it prints capability/ex.com/prod/ctx/thing#r2 with its text and the proposal as adding it

  @r22
  Scenario Outline: a reference in neither requirement form, or a reversed range, is unresolved
    Pins the forms a requirement reference in a list may take.
    Given a capability thing with requirements r1 to r3
    And a capability-proposal whose list names <reference>
    When `model check` is run
    Then <reference> is printed as unresolved

    Examples:
      | reference                |
      | thing                    |
      | thing#2                  |
      | thing#line2              |
      | thing#r3-r1              |
      | design-decision/thing#r1 |
      | thing#behaviour/r2       |

  @r23
  Scenario Outline: a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id
    Pins that an absent requirement is an unresolved reference whether added or removed, and that adding a retired id is a v15c instead.
    Given a capability thing with requirement r1 that lists r4 as retired
    And a capability-proposal that <change> thing#<id>
    When `model check` is run
    Then thing#<id> is <printed>

    Examples:
      | change  | id | printed                                  |
      | adds    | r9 | printed as unresolved                    |
      | removes | r9 | printed as unresolved                    |
      | adds    | r4 | printed under v15c and not as unresolved |
      | removes | r4 | printed as unresolved                    |

  @r66
  Scenario Outline: a proposal's list naming a term the glossary lacks is unresolved, unless a merged proposal removes it
    Pins that term/<term> in a proposal's list is read against the glossary, and that a settled proposal may remove a term already gone.
    Given a glossary with the term store
    And a <status> capability-proposal whose <list> names term/<term>
    When `model check` is run
    Then term/<term> is <printed>

    Examples:
      | status    | list    | term  | printed                   |
      | drafted   | adds    | store | not printed as unresolved |
      | drafted   | changes | store | not printed as unresolved |
      | drafted   | adds    | shelf | printed as unresolved     |
      | drafted   | removes | shelf | printed as unresolved     |
      | merged    | removes | shelf | not printed as unresolved |
      | formulated | removes | shelf | not printed as unresolved |
      | merged    | adds    | shelf | printed as unresolved     |

  @r24
  Scenario Outline: a frontmatter reference to nothing, or to the wrong kind, is unresolved
    Pins that each named frontmatter reference must reach a node, and that supersedes, under, for, blocked_by and depends_on must reach a node of the kind they need.
    Given a file whose <field> names <target>
    When `model check` is run
    Then that <field> is printed as unresolved

    Examples:
      | field      | target                                   |
      | supersedes | an id nothing in the repository has      |
      | source     | an id nothing in the repository has      |
      | part_of    | an id nothing in the repository has      |
      | argues     | an id nothing in the repository has      |
      | under      | an id nothing in the repository has      |
      | for        | an id nothing in the repository has      |
      | blocked_by | an id nothing in the repository has      |
      | depends_on | an id nothing in the repository has      |
      | under      | a decision, where a capability is needed |

  @r25
  Scenario Outline: a malformed index or capability file is a file problem
    Pins the shape spec/index.md and each capability file must have to be read.
    Given a bounded context with id bounded-context/acme.com/shop/cart in which <case>
    When `model check` is run
    Then it prints a file problem naming <file>

    Examples:
      | case                                                                      | file                       |
      | spec/index.md is missing                                                  | spec/index.md              |
      | spec/index.md has no id                                                   | spec/index.md              |
      | spec/capabilities/thing.md has the id capability/acme.com/shop/cart/other | spec/capabilities/thing.md |
      | spec/capabilities/thing.md has no ## Behaviour section                    | spec/capabilities/thing.md |
      | spec/capabilities/thing.md lists retired: [three]                         | spec/capabilities/thing.md |
      | spec/capabilities/thing.md has formulated_as: features/thing.feature      | spec/capabilities/thing.md |

  @r61
  Scenario Outline: a path of the old layout is a file problem naming scripts/migrate
    Pins that `model check` refuses a repository not yet relocated to the final layout, each old path named with the script that relocates it.
    Given a bounded context the grammar accepts, with <path> at its root
    When `model check` is run
    Then it prints a file problem naming <path> and scripts/migrate

    Examples:
      | path              |
      | spec/decisions.md |
      | decisions/        |
      | work/             |
      | records/          |

  @r26
  Scenario Outline: a feature file no capability is formulated as, with a title twice, or with a scenario tagged @holding, is a file problem
    Pins which feature files belong to a capability, that titles are unique among the scenarios not deprecated, and that the tag @holding is refused.
    Given a capability thing
    And a feature file <file> in which <titles>
    When `model check` is run
    Then it <prints> a file problem naming <file>

    Examples:
      | file                       | titles                                                                     | prints          |
      | features/stray.feature     | every scenario has its own title                                           | prints          |
      | features/thing.feature     | every scenario has its own title                                           | does not print  |
      | features/sub/thing.feature | every scenario has its own title                                           | prints          |
      | features/thing.feature     | two scenarios are titled "Apply a code"                                    | prints          |
      | features/thing.feature     | two scenarios are titled "Apply a code" and one of them is tagged @deprecated | does not print  |
      | features/thing.feature     | a scenario with its own title is tagged @holding                           | prints          |
      | features/thing.feature     | a scenario is tagged @deprecated and @holding                              | prints          |

  @r27
  Scenario Outline: a malformed work directory or work file is a file problem
    Pins the shape each initiative and part file must have, and that a missing initiative.md is charged to its directory.
    Given a repository with a work directory .shop/work/i1 in which <case>
    When `model check` is run
    Then it prints a file problem naming <named>

    Examples:
      | case                                                                 | named                                              |
      | there is no initiative.md                                            | .shop/work/i1, and not .shop/work/i1/initiative.md |
      | initiative.md has no id                                              | .shop/work/i1/initiative.md                        |
      | the part p1.md has no id                                             | .shop/work/i1/p1.md                                |
      | the part p1.md has the kind banana                                   | .shop/work/i1/p1.md                                |
      | the part p1.md has no status                                         | .shop/work/i1/p1.md                                |
      | the part p1.md has a status not in its kind's lifecycle              | .shop/work/i1/p1.md                                |
      | the part p1.md has the kind capability-proposal and the status built | .shop/work/i1/p1.md                                |
      | initiative.md has the priority high                                  | .shop/work/i1/initiative.md                        |
      | initiative.md has a date written 16/10/2026                          | .shop/work/i1/initiative.md                        |

  @r27
  Scenario: a work-item accepting a requirement no scenario names is a file problem
    Pins that a work-item may accept only requirements a scenario already names.
    Given a capability thing with requirement r2 that no scenario names
    And a work-item in .shop/work/i1/w1.md that accepts thing#r2
    When `model check` is run
    Then it prints a file problem naming .shop/work/i1/w1.md

  @r27
  Scenario: a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem
    Pins that a guarantees capability's requirements, which no scenario names, may be accepted by a work-item.
    Given a capability thing in the guarantees group with requirement r2 that no scenario names
    And a work-item in .shop/work/i1/w1.md that accepts thing#r2
    When `model check` is run
    Then it prints no file problem naming .shop/work/i1/w1.md

  @r27
  Scenario: a green work-item accepting a retired id is no file problem
    Pins that a retired id is left out of what a scenario must name for a work-item to accept it, once that work-item is green.
    Given a capability thing whose frontmatter lists r2 as retired
    And a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2
    When `model check` is run
    Then it prints no file problem naming .shop/work/i1/w1.md

  @r110
  Scenario Outline: a work-item not named w<n>.md, or two work-items with one id, is a file problem
    Pins that a work-item's file is named by its id and that no id is held by two work-items, in one initiative or across them.
    Given a repository in which <case>
    When `model check` is run
    Then it <prints> a file problem

    Examples:
      | case                                                                                              | prints         |
      | a work-item in .shop/work/i1/fix-login.md has the id w3                                           | prints         |
      | a work-item in .shop/work/i1/w3.md has the id w3                                                  | does not print |
      | a work-item in .shop/work/i1/w3.md and a work-item in .shop/work/i2/w3.md each have the id w3     | prints         |
      | a work-item in .shop/work/i1/w3.md has the id w3 and one in .shop/work/i2/w4.md has the id w4     | does not print |

  @r29
  Scenario Outline: a malformed decision, record or frontmatter is a file problem
    Pins the frontmatter faults in decisions, records and shared ids that `model check` refuses.
    Given a repository in which <case>
    When `model check` is run
    Then it prints a file problem

    Examples:
      | case                                                         |
      | a decision under spec/decisions/ has no id                   |
      | a decision under spec/decisions/ has no ## Decision section  |
      | a record under .shop/records/ with an id has the kind banana |
      | a frontmatter value is written as a folded block, with >     |
      | a frontmatter value is written as a literal block, with \|   |
      | a decision and an observation have the same id               |

  @r2
  Scenario: file problems are each printed and make `model check` exit with an error
    Pins that every file problem is shown and that any one of them makes `model check` exit with an error.
    Given a repository with two capabilities that each have no ## Behaviour section
    When `model check` is run
    Then it prints a file problem for each of the two capabilities
    And it exits with an error

  @r33
  Scenario Outline: with --json `model check`'s findings are one JSON object
    Pins the machine-readable output and that it does not change whether `model check` exits successfully.
    Given a repository <repository>
    When `model check` is run with --json
    Then it prints one JSON object with the violations, warnings, unresolved references and file problems
    And the object maps each code it prints to its plain label
    And it exits <exit>

    Examples:
      | repository                             | exit          |
      | the grammar accepts                    | successfully  |
      | with a requirement no scenario names   | with an error |

  @r34
  Scenario Outline: only a capability-change initiative may have several parts directly
    Pins that an initiative has one part directly, except a capability-change with capability-proposals.
    Given <initiative> with <parts> directly under it
    When `model check` is run
    Then the initiative is <printed> under v_k5

    Examples:
      | initiative                                   | parts                    | printed |
      | an initiative that is not a capability-change | two parts                | printed |
      | a capability-change initiative               | two capability-proposals | not printed |

  @r35
  Scenario: a proposal arguing two capabilities is refused
    Pins that a capability-proposal argues one capability.
    Given capabilities thing and other
    And a capability-proposal that argues both thing and other
    When `model check` is run
    Then the output names v_k6 with the proposal

  @r36
  Scenario: an initiative may be `done` when its proposal is formulated
    Pins that formulated is a closed status for a capability-proposal under a `done` initiative.
    Given a capability-change initiative with status `done`
    And under it a capability-proposal with status formulated, whose requirements scenarios name
    When `model check` is run
    Then no violation names the initiative

  @r37
  Scenario: a current decisions index passes `model decisions --check`
    Pins what `model decisions --check` says of a current index.
    Given a spec/decisions/index.md that is what `model decisions` writes
    When `model decisions --check` is run
    Then it says the file is current
    And it exits successfully

  @r14
  Scenario: writing the decisions index leaves out decisions with no id
    Pins that only decisions with an id are indexed.
    Given two decisions under spec/decisions/, one of them with no id
    When `model decisions` is run
    Then spec/decisions/index.md lists the decision with an id and not the one without

  @r105
  Scenario: why refuses an argument that is not a requirement reference
    Pins that `model why` takes only a requirement reference.
    Given a capability thing
    When `model why` is run for thing
    Then it is refused because thing is not a requirement reference
    And it exits with an error

  @r16
  Scenario: why on a requirement no capability has still lists its proposals
    Pins that a missing requirement does not hide the proposals that name it.
    Given a capability thing with no requirement r9
    And a capability-proposal that changes thing#r9
    When `model why` is run for thing#r9
    Then it says no capability has thing#r9 where the requirement's text would be
    And it lists the proposal

  @r16
  Scenario Outline: why lists every proposal naming the requirement by date, each with its status and date
    Pins that removing proposals are listed too, in date order with status and date.
    Given a capability thing with requirement r2
    And <proposals>
    When `model why` is run for thing#r2
    Then it lists <listed>, in that order, each with its status and date

    Examples:
      | proposals                                                                                                   | listed      |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that adds thing#r2    | p2 then p1  |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that changes thing#r2 | p2 then p1  |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that removes thing#r2 | p2 then p1  |
      | only a capability-proposal p1 dated 2026-10-01 that removes thing#r2                                        | p1          |

  @r17
  Scenario Outline: why says so and succeeds when the only proposals naming the requirement remove it
    Pins that a proposal that removes the requirement is no proposal that adds or changes it.
    Given a capability thing with requirement r2
    And <proposals>
    When `model why` is run for thing#r2
    Then it says no capability-proposal adds or changes thing#r2
    And it exits successfully

    Examples:
      | proposals                                                                                                   |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that removes thing#r2 |
      | only a capability-proposal p1 dated 2026-10-01 that removes thing#r2                                        |

  @r43
  Scenario Outline: a node may be written in short where its field allows it
    Pins that the kind-and-name short form is read in any field, and the bare name only in a field that fixes the kind.
    Given a bounded context with id bounded-context/ex.com/prod/ctx, a capability thing and an initiative i1
    And a capability-proposal whose <field> is written <written>
    When `model check` is run
    Then <written> is <reading>

    Examples:
      | field   | written                          | reading                                                                 |
      | argues  | thing                            | read as capability/ex.com/prod/ctx/thing and not printed as unresolved |
      | argues  | capability/thing                 | read as capability/ex.com/prod/ctx/thing and not printed as unresolved |
      | argues  | capability/ex.com/prod/ctx/thing | read as capability/ex.com/prod/ctx/thing and not printed as unresolved |
      | part_of | initiative/i1                    | read as initiative/ex.com/prod/ctx/i1 and not printed as unresolved    |
      | part_of | i1                               | printed as unresolved                                                  |

  @r20
  Scenario: a deprecated scenario names no requirement
    Pins that a scenario tagged @deprecated does not count as a requirement's acceptance-scenario.
    Given a capability thing with requirement r2
    And its only scenario tagged @r2 is also tagged @deprecated
    When `model check` is run
    Then the requirement thing#r2 is printed under v_s3

  @r64
  Scenario Outline: a decision's source is a list of ids and its by is not read
    Pins that each id in a decision's source must name a node, and that its by, where the free text goes, is never read as a reference.
    Given a decision whose source is <source> and whose by is <by>
    When `model check` is run
    Then the decision's source is <printed> as unresolved

    Examples:
      | source                      | by                         | printed     |
      | [observation/obs-1]         | the person, 2026-10-19     | not printed |
      | [observation/ghost]         | the person, 2026-10-19     | printed     |
      | the person, 2026-10-19      | none                       | printed     |
      | [observation/obs-1]         | observation/ghost          | not printed |

  @r46
  Scenario Outline: a node whose id is not in type-first form is a file problem
    Pins that every id a file gives is its own kind, the context path and a name, and that the bounded context's is bounded-context and the context path.
    Given a bounded context whose context path is ex.com/prod/ctx
    And <file> gives <node> the id <id>
    When `model check` is run
    Then it prints a file problem naming <file>

    Examples:
      | file                       | node                        | id                                     |
      | spec/index.md              | the bounded context         | ctx                                    |
      | spec/index.md              | the bounded context         | bounded-context/ctx                    |
      | spec/capabilities/thing.md | the capability              | thing                                  |
      | spec/capabilities/thing.md | the capability              | ctx/thing                              |
      | spec/capabilities/thing.md | the capability              | design-decision/ex.com/prod/ctx/thing  |
      | spec/decisions/0001-x.md      | the decision                | decision/x                             |
      | .shop/work/i1/initiative.md   | the initiative              | i1                                     |
      | .shop/work/i1/p1.md           | a work-item                 | capability-proposal/ex.com/prod/ctx/p1 |
      | .shop/records/observations.md | an observation, by heading, | obs-1                                  |
      | .shop/records/f1.md           | a review-finding            | f1                                     |

  @r24
  Scenario Outline: a reference in a refused form is unresolved
    Pins that the context-name form and the old decision/ and obs/ prefixes name nothing, even where a node of that name exists.
    Given a bounded context with id bounded-context/ex.com/prod/ctx, a capability thing with requirement r1, a decision x and an observation x
    And <file> whose <field> is written <reference>
    When `model check` is run
    Then <reference> is printed as unresolved

    Examples:
      | file                  | field    | reference    |
      | a capability-proposal | adds     | ctx/thing#r1 |
      | a capability-proposal | argues   | ctx/thing    |
      | a capability          | rests_on | decision/x   |
      | an initiative         | source   | obs/x        |

  @r48
  Scenario: a glossary bullet is a term of the bounded context
    Pins that a definition containing a period, as in "e.g. a", is one definition, split from its avoided words only at ". Not:".
    Given a bounded context whose glossary has the bullet "- **Suite record**: a whole-suite result, e.g. a green run, logged once. Not: test record, run."
    When `model facts` is run
    Then it prints the term term/ex.com/prod/ctx/suite-record
    And its avoided words are "test record" and "run", and nothing else

  @r49
  Scenario Outline: a glossary bullet not in the entry form is a file problem
    Given a bounded context whose glossary has the bullet <bullet>
    When `model check` is run
    Then it prints one file problem naming spec/index.md

    Examples:
      | bullet                                                   |
      | - batch: the slices one session plans.                   |
      | - **batch** the slices one session plans.                |
      | - **batch**: the slices one session plans                |
      | - **batch**: the slices one session plans. Not: sprint   |
      | - **batch**: . Not: sprint.                              |
      | - **batch**: the slices. Not: sprint, , lot.             |

  @r48
  Scenario: facts give each term its kind, its context and its avoided words
    Given a bounded context whose glossary defines batch, avoiding sprint and lot, and slice, avoiding nothing
    When `model facts` is run
    Then each term has a node fact of kind term and a term_of fact naming the bounded context
    And batch has an avoid fact for sprint and one for lot
    And slice has no avoid fact

  @r51
  Scenario: a mention is a whole word in any case, plural allowed
    Given a glossary term store that avoids shelf
    And requirements that say "the Store", "the stores", "restore" and "a shelf and a store-front"
    And a scenario whose steps say "a shelf" and another whose title says "the store"
    When `model facts` is run
    Then "the Store" and "the stores" each mention store
    And "restore" and "store-front" mention nothing
    And the requirement and the scenario saying "a shelf" each mention shelf

  @r52
  Scenario: a requirement or scenario using an avoided word is v_t1
    Given a glossary term slice that avoids chunk
    And a requirement that says "chunk", a scenario titled "chunks are planned" and a deprecated scenario titled "a chunk as it was"
    When `model check` is run
    Then v_t1 names the requirement, chunk and the term slice
    And v_t1 names the scenario, chunk and the term slice
    And v_t1 does not name the deprecated scenario

  @r53
  Scenario: two entries for one term are v_t2
    Given a glossary with an entry for slice and another for Slice
    When `model check` is run
    Then v_t2 names term/ex.com/prod/ctx/slice

  @r54
  Scenario: an avoided word that is a term is v_t3
    Given a glossary where slice avoids batch, batch is a term, and hand-back avoids Hand-back
    When `model check` is run
    Then v_t3 names batch and hand-back

  @r55
  Scenario: without clingo `model check` tries again under the first interpreter that has it
    Pins the order of the search and that the active virtualenv's bin/ is skipped.
    Given an interpreter that cannot import clingo
    And on PATH, in order, a virtualenv's python3 that has clingo, a python3 without it and two python3s with it
    When `model check` is run
    Then it asks the one without clingo, then the first with it, and tries again under that one
    And it never asks the virtualenv's python3 or the second with clingo
    But when $SHOPSYSTEM_MODEL_PYTHON names a python3 with clingo, it tries again under that one

  @r55
  Scenario: `model check` tries again only once
    Given an interpreter that cannot import clingo
    And a python3 on PATH that says it has clingo but runs `model check` without it
    When `model check` is run
    Then `model check` tries again under that python3 once

  @r12
  Scenario: with no interpreter that has clingo `model check` names each one it tried
    Given an interpreter that cannot import clingo
    And no python3 that can, whether PATH has none or $SHOPSYSTEM_MODEL_PYTHON and PATH name ones without it
    When `model check` is run
    Then it names clingo and pip install clingo
    And it names each interpreter it tried, /usr/local/bin/python3 and /usr/bin/python3 among them
    And it exits with an error

  @r36
  Scenario: a withdrawn part is closed
    Pins that withdrawn is a status of a capability-proposal and a work-item, and that it closes the part.
    Given a capability-change initiative with status `done`
    And under it a capability-proposal with status withdrawn, and under that a work-item with status withdrawn
    When `model check` is run
    Then no violation names the initiative

  @r59
  Scenario: an abandoned initiative with an open part is v_d2
    Given an abandoned capability-change initiative
    And under it a capability-proposal with status withdrawn, and under that a work-item with status drafted
    When `model check` is run
    Then v_d2 names the initiative
    And once the work-item is withdrawn too, no violation names the initiative

  @r3
  Scenario: a table row with an id is a requirement, and its header, separator and lead sentence are not
    Given a capability whose Behaviour has a ### heading, a lead sentence, and a table with a header row, a separator and rows marked [r1] and [r2]
    And a scenario tagged @r2
    When `model check` is run
    Then it prints no v15a

  @r103
  Scenario: a Behaviour line in none of EARS's patterns is v_e1
    Given a capability whose Behaviour has these lines
      | id | line                                                                                   |
      | r1 | **When** asked, `thing` shall answer.                                                  |
      | r2 | `thing` answers when asked.                                                            |
      | r3 | **If** asked, `thing` shall refuse.                                                    |
      | r4 | **When** asked, **Where** configured, `thing` shall answer.                            |
      | r5 | **Where** configured, **While** idle, **When** asked, `thing` shall answer.            |
      | r6 | **If** asked, then `thing` shall answer.                                               |
      | r7 | **If** asked, then **When** idle, `thing` shall answer.                                |
      | r8 | when asked, `thing` shall answer.                                                      |
      | r9 | Sometimes `thing` shall answer.                                                        |
    When `model check` is run
    Then v_e1 names r2, r3, r4, r7, r8 and r9
    And v_e1 does not name r1, r5 or r6

  @r103
  Scenario: a table row is judged by its lead sentence
    Given a capability whose Behaviour has a table with rows marked [r1] and [r2], led by a sentence that names no system
    When `model check` is run
    Then v_e1 names r1 and r2

  @r104
  Scenario: a Behaviour line with two shalls or two sentences is v_e2
    Given a capability whose Behaviour has these lines
      | id | line                                                                         |
      | r1 | **When** asked, `thing` shall answer.                                        |
      | r2 | **When** asked, `thing` shall answer and `thing` shall log.                  |
      | r3 | **When** asked, `thing` shall answer. It is quick.                           |
      | r4 | **When** asked, `thing` shall read `a.b` and say "so. it is."                |
      | r5 | **When** asked, `thing` shall answer, e.g. with a value.                     |
      | r6 | `thing` answers when asked.                                                  |
    When `model check` is run
    Then v_e2 names r2 and r3
    And v_e2 does not name r1, r4, r5 or r6

  @r5
  Scenario: a merged capability-proposal adding an id its capability lists as retired is not v15c
    Pins that a settled proposal may name a retired id, as a proposal that is not settled may not.
    Given a capability thing with requirement r1 that lists r4 as retired
    And a merged capability-proposal that adds thing#r4
    When `model check` is run
    Then thing#r4 is not printed under v15c

  @r23
  Scenario: a merged capability-proposal may add or remove an id its capability lists as retired
    Pins that a settled proposal's retired id, added or removed, is read as that requirement and not as unresolved.
    Given a capability thing with requirement r1 that lists r4 as retired
    And a merged capability-proposal that adds thing#r4 and removes thing#r4
    When `model check` is run
    Then thing#r4 is not printed as unresolved

  @r107
  Scenario Outline: a scenario with more than one requirement tag, its own and its feature's together, is v_s2
    Pins that a scenario names one requirement, wherever its tags sit, and that a deprecated scenario names none.
    Given a capability thing with requirements r1 and r2
    And in features/thing.feature a scenario <tagged>
    When `model check` is run
    Then the scenario is <printed> under v_s2

    Examples:
      | tagged                                  | printed     |
      | tagged @r1 @r2                          | printed     |
      | tagged @r1, in a feature tagged @r2     | printed     |
      | tagged @r1                              | not printed |
      | tagged @r1 @r2 @deprecated              | not printed |

  @r106
  Scenario Outline: a work-item with no accepts and no check is v_w4, unless it is withdrawn
    Pins that a work-item says how its work is shown complete.
    Given a capability thing with requirement r1 that a scenario names
    And a work-item w1 in .shop/work/i1/ with status <status>, <fields>
    When `model check` is run
    Then w1 is <printed> under v_w4

    Examples:
      | status    | fields                          | printed     |
      | drafted   | no accepts and no check         | printed     |
      | withdrawn | no accepts and no check         | not printed |
      | drafted   | accepts thing#r1 and no check   | not printed |
      | drafted   | a check and no accepts          | not printed |

  @r106
  Scenario: a work-item accepting a requirement no scenario names yet, with no check, is not v_w4
    Pins that a work-item's accepts counts toward saying how its work is shown complete, whether or not a scenario names the requirement yet.
    Given a capability thing with requirement r2 that no scenario names
    And a work-item w1 in .shop/work/i1/ with status drafted, accepts thing#r2 and no check
    When `model check` is run
    Then w1 is not printed under v_w4

  @r51
  Scenario: a code span, a double-quoted string and a tag are no mention
    Given a glossary term store that avoids shelf
    And a capability whose Behaviour has these lines
      | id | line                                       |
      | r1 | The `shelf` shall stay.                    |
      | r2 | The thing shall say "a shelf".             |
      | r3 | The thing shall name the tag @shelf.       |
      | r4 | The thing shall keep a shelf.              |
    When `model facts` is run
    Then only r4 mentions shelf

  @r3
  Scenario: a table row whose id lost its brackets is a line with no id
    Given a capability whose Behaviour has a table whose row is marked r1 without brackets
    When `model check` is run
    Then the output names v15a

  @r103
  Scenario: a table is led only by the sentence just before it
    Given a capability whose Behaviour has a table led by a good sentence, a ### heading, and a second table with a row marked [r2] and no lead
    When `model check` is run
    Then v_e1 names r2
    And v_e1 does not name r1

  @r108
  Scenario: `model why --json` prints the requirement's text and its proposals as one JSON object
    Pins that why's answer can be read by a program, each proposal with its status and date.
    Given a capability thing with requirement r2
    And a capability-proposal p1 dated 2026-09-01 that adds thing#r2
    When `model why --json` is run for thing#r2
    Then it prints one JSON object
    And the object gives the requirement's text and p1 with its status and date

  @r65
  Scenario: `model rules` prints every rule with its plain label
    Given any repository
    When `model rules` is run
    Then it prints each rule's code and plain label, one a line, the violations first and then the warnings
    And it exits successfully

  @r109
  Scenario: `model rules --json` prints every rule's code, plain label and kind as one JSON object
    Pins that the rules can be read by a program, each telling whether it is a violation or a warning.
    Given any repository
    When `model rules --json` is run
    Then it prints one JSON object
    And the object gives each rule that `model rules` prints with its code, its plain label and its kind, violation or warning

  @r14
  Scenario: the decisions index is written when there is no decision yet
    Pins that a repository with no spec/decisions/ directory still gets its index, with no row.
    Given a repository with no spec/decisions/
    When `model decisions` is run
    Then spec/decisions/index.md is written with its header and no row

  @r113
  Scenario: an initiative dated after 2026-10-23 that fulfils no request is v16a
    Pins that from 2026-10-24 on every initiative fulfils a request, and that one dated on or before 2026-10-23 need not.
    Given an initiative i1 dated 2026-10-24 that fulfils no request
    And an initiative i2 dated 2026-10-23 that fulfils no request
    And an initiative i3 dated 2026-10-24 that fulfils the request q1
    When `model check` is run
    Then v16a names i1
    And v16a does not name i2 or i3

  @r114
  Scenario Outline: a done initiative whose own request in this context is not delivered is v_d1
    Pins that an initiative is done only once each request this context raised to itself under it is delivered.
    Given an initiative i1 with status done
    And a request q1 in .shop/work/requests/q1.md whose asker is <asker>, whose <field> names i1, with status <status>
    When `model check` is run
    Then v_d1 <names> i1

    Examples:
      | asker           | field   | status    | names         |
      | this context    | source  | open      | names         |
      | this context    | part_of | accepted  | names         |
      | this context    | source  | delivered | does not name |
      | this context    | part_of | delivered | does not name |
      | another context | source  | open      | does not name |

  @r119
  Scenario: a delivered request whose initiative is not done is v_d3
    Pins that a request is delivered only while the initiative that fulfils it is done.
    Given a delivered request q1
    And an initiative i1 with status started that fulfils q1
    When `model check` is run
    Then v_d3 names q1
    And once i1 is done, v_d3 does not name q1

  @r115
  Scenario: a request that is part of no job-thread and cites no origin is v17
    Pins that every request says where it comes from.
    Given a request q1 that is part of no job-thread and cites no origin
    And a request q2 that cites an observation as its origin
    When `model check` is run
    Then v17 names q1
    And v17 does not name q2

  @r116
  Scenario: a delivered request whose resolution names a requirement the spec does not have is v3
    Pins that a resolution names only requirements the spec has.
    Given a capability thing with requirement r1 and no requirement r9
    And a delivered request q1 whose resolution names thing#r9
    And a delivered request q2 whose resolution names thing#r1
    When `model check` is run
    Then v3 names q1 and thing#r9
    And v3 does not name q2

  @r117
  Scenario Outline: an id of a kind kept in .shop/work/ with another context's path is v18
    Pins that this context's files name work only of their own context, judged from the id whether or not anything in the repository has it.
    Given a repository whose bounded context is bounded-context/missingmass.io/shopsystem/shopsystem-bdd
    And an initiative i1 whose source names <id>
    And nothing in the repository has the id <id>
    When `model check` is run
    Then v18 <names> <id>

    Examples:
      | id                                                      | names         |
      | request/missingmass.io/shopsystem/other/q3              | names         |
      | initiative/missingmass.io/shopsystem/other/i2           | names         |
      | capability-proposal/missingmass.io/shopsystem/other/p1  | names         |
      | work-item/missingmass.io/shopsystem/other/w4            | names         |
      | observation/missingmass.io/shopsystem/other/2026-10-01-x | does not name |
      | request/missingmass.io/shopsystem/shopsystem-bdd/q3     | does not name |

  @r112
  Scenario: a request not of the form `work request` writes is a file problem
    Pins that `model check` reads a request only in the form `work request` gives it.
    Given a request in .shop/work/requests/q1.md with no asker
    And a request in .shop/work/requests/q2.md that `work request` wrote
    When `model check` is run
    Then it prints a file problem naming .shop/work/requests/q1.md
    And it prints no file problem naming .shop/work/requests/q2.md

  @r118
  Scenario Outline: an initiative of kind job or job-path is a file problem
    Pins that job and job-path are not kinds an initiative may have.
    Given a repository with an initiative in .shop/work/i1/initiative.md of kind <kind>
    When `model check` is run
    Then it <prints> a file problem naming .shop/work/i1/initiative.md

    Examples:
      | kind              | prints         |
      | job               | prints         |
      | job-path          | prints         |
      | capability-change | does not print |
