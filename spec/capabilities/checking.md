---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/checking
title: Checking
narrator: the person
group: service
area: specification
specifies: service specification: check, consult, renew, inventory, translate
language: codified-2
retired: [g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g25, r25, g31, r31, g34, r34, g37, r37, g40, r40, g42, r42, g43, r43, g45, r45, g56, r56, g94, r94, g91, r91, g100, r100]
unbuilt: []
---

# Checking

## Purpose
This specification checked as a whole: its rules, the catalogue of the rules, the file forms it keeps and the facts the
checks read.

## Behaviour

### [g1] `model rules` prints every rule
Restates: design-model-check#r65@0.29.
- [r1] When the person consults the rule catalogue, the specification service shall return every rule and complete the
  request.

### [g2] `model forms` lists every file form
- [r2] When the person inventories this specification, the specification service shall return every file form and
  complete the request.

### [g3] the check exits successfully when nothing violates a rule
Restates: design-model-check#r1@0.29.
- [r3] While nothing violates a rule, when the person validates this specification, the specification service shall
  return `0 violations` and complete the request.

### [g18] A request not of the form `work request` writes
Restates: design-model-check#r112@0.29.
- [r18] While a request does not conform to the request form, if the person validates this specification, then the
  specification service shall fail the check and name the request.

### [g19] A scenario that names a requirement its capability does not have
Restates: design-model-check#r9@0.29.
- [r19] While a scenario refers to a requirement id that the capability of the scenario does not hold, if the person
  validates this specification, then the specification service shall fail the check and name the scenario.

### [g20] A capability with no capability id
Restates: design-model-check#r25@0.29.
- [r20] While a capability does not conform to the capability id form, if the person validates this specification, then
  the specification service shall fail the check and name the capability.

### [g21] A capability with no Behaviour section
Restates: design-model-check#r25@0.29.
- [r21] While a capability has no section whose heading is `Behaviour`, if the person validates this specification, then
  the specification service shall fail the check and name the capability.

### [g22] A feature file of no capability
Restates: design-model-check#r26@0.29.
- [r22] While a feature does not conform to the feature form, if the person validates this specification, then the
  specification service shall fail the check and name the feature.

### [g23] A glossary bullet in no form of a term entry
Restates: design-model-check#r48@0.29, design-model-check#r49@0.29.
- [r23] While a term does not conform to the entry form, if the person validates this specification, then the
  specification service shall fail the check and name the term.

### [g24] A repository not on the final layout
Restates: design-model-check#r61@0.29.
- [r24] While this bounded context does not conform to the final layout, if the person validates this specification,
  then the specification service shall fail the check and name `scripts/migrate`.

### [g26] A context with no job has no unserved capability
Restates: design-model-check#r111@0.29.
- [r26] While this bounded context has no job, when the person validates this specification, the specification service
  shall return no capability that violates `w_unserved_cap`.

### [g27] the check tries again under an interpreter that has clingo
Restates: design-model-check#r55@0.29.
- [r27] While this interpreter does not import `clingo` and another interpreter imports `clingo`, when the person
  validates this specification, the specification service shall return `0 violations`.

### [g28] No interpreter has clingo
Restates: design-model-check#r12@0.29.
- [r28] While no interpreter imports `clingo`, if the person validates this specification, then the specification
  service shall fail the check and name this interpreter.

### [g29] `model facts` prints the facts
Restates: design-model-check#r13@0.29.
- [r29] When the person translates this specification, the specification service shall return every fact of this bounded
  context.

### [g30] the check refuses a verb with no frame
- [r30] While a verb has no frame, if the person validates this specification, then the specification service shall fail
  the check and name the verb.

### [g32] the check refuses a term with no part of speech
- [r32] While a term has no part of speech, if the person validates this specification, then the specification service
  shall fail the check and name the term.

### [g33] the check reads a frame with a preposition
- [r33] While a frame of a term has a preposition, when the person validates this specification, the specification
  service shall complete the request.

### [g35] `model rules --write` writes the rule catalogue
- [r35] When the person renews the rule catalogue, the specification service shall keep a rule catalogue and complete
  the request.

