---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-verify-r2
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Revision 2, verified by measurement

This record checks `gf-conversion` at 21341c3e, the layer 5 gate. I did not rely on `gate-r2-done.md` or the
reports. Each item below comes from a command or script I ran myself. The scripts were written to the session
scratchpad, and every seed and regeneration ran in scratch copies made with `git archive HEAD`. The tracked tree
was not changed.

## Summary

| item | holds | measured |
|---|---|---|
| no given block that is not example data | yes | 50 blocks with 83 given lines. All 83 are file, log or measurement contents. The figure was 234 at 7e0684d2 |
| no two statements in a group share their trigger and condition | yes | 405 groups and 405 statements. No group has more than one statement |
| the person's point 2 in full (repeated "… shall" combined with "and") | **partly** | 8 subjects keep 17 ubiquitous statements in separate groups, each opening the same "<actor> shall" |
| no relation entry, no `Means:`, no term entry over one sentence | yes | 0 relation entries, 0 `Means:`, 0 glosses over one sentence (by two independent sentence splits) |
| brief E: a condition's definition parsed into a rule | **no** | 13 of 128 condition glosses parse as `Def`. 115 are English prose that nothing parses. The 88 former `Means:` became these glosses |
| `model logic` uses `&tel` and telingo's incremental horizon | yes | `&tel{}` is in spec_logic and spec_solve. Both spec_engine and spec_trace call `telingo.imain(imin=0, imax=bound)`. No `HORIZON =` remains |
| a seeded conflict is found, and its core names both ids | yes | 2 seeds, each L1 with both ids. The clean spec gives `no findings` |
| `features generate` reads traces and is byte-stable | yes | Regenerated from empty with two hash seeds: identical to each other and to HEAD. After an unrelated edit, only the new scenario was added |
| P15's e2e test | yes | `1 passed in 17.36s` |
| the suite | yes | `864 passed, 1 skipped, 125 subtests passed in 369.13s` |
| the size limit | yes | `tools size --limit 300` exits 0 with no output |
| `model restates` | yes | `581 ids: 513 restated, 68 dropped, 0 pending, 0 missing` |

## 1. Given blocks (the person's point 1)

