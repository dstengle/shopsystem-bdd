/tmp/work-run-i29-uk3_aing/supervision-5-apply/.shop/scratch/5-apply/drafts/round-2/spec/capabilities/supervision.md

## Change list

The drafted sections are Purpose and Behaviour, each whole, built from the current spec/capabilities/supervision.md. r100, r101, r9 and r82 are kept as the current spec has them. The frontmatter does not change: `retired` stays `[]`.

| change | capability | id | line | source |
|---|---|---|---|---|
| added | supervision | r105 | **When** `work run` finds an initiative that is not `done`, that has at least one work-item, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. | answers 1 (a) "keep r105's wording", 2 (a) "add 'that has at least one work-item' to r105", 3 (a) "r105 also requires 'and whose measurement and analysis record `work run` has committed'" |
| added | supervision | r106 | **When** `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch. | round-1 draft, as drafted (no answer changes it) |
| added | supervision | r107 | **If** a change list that `work run` reads names a capability that neither `spec/capabilities/` nor the round's drafts have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability. | answers 5 (a) "r107 exempts a capability the round's drafts add ('...neither `spec/capabilities/` nor the round's drafts have...')", 6 (a) "r107 as drafted (only the missing capability gets no proposal)" |
| added | supervision | r108 | **When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the round of the kind `integrate` that wrote the proposal. | round-1 draft, as drafted (no answer changes it) |
| added | supervision | r109 | **When** `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch. | answer 4 (a) "add a new line: 'When `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.'" |

No lines changed or removed. No glossary terms added, changed or removed.

Purpose changes from the current spec. The clause "and starts the initiative's measurement and analysis" becomes "starts the initiative's measurement and analysis and commits them, and sets the initiative `done`, committing it, when what it delivers is closed". This covers r106, r105 and r109.

## Questions

None.

## Cut sentences

None.
