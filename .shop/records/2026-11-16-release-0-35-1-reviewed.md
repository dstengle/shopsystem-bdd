---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-16-release-0-35-1-reviewed
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-16
---

# Release 0.35.1 reviewed

A fresh agent's adversarial review of the branch `plan-release-0.35.1` (four commits) against its plan `.shop/records/2026-11-16-release-0.35.1/plan.md`, each claim of the release notes tested on scratch copies of the construct catalogue's context and of this repository's `spec/` with main's `scripts/model` and `scripts/features`. Verdict: mergeable once findings 1 and 2 are corrected, which the session did on the branch before the merge.

## Findings

1. **Fix before merge.** CHANGELOG.md's b297 bullet and docs/writing-requirements.md said holds-exactly on a response's object reads "any restriction" its every half reads. A relative clause that reaches a second thing ("... holds exactly the files that cover the line of a stage") is still `unread ... no translation of a negated restriction (not) on an object` with `print` and with `return`, while its every half alone reads. A value, a negated value, "that a session keeps", "that cover a line", "that do not cover a line" and "that no session keeps" read in both tools. Corrected to name those.
2. **Fix before merge.** docs/upgrading.md said all four forms "are now read by `model logic`". "holds no K" and an order on a verb framed on the collection's kind were read by `model logic` in 0.35.0 (b299's and b298's notes; spec_lf_quant.negated unchanged); only their scenarios are new. Corrected.
3. **Observation.** writing-requirements' "An order is a property of a response's object, whatever the act" overreaches for order-by-every: it reads after a verb framed on `thing`, fails to parse after a verb framed on the member's kind (b300), and gets no scenario after one framed on the collection's kind (b312). Corrected on the branch, and the CHANGELOG names b300 and b312. grammar/language.md and the refusal messages still say "what a response prints" (b302).
4. **Observation.** The z bump holds: `git diff v0.35.0 main -- features/` only adds the scenarios of r314, r315, r125-r128 and r41, and every new code path was a TraceError or a refusal before. Unsaid: 0.35.0's `features generate` only warned (`no scenario: ...`) and exited 0 for "holds no K" and the framed order, so a consumer may hold such lines and find its features stale after the upgrade. Added to upgrading.md.
5. **Observation.** The order-by scenario of "a worktree that holds a file, ordered by ..." says "the worktree w1 holds the file f1" with no Given bringing in f1, on `print` as on `return`; from 0.35.0 (b311).
6. **Observation.** The branch's commits end only in `Release: 0.35.1`, without the attribution trailers main's commits carry.
7. **Observation.** "shall return a worktree that holds nothing" beside "shall not return a worktree that holds a file" gives an L1 though the two restrictions cannot hold of one worktree; the same with `print` and with 0.35.0's "holds no file". The check's existing coarseness, newly reachable.

## Checked and true

"holds nothing" and "holds no file" get their Thens after the act, the latter with a file the worktree does not hold, after `return` framed on worktree and after `write` and `print` in this repository's spec; the CHANGELOG's b298 example generates the order Then and the three-member counter-example; b307's `_logic` adds `<id>: no translation: <why>` for the item's ids; r41, r125-r128, r314, r315 pass; the docs tests pass; the version strings and both anchors are right.
