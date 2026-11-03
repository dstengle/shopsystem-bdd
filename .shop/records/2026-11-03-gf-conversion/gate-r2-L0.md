---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-L0
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion, revision 2: layer 0 (baselines)

Taken by the layer 1 gate on `gf-conversion` before merging R1–R3 (layer 0 had not run when the packages
started; R1 built its own L0 from a `git archive` of 864f61e9 and found the same empty list).

1. `- **push** (event): …` moved unchanged from `spec/capabilities/role-boundaries.md` to `spec/index.md`'s
   glossary, after `commit`. `model lexicon --check`: 386 terms, 0 problems, before and after.
2. `logic-baseline-r2.json`: `python3 scripts/model logic --json` on the code of 7e0684d2 (864f61e9 adds only
   records). Exit 0, **310 s** wall time. Findings: 7, all L2 (analysis-tools r2/r3/r4, r41/r42; batch-measurement
   r4/r5, r9/r23; feature-file-tools r1/r2; migration-tools r11/r12/r13, r16/r18); no L1, L3 or L4. A second run
   gave the same bytes.
3. `.shop/scratch/unparsed.sh` written with the plan's text (gitignored).
4. `unparsed-L0.txt`: 0 lines. Every Behaviour and U line parses.
