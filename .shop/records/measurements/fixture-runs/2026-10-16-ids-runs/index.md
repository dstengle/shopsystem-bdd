---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-ids-runs
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-16
---

# Fixture harness runs (ids/runs): the per-run facts, 2026-10-16 to 2026-10-20

The per-run facts of the headless fixture harness in `/home/vscode/scratch/shopsystem-bdd/ids/runs/` (git-ignored scratch), one section per run directory, grouped by case family: each run's `case`, `base` (the fixture's commit), `prompt.txt`, `fixture.log` (the fixture's suite before the run), `stderr.log`, `work-run.out`, `score.txt`, `seconds`, `session-exit` and baseline captures, inline as they were (the body below was assembled from those files by a one-off script, /tmp/archive-tools/fixtures/gen_runs.py, which copied each file's text verbatim; prompts byte-identical across runs are shown once per family). Each run was one `claude -p` session on a fresh fixture; the scores and costs of the A/B/T/U runs are in the records `2026-10-16-0-19-0-ids-fixture-scores-and-costs`, `2026-10-17-0-19-0-type-first-ids-fixture-scores` and `2026-10-17-0-20-0-consistency-fixture-scores`, the test-* self-test results in `2026-10-17-ids-harness-selftest`, and the deliver-real runs (shake, g1, r1, s1, v1-v3, x1, ro-*) are summarised in `2026-10-20-deliver-real-test-log.md`; A/B in `2026-10-16-requirement-ids-test-log.md`, T in its "Type-first ids" section, U in `2026-10-17-ubiquitous-language-test-log.md`. Left in scratch: each run's `repo/` (the fixture repository after the run) and the transcript*.jsonl session logs (counts and sizes are listed per run).

Assembled from the run directories under `/home/vscode/scratch/shopsystem-bdd/ids/runs/` (git-ignored scratch); file texts as they were.

---

Run directories: 94. Transcripts (transcript*.jsonl) in them: 77 files, 6120641 bytes, left in scratch.

## A: 0.18.0 (plugin A at e3c846d), scored with 0.19.0's checks, cost only (2026-10-16)

**prompt.txt** (byte-identical in A-formulate-1, A-formulate-2):

```text
The lending note's lines are approved and committed in spec/ (see git show HEAD: lend-items is new, and keep-items' count line changed). Use shopsystem-bdd:formulating-features for those two capabilities and commit. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/A/scripts. Stop when the features are committed: do not slice, plan or implement. Questions that come back are shown to me at the end, with their two readings; everything else is written and committed, as the skill says. I am away, so ask me nothing and wait for nothing.
```

**prompt.txt** (byte-identical in A-integrate-1, A-integrate-2):

```text
The brainstorming note docs/superpowers/specs/2026-10-02-lending-design.md is approved. Use shopsystem-bdd:integrating-a-proposal to integrate it into spec/. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/A/scripts. Stop at the gate: show me the added, changed and removed Behaviour lines and the questions, and end your turn there. I will answer in my next message. Apply nothing to spec/ before I answer, and ask me nothing else before the gate.
```

### A-formulate-1

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (257531 B)
- transcripts: 1 (257531 B), not archived
- repo/: present, not archived

`base`: `20b07aa`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.14s
```

`stderr.log`: empty

### A-formulate-2

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (244610 B)
- transcripts: 1 (244610 B), not archived
- repo/: present, not archived

`base`: `8652adb`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.10s
```

`stderr.log`: empty

### A-integrate-1

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (193047 B)
- transcripts: 1 (193047 B), not archived
- repo/: present, not archived

`base`: `ac44e41`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.09s
```

`stderr.log`: empty

### A-integrate-2

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (185876 B)
- transcripts: 1 (185876 B), not archived
- repo/: present, not archived

`base`: `c271cfb`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.14s
```

`stderr.log`: empty

## B: 0.19.0 requirement ids (plugin B at 8b61d65) (2026-10-16)

**prompt.txt** (byte-identical in B-apply-1, B-apply-2, B-apply-3):

```text
The brainstorming note docs/superpowers/specs/2026-10-02-lending-design.md is approved, and its integration round 1 is done: the drafts are in .superpowers/spec-drafts/2026-10-02-lending-design/round-1/, and the gate you showed me is gate.md there. My answer, on 2026-10-16: "Yes, the lines are approved as shown." Use shopsystem-bdd:integrating-a-proposal to apply the approved drafts to spec/ and commit. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop when spec/ is committed: do not formulate, slice, plan or implement. I am away, so ask me nothing and wait for nothing.
```

**prompt.txt** (byte-identical in B-formulate-1, B-formulate-2, B-formulate-3, B-noclingo-1, B-noclingo-2, B-noclingo-3):

```text
The lending note's lines are approved and committed in spec/ (see git show HEAD: lend-items is new, and keep-items' count line changed). Use shopsystem-bdd:formulating-features for those two capabilities and commit. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop when the features are committed: do not slice, plan or implement. Questions that come back are shown to me at the end, with their two readings; everything else is written and committed, as the skill says. I am away, so ask me nothing and wait for nothing.
```

**prompt.txt** (byte-identical in B-integrate-1, B-integrate-2, B-integrate-3):

```text
The brainstorming note docs/superpowers/specs/2026-10-02-lending-design.md is approved. Use shopsystem-bdd:integrating-a-proposal to integrate it into spec/. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop at the gate: show me the added, changed and removed Behaviour lines and the questions, and end your turn there. I will answer in my next message. Apply nothing to spec/ before I answer, and ask me nothing else before the gate.
```

**prompt.txt** (byte-identical in B-migrate-1, B-migrate-2, B-migrate-3):

```text
This repository is on capability files, but its Behaviour lines carry no [r<n>] ids. Use shopsystem-bdd:migrating-to-capabilities to add them. The context id is missingmass.io/demo/shelf: the owner's domain missingmass.io, the product demo, the context shelf; that is my answer for the gate's context id. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop when it is committed. I am away, so ask me nothing and wait for nothing.
```

### B-apply-1

