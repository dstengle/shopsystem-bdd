# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # [r118] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`.
  @r118
  Scenario: under a delegation, an answer to a reviewer's question that asks for a change returns the work-item to ready
    Pins that a work-item whose review a session answered in the person's place goes back to its implementer when the answer wants it changed, without the person.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
    And the session answering under the delegation answers "No, remove the old reader.", an answer that asks for a change, and every worker gives DONE
    When the person runs `work run i1`
    Then w1's transition from awaiting-answer to ready was made once the session had answered

  # [r119] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that accepts the work-item as it is, `work run` shall transition the work-item to `done`.
  @r119
  Scenario: under a delegation, an answer to a reviewer's question that accepts the work-item as it is transitions the work-item to done
    Pins that a work-item whose review a session answered in the person's place moves on as it stands, not back to its implementer, when the answer takes it as it is, without the person.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
    And the session answering under the delegation answers "Yes, keep it as it is.", an answer that accepts the work-item as it is, and every worker gives DONE
    When the person runs `work run i1`
    Then w1's transition from awaiting-answer to done was made once the session had answered
