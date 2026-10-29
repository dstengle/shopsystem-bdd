/tmp/work-run-i60-_83tsys1/i60-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/requests.md
/tmp/work-run-i60-_83tsys1/i60-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | note sentence |
|---|---|---|---|---|
| added | requests | requests#r59 | **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has. | "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has, and commit the request." (line 1) |
| added | requests | requests#r60 | **When** `work delegate` writes a delegation in a request, `work` shall commit the request. | "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has, and commit the request." (line 1; its second response, split off so each line has one response) |
| added | requests | requests#r61 | **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing. | "**If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing." (line 2) |
| added | requests | requests#r62 | **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing. | "**If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing." (line 3) |
| added | requests | requests#r63 | **When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date. | "**When** the person gives a session a delegation for a request outside `work request`, the session shall write it in the request with `work delegate` in the same reply, in the person's words and with the date." (line 4) |
| added | supervision | supervision#r211 | **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started. | "**When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started." (line 5) |

No glossary term added, changed or removed.

Implementation, may change (requests), added: "r59, r60: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one."

## Questions

1. requests, the glossary: the entry **delegation** says "given with a request"; a delegation can now be given after the request is raised. Glossary changes are never delegated, so this is the person's to decide. If yes, the entry would read: `- **delegation**: the person's words, given with a request or after it is raised, naming the questions a session may answer in the person's place.` If no, the entry stays.
2. requests#r60: the note says "commit the request" but not on which branch. If on the current branch, as r12 says for the other commands: "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." (Or r12 changed to name `work delegate`, and r60 dropped.) If not, r60 stays as drafted.
3. requests: whose part of a request is the delegation, and may either side run `work delegate`? If only the asker's side: "**If** a side other than the request's asker runs `work delegate`, **then** `work delegate` shall refuse, naming the side that writes the delegation, and change nothing." r4 would then need `work delegate` in its list of what writes the asker's part. If either side may: no line, and r4 and r34 stay as they are.
4. requests: does `work delegate` keep to turns, as r16 does for the other commands that write a part of a request? If yes: "**If** `work delegate` is run in the other side's turn, **then** `work delegate` shall refuse, because it is the other side's turn, and change nothing." If no, with the line I would write: "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is."
5. requests#r59: the note says nothing about whether `work delegate` changes the request's status or turn. If it leaves them as they are: "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn."
6. requests#r62: `withdrawn` is not a request status this spec names yet (withdrawing a whole request is under Not yet). Should r62 keep `withdrawn` as it is, ready for when the status exists, or drop it until then: "**If** `work delegate` is given a request that is `delivered` or `refused`, **then** `work delegate` shall refuse, naming the request's status, and change nothing."
7. requests#r63: this line's narrator is a session the person talks to. The capability's narrator is "a context taking in or raising a request". Should it stay in requests, as the placement says, or go to role-boundaries, the capability for what a session does?

## Cut sentences

None. Every line of the note landed in a Behaviour line. The request's title, "A delegation is given to a request after it is raised", is the heading, not a sentence of the note.