- files: base (8 B), case (6 B), fixture.log (18 B), prompt.txt (619 B), stderr.log (0 B), transcript.jsonl (92276 B)
- transcripts: 1 (92276 B), not archived
- repo/: present, not archived

`base`: `cd62c63`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.13s
```

`stderr.log`: empty

### B-apply-2

- files: base (8 B), case (6 B), fixture.log (18 B), prompt.txt (619 B), stderr.log (0 B), transcript.jsonl (96474 B)
- transcripts: 1 (96474 B), not archived
- repo/: present, not archived

`base`: `991f00f`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.12s
```

`stderr.log`: empty

### B-apply-3

- files: base (8 B), case (6 B), fixture.log (18 B), prompt.txt (619 B), stderr.log (0 B), transcript.jsonl (86232 B)
- transcripts: 1 (86232 B), not archived
- repo/: present, not archived

`base`: `1288eb4`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.09s
```

`stderr.log`: empty

### B-formulate-1

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (218787 B)
- transcripts: 1 (218787 B), not archived
- repo/: present, not archived

`base`: `05f3361`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.13s
```

`stderr.log`: empty

### B-formulate-2

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (226067 B)
- transcripts: 1 (226067 B), not archived
- repo/: present, not archived

`base`: `b0c10d1`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.09s
```

`stderr.log`: empty

### B-formulate-3

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (240050 B)
- transcripts: 1 (240050 B), not archived
- repo/: present, not archived

`base`: `7ffd20a`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.09s
```

`stderr.log`: empty

### B-integrate-1

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (206035 B)
- transcripts: 1 (206035 B), not archived
- repo/: present, not archived

`base`: `277989a`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.19s
```

`stderr.log`: empty

### B-integrate-2

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (181223 B)
- transcripts: 1 (181223 B), not archived
- repo/: present, not archived

`base`: `b3adce1`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.13s
```

`stderr.log`: empty

### B-integrate-3

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (199288 B)
- transcripts: 1 (199288 B), not archived
- repo/: present, not archived

`base`: `8911c4d`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.12s
```

`stderr.log`: empty

### B-migrate-1

- files: base (8 B), baseline/features/keep-items.feature (1500 B), baseline/passed (321 B), baseline/summary (18 B), baseline/tags (46 B), case (8 B), fixture.log (18 B), prompt.txt (470 B), stderr.log (0 B), transcript.jsonl (81386 B)
- transcripts: 1 (81386 B), not archived
- repo/: present, not archived

`base`: `f8a590c`

`baseline/features/keep-items.feature`:

```text
# formulated from spec/capabilities/keep-items.md
@shelf
Feature: Keep items
  Narrator: a reader

  @slice-1
  Scenario Outline: A book added is held under an id made from its title
    The id follows the title.
    Given an empty shelf
    When the reader adds the book "<title>"
    Then the shelf holds the book as "<id>"

    Examples:
      | title        | id                |
      | Dune Messiah | book/dune-messiah |
      | Dune         | book/dune         |

  @slice-1
  Scenario: A book whose title is already held is refused as a duplicate
    One book a title.
    Given a shelf holding the book "Dune"
    When the reader tries to add the book "Dune"
    Then the add is refused because it is a duplicate

  @slice-1
  Scenario: The shelf answers with the number of books it holds
    A count of what is held.
    Given a shelf holding the book "Dune"
    When the reader asks how many books there are
    Then the shelf answers 1

  @slice-2
  Scenario: The shelf answers with the title of a book asked for by its id
    The title comes back from the id.
    Given a shelf holding the book "Dune"
    When the reader asks for the title of "book/dune"
    Then the shelf answers "Dune"

  @slice-1 @holding
  Scenario: The shelf lists the titles in the order they were added (held)
    Held for: removal
    Order of adding.
    Given a shelf holding the book "Dune"
    And a shelf holding the book "Emma"
    When the reader lists the books
    Then the shelf answers "Dune, Emma"
```

`baseline/passed`:

```text
PASSED tests/test_keep_items.py::test_added[Dune Messiah-book/dune-messiah]
PASSED tests/test_keep_items.py::test_added[Dune-book/dune]
PASSED tests/test_keep_items.py::test_count
PASSED tests/test_keep_items.py::test_duplicate
PASSED tests/test_keep_items.py::test_list
PASSED tests/test_keep_items.py::test_title_by_id
```

`baseline/summary`:

```text
6 passed in 0.10s
```

`baseline/tags`:

```text
holding 1
shelf 6
slice-1 5
slice-2 1
total 6
```

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.11s
```

`stderr.log`: empty

### B-migrate-2

- files: base (8 B), baseline-ids/features/keep-items.feature (1500 B), baseline-ids/pytest.txt (581 B), baseline-ids/tags.txt (46 B), case (8 B), fixture.log (18 B), prompt.txt (470 B), stderr.log (0 B), transcript.jsonl (84947 B)
- transcripts: 1 (84947 B), not archived
- repo/: present, not archived

`base`: `603c104`

`baseline-ids/features/keep-items.feature`:

```text
# formulated from spec/capabilities/keep-items.md
@shelf
Feature: Keep items
  Narrator: a reader

  @slice-1
  Scenario Outline: A book added is held under an id made from its title
    The id follows the title.
    Given an empty shelf
    When the reader adds the book "<title>"
    Then the shelf holds the book as "<id>"

    Examples:
      | title        | id                |
      | Dune Messiah | book/dune-messiah |
      | Dune         | book/dune         |

  @slice-1
  Scenario: A book whose title is already held is refused as a duplicate
    One book a title.
    Given a shelf holding the book "Dune"
    When the reader tries to add the book "Dune"
    Then the add is refused because it is a duplicate

  @slice-1
  Scenario: The shelf answers with the number of books it holds
    A count of what is held.
    Given a shelf holding the book "Dune"
    When the reader asks how many books there are
    Then the shelf answers 1

  @slice-2
  Scenario: The shelf answers with the title of a book asked for by its id
    The title comes back from the id.
    Given a shelf holding the book "Dune"
    When the reader asks for the title of "book/dune"
    Then the shelf answers "Dune"

  @slice-1 @holding
  Scenario: The shelf lists the titles in the order they were added (held)
    Held for: removal
    Order of adding.
    Given a shelf holding the book "Dune"
    And a shelf holding the book "Emma"
    When the reader lists the books
    Then the shelf answers "Dune, Emma"
```

