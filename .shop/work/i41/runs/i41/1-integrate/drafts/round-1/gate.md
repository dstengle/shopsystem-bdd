# Gate, i41 round 1: supervision

Drafts: .shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md (frontmatter `retired`: r3, r5, r16, r112, r113, r80, r114, r71)

## supervision

### Added
- [r140] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
- [r141] **When** `work run` starts a round of the kind `integrate` for a capability-proposal that has answers, `work run` shall give the round the capability-proposal's questions and answers and the initiative's ledger, with the accepted lines of the request the initiative fulfils.
- [r142] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory.
- [r143] **When** `work run` starts a round of the kind `integrate` for a capability-proposal, `work run` shall keep the proposal's status until the round ends.
- [r144] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall transition the proposal to `approved`.
- [r145] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.
- [r146] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, `work run` shall start a round of the kind `formulate` for the proposal.
- [r147] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall take that as the round's output.
- [r148] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall write no second capability-proposal for that proposal's capability.

### Changed
None.

### Removed (ids retired)
- [r80] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `approved`. (replaced by r144)
- [r114] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied. (replaced by r145)
- [r71] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall start a round of the kind `formulate` for the proposal. (replaced by r146)

## Glossary
No entry added, changed or removed. Decisions: none.

## Questions
1. Glossary: "capability-proposal", "drafts" and "change list" are not glossary terms, though r92, r107, r108 already use them. Add them? Yes: add entries `capability-proposal` (the node of an initiative that names the requirement ids and terms one capability's drafts add, change and remove, taken by `work run` through its gate, apply and formulate rounds), `drafts` (the files a round of the kind `integrate` writes under its drafts path, kept on the initiative branch, which a round of the kind `apply` applies to `spec/`) and `change list` (the list a round of the kind `integrate` or `apply` gives of each requirement and term it adds, changes or removes). No: nothing changes. No reading recommended by the writer.
2. r132 lists "an integrate or apply round's change list" as a stage's output; r147 adds a second output for apply. Yes: retire r132 and add r149 reading "an integrate round's change list; an apply round's change list, or its finding that it applies nothing because the capability-proposal's answers give what its drafts do not hold" (rest as r132). No: r132 stays and r147 extends it.
3. r92 writes a `drafted` capability-proposal for each capability an integrate round's change list names; r148 writes no second one when anew. Reading A (recommended): r92 stays and r148 is the exception when the round was started for a capability-proposal (r140). Reading B: retire r92 and add r149: "**When** a round of the kind `integrate` that `work run` started for an initiative, not for a capability-proposal, ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability."
4. r142 gives two responses. Yes: split; r142 becomes "... `work run` shall set the capability-proposal `drafted`." and r149 is added: "**When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall keep the proposal's earlier drafts in their round's directory." No: r142 stays as drafted.
5. Should a later gate or apply round be given the drafts of the newest integrate round? Yes: add "**When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal that was drafted anew, `work run` shall give the round the path of the kept drafts of the last round of the kind `integrate` that drafted it." No: nothing changes, r108 already says "the round that wrote the proposal".