- **The fenced blocks.** A scratch script read every ```` ```given ```` fence in `spec/capabilities/*.md` and
  `spec/universal.md`, and printed each block's group and first lines. It found 50 blocks, in four capabilities:
  - analysis-tools: 5
  - batch-measurement: 9
  - feature-file-tools: 15
  - migration-tools: 21

  I read the blocks one by one. Each top-level line is `the <kind> \`<name>\` holds:` followed by a docstring, or
  `holds "<text>"`. The contents are:
  - Python files;
  - `requirements.txt`;
  - initiative logs (JSON lines);
  - measurement JSON;
  - feature files;
  - test modules;
  - capability files;
  - tracked files of the old layout.

  None of the lines restates a condition.
- **The spec reader.** `spec_read.capability()` was run over the 19 capabilities, and each `(line, block)` was
  passed to `spec_read_given.example()`. It reports 19 capabilities, 405 groups, 405 requirements and 0 reader
  problems, with 83 given lines, all 83 example data and 0 not.
- **A While clause now reaches the Givens through the translation.** The person's own example comes out as asked:
  - `features/supervision.feature` @g2 reads `Given a work-item w1 that is \`drafted\``, then
    `And the work-item w1 is not waiting`.
  - @g13 reads `Given a session s1` and `And the session s1 is faulty`, with no given block.

## 2. Statements that share a trigger and condition (the person's point 2)

- **Inside a group.** The script split each requirement at ` shall ` and compared the prefixes within each group:
  - 0 groups have more than one statement;
  - 0 groups have two statements with the same prefix;
  - 194 requirements have `and` after `shall`. This is the combined form, for example r12 "shall set the status of
    the work-item to `awaiting-answer` and ask a question on the work-item", which was r16 and r17 before.
- **Across groups in one capability.** The same prefix comparison was run between groups of the same capability.
  Eight prefixes repeat, and all of them are ubiquitous statements with no trigger and no condition:
  - code-research r2 and r5, "The researcher shall not …";
  - delivery r2 and r6;
  - planning r3 and r6;
  - red-green r2, r3 and r15, "The implementer shall not use `--whole-suite`" / "… change a feature or write a
    status" / "… push a commit or merge a work-item branch";
  - role-boundaries r3 and r5;
  - spec-consistency r4 and r9;
  - spec-migration r5, r8 and r10;
  - trials r2 and r3.

  The Done means asks only about statements within a group, and that holds. The person's wording, "the same
  sentence through the shall portion … combined into the same simple sentence with 'and'", also covers these 17,
  and they were not combined. All of them are in `guarantees` capabilities, so none of them has a scenario.

## 3. Terms (the person's point 3)

- **The lexicon's own check.** `model lexicon --check` exits 0: `366 terms, 0 problems`. The 366 are 24 actors,
  142 kinds, 38 events, 25 attributes, 128 conditions and 9 resources.
- **Measured directly.** `spec_lexicon.read('.')` gives:
  - relation entries: `[]`;
  - entries with `Means:`: `[]`;
  - glosses over one sentence: 0 by `one_sentence()`, and 0 by my own split on `.`, `;`, `!` or `?` followed by a
    capital letter or a code span.
- **The longest glosses** are 35 words (complete), 33 (suite difference, crossing) and 30 (stage).
- **Compared with 7e0684d2.** `git grep -c` counted 88 `Means:` lines, 88 condition entries and 61 relation
  entries then. At HEAD the counts are 0 `Means:`, 128 conditions and 0 relation entries.
- **Brief E is not met.** Every condition's definition was given to `spec_grammar.parse(root, text, grammar="Def")`,
  as `spec_solve.definitions` does. 13 of 128 parse, for example "A result is outputless when the result gives no
  question and the result gives no output." The other 115 are prose glosses, and `spec_solve.definitions` gives no
  rule for them. Examples:
  - `faulty`: "a session that ends in an error or at its turn limit, or leaves output that holds no JSON result."
    At 7e0684d2 this was `Means: it ends in an error or …`.
  - `bare`: "an initiative that fulfils a request and has no capability-proposal, no glossary-proposal and no
    work-item."
  - `free`: "a resource that no session holds, or a counted resource that fewer sessions hold than its number."

  The `Means:` keyword is gone, but most of what it held is now in glosses. Many of these glosses still carry logic
  (and, or, no, whose), which is what the person objected to ("long definitions which include logic"). In the logic
  these conditions are opaque atoms.
- **The relations.** An awk pass counted the `## Relations` tables: 64 rows, 25 of them a bare preposition:
  - of 6;
  - on, for, in and with 4 each;
  - outside 2;
  - under 1.

  With `Kind of:` the rows expand to 76 relations.

  Six kind pairs have two or three relations. Each word is distinct, so D's "distinct verbs" holds:
  - work-item→initiative: kept in, of;
  - commit→work-item: belongs to, of;
  - request→bounded context: asker, upstream;
  - capability-proposal→requirement: adds, removes;
  - glossary-proposal→term: adds, changes, removes;
  - term→glossary-proposal: added by, changed by, removed by.

  Whether a table of rows is an acceptable answer to point 3 is still the person's call 16 in `gate-r2-done.md`.

## 4. One translation into telingo, and conflicts (the person's point 4)

- **The code.** I grepped `scripts/` and `grammar/` for `&tel`, `imain`, horizon and `HORIZON`:
  - `&tel{}` appears in `spec_logic.py` (lines 183, 196, 226, 260) and in `spec_solve.py`'s guard (line 40);
  - `spec_engine.py:86` and `spec_trace.py:80` both call
    `telingo.imain(proxy, future, parts, …, imin=0, imax=…)`. imax is `horizon_bound(edges, start)`, the longest
    path in the cone plus 2;
  - `grep -rn 'HORIZON *=' scripts/` finds nothing;
  - L4 is a solver query (`>?`, spec_solve.py lines 9 and 230).
- **The clean spec.** `model logic` on a clean copy exits 0 with `no findings` in 156 s.
- **Seed 1, a direct contradiction.** In a copy, supervision gained
  `[g85] [r85] When \`work run\` merges a work-item branch, \`work run\` shall not delete the work-item branch.`,
  against r16, which says it shall delete it. `model logic supervision` (5 min 13 s) printed 4 L1 findings:
  - `L1 supervision#g85 (r85) cannot happen: conflicts with supervision#r16`
  - `L1 supervision#g16 (r16) cannot happen: conflicts with supervision#r85`
  - g14 (r14) and g20 (r20) conflict with r16 and r85, because both of them merge.
- **Seed 2, a value conflict under a While.** In a copy, supervision gained
  `[r85] While a work-item branch is lost, when a session ends an \`implement\` stage for a work-item, \`work run\` shall set the status of the work-item to \`ready\`.`,
  against r19, which sets it to `failed`. `model logic supervision` exits 1 in 227 s with:
  - `L1 supervision#g19 (r19) cannot happen: conflicts with supervision#r85`
  - `L1 supervision#g85 (r85) cannot happen: conflicts with supervision#r19`

## 5. Gherkin read from traces, byte-stable

- **What features_generate does.** `scripts/features_generate.py` is 112 lines. It takes each scenario from
  `spec_trace.traces(ctx, groups)` and `spec_trace.read(model, …)`, and it has no scenario rules of its own.
  `spec_trace` solves on `telingo.imain` with the minimisation of `grammar/background.lp`.
- **Three scratch copies.** Each ran `features generate`, side by side:
  - g1 deleted `features/*.feature` and ran with `PYTHONHASHSEED=1`: exit 0, 102 s;
  - g2 deleted them and ran with `PYTHONHASHSEED=2`: exit 0, 102 s;
  - g3 kept the files, added an unrelated supervision group
    `[g85] [r85] When \`work run\` merges a work-item branch, \`work run\` shall log the work-item branch.`, and ran
    with `PYTHONHASHSEED=3`: exit 0, 104 s.
- **The diffs.**
  - `diff -r` of HEAD's `features/` against g1: identical.
  - g1 against g2: identical.
  - HEAD against g3: the only change is five lines appended to `supervision.feature` (the new @g85 scenario). Every
    other byte of all 8 feature files is unchanged.
- **One small thing seen.** The new scenario's When names `the work-item branch w1`, but no Given introduces it
  first:
  `When \`work run\` merges the work-item branch w1` / `Then \`work run\` logs the work-item branch w1`.
- **Coverage.** Every service group has a scenario except supervision g80 to g83. Those are resource invariants
  ("Every stage … shall hold …"), which are logic-only by design.

## 6. A new request through the new system (P15)

- `python3 -m pytest -q -p no:randomly tests/scripts/test_e2e_codified.py` gives `1 passed in 17.36s`.
- The test runs the real GF, `features generate --check` and `model logic` (test lines 203 to 228). The logic check
  refuses the first drafts, and that is part of the test. Nothing in it is mocked except the claude sessions, which
  stub_claude stands in for.

## 7. The suite and the size limit

- `python3 -m pytest -q -p no:randomly -n auto` exits 0: `864 passed, 1 skipped, 125 subtests passed in 369.13s`.
- `python3 scripts/tools size --limit 300` exits 0 and prints nothing.
- `python3 scripts/model restates` prints `581 ids: 513 restated, 68 dropped, 0 pending, 0 missing`.

## What does not hold

1. **Brief E.** 115 condition definitions are prose glosses that are not parsed into rules. Several of them carry
   logic. To close it, write each one as a `Def` sentence, make it an attribute value, or shorten it to a gloss with
   no logic, and add a check that every condition gloss containing and, or, no or whose parses as a `Def`.
2. **Point 2 across groups.** 17 ubiquitous statements in 8 sets repeat their "<actor> shall". They could each be
   merged into one statement with "and", for example red-green "The implementer shall not use `--whole-suite`,
   change a feature, write a status, push a commit or merge a work-item branch". Merging them loses one group title
   per statement, so it is a judgement for the next pass.
3. **Call 16 (still open).** The 25 rows that are a bare preposition stay for the person to decide on.
