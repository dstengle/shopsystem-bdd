# formulated from spec/capabilities/design-model-check.md
Feature: Design model check
  Narrator: a person or session verifying a repository against the design model

  # [r120] | v17 | a request neither is part of a job-thread, cites an origin nor is raised for a request
  # replaces the scenario @r115 (retired r115)
  @r120
  Scenario: a request that is part of no job-thread, cites no origin and is raised for no request is v17
    Pins that every request says where it comes from: a job-thread, an origin or the request it is raised for.
    Given a request q1 that is part of no job-thread, cites no origin and is raised for no request
    And a request q2 that cites an observation as its origin
    And a request q3 that is part of a job-thread
    And a request q4 raised for the request request/missingmass.io/shopsystem/other/q7
    When `model check` is run
    Then v17 names q1
    And v17 does not name q2, q3 or q4

  # [r121] | v18 | an id in this context's files has another context's path on a kind kept in `.shop/work/`, judged from the id alone, other than the request a request is raised for
  # replaces the scenario @r117 (retired r117)
  # No scenario: the line admits two readings; see the question in design-model-check.reply.md.
