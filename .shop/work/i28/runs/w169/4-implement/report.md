## Budget
- agents/initiative-round.md
- skills/integrating-a-proposal/SKILL.md
- agents/capability-writer.md
- docs/capability-format.md

## Changed
Text only, in those four files: an integrate round, given requirement ids other initiatives' drafts add (label "Ids drafted elsewhere"), passes them to the writer, numbers added lines above every listed id on the same capability, and checks the change list's adds against them. No ids given: numbering unchanged. Ids on other capabilities and term/ ids do not count; round 2+ uses its own brief's ids.

## Red/green
spec-integration is a guarantees capability: no scenario. `python3 -m pytest -q --work-item w169` collects none (per plan; not re-run: nothing to assert). Suite record at start: 859 passed, 0 failed at 24bbf163 (4 expected-red titles listed in brief, none this work-item's).
Plan contained no code.

## Tests changed under an allowance
none

## Open questions
- The label "Ids drafted elsewhere" must match what w170's integrate_lines writes; w170 should use it or reconcile.
- A given id equal to an existing spec/ id: covered by "above the highest"; stated in the round text.

## Outside the file set
none

## tools size
(no files over 300 lines; printed nothing)

Commit: 4e17518d. Concerns: none.