### [g36] `model rules --check` refuses a catalogue that lacks a catalogue entry
- [r36] While a rule has a catalogue entry that a rule catalogue does not hold, if the person renews the rule catalogue
  with the audit, then the specification service shall fail the check, name the rule catalogue and change no file.

### [g38] the check passes a verb with two frames
- [r38] While a term has more than one frame, when the person validates this specification, the specification service
  shall complete the request.

### [g39] the check passes a verb with two senses told apart by kinds
- [r39] While a term has more than one sense, when the person validates this specification, the specification service
  shall complete the request.

### [g41] `model lexicon` shows the terms of the imported packs
- [r41] While this bounded context imports a pack, when the person looks up the pack, the language service shall return
  every term of the pack and complete the request.

### [g44] the check passes a term marked Redefines:
- [r44] While a term redefines a pack, when the person validates this specification, the specification service shall
  complete the request.

### [g46] the check refuses a capability in the old language, naming `migrate upgrade`
- [r46] If the person validates this specification with a capability whose language is `codified-1`, then the
  specification service shall refuse the request and name the capability.

### [g47] `model forms --check` refuses a file form written by hand
- [r47] While the writer of a file form is `hand`, when the person inventories this specification with the audit, the
  specification service shall fail the check and name the file form.

### [g48] Each operation of an adapter contract is given the requirements that govern it
- [r48] While a requirement governs an operation that an adapter contract holds, when the person annotates the adapter contract, the specification service shall keep an adapter contract that holds an operation that holds the requirement and complete the request.

### [g49] An operation missing a requirement that governs it fails the check
- [r49] While a requirement governs an operation that an adapter contract holds and the operation does not hold the requirement, if the person validates this specification, then the specification service shall fail the check and name the operation and the requirement.

### [g50] An operation holding a requirement that no longer governs it fails the check
- [r50] While an adapter contract holds an operation and the operation holds a requirement and the requirement does not govern the operation, if the person validates this specification, then the specification service shall fail the check and name the operation and the requirement.

### [g51] A stale adapter contract fails the audit
- [r51] While a requirement governs an operation that an adapter contract holds and the operation does not hold the requirement, if the person annotates the adapter contract with the audit, then the specification service shall fail the check, name the adapter contract and change no file.

### [g52] A violation of a rule fails the check under the rule's code
- [r52] While a capability violates a rule whose severity is `error`, if the person validates this specification, then the specification service shall fail the check and name the rule.

### [g53] A warning is named and the check passes
- [r53] While a capability violates a rule whose severity is `warning` and nothing violates a rule whose severity is `error`, when the person validates this specification, the specification service shall name the rule and complete the request.

### [g54] A requirement that uses a rule the rule catalogue does not define fails the check
- [r54] While a requirement uses a rule that has no catalogue entry, if the person validates this specification, then the specification service shall fail the check and name the rule.

### [g55] A catalogue entry with no purpose fails the check
- [r55] While a catalogue entry has no purpose, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry.

### [g57] A catalogue entry that names an undelivered item fails the check
- [r57] While a catalogue entry mentions an item whose status is not `delivered`, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry and the item.

### [g58] A catalogue entry that names neither an item nor a release fails the check
- [r58] While a catalogue entry mentions no item and the catalogue entry mentions no release, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry.

### [g59] `spec catalogue entry` writes a catalogue entry's purpose
- [r59] When the person describes a catalogue entry with a purpose, the specification service shall keep a catalogue entry that has the purpose and complete the request.

### [g60] `spec catalogue entry` writes the item a catalogue entry came by
- [r60] When the person describes a catalogue entry with an item, the specification service shall keep a catalogue entry that mentions the item and complete the request.

### [g61] `spec catalogue entry` refuses an entry of no rule and no construct
- [r61] If the person describes a catalogue entry in the rule catalogue that no rule has, then the specification service shall refuse the request and name the catalogue entry.

### [g62] `spec catalogue entry` refuses a construct catalogue entry of no construct
- [r62] If the person describes a catalogue entry in the construct catalogue that no construct has, then the specification service shall refuse the request and name the catalogue entry.

### [g63] the check passes an attribute with two senses told apart by kinds
- [r63] While a term whose part of speech is `attribute` has more than one sense, when the person validates this specification, the specification service shall complete the request.

