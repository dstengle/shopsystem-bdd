# formulated from spec/capabilities/feature-file-tools.md
Feature: Feature file tools
  Narrator: a session editing feature files

  @r1
  Scenario: every feature file under the directory is read, and docstring text is not
    A feature file in a nested directory under the default features directory is read, and a tag or scenario written inside a docstring is not.
    Given a feature file features/cart/nested.feature with a scenario "Nested" tagged @slice-1
    And the scenario "Nested" has a docstring with the lines "@slice-1" and "Scenario: Phantom"
    When the session runs `features list --tag slice-1` without --dir
    Then the output lists features/cart/nested.feature with "Nested"
    And the output does not list "Phantom"

  @r2
  Scenario: a feature file with a Rule block is refused
    A Rule block is not read as part of the feature; the command refuses and says which file has it.
    Given a feature file features/rules.feature that has a Rule: block
    When the session runs `features list --title Cart`
    Then the command is rejected because the feature file has a Rule: block
    And the refusal names features/rules.feature

  @r2
  Scenario Outline: an edit is refused when it would leave a Rule: block outside a docstring
    Pins that a Rule: line inside a docstring is no Rule: block, and that a refused edit changes no file.
    Given an edit by features that would leave features/cart.feature with <content>
    When the session runs that edit
    Then <effect>

    Examples:
      | content                                      | effect                                                                                                       |
      | a Rule: block outside a docstring            | the edit is rejected because features could not read the edited file, and every file is as it was            |
      | a Rule: line inside a docstring              | the edit is made                                                                                             |

  @r4
  Scenario: counting by tag counts outline rows, inherited tags and untagged scenarios
    Pins that each Examples row is a scenario with its feature's and its own table's tags, and that the total leaves no scenario out.
    Given a feature file features/cart.feature tagged @cart
    And it has a scenario "Plain" with no tags of its own
    And it has a scenario "Own tag" tagged @slice-1
    And it has a Scenario Outline "Outlined" tagged @slice-2 with an Examples table tagged @r3 of 2 rows and an untagged Examples table of 1 row
    And a feature file features/misc.feature with no tags has a scenario "Untagged" with no tags
    When the session runs `features count --by-tag`
    Then it prints 5 scenarios for cart, 1 for slice-1, 3 for slice-2 and 2 for r3
    And it prints a total of 6

  @r5
  Scenario: listing by tag includes the feature's and the Examples' tags
    A scenario has a tag when it has it itself, when its feature has it, or when its Examples table has it.
    Given a feature file features/cart.feature tagged @cart
    And it has a scenario "Plain" with no tags of its own
    And it has a scenario "Own tag" tagged @checkout
    And it has a Scenario Outline "Outlined" whose one Examples table is tagged @checkout and has one row
    And another feature file features/stock.feature tagged @checkout has a scenario "Elsewhere"
    And a feature file features/misc.feature has a scenario "Untagged" with no tags
    When the session runs `features list --tag checkout`
    Then the output lists features/cart.feature with "Own tag"
    And the output lists features/cart.feature with "Outlined"
    And the output lists features/stock.feature with "Elsewhere"
    And the output does not list "Plain" or "Untagged"

  @r5
  Scenario: listing by title finds every scenario whose title contains the text
    A title matches when the text appears anywhere in it, not only when it equals it.
    Given a feature file features/cart.feature with scenarios "Apply a code", "Code expired" and "Empty cart"
    When the session runs `features list --title "ode"`
    Then the output lists features/cart.feature with "Apply a code"
    And the output lists features/cart.feature with "Code expired"
    And the output does not list "Empty cart"

  @r7 @deprecated
  Scenario: listing that matches nothing prints nothing and fails (deprecated)
    Deprecated for: listing that matches nothing prints nothing and succeeds
    An empty list is not a success.
    Given a feature file features/cart.feature with no scenario tagged @slice-9
    When the session runs `features list --tag slice-9`
    Then nothing is printed
    And it exits with an error

  @r7
  Scenario: listing that matches nothing prints nothing and succeeds
    A list with no match has still answered, so it prints nothing and does not fail.
    Given a feature file features/cart.feature with no scenario tagged @slice-9
    When the session runs `features list --tag slice-9`
    Then nothing is printed
    And it exits successfully

  @r60
  Scenario: listing with --json prints the matching scenarios as one JSON object
    Pins that the whole list, each scenario with its file and title, is printed as a single JSON object.
    Given a feature file features/cart.feature with scenarios "Apply a code" and "Empty cart" tagged @checkout
    And a feature file features/stock.feature with a scenario "Restock" tagged @checkout
    And a feature file features/misc.feature with a scenario "Untagged" with no tags
    When the session runs `features list --tag checkout --json`
    Then the output is one JSON object
    And it gives features/cart.feature with "Apply a code", features/cart.feature with "Empty cart" and features/stock.feature with "Restock"
    And it gives no other scenario

  @r35
  Scenario Outline: retagging a title that is not in exactly one file is refused
    The title must pick out one file; otherwise nothing is changed and every file that has it is named.
    Given the title "Apply a code" is in <files with it>
    When the session runs `features tag "Apply a code" r7`
    Then the command is rejected because the title is not in exactly one file
    And the refusal names <files named>
    And no file is changed

    Examples:
      | files with it                                  | files named                                    |
      | no feature file                                | no file                                        |
      | features/cart.feature and features/old.feature | features/cart.feature and features/old.feature |

  @r46
  Scenario: retagging with a tag that is not a requirement tag is refused
    Only r<n> is a tag features tag accepts.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the session runs `features tag "Apply a code" wip`
    Then the command is rejected because the tag is not written r<n>
    And no file is changed

  @r12
  Scenario: relocating a scenario takes its block to the end of the destination
    The block leaves its source file and arrives unchanged after everything already in the destination.
    Given a feature file features/old.feature with scenarios "Apply a code" and "Empty cart"
    And a feature file features/cart.feature whose last scenario is "Checkout"
    When the session runs `features move "Apply a code" --to features/cart.feature`
    Then features/old.feature has "Empty cart" and not "Apply a code"
    And the block of "Apply a code" follows "Checkout" at the end of features/cart.feature, unchanged

  @r13
  Scenario: relocating with the Background inlined puts its steps first
    A relocated scenario keeps the steps its source Background gave it.
    Given a feature file features/old.feature whose Background has the step "Given the date is 2026-10-16"
    And its scenario "Apply a code" has first step "Given a cart with product Mug at price 8.00"
    And a feature file features/cart.feature
    When the session runs `features move "Apply a code" --to features/cart.feature --inline-background`
    Then the relocated "Apply a code" has the steps "Given the date is 2026-10-16" then "Given a cart with product Mug at price 8.00"

  @r14
  Scenario Outline: relocating with feature tags kept adds the missing ones on a tag line of their own
    Pins that only the feature tags the destination lacks are kept, on their own line just above the Scenario: line, with the scenario's own tag lines left as they were.
    Given a feature file features/old.feature with the feature tags @cart and @checkout
    And its scenario "Apply a code" has <own tag lines>
    And a feature file features/cart.feature with the feature tag @cart
    When the session runs `features move "Apply a code" --to features/cart.feature --keep-feature-tags`
    Then the relocated "Apply a code" has the tag lines <tag lines after>, the last directly above its Scenario: line

    Examples:
      | own tag lines           | tag lines after             |
      | the tag line "@slice-2" | "@slice-2" then "@checkout" |
      | no tag line             | "@checkout"                 |

  @r46
  Scenario: relocating to a destination that does not exist is refused
    `features move` never creates a file.
    Given a feature file features/old.feature with a scenario "Apply a code"
    And no file features/missing.feature
    When the session runs `features move "Apply a code" --to features/missing.feature`
    Then the command is rejected because the destination does not exist
    And no file is changed

  @r16
  Scenario: two trees alike scenario by scenario pass `features verify-moved`
    Scenarios may sit in other files, but alike by title in tags, description and steps they all match.
    Given a tree old/ with "Apply a code" and "Empty cart" in old/cart.feature
    And a tree features/ with "Apply a code" in features/codes.feature and "Empty cart" in features/cart.feature, each alike in effective tags, description, Background and own steps
    When the session runs `features verify-moved --from old`
    Then it prints that 2 scenarios match
    And it exits successfully

  @r17
  Scenario Outline: a scenario that changed between the trees is named with what changed
    `verify-moved` names which of effective tags, description or steps differ.
    Given trees old/ and features/ that both have "Apply a code"
    And the two copies of "Apply a code" differ in their <part>
    When the session runs `features verify-moved --from old`
    Then it names "Apply a code" with its <part> as changed
    And it exits with an error

    Examples:
      | part           |
      | effective tags |
      | description    |
      | steps          |

  @r17
  Scenario Outline: a title that appears twice in either tree is a duplicate
    Scenarios are matched by title, so a title that appears twice cannot be matched.
    Given trees old/ and features/ that both have "Apply a code"
    And <tree> has a second scenario titled "Apply a code"
    When the session runs `features verify-moved --from old`
    Then it names "Apply a code" as a duplicate
    And it exits with an error

    Examples:
      | tree      |
      | old/      |
      | features/ |

  @r19
  Scenario Outline: deprecating a scenario marks it deprecated and writes what for
    A deprecated scenario has the tag @deprecated, a "(deprecated)" title and a line naming what it is deprecated for, and nothing else in it changes.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    And <replacement>
    When the session runs `features deprecate "Apply a code" <option>`
    Then the scenario has the tag @deprecated
    And its title is "Apply a code (deprecated)"
    And it has a description line naming <deprecated for> as what it is deprecated for
    And nothing else in the scenario is changed

    Examples:
      | replacement                          | option                  | deprecated for  |
      | a scenario "Apply a voucher" exists  | --for "Apply a voucher" | Apply a voucher |
      | no scenario "Apply a voucher" exists | --for "Apply a voucher" | Apply a voucher |
      | no replacement is planned            | --for-removal           | removal         |

  @r46
  Scenario: deprecating a scenario already deprecated is refused
    A scenario is deprecated once.
    Given a feature file features/cart.feature with a scenario "Apply a code (deprecated)" tagged @deprecated
    When the session runs `features deprecate "Apply a code (deprecated)" --for "Apply a voucher"`
    Then the command is rejected because the scenario is already deprecated

  @r21
  Scenario Outline: the deprecated list shows each deprecated scenario and what will retire it
    For each deprecated scenario the list says what it is deprecated for and where its replacement stands.
    Given a feature file features/cart.feature with a deprecated scenario "Apply a code (deprecated)" deprecated for <deprecated for>
    And <replacement>
    When the session runs `features deprecated`
    Then the list shows "Apply a code (deprecated)" deprecated for <deprecated for>, with <shown>

    Examples:
      | deprecated for    | replacement                                                       | shown                                            |
      | "Apply a voucher" | a scenario "Apply a voucher" tagged @r3 in features/codes.feature | features/codes.feature and @r3                   |
      | "Apply a voucher" | no scenario titled "Apply a voucher"                              | that no scenario has the title "Apply a voucher" |
      | removal           | no replacement                                                    | that it is deprecated for removal                |

  @r21
  Scenario: the deprecated list says when nothing is deprecated
    An empty list is printed as such, not left blank.
    Given feature files in which no scenario is tagged @deprecated
    When the session runs `features deprecated`
    Then it says that none is deprecated

  @r23
  Scenario: retiring a deprecated scenario removes its block
    Only the deprecated scenario's block goes; the rest of the file stays as it was.
    Given a feature file features/cart.feature with a scenario "Empty cart" and a scenario "Apply a code (deprecated)" tagged @deprecated
    When the session runs `features retire "Apply a code (deprecated)"`
    Then features/cart.feature no longer has "Apply a code (deprecated)"
    And the rest of features/cart.feature is as it was

  @r24
  Scenario: retiring a scenario that is not deprecated is refused
    Only a deprecated scenario can be retired.
    Given a feature file features/cart.feature with a scenario "Apply a code" not tagged @deprecated
    When the session runs `features retire "Apply a code"`
    Then the command is rejected because the scenario is not deprecated
    And features/cart.feature is as it was

  @r25
  Scenario Outline: a binding that names no scenario is printed
    A binding fails when no feature file has its title, or when the feature it names does not have it.
    Given a test module tests/test_cart.py whose line 12 binds the title "Apply a code" in the feature cart.feature
    And <where the title is>
    When the session runs `features bindings` without --tests
    Then it prints tests/test_cart.py, line 12, the title "Apply a code" and the feature cart.feature
    And it exits with an error

    Examples:
      | where the title is                                       |
      | no feature file has the title "Apply a code"             |
      | only features/codes.feature has the title "Apply a code" |

  @r26
  Scenario: bindings that all name a scenario pass
    `bindings` says so when every binding is good.
    Given a test module tests/test_cart.py binding "Apply a code" in cart.feature
    And features/cart.feature has the scenario "Apply a code"
    When the session runs `features bindings`
    Then it says that every binding names a scenario
    And it exits successfully

  @r57
  Scenario Outline: a scenarios() call binds every scenario of the feature files it names
    A call that names a feature file binds each of its scenarios, and one that names a directory binds those of every feature file under it.
    Given <feature file> has the scenarios "Apply a code" and "Empty cart"
    And a test module tests/test_cart.py calling <call>
    When the session runs `features bindings --unbound`
    Then it prints neither "Apply a code" nor "Empty cart" as bound by no test

    Examples:
      | feature file              | call                      |
      | features/cart.feature     | scenarios("cart.feature") |
      | features/sub/cart.feature | scenarios("sub")          |

  @r58
  Scenario: --unbound prints a scenario that no call binds
    Without a binding the scenario never runs, so its file and title are printed.
    Given features/cart.feature has the scenarios "Apply a code" and "Empty cart"
    And a test module tests/test_cart.py binding "Empty cart" in cart.feature
    When the session runs `features bindings --unbound`
    Then it prints features/cart.feature and the title "Apply a code"
    And it exits with an error

  @r58
  Scenario: --unbound prints a scenario bound twice with each call
    A scenario bound by more than one call is printed with the module and line of every call.
    Given features/cart.feature has the scenarios "Apply a code" and "Empty cart"
    And test modules tests/test_a.py and tests/test_b.py binding "Apply a code" at lines 12 and 5
    And a test module tests/test_c.py binding "Empty cart" in cart.feature
    When the session runs `features bindings --unbound`
    Then it prints features/cart.feature, the title "Apply a code" and the calls tests/test_a.py:12 and tests/test_b.py:5
    And it exits with an error

  @r58
  Scenario: --unbound looks only at the feature files it names
    A scenario in a file that is not named is not printed, bound or not.
    Given features/cart.feature has the scenarios "Apply a code" and "Empty cart"
    And features/old.feature has the scenarios "Old rule" and "Older rule"
    And a test module tests/test_cart.py binding "Apply a code" in cart.feature
    And a test module tests/test_c.py binding "Empty cart" in cart.feature
    When the session runs `features bindings --unbound features/cart.feature`
    Then it prints neither "Old rule" nor "Older rule"

  @r62
  Scenario Outline: bindings with --json prints what it found wrong as one JSON object
    Pins that the wrong bindings, or with --unbound the scenarios bound by no test or by more than one, are printed as a single JSON object.
    Given features/cart.feature has the scenarios "Apply a code", "Empty cart" and "Checkout"
    And <bindings>
    When the session runs `features bindings <options>`
    Then the output is one JSON object
    And it gives <found>

    Examples:
      | bindings                                                                                                                                                       | options          | found                                                                                                                              |
      | a test module tests/test_cart.py whose line 12 binds the title "Apply a voucher" in the feature cart.feature                                                   | --json           | the binding at tests/test_cart.py line 12 of "Apply a voucher" in cart.feature                                                     |
      | test modules tests/test_a.py and tests/test_b.py binding "Empty cart" in cart.feature at lines 12 and 5, and tests/test_c.py binding "Checkout" in cart.feature | --json --unbound | "Apply a code" in features/cart.feature as bound by no test, and "Empty cart" as bound by tests/test_a.py:12 and tests/test_b.py:5 |

  @r46
  Scenario: a test module that does not parse is refused
    Bindings cannot be read from a module that does not parse, and the module is named.
    Given a test module tests/test_broken.py that does not parse
    When the session runs `features bindings`
    Then the command is rejected because the test module does not parse
    And the refusal names tests/test_broken.py

  @r28
  Scenario Outline: rebinding rewrites each binding of the old title
    Only the title in the binding calls changes, whatever their number.
    Given a feature file features/cart.feature with a scenario "Apply a voucher"
    And test modules with <bindings> binding calls naming "Apply a code"
    When the session runs `features rebind "Apply a code" "Apply a voucher"`
    Then each of those binding calls names "Apply a voucher"
    And nothing else in the test modules is changed

    Examples:
      | bindings |
      | 2        |
      | 0        |

  @r29
  Scenario: rebinding to a title no scenario has is refused
    A binding is never pointed at a scenario that does not exist.
    Given a test module binding "Apply a code"
    And no feature file has a scenario "Apply a voucher"
    When the session runs `features rebind "Apply a code" "Apply a voucher"`
    Then the command is rejected because no scenario has the new title
    And no test module is changed

  @r35
  Scenario Outline: relocating a title that no file or several files have is refused
    Without --file, `move`, `deprecate` or `retire` needs the title in exactly one file; a refusal names every file that has it.
    Given <holders> the title "Apply a code"
    When the session runs `features move "Apply a code" --to features/codes.feature` without --file
    Then the command is rejected because <reason>
    And the refusal names <named>
    And no file is changed

    Examples:
      | holders                                                  | reason                       | named                                          |
      | no feature file has                                      | no file has the title        | no file                                        |
      | features/cart.feature and features/old.feature both have | several files have the title | features/cart.feature and features/old.feature |

  @r46
  Scenario: relocating a scenario to its own file is refused
    `features move` must take the scenario somewhere else.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the session runs `features move "Apply a code" --to features/cart.feature`
    Then the command is rejected because the destination is the scenario's own file
    And no file is changed

  @r17
  Scenario Outline: a title in only one tree is missing or added
    Every title must be in both trees; one in only the source is missing, one in only the other is added.
    Given trees old/ and features/
    And the title "Apply a code" is only in <tree>
    When the session runs `features verify-moved --from old`
    Then it names "Apply a code" as <named as>
    And it exits with an error

    Examples:
      | tree      | named as |
      | old/      | missing  |
      | features/ | added    |

  @r46
  Scenario: deprecating for a new title written over two lines is refused
    A title is one line: a line break in --for would add a line to the scenario besides its Deprecated for: line.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the session deprecates "Apply a code" for a new title written over two lines
    Then the command is rejected because a title is one line
    And no file is changed

  @r21
  Scenario Outline: the deprecated list flags a deprecated scenario it cannot place
    A deprecated scenario with nothing to say what it is deprecated for, or whose replacement has no requirement tag, is flagged on its own line.
    Given a feature file features/cart.feature with a scenario "Apply a code (deprecated)" tagged @deprecated
    And <condition>
    When the session runs `features deprecated`
    Then the line for "Apply a code (deprecated)" says <said>

    Examples:
      | condition                                                                      | said                                      |
      | the scenario has no Deprecated for: line                                       | that it has no Deprecated for: line       |
      | it is deprecated for "Apply a voucher", and "Apply a voucher" has no @r<n> tag | that the replacement has no @r<n> tag     |

  @r61
  Scenario: the deprecated list with --json prints each deprecated scenario as one JSON object
    Pins that every deprecated scenario, with what it is deprecated for and its replacement, is in a single JSON object.
    Given a feature file features/cart.feature with a deprecated scenario "Apply a code (deprecated)" deprecated for "Apply a voucher"
    And a scenario "Apply a voucher" tagged @r3 in features/codes.feature
    And a deprecated scenario "Empty cart (deprecated)" in features/cart.feature deprecated for removal
    When the session runs `features deprecated --json`
    Then the output is one JSON object
    And it gives "Apply a code (deprecated)" deprecated for "Apply a voucher", with its replacement in features/codes.feature tagged @r3
    And it gives "Empty cart (deprecated)" deprecated for removal

  @r29
  Scenario: rebinding to a title several feature files have is refused
    The new title must pick out one scenario.
    Given a test module binding "Apply a code"
    And features/cart.feature and features/codes.feature both have a scenario "Apply a voucher"
    When the session runs `features rebind "Apply a code" "Apply a voucher"`
    Then the command is rejected because several feature files have the new title
    And no test module is changed

  @r29
  Scenario: rebinding a title written over several lines is refused
    A binding whose title string spans lines is not rewritten.
    Given a feature file with a scenario "Apply a voucher"
    And a test module tests/test_cart.py whose binding call at line 20 names "Apply a code" in a string written over several lines
    When the session runs `features rebind "Apply a code" "Apply a voucher"`
    Then the command is rejected because the binding's title is written over several lines
    And no test module is changed

  @r46
  Scenario: a refusal says why on stderr and fails
    Whatever is refused, the reason goes to stderr and the command fails.
    Given a feature file features/cart.feature with a scenario "Apply a code" not tagged @deprecated
    When the session runs `features retire "Apply a code"`
    Then the reason for the refusal is written to stderr
    And it exits with an error

  @r51
  Scenario Outline: tagging with a requirement id makes it the scenario's one requirement tag
    Pins that @r<n> takes the place of every @r<m> tag the scenario has, or joins its tags when it has none, and that its other tags and every other line stay as they were.
    Given a feature file features/cart.feature whose only scenario "Apply a code" has the tags <tags before>
    When the session runs `features tag "Apply a code" r7`
    Then the scenario's tags are <tags after>
    And every other line of features/cart.feature is unchanged

    Examples:
      | tags before                 | tags after             |
      | @wip, @slice-2, @r1 and @r4 | @wip, @slice-2 and @r7 |
      | @wip and @slice-2           | @wip, @slice-2 and @r7 |

  @r52
  Scenario: --file works in that file only, whatever other files have the title
    A title two files have is tagged in either file by naming it, and nothing else in either file changes.
    `tag` is the example; `deprecate`, `retire` and `move` look for the title in the named file the same way.
    Given features/cart.feature and features/old.feature both have a scenario "Apply a code"
    When the session runs `features tag "Apply a code" r7 --file features/cart.feature`
    Then the scenario "Apply a code" in features/cart.feature is tagged @r7
    And every other line of features/cart.feature is unchanged
    And features/old.feature is unchanged

  @r35
  Scenario: --file naming a file that does not have the title is refused
    The file named must have the title, or the command stops.
    Given a feature file features/cart.feature without a scenario "Voucher"
    And features/codes.feature has a scenario "Voucher"
    When the session runs `features tag "Voucher" r7 --file features/cart.feature`
    Then the command is rejected because the file does not have the title
    And the refusal names features/cart.feature
    And no file is changed

  @r35
  Scenario: --file naming a file that has the title twice is refused
    Two scenarios with the title in the file named leave no one scenario to work on.
    Given a feature file features/cart.feature with two scenarios "Apply a code"
    When the session runs `features tag "Apply a code" r7 --file features/cart.feature`
    Then the command is rejected because the file has the title twice
    And the refusal names features/cart.feature
    And no file is changed

  @r35
  Scenario: --file naming a file outside --dir is refused
    A file outside the directory features reads is not one it edits.
    Given a feature file elsewhere/other.feature outside the features directory with a scenario "Apply a code"
    When the session runs `features tag "Apply a code" r7 --file elsewhere/other.feature`
    Then the command is rejected because the file is outside --dir
    And no file is changed

  @r35
  Scenario: --to naming a file outside --dir is refused
    A move never takes a scenario to a file outside the directory features reads.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    And a feature file elsewhere/other.feature outside the features directory
    When the session runs `features move "Apply a code" --to elsewhere/other.feature`
    Then the command is rejected because the destination is outside --dir
    And the refusal names features/cart.feature
    And no file is changed

  @r56
  Scenario: rebind --file rewrites only the bindings whose feature names that file
    After the scenario in one of two files with a title is deprecated, only the bindings of that file follow it.
    Given tests binding "Apply a code" to features/cart.feature and to features/old.feature
    When the session runs `features rebind "Apply a code" "Apply a code (deprecated)" --file features/cart.feature`
    Then the binding to features/cart.feature names "Apply a code (deprecated)"
    And the binding to features/old.feature is unchanged