`baseline-ids/pytest.txt`:

```text
......                                                                   [100%]
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED tests/test_keep_items.py::test_added[Dune Messiah-book/dune-messiah]
PASSED tests/test_keep_items.py::test_added[Dune-book/dune]
PASSED tests/test_keep_items.py::test_duplicate
PASSED tests/test_keep_items.py::test_count
PASSED tests/test_keep_items.py::test_title_by_id
PASSED tests/test_keep_items.py::test_list
6 passed in 0.10s
```

`baseline-ids/tags.txt`:

```text
holding 1
shelf 6
slice-1 5
slice-2 1
total 6
```

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

`stderr.log`: empty

### B-migrate-3

- files: base (8 B), case (8 B), fixture.log (18 B), prompt.txt (470 B), stderr.log (0 B), transcript.jsonl (71152 B)
- transcripts: 1 (71152 B), not archived
- repo/: present, not archived

`base`: `6e6c5b3`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.09s
```

`stderr.log`: empty

### B-noclingo-1

- files: base (8 B), case (9 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (259594 B)
- transcripts: 1 (259594 B), not archived
- repo/: present, not archived

`base`: `1db495c`

`case`: `noclingo`

`fixture.log`:

```text
4 passed in 0.11s
```

`stderr.log`: empty

### B-noclingo-2

- files: base (8 B), case (9 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (231488 B)
- transcripts: 1 (231488 B), not archived
- repo/: present, not archived

`base`: `1891b38`

`case`: `noclingo`

`fixture.log`:

```text
4 passed in 0.10s
```

`stderr.log`: empty

### B-noclingo-3

- files: base (8 B), case (9 B), fixture.log (18 B), prompt.txt (564 B), stderr.log (0 B), transcript.jsonl (251727 B)
- transcripts: 1 (251727 B), not archived
- repo/: present, not archived

`base`: `e6856f7`

`case`: `noclingo`

`fixture.log`:

```text
4 passed in 0.09s
```

`stderr.log`: empty

## T: 0.19.0 type-first ids reruns (plugin B at 1a7b92a) (2026-10-17)

**prompt.txt** (byte-identical in T-integrate-1, T-integrate-2, T-integrate-3):

```text
The brainstorming note docs/superpowers/specs/2026-10-02-lending-design.md is approved. Use shopsystem-bdd:integrating-a-proposal to integrate it into spec/. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop at the gate: show me the added, changed and removed Behaviour lines and the questions, and end your turn there. I will answer in my next message. Apply nothing to spec/ before I answer, and ask me nothing else before the gate.
```

**prompt.txt** (byte-identical in T-migrate-1, T-migrate-2, T-migrate-3):

```text
This repository is on capability files, but its Behaviour lines carry no [r<n>] ids. Use shopsystem-bdd:migrating-to-capabilities to add them. The context path is missingmass.io/demo/shelf: the owner's domain missingmass.io, the product demo, the context shelf; that is my answer for the gate's context path. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop when it is committed. I am away, so ask me nothing and wait for nothing.
```

### T-integrate-1

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (210363 B)
- transcripts: 1 (210363 B), not archived
- repo/: present, not archived

`base`: `517e9c1`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.12s
```

`stderr.log`: empty

### T-integrate-2

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (205868 B)
- transcripts: 1 (205868 B), not archived
- repo/: present, not archived

`base`: `77785e2`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.58s
```

`stderr.log`: empty

### T-integrate-3

- files: base (8 B), case (10 B), fixture.log (18 B), prompt.txt (477 B), stderr.log (0 B), transcript.jsonl (187186 B)
- transcripts: 1 (187186 B), not archived
- repo/: present, not archived

`base`: `f3a447e`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.14s
```

`stderr.log`: empty

### T-migrate-1

- files: base (8 B), baseline/features/keep-items.feature (1500 B), baseline/passed.txt (321 B), baseline/summary.txt (18 B), baseline/tags.txt (46 B), case (8 B), fixture.log (18 B), prompt.txt (474 B), stderr.log (0 B), transcript.jsonl (92101 B)
- transcripts: 1 (92101 B), not archived
- repo/: present, not archived

`base`: `6d9e8b7`

`baseline/features/keep-items.feature`:

```text
# formulated from spec/capabilities/keep-items.md
@shelf
Feature: Keep items
  Narrator: a reader

  @slice-1
  Scenario Outline: A book added is held under an id made from its title
    The id follows the title.
    Given an empty shelf
    When the reader adds the book "<title>"
    Then the shelf holds the book as "<id>"

    Examples:
      | title        | id                |
      | Dune Messiah | book/dune-messiah |
      | Dune         | book/dune         |

  @slice-1
  Scenario: A book whose title is already held is refused as a duplicate
    One book a title.
    Given a shelf holding the book "Dune"
    When the reader tries to add the book "Dune"
    Then the add is refused because it is a duplicate

  @slice-1
  Scenario: The shelf answers with the number of books it holds
    A count of what is held.
    Given a shelf holding the book "Dune"
    When the reader asks how many books there are
    Then the shelf answers 1

  @slice-2
  Scenario: The shelf answers with the title of a book asked for by its id
    The title comes back from the id.
    Given a shelf holding the book "Dune"
    When the reader asks for the title of "book/dune"
    Then the shelf answers "Dune"

  @slice-1 @holding
  Scenario: The shelf lists the titles in the order they were added (held)
    Held for: removal
    Order of adding.
    Given a shelf holding the book "Dune"
    And a shelf holding the book "Emma"
    When the reader lists the books
    Then the shelf answers "Dune, Emma"
```

`baseline/passed.txt`:

```text
PASSED tests/test_keep_items.py::test_added[Dune Messiah-book/dune-messiah]
PASSED tests/test_keep_items.py::test_added[Dune-book/dune]
PASSED tests/test_keep_items.py::test_duplicate
PASSED tests/test_keep_items.py::test_count
PASSED tests/test_keep_items.py::test_title_by_id
PASSED tests/test_keep_items.py::test_list
```

`baseline/summary.txt`:

```text
6 passed in 0.13s
```

`baseline/tags.txt`:

```text
holding 1
shelf 6
slice-1 5
slice-2 1
total 6
```

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.58s
```

`stderr.log`: empty

### T-migrate-2

- files: base (8 B), case (8 B), fixture.log (18 B), prompt.txt (474 B), stderr.log (0 B), transcript.jsonl (79203 B)
- transcripts: 1 (79203 B), not archived
- repo/: present, not archived

`base`: `4bfbf14`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

`stderr.log`: empty

### T-migrate-3

- files: base (8 B), case (8 B), fixture.log (18 B), prompt.txt (474 B), stderr.log (0 B), transcript.jsonl (92572 B)
- transcripts: 1 (92572 B), not archived
- repo/: present, not archived

`base`: `f8eff82`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.13s
```

`stderr.log`: empty

## U: 0.20.0 consistency checking (plugin B at 73ee3fb) (2026-10-17)

**prompt.txt** (byte-identical in U-consistency-fix-1, U-consistency-fix-2, U-consistency-fix-3):

```text
Use shopsystem-bdd:checking-spec-consistency in fix mode on this repository's spec. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. My answers, given now because I am away: if you propose a term for book and volume, I approve it, with volume as an avoided word under book. Where the count scenario's wording differs from its line, the line is right. For the line about a friend who has too many books, the reading is more than 3 books. Defer anything else to the backlog. Stop when it is committed. Ask me nothing and wait for nothing.
```

**prompt.txt** (byte-identical in U-consistency-report-1, U-consistency-report-2, U-consistency-report-3):

```text
Use shopsystem-bdd:checking-spec-consistency in report mode on this repository's spec. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/B/scripts. Stop when the findings are written. I am away, so ask me nothing and wait for nothing.
```

### U-consistency-fix-1

- files: base (8 B), case (16 B), fixture.log (18 B), prompt.txt (575 B), stderr.log (0 B), transcript.jsonl (285933 B)
- transcripts: 1 (285933 B), not archived
- repo/: present, not archived

`base`: `7f8e7f5`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.12s
```

`stderr.log`: empty

### U-consistency-fix-2

- files: base (8 B), case (16 B), fixture.log (18 B), prompt.txt (575 B), stderr.log (0 B), transcript.jsonl (261741 B)
- transcripts: 1 (261741 B), not archived
- repo/: present, not archived

`base`: `8792324`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.11s
```

`stderr.log`: empty

### U-consistency-fix-3

- files: base (8 B), case (16 B), fixture.log (18 B), prompt.txt (575 B), stderr.log (0 B), transcript.jsonl (304105 B)
- transcripts: 1 (304105 B), not archived
- repo/: present, not archived

`base`: `f475198`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.12s
```

`stderr.log`: empty

### U-consistency-report-1

- files: base (8 B), case (19 B), fixture.log (18 B), prompt.txt (261 B), stderr.log (0 B), transcript.jsonl (160348 B)
- transcripts: 1 (160348 B), not archived
- repo/: present, not archived

`base`: `f8c6a31`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.12s
```

`stderr.log`: empty

### U-consistency-report-2

- files: base (8 B), case (19 B), fixture.log (18 B), prompt.txt (261 B), stderr.log (0 B), transcript.jsonl (162954 B)
- transcripts: 1 (162954 B), not archived
- repo/: present, not archived

`base`: `67640e2`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.12s
```

`stderr.log`: empty

### U-consistency-report-3

- files: base (8 B), case (19 B), fixture.log (18 B), prompt.txt (261 B), stderr.log (0 B), transcript.jsonl (163420 B)
- transcripts: 1 (163420 B), not archived
- repo/: present, not archived

`base`: `43b3db0`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.11s
```

`stderr.log`: empty

## test-*: the harness self-test's hand-made fixtures, no model (2026-10-17)

### test-done-apply

- files: base (8 B), case (6 B), fixture.log (18 B), transcript.jsonl (1204 B)
- transcripts: 1 (1204 B), not archived
- repo/: present, not archived

`base`: `9718c85`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-done-consistency-fix

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-done-consistency-report

- files: base (8 B), case (19 B), fixture.log (18 B), transcript.jsonl (1165 B)
- transcripts: 1 (1165 B), not archived
- repo/: present, not archived

`base`: `c480ac3`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-done-formulate

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (1036 B)
- transcripts: 1 (1036 B), not archived
- repo/: present, not archived