### [g64] A contract is prepared in the contract form
- [r64] When the person prepares a contract, the specification service shall return a contract that conforms to the contract form and change nothing.

### [g65] A contract holds the requirements that govern its operations
- [r65] While a requirement governs an operation, when the person prepares a contract, the specification service shall return a contract that holds the requirement.

### [g66] A contract holds the properties of its operations
- [r66] While an operation has a property, when the person prepares a contract, the specification service shall return a contract that holds the property.

### [g67] A property that refers to no operation is refused
- [r67] While a property refers to an operation that does not exist, if the person validates this specification, then the specification service shall fail the check and name the property.

### [g69] A port's operation needs no table in the CLI contract
- [r69] While an area whose kind is `port` holds an operation and no adapter contract holds an operation table of the operation, when the person validates this specification, the specification service shall complete the request.

### [g70] A port line relied on by a line that does not exist is refused
- [r70] While a requirement supports a requirement id that no requirement has, if the person validates this specification, then the specification service shall fail the check and name the requirement id.

### [g71] An operation requested only by a response is requested
- [r71] While a requirement uses `response-request` and the requirement uses an operation and no requirement governs the operation, when the person validates this specification, the specification service shall complete the request.

### [g72] A line triggered on the refusal of a response's request states its reasons
- [r72] While a requirement uses `response-request` and the requirement uses an operation and another requirement has a trigger that uses a refusal and the operation, when the person validates this specification, the specification service shall complete the request.

### [g73] A contract published keeps the specification at a version
- [r73] When the person publishes a contract with the `1.2.0` version, the specification service shall keep a contract that has the `1.2.0` version.

### [g74] A later contract supersedes every published one
- [r74] When the person publishes a contract with the `1.3.0` version, the specification service shall set the status of every contract whose status is `published` to `superseded`.

### [g75] A contract at a version already published is refused
- [r75] While a contract has the `1.2.0` version, if the person publishes a contract with the `1.2.0` version, then the specification service shall refuse the request and name the version.

### [g76] A contract is refused while a requirement is out of the language
- [r76] While a requirement does not conform to the language reference, if the person publishes a contract, then the specification service shall refuse the request and name the requirement.

### [g77] A contract published holds the requirements and the terms
- [r77] When the person publishes a contract, the specification service shall keep a contract whose status is `published` and keep every requirement and every term in the contract.

### [g78] A downstream context fetches the published contract without a context request
- [r78] When a downstream context fetches a contract, the specification service shall return the contract whose status is `published` and change nothing.

### [g79] A contract fetched at a version never published is refused
- [r79] While no contract has the `2.0.0` version, if a downstream context fetches a contract with the `2.0.0` version, then the specification service shall refuse the request and name the version.

### [g80] A downstream context fetches a contract at a version
- [r80] When a downstream context fetches a contract with the `1.2.0` version, the specification service shall return the contract that has the `1.2.0` version.

### [g81] A contract obtained from an upstream is kept
- [r81] When the person obtains a contract from a bounded context, the specification service shall keep the contract and keep no context request.

### [g82] A contract is not obtained from a bounded context that has no contract
- [r82] If the person obtains a contract from a bounded context that has no contract, then the specification service shall refuse the request and name the bounded context.

### [g83] A contract at a version that is not a version is refused
- [r83] If the person publishes a contract with a version that does not conform to the version form, then the specification service shall refuse the request and name the version and the `version not in the version form` reason.

### [g87] An adapter spec with its adapter decisions and its providers' contracts is valid
- [r87] While an adapter spec holds an adapter decision and the adapter spec holds a contract of a provider of the adapter spec, when the person validates the adapter spec, the specification service shall complete the request.

### [g84] An adapter spec whose id is out of the adapter spec id form is refused
- [r84] While the id of an adapter spec does not conform to the adapter spec id form, if the person validates the adapter spec, then the specification service shall fail the check and name the id.

### [g85] An adapter spec that realises a line that does not exist is refused
- [r85] While an adapter spec realises a requirement id that no requirement has, if the person validates the adapter spec, then the specification service shall fail the check and name the requirement id.

