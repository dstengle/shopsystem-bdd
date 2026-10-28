# formulate: spec-integration (r54, r55)

## Draft
/tmp/work-run-i46-0i81ojqg/spec-integration-1-formulate/.shop/scratch/1-formulate/drafts/spec-integration.feature

As the input prompt asked, this is the whole feature file. Scenarios @r44, @r45 and @r46 are unchanged. Two scenarios are new: @r54 and @r55. r17 is retired, so it has no scenario.

## Coverage
| line | scenario |
|---|---|
| r54 | @r54 a round of the kind integrate that drafts a change to the glossary gives the terms it adds, changes and removes in the change list's entry for the glossary and in no entry for a capability |
| r55 | @r55 while the person has not approved the terms of a glossary-proposal, no round applies any of them to spec/index.md |

## Questions
None. I read r54 and r55 each in one way. Both scenarios avoid the case listed under "Partial approval" below.

## Cases no line mentions
- Partial approval (r55). Suppose the person approves some of a glossary-proposal's terms and refuses or questions others. One reading is that no term is applied until all of them are approved. The other is that each approved term is applied on its own. The @r55 scenario uses a glossary-proposal with none of its terms approved, so it does not choose a reading. If this case matters, it is a question for the spec.
- Which round r55 constrains. The scenario shows a round of the kind apply that runs on another approved capability-proposal of the same initiative. No line says whether a round of the kind apply can be started on a glossary-proposal that is not approved, or what it would do then.
- A round of the kind integrate whose glossary change only rewrites a term's "Not:" words (r54). I take that to be a changed term, but no line says so.
- A round of the kind integrate that drafts a glossary change but no capability line (r54). The change list would then have no capability entry at all. No line says whether the change list must still have the glossary entry in that case. I assume it must.
