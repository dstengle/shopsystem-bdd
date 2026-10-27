# formulated from spec/capabilities/supervision.md
Feature: Supervision
  Narrator: the person who started `work run`

  # [r136] **While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised.
  @r136
  Scenario: a formulated capability-proposal whose integrate round raised the lines of a request into an upstream gets no work-item while that request is not delivered
    Pins that work waiting on an upstream does not begin before the upstream delivers it, and that only the proposal those lines came with waits, not the initiative's other proposals.
    Given i1 is started and fulfils the request q1, and i1's capability-proposal p1 is formulated, its adds naming thing#r1, and i1's capability-proposal p2 is formulated, its adds naming other#r4
    And p1 was written by an integrate round that gave the lines of a request into the upstream catalogue: "When a book is listed, the catalogue shall give its edition.", and p2 by an integrate round that gave no lines into an upstream
    And the request q2 in catalogue, with the line "When a book is listed, the catalogue shall give its edition." as its one line, is raised by i1 for q1 and is awaiting-upstream
    And every worker gives DONE
    When the person runs `work run i1`
    Then `work add` drafted no work-item part of p1
    And `work add` drafted one work-item in i1, part of p2: under other accepting other#r4