### [g86] An adapter spec that holds no contract of its provider is refused
- [r86] While a provider of an adapter spec has no contract that the adapter spec holds, if the person validates the adapter spec, then the specification service shall fail the check and name the provider.

### [g88] A contract is not obtained by an id out of the context id form
- [r88] If the person obtains a contract from a bounded context whose id does not conform to the context id form, then the specification service shall refuse the request and name the id and the `id not in the context id form` reason.

### [g89] A bounded context that cannot be reached is not reported as having no contract
- [r89] If the person obtains a contract from a bounded context whose availability is `unreachable`, then the specification service shall refuse the request and name the bounded context and the `bounded context unreachable` reason.

### [g90] A contract obtained keeps every other bounded context's contract as it was
- [r90] While a bounded context has a contract, when the person obtains a contract from another bounded context, the specification service shall keep the contract and change no contract of a bounded context.

### [g92] An adapter spec whose id does not match its own name is refused
- [r92] While the id of an adapter spec does not match the adapter spec, if the person validates the adapter spec, then the specification service shall fail the check and name the id.

### [g93] A provider's version that is not a version is refused
- [r93] While a provider of an adapter spec has a version that does not conform to the version form, if the person validates the adapter spec, then the specification service shall fail the check and name the version.

### [g95] A port operation that no core line requests is refused
- [r95] While a driven port holds an operation and no core line that uses `response-request` uses the operation, if the person validates this specification, then the specification service shall fail the check and name the operation.

### [g96] A port outcome that no core line handles and no port line excludes is refused
- [r96] While a driven port holds an operation that has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, if the person validates this specification, then the specification service shall fail the check and name the operation outcome.

### [g97] A port line relied on by a core line that does not request its operation is refused
- [r97] While a port line that governs an operation supports a requirement id and no core line that has the requirement id uses the operation, if the person validates this specification, then the specification service shall fail the check and name the requirement id.

### [g98] A port line that no core line relies on is refused
- [r98] While a port line governs an operation and no core line relies on the port line, if the person validates this specification, then the specification service shall fail the check and name the port line.

### [g99] A port line that excludes an unhandled outcome needs no citation of its core lines
- [r99] While a core line that uses `response-request` uses an operation and a port line that governs the operation supports no requirement id and the port line excludes an operation outcome that no core line handles, when the person validates this specification, the specification service shall complete the request.

### [g101] A lifecycle transition that no operation of its own area performs fails the check
- [r101] While an area holds a lifecycle and the lifecycle has a transition and another area holds an operation that performs the transition, if the person validates this specification, then the specification service shall fail the check and name the transition.

### [g102] A bounded context that fails to answer is not reported as unreachable
- [r102] If the person obtains a contract from a bounded context whose health is `failing`, then the specification service shall refuse the request and name the bounded context and the `bounded context failing` reason.

### [g103] A contract of an available provider in the context id form is obtained only for an adapter spec of the provider
- [r103] While the id of a provider conforms to the context id form and the provider is `available`, if the person obtains a contract from the provider that no adapter spec has, then the specification service shall refuse the request and name the provider and the `no adapter spec has the provider` reason.

### [g104] A domain model whose element refers to a term of an imported pack passes the check
- [r104] While this bounded context imports a pack and the pack has a term and an element refers to the term, when the person validates this specification, the specification service shall complete the request.

### [g105] The base pack shows its terms
- [r105] While this bounded context imports the `base` pack, when the person looks up the pack, the language service shall return every term of the pack and complete the request.

### [g106] A line of an adapter spec reads a term of its provider's contract
- [r106] While an adapter spec holds a contract and a requirement of the adapter spec uses a term that the contract holds, when the person validates the adapter spec, the specification service shall complete the request.

### [g107] A provider's term that clashes with another term is read under its new word
- [r107] While an adapter spec holds a contract that holds a term and the term clashes with another term and the adapter spec renames the term, when the person validates the adapter spec, the specification service shall complete the request.

### [g108] A provider's term that clashes with another term and is not renamed is refused
- [r108] While an adapter spec holds a contract that holds a term and the term clashes with another term and the adapter spec does not rename the term, if the person validates the adapter spec, then the specification service shall fail the check and name the term.

