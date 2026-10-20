# formulated from spec/capabilities/feature-file-tools.md
Feature: Feature file tools
  Narrator: an agent or session editing feature files

  @r1
  Scenario: every feature file under the directory is read, and docstring text is not
    A feature file in a nested directory under the default features directory is read, and a tag or scenario written inside a docstring is not.
    Given a feature file features/cart/nested.feature with a scenario "Nested" tagged @slice-1
    And the scenario "Nested" has a docstring holding the lines "@slice-1" and "Scenario: Phantom"
    When the agent runs features list --tag slice-1 without --dir
    Then the output lists features/cart/nested.feature with "Nested"
    And the output does not list "Phantom"

  @r2
  Scenario: a feature file with a Rule block is refused
    A Rule block is not read as part of the feature; the command refuses and says which file holds it.
    Given a feature file features/rules.feature that holds a Rule: block
    When the agent runs features list --title Cart
    Then the command is rejected because the feature file holds a Rule: block
    And the refusal names features/rules.feature

  @r2
  Scenario Outline: an edit is refused only when it would leave a Rule: block outside a docstring
    Pins that the one thing an edit's result is checked for is a Rule: block outside a docstring, and that a refused edit changes no file.
    Given an edit by features that would leave features/cart.feature holding <result>
    When the agent runs that edit
    Then <outcome>

    Examples:
      | result                                       | outcome                                                                                                      |
      | a Rule: block outside a docstring            | the edit is rejected because features could not read the result, and every file is as it was                 |
      | a Rule: line inside a docstring              | the edit is made                                                                                             |
      | two scenarios titled "Apply a code"          | the edit is made                                                                                             |

  @r4
  Scenario: counting by tag counts outline rows, inherited tags and untagged scenarios
    Pins that each Examples row is a scenario carrying its feature's and its own table's tags, and that the total leaves no scenario out.
    Given a feature file features/cart.feature tagged @cart
    And it has a scenario "Plain" with no tags of its own
    And it has a scenario "Own tag" tagged @slice-1
    And it has a Scenario Outline "Outlined" tagged @slice-2 with an Examples table tagged @r3 of 2 rows and an untagged Examples table of 1 row
    And a feature file features/misc.feature with no tags has a scenario "Untagged" with no tags
    When the agent runs features count --by-tag
    Then it prints 5 scenarios for cart, 1 for slice-1, 3 for slice-2 and 2 for r3
    And it prints a total of 6

  @r5
  Scenario: listing by tag includes the feature's and the Examples' tags
    A scenario holds a tag when it carries it itself, when its feature carries it, or when its Examples table carries it.
    Given a feature file features/cart.feature tagged @cart
    And it has a scenario "Plain" with no tags of its own
    And it has a scenario "Own tag" tagged @checkout
    And it has a Scenario Outline "Outlined" whose one Examples table is tagged @checkout and has one row
    And another feature file features/stock.feature tagged @checkout has a scenario "Elsewhere"
    And a feature file features/misc.feature has a scenario "Untagged" with no tags
    When the agent runs features list --tag checkout
    Then the output lists features/cart.feature with "Own tag"
    And the output lists features/cart.feature with "Outlined"
    And the output lists features/stock.feature with "Elsewhere"
    And the output does not list "Plain" or "Untagged"

  @r5
  Scenario: listing by title finds every scenario whose title contains the text
    A title matches when the text appears anywhere in it, not only when it equals it.
    Given a feature file features/cart.feature with scenarios "Apply a code", "Code expired" and "Empty cart"
    When the agent runs features list --title "ode"
    Then the output lists features/cart.feature with "Apply a code"
    And the output lists features/cart.feature with "Code expired"
    And the output does not list "Empty cart"

  @r7
  Scenario: listing that matches nothing prints nothing and fails
    An empty result is not a success.
    Given a feature file features/cart.feature with no scenario tagged @slice-9
    When the agent runs features list --tag slice-9
    Then nothing is printed
    And it exits 1

  @r35
  Scenario Outline: retagging a title that is not in exactly one file is refused
    The title must pick out one file; otherwise nothing is changed and every file holding it is named.
    Given the title "Apply a code" is held by <files holding it>
    When the agent runs features tag "Apply a code" slice-2
    Then the command is rejected because the title is not held by exactly one file
    And the refusal names <files named>
    And no file is changed

    Examples:
      | files holding it                               | files named                                    |
      | no feature file                                | no file                                        |
      | features/cart.feature and features/old.feature | features/cart.feature and features/old.feature |

  @r46
  Scenario: retagging with a tag that is not a requirement tag is bad usage
    Only r<n> is a tag features tag accepts.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the agent runs features tag "Apply a code" wip
    Then the command is rejected as bad usage because the tag is not written r<n>
    And no file is changed

  @r12
  Scenario: moving a scenario takes its block to the end of the destination
    The block leaves its source file and arrives unchanged after everything already in the destination.
    Given a feature file features/old.feature with scenarios "Apply a code" and "Empty cart"
    And a feature file features/cart.feature whose last scenario is "Checkout"
    When the agent runs features move "Apply a code" --to features/cart.feature
    Then features/old.feature holds "Empty cart" and not "Apply a code"
    And the block of "Apply a code" follows "Checkout" at the end of features/cart.feature, unchanged

  @r13
  Scenario: moving with the Background inlined puts its steps first
    A moved scenario keeps the steps its source Background gave it.
    Given a feature file features/old.feature whose Background has the step "Given the date is 2026-10-16"
    And its scenario "Apply a code" has first step "Given a cart holding product Mug at price 8.00"
    And a feature file features/cart.feature
    When the agent runs features move "Apply a code" --to features/cart.feature --inline-background
    Then the moved "Apply a code" has the steps "Given the date is 2026-10-16" then "Given a cart holding product Mug at price 8.00"

  @r14
  Scenario Outline: moving with feature tags kept adds the missing ones on a tag line of their own
    Pins that only the feature tags the destination lacks are kept, on their own line just above the Scenario: line, with the scenario's own tag lines left as they were.
    Given a feature file features/old.feature with the feature tags @cart and @checkout
    And its scenario "Apply a code" has <own tag lines>
    And a feature file features/cart.feature with the feature tag @cart
    When the agent runs features move "Apply a code" --to features/cart.feature --keep-feature-tags
    Then the moved "Apply a code" has the tag lines <tag lines after>, the last directly above its Scenario: line

    Examples:
      | own tag lines           | tag lines after             |
      | the tag line "@slice-2" | "@slice-2" then "@checkout" |
      | no tag line             | "@checkout"                 |

  @r46
  Scenario: moving to a destination that does not exist is refused
    A move never creates a file.
    Given a feature file features/old.feature with a scenario "Apply a code"
    And no file features/missing.feature
    When the agent runs features move "Apply a code" --to features/missing.feature
    Then the command is rejected because the destination does not exist
    And no file is changed

  @r16
  Scenario: two trees alike scenario by scenario pass the move check
    Scenarios may sit in other files, but alike by title in tags, description and steps they all match.
    Given a tree old/ with "Apply a code" and "Empty cart" in old/cart.feature
    And a tree features/ with "Apply a code" in features/codes.feature and "Empty cart" in features/cart.feature, each alike in effective tags, description, Background and own steps
    When the agent runs features verify-moved --from old
    Then it prints that 2 scenarios match
    And it exits 0

  @r17
  Scenario Outline: a scenario that changed in the move is named with what changed
    The check names which of effective tags, description or steps differ.
    Given trees old/ and features/ that both hold "Apply a code"
    And the two copies of "Apply a code" differ in their <part>
    When the agent runs features verify-moved --from old
    Then it names "Apply a code" with its <part> as changed
    And it exits 1

    Examples:
      | part           |
      | effective tags |
      | description    |
      | steps          |

  @r17
  Scenario Outline: a title held twice in either tree is a duplicate
    Scenarios are matched by title, so a title held twice cannot be matched.
    Given trees old/ and features/ that both hold "Apply a code"
    And <tree> holds a second scenario titled "Apply a code"
    When the agent runs features verify-moved --from old
    Then it names "Apply a code" as a duplicate
    And it exits 1

    Examples:
      | tree      |
      | old/      |
      | features/ |

  @r19
  Scenario Outline: deprecating a scenario marks it deprecated and records what for
    A deprecated scenario has the tag @deprecated, a "(deprecated)" title and a line naming what it is deprecated for, and nothing else in it changes.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    And <replacement>
    When the agent runs features deprecate "Apply a code" <option>
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
    When the agent runs features deprecate "Apply a code (deprecated)" --for "Apply a voucher"
    Then the command is rejected because the scenario is already deprecated

  @r21
  Scenario Outline: the deprecated list shows each deprecated scenario and what will retire it
    For each deprecated scenario the list says what it is deprecated for and where its replacement stands.
    Given a feature file features/cart.feature with a deprecated scenario "Apply a code (deprecated)" deprecated for <deprecated for>
    And <replacement>
    When the agent runs features deprecated
    Then the list shows "Apply a code (deprecated)" deprecated for <deprecated for>, with <shown>

    Examples:
      | deprecated for    | replacement                                                       | shown                                            |
      | "Apply a voucher" | a scenario "Apply a voucher" tagged @r3 in features/codes.feature | features/codes.feature and @r3                   |
      | "Apply a voucher" | no scenario titled "Apply a voucher"                              | that no scenario has the title "Apply a voucher" |
      | removal           | no replacement                                                    | that it is deprecated for removal                |

  @r21
  Scenario: the deprecated list says when nothing is deprecated
    An empty list is stated, not left blank.
    Given feature files in which no scenario is tagged @deprecated
    When the agent runs features deprecated
    Then it says that none is deprecated

  @r23
  Scenario: retiring a deprecated scenario removes its block
    Only the deprecated scenario's block goes; the rest of the file stays as it was.
    Given a feature file features/cart.feature with a scenario "Empty cart" and a scenario "Apply a code (deprecated)" tagged @deprecated
    When the agent runs features retire "Apply a code (deprecated)"
    Then features/cart.feature no longer holds "Apply a code (deprecated)"
    And the rest of features/cart.feature is as it was

  @r24
  Scenario: retiring a scenario that is not deprecated is refused
    Only a deprecated scenario can be retired.
    Given a feature file features/cart.feature with a scenario "Apply a code" not tagged @deprecated
    When the agent runs features retire "Apply a code"
    Then the command is rejected because the scenario is not deprecated
    And features/cart.feature is as it was

  @r25
  Scenario Outline: a binding that names no scenario is reported
    A binding fails when no feature file has its title, or when the feature it names does not have it.
    Given a test module tests/test_cart.py whose line 12 binds the title "Apply a code" in the feature cart.feature
    And <where the title is>
    When the agent runs features bindings without --tests
    Then it reports tests/test_cart.py, line 12, the title "Apply a code" and the feature cart.feature
    And it exits 1

    Examples:
      | where the title is                                       |
      | no feature file has the title "Apply a code"             |
      | only features/codes.feature has the title "Apply a code" |

  @r26
  Scenario: bindings that all name a scenario pass
    The check says so when every binding is good.
    Given a test module tests/test_cart.py binding "Apply a code" in cart.feature
    And features/cart.feature has the scenario "Apply a code"
    When the agent runs features bindings
    Then it says that every binding names a scenario
    And it exits 0

  @r46
  Scenario: a test module that does not parse is refused
    Bindings cannot be read from a module that does not parse, and the module is named.
    Given a test module tests/test_broken.py that does not parse
    When the agent runs features bindings
    Then the command is rejected because the test module does not parse
    And the refusal names tests/test_broken.py

  @r28
  Scenario Outline: rebinding rewrites each binding of the old title and counts them
    Only the title in the binding calls changes, and the count is printed even when it is zero.
    Given a feature file features/cart.feature with a scenario "Apply a voucher"
    And test modules with <bindings> binding calls naming "Apply a code"
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then each of those binding calls names "Apply a voucher"
    And nothing else in the test modules is changed
    And it prints that <bindings> bindings were rebound

    Examples:
      | bindings |
      | 2        |
      | 0        |

  @r29
  Scenario: rebinding to a title no scenario has is refused
    A binding is never pointed at a scenario that does not exist.
    Given a test module binding "Apply a code"
    And no feature file has a scenario "Apply a voucher"
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then the command is rejected because no scenario has the new title
    And no test module is changed

  @r35
  Scenario Outline: moving a title that no file or several files hold is refused
    Without --file, a move, deprecate or retire needs the title in exactly one file; a refusal names every file that holds it.
    Given <holders> the title "Apply a code"
    When the agent runs features move "Apply a code" --to features/codes.feature without --file
    Then the command is rejected because <reason>
    And the refusal names <named>
    And no file is changed

    Examples:
      | holders                                                  | reason                       | named                                          |
      | no feature file holds                                    | no file holds the title      | no file                                        |
      | features/cart.feature and features/old.feature both hold | several files hold the title | features/cart.feature and features/old.feature |

  @r46
  Scenario: moving a scenario to its own file is refused
    A move must take the scenario somewhere else.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the agent runs features move "Apply a code" --to features/cart.feature
    Then the command is rejected because the destination is the scenario's own file
    And no file is changed

  @r17
  Scenario Outline: a title in only one tree is missing or added
    Every title must be in both trees; one in only the source is missing, one in only the other is added.
    Given trees old/ and features/
    And the title "Apply a code" is only in <tree>
    When the agent runs features verify-moved --from old
    Then it names "Apply a code" as <named as>
    And it exits 1

    Examples:
      | tree      | named as |
      | old/      | missing  |
      | features/ | added    |

  @r5
  Scenario Outline: a tag is found with or without its leading @
    The leading @ is optional when listing by tag.
    Given a feature file features/cart.feature with a scenario "Apply a code" tagged @slice-2
    When the agent runs features list --tag <tag>
    Then the output lists features/cart.feature with "Apply a code"

    Examples:
      | tag      |
      | @slice-2 |
      | slice-2  |

  @r19
  Scenario: deprecating a scenario prints its file and new title
    The agent sees where the deprecated scenario is and what it is now called.
    Given a feature file features/cart.feature with a scenario "Apply a code"
    When the agent runs features deprecate "Apply a code" --for-removal
    Then it prints features/cart.feature and "Apply a code (deprecated)"

  @r21
  Scenario Outline: the deprecated list flags a deprecated scenario it cannot place
    A deprecated scenario with nothing to say what it is deprecated for, or whose replacement has no requirement tag, is flagged on its own line.
    Given a feature file features/cart.feature with a scenario "Apply a code (deprecated)" tagged @deprecated
    And <condition>
    When the agent runs features deprecated
    Then the line for "Apply a code (deprecated)" says <said>

    Examples:
      | condition                                                                      | said                                      |
      | the scenario has no Deprecated for: line                                       | that it has no Deprecated for: line       |
      | it is deprecated for "Apply a voucher", and "Apply a voucher" has no @r<n> tag | that the replacement carries no @r<n> tag |

  @r29
  Scenario: rebinding to a title several feature files hold is refused
    The new title must pick out one scenario.
    Given a test module binding "Apply a code"
    And features/cart.feature and features/codes.feature both hold a scenario "Apply a voucher"
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then the command is rejected because several feature files hold the new title
    And no test module is changed

  @r29
  Scenario: rebinding a title written over several lines is refused
    A binding whose title string spans lines is not rewritten, and the module and line are named.
    Given a feature file with a scenario "Apply a voucher"
    And a test module tests/test_cart.py whose binding call at line 20 names "Apply a code" in a string written over several lines
    When the agent runs features rebind "Apply a code" "Apply a voucher"
    Then the command is rejected because the binding's title is written over several lines
    And the refusal names tests/test_cart.py and line 20
    And no test module is changed

  @r46
  Scenario: a refusal says why on stderr and fails
    Whatever is refused, the reason goes to stderr and the command fails.
    Given a feature file features/cart.feature with a scenario "Apply a code" not tagged @deprecated
    When the agent runs features retire "Apply a code"
    Then the reason for the refusal is written to stderr
    And it exits 1

  @r51
  Scenario: tagging with a requirement id adds it to the scenario's requirement tags
    The new @r<n> joins the scenario's tags; its other tags, other @r<m> tags included, and every other line stay as they were.
    Given a feature file features/cart.feature whose only scenario "Apply a code" has the tags @wip, @slice-2, @r1 and @r4
    When the agent runs features tag "Apply a code" r7
    Then the scenario's tags are @wip, @slice-2, @r1, @r4 and @r7
    And every other line of features/cart.feature is unchanged

  @r51 @deprecated
  Scenario: tagging with a requirement id makes it the scenario's one requirement tag (deprecated)
    Deprecated for: tagging with a requirement id adds it to the scenario's requirement tags
    A scenario ends with one @r<n> tag, the new one, and keeps every other tag and line.
    Given a feature file features/cart.feature whose only scenario "Apply a code" has the tags @wip, @slice-2, @r1 and @r4
    When the agent runs features tag "Apply a code" r7
    Then the scenario's tags are @wip, @slice-2 and @r7
    And every other line of features/cart.feature is unchanged

  @r52
  Scenario: --file works in that file only, whatever other files hold the title
    A title two files hold is tagged in either file by naming it, and nothing else in either file changes.
    tag is the example; deprecate, retire and move look for the title in the named file the same way.
    Given features/cart.feature and features/old.feature both hold a scenario "Apply a code"
    When the agent runs features tag "Apply a code" r7 --file features/cart.feature
    Then the scenario "Apply a code" in features/cart.feature is tagged @r7
    And every other line of features/cart.feature is unchanged
    And features/old.feature is unchanged

  @r35
  Scenario: --file naming a file that does not hold the title is refused
    The file named must hold the title, or the command stops.
    Given a feature file features/cart.feature without a scenario "Voucher"
    And features/codes.feature holds a scenario "Voucher"
    When the agent runs features tag "Voucher" r7 --file features/cart.feature
    Then the command is rejected because the file does not hold the title
    And the refusal names features/cart.feature
    And no file is changed

  @r35
  Scenario: --file naming a file that holds the title twice is refused
    Two scenarios with the title in the file named leave no one scenario to work on.
    Given a feature file features/cart.feature with two scenarios "Apply a code"
    When the agent runs features tag "Apply a code" r7 --file features/cart.feature
    Then the command is rejected because the file holds the title twice
    And the refusal names features/cart.feature
    And no file is changed

  @r35
  Scenario: --file naming a file outside --dir is refused
    A file outside the directory features reads is not one it edits.
    Given a feature file elsewhere/other.feature outside the features directory with a scenario "Apply a code"
    When the agent runs features tag "Apply a code" r7 --file elsewhere/other.feature
    Then the command is rejected because the file is outside --dir
    And no file is changed

  @r56
  Scenario: rebind --file rewrites only the bindings whose feature names that file
    After one of two files holding a title is held, only the bindings of that file follow it.
    Given tests binding "Apply a code" to features/cart.feature and to features/old.feature
    When the agent runs features rebind "Apply a code" "Apply a code (held)" --file features/cart.feature
    Then the binding to features/cart.feature names "Apply a code (held)"
    And the binding to features/old.feature is unchanged
