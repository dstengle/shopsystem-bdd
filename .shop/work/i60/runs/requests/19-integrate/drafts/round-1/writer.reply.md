/tmp/work-run-i60-4cwide4y/requests-19-integrate/.shop/scratch/19-integrate/drafts/round-1/spec/capabilities/requests.md

## Change list

| change | capability | id | line | from |
|---|---|---|---|---|
| added | requests | r65 | **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has. | request q39 line 1 |
| added | requests | r66 | **When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch. | q39 line 1, answer 2026-10-29 reading A |
| added | requests | r67 | **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing. | q39 line 2 |
| added | requests | r68 | **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing. | q39 line 3, answer reading A |
| added | requests | r69 | **When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date. | q39 line 4, answer reading A (stays in requests) |
| added | requests | r70 | **When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is. | answer 2026-10-29 reading B |
| added | requests | r71 | **When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn. | answer 2026-10-29 reading A |

Changed: none. Removed: none. Glossary: no change. Retired list unchanged.

Implementation added: "r65, r66: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one."

## Questions

None.

## Cut sentences

None.