### [g109] An assumed description whose line has no scenario is refused
- [r109] While an adapter spec holds an assumed description that holds a requirement id that no scenario refers to, if the person validates the adapter spec, then the specification service shall fail the check and name the requirement id.

### [g110] A capability whose requirement group serves a job is not unserved
- [r110] While this bounded context has a job and a requirement group of a capability serves the job, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.

### [g111] An operation requested only by a response's request with no parameter is requested
- [r111] While a requirement has a response that uses an operation and no parameter and no requirement governs the operation, when the person validates this specification, the specification service shall complete the request.

### [g112] A transition that only a forbidden set reaches is named as a transition no line causes
- [r112] While a lifecycle has a transition and a requirement that forbids an act uses `set-attribute` and the transition and no operation performs the transition, when the person validates this specification, the specification service shall name the transition and complete the request.

### [g113] A domain model object spelled by an imported pack's term reads as the term's kind
- [r113] While this bounded context imports a pack and the pack has a term and the term spells an element and no term means the element and another element refers to the term, when the person validates this specification, the specification service shall complete the request.

### [g123] A job served here that the product assigns to another bounded context fails the check
- [r123] While a requirement group serves a job and this bounded context has the job and another bounded context holds the job, if the person validates this specification, then the specification service shall fail the check and name the job.

### [g114] A job of the product that no bounded context holds is named
- [r114] While this product holds a job and no bounded context holds the job, when the person validates this specification, the specification service shall name the job and complete the request.

### [g115] A job assigned here that no requirement group serves is named
- [r115] While this bounded context holds a job and no requirement group serves the job, when the person validates this specification, the specification service shall name the job and complete the request.

### [g116] A product actor of a job whose actor here triggers no line of the job's trace is named
- [r116] While this bounded context holds a job and an agent plays a product actor of the job and the agent triggers no requirement that the job reaches, when the person validates this specification, the specification service shall name the product actor and complete the request.

### [g117] A job whose needs close a cycle fails the check
- [r117] While this product holds a job and the job needs a need that depends on the job, if the person validates this specification, then the specification service shall fail the check and name the need.

### [g118] A subdomain that no bounded context addresses is named
- [r118] While this product holds a subdomain and no bounded context addresses the subdomain, when the person validates this specification, the specification service shall name the subdomain and complete the request.

### [g119] A subdomain of a job that the job's trace reaches no bounded context of is named
- [r119] While this bounded context holds a job and a subdomain serves the job and the job reaches no bounded context that addresses the subdomain, when the person validates this specification, the specification service shall name the subdomain and complete the request.

### [g120] A capability a job's trace reaches contributes to the job
- [r120] While this bounded context has a job and the job reaches a capability, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.

### [g121] A capability that has a port line contributes to the jobs it serves through the port
- [r121] While this bounded context has a job and a capability has a port line, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.

### [g122] A guarantees capability contributes to the jobs whose lines it constrains
- [r122] While this bounded context has a job and a requirement group serves the job and the group of a capability is `guarantees`, when the person validates this specification, the specification service shall return no capability that violates `w_unserved_cap`.

### [g124] A product not of the product form is named by the check, which completes
- [r124] While this product does not conform to the product form, when the person validates this specification, the specification service shall name this product and complete the request.

### [g125] A port outcome a reply trigger is on is handled
- [r125] While a driven port holds an operation that has an operation outcome and a core line that uses `reply-trigger` handles the operation outcome, when the person validates this specification, the specification service shall complete the request.

### [g127] A contract published is deposited in the contract registry at its version
- [r127] When the person publishes a contract with a version, the specification service shall deposit the contract with the version.

### [g131] A contract fetched is retrieved from the contract registry at its version
- [r131] When a downstream context fetches a contract with a version, the specification service shall retrieve the contract with the version.

### [g126] A contract obtained is retrieved from the contract registry for its bounded context and version
- [r126] When the person obtains a contract from a bounded context with a version, the specification service shall retrieve the contract with the bounded context and the version.

### [g128] A deposit the contract registry completes publishes the contract
- [r128] When the contract registry service completes the request to deposit a contract, the specification service shall keep the contract.

### [g129] A contract the contract registry returns is returned to whoever asked for it
- [r129] When the contract registry service returns the request to retrieve a contract, the specification service shall return the contract.