`base`: `8120ac0`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-done-integrate

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (5323 B)
- transcripts: 1 (5323 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-done-migrate

- files: base (8 B), case (8 B), fixture.log (18 B), transcript.jsonl (1003 B)
- transcripts: 1 (1003 B), not archived
- repo/: present, not archived

`base`: `ae6eea8`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

### test-done-noclingo

- files: base (8 B), case (9 B), fixture.log (18 B), transcript.jsonl (1003 B)
- transcripts: 1 (1003 B), not archived
- repo/: present, not archived

`base`: `433f391`

`case`: `noclingo`

`fixture.log`:

```text
4 passed in 0.09s
```

### test-fresh-apply

- files: base (8 B), case (6 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `59d36f9`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-fresh-consistency-fix

- files: base (8 B), case (16 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `9d73996`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.11s
```

### test-fresh-consistency-report

- files: base (8 B), case (19 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `9d73996`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-fresh-formulate

- files: base (8 B), case (10 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `2ee6d8f`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.09s
```

### test-fresh-integrate

- files: base (8 B), case (10 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `ff46fc3`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-fresh-migrate

- files: base (8 B), case (8 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `b08d402`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

### test-fresh-noclingo

- files: base (8 B), case (9 B), fixture.log (18 B)
- transcripts: none
- repo/: present, not archived

`base`: `ecd25e8`

`case`: `noclingo`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-mut-apply-line-kept

- files: base (8 B), case (6 B), fixture.log (18 B), transcript.jsonl (1204 B)
- transcripts: 1 (1204 B), not archived
- repo/: present, not archived

`base`: `9718c85`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-mut-apply-message

- files: base (8 B), case (6 B), fixture.log (18 B), transcript.jsonl (1204 B)
- transcripts: 1 (1204 B), not archived
- repo/: present, not archived

`base`: `9718c85`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-mut-apply-no-removes

- files: base (8 B), case (6 B), fixture.log (18 B), transcript.jsonl (1204 B)
- transcripts: 1 (1204 B), not archived
- repo/: present, not archived

`base`: `9718c85`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-mut-apply-not-retired

- files: base (8 B), case (6 B), fixture.log (18 B), transcript.jsonl (1204 B)
- transcripts: 1 (1204 B), not archived
- repo/: present, not archived

`base`: `9718c85`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-mut-apply-restored

- files: base (8 B), case (6 B), fixture.log (18 B), transcript.jsonl (1403 B)
- transcripts: 1 (1403 B), not archived
- repo/: present, not archived

`base`: `9718c85`

`case`: `apply`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-mut-consistency-fix-drift-kept

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-glossary

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-message

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-reading

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-renumbered

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-suite-red

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-unresolved

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-fix-volume-left

- files: base (8 B), case (16 B), fixture.log (18 B), transcript.jsonl (1120 B)
- transcripts: 1 (1120 B), not archived
- repo/: present, not archived

`base`: `a67dbc1`

`case`: `consistency-fix`

`fixture.log`:

```text
2 passed in 0.09s
```

### test-mut-consistency-report-committed

- files: base (8 B), case (19 B), fixture.log (18 B), transcript.jsonl (1165 B)
- transcripts: 1 (1165 B), not archived
- repo/: present, not archived

`base`: `c480ac3`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-mut-consistency-report-no-a

- files: base (8 B), case (19 B), fixture.log (18 B), transcript.jsonl (1165 B)
- transcripts: 1 (1165 B), not archived
- repo/: present, not archived

`base`: `c480ac3`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-mut-consistency-report-no-b

- files: base (8 B), case (19 B), fixture.log (18 B), transcript.jsonl (1165 B)
- transcripts: 1 (1165 B), not archived
- repo/: present, not archived

`base`: `c480ac3`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-mut-consistency-report-no-c

- files: base (8 B), case (19 B), fixture.log (18 B), transcript.jsonl (1165 B)
- transcripts: 1 (1165 B), not archived
- repo/: present, not archived

`base`: `c480ac3`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-mut-consistency-report-spec-edited

- files: base (8 B), case (19 B), fixture.log (18 B), transcript.jsonl (1165 B)
- transcripts: 1 (1165 B), not archived
- repo/: present, not archived

`base`: `c480ac3`

`case`: `consistency-report`

`fixture.log`:

```text
2 passed in 0.10s
```

### test-mut-formulate-lend-v_s3

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (1036 B)
- transcripts: 1 (1036 B), not archived
- repo/: present, not archived

`base`: `8120ac0`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-mut-formulate-r4-left

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (955 B)
- transcripts: 1 (955 B), not archived
- repo/: present, not archived

`base`: `455878c`

`case`: `formulate`

`fixture.log`:

```text
4 passed in 0.11s
```

### test-mut-integrate-no-removal

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (5083 B)
- transcripts: 1 (5083 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-mut-integrate-renumbered

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (5323 B)
- transcripts: 1 (5323 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-mut-integrate-wasnow-r8

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (14296 B)
- transcripts: 1 (14296 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-mut-migrate-index

- files: base (8 B), case (8 B), fixture.log (18 B), transcript.jsonl (1003 B)
- transcripts: 1 (1003 B), not archived
- repo/: present, not archived

`base`: `ae6eea8`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

### test-mut-migrate-old-decision

- files: base (8 B), case (8 B), fixture.log (18 B), transcript.jsonl (1003 B)
- transcripts: 1 (1003 B), not archived
- repo/: present, not archived

`base`: `ae6eea8`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

### test-mut-migrate-two-commits

- files: base (8 B), case (8 B), fixture.log (18 B), transcript.jsonl (1003 B)
- transcripts: 1 (1003 B), not archived
- repo/: present, not archived

`base`: `ae6eea8`

`case`: `migrate`

`fixture.log`:

```text
6 passed in 0.10s
```

### test-mut-noclingo-unformulated

- files: base (8 B), case (9 B), fixture.log (18 B), transcript.jsonl (1003 B)
- transcripts: 1 (1003 B), not archived
- repo/: present, not archived

`base`: `433f391`

`case`: `noclingo`

`fixture.log`:

```text
4 passed in 0.09s
```

### test-ok-integrate-bold-label

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (17473 B)
- transcripts: 1 (17473 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-ok-integrate-forms

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (5473 B)
- transcripts: 1 (5473 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-ok-integrate-labels

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (14305 B)
- transcripts: 1 (14305 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-ok-integrate-late-message

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (11113 B)
- transcripts: 1 (11113 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

### test-ok-integrate-wasnow

- files: base (8 B), case (10 B), fixture.log (18 B), transcript.jsonl (14296 B)
- transcripts: 1 (14296 B), not archived
- repo/: present, not archived

`base`: `d955db8`

`case`: `integrate`

`fixture.log`:

```text
4 passed in 0.10s
```

## deliver-real shakedowns, work run started directly (2026-10-20)

### shake-1

- files: base (41 B), case (28 B), fixture.log (346 B), score.txt (3479 B), seconds (4 B), work-run.out (654 B)
- transcripts: none
- repo/: present, not archived

`base`: `c55ff9b4f6e29efe465e6f4495c004536bd37885`

`case`: `deliver-real direct f9da946`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.11s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    awaiting-ruling: - When two adds give the same id (the same title added twice, or 'Dune' then 'Dune!', which both become book/dune), how many books does the shelf hold? Reading A, a book is an id: after adding 'Dune' twice, or 'Dune' and 'Dune!', the reader asks how many books there are and the shelf answers 1. Only
PASS green-runs n/a (not green)
PASS log        stages ['research', 'plan']
PASS work-files only work run's commits
PASS no-read    n/a (work run started directly, no session)
     worker 1-research     $0.02766799 125s 42 turns; success; models claude-haiku-5-5; denials 8 ['echo "--- status" && git status --porcelain && echo "--- work item" && cat .shop/work/i1/keep-items-1.md && echo "--- capability" && cat spec/capabilities/keep-items.md && echo "--- run dir" && ls -la .shop/scratch/1-research/ && echo "--- tree" && git ls-files | head -100 && echo "--- tools" && ls /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/ && python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools --help', 'echo "--- tree"; cd /home/vscode/scratch/shopsystem-bdd/ids/runs/shake-1/repo/.shop/worktrees/keep-items-1-1-research && git ls-files; echo "--- tools"; ls /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/; python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools --help', 'for f in features/keep-items.feature shelf/__init__.py shelf/shelf.py tests/test_keep_items.py tests/test_shelf.py conftest.py pytest.ini spec/decisions/0001-books-in-memory.md spec/index.md .shop/work/i1/initiative.md .shop/work/i1/listing-keep-items.md; do echo "=== $f"; cat -n "$f"; done; echo; git log --oneline -3; git rev-parse HEAD', 'mkdir -p .shop/scratch/keep-items-1-1-research && echo "--- tools probe" && python3 -I /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools probe; echo "exit $?"; echo "--- refs Shelf" && python3 -I /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools refs Shelf; echo "exit $?"; echo "--- refs Shelf.holds" && python3 -I /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools refs Shelf.holds; echo "exit $?"; echo "--- refs Shelf.add" && python3 -I /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools refs Shelf.add; echo "exit $?"; echo "--- tests-of (no map expected)" && python3 -I /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/tools tests-of shelf/shelf.py:Shelf.add --by-file; echo "exit $?"; echo "--- pytest r2 by name" && PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider -k "The shelf answers with the number of books it holds" 2>&1 | tail -60; echo "--- pytest work-item" && PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider --work-item keep-items-1 2>&1 | tail -40; echo "--- pytest r1 by name" && PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider -k "A book added is held under an id made from its title" 2>&1 | tail -15', 'mkdir -p .shop/scratch/keep-items-1-1-research/copy && cp -r shelf tests features conftest.py pytest.ini .shop/scratch/keep-items-1-1-research/copy/ && ls -R .shop/scratch/keep-items-1-1-research/copy | head -30', 'cp -r shelf tests features conftest.py pytest.ini .shop/scratch/keep-items-1-1-research/copy/ && ls .shop/scratch/keep-items-1-1-research/copy']
     worker 2-plan         $0.23995840000000002 51s 12 turns; success; models claude-opus-5-5; denials 0 []
     cost: session $None + workers $0.27 = $0.27
shake-1: PASS
```

`seconds`: `178`

`work-run.out`:

```text
keep-items-1 awaiting-ruling
  - When two adds give the same id (the same title added twice, or 'Dune' then 'Dune!', which both become book/dune), how many books does the shelf hold? Reading A, a book is an id: after adding 'Dune' twice, or 'Dune' and 'Dune!', the reader asks how many books there are and the shelf answers 1. Only the last title stays stored under book/dune, as today. Reading B, each add is a book: in both cases the shelf answers 2. The shelf keeps every add in the order it was added, and holds('book/dune') is still true. keep-items#r1, keep-items#r2 and design-decision/books-in-memory do not choose between these readings.
exit 3
```

### shake-2

- files: base (41 B), case (28 B), fixture.log (346 B), score.txt (976 B), seconds (3 B), work-run.out (208 B)
- transcripts: none
- repo/: present, not archived

`base`: `334d00a07a3a6a3ad58d72e676678d07ca879242`

`case`: `deliver-real direct f9da946`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.11s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    awaiting-ruling: - code-scout gave no result file (/home/vscode/scratch/shopsystem-bdd/ids/runs/shake-2/repo/.shop/worktrees/keep-items-1-1-research/.shop/scratch/1-research/result.json)
PASS green-runs n/a (not green)
PASS log        stages ['research']
PASS work-files only work run's commits
PASS no-read    n/a (work run started directly, no session)
     worker 1-research     $0.02019929 94s 29 turns; success; models claude-haiku-5-5; denials 8 ['echo "--- status" && git status --porcelain && echo "--- work-item" &&', 'export PYTHONDONTWRITEBYTECODE=1; echo "--- r2 scenario"; python3 -m p', 'PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider -W ', 'mkdir -p /home/vscode/scratch/shopsystem-bdd/ids/runs/shake-2/repo/.sh', 'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/vscode/scratch/shopsystem-b', 'git grep -n -E "holding|asks how many|answers|reader asks" -- tests sh']
     cost: session $None + workers $0.02 = $0.02
shake-2: PASS
```

`seconds`: `95`

`work-run.out`:

```text
keep-items-1 awaiting-ruling
  - code-scout gave no result file (/home/vscode/scratch/shopsystem-bdd/ids/runs/shake-2/repo/.shop/worktrees/keep-items-1-1-research/.shop/scratch/1-research/result.json)
exit 3
```

## deliver-real sessions g1, r1, s1, v1-v3, x1 (2026-10-20)

**prompt.txt** (byte-identical in r1, g1, s1, v1, v2, v3, x1):

```text
Deliver the initiative i1. Use shopsystem-bdd:delivering-an-initiative. The plugin's scripts are at /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts. I am away, so ask me nothing and wait for nothing but work run; end your turn when you have shown what it printed.
```

### r1

- files: base (41 B), case (29 B), fixture.log (346 B), prompt.txt (274 B), score.txt (748 B), seconds (3 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (55594 B)
- transcripts: 1 (55594 B), not archived
- repo/: present, not archived

`base`: `da4544ef18eeffda59b69b4f4029582c5c9da77c`

`case`: `deliver-real session 3062e1e`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.11s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    awaiting-ruling: - code-scout gave no result file (/home/vscode/scratch/shopsystem-bdd/ids/runs/r1/repo/.shop/worktrees/keep-items-1-1-research/.shop/scratch/1-research/result.json)
PASS green-runs n/a (not green)
PASS log        stages ['research']
PASS work-files only work run's commits
PASS no-read    work run started; after it: none; source before: none; calls after start: ['Bash {"command": "python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/w', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-r1-']
     worker 1-research     $0.017149209999999998 81s 32 turns; success; models claude-haiku-5-5; denials 0 []
     cost: session $0.1119647 + workers $0.02 = $0.13
r1: PASS
```

`seconds`: `96`

`session-exit`: `exit 0`

`stderr.log`: empty

### g1

- files: base (41 B), case (29 B), fixture.log (346 B), prompt.txt (274 B), score.txt (758 B), seconds (3 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (54347 B)
- transcripts: 1 (54347 B), not archived
- repo/: present, not archived

`base`: `8473b9659987c3dd1c7ccb54ba42fdf04f38ecdc`

`case`: `deliver-real session 3ab836c`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.12s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    awaiting-ruling: - code-scout gave no result file (/home/vscode/scratch/shopsystem-bdd/ids/runs/g1/repo/.shop/worktrees/keep-items-1-1-research/.shop/scratch/1-research/result.json)
PASS green-runs n/a (not green)
PASS log        stages ['research']
PASS work-files only work run's commits
PASS no-read    work run started; after it: none; source before: none; calls after start: ['Bash {"command": "python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/w', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-g1-']
     worker 1-research     $0.012957469999999999 59s 31 turns; success; models claude-haiku-5-5; denials 0 []
     cost: session $0.11670640000000002 + workers $0.01 = $0.13
g1: PASS
```

`seconds`: `73`

`session-exit`: `exit 0`

`stderr.log`: empty

### s1

- files: base (41 B), case (29 B), fixture.log (346 B), prompt.txt (274 B), score.txt (1127 B), seconds (4 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (56006 B)
- transcripts: 1 (56006 B), not archived
- repo/: present, not archived

`base`: `3395613d553873684ad54349c4368dba05755a9e`

`case`: `deliver-real session 54bee73`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.11s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    awaiting-ruling: - Re-run with shopsystem-bdd:bdd-red-green loaded into the agent's context. A Skill tool call returned 'No such tool available'.
PASS green-runs n/a (not green)
PASS log        stages ['research', 'plan', 'implement']
PASS work-files only work run's commits
FAIL no-read    work run started; after it: ['Bash {"command": "cd /home/vscode/scratch/shopsystem-bdd/ids/runs/s1/repo && python3 /home/vscode/scratch/shopsystem-bdd/ids/']; source before: none; calls after start: ['Bash {"command": "cd /home/vscode/scratch/shopsystem-bdd/ids/runs/s1/repo && python3 ', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-s1-']
     worker 1-research     $0.01579531 73s 33 turns; success; models claude-haiku-5-5; denials 0 []
     worker 2-plan         $0.1865578 44s 12 turns; success; models claude-opus-5-5; denials 0 []
     worker 3-implement    $0.0640992 10s 6 turns; success; models claude-sonnet-5-5; denials 1 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/s1/repo/.shop/worktree']
     cost: session $0.11707409999999999 + workers $0.27 = $0.38
s1: FAIL
```

`seconds`: `141`

`session-exit`: `exit 0`

`stderr.log`: empty

### v1

- files: base (41 B), case (29 B), fixture.log (346 B), prompt.txt (274 B), score.txt (1383 B), seconds (4 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (51553 B)
- transcripts: 1 (51553 B), not archived
- repo/: present, not archived

`base`: `7d6311fbd6358f80cc7a8dfc4a4326328b289dab`

`case`: `deliver-real session 3ab836c`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.12s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    green
PASS green-runs work-item: 1 passed, 3 deselected, 4 warnings in 0.11s; suite: 4 passed, 6 warnings in 0.11s; features changed: none
PASS log        stages ['research', 'plan', 'implement', 'review']
PASS work-files only work run's commits
PASS no-read    work run started; after it: none; source before: none; calls after start: ['Bash {"command": "python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/w', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-v1-']
     worker 1-research     $0.01809237 84s 33 turns; success; models claude-haiku-5-5; denials 1 ['Write']
     worker 2-plan         $0.1802794 36s 12 turns; success; models claude-opus-5-5; denials 0 []
     worker 3-implement    $0.15585720000000003 20s 11 turns; success; models claude-sonnet-5-5; denials 2 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v1/repo/.shop/worktree', 'cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v1/repo/.shop/worktree']
     worker 4-review       $0.28849299999999994 44s 14 turns; success; models claude-opus-5-5; denials 3 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v1/repo/.shop/worktree', 'cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v1/repo/.shop/worktree', 'W=/home/vscode/scratch/shopsystem-bdd/ids/runs/v1/repo/.shop/worktrees']
     cost: session $0.1106579 + workers $0.64 = $0.75
v1: PASS
```

`seconds`: `200`

`session-exit`: `exit 0`

`stderr.log`: empty

### v2

- files: base (41 B), case (29 B), fixture.log (346 B), prompt.txt (274 B), score.txt (1305 B), seconds (4 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (54241 B)
- transcripts: 1 (54241 B), not archived
- repo/: present, not archived

`base`: `68562323fb1b9f90e9e7dd57eff568c9c27f060d`

`case`: `deliver-real session 3ab836c`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.11s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.11s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    green
PASS green-runs work-item: 1 passed, 3 deselected, 4 warnings in 0.11s; suite: 4 passed, 6 warnings in 0.11s; features changed: none
PASS log        stages ['research', 'plan', 'implement', 'review']
PASS work-files only work run's commits
PASS no-read    work run started; after it: none; source before: none; calls after start: ['Bash {"command": "python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/w', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-v2-']
     worker 1-research     $0.01473456 65s 29 turns; success; models claude-haiku-5-5; denials 0 []
     worker 2-plan         $0.18864740000000002 35s 12 turns; success; models claude-opus-5-5; denials 0 []
     worker 3-implement    $0.1438237 24s 13 turns; success; models claude-sonnet-5-5; denials 3 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v2/repo/.shop/worktree', 'cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v2/repo/.shop/worktree', "cat >> .shop/scratch/3-implement/report.md <<'EOF'\n\n## Changed\n`Shelf."]
     worker 4-review       $0.2402564 40s 10 turns; success; models claude-opus-5-5; denials 1 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v2/repo/.shop/worktree']
     cost: session $0.11554100000000002 + workers $0.59 = $0.70
v2: PASS
```

`seconds`: `182`

`session-exit`: `exit 0`

`stderr.log`: empty

### v3

- files: base (41 B), case (29 B), fixture.log (346 B), prompt.txt (274 B), score.txt (1298 B), seconds (4 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (53616 B)
- transcripts: 1 (53616 B), not archived
- repo/: present, not archived

`base`: `1fcc32ae78fae2bb7e278d56f764fda91c82067f`

`case`: `deliver-real session 3ab836c`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.09s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.08s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`score.txt`:

```text
PASS outcome    green
PASS green-runs work-item: 1 passed, 3 deselected, 4 warnings in 0.12s; suite: 4 passed, 6 warnings in 0.11s; features changed: none
PASS log        stages ['research', 'plan', 'implement', 'review']
PASS work-files only work run's commits
PASS no-read    work run started; after it: none; source before: none; calls after start: ['Bash {"command": "python3 /home/vscode/scratch/shopsystem-bdd/ids/plugins/D/scripts/w', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-v3-']
     worker 1-research     $0.0143932 70s 30 turns; success; models claude-haiku-5-5; denials 1 ['Write']
     worker 2-plan         $0.1660042 29s 12 turns; success; models claude-opus-5-5; denials 0 []
     worker 3-implement    $0.1342815 22s 12 turns; success; models claude-sonnet-5-5; denials 2 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v3/repo/.shop/worktree', 'cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v3/repo/.shop/worktree']
     worker 4-review       $0.2164026 36s 10 turns; success; models claude-opus-5-5; denials 2 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/v3/repo/.shop/worktree', 'C=$(git log --format=%H -1 --grep="^work: keep-items-1 ready -> claime']
     cost: session $0.11427910000000001 + workers $0.53 = $0.65
v3: PASS
```

`seconds`: `174`

`session-exit`: `exit 0`

`stderr.log`: empty

### x1

- files: base (41 B), case (29 B), fixture.log (131 B), prompt.txt (274 B), score.txt (1311 B), seconds (4 B), session-exit (7 B), stderr.log (0 B), transcript.jsonl (55477 B)
- transcripts: 1 (55477 B), not archived
- repo/: present, not archived

`base`: `cc78bc09e76c31fbfcc2bccb340c76aebc284335`

`case`: `deliver-real session df78fe7`

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.11s
cc78bc0 shelf: keep-items r1; initiative i1 with its formulated proposal
```

`score.txt`:

```text
PASS outcome    green
PASS green-runs work-item: 1 passed, 3 deselected, 4 warnings in 0.11s; suite: 4 passed, 6 warnings in 0.11s; features changed: none
PASS log        stages ['research', 'plan', 'implement', 'review']
PASS work-files only work run's commits
PASS no-read    work run started; after it: none; source before: none; calls after start: ['Bash {"command": "cd /home/vscode/scratch/shopsystem-bdd/ids/runs/x1/repo; python3 /h', 'Read {"file_path": "/tmp/claude-1000/-home-vscode-scratch-shopsystem-bdd-ids-runs-x1-']
     worker 1-research     $0.01539717 69s 32 turns; success; models claude-haiku-5-5; denials 1 ['Write']
     worker 2-plan         $0.1954218 44s 12 turns; success; models claude-opus-5-5; denials 0 []
     worker 3-implement    $0.1497673 26s 14 turns; success; models claude-sonnet-5-5; denials 3 ['cd /home/vscode/scratch/shopsystem-bdd/ids/runs/x1/repo/.shop/worktree', 'cd /home/vscode/scratch/shopsystem-bdd/ids/runs/x1/repo/.shop/worktree', "cat >> .shop/scratch/3-implement/report.md <<'EOF'\n\n## Changed\nAdded `"]
     worker 4-review       $0.22638200000000003 38s 9 turns; success; models claude-opus-5-5; denials 1 ['R=.shop/work/i1/runs/keep-items-1; cat $R/1-research/notes.md $R/2-pla']
     cost: session $0.12283200000000002 + workers $0.59 = $0.71
x1: PASS
```

`seconds`: `199`

`session-exit`: `exit 0`

`stderr.log`: empty

## ro-*: research-only tool-list experiment, d = default tool list, n = no bare Write (2026-10-20)

### ro-d1

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.13s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty

### ro-d2

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.14s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty

### ro-d3

- files: fixture.log (346 B), work-run.out (199 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.13s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`:

```text
keep-items-1 awaiting-ruling
  - code-scout gave no result file (/home/vscode/scratch/shopsystem-bdd/ids/runs/ro-d3/repo/.shop/worktrees/keep-items-1-1-research/.shop/scratch/1-research/result.json)
```

### ro-d4

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.13s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty

### ro-n1

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.14s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty

### ro-n2

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.14s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty

### ro-n3

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.14s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty

### ro-n4

- files: fixture.log (346 B), work-run.out (0 B)
- transcripts: none
- repo/: present, not archived

`fixture.log`:

```text
-m pytest -q -> 1 1 failed, 3 passed, 4 warnings in 0.14s
-m pytest -q --work-item keep-items-1 -> 1 1 failed, 3 deselected, 2 warnings in 0.10s
---
id: work-item/example.org/library/shelf/keep-items-1
kind: work-item
part_of: capability-proposal/listing-keep-items
status: drafted
under: keep-items
accepts: [keep-items#r2]
---

# keep-items-1
```

`work-run.out`: empty
