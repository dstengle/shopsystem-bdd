# formulated from spec/capabilities/migration-tools.md
Feature: Migration tools
  Narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases

  @r1
  Scenario: `migrate run` relocates decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git
    Pins where each of these old directories lands, keeping a record's path, and that git sees each relocation as a rename.
    Given a repository on the old system with decisions/0001-d0.md, work/i1/w1.md and records/logs/r1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0001-d0.md has the content decisions/0001-d0.md had, apart from the id r9 gives it
    And .shop/work/i1/w1.md has the content work/i1/w1.md had
    And .shop/records/logs/r1.md has the content records/logs/r1.md had, apart from any id r9 and about r12 give it
    And decisions/, work/ and records/ are gone
    And git status shows each of the three as renamed

  @r1
  Scenario: `migrate run` relocates a file under records/ that is not text as it is
    Pins that a file that is not text, such as an image, is relocated like any other.
    Given a repository on the old system with records/img/a.png, which is not text
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/img/a.png is records/img/a.png as it was, byte for byte
    And records/img/a.png is gone

  @r2
  Scenario: `migrate run` replaces a ledger entry with a decision file named by its heading, with its first paragraph, accepted, with its date and source
    Pins the file a ledger entry that nothing supersedes becomes, and where each of its fields comes from.
    Given a repository on the old system whose spec/decisions.md has nothing but the entry `## decision/0007-a`
    And the entry is dated 2025-03-01, its source is alice, and its first paragraph is "We do a."
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md has the summary "We do a." and its Decision has "We do a."
    And its status is accepted, its date is 2025-03-01 and its by is alice

  @r2
  Scenario: `migrate run` ends an entry's first paragraph at its date or source line, with or without a blank line before it
    Pins that an entry's first paragraph ends at the first blank line or the first `date:` or `source:` line.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a`, its first paragraph "We do a." followed with no blank line by its date 2025-03-01 and its source alice
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md has the summary "We do a."
    And its date is 2025-03-01 and its by is alice

  @r2
  Scenario Outline: `migrate run` writes a first paragraph and a source that hold <what> so that model reads them as they are
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
  Scenario: `migrate run` puts an entry's whole text in its decision file's Decision, its first paragraph also being its summary
    Pins that no text of an entry is lost when the ledger goes.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a` with the paragraphs "We do a." and "Because b."
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md has the summary "We do a."
    And its Decision has "We do a." and then "Because b."

  @r2
  Scenario: `migrate run` gives a decision file its entry's supersedes and revisit_when, and the entry it supersedes the status `superseded`
    Pins that an entry's supersedes and revisit_when are kept, the `superseded` entry named by its new id and no longer accepted.
    Given a repository on the old system whose spec/decisions.md has the entries `## decision/0003-b` and `## decision/0007-a`
    And the entry 0007-a has supersedes: decision/0003-b and revisit_when: b comes back
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md's supersedes is design-decision/example.org/acme/shop/b and its revisit_when is "b comes back"
    And spec/decisions/0007-a.md's status is accepted
    And spec/decisions/0003-b.md's status is `superseded`

  @r2
  Scenario: `migrate run` keeps both decisions an entry's supersedes names, each by its new id, and supersedes both
    Pins that a supersedes naming two decisions loses neither.
    Given a repository on the old system whose spec/decisions.md has the entries `## decision/0003-b`, `## decision/0004-c` and `## decision/0007-a`
    And the entry 0007-a has supersedes naming decision/0003-b and decision/0004-c
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md's supersedes names design-decision/example.org/acme/shop/b and design-decision/example.org/acme/shop/c, and nothing else
    And spec/decisions/0003-b.md's and spec/decisions/0004-c.md's status is `superseded`

  @r17
  Scenario Outline: `migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by after the source, <case>
    Pins that supersedes names only decisions, and that by is exactly the entry's source then `; supersedes <id> <qualifier>`, with no stray punctuation.
    Given a repository on the old system whose spec/decisions.md has the entries `## decision/0003-b`, `## decision/0004-c` and `## decision/0007-a`
    And the entry 0007-a's source is alice and its supersedes is <supersedes>
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md's supersedes names <ids>, and nothing else
    And its by is exactly "alice; supersedes design-decision/example.org/acme/shop/b (for artifacts)"

    Examples:
      | case                                | supersedes                                       | ids                                                                                    |
      | one decision                        | decision/0003-b (for artifacts)                  | design-decision/example.org/acme/shop/b                                                |
      | two decisions, the first qualified  | decision/0003-b (for artifacts), decision/0004-c | design-decision/example.org/acme/shop/b and design-decision/example.org/acme/shop/c    |

  @r11
  Scenario Outline: `migrate run` removes a ledger that holds nothing but <what> once it has replaced every entry
    Pins the ledgers migrate removes.
    Given a repository on the old system whose spec/decisions.md has <ledger>
    And the entry's first paragraph is "We do a."
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions.md is gone
    And spec/decisions/0007-a.md has the summary "We do a."

    Examples:
      | what                    | ledger                                                                        |
      | its entries             | nothing but the entry `## decision/0007-a`                                    |
      | a title and its entries | the title `# Decisions` and a blank line, then the entry `## decision/0007-a` |

  @r13
  Scenario Outline: `migrate run` numbers each ledger entry with no number, in ledger order, from one above the ledger's highest entry number, <case>
    Pins that a new number is above every number in the ledger, not only the last, starts at 1 in a ledger with none, and follows the ledger's order.
    Given a repository on the old system whose spec/decisions.md has, in order, the entries <entries>
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/ has <files>
    And spec/decisions/<b file> gives the id design-decision/example.org/acme/shop/b

    Examples:
      | case                   | entries                                                                         | files                                         | b file    |
      | among numbered entries | `## decision/0007-a`, `## decision/b`, `## decision/0003-c` and `## decision/d` | 0007-a.md, 0008-b.md, 0003-c.md and 0009-d.md | 0008-b.md |
      | with no numbered entry | `## decision/b` and `## decision/d`                                             | 0001-b.md and 0002-d.md                       | 0001-b.md |

  @r7
  Scenario Outline: `migrate run` that finds <found> in spec/decisions.md names it, exits non-zero and changes no file, the ledger included
    Pins that ledger text migrate cannot replace stops `migrate run`.
    Given a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a` and <found>
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not replace <named>
    And it exits non-zero
    And nothing under the repository has changed

    Examples:
      | found                                     | named                                                       |
      | before it the text "Notes on the ledger." | the ledger text "Notes on the ledger." outside its entries  |
      | after it the heading `## decision/0007-a` | the ledger entry `## decision/0007-a`, which is there twice |

  @r7
  Scenario Outline: `migrate run` whose ledger entry's decision file would land on <there> names it, exits non-zero and changes no file
    Pins that the decision file migrate writes for a ledger entry, numbered or numbered by migrate, never takes the place of a file that is there or relocates there.
    Given a repository on the old system whose spec/decisions.md has, in order, the entries <entries>, and <there>
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not write spec/decisions/<file> for the ledger entry <entry>
    And it exits non-zero
    And nothing under the repository has changed

    Examples:
      | entries                                  | there                                                        | file      | entry                |
      | `## decision/0007-a`                     | decisions/0007-a.md, which is relocated to spec/decisions/0007-a.md | 0007-a.md | `## decision/0007-a` |
      | `## decision/0007-a`                     | a tracked spec/decisions/0007-a.md                           | 0007-a.md | `## decision/0007-a` |
      | `## decision/0007-a`                     | an untracked spec/decisions/0007-a.md                        | 0007-a.md | `## decision/0007-a` |
      | `## decision/0007-a` and `## decision/b` | decisions/0008-b.md, which is relocated to spec/decisions/0008-b.md | 0008-b.md | `## decision/b`      |

  @r3
  Scenario: `migrate run` deprecates a @holding scenario as `features deprecate` does
    Pins that migrate leaves a @holding scenario, and the tests that name it, as `features deprecate` would.
    Given a repository on the old system whose features/thing.feature has a scenario "s1" tagged @holding
    And a test that names "s1" by title
    And a copy of that repository on which `features deprecate` has been run for "s1"
    When the session runs `migrate run --context example.org/acme/shop` on the repository
    Then features/thing.feature and the test are as they are in the copy

  @r4
  Scenario: `migrate run` gives spec/index.md the id bounded-context/<path>
    Pins that the path given to --context is the one the context's id holds.
    Given a repository on the old system whose spec/index.md gives no id
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/index.md gives the id bounded-context/example.org/acme/shop

  @r5
  Scenario: `migrate run` rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it relocated or renamed
    Pins each of the three kinds of reference `migrate run` rewrites in a tracked text file.
    Given a repository on the old system with work/i1/w1.md
    And a tracked README.md that names work/i1/w1.md
    And a tracked notes/n1.md with the Markdown link `[w1](../work/i1/w1.md)`
    And its spec/decisions.md has the entry `## decision/0007-a`
    And a capability spec/capabilities/thing.md whose frontmatter rests_on names decision/0007-a
    When the session runs `migrate run --context example.org/acme/shop`
    Then README.md names .shop/work/i1/w1.md where it named work/i1/w1.md
    And notes/n1.md has the link `[w1](../.shop/work/i1/w1.md)`
    And spec/capabilities/thing.md's rests_on names design-decision/example.org/acme/shop/a

  @r5
  Scenario: `migrate run` rewrites a frontmatter id and a supersedes that name a ledger entry it numbered
    Pins that an entry with no number, numbered by r13, is named afterwards by its new id everywhere, and is `superseded` as r2 says.
    Given a repository on the old system whose spec/decisions.md has, in order, the entries `## decision/0007-a` and `## decision/b`
    And the entry 0007-a has supersedes: decision/b
    And a capability spec/capabilities/thing.md whose frontmatter rests_on names decision/b
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0008-b.md gives the id design-decision/example.org/acme/shop/b
    And spec/capabilities/thing.md's rests_on names design-decision/example.org/acme/shop/b
    And spec/decisions/0007-a.md's supersedes is design-decision/example.org/acme/shop/b
    And spec/decisions/0008-b.md's status is `superseded`

  @r5
  Scenario Outline: `migrate run` rewrites a decision file's by that names <old>, a path it relocated
    Pins that a path written in words in by follows the file it names.
    Given a repository on the old system with <old>
    And its spec/decisions.md has the entry `## decision/0007-a`, whose source is "alice, from <old>"
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0007-a.md's by is "alice, from <new>"

    Examples:
      | old                          | new                                            |
      | adrs/0001-use-x.md           | .shop/records/decision-arguments/0001-use-x.md |
      | docs/superpowers/specs/s1.md | .shop/records/archive/design-notes/s1.md       |

  @r6
  Scenario Outline: after `migrate run` on a repository with <what>, `model check` prints no unresolved reference or file problem
    Pins that a repository run through migrate leaves `model check` nothing unresolved and no file problem to print.
    Given a repository on the old system with <what>
    And the session has run `migrate run --context example.org/acme/shop`
    When the session runs `model check`
    Then it prints no unresolved reference and no file problem

    Examples:
      | what                                                                                                                                                                                  |
      | decisions/, work/, records/, adrs/, docs/superpowers/plans/, docs/superpowers/specs/, docs/superpowers/requests/, a ledger spec/decisions.md, a capability and a @holding scenario |
      | a capability spec/capabilities/thing.md whose frontmatter has formulated_as: features/thing.feature                                                                                  |
      | a capability spec/capabilities/thing.md whose id is capability/thing                                                                                                                 |
      | a ledger whose entry 0007-a has supersedes: decision/0003-b (for artifacts), and the entry 0003-b                                                                                    |

  @r7
  Scenario: `migrate run` that cannot make two of its changes names both, exits non-zero and changes no file
    Pins that `migrate run` is all or nothing, and names each change it could not make rather than the first.
    Given a repository on the old system with work/i1/w1.md, and .shop/work/i1/w1.md already exists
    And it has records/archive/plans/p1.md and docs/superpowers/plans/p1.md, which would both be relocated to .shop/records/archive/plans/p1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not `move work/i1/w1.md onto .shop/work/i1/w1.md`
    And it says it could not `move both records/archive/plans/p1.md and docs/superpowers/plans/p1.md to .shop/records/archive/plans/p1.md`
    And it exits non-zero
    And nothing under the repository has changed

  @r7
  Scenario: `migrate run` that would relocate a file onto an untracked file names the relocation, exits non-zero and changes no file
    Pins that a file already there stops a relocation onto it whether or not git tracks it.
    Given a repository on the old system with work/i1/w1.md and work/i1/w2.md, and an untracked .shop/work/i1/w2.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not `move work/i1/w2.md onto .shop/work/i1/w2.md`
    And it exits non-zero
    And nothing under the repository has changed

  @r8
  Scenario: `migrate run` relocates docs/superpowers/plans/, specs/ and requests/ under .shop/records/archive/, with git
    Pins where plans, design notes and requests land, and that git sees each relocation as a rename.
    Given a repository on the old system with docs/superpowers/plans/p1.md, docs/superpowers/specs/s1.md and docs/superpowers/requests/q1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/archive/plans/p1.md has the content docs/superpowers/plans/p1.md had, apart from the id r9 and the about r12 give it
    And .shop/records/archive/design-notes/s1.md has the content docs/superpowers/specs/s1.md had, apart from the id r9 and the about r12 give it
    And .shop/records/archive/requests/q1.md has the content docs/superpowers/requests/q1.md had, apart from the id r9 and the about r12 give it
    And docs/superpowers/plans/, docs/superpowers/specs/ and docs/superpowers/requests/ are gone
    And git status shows each of the three as renamed

  @r14
  Scenario: `migrate run` relocates adrs/ to .shop/records/decision-arguments/, with git
    Pins where ADRs land, and that git sees the relocation as a rename.
    Given a repository on the old system with adrs/0001-use-x.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/decision-arguments/0001-use-x.md has the content adrs/0001-use-x.md had, apart from the id r9 and the about r12 give it
    And adrs/ is gone
    And git status shows it as renamed

  @r9
  Scenario: `migrate run` gives a capability, a decision file, a plan, a request, a design note, an ADR and a test log the type-first id of its kind
    Pins the id each kind gets, as <kind>/<context path>/<name>, the name being the file's stem, a decision file's alone without its number.
    Given a repository on the old system with a capability spec/capabilities/thing.md with no id
    And its spec/decisions.md has the entry `## decision/0007-a`
    And it has docs/superpowers/plans/p1.md, docs/superpowers/requests/q1.md, docs/superpowers/specs/s1.md, adrs/0001-use-x.md and records/logs/run1-test-log.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/capabilities/thing.md gives the id capability/example.org/acme/shop/thing
    And spec/decisions/0007-a.md gives the id design-decision/example.org/acme/shop/a
    And .shop/records/archive/plans/p1.md gives the id initiative-archive/example.org/acme/shop/p1
    And .shop/records/archive/requests/q1.md gives the id initiative-archive/example.org/acme/shop/q1
    And .shop/records/archive/design-notes/s1.md gives the id decision-argument/example.org/acme/shop/s1
    And .shop/records/decision-arguments/0001-use-x.md gives the id decision-argument/example.org/acme/shop/0001-use-x
    And .shop/records/logs/run1-test-log.md gives the id measurement/example.org/acme/shop/run1-test-log

  @r9
  Scenario: `migrate run` gives a capability whose id is the short form capability/<name> its full id
    Pins that a capability's id ends as capability/<context path>/<name> whatever form it had.
    Given a repository on the old system with a capability spec/capabilities/thing.md whose id is capability/thing
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/capabilities/thing.md gives the id capability/example.org/acme/shop/thing

  @r9
  Scenario Outline: `migrate run` gives a README.md it relocates to <new> no id, kind or about
    Pins that a README.md is not a record wherever it lands under .shop/records/, and so has no frontmatter from migrate.
    Given a repository on the old system with <old>
    When the session runs `migrate run --context example.org/acme/shop`
    Then <new> has the content <old> had, with no id, no kind and no about

    Examples:
      | old                   | new                                        |
      | records/logs/README.md | .shop/records/logs/README.md               |
      | adrs/README.md         | .shop/records/decision-arguments/README.md |
      | decisions/README.md    | spec/decisions/README.md                   |

  @r10
  Scenario: `migrate run` numbers each Behaviour line with no id, in Behaviour order, from one above the highest id its capability has ever used
    Pins that a new number reuses neither a live nor a retired id, and that new numbers follow the lines' order.
    Given a repository on the old system with a capability spec/capabilities/thing.md whose retired: lists r4
    And whose Behaviour lines are, in order, one with [r1], one with no id, one with [r3] and one with no id
    When the session runs `migrate run --context example.org/acme/shop`
    Then the Behaviour lines of spec/capabilities/thing.md are, in order, [r1], [r5], [r3] and [r6]

  @r12
  Scenario: `migrate run` gives each relocated record kind with no about the context as its about
    Pins what a moved record that is given an id is about when it says nothing of it.
    Given a repository on the old system with docs/superpowers/plans/p1.md, docs/superpowers/requests/q1.md, docs/superpowers/specs/s1.md, adrs/0001-use-x.md and records/logs/run1-test-log.md, none with an about
    When the session runs `migrate run --context example.org/acme/shop`
    Then .shop/records/archive/plans/p1.md, .shop/records/archive/requests/q1.md, .shop/records/archive/design-notes/s1.md, .shop/records/decision-arguments/0001-use-x.md and .shop/records/logs/run1-test-log.md are each about bounded-context/example.org/acme/shop

  @r15 @deprecated
  Scenario Outline: `migrate run` on a repository with <change> refuses, naming it, exits non-zero and changes no file (deprecated)
    Deprecated for: `<command>` on a repository with <change> refuses, naming it, exits with an error and changes no file
    Pins that migrate starts only from a working tree with nothing uncommitted, untracked files included.
    Given a repository on the old system with work/i1/w1.md
    And <change>
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate refuses, naming <named>
    And it exits non-zero
    And nothing under the repository has changed

    Examples:
      | change                                            | named       |
      | a tracked README.md changed since the last commit | README.md   |
      | an untracked notes/n2.md                          | notes/n2.md |
      | a tracked README.md deleted since the last commit | README.md   |

  @r15
  Scenario Outline: `<command>` on a repository with <change> refuses, naming it, exits with an error and changes no file
    Pins that both commands start only from a working tree with nothing uncommitted, untracked files included.
    Given <repository>
    And <change>
    When the session runs `<command>`
    Then migrate refuses, naming <named>
    And it exits with an error
    And nothing under the repository has changed

    Examples:
      | command                                     | repository                                                                                  | change                                            | named       |
      | migrate run --context example.org/acme/shop | a repository on the old system with work/i1/w1.md                                           | a tracked README.md changed since the last commit | README.md   |
      | migrate run --context example.org/acme/shop | a repository on the old system with work/i1/w1.md                                           | an untracked notes/n2.md                          | notes/n2.md |
      | migrate run --context example.org/acme/shop | a repository on the old system with work/i1/w1.md                                           | a tracked README.md deleted since the last commit | README.md   |
      | migrate upgrade                             | a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md | a tracked README.md changed since the last commit | README.md   |
      | migrate upgrade                             | a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md | an untracked notes/n2.md                          | notes/n2.md |
      | migrate upgrade                             | a repository on the final layout whose plugin version is 0.23.1, with a work-item .shop/work/i1/a.md | a tracked README.md deleted since the last commit | README.md   |

  @r16
  Scenario: `migrate run` adds every file it wrote or relocated to git and writes spec/decisions/index.md
    Pins that git has every file migrate leaves, the decisions index included.
    Given a repository on the old system with work/i1/w1.md
    And its spec/decisions.md has nothing but the entry `## decision/0007-a`
    When the session runs `migrate run --context example.org/acme/shop`
    Then git status shows .shop/work/i1/w1.md, spec/decisions/0007-a.md and spec/decisions/index.md as staged, and no file as untracked or changed but not staged
    And `model decisions --check` says spec/decisions/index.md is current

  @r1
  Scenario: `migrate run` from a subdirectory relocates the repository's top-level directories
    Pins that the top level r1 names is the repository's, wherever in it the session runs migrate.
    Given a repository on the old system with work/i1/w1.md and a tracked notes/n1.md
    When the session runs `migrate run --context example.org/acme/shop` from notes/
    Then .shop/work/i1/w1.md has the content work/i1/w1.md had
    And notes/.shop does not exist

  @r4 @r5
  Scenario: `migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>, and rewrites what names the old id
    Pins that a context id in another form is replaced, not kept, and that a frontmatter id naming it follows.
    Given a repository on the old system whose spec/index.md gives the id bounded-context/shop
    And a tracked notes/n1.md whose frontmatter about names bounded-context/shop
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/index.md gives the id bounded-context/example.org/acme/shop
    And notes/n1.md's about names bounded-context/example.org/acme/shop

  @r9 @r5
  Scenario: `migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id, and rewrites what names the old id
    Pins that a moved decision file's id in another form is replaced, not kept, and that a frontmatter id naming it follows.
    Given a repository on the old system with decisions/0001-x.md whose id is decision/0001-x
    And a capability spec/capabilities/thing.md whose frontmatter rests_on names decision/0001-x
    When the session runs `migrate run --context example.org/acme/shop`
    Then spec/decisions/0001-x.md gives the id design-decision/example.org/acme/shop/x
    And spec/capabilities/thing.md's rests_on names design-decision/example.org/acme/shop/x

  @r5
  Scenario: `migrate run` rewrites nothing through a tracked symbolic link, and leaves the file outside the repository it points to as it was
    Pins that a tracked symbolic link is not one of the repository's text files: the file it points to, outside the repository, is not migrate's to change.
    Given a repository on the old system with work/i1/w1.md
    And a tracked linked.md, a symbolic link to a file outside the repository that names work/i1/w1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then the file outside the repository is as it was
    And linked.md is the same symbolic link
    And .shop/work/i1/w1.md has the content work/i1/w1.md had

  @r5
  Scenario: `migrate run` keeps the CRLF line endings of a file in which it rewrites a path
    Pins that a rewrite changes the path it names and nothing else, line endings included.
    Given a repository on the old system with work/i1/w1.md
    And a tracked notes/n1.md with CRLF line endings that names work/i1/w1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then notes/n1.md is as it was, byte for byte, with .shop/work/i1/w1.md for work/i1/w1.md

  @r7
  Scenario Outline: `migrate run` that would <what> names it, exits non-zero and changes no file
    Pins that migrate checks every change before it makes one: none goes through a symbolic link, over a file git does not hold, or under a file.
    Given a repository on the old system with work/i1/w1.md and <there>
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not <named>
    And it exits non-zero
    And nothing under the repository has changed

    Examples:
      | what                                             | there                                                                                  | named                                                                    |
      | give a plan that is a symbolic link its id       | docs/superpowers/plans/p1.md, a tracked symbolic link to a file outside the repository | change docs/superpowers/plans/p1.md: it is a symbolic link               |
      | write spec/decisions/index.md over an ignored file | an ignored spec/decisions/index.md                                                   | write spec/decisions/index.md                                            |
      | move a file under an ignored file                | an ignored file .shop                                                                  | move work/i1/w1.md to .shop/work/i1/w1.md: .shop is not a directory      |

  @r7
  Scenario: `migrate run` outside a git repository says so, exits non-zero and changes no file
    Pins that migrate, which relocates with git, names the repository it could not find rather than failing part way.
    Given a directory that is not a git repository, with work/i1/w1.md
    When the session runs `migrate run --context example.org/acme/shop`
    Then migrate says it could not find a git repository
    And it exits non-zero
    And nothing under the repository has changed

  @r18
  Scenario: `migrate status` prints the repository's plugin version, the plugin's version and each pending upgrade step with its version and description
    Pins what a person or the SessionStart hook learns from `migrate status` about where a repository stands.
    Given a repository on the final layout whose .shop/plugin-version is 0.23.1
    When the session runs `migrate status`
    Then migrate prints 0.23.1 as the repository's plugin version and the plugin's version as the plugin's
    And it prints the pending upgrade step 0.24.0 "work-items named by ids"
    And it exits successfully

  @r19
  Scenario: a repository with .shop/ and no .shop/plugin-version is taken to be on 0.23.1
    Pins the plugin version of a repository from before plugin versions were recorded.
    Given a repository with .shop/ and no .shop/plugin-version
    When the session runs `migrate status`
    Then migrate prints 0.23.1 as the repository's plugin version

  @r20
  Scenario: `migrate upgrade` applies the pending upgrade step, records the plugin's version and commits it all in one commit naming the step
    Pins that an upgrade leaves the repository on the plugin's version, with the step's changes and the version in one commit and nothing uncommitted.
    Given a repository on the final layout whose .shop/plugin-version is 0.23.1, with a work-item .shop/work/i1/a.md
    When the session runs `migrate upgrade`
    Then the work-item that was .shop/work/i1/a.md is w1
    And .shop/plugin-version holds the plugin's version
    And git log has one commit more than before, and it names the upgrade step "work-items named by ids"
    And git status shows nothing uncommitted

  @r22
  Scenario: a session starting in a repository with a pending upgrade step is told to offer the upgrade and run it only on the person's yes
    Pins that the person is offered the upgrade at a session's start, and that the session does not upgrade without their yes.
    Given a repository with .shop/ whose .shop/plugin-version is 0.23.1
    When the person starts a session in it
    Then the plugin's SessionStart hook tells the session to offer the person the upgrade from 0.23.1 to the plugin's version, naming the upgrade step "work-items named by ids"
    And it tells the session to run `migrate upgrade` only on the person's yes

  @r23
  Scenario: a session starting in a repository on a plugin version above the plugin's is told to tell the person to update the plugin
    Pins that a plugin older than the repository is pointed out to the person.
    Given a repository with .shop/ whose .shop/plugin-version is 99.0.0
    When the person starts a session in it
    Then the plugin's SessionStart hook tells the session to tell the person to update the plugin

  @r24
  Scenario: a session starting in a repository on the plugin's version is told nothing
    Pins that a repository that needs nothing adds nothing to a session's start.
    Given a repository with .shop/ whose .shop/plugin-version is the plugin's version
    When the person starts a session in it
    Then the plugin's SessionStart hook tells the session nothing

  @r25
  Scenario: the upgrade step "work-items named by ids" numbers every work-item from 1, by its initiative's number and then its file name
    Pins that work-item ids are numbered across the bounded context, initiatives by number, not text, and a work-item's place within its initiative by file name.
    Given a repository on the final layout whose .shop/plugin-version is 0.23.1
    And work-items .shop/work/i10/a.md, .shop/work/i2/b.md and .shop/work/i2/a.md
    When the session runs `migrate upgrade`
    Then the work-item that was .shop/work/i2/a.md is w1
    And the work-item that was .shop/work/i2/b.md is w2
    And the work-item that was .shop/work/i10/a.md is w3

  @r26
  Scenario: the upgrade step "work-items named by ids" renames a work-item's file and stage directories and rewrites its name where its initiative names it
    Pins what the step changes for one work-item and what it leaves: its file, id, heading, runs, log lines and the references of its initiative's work-items, and no free text in records.
    Given a repository on the final layout whose .shop/plugin-version is 0.23.1
    And .shop/work/i1/size-check.md, a work-item with the heading "# size-check", a directory .shop/work/i1/runs/size-check/ and a line of .shop/work/i1/log.jsonl for size-check
    And .shop/work/i1/docs.md, a work-item with no heading, whose depends_on names size-check
    And .shop/records/observations.md, which names size-check in its text
    When the session runs `migrate upgrade`
    Then .shop/work/i1/size-check.md is now .shop/work/i1/w2.md, its id work-item/<context path>/w2 and its heading "# size-check"
    And .shop/work/i1/docs.md is now .shop/work/i1/w1.md, its heading "# docs" and its depends_on naming w2
    And .shop/work/i1/runs/size-check/ is now .shop/work/i1/runs/w2/
    And the line of .shop/work/i1/log.jsonl names w2
    And .shop/records/observations.md still names size-check

  @r27
  Scenario: `migrate upgrade` with no pending upgrade step says so, exits successfully and changes nothing
    Pins that an upgrade of a repository already on the plugin's version is harmless.
    Given a repository on the final layout whose .shop/plugin-version is the plugin's version
    When the session runs `migrate upgrade`
    Then migrate says no upgrade step is pending
    And it exits successfully
    And nothing under the repository has changed

  @r28
  Scenario: a session starting in a repository without .shop/ is told nothing
    Pins that the hook says nothing of upgrades where the final layout is not in use.
    Given a repository without .shop/
    When the person starts a session in it
    Then the plugin's SessionStart hook tells the session nothing
