# formulated from spec/capabilities/design-model-check.md
Feature: Design model check
  Narrator: a person or agent checking a repository against the design model

  @r1
  Scenario: a repository the grammar accepts passes
    Given a bounded context with one capability whose requirement r1 has a scenario tagged @r1
    When model check is run
    Then it reports 0 violations, 0 unresolved references and 0 file problems
    And it exits 0

  @r2
  Scenario: violations are printed by their grammar name and fail the check
    Given a bounded context with a requirement no scenario names
    When model check is run
    Then the output names v_s3 with the requirement's id
    And it exits 1

  @r3
  Scenario: a requirement bullet without an id is refused
    Given a capability whose Behaviour has a bullet with no [r<n>]
    When model check is run
    Then the output names v15a

  @r4
  Scenario: two requirements with one id are refused
    Given a capability whose Behaviour has two bullets marked [r1]
    When model check is run
    Then the output names v15b

  @r5
  Scenario: a retired id used again is refused
    Given a capability that lists r1 as retired and has a requirement [r1]
    When model check is run
    Then the output names v15c

  @r6
  Scenario: a proposal changing a requirement no capability has is refused
    Given a capability-proposal that changes r9 of a capability with no r9
    When model check is run
    Then the output names v15e with the proposal and the requirement

  @r7
  Scenario: a proposal formulated before its requirement has a scenario is refused
    Given a capability-proposal with status formulated that adds a requirement no scenario names
    When model check is run
    Then the output names v15f with the proposal

  @r8
  Scenario: a guarantees capability needs no scenarios
    Given a capability in the guarantees group whose requirements no scenario names
    When model check is run
    Then the output does not name v_s3

  @r9
  Scenario: references that name nothing are reported
    Given a scenario tagged @r7 in a capability with no r7, and a capability resting on a decision that does not exist
    When model check is run
    Then each is reported as unresolved
    And it exits 1

  @r10
  Scenario: a part that reaches no initiative is refused
    Given a work-item whose part_of names nothing
    When model check is run
    Then the output names v9c with the work-item

  @r11
  Scenario: warnings are counted and do not fail the check
    Given a bounded context the grammar accepts, with an observation no initiative cites
    When model check is run
    Then the output gives w_uncited_obs with its count
    And it exits 0

  @r12
  Scenario: without clingo the check says how to install it
    Given an interpreter without the clingo package
    When model check is run
    Then it names clingo and the pip command that installs it
    And it exits 2

  @r13
  Scenario: facts are printed in clingo's syntax
    Given a bounded context with one capability
    When model facts is run
    Then each line is one fact, such as a node fact for the capability

  @r14
  Scenario: the decisions index lists every decision
    Given two decisions under decisions/, one superseding the other
    When model decisions is run
    Then spec/decisions.md has a row for each with its summary, status and what it supersedes

  @r15
  Scenario: a stale decisions index is reported and left alone
    Given a spec/decisions.md that differs from what model decisions writes
    When model decisions --check is run
    Then it says the file is not current, exits 1, and the file is unchanged

  @r16
  Scenario: why traces a requirement to its initiative's sources
    Given an initiative citing an observation, with a capability-proposal that adds r1
    When model why is run for that requirement
    Then it prints the requirement, the proposal, the initiative and the observation

  @r17
  Scenario: why with no proposal says so
    Given a requirement no capability-proposal adds or changes
    When model why is run for it
    Then it says no capability-proposal adds or changes it
    And it exits 1

  @r18
  Scenario: a range of ids stands for each id in it
    Given a capability-proposal that adds thing#r1-r3
    When model why is run for thing#r2
    Then it prints the proposal as adding it

  @r19
  Scenario Outline: model reads the repository's files under its root
    Pins which files of a repository model reads, and that the root is the current directory unless --root names one.
    Given a repository in a directory holding <file>
    When model facts is run <how>
    Then the facts printed <outcome> what <file> holds

    Examples:
      | file                               | how                                   | outcome         |
      | spec/index.md                      | with --root naming that directory     | include         |
      | spec/capabilities/thing.md         | with --root naming that directory     | include         |
      | features/sub/thing.feature         | with --root naming that directory     | include         |
      | decisions/0001-one.md              | with --root naming that directory     | include         |
      | work/i1/initiative.md              | with --root naming that directory     | include         |
      | records/observations.md            | with --root naming that directory     | include         |
      | records/review/f1.md with an id    | with --root naming that directory     | include         |
      | records/review/f2.md with no id    | with --root naming that directory     | do not include  |
      | spec/capabilities/thing.md         | from that directory with no --root    | include         |

  @r20
  Scenario Outline: a scenario names a requirement by its tag in its capability's feature file
    Pins where an @r<n> tag may sit, and which feature file a capability's scenarios are read from.
    Given a capability thing with requirement r2, <formulated as>
    And a scenario in <feature file> with the tag @r2 <placed>
    When model check is run
    Then the requirement thing#r2 is <reported> under v_s3

    Examples:
      | formulated as                                  | feature file              | placed                  | reported |
      | formulated_as features/thing.feature           | features/thing.feature    | on the scenario         | not      |
      | formulated_as features/thing.feature           | features/thing.feature    | on its feature          | not      |
      | giving no formulated_as                        | features/thing.feature    | on the scenario         | not      |
      | formulated_as features/sub/thing-flow.feature  | features/sub/thing-flow.feature | on the scenario   | not      |
      | formulated_as features/sub/thing-flow.feature  | features/other.feature    | on the scenario         | still    |

  @r21
  Scenario: a reference written name#r<n> is that capability's requirement
    Pins that the part before # is the capability's name in this bounded context and the part after it the requirement's id.
    Given a bounded context with id bounded-context/ex.com/prod/ctx and a capability thing with requirement r2
    And a capability-proposal that adds thing#r2
    When model why is run for capability/thing#r2
    Then it prints capability/ex.com/prod/ctx/thing#r2 with its text and the proposal as adding it

  @r22
  Scenario Outline: a reference in neither requirement form, or a reversed range, is unresolved
    Pins the forms a requirement reference in a list may take.
    Given a capability thing with requirements r1 to r3
    And a capability-proposal whose list names <reference>
    When model check is run
    Then <reference> is reported as unresolved

    Examples:
      | reference                |
      | thing                    |
      | thing#2                  |
      | thing#line2              |
      | thing#r3-r1              |
      | design-decision/thing#r1 |

  @r23
  Scenario Outline: a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id
    Pins that an absent requirement is an unresolved reference whether added or removed, and that adding a retired id is a v15c instead.
    Given a capability thing with requirement r1 that lists r4 as retired
    And a capability-proposal that <change> thing#<id>
    When model check is run
    Then thing#<id> is <reported>

    Examples:
      | change  | id | reported                                  |
      | adds    | r9 | reported as unresolved                    |
      | removes | r9 | reported as unresolved                    |
      | adds    | r4 | reported under v15c and not as unresolved |
      | removes | r4 | reported as unresolved                    |

  @r24
  Scenario Outline: a frontmatter reference to nothing, or to the wrong kind, is unresolved
    Pins that each named frontmatter reference must reach a node, and that supersedes, under, for, blocked_by and depends_on must reach a node of the kind they need.
    Given a file whose <field> names <target>
    When model check is run
    Then that <field> is reported as unresolved

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
    When model check is run
    Then it reports a file problem naming <file>

    Examples:
      | case                                                                      | file                       |
      | spec/index.md is missing                                                  | spec/index.md              |
      | spec/index.md has no id                                                   | spec/index.md              |
      | spec/capabilities/thing.md has the id capability/acme.com/shop/cart/other | spec/capabilities/thing.md |
      | spec/capabilities/thing.md has no ## Behaviour section                    | spec/capabilities/thing.md |
      | spec/capabilities/thing.md lists retired: [three]                         | spec/capabilities/thing.md |

  @r26
  Scenario Outline: a feature file no capability is formulated as, or with a title twice, is a file problem
    Pins which feature files belong to a capability, and that titles are unique among the scenarios not held.
    Given a capability thing, <formulated as>
    And a feature file <file> in which <titles>
    When model check is run
    Then it <reports> a file problem naming <file>

    Examples:
      | formulated as                                  | file                   | titles                                                                     | reports         |
      | formulated_as features/thing.feature           | features/stray.feature | every scenario has its own title                                           | reports         |
      | giving no formulated_as                        | features/thing.feature | every scenario has its own title                                           | does not report |
      | formulated_as features/sub/thing-flow.feature  | features/thing.feature | every scenario has its own title                                           | reports         |
      | formulated_as features/thing.feature           | features/thing.feature | two scenarios are titled "Apply a code"                                    | reports         |
      | formulated_as features/thing.feature           | features/thing.feature | two scenarios are titled "Apply a code" and one of them is tagged @holding | does not report |

  @r27
  Scenario Outline: a malformed work directory or work file is a file problem
    Pins the shape each initiative and part file must have, and that a missing initiative.md is charged to its directory.
    Given a repository with a work directory work/i1 in which <case>
    When model check is run
    Then it reports a file problem naming <named>

    Examples:
      | case                                                  | named                                     |
      | there is no initiative.md                             | work/i1, and not work/i1/initiative.md    |
      | initiative.md has no id                               | work/i1/initiative.md                     |
      | the part p1.md has no id                              | work/i1/p1.md                             |
      | the part p1.md has the kind banana                    | work/i1/p1.md                             |
      | the part p1.md has no status                          | work/i1/p1.md                             |
      | the part p1.md has a status not in its kind's lifecycle | work/i1/p1.md                           |
      | initiative.md has the priority high                   | work/i1/initiative.md                     |
      | initiative.md has a date written 16/10/2026           | work/i1/initiative.md                     |

  @r28
  Scenario: a work-item accepting a requirement no scenario names is a file problem
    Pins that a work-item may accept only requirements a scenario already names.
    Given a capability thing with requirement r2 that no scenario names
    And a work-item in work/i1/w1.md that accepts thing#r2
    When model check is run
    Then it reports a file problem naming work/i1/w1.md

  @r29
  Scenario Outline: a malformed decision, record or frontmatter is a file problem
    Pins the frontmatter faults in decisions, records and shared ids that model check refuses.
    Given a repository in which <case>
    When model check is run
    Then it reports a file problem

    Examples:
      | case                                                         |
      | a decision under decisions/ has no id                        |
      | a record under records/ with an id has the kind banana       |
      | a frontmatter value is written as a folded block, with >     |
      | a frontmatter value is written as a literal block, with \|   |
      | a decision and an observation have the same id               |

  @r30
  Scenario: file problems are each printed and fail the check
    Pins that every file problem is shown and that any one of them fails the check.
    Given a repository with two capabilities that each have no ## Behaviour section
    When model check is run
    Then it prints a file problem for each of the two capabilities
    And it exits 1

  @r31
  Scenario: the check ends with the four counts
    Pins the summary every plain-text check ends with.
    Given a repository with one violation, one warning, one unresolved reference and one file problem
    When model check is run without --json
    Then it prints the four counts, each 1

  @r32
  Scenario Outline: rows of a violated relation are limited, saying how many more there are
    Pins the row limit per violated relation, given or by default.
    Given a repository with <rows> requirements no scenario names
    When model check is run <limit>
    Then it prints <shown> rows under v_s3
    And it says there are <more> more

    Examples:
      | rows | limit           | shown | more |
      | 5    | with --limit 2  | 2     | 3    |
      | 12   | with no --limit | 10    | 2    |

  @r33
  Scenario Outline: with --json the check's findings are one JSON object
    Pins the machine-readable output and that it does not change the exit status.
    Given a repository <state>
    When model check is run with --json
    Then it prints one JSON object holding the violations, warnings, unresolved references and file problems
    And it exits <status>

    Examples:
      | state                                  | status |
      | the grammar accepts                    | 0      |
      | with a requirement no scenario names   | 1      |

  @r34
  Scenario Outline: only a capability-change initiative may hold several parts directly
    Pins that an initiative holds one part directly, except a capability-change holding capability-proposals.
    Given <initiative> with <parts> directly under it
    When model check is run
    Then the initiative is <reported> under v_k5

    Examples:
      | initiative                                   | parts                    | reported |
      | an initiative that is not a capability-change | two parts                | reported |
      | a capability-change initiative               | two capability-proposals | not reported |

  @r35
  Scenario: a proposal arguing two capabilities is refused
    Pins that a capability-proposal argues one capability.
    Given capabilities thing and other
    And a capability-proposal that argues both thing and other
    When model check is run
    Then the output names v_k6 with the proposal

  @r36
  Scenario: an initiative may be done when its proposal is formulated
    Pins that formulated is a closed status for a capability-proposal under a done initiative.
    Given a capability-change initiative with status done
    And under it a capability-proposal with status formulated, whose requirements scenarios name
    When model check is run
    Then no violation names the initiative

  @r37
  Scenario: a current decisions index passes the check
    Pins the passing outcome of the decisions index check.
    Given a spec/decisions.md that is what model decisions writes
    When model decisions --check is run
    Then it says the file is current
    And it exits 0

  @r38
  Scenario: writing the decisions index names the file and leaves out decisions with no id
    Pins what writing the index reports and that only decisions with an id are indexed.
    Given two decisions under decisions/, one of them with no id
    When model decisions is run
    Then it prints spec/decisions.md as the file it wrote
    And spec/decisions.md lists the decision with an id and not the one without

  @r39
  Scenario: why refuses an argument that is not a requirement reference
    Pins that model why takes only a requirement reference.
    Given a capability thing
    When model why is run for thing
    Then it is refused because thing is not a requirement reference
    And it exits 2

  @r40
  Scenario: why on a requirement no capability has still lists its proposals
    Pins that a missing requirement does not hide the proposals that name it.
    Given a capability thing with no requirement r9
    And a capability-proposal that changes thing#r9
    When model why is run for thing#r9
    Then it says no capability has thing#r9 where the requirement's text would be
    And it lists the proposal

  @r41
  Scenario Outline: why lists every proposal naming the requirement by date, and fails when none adds or changes it
    Pins that removing proposals are listed too, in date order with status and date, but only one that adds or changes the requirement makes why succeed.
    Given a capability thing with requirement r2
    And <proposals>
    When model why is run for thing#r2
    Then it lists <listed>, in that order, each with its status and date
    And it exits <status>

    Examples:
      | proposals                                                                                                   | listed      | status |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that adds thing#r2    | p2 then p1  | 0      |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that changes thing#r2 | p2 then p1  | 0      |
      | a capability-proposal p1 dated 2026-10-01 that removes thing#r2 and a capability-proposal p2 dated 2026-09-01 that removes thing#r2 | p2 then p1  | 1      |
      | only a capability-proposal p1 dated 2026-10-01 that removes thing#r2                                        | p1          | 1      |

  @r42
  Scenario: the behaviour/ form of a reference names the same requirement
    Pins that #behaviour/r<n> and #r<n> are one requirement.
    Given a bounded context with id bounded-context/ex.com/prod/ctx and a capability thing with requirement r2
    And a capability-proposal that adds capability/ex.com/prod/ctx/thing#behaviour/r2
    When model why is run for capability/ex.com/prod/ctx/thing#r2
    Then it prints the proposal as adding it

  @r43
  Scenario Outline: a node may be written in short where its field allows it
    Pins that the kind-and-name short form is read in any field, and the bare name only in a field that fixes the kind.
    Given a bounded context with id bounded-context/ex.com/prod/ctx, a capability thing and an initiative i1
    And a capability-proposal whose <field> is written <written>
    When model check is run
    Then <written> is <outcome>

    Examples:
      | field   | written                          | outcome                                                                 |
      | argues  | thing                            | read as capability/ex.com/prod/ctx/thing and not reported as unresolved |
      | argues  | capability/thing                 | read as capability/ex.com/prod/ctx/thing and not reported as unresolved |
      | argues  | capability/ex.com/prod/ctx/thing | read as capability/ex.com/prod/ctx/thing and not reported as unresolved |
      | part_of | initiative/i1                    | read as initiative/ex.com/prod/ctx/i1 and not reported as unresolved    |
      | part_of | i1                               | reported as unresolved                                                  |

  @r44
  Scenario: a held scenario names no requirement
    Pins that a scenario tagged @holding does not count as a requirement's acceptance-scenario.
    Given a capability thing with requirement r2
    And its only scenario tagged @r2 is also tagged @holding
    When model check is run
    Then the requirement thing#r2 is reported under v_s3

  @r45
  Scenario: without a decisions directory the ledger's design-decision headings are the decisions
    Pins where decisions and their summaries come from in a repository that keeps them only in spec/decisions.md.
    Given a repository with no decisions/ directory
    And a spec/decisions.md with the heading ## design-decision/one, a line of text below it, and a date: line after that
    And a capability that rests on design-decision/one
    When model check is run
    Then design-decision/one is not reported as unresolved
    And that line of text is read as the decision's summary

  @r46
  Scenario Outline: a node whose id is not in type-first form is a file problem
    Pins that every id a file gives is its own kind, the context path and a name, and that the bounded context's is bounded-context and the context path.
    Given a bounded context whose context path is ex.com/prod/ctx
    And <file> gives <node> the id <id>
    When model check is run
    Then it reports a file problem naming <file>

    Examples:
      | file                       | node                        | id                                     |
      | spec/index.md              | the bounded context         | ctx                                    |
      | spec/index.md              | the bounded context         | bounded-context/ctx                    |
      | spec/capabilities/thing.md | the capability              | thing                                  |
      | spec/capabilities/thing.md | the capability              | ctx/thing                              |
      | spec/capabilities/thing.md | the capability              | design-decision/ex.com/prod/ctx/thing  |
      | decisions/0001-x.md        | the decision                | decision/x                             |
      | work/i1/initiative.md      | the initiative              | i1                                     |
      | work/i1/p1.md              | a work-item                 | capability-proposal/ex.com/prod/ctx/p1 |
      | records/observations.md    | an observation, by heading, | obs-1                                  |
      | records/f1.md              | a review-finding            | f1                                     |

  @r47
  Scenario Outline: a reference in a refused form is unresolved
    Pins that the context-name form and the old decision/ and obs/ prefixes name nothing, even where a node of that name exists.
    Given a bounded context with id bounded-context/ex.com/prod/ctx, a capability thing with requirement r1, a decision x and an observation x
    And <file> whose <field> is written <reference>
    When model check is run
    Then <reference> is reported as unresolved

    Examples:
      | file                  | field    | reference    |
      | a capability-proposal | adds     | ctx/thing#r1 |
      | a capability-proposal | argues   | ctx/thing    |
      | a capability          | rests_on | decision/x   |
      | an initiative         | source   | obs/x        |
