---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-16-release-review-0-36-0
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-16
---

# Release review 0.36.0

A fresh agent's adversarial review of `plan-release-0.35.2` after plan-2.md (main merged with batches 41 and 42, the notes, docs, skill and module-map edits) and the renumbering to 0.36.0, against plan.md, plan-2.md and the first review (2026-11-16-release-review-0-35-2). Verdict: merge as 0.36.0 once finding 1 is fixed; the session fixed findings 1, 4, 5 and 7's wrapping on the branch before the merge.

## Findings

1. **Fix before merge.** CHANGELOG said "Every K in the Y, ordered by T" reads with the order on the Ks "as 0.35.1 read it"; 0.35.1 put it on the Y (`every [x5: file] in(x5, x3) ordered(x3, version, ascending)`), HEAD on the Ks (`... scope give(...) ordered(x5, version, ascending)`). Fixed.
2. **Observation.** No 0.35.1 scenario of such a line existed (0.35.1's features generate exited 1 on the give line, and refused the print form as two meanings), so b328 changes model parse and model logic, not a feature; the y bump stands on b286.
3. **Observation.** b286 confirmed: "print a worktree that holds a file" gained "Given a file f1 / And a worktree w1"; in the ordered variant f1 is now the first member. Side note: in that ordered variant the form orders the worktree (`ordered(x4 worktree, version)`) while the scenario gives the files' versions.
4. **Observation.** b6 resolves only a request whose item records request_lines, which only `work accept` from this release writes; Upgrading should say so. Added.
5. **Observation.** b77: a consumer's ready item with a v15n group is refused at its next ready check or batch start. Added to Upgrading.
6. **Observation.** docs/reference/commands.md's `work batch merged` (b6), `work sync` and `work show` (b39) sections, and troubleshooting.md (v15n, the work shape refusal), lag batches 41 and 42.
7. **Observation.** Two CHANGELOG lines over the 120-column wrap (rewrapped); the commits before the renumbering end `Release: 0.35.2`; the tag is v0.36.0, not plan.md's v0.35.2.

## Checked and holding

Version strings 0.36.0 everywhere; both anchors; docs tests; the merge changes only release text, docs, the skill and CLAUDE.md; only requests#r77 removed from features since v0.35.1; b65's refusal and backlog hint; b40's offer text with and without a capability; b39's optional --from and confirmation line; recipes' --no-line example; the module-map rows.
