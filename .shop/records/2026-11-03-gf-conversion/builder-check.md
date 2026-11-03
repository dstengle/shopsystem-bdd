---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-builder-check
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion: a builder's check of design.md and plan.md

Read as a builder who has only `brief.md`, `design.md`, `plan.md` and the cited code. Checked against the tree at
96818f71 (branch `gf-conversion`) and the environment (Debian 13, Python 3.11.15, pip 24, pytest-xdist 3.8 present).

## Blocking contradictions

1. **The codified flag is per context, the conversion is per capability.** §13.4 makes `language: codified-1` one
   flag in `spec/index.md`; P11 sets it at the end of layer 3, but supervision stays in 0.29 form until P12 (layer 4).
   - The layer 3 gate ("`model check` on the live repo gives no v_p rows") then fails on supervision's 164 unparsed lines.
   - P9/P10/P11 accept `features generate --check <c>` (and P7 says generate refuses while uncodified) in worktrees
     where the flag is not yet set, since P11 merges last. Those checks cannot pass inside the packages.
   - Needed: a per-capability marker (e.g. `language: codified-1` in each capability's frontmatter), or the
     uncodified reader kept for unconverted capabilities in a codified context until P12.
2. **P7: "`features generate --check` exits 0" but §13.4 says generate "refuses" in an uncodified context.** A refusal
   is normally exit 1 or 2. Say which exit code.
3. **§16.2 says the guarantees capabilities have 226 requirements.** The live count is 156 (10+14+14+8+13+20+7+18+26+21+5).
   The other buckets are right (114, 147, 164), and the total of 581 is correct.
4. **§14.1 `ThenK_A` linearises as `i1 is v`, with no kind word.** Every kind's typed fun then gives the same
   pytest-bdd pattern, so dispatch by (template, kind) is impossible from the text. Either the text names the kind,
   or the handler infers it from the instance prefix. The same applies to `WhenBecomes`.
5. **P9 retires formulation's lines, and P12 writes their replacements in supervision.** P9's restates-coverage check
   for formulation then has to list them as dropped, and P12 restates them again. Spec-integration's script
   requirements "move to that script's service capability" (§6.12), but those files are owned by P10/P11 in the same
   layer. The design needs a cross-capability `Restates:` form (`formulation#r5@0.29`) and a rule for who writes a moved line.

## Questions a builder needs answered

6. What are the keys of `restated.json`? The 0.29 ids repeat across capabilities (each file starts at r1), so the key
   must be `<cap>#r<n>`. Is `Restates: r66@0.29` read as being in the group's own capability?
7. Who parses a term entry (§10.1)? P2's `spec_lexicon.read` and P3's `spec_read.capability(...).terms` are built in
   parallel, which makes two parsers of one format. Name one owner, and have the other call it.
8. Who decides `logic_only(G)`? P5 (`model_spec`) and P7 (`features_generate`) would each implement it. Put it in
   one function, e.g. `spec_tree`.
9. How does `work request` find an upstream repository on disk to load its grammar (G2, §11.3)? Today a request
   names an upstream by id.
10. What does `telingo.imain` do here? Its signature (`telingo/__init__.py:24`) takes no extra assumptions and no
    `on_core`, so the unsat cores over `on(r<n>)` need a copy of its loop. Is L1 "unsat at every horizon 0..3" or
    "at 3"? The witness's trigger at step 1 needs at least 2 steps.
11. L4: "unreachable from any initial state". With an unconstrained initial state, every pre-state is reachable at
    step 0. Which initial states count?
12. pgf literals: `CodeLit : String -> Code` matches any token, so a backticked lexicon word (`` `drafted` ``) parses
    both as the word and as a CodeLit, which gives two trees and a v_p2. The spike never parsed literals. How is the
    word preferred (a tokeniser pre-pass, or the guard dropping the CodeLit tree)?
13. How do `given` blocks hold multi-line data? Today's scenarios use docstrings and tables, and the Steps grammar
    is one line each.
14. "Its lines written or checked as codified" (brief). Who turns a person's English request into codified lines?
    No package gives the person or a session help to write them, e.g. a skill on `work request` or a hint from
    `model parse`.

## Gaps (files a package must change but does not own)

15. P8's acceptance (`grep -rn feature-formulator agents skills scripts`) cannot pass. `scripts/supervise_worker.py`,
    `skills/delivering-an-initiative/SKILL.md` and `skills/migrating-to-capabilities/SKILL.md` (P13's, layer 4) name
    it, and `tests/scripts/test_agents.py:7` lists it. P8 owns none of these.
16. P10 removes `tag/move/deprecate/retire/rebind/verify-moved`, but `scripts/features` (CLI), `features_bindings.py`
    (`cmd_rebind`), `features_report.py` (`cmd_verify`) and the tests that cover them (`test_features.py`,
    `test_features_deprecating.py`, `test_features_scenarios.py`; `test_features_edit*.py` does not exist) are unowned
    in layer 3.
17. Layer 3: `tests/scenarios/conftest.py`, the `world_*.py` shared handlers and `vocab.py` belong to P7 (layer 2) only,
    yet P8 and P9–P11 will all extend them in parallel. Name an owner per layer, or forbid changes and add per-capability
    handler modules.
18. P13 adds rule v_p0 and deletes the uncodified paths, but it does not own `scripts/model.lp`, `model_check.py` or
    `features_generate.py`.
19. P1's acceptance uses `tools probe --json`, which does not exist today (only `--log`). It is implied work, not in the Goal.
20. Owned test globs that match no file: `test_tools_env*`, `test_model_work*`, `test_model_requests*`,
    `test_model_facts*`, `test_model_parse*`, `test_model_report*` and `test_supervise_draft*`. The real tests of those
    modules (`test_model.py`, `test_model_reading.py`, `test_model_output.py`, `test_model_glossary.py`, `test_tools.py`)
    are owned by nobody, but P4/P5 will break them. `test_spec_consistency.py` and `spec_consistency_*` steps do not exist.
21. Spike: the brief says `gf/` holds the Ears and Steps grammars, but it holds the GF install. No spike `.gf` source is
    on disk, only `Ears.pgf` and `Steps.pgf`.
22. Done means: nothing runs `measure`, `tools map/tests-of/untested` or `features count/list/bindings` on the converted
    spec. Add a smoke check to the layer 4 gate.

## Acceptance checks that cannot be run as written

23. P4: `model check 2>&1 | grep -vq "kind 'design'"` always succeeds (it matches any other line). Use `! ... | grep -q`.
    `pytest tests/scripts/test_model_work*.py` errors with no such file.
24. P8: `pytest tests/scripts/test_supervise_draft*.py`: no such file unless P8 creates one.
25. P3: `grep -q 'design model v5' spec/index.md docs/design-model/README.md` passes if either file matches. Use two greps.
26. P10: `features vocab --check --tests tests/scenarios` "for these features". The command has no feature filter, and the
    unconverted features (work-queue, requests, supervision) fail it.
27. P1: "a second install downloads nothing" has no observable output. Name the line `install` prints.
28. P14's live run needs the real `claude` and its budget. It is evidence, as the plan says, not a gate.
29. Baseline "today's 23" is not re-verified here (1137 tests are collected).

## Toolchain risks

30. Verified working: the GF deb URL returns 200; the spike's deb matches the design's sha256; the ubuntu-24.04 build
    runs on Debian 13 via the spike's `gfc` wrapper (3.12.0); pgf 1.1, clingo 5.8.2 and telingo 2.1.3 wheels download
    for cp311; telingo needs `clingo>=5.6`; the interpreter is not externally managed and user site is enabled;
    `dpkg-deb` is present.
31. Remaining risks:
    - The `ar`+`zstandard` fallback needs an unpinned `zstandard` wheel (not installed).
    - GF is Linux x86_64 only by this design: no macOS or arm64 path, and pgf has no linux-aarch64 wheel.
    - `gf` is a zsh git alias, which matters only for the PATH fallback.
    - pytest-xdist workers, or parallel worktrees, compiling into one shared `~/.cache/.../pgf/<sha>` race: write to a
      temporary directory and rename.
    - The suite needs the GF binary: tests that compile must find it, or fail loudly.
    - `Typed.gf` grows as kinds×attributes×templates. Compile time and parse ambiguity (coordinated NPs, literals) are
      unmeasured.
    - Hyphenated or backticked terms (`work-item`, `` `work run` ``) need identifier mangling in `Lex`/`Typed`.