### [g130] A retrieval the contract registry refuses names the version and changes nothing
- [r130] When the contract registry service refuses the request to retrieve a contract, the specification service shall name the version of the contract and change nothing.

### [g132] Obtaining from a bounded context outside the shop that no upstream entry identifies is refused naming it
- [r132] While a bounded context is not in the shop, if the person obtains a contract from the bounded context that no upstream entry identifies, then the specification service shall refuse the request and name the bounded context and the `bounded context not an upstream` reason.

### [g133] Obtaining from a failing provider that no adapter spec has is refused naming the provider
- [r133] While the health of a provider is `failing`, if the person obtains a contract from the provider that no adapter spec has, then the specification service shall refuse the request and name the provider and the `bounded context failing` reason.

### [g134] A deposit the contract registry refuses names the version and changes nothing
- [r134] When the contract registry service refuses the request to deposit a contract, the specification service shall name the version of the contract and change nothing.

### [g135] A provider operation an adapter spec uses that no held contract declares
- [r135] While an adapter spec realises the requirement id of a port line that governs an operation and the operation uses another operation and the adapter spec holds no contract that holds the operation, if the person validates the adapter spec, then the specification service shall fail the check and name the operation.

### [g136] A port operation of an adapter spec that uses no provider operation
- [r136] While an adapter spec realises the requirement id of a port line that governs an operation and the operation uses no operation, if the person validates the adapter spec, then the specification service shall fail the check and name the operation.

### [g137] An obtained contract is registered with the contract registry for each adapter spec of its provider
- [r137] While an adapter spec has a provider, when the person obtains a contract from the provider, the specification service shall register the contract for the adapter spec with the provider.

### [g138] An obtained contract is registered at the version its adapter spec pins, not a later one
- [r138] While an adapter spec has a provider and the provider has the `1.2.0` version and the provider has a contract that has the `1.3.0` version, when the person obtains a contract from the provider, the specification service shall register the contract for the adapter spec with the provider and the `1.2.0` version.

### [g139] A registration the contract registry completes keeps the obtained contract
- [r139] When the contract registry service completes the request to register a contract for an adapter spec, the specification service shall keep the contract.

### [g140] A registration the contract registry refuses names the adapter spec and changes nothing
- [r140] When the contract registry service refuses the request to register a contract for an adapter spec, the specification service shall name the adapter spec and change nothing.

### [g141] Obtaining from a bounded context whose upstream entry holds no shared store is refused as unreachable
- [r141] While an upstream entry identifies a bounded context and the upstream entry holds no shared store, if the person obtains a contract from the bounded context, then the specification service shall refuse the request and name the bounded context and the `bounded context unreachable` reason.

### [g142] A registration the contract registry refuses deregisters the contract registered for another adapter spec of the provider
- [r142] While an adapter spec has a provider, when the contract registry service refuses the request to register a contract for the adapter spec, the specification service shall deregister the contract for a different adapter spec that has the provider.

### [g143] A completed deregistration changes nothing more
- [r143] When the contract registry service completes the request to deregister a contract for an adapter spec, the specification service shall change nothing.

## Dropped
- design-model-check#r2@0.29: retired with checking#r4 by b370.
- design-model-check#r3@0.29: retired with checking#r4 by b370.
- spec-integration#r16@0.29: retired with checking#r4 by b370.
- design-model-check#r4@0.29: retired with checking#r5 by b370.
- design-model-check#r5@0.29: retired with checking#r6 by b370.
- design-model-check#r8@0.29: retired with checking#r10 by b370.
- design-model-check#r107@0.29: retired with checking#r11 by b370.
- design-model-check#r120@0.29: retired with checking#r12 by b370.
- design-model-check#r116@0.29: retired with checking#r13 by b370.
- design-model-check#r52@0.29: retired with checking#r14 by b370.
- design-model-check#r53@0.29: retired with checking#r15 by b370.
- design-model-check#r54@0.29: retired with checking#r16 by b370.
- design-model-check#r103@0.29: retired with checking#r17 by b370.
- design-model-check#r104@0.29: retired with checking#r17 by b370.
- design-model-check#r11@0.29: retired with checking#r25 by b370.
