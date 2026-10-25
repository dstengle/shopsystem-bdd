# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # r120: **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is.
  # placed after @r119 and before @r89, in the lines' order
  @r120
  Scenario: under a delegation, the session answering a reviewer's question is asked to say in its result whether its answer asks for a change or accepts the work-item as it is
    Pins that the brief of a session answering a reviewer's question in the person's place asks the session to say which way its answer goes, so that `work run` can tell from the result alone.
    Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
    And the session answering under the delegation answers "Yes, keep it as it is.", and every worker gives DONE
    When the person runs `work run i1`
    Then the brief of the session answering "Is the old reader kept?" asks it to give in its result whether its answer asks for a change or accepts w1 as it is
