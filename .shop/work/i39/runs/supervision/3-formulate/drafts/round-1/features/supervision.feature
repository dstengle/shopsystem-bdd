# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # supervision#r135: **When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation.
  # Placed after @r92 and before @r107.
  @r135
  Scenario: the lines an integrate round gives into an upstream are raised with `work request`, raised for the request the initiative fulfils and with its delegation
    Pins that what an integration needs from an upstream reaches that upstream as a request tied to the request it serves and answerable under the same delegation.
    Given i1 is proposed and fulfils the request q1, whose line 1 has the line outcome accepted, and which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
    And the integrate round for i1 gives DONE with a change list that adds thing#r4 on thing, and gives the lines of a request into the upstream catalogue: "When a book is listed, the catalogue shall give its edition."
    And every other round ends
    When the person runs `work run i1`
    Then `work request` was run for the upstream catalogue, with the line "When a book is listed, the catalogue shall give its edition." as its one line
    And the request it wrote in catalogue is raised for q1 and gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
