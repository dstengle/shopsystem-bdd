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
