/tmp/work-run-i51-66fnayzb/supervision-6-integrate/.shop/scratch/6-integrate/drafts/round-6/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | supervision | r162 | **When** a question of an initiative names a term of the glossary or a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation. | "the person replaces the 'mentions the glossary' rule with a check triggered by a change to the glossary." |
| removed | supervision | r163 | **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that names neither a term of the glossary nor a glossary-proposal to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise. | "the person replaces the 'mentions the glossary' rule with a check triggered by a change to the glossary." |
| added | supervision | r209 | **When** a question of an initiative is a question of a glossary-proposal or has a reading that adds, changes or removes a `term/<term>`, `work run` shall leave the question for the person, giving it to no session under a delegation. | "A question of a glossary-proposal, or a question one of whose readings adds, changes or removes a term/<term>, is left for the person and given to no session under a delegation" |
| added | supervision | r210 | **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that is neither a question of a glossary-proposal nor has a reading that adds, changes or removes a `term/<term>`, whatever words it uses, to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise. | "every other question of the initiative is given to a session under the delegation, whatever words it uses." (the session of its own, the delegation, the files that one question names and nothing else, answering if covered and leaving it for the person otherwise, from q37 line 2) |

The frontmatter is drafted whole, with r162 and r163 added to `retired`. The whole Behaviour section is drafted, with r209 and r210 where r162 and r163 were. No glossary term is added, changed or removed, and no decision is drafted. r176 and r188-r190 are not drafted.

## Questions

None.

## Cut sentences

- "r176 (a question on a term names the glossary) is dropped, since the check no longer reads the question's words." This is an instruction about the draft. r176 was never in spec/, so it is not drafted.
- "No word of the question is matched against the glossary's terms." r209 and r210 follow this: they test only what a question is of and what its readings change, never its words. It is not a Behaviour line of its own.
- "r174 and r175 are redrafted to say so" This is an instruction about the draft. The redrafted lines are r209 and r210.
