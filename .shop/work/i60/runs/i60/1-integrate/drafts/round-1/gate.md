# Gate, i60 round 1

## requests (spec/capabilities/requests.md)
Added:
- [r59] **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.
- [r60] **When** `work delegate` writes a delegation in a request, `work` shall commit the request.
- [r61] **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
- [r62] **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
- [r63] **When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date.

Implementation note added: r59, r60: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one.

## supervision (spec/capabilities/supervision.md)
Added:
- [r211] **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started.

## Glossary
No change drafted. Decisions: none. Cut sentences: none.

## Questions
1. Glossary, entry **delegation** says "given with a request"; it can now be given after. Glossary changes are the person's. Yes -> change to: `- **delegation**: the person's words, given with a request or after it is raised, naming the questions a session may answer in the person's place.` No -> entry stays. Recommended: yes.
2. requests#r60: commit on which branch? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." Reading B: r60 stays as drafted.
3. Whose part is the delegation; may either side run `work delegate`? Reading A: only the asker's side: "**If** a side other than the request's asker runs `work delegate`, **then** `work delegate` shall refuse, naming the side that writes the delegation, and change nothing." (r4 then names `work delegate`.) Reading B: either side, no line.
4. Does `work delegate` keep to turns as r16? Reading A: "**If** `work delegate` is run in the other side's turn, **then** `work delegate` shall refuse, because it is the other side's turn, and change nothing." Reading B (recommended, since a delegation comes from the person at any moment): "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is."
5. Does `work delegate` change status or turn? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn." Reading B: no line.
6. r62 names `withdrawn`, a status this spec does not yet name. Reading A (recommended): keep as drafted. Reading B: drop it until it exists: "...`delivered` or `refused`...".
7. r63's narrator is a session; requests' narrator is a context taking in or raising a request. Reading A (recommended): stay in requests. Reading B: move to role-boundaries.
