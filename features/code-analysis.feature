# generated from spec/capabilities/code-analysis.md by features generate; do not edit
Feature: Code analysis
  Narrator: the person

  @g1 @r1
  Scenario: A coverage map is kept while a test breaks
    Given a test t1
    And the test t1 breaks
    When the person maps this repository
    Then the code analysis service keeps the coverage map c1
    And the code analysis service completes this request

  @g2 @r2
  Scenario: Mapping replaces the coverage map
    Given a coverage map c1
    And the coverage map c1 exists
    And a coverage map c2
    When the person maps this repository
    Then the code analysis service keeps the coverage map c2

  @g3 @r3
  Scenario: A function traced gives the tests that execute it
    Given a coverage map c1
    And the coverage map c1 exists
    And a function f1
    And a test t1
    And the test t1 executes the function f1
    And a test t2
    And the test t2 executes the function f1
    And a test t3
    And the test t3 does not execute the function f1
    And a test t4
    And the test t4 executes the function f1
    And a test t5
    And the test t5 executes the function f1
    When the person traces the function f1
    Then the code analysis service returns the test t1
    And the code analysis service returns the test t2
    And the code analysis service does not return the test t3
    And the code analysis service returns the number of tests that execute the function f1
    And the code analysis service returns the revision of the coverage map c1

  @g4 @r4
  Scenario: A function traced by file gives the Python files of its tests
    Given a coverage map c1
    And the coverage map c1 exists
    And a function f1
    And a Python file p1
    And a test t1
    And the test t1 executes the function f1
    And the Python file p1 holds the test t1
    And a Python file p2
    And a test t2
    And the test t2 executes the function f1
    And the Python file p2 holds the test t2
    And a Python file p3
    And a test t3
    And the test t3 executes the function f1
    And the Python file p3 does not hold the test t3
    When the person traces the function f1 with the file view
    Then the code analysis service returns the Python file p1
    And the code analysis service returns the Python file p2
    And the code analysis service does not return the Python file p3

  @g5 @r5
  Scenario: A function no test executes traced gives the coverage map's commit
    Given a coverage map c1
    And the coverage map c1 exists
    And a function f1
    And no test executes the function f1
    When the person traces the function f1
    Then the code analysis service returns the revision of the coverage map c1
    And the code analysis service completes this request

  @g6 @r6
  Scenario: An identifier no Python file defines is not traced
    Given a coverage map c1
    And the coverage map c1 exists
    And an identifier i1
    And no Python file defines the identifier i1
    When the person traces the identifier i1
    Then the code analysis service refuses this request
    And the code analysis service names the identifier i1

  @g7 @r7
  Scenario: A function is not traced with no coverage map
    Given no coverage map exists
    And a function f1
    When the person traces the function f1
    Then the code analysis service refuses this request
    And the code analysis service names this coverage map

  @g8 @r8
  Scenario: A Python file screened gives its functions no test executes
    Given a coverage map c1
    And the coverage map c1 exists
    And a Python file p1
    And a function f1
    And the Python file p1 has the function f1
    And no test executes the function f1
    And a function f2
    And the Python file p1 has the function f2
    And no test executes the function f2
    And a function f3
    And no test executes the function f3
    And the Python file p1 does not have the function f3
    When the person screens the Python file p1
    Then the code analysis service returns the function f1
    And the code analysis service returns the function f2
    And the code analysis service does not return the function f3
    And the code analysis service returns the revision of the coverage map c1
    And the code analysis service completes this request

  @g9 @r9
  Scenario: An identifier located gives its references
    Given a Python file p1
    And an identifier i1
    And the Python file p1 defines the identifier i1
    And a reference r1
    And the reference r1 is to the identifier i1
    And a reference r2
    And the reference r2 is to the identifier i1
    And a reference r3
    And the reference r3 is not to the identifier i1
    And a reference r4
    And the reference r4 is to the identifier i1
    And a reference r5
    And the reference r5 is to the identifier i1
    When the person locates the identifier i1
    Then the code analysis service returns the reference r1
    And the code analysis service returns the reference r2
    And the code analysis service does not return the reference r3
    And the code analysis service returns the number of references to the identifier i1
    And the code analysis service completes this request

  @g10 @r10
  Scenario: An identifier no Python file defines is not located
    Given an identifier i1
    And no Python file defines the identifier i1
    When the person locates the identifier i1
    Then the code analysis service refuses this request
    And the code analysis service names the identifier i1

  @g11 @r11
  Scenario: A file linted gives each finding under its analysis tool and fails
    Given a finding f2
    And an analysis tool a1
    And the analysis tool a1 has the finding f2
    And a file f1
    And the file f1 holds the finding f2
    And a heading h1
    And the analysis tool a1 has the heading h1
    When the person lints the file f1
    Then the code analysis service returns the heading h1
    And the code analysis service returns the finding f2
    And the code analysis service fails this check
    And the code analysis service names the finding f2

  @g12 @r12
  Scenario: Linting fails while `vulture` is missing
    Given the presence of `vulture` is `missing`
    And a file f1
    When the person lints the file f1
    Then the code analysis service fails this check
    And the code analysis service names `vulture`

  @g13 @r13
  Scenario: A Python file over the size limit fails the sizing
    Given a Python file p1
    And a size limit s1
    And the Python file p1 exceeds the size limit s1
    When the person sizes this repository with the size limit s1
    Then the code analysis service returns the Python file p1
    And the code analysis service fails this check
    And the code analysis service names the Python file p1

  @g14 @r14
  Scenario: Sizing passes when no Python file exceeds the default limit
    Given no Python file exceeds `300`
    When the person sizes this repository without a size limit
    Then the code analysis service completes this request
