---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: a session reading or generating feature files
group: service
language: codified-2
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/plugin-scenarios-run-as-pytest-bdd, design-decision/query-commands-answer-in-their-output]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g42, r42, g43, r43, g44, r44, g105, r105, g88, r88, g89, r89, g90, r90, g91, r91, g92, r92, g93, r93, g94, r94, g95, r95, g96, r96, g97, r97, g98, r98, g99, r99, g100, r100, g101, r101, g102, r102, g103, r103, g104, r104, g106, r106, g107, r107, g108, r108, g109, r109, g110, r110, g111, r111, g113, r113, g112, r112, g117, r117, g118, r118, g119, r119, g114, r114, g115, r115, g116, r116, g120, r120, g121, r121, g122, r122, g123, r123, g124, r124, g125, r125, g126, r126, g127, r127, g128, r128, g129, r129, g130, r130, g132, r132, g131, r131, g133, r133, g134, r134, g135, r135]
unbuilt: []
---

# Feature file tools

## Purpose
`scripts/features` reads Gherkin feature files without the test runner: it counts and lists scenarios by tag or
title, lists the deprecated scenarios kept from before the conversion, and verifies that every scenario has exactly
one test binding it. It writes each codified service capability's feature file from its requirement groups
(`generate`), and checks that every step of a generated feature has a handler (`vocab`). It is not a Gherkin runner
and runs no test; it edits no feature file by hand, since the generator owns them. Which sentences `generate` writes
the scenario of is the language reference's to say (`grammar/language.md`, its constructs and their tested lines),
not a line here for each construct.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next scenario's tag
  lines. A Scenario Outline counts once per Examples row, and each scenario takes its feature's tags and its Examples
  table's tags.
- `list --tag` takes the tag with its leading `@` or without; `list` matching nothing prints nothing and exits 0.
- Output lines: `list` prints `<path>: <title>`; `deprecated` prints
  `<path>: <title> | for: <what> | <replacement's path> @r<n>` or `none deprecated`; `bindings` prints
  `<path>:<line>: no scenario titled "<title>" in <feature>`, and with `--unbound`
  `<feature path>: <title> | bound by no test` or `<feature path>: <title> | bound by <module>:<line>, <module>:<line>`.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up among
  the module's own top-level assignments. A `scenario` or `scenarios` path names a feature file by its base name, or
  a directory by every feature file under it. A test module under `--tests` that does not parse is refused, named.
- `bindings --unbound` takes feature files after it; with none, every feature file under `--dir`. A scenario bound by
  more than one call is printed with each call's module and line.
- `generate` and `vocab` are the GF conversion's design §13.4 and §14: `generate --check` with no names prints
  `skipped <c>: not codified` for each service capability not yet codified; naming one exits 2; `--preview <file>`
  prints a draft's feature and writes nothing. `vocab --check --tests <dir> [<feature>...]` loads `<dir>`'s
  `world_*.py` and `*_handlers*.py` and names each step with no handler and each key two handlers claim.
- Exit code: 0 success, 1 a check failed or a file was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.

## Dropped

