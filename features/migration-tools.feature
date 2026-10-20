# formulated from spec/capabilities/migration-tools.md
Feature: Migration tools
  Narrator: a person or session migrating a repository to the final layout

  @r1
  Scenario: run moves decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git
    Pins where each of these old directories lands, keeping a record's path, and that git sees each move as a rename.
    Given a repository on the old system with decisions/0001-d0.md, work/i1/w1.md and records/logs/r1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0001-d0.md has the content decisions/0001-d0.md had, apart from the id r9 gives it
    And .shop/work/i1/w1.md has the content work/i1/w1.md had
    And .shop/records/logs/r1.md has the content records/logs/r1.md had, apart from any id r9 and about r12 give it
    And decisions/, work/ and records/ are gone
    And git status shows each of the three as renamed

  @r1
  Scenario: run moves a file under records/ that is not text as it is
    Pins that a file that is not text, such as an image, moves like any other.
    Given a repository on the old system with records/img/a.png, which is not text
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/img/a.png is records/img/a.png as it was, byte for byte
    And records/img/a.png is gone

  @r2 @r11
  Scenario: run replaces a ledger that has only entries with a decision file for each, named by its heading, with its first paragraph, accepted, with its date and source
    Pins the file a ledger entry becomes, where each of its fields comes from, and that a ledger of nothing but entries is gone.
    Given a repository on the old system whose spec/decisions.md has nothing but the entry `## decision/0007-a`
    And the entry is dated 2025-03-01, its source is alice, and its first paragraph is "We do a."
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions.md is gone
    And spec/decisions/0007-a.md has the summary "We do a." and its Decision has "We do a."
    And its status is accepted, its date is 2025-03-01 and its by is alice

  @r2
  Scenario: run ends an entry's first paragraph at its date or source line, with or without a blank line before it
    Pins that an entry's first paragraph ends at the first blank line or the first `date:` or `source:` line.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a`, its first paragraph "We do a." followed with no blank line by its date 2025-03-01 and its source alice
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md has the summary "We do a."
    And its date is 2025-03-01 and its by is alice

  @r2
  Scenario Outline: run writes a first paragraph and a source that hold <what> so that model reads them as they are
    Pins that a decision file's summary and by are the entry's own text, whatever its punctuation.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a`, its first paragraph <paragraph> and its source <source>
    When the session runs `migrate run --context example.org/acme/shop`
    Then model reads spec/decisions/0007-a.md's summary as <paragraph> and its by as <source>

    Examples:
      | what                  | paragraph                    | source      |
      | a leading [ and a #   | [Scripts] read: one #1 form. | alice #2    |
      | double quotes and a # | We do "a" #1, not "b".       | "bob" #3    |
      | single quotes and a # | It's Bob's #1 form.          | o'neil's #4 |

  @r2
  Scenario: run puts an entry's whole text in its decision file's Decision, its first paragraph also being its summary
    Pins that no text of an entry is lost when the ledger goes.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a` with the paragraphs "We do a." and "Because b."
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md has the summary "We do a."
    And its Decision has "We do a." and then "Because b."

  @r2 @r5
  Scenario: run gives a decision file its entry's supersedes and revisit_when
    Pins that an entry's supersedes and revisit_when are kept, a superseded entry named by its new id.
    Given a repository on the old system whose spec/decisions.md has the entries `## decision/0003-b` and `## decision/0007-a`
    And the entry 0007-a has supersedes: decision/0003-b and revisit_when: b comes back
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md's supersedes is design-decision/example.org/acme/shop/b and its revisit_when is "b comes back"

  @r2 @r11
  Scenario: run replaces a ledger that holds a title and its entries
    Pins that a ledger holding nothing but a title and its entries is gone once its every entry is replaced.
    Given a repository on the old system whose spec/decisions.md starts with the title `# Decisions` and a blank line, then the entry `## decision/0007-a`
    And the entry's first paragraph is "We do a."
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions.md is gone
    And spec/decisions/0007-a.md has the summary "We do a."

  @r7 @r11
  Scenario Outline: run that finds <found> in spec/decisions.md names it, exits non-zero and changes no file, the ledger included
    Pins that a ledger heading migrate cannot replace, or ledger text that is neither an entry nor its title, stops the run.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a` and <found>
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not replace <named>
    And it exits non-zero
    And nothing under the repository has changed

    Examples:
      | found                                     | named                                                       |
      | after it the heading `## decision/b`      | the ledger entry `## decision/b`                            |
      | before it the text "Notes on the ledger." | the ledger text "Notes on the ledger." outside its entries  |
      | after it the heading `## decision/0007-a` | the ledger entry `## decision/0007-a`, which is there twice |

  @r7
  Scenario Outline: run whose ledger entry's decision file would land on <there> names it, exits non-zero and changes no file
    Pins that the decision file migrate writes for a ledger entry never takes the place of a file that is there or moves there.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a`, and <there>
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not write spec/decisions/0007-a.md for the ledger entry `## decision/0007-a`
    And it exits non-zero
    And nothing under the repository has changed

    Examples:
      | there                                                        |
      | decisions/0007-a.md, which moves to spec/decisions/0007-a.md |
      | a tracked spec/decisions/0007-a.md                           |
      | an untracked spec/decisions/0007-a.md                        |

  @r3
  Scenario: run deprecates a @holding scenario as `features deprecate` does
    Pins that migrate leaves a @holding scenario, and the tests that name it, as `features deprecate` would.
    Given a repository on the old system whose features/thing.feature has a scenario "s1" tagged @holding
    And a test that names "s1" by title
    And a copy of that repository on which `features deprecate` has been run for "s1"
    When the session runs `migrate run --context example.org/acme/shop` on the repository
    Then features/thing.feature and the test are as they are in the copy

  @r4
  Scenario: run gives spec/index.md the id bounded-context/<path>
    Pins that the path given to --context is the one the context's id carries.
    Given a repository on the old system whose spec/index.md gives no id
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/index.md gives the id bounded-context/example.org/acme/shop

  @r5
  Scenario: run rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it moved or renamed
    Pins each of the three kinds of reference run rewrites in a tracked text file.
    Given a repository on the old system with work/i1/w1.md
    And a tracked README.md that names work/i1/w1.md
    And a tracked notes/n1.md with the Markdown link `[w1](../work/i1/w1.md)`
    And its spec/decisions.md has the entry `## decision/0007-a`
    And a capability spec/capabilities/thing.md whose frontmatter rests_on names decision/0007-a
    When the session runs `migrate run --context example.org/acme/shop`
    Then README.md names .shop/work/i1/w1.md where it named work/i1/w1.md
    And notes/n1.md has the link `[w1](../.shop/work/i1/w1.md)`
    And spec/capabilities/thing.md's rests_on names design-decision/example.org/acme/shop/a

  @r6
  Scenario: after run, model check reports no violation, unresolved reference or file problem
    Pins that a repository run through migrate passes model check.
    Given a repository on the old system with decisions/, work/, records/, docs/superpowers/plans/, docs/superpowers/specs/, a ledger spec/decisions.md, a capability and a @holding scenario
    And the session has run `migrate run --context example.org/acme/shop`
    When the session runs `model check`
    Then it reports no violation, no unresolved reference and no file problem

  @r7
  Scenario: run that cannot make two of its changes names both, exits non-zero and changes no file
    Pins that run is all or nothing, and names each change it could not make rather than the first.
    Given a repository on the old system with work/i1/w1.md, and .shop/work/i1/w1.md already exists
    And it has records/archive/plans/p1.md and docs/superpowers/plans/p1.md, which both move to .shop/records/archive/plans/p1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not move work/i1/w1.md onto .shop/work/i1/w1.md
    And it says it could not move both records/archive/plans/p1.md and docs/superpowers/plans/p1.md to .shop/records/archive/plans/p1.md
    And it exits non-zero
    And nothing under the repository has changed

  @r7
  Scenario: run that would move a file onto an untracked file names the move, exits non-zero and changes no file
    Pins that a file already there stops a move onto it whether or not git tracks it.
    Given a repository on the old system with work/i1/w1.md and work/i1/w2.md, and an untracked .shop/work/i1/w2.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not move work/i1/w2.md onto .shop/work/i1/w2.md
    And it exits non-zero
    And nothing under the repository has changed

  @r8
  Scenario: run moves docs/superpowers/plans/ and docs/superpowers/specs/ under .shop/records/archive/, with git
    Pins where plans and design notes land, and that git sees each move as a rename.
    Given a repository on the old system with docs/superpowers/plans/p1.md and docs/superpowers/specs/s1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/archive/plans/p1.md has the content docs/superpowers/plans/p1.md had, apart from the id r9 and the about r12 give it
    And .shop/records/archive/design-notes/s1.md has the content docs/superpowers/specs/s1.md had, apart from the id r9 and the about r12 give it
    And docs/superpowers/plans/ and docs/superpowers/specs/ are gone
    And git status shows each of the two as renamed

  @r9
  Scenario: run gives a capability, a decision file, a plan, a design note and a test log the type-first id of its kind
    Pins the id each kind gets, as <kind>/<context path>/<name>, the name being the file's stem.
    Given a repository on the old system with a capability spec/capabilities/thing.md with no id
    And its spec/decisions.md has the entry `## decision/0007-a`
    And it has docs/superpowers/plans/p1.md, docs/superpowers/specs/s1.md and records/logs/run1-test-log.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/capabilities/thing.md gives the id capability/example.org/acme/shop/thing
    And spec/decisions/0007-a.md gives the id design-decision/example.org/acme/shop/a
    And .shop/records/archive/plans/p1.md gives the id initiative-archive/example.org/acme/shop/p1
    And .shop/records/archive/design-notes/s1.md gives the id decision-argument/example.org/acme/shop/s1
    And .shop/records/logs/run1-test-log.md gives the id measurement/example.org/acme/shop/run1-test-log

  @r10
  Scenario: run numbers each Behaviour line with no id, in Behaviour order, from one above the highest id its capability has ever used
    Pins that a new number reuses neither a live nor a retired id, and that new numbers follow the lines' order.
    Given a repository on the old system with a capability spec/capabilities/thing.md whose retired: lists r4
    And whose Behaviour lines are, in order, one with [r1], one with no id, one with [r3] and one with no id
    When the session runs `migrate run --context example.org/acme/shop`
    Then the Behaviour lines of spec/capabilities/thing.md are, in order, [r1], [r5], [r3] and [r6]

  @r12
  Scenario: run gives a moved plan, design note and test log with no about the context as their about
    Pins what a moved record that is given an id is about when it says nothing of it.
    Given a repository on the old system with docs/superpowers/plans/p1.md, docs/superpowers/specs/s1.md and records/logs/run1-test-log.md, none with an about
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/archive/plans/p1.md, .shop/records/archive/design-notes/s1.md and .shop/records/logs/run1-test-log.md are each about bounded-context/example.org/acme/shop
