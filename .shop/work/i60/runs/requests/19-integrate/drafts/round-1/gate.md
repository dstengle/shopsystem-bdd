# Gate, requests q39, integrate round 1

## requests (spec/capabilities/requests.md)
Added:
- [r65] **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.
- [r66] **When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch. (answer 2026-10-29, reading A)
- [r67] **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
- [r68] **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
- [r69] **When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date.
- [r70] **When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is. (answer 2026-10-29, reading B)
- [r71] **When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn. (answer 2026-10-29, reading A)
Changed: none. Removed: none.
Implementation note added: r65, r66: `work delegate` is a command of `scripts/work`; it writes the delegation as the frontmatter field `delegation`, replacing the field's value where the request has one.

## supervision
No change: r211 (line 5) is already in spec/.

## Glossary
No change drafted (entry **delegation**, "given with a request", is the person's to change and no answer to it is given). Decisions: none. Cut sentences: none.

## Questions
1. r70 (whichever side's turn it is) and the answer that either side may run `work delegate` meet r16 ("a command other than `work resolve` ... in the other side's turn ... refuse") and r55 (a side writing the other side's part is refused when the asker is not the upstream itself). Reading A (recommended): the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes. Reading B: r16 and r55 are retired and redrafted with "other than `work resolve` and `work delegate`".
