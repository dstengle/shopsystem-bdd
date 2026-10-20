---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-ubiquitous-language-test-log
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-17
---

# A ubiquitous language: test log (0.20.0)

Branch `0.20.0-ubiquitous-language`, commits `25aaec3` to the release commit. Plugin B for the runs is a detached
worktree at `73ee3fb`. Numbers are from the controller's evidence files for Task 6 and the SDD ledger.

## What changed

- Glossary terms: entries in `spec/index.md` are terms (`term/<name>`) with the words they avoid (`Not:`). The
  design model reads them and checks three rules: `v_t1` (a line or scenario uses an avoided word), `v_t2` (a term
  with two entries) and `v_t3` (a term that avoids a term of its own glossary).
- The consistency skill `checking-spec-consistency` and the `spec-checker` agent: report mode and fix mode; the
  integration and formulation skills teach the glossary terms.
- `model` finds clingo behind a virtualenv: it tries the other `python3` interpreters on the PATH, and says what it
  tried when none holds clingo.
- `features` takes `--file`: `tag`, `hold`, `retire`, `move` (r52-r55) and `rebind` (r56) can be limited to one
  feature file, which removes the by-hand tagging of a title that appears in two files.
- Version 0.20.0, README, `spec/index.md`. Initiative i9's proposals are drafted and await the gate.

## Fixture cases and results

Fixture: the type-first shelf spec, `lend-items` formulated, glossary entries `book` (Not: item) and `friend`.
Planted: (a) `volume` for `book` in lend-items#r3 and its scenario, (b) keep-items#r3's scenario answering with
titles where the line says the number, (c) lend-items#r7 "too many books" with no bound.

**consistency-report** (report mode; stop when the findings are written). Checks: the findings name (a) with both
words, (b) by title or keep-items r3, (c) as lend-items r7; `spec/` and `features/` unchanged; no commit.

| run | result | cost |
|---|---|---|
| 1 | ok 5/5 | $0.29, 8 turns |
| 2 | ok 5/5 | $0.29 |
| 3 | ok 5/5 | $0.29 |

**consistency-fix** (the prompt gives the answers: approve `book` with `volume` avoided; for (b) the line is right;
for (c) reading A, "more than 3 books"; defer the rest). Checks: the glossary avoids `volume` under `book`; no line or
scenario says `volume`; `model check` shows no `v_t` row, 0 unresolved, 0 file problems, no new violation; ids kept
and no other line reworded; suite green; a commit names `volume`; r7 bounded at 3; the keep-items r3 scenario
follows its line.

| run | result | cost |
|---|---|---|
| 1 | ok 8/8 | $0.47, 20 turns |
| 2 | ok 8/8 | $0.42, 16 turns |
| 3 | ok 8/8 | $0.54, 22 turns |

Report 3/3 and fix 3/3. Fix-1's commits each name their ids and terms: the spec change (`term/book`, lend-items#r3),
the scenarios following, r7 bounded to "more than 3 books" and its scenario, and the plan backlog entry.

## The scorer fix

Fix-1 first scored FAIL on r7. The scorer rejected any "too many", but the line keeps "because the friend has too
many books" as its reason for refusing. The scorer now rejects only "who has too many" (the unbounded form). Fix-1
was rescored ok, the self-test is clean, and its reading mutation still fails. The controller made this fix in the
scratch harness, outside the repository, and it was not reviewed.

## kb report-mode run

A clone of the id-migrated kb trial (`a52b712`), plugin B at `73ee3fb`, one session in report mode.

- Cost $3.28, 32 turns, 22 `spec-checker` dispatches (21 capabilities and the whole context), all returned.
- 77 findings: 40 on terms, 10 lines with two readings, 27 other drift. Of the terms, 22 are one cluster
  (scenarios say "version" where lines say "revision"); others are history/journal, folder/directory,
  part/item/node, check/validate, fault/error/violation, client/caller, kind/type, role/actor, piece of
  work/execution, set/batch, words for two things (name, place, version, reference) and one missing term.
- The trial's three issues were all found: version/revision (F19-F40); journal/history (a two-words cluster);
  and the query-the-store r6 mismatch (F70, "each with what links to it" against the scenario's pinned outcome),
  which is classed as drift, not as two readings.
- `model check` gave 10 `v_s3` and no `v_t` rows (kb has no glossary), with clingo found. The session said it does not
  know what `v_s3` means: the skill does not gloss it.
- Nothing outside `.superpowers/spec-drafts/` changed and nothing was committed.

## What the reviews and rounds caught

- **Search order**: `model` did not pin the order it searched interpreters in; fixed and asserted (the tried list too).
- **Paths**: an empty PATH entry and a virtualenv's `bin/` were not resolved.
- **A held scenario** was left unpinned by a test.
- **Every row**: the skill read ten rows where a check had more; it now passes `--limit`.
- **Rebind**: a hold changes a title, and `features rebind` could not be limited to the file; it takes `--file` (r56).
- **Order**: `v_t1` rows of a newly avoided word are allowed in the spec commit until formulation rewords them.
- **Slicing**: a reworded step holds the old scenario and goes to slicing; a title-only reword is rebound.
- **Two entries for one word**: the shared word goes to one entry, the other meaning takes a new word.
- **Carried from 0.19.0**: Adding Ids commits `decisions/`, `records/` and `work/` and rewrites `obs/` references.

## Not tested

- Fix mode on kb.
- A run where a term change rides with a capability-proposal in a repository with `work/`.
- The full path of fix step 1 (more than two lines changed, through `spec-round`).
- The clingo-missing path of `checking-spec-consistency`.
- A title shared by two feature files, held and rebound through `--file` in a session (the script test covers it).
- A real batch in a consuming repository, measured with `scripts/measure`.