- r12@0.29: removed with `features move`: the generator owns the feature files (the GF conversion's design §15)
- r13@0.29: removed with `features move`: the generator owns the feature files (the GF conversion's design §15)
- r14@0.29: removed with `features move`: the generator owns the feature files (the GF conversion's design §15)
- r16@0.29: removed with `features verify-moved`: the generator owns the feature files (the GF conversion's design §15)
- r17@0.29: removed with `features verify-moved`: the generator owns the feature files (the GF conversion's design §15)
- r19@0.29: removed with `features deprecate`: the generator owns the feature files (the GF conversion's design §15)
- r23@0.29: removed with `features retire`: the generator owns the feature files (the GF conversion's design §15)
- r24@0.29: removed with `features retire`: the generator owns the feature files (the GF conversion's design §15)
- r28@0.29: removed with `features rebind`: the generator owns the feature files (the GF conversion's design §15)
- r29@0.29: removed with `features rebind`: the generator owns the feature files (the GF conversion's design §15)
- r35@0.29: the title lookup of `tag`, `move`, `deprecate` and `retire`, which are removed: the generator owns the feature files (the GF conversion's design §15)
- r51@0.29: removed with `features tag`: the generator owns the feature files (the GF conversion's design §15)
- r52@0.29: `--file` chose the file of a title for `tag`, `move`, `deprecate` and `retire`, which are removed: the generator owns the feature files (the GF conversion's design §15)
- r56@0.29: removed with `features rebind`: the generator owns the feature files (the GF conversion's design §15)
- feature-file-tools#r60@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)
- feature-file-tools#r61@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)
- feature-file-tools#r62@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)

## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g88 | feature-reading#g1 |
| r88 | feature-reading#r1 |
| g89 | feature-reading#g2 |
| r89 | feature-reading#r2 |
| g90 | feature-reading#g3 |
| r90 | feature-reading#r3 |
| g91 | feature-reading#g4 |
| r91 | feature-reading#r4 |
| g92 | feature-reading#g5 |
| r92 | feature-reading#r5 |
| g93 | feature-reading#g6 |
| r93 | feature-reading#r6 |
| g94 | feature-reading#g7 |
| r94 | feature-reading#r7 |
| g95 | dropped |
| r95 | dropped |
| g96 | feature-reading#g8 |
| r96 | feature-reading#r8 |
| g97 | feature-reading#g9 |
| r97 | feature-reading#r9 |
| g98 | feature-reading#g10 |
| r98 | feature-reading#r10 |
| g99 | dropped |
| r99 | dropped |
| g100 | feature-reading#g11 |
| r100 | feature-reading#r11 |
| g101 | feature-reading#g12 |
| r101 | feature-reading#r12 |
| g102 | feature-reading#g13 |
| r102 | feature-reading#r13 |
| g103 | feature-reading#g14 |
| r103 | feature-reading#r14 |
| g104 | dropped |
| r104 | dropped |
| g106 | scenarios#g1 |
| r106 | scenarios#r1 |
| g107 | scenarios#g2 |
| r107 | scenarios#r2 |
| g108 | scenarios#g3 |
| r108 | scenarios#r3 |
| g109 | scenarios#g4 |
| r109 | scenarios#r4 |
| g110 | scenarios#g5 |
| r110 | scenarios#r5 |
| g111 | scenarios#g6 |
| r111 | scenarios#r6 |
| g113 | scenarios#g7 |
| r113 | scenarios#r7 |
| g112 | scenarios#g8 |
| r112 | scenarios#r8 |
| g117 | scenarios#g9 |
| r117 | scenarios#r9 |
| g118 | scenarios#g10 |
| r118 | scenarios#r10 |
| g119 | scenarios#g11 |
| r119 | scenarios#r11 |
| g114 | scenarios#g12 |
| r114 | scenarios#r12 |
| g115 | scenarios#g13 |
| r115 | scenarios#r13 |
| g116 | scenarios#g14 |
| r116 | scenarios#r14 |
| g120 | scenarios#g15 |
| r120 | scenarios#r15 |
| g121 | scenarios#g16 |
| r121 | scenarios#r16 |
| g122 | scenarios#g17 |
| r122 | scenarios#r17 |
| g123 | scenarios#g18 |
| r123 | scenarios#r18 |
| g124 | scenarios#g19 |
| r124 | scenarios#r19 |
| g125 | scenarios#g20 |
| r125 | scenarios#r20 |
| g126 | scenarios#g21 |
| r126 | scenarios#r21 |
| g127 | scenarios#g22 |
| r127 | scenarios#r22 |
| g128 | scenarios#g23 |
| r128 | scenarios#r23 |
| g129 | scenarios#g24 |
| r129 | scenarios#r24 |
| g130 | scenarios#g25 |
| r130 | scenarios#r25 |
| g132 | scenarios#g26 |
| r132 | scenarios#r26 |
| g131 | scenarios#g27 |
| r131 | scenarios#r27 |
| g133 | scenarios#g28 |
| r133 | scenarios#r28 |
| g134 | scenarios#g29 |
| r134 | scenarios#r29 |
| g135 | scenarios#g30 |
| r135 | scenarios#r30 |
