# generated from spec/capabilities/checking.md by features generate; do not edit
Feature: Checking
  Narrator: the person

  @g1 @r1
  Scenario: `model rules` prints every rule
    Given a rule r1
    And a rule r2
    When the person consults this rule catalogue
    Then the specification service returns the rule r1
    And the specification service returns the rule r2
    And the specification service completes this request

  @g2 @r2
  Scenario: `model forms` lists every file form
    Given a file form f1
    And a file form f2
    When the person inventories this specification
    Then the specification service returns the file form f1
    And the specification service returns the file form f2
    And the specification service completes this request

  @g3 @r3
  Scenario: the check exits successfully when nothing violates a rule
    Given no thing violates a rule
    When the person validates this specification
    Then the specification service returns `0 violations`
    And the specification service completes this request

  @g18 @r18
  Scenario: A request not of the form `work request` writes
    Given a request r1
    And the request r1 does not conform to the request form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the request r1

  @g19 @r19
  Scenario: A scenario that names a requirement its capability does not have
    Given a capability c1
    And a scenario s1
    And the scenario s1 has the capability c1
    And a requirement id r1
    And the capability c1 does not hold the requirement id r1
    And the scenario s1 refers to the requirement id r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the scenario s1

  @g20 @r20
  Scenario: A capability with no capability id
    Given a capability c1
    And the capability c1 does not conform to the capability id form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the capability c1

  @g21 @r21
  Scenario: A capability with no Behaviour section
    Given a capability c1
    And the capability c1 has no section
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the capability c1

  @g22 @r22
  Scenario: A feature file of no capability
    Given a feature f1
    And the feature f1 does not conform to the feature form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the feature f1

  @g23 @r23
  Scenario: A glossary bullet in no form of a term entry
    Given a term t1
    And the term t1 does not conform to the entry form
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

  @g24 @r24
  Scenario: A repository not on the final layout
    Given this bounded context does not conform to the final layout
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names `scripts/migrate`

  @g26 @r26
  Scenario: A context with no job has no unserved capability
    Given this bounded context has no job
    And a capability c1
    And the capability c1 violates `w_unserved_cap`
    When the person validates this specification
    Then the specification service does not return the capability c1

  @g27 @r27
  Scenario: the check tries again under an interpreter that has clingo
    Given this interpreter does not import `clingo`
    And an interpreter i1
    And the interpreter i1 imports `clingo`
    When the person validates this specification
    Then the specification service returns `0 violations`

  @g28 @r28
  Scenario: No interpreter has clingo
    Given no interpreter imports `clingo`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names this interpreter

  @g29 @r29
  Scenario: `model facts` prints the facts
    Given a fact f1
    And this bounded context has the fact f1
    And a fact f2
    And this bounded context has the fact f2
    And a fact f3
    And this bounded context does not have the fact f3
    When the person translates this specification
    Then the specification service returns the fact f1
    And the specification service returns the fact f2
    And the specification service does not return the fact f3

  @g30 @r30
  Scenario: the check refuses a verb with no frame
    Given a verb v1
    And the verb v1 has no frame
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the verb v1

  @g32 @r32
  Scenario: the check refuses a term with no part of speech
    Given a term t1
    And the term t1 has no part of speech
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the term t1

  @g33 @r33
  Scenario: the check reads a frame with a preposition
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a preposition p1
    And the frame f1 has the preposition p1
    When the person validates this specification
    Then the specification service completes this request

  @g35 @r35
  Scenario: `model rules --write` writes the rule catalogue
    When the person renews this rule catalogue
    Then the specification service keeps the rule catalogue r1
    And the specification service completes this request

  @g36 @r36
  Scenario: `model rules --check` refuses a catalogue that lacks a catalogue entry
    Given a catalogue entry c1
    And a rule catalogue r2
    And the rule catalogue r2 does not hold the catalogue entry c1
    And a rule r1
    And the rule r1 has the catalogue entry c1
    When the person renews the rule catalogue r2 with the audit
    Then the specification service fails this check
    And the specification service names the rule catalogue r2
    And the specification service does not change a file

  @g38 @r38
  Scenario: the check passes a verb with two frames
    Given a frame f1
    And a term t1
    And the term t1 has the frame f1
    And a frame f2
    And the term t1 has the frame f2
    When the person validates this specification
    Then the specification service completes this request

  @g39 @r39
  Scenario: the check passes a verb with two senses told apart by kinds
    Given a sense s1
    And a term t1
    And the term t1 has the sense s1
    And a sense s2
    And the term t1 has the sense s2
    When the person validates this specification
    Then the specification service completes this request

  @g41 @r41
  Scenario: `model lexicon` shows the terms of the imported packs
    Given a pack p1
    And this bounded context imports the pack p1
    And a term t1
    And the pack p1 has the term t1
    And a term t2
    And the pack p1 has the term t2
    And a term t3
    And the pack p1 does not have the term t3
    When the person looks up the pack p1
    Then the language service returns the term t1
    And the language service returns the term t2
    And the language service does not return the term t3
    And the language service completes this request

  @g44 @r44
  Scenario: the check passes a term marked Redefines:
    Given a term t1
    And a pack p1
    And the term t1 redefines the pack p1
    When the person validates this specification
    Then the specification service completes this request

  @g46 @r46
  Scenario: the check refuses a capability in the old language, naming `migrate upgrade`
    Given a capability c1
    And the language of the capability c1 is `codified-1`
    When the person validates this specification with the capability c1
    Then the specification service refuses this request
    And the specification service names the capability c1

  @g47 @r47
  Scenario: `model forms --check` refuses a file form written by hand
    Given a file form f1
    And the writer of the file form f1 is `hand`
    When the person inventories this specification with the audit
    Then the specification service fails this check
    And the specification service names the file form f1

  @g48 @r48
  Scenario: Each operation of an adapter contract is given the requirements that govern it
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the requirement r1 governs the operation o1
    And an operation o2
    And an adapter contract a2
    When the person annotates the adapter contract a1
    Then the operation o2 holds the requirement r1
    And the specification service keeps the adapter contract a2
    And the adapter contract a2 holds the operation o2
    And the specification service completes this request

  @g49 @r49
  Scenario: An operation missing a requirement that governs it fails the check
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the requirement r1 governs the operation o1
    And the operation o1 does not hold the requirement r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the operation o1
    And the specification service names the requirement r1

  @g50 @r50
  Scenario: An operation holding a requirement that no longer governs it fails the check
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the operation o1 holds the requirement r1
    And the requirement r1 does not govern the operation o1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the operation o1
    And the specification service names the requirement r1

  @g51 @r51
  Scenario: A stale adapter contract fails the audit
    Given an operation o1
    And an adapter contract a1
    And the adapter contract a1 holds the operation o1
    And a requirement r1
    And the requirement r1 governs the operation o1
    And the operation o1 does not hold the requirement r1
    When the person annotates the adapter contract a1 with the audit
    Then the specification service fails this check
    And the specification service names the adapter contract a1
    And the specification service does not change a file

  @g52 @r52
  Scenario: A violation of a rule fails the check under the rule's code
    Given a rule r1
    And the severity of the rule r1 is `error`
    And a capability c1
    And the capability c1 violates the rule r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the rule r1

  @g53 @r53
  Scenario: A warning is named and the check passes
    Given a rule r1
    And the severity of the rule r1 is `warning`
    And a capability c1
    And the capability c1 violates the rule r1
    And no rule whose severity is `error` exists
    When the person validates this specification
    Then the specification service names the rule r1
    And the specification service completes this request

  @g54 @r54
  Scenario: A requirement that uses a rule the rule catalogue does not define fails the check
    Given a rule r2
    And the rule r2 has no catalogue entry
    And a requirement r1
    And the requirement r1 uses the rule r2
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the rule r2

  @g55 @r55
  Scenario: A catalogue entry with no purpose fails the check
    Given a catalogue entry c1
    And the catalogue entry c1 has no purpose
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the catalogue entry c1

  @g57 @r57
  Scenario: A catalogue entry that names an undelivered item fails the check
    Given an item i1
    And the status of the item i1 is not `delivered`
    And a catalogue entry c1
    And the catalogue entry c1 mentions the item i1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the catalogue entry c1
    And the specification service names the item i1

  @g58 @r58
  Scenario: A catalogue entry that names neither an item nor a release fails the check
    Given a catalogue entry c1
    And the catalogue entry c1 mentions no item
    And the catalogue entry c1 mentions no release
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the catalogue entry c1

  @g59 @r59
  Scenario: `spec catalogue entry` writes a catalogue entry's purpose
    Given a catalogue entry c1
    And a purpose p1
    When the person describes the catalogue entry c1 with the purpose p1
    Then the specification service keeps the catalogue entry c2
    And the catalogue entry c2 has the purpose p1
    And the specification service completes this request

  @g60 @r60
  Scenario: `spec catalogue entry` writes the item a catalogue entry came by
    Given a catalogue entry c1
    And an item i1
    When the person describes the catalogue entry c1 with the item i1
    Then the specification service keeps the catalogue entry c2
    And the catalogue entry c2 mentions the item i1
    And the specification service completes this request

  @g61 @r61
  Scenario: `spec catalogue entry` refuses an entry of no rule and no construct
    Given a catalogue entry c1
    And this rule catalogue holds the catalogue entry c1
    And no rule has the catalogue entry c1
    When the person describes the catalogue entry c1
    Then the specification service refuses this request
    And the specification service names the catalogue entry c1

  @g62 @r62
  Scenario: `spec catalogue entry` refuses a construct catalogue entry of no construct
    Given a catalogue entry c1
    And this construct catalogue holds the catalogue entry c1
    And no construct has the catalogue entry c1
    When the person describes the catalogue entry c1
    Then the specification service refuses this request
    And the specification service names the catalogue entry c1

  @g63 @r63
  Scenario: the check passes an attribute with two senses told apart by kinds
    Given a term t1
    And the part of speech of the term t1 is `attribute`
    And a sense s1
    And the term t1 has the sense s1
    And a sense s2
    And the term t1 has the sense s2
    When the person validates this specification
    Then the specification service completes this request

  @g64 @r64
  Scenario: A contract is prepared in the contract form
    Given a contract c1
    When the person prepares the contract c1
    Then the specification service returns the contract c2
    And the contract c2 conforms to the contract form
    And the specification service changes nothing

  @g65 @r65
  Scenario: A contract holds the requirements that govern its operations
    Given a requirement r1
    And an operation o1
    And the requirement r1 governs the operation o1
    And a contract c1
    When the person prepares the contract c1
    Then the specification service returns the contract c2
    And the contract c2 holds the requirement r1

  @g66 @r66
  Scenario: A contract holds the properties of its operations
    Given a property p1
    And an operation o1
    And the operation o1 has the property p1
    And a contract c1
    When the person prepares the contract c1
    Then the specification service returns the contract c2
    And the contract c2 holds the property p1

  @g67 @r67
  Scenario: A property that refers to no operation is refused
    Given an operation o1
    And the operation o1 does not exist
    And a property p1
    And the property p1 refers to the operation o1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the property p1

  @g69 @r69
  Scenario: A port's operation needs no table in the CLI contract
    Given an area a1
    And the kind of the area a1 is `port`
    And an operation o1
    And the area a1 holds the operation o1
    And the operation o1 has no operation table
    When the person validates this specification
    Then the specification service completes this request

  @g70 @r70
  Scenario: A port line relied on by a line that does not exist is refused
    Given a requirement id r2
    And no requirement has the requirement id r2
    And a requirement r1
    And the requirement r1 supports the requirement id r2
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the requirement id r2

  @g71 @r71
  Scenario: An operation requested only by a response is requested
    Given a requirement r1
    And the requirement r1 uses `response-request`
    And an operation o1
    And the requirement r1 uses the operation o1
    And no requirement governs the operation o1
    When the person validates this specification
    Then the specification service completes this request

  @g72 @r72
  Scenario: A line triggered on the refusal of a response's request states its reasons
    Given a requirement r1
    And the requirement r1 uses `response-request`
    And an operation o1
    And the requirement r1 uses the operation o1
    And a trigger t1
    And a refusal r3
    And the trigger t1 uses the refusal r3
    And the trigger t1 uses the operation o1
    And a requirement r2
    And the requirement r2 has the trigger t1
    When the person validates this specification
    Then the specification service completes this request

  @g73 @r73
  Scenario: A contract published keeps the specification at a version
    Given a contract c1
    When the person publishes the contract c1 with `1.2.0`
    Then the specification service keeps the contract c2
    And the contract c2 has `1.2.0`

  @g74 @r74
  Scenario: A later contract supersedes every published one
    Given a contract c1
    And a contract c2
    And the status of the contract c2 is `published`
    And a contract c3
    And the status of the contract c3 is `published`
    And a contract c4
    And the status of the contract c4 is `superseded`
    When the person publishes the contract c1 with `1.3.0`
    Then the specification service sets the status of the contract c2 to `superseded`
    And the specification service sets the status of the contract c3 to `superseded`
    And the specification service does not set the status of the contract c4 to `superseded`

  @g75 @r75
  Scenario: A contract at a version already published is refused
    Given a contract c1
    And the contract c1 has `1.2.0`
    And a contract c2
    When the person publishes the contract c2 with `1.2.0`
    Then the specification service refuses this request
    And the specification service names `1.2.0`

  @g76 @r76
  Scenario: A contract is refused while a requirement is out of the language
    Given a requirement r1
    And the requirement r1 does not conform to the language reference
    And a contract c1
    When the person publishes the contract c1
    Then the specification service refuses this request
    And the specification service names the requirement r1

  @g77 @r77
  Scenario: A contract published holds the requirements and the terms
    Given a contract c1
    And a requirement r1
    And a requirement r2
    And a term t1
    And the contract c2 holds the term t1
    And a term t2
    And the contract c2 holds the term t2
    And a term t3
    And the contract c2 does not hold the term t3
    When the person publishes the contract c1
    Then the specification service keeps the contract c2
    And the status of the contract c2 is `published`
    And the specification service keeps the requirement r1
    And the specification service keeps the requirement r2
    And the specification service keeps the term t1
    And the specification service keeps the term t2
    And the specification service does not keep the term t3

  @g78 @r78
  Scenario: A downstream context fetches the published contract without a context request
    Given a downstream context d1
    And a contract c1
    When the downstream context d1 fetches the contract c1
    Then the status of the contract c1 is `published`
    And the specification service returns the contract c1
    And the specification service changes nothing

  @g79 @r79
  Scenario: A contract fetched at a version never published is refused
    Given no contract has `2.0.0`
    And a downstream context d1
    And a contract c1
    When the downstream context d1 fetches the contract c1 with `2.0.0`
    Then the specification service refuses this request
    And the specification service names `2.0.0`

  @g80 @r80
  Scenario: A downstream context fetches a contract at a version
    Given a downstream context d1
    And a contract c1
    When the downstream context d1 fetches the contract c1 with `1.2.0`
    Then the contract c1 has `1.2.0`
    And the specification service returns the contract c1

  @g81 @r81
  Scenario: A contract obtained from an upstream is kept
    Given a contract c1
    And a bounded context b1
    When the person obtains the contract c1 from the bounded context b1
    Then the specification service keeps the contract c1
    And the specification service does not keep a context request

  @g82 @r82
  Scenario: A contract is not obtained from a bounded context that has no contract
    Given a bounded context b1
    And the bounded context b1 has no contract
    And a contract c1
    When the person obtains the contract c1 from the bounded context b1
    Then the specification service refuses this request
    And the specification service names the bounded context b1

  @g83 @r83
  Scenario: A contract at a version that is not a version is refused
    Given a version v1
    And the version v1 does not conform to the version form
    And a contract c1
    When the person publishes the contract c1 with the version v1
    Then the specification service refuses this request
    And the specification service names the version v1
    And the specification service names `version not in the version form`

  @g84 @r84
  Scenario: An adapter spec whose id is out of the adapter spec id form is refused
    Given an id i1
    And an adapter spec a1
    And the adapter spec a1 has the id i1
    And the id i1 does not conform to the adapter spec id form
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the id i1

  @g85 @r85
  Scenario: An adapter spec that realises a line that does not exist is refused
    Given a requirement id r1
    And no requirement has the requirement id r1
    And an adapter spec a1
    And the adapter spec a1 realises the requirement id r1
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the requirement id r1

  @g86 @r86
  Scenario: An adapter spec that holds no contract of its provider is refused
    Given a provider p1
    And an adapter spec a1
    And the adapter spec a1 has the provider p1
    And the adapter spec a1 holds no contract
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the provider p1

  @g87 @r87
  Scenario: An adapter spec with its adapter decisions and its providers' contracts is valid
    Given an adapter decision a2
    And an adapter spec a1
    And the adapter spec a1 holds the adapter decision a2
    And a provider p1
    And the adapter spec a1 has the provider p1
    And a contract c1
    And the provider p1 has the contract c1
    And the adapter spec a1 holds the contract c1
    When the person validates the adapter spec a1
    Then the specification service completes this request

  @g88 @r88
  Scenario: A contract is not obtained by an id out of the context id form
    Given an id i1
    And a bounded context b1
    And the bounded context b1 has the id i1
    And the id i1 does not conform to the context id form
    And a contract c1
    When the person obtains the contract c1 from the bounded context b1
    Then the specification service refuses this request
    And the specification service names the id i1
    And the specification service names `id not in the context id form`

  @g89 @r89
  Scenario: A bounded context that cannot be reached is not reported as having no contract
    Given a bounded context b1
    And the availability of the bounded context b1 is `unreachable`
    And a contract c1
    When the person obtains the contract c1 from the bounded context b1
    Then the specification service refuses this request
    And the specification service names the bounded context b1
    And the specification service names `bounded context unreachable`

  @g90 @r90
  Scenario: A contract obtained keeps every other bounded context's contract as it was
    Given a contract c1
    And a bounded context b1
    And the bounded context b1 has the contract c1
    And a contract c2
    And a bounded context b2
    And a contract c3
    And a bounded context b3
    And the bounded context b3 has the contract c3
    When the person obtains the contract c2 from the bounded context b2
    Then the specification service keeps the contract c2
    And the specification service does not change the contract c3

  @g91 @r91
  Scenario: An obtained contract is held by the adapter spec of its provider
    Given a provider p1
    And an adapter spec a1
    And the adapter spec a1 has the provider p1
    And a contract c1
    When the person obtains the contract c1 from the provider p1
    Then the adapter spec a1 holds the contract c1
    And the specification service keeps the contract c1

  @g92 @r92
  Scenario: An adapter spec whose id does not match its own name is refused
    Given an id i1
    And an adapter spec a1
    And the adapter spec a1 has the id i1
    And the id i1 does not match the adapter spec a1
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the id i1

  @g93 @r93
  Scenario: A provider's version that is not a version is refused
    Given a provider p1
    And an adapter spec a1
    And the adapter spec a1 has the provider p1
    And a version v1
    And the version v1 does not conform to the version form
    And the provider p1 has the version v1
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the version v1

  @g95 @r95
  Scenario: A port operation that no core line requests is refused
    Given an operation o1
    And a driven port d1
    And the driven port d1 holds the operation o1
    And no core line uses `response-request`
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the operation o1

  @g96 @r96
  Scenario: A port outcome that no core line handles and no port line excludes is refused
    Given an operation outcome o2
    And an operation o1
    And the operation o1 has the operation outcome o2
    And a driven port d1
    And the driven port d1 holds the operation o1
    And no core line handles the operation outcome o2
    And no port line excludes the operation outcome o2
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the operation outcome o2

  @g97 @r97
  Scenario: A port line relied on by a core line that does not request its operation is refused
    Given a port line p1
    And an operation o1
    And the port line p1 governs the operation o1
    And a requirement id r1
    And the port line p1 supports the requirement id r1
    And no core line has the requirement id r1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the requirement id r1

  @g98 @r98
  Scenario: A port line that no core line relies on is refused
    Given a port line p1
    And an operation o1
    And the port line p1 governs the operation o1
    And no core line relies on the port line p1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the port line p1

  @g99 @r99
  Scenario: A port line that excludes an unhandled outcome needs no citation of its core lines
    Given a core line c1
    And the core line c1 uses `response-request`
    And an operation o1
    And the core line c1 uses the operation o1
    And a port line p1
    And the port line p1 governs the operation o1
    And the port line p1 supports no requirement id
    And an operation outcome o2
    And no core line handles the operation outcome o2
    And the port line p1 excludes the operation outcome o2
    When the person validates this specification
    Then the specification service completes this request

  @g100 @r100
  Scenario: An obtained contract is kept at the version its adapter spec pins, not a later one
    Given a provider p1
    And an adapter spec a1
    And the adapter spec a1 has the provider p1
    And the provider p1 has `1.2.0`
    And a contract c1
    And the contract c1 has `1.3.0`
    And the provider p1 has the contract c1
    And a contract c2
    When the person obtains the contract c2 from the provider p1
    Then the specification service keeps the contract c3
    And the contract c3 has `1.2.0`
    And the adapter spec a1 holds the contract c3
    And the specification service keeps the adapter spec a1

  @g101 @r101
  Scenario: A lifecycle transition that no operation of its own area performs fails the check
    Given a lifecycle l1
    And an area a1
    And the area a1 holds the lifecycle l1
    And a transition t1
    And the lifecycle l1 has the transition t1
    And an operation o1
    And the operation o1 performs the transition t1
    And an area a2
    And the area a2 holds the operation o1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the transition t1

  @g102 @r102
  Scenario: A bounded context that fails to answer is not reported as unreachable
    Given a bounded context b1
    And the health of the bounded context b1 is `failing`
    And a contract c1
    When the person obtains the contract c1 from the bounded context b1
    Then the specification service refuses this request
    And the specification service names the bounded context b1
    And the specification service names `bounded context failing`

  @g103 @r103
  Scenario: A contract of an available provider in the context id form is obtained only for an adapter spec of the provider
    Given an id i1
    And a provider p1
    And the provider p1 has the id i1
    And the id i1 conforms to the context id form
    And the availability of the provider p1 is `available`
    And no adapter spec has the provider p1
    And a contract c1
    When the person obtains the contract c1 from the provider p1
    Then the specification service refuses this request
    And the specification service names the provider p1
    And the specification service names `no adapter spec has the provider`

  @g104 @r104
  Scenario: A domain model whose element refers to a term of an imported pack passes the check
    Given a pack p1
    And this bounded context imports the pack p1
    And a term t1
    And the pack p1 has the term t1
    And an element e1
    And the element e1 refers to the term t1
    When the person validates this specification
    Then the specification service completes this request

  @g105 @r105
  Scenario: The base pack shows its terms
    Given this bounded context imports `base`
    And a term t1
    And `base` has the term t1
    And a term t2
    And `base` has the term t2
    And a term t3
    And `base` does not have the term t3
    When the person looks up `base`
    Then the language service returns the term t1
    And the language service returns the term t2
    And the language service does not return the term t3
    And the language service completes this request

  @g106 @r106
  Scenario: A line of an adapter spec reads a term of its provider's contract
    Given a contract c1
    And an adapter spec a1
    And the adapter spec a1 holds the contract c1
    And a requirement r1
    And the adapter spec a1 has the requirement r1
    And a term t1
    And the contract c1 holds the term t1
    And the requirement r1 uses the term t1
    When the person validates the adapter spec a1
    Then the specification service completes this request

  @g107 @r107
  Scenario: A provider's term that clashes with another term is read under its new word
    Given a term t1
    And a contract c1
    And the contract c1 holds the term t1
    And an adapter spec a1
    And the adapter spec a1 holds the contract c1
    And a term t2
    And the term t1 clashes with the term t2
    And the adapter spec a1 renames the term t2
    When the person validates the adapter spec a1
    Then the specification service completes this request

  @g108 @r108
  Scenario: A provider's term that clashes with another term and is not renamed is refused
    Given a term t1
    And a contract c1
    And the contract c1 holds the term t1
    And an adapter spec a1
    And the adapter spec a1 holds the contract c1
    And a term t2
    And the term t1 clashes with the term t2
    And the adapter spec a1 does not rename the term t2
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the term t2

  @g109 @r109
  Scenario: An assumed description whose line has no scenario is refused
    Given a requirement id r1
    And no scenario refers to the requirement id r1
    And an assumed description a2
    And the assumed description a2 holds the requirement id r1
    And an adapter spec a1
    And the adapter spec a1 holds the assumed description a2
    When the person validates the adapter spec a1
    Then the specification service fails this check
    And the specification service names the requirement id r1

  @g110 @r110
  Scenario: A capability whose requirement group serves a job is not unserved
    Given a job j1
    And this bounded context has the job j1
    And a requirement group r1
    And a capability c1
    And the capability c1 has the requirement group r1
    And the requirement group r1 serves the job j1
    And a capability c2
    And the capability c2 violates `w_unserved_cap`
    When the person validates this specification
    Then the specification service does not return the capability c2

  @g111 @r111
  Scenario: An operation requested only by a response's request with no parameter is requested
    Given a response r2
    And an operation o1
    And the response r2 uses the operation o1
    And the response r2 uses no parameter
    And a requirement r1
    And the requirement r1 has the response r2
    And no requirement governs the operation o1
    When the person validates this specification
    Then the specification service completes this request

  @g112 @r112
  Scenario: A transition that only a forbidden set reaches is named as a transition no line causes
    Given a transition t1
    And a lifecycle l1
    And the lifecycle l1 has the transition t1
    And a requirement r1
    And an act a1
    And the requirement r1 forbids the act a1
    And the requirement r1 uses `set-attribute`
    And the requirement r1 uses the transition t1
    And no operation performs the transition t1
    When the person validates this specification
    Then the specification service names the transition t1
    And the specification service completes this request

  @g113 @r113
  Scenario: A domain model object spelled by an imported pack's term reads as the term's kind
    Given a pack p1
    And this bounded context imports the pack p1
    And a term t1
    And the pack p1 has the term t1
    And an element e1
    And the term t1 spells the element e1
    And no term means the element e1
    And an element e2
    And the element e2 refers to the term t1
    When the person validates this specification
    Then the specification service completes this request

  @g114 @r114
  Scenario: A job of the product that no bounded context holds is named
    Given a job j1
    And this product holds the job j1
    And no bounded context holds the job j1
    When the person validates this specification
    Then the specification service names the job j1
    And the specification service completes this request

  @g115 @r115
  Scenario: A job assigned here that no requirement group serves is named
    Given a job j1
    And this bounded context holds the job j1
    And no requirement group serves the job j1
    When the person validates this specification
    Then the specification service names the job j1
    And the specification service completes this request

  @g116 @r116
  Scenario: A product actor of a job whose actor here triggers no line of the job's trace is named
    Given a job j1
    And this bounded context holds the job j1
    And a product actor p1
    And the job j1 has the product actor p1
    And an agent a1
    And the agent a1 plays the product actor p1
    And the job j1 reaches no requirement
    When the person validates this specification
    Then the specification service names the product actor p1
    And the specification service completes this request

  @g117 @r117
  Scenario: A job whose needs close a cycle fails the check
    Given a job j1
    And this product holds the job j1
    And a need n1
    And the need n1 depends on the job j1
    And the job j1 needs the need n1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the need n1

  @g118 @r118
  Scenario: A subdomain that no bounded context addresses is named
    Given a subdomain s1
    And this product holds the subdomain s1
    And no bounded context addresses the subdomain s1
    When the person validates this specification
    Then the specification service names the subdomain s1
    And the specification service completes this request

  @g119 @r119
  Scenario: A subdomain of a job that the job's trace reaches no bounded context of is named
    Given a job j1
    And this bounded context holds the job j1
    And a subdomain s1
    And the subdomain s1 serves the job j1
    And no bounded context addresses the subdomain s1
    When the person validates this specification
    Then the specification service names the subdomain s1
    And the specification service completes this request

  @g120 @r120
  Scenario: A capability a job's trace reaches contributes to the job
    Given a job j1
    And this bounded context has the job j1
    And a capability c1
    And the job j1 reaches the capability c1
    And a capability c2
    And the capability c2 violates `w_unserved_cap`
    When the person validates this specification
    Then the specification service does not return the capability c2

  @g121 @r121
  Scenario: A capability that has a port line contributes to the jobs it serves through the port
    Given a job j1
    And this bounded context has the job j1
    And a port line p1
    And a capability c1
    And the capability c1 has the port line p1
    And a capability c2
    And the capability c2 violates `w_unserved_cap`
    When the person validates this specification
    Then the specification service does not return the capability c2

  @g122 @r122
  Scenario: A guarantees capability contributes to the jobs whose lines it constrains
    Given a job j1
    And this bounded context has the job j1
    And a requirement group r1
    And the requirement group r1 serves the job j1
    And a capability c1
    And the group of the capability c1 is `guarantees`
    And a capability c2
    And the capability c2 violates `w_unserved_cap`
    When the person validates this specification
    Then the specification service does not return the capability c2

  @g123 @r123
  Scenario: A job served here that the product assigns to another bounded context fails the check
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And this bounded context has the job j1
    And a bounded context b1
    And the bounded context b1 holds the job j1
    When the person validates this specification
    Then the specification service fails this check
    And the specification service names the job j1

  @g124 @r124
  Scenario: A product not of the product form is named by the check, which completes
    Given this product does not conform to the product form
    When the person validates this specification
    Then the specification service names this product
    And the specification service completes this request

  @g125 @r125
  Scenario: A port outcome a reply trigger is on is handled
    Given an operation outcome o2
    And an operation o1
    And the operation o1 has the operation outcome o2
    And a driven port d1
    And the driven port d1 holds the operation o1
    And a core line c1
    And the core line c1 uses `reply-trigger`
    And the core line c1 handles the operation outcome o2
    When the person validates this specification
    Then the specification service completes this request
