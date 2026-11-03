# generated from spec/capabilities/feature-file-tools.md by features generate; do not edit
Feature: Feature file tools
  Narrator: a session reading or generating feature files

  @g1 @r1
  Scenario: `features count --by-tag` counts every scenario, and a docstring's text is none
    Given a feature file `features/notes.feature`
    When the person runs `features count --by-tag`
    Then `features` prints the number of scenarios

  @g2 @r2
  Scenario: `features count --by-tag` counts a Scenario Outline once for each Examples row
    Given a feature file `features/outline.feature`
    When the person runs `features count --by-tag`
    Then `features` prints the number of scenarios

  @g3 @r3 @r4
  Scenario: a docstring's text is no tag
    Given a feature file `features/notes.feature`
    When the person runs `features list --tag slice-9`
    Then `features` does not print the feature file `features/notes.feature`
    And `features` exits successfully

  @g4 @r5
  Scenario: every feature file under the directory is read, however deep
    Given the feature file `features/sub/deep.feature` holds:
      """
      Feature: Deep
        Scenario: Deep down
          Given a step
      """
    When the person runs `features list --title Deep`
    Then `features` prints the feature file `features/sub/deep.feature`

  @g5 @r6
  Scenario: `features list --tag` prints each scenario whose tags, its feature's included, have the tag
    Given the feature file `features/cart.feature` holds:
      """
      @cart
      Feature: Cart
        Scenario: Adding
          Given a step
      """
    When the person runs `features list --tag cart`
    Then `features` prints the feature file `features/cart.feature` and "Adding"

  @g6 @r7
  Scenario: `features list --title` prints each scenario whose title holds the text
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
        Scenario: Paying
          Given a step
      """
    When the person runs `features list --title Add`
    Then `features` prints the feature file `features/cart.feature` and "Adding"

  @g7 @r8
  Scenario: `features list --json` prints the scenarios it found as one JSON object
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
      """
    And `--json` is given
    When the person runs `features list --title Add`
    Then `features` prints the feature file `features/cart.feature` and "Adding"

  @g8 @r9
  Scenario: a feature file with a `Rule:` block is refused
    Given a feature file `features/rule.feature`
    When the person runs `features count --by-tag`
    Then `features` exits with an error naming the feature file `features/rule.feature`
    And `features` changes nothing

  @g9 @r10
  Scenario: `features deprecated` prints each deprecated scenario with what replaces it
    Given the feature file `features/shelf.feature` holds:
      """
      Feature: Shelf
        @deprecated
        Scenario: Lending (deprecated)
          Deprecated for: Lending a book
          Given a step
        @r4
        Scenario: Lending a book
          Given a step
      """
    When the person runs `features deprecated`
    Then `features` prints "Lending" and "@r4"

  @g10 @r11
  Scenario: `features deprecated` says when nothing is deprecated
    Given the feature file `features/shelf.feature` holds:
      """
      Feature: Shelf
        Scenario: Lending
          Given a step
      """
    When the person runs `features deprecated`
    Then `features` prints "none deprecated"

  @g11 @r12
  Scenario: `features deprecated --json` prints the deprecated scenarios as one JSON object
    Given the feature file `features/shelf.feature` holds:
      """
      Feature: Shelf
        @deprecated
        Scenario: Lending (deprecated)
          Deprecated for: removal
          Given a step
      """
    And `--json` is given
    When the person runs `features deprecated`
    Then `features` prints "Lending"

  @g12 @r13 @r14
  Scenario: `features bindings` says so when every binding names a scenario
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
      """
    And the test module `tests/test_cart.py` holds:
      """
      from pytest_bdd import scenario
      @scenario("cart.feature", "Adding")
      def test_adding():
          pass
      """
    When the person runs `features bindings`
    Then `features` prints "every binding names a scenario"
    And `features` exits successfully

  @g13 @r15
  Scenario: `features bindings` names a binding whose title no feature file has
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
      """
    And the test module `tests/test_cart.py` holds:
      """
      from pytest_bdd import scenario
      @scenario("cart.feature", "Paying")
      def test_paying():
          pass
      """
    When the person runs `features bindings`
    Then `features` exits with an error naming the test module `tests/test_cart.py`
    And `features` changes nothing

  @g14 @r16
  Scenario: a `scenarios(...)` call binds every scenario of the feature file it names
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
        Scenario: Paying
          Given a step
      """
    And the test module `tests/test_cart.py` holds:
      """
      from pytest_bdd import scenarios
      scenarios("cart.feature")
      """
    When the person runs `features bindings --unbound`
    Then `features` exits successfully

  @g15 @r17
  Scenario: `features bindings --unbound` names a scenario no test binds
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
        Scenario: Paying
          Given a step
      """
    And the test module `tests/test_cart.py` holds:
      """
      from pytest_bdd import scenario
      @scenario("cart.feature", "Adding")
      def test_adding():
          pass
      """
    When the person runs `features bindings --unbound`
    Then `features` exits with an error naming "Paying"
    And `features` changes nothing

  @g16 @r18
  Scenario: `features bindings --json` prints what it found wrong as one JSON object
    Given the feature file `features/cart.feature` holds:
      """
      Feature: Cart
        Scenario: Adding
          Given a step
        Scenario: Paying
          Given a step
      """
    And the test module `tests/test_cart.py` holds:
      """
      from pytest_bdd import scenario
      @scenario("cart.feature", "Adding")
      def test_adding():
          pass
      """
    And `--json` is given
    When the person runs `features bindings --unbound`
    Then `features` prints "Paying"

  @g17 @r19 @r20
  Scenario: `features generate` writes the feature file of a codified service capability
    Given a term `book`
    And a capability `shelf`
    And a feature file `features/shelf.feature`
    When the person runs `features generate`
    Then `features` prints the feature file `features/shelf.feature`
    And `features` exits successfully

  @g18 @r21
  Scenario: `features generate --check` names a feature file that differs from its capability
    Given a term `book`
    And a capability `shelf`
    And the feature file `features/shelf.feature` holds:
      """
      Feature: Shelf
        Scenario: Edited by hand
          Given a step
      """
    And `--check` is given
    When the person runs `features generate`
    Then `features` exits with an error naming the feature file `features/shelf.feature`
    And `features` changes nothing

  @g19 @r23
  Scenario: `features vocab --check` names a step with no handler
    Given a term `book`
    And a capability `shelf`
    And a feature file `features/shelf.feature`
    When the person runs `features vocab --check`
    Then `features` exits with an error naming the feature file `features/shelf.feature`
    And `features` changes nothing
