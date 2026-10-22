---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-release-ledger-snapshot
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-22
---

# Release 0.22.0: coordinator's ledger, as of 2026-10-22

A snapshot of the coordinator's ledger for 0.22.0 (begun as 0.21.1) while the release is open; the live file stays in .shop/scratch/run/ledger-0.22.0.md.

Archived from `.shop/scratch/run/ledger-0.22.0.md` (git-ignored scratch), text as it was.

---

# 0.21.1 ledger (from main 2134b37, branch release-0.21.1)
- The person, 2026-10-21: one requirement per scenario (steps shared in code); lines say exits successfully / with an error; awaiting a ruling = error; do it as 0.21.1 now.
- a8422f9: decisions 0054 (supersedes 0052), 0055; observation 2026-10-21-one-requirement-per-scenario.
- Spec pass dispatched (general agent: this session's installed agents are pre-0.21.0 until restart).
- b392b45 spec lines: supervision r9, r10, r32; dmc r20 + row r107 (v_s2); formulation r4, r11, r13; spec-migration r2, r11; fft r51; exit wording in analysis-tools, batch-measurement, work-queue, migration-tools; i17 with work-items v-s2-one-tag, features-tag-replaces. Open: query commands' 'nothing found' now worded as errors (tools tests-of/untested, features list, model why) — asked the person. Blind formulation round dispatched.
- The person: query commands' 'nothing found' keeps 'exits with an error' (grep convention).
- 0.21.1 not cut: rolled into 0.22.0 (the person, 2026-10-21). Branch renamed release-0.22.0 (pushed; remote release-0.21.1 deleted). Structured output for query commands to be designed in 0.22.0 (default or flag open); 0055 reworded then. kb's migration waits for 0.22.0.
- The person approved (2026-10-22) the fault design: failed status (not final), verify push before a stage, push after every commit, work retry; lines supervision r33-r41, work-queue r8, glossary failed, decision 0056 (cd42cd6). Formulator answered (14 Qs) and asked for scenarios of the new lines.
- The person (2026-10-22): record the formulator's questions, and questions from any other initiative still in the working directory, and any other data worth later analysis; add the five lessons to capability-format and spec-checker in 0.22.0. Gate verdicts exported from the three artifact pages to .shop/scratch/gate-export/; job-only drafts and gate pages copied to .shop/scratch/from-job/. Archive agent (main checkout) and lessons agent (worktree wt-lessons, branch lessons) dispatched.
- lessons DONE on branch lessons (3692513..cbbad8d): spec-consistency r22-r27 (table of finding kinds), review r29 (no-line code = Important), r30 (fix now — beyond the approval: gate decision). capability-format.md 395 lines (Markdown; limit is for code and tests). Merge after the archive agent finishes. Formulator drafts final (no open questions).
