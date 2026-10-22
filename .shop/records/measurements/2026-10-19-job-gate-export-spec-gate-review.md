---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-job-gate-export-spec-gate-review
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# Spec Gate Review: the person's verdicts and line notes

The person's verdicts and line notes on the Spec Gate Review page, exported from the page's review store (collections `verdicts` and `lineNotes`) and copied out of a job workspace on 2026-10-22. `at` is the save time in epoch milliseconds: these were saved on 2026-10-19, 00:18-15:16 UTC. They are the person's own words, kept exactly. They judge the page's earlier content (i1's first-spec proposals, i2, i3's requirement-ids and i9's ubiquitous-language proposals, decisions 0022-0034, initiatives i8, i10 and i11, and question cards `carry`, `deprecated`, `forms`, `glossary`, `glossary2`, `labels`); the copy of the page in initiative-archive/2026-10-21-job-gate-pages holds its later i13 (EARS) content, so the questions' card texts are not in it. A `verdict` of null is a note saved without a verdict.

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0022.json`

~~~~~~
{
  "at": 1792413836399,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-adopts-the-design-model",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0023.json`

~~~~~~
{
  "at": 1792413904471,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/scenario-names-requirement-by-tag",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0024.json`

~~~~~~
{
  "at": 1792413898796,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/retired-ids-in-capability-frontmatter",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0025.json`

~~~~~~
{
  "at": 1792413917462,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/model-check-solves-with-clingo",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0026.json`

~~~~~~
{
  "at": 1792413949496,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-file-forms",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0027.json`

~~~~~~
{
  "at": 1792413973563,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/capability-ids-are-context-scoped",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0028.json`

~~~~~~
{
  "at": 1792414122187,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-scenarios-run-as-unittest",
  "note": "Why unittest? scenarios are gherkin and broken down into step files.",
  "type": "decision",
  "verdict": null
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0031.json`

~~~~~~
{
  "at": 1792419771035,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/held-scenario-formulates-no-requirement",
  "note": "What does \"held\" mean. I find this term confusing. What are synonyms that would work here.",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0032.json`

~~~~~~
{
  "at": 1792414292548,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/model-reads-a-ledger",
  "note": "decisions.md is supposed to be generated, if there are decisions, they MUST map to a file in the decision directory.",
  "type": "decision",
  "verdict": null
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0033.json`

~~~~~~
{
  "at": 1792414303398,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/glossary-terms-are-standing",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/decision-0034.json`

~~~~~~
{
  "at": 1792414307045,
  "item": "design-decision/missingmass.io/shopsystem/shopsystem-bdd/consistency-check-on-demand",
  "note": "",
  "type": "decision",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/ext-design-model-check.json`

~~~~~~
{
  "at": 1792419651623,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/withdrawn-design-model-check",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-analysis-tools.json`

~~~~~~
{
  "at": 1792371405996,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-analysis-tools",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-batch-analysis.json`

~~~~~~
{
  "at": 1792371585835,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-batch-analysis",
  "note": "",
  "type": "proposal",
  "verdict": null
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-batch-measurement.json`

~~~~~~
{
  "at": 1792420705022,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-batch-measurement",
  "note": "Batch-measurement is a lower priority and can be held for the release right after the migration release. Will this have any repurcussions on the migration release?",
  "type": "proposal",
  "verdict": "change"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-code-research.json`

~~~~~~
{
  "at": 1792372036708,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-code-research",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-feature-file-tools.json`

~~~~~~
{
  "at": 1792420728574,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-feature-file-tools",
  "note": "It seems like in this instance carry could be replaced by keep? If so, replace any instance of carry with keep when it fits.",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-formulation.json`

~~~~~~
{
  "at": 1792418994507,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-formulation",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-red-green.json`

~~~~~~
{
  "at": 1792372244078,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-red-green",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-review.json`

~~~~~~
{
  "at": 1792419003278,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-review",
  "note": "What is the behind the name \"first-spec-review\"? Why is it first-?",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-role-boundaries.json`

~~~~~~
{
  "at": 1792422949125,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-role-boundaries",
  "note": "specs are standing, not moving. This should be initiative-round\n\nThe implementer should certainly have access to skills. bdd-red-green is only a development strategy/process, not an actual coding skill, like front-end coding, etc. Is the concern that the implementer would deviate from the red-green order of doing things?",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-slice-plan-tool.json`

~~~~~~
{
  "at": 1792413615369,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-slice-plan-tool",
  "note": "This is where I thought we were moving to work with initiatives and work-items. work-items have dependencies that replace slicing, or can you explain how they go together?",
  "type": "proposal",
  "verdict": null
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-slicing.json`

~~~~~~
{
  "at": 1792413705600,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-slicing",
  "note": "See previous question about slicing",
  "type": "proposal",
  "verdict": null
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-spec-integration.json`

~~~~~~
{
  "at": 1792419654705,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-spec-integration",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i1-spec-migration.json`

~~~~~~
{
  "at": 1792413846452,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-spec-migration",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i2-design-model-check.json`

~~~~~~
{
  "at": 1792371418731,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/model-check",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i3-design-model-check.json`

~~~~~~
{
  "at": 1792422943484,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-design-model-check",
  "note": "r22 - agreed, only accept single form\n\n@holding still doesn't make sense to me.  It doesn't indicate direction, since you can hold things for release that will eventually go out, which is not this situation. Can we use deprecated?\n\nHow many places are we using the term hold? Are any of them ambiguous. Can they be replaced.\n\nThe same goes for carry or carries. Does this mean contain or lifting up something else? ",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i3-feature-file-tools.json`

~~~~~~
{
  "at": 1792418534139,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-feature-file-tools",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i3-formulation.json`

~~~~~~
{
  "at": 1792370238326,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-formulation",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i3-spec-integration.json`

~~~~~~
{
  "at": 1792370366469,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-spec-integration",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i3-spec-migration.json`

~~~~~~
{
  "at": 1792371427279,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-spec-migration",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i9-design-model-check.json`

~~~~~~
{
  "at": 1792369127034,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-design-model-check",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i9-feature-file-tools.json`

~~~~~~
{
  "at": 1792417593673,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-feature-file-tools",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i9-formulation.json`

~~~~~~
{
  "at": 1792369404424,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-formulation",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i9-spec-consistency.json`

~~~~~~
{
  "at": 1792417744689,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-spec-consistency",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/i9-spec-integration.json`

~~~~~~
{
  "at": 1792418096201,
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-spec-integration",
  "note": "",
  "type": "proposal",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/initiative-i10.json`

~~~~~~
{
  "at": 1792417569018,
  "item": "initiative/missingmass.io/shopsystem/shopsystem-bdd/i10",
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/initiative-i11.json`

~~~~~~
{
  "at": 1792417570350,
  "item": "initiative/missingmass.io/shopsystem/shopsystem-bdd/i11",
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/initiative-i8.json`

~~~~~~
{
  "at": 1792417575677,
  "item": "initiative/missingmass.io/shopsystem/shopsystem-bdd/i8",
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/question-carry.json`

~~~~~~
{
  "at": 1792422939866,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/question-deprecated.json`

~~~~~~
{
  "at": 1792422914006,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/question-forms.json`

~~~~~~
{
  "at": 1792421019674,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/question-glossary.json`

~~~~~~
{
  "at": 1792419675267,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/question-glossary2.json`

~~~~~~
{
  "at": 1792421955513,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/verdicts/question-labels.json`

~~~~~~
{
  "at": 1792422968878,
  "note": "I think I get it now, but workflow is much too generic here. What else can we use?",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-batch-measurement-r1.json`

~~~~~~
{
  "at": 1792371764713,
  "capability": "batch-measurement",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-batch-measurement",
  "line": "r1",
  "note": "The term \"fact\" is being used in multiple ways in the same bounded context. What is this facts file? Is this the pre-existing skill? Will it be used in the future and if so, this should be scheduled for change in a future version."
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-batch-measurement-r34.json`

~~~~~~
{
  "at": 1792371957558,
  "capability": "batch-measurement",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-batch-measurement",
  "line": "r34",
  "note": "This language is confusing."
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-batch-measurement-r4.json`

~~~~~~
{
  "at": 1792418599927,
  "capability": "batch-measurement",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-batch-measurement",
  "line": "r4",
  "note": ""
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-feature-file-tools-r14.json`

~~~~~~
{
  "at": 1792418954719,
  "capability": "feature-file-tools",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-feature-file-tools",
  "line": "r14",
  "note": ""
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-feature-file-tools-r8.json`

~~~~~~
{
  "at": 1792372109504,
  "capability": "feature-file-tools",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-feature-file-tools",
  "line": "r8",
  "note": "Same question about slices"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-role-boundaries-r1.json`

~~~~~~
{
  "at": 1792419069412,
  "capability": "role-boundaries",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-role-boundaries",
  "line": "r1",
  "note": "What is a spec-round?"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i1-role-boundaries-r4.json`

~~~~~~
{
  "at": 1792419047366,
  "capability": "role-boundaries",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/first-spec-role-boundaries",
  "line": "r4",
  "note": "Why no skill tool?"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i3-design-model-check-r22.json`

~~~~~~
{
  "at": 1792418433902,
  "capability": "design-model-check",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-design-model-check",
  "line": "r22",
  "note": "Why have two different forms? That is my confusion, not necessarily the name, although I like requirement better"
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i3-feature-file-tools-r11.json`

~~~~~~
{
  "at": 1792418523626,
  "capability": "feature-file-tools",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/requirement-ids-feature-file-tools",
  "line": "r11",
  "note": "Agreed on withdrawing slicing."
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i9-feature-file-tools-r52.json`

~~~~~~
{
  "at": 1792369342846,
  "capability": "feature-file-tools",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-feature-file-tools",
  "line": "r52",
  "note": "Is it necessary to enumerate subcommands here or should this be an invariant that gets handled in a way that always works."
}
~~~~~~

## `.shop/scratch/gate-export/spec-gate-review/lineNotes/i9-spec-integration-r16.json`

~~~~~~
{
  "at": 1792417539436,
  "capability": "spec-integration",
  "item": "capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ubiquitous-language-spec-integration",
  "line": "r16",
  "note": ""
}
~~~~~~
