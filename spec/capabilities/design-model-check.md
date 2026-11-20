---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or session verifying a repository against the design model
group: service
language: codified-2
rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-names-one-requirement, design-decision/query-commands-answer-in-their-output, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items, design-decision/work-items-named-by-ids, design-decision/the-glossary-is-a-target-of-spec-work]
retired: [r8, r9, r12, r13, r14, r15, r16, r17, r18, r21, r26, r27, r29, r31, r32, r33, r34, r35, r37, r39, r45, r46, r53, g73, r73, g72, r72, g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g10, r10, g11, r11, g19, r19, g20, r20, g22, r22, g23, r23, g24, r24, g25, r25, g28, r28, g30, r30, g36, r36, g38, r38, g40, r40, g41, r41, g42, r42, g43, r43, g44, r44, g47, r47, g48, r48, g49, r49, g51, r51, g52, r52, g57, r57, g58, r58, g59, r59, g60, r60, g61, r61, g62, r62, g63, r63, g66, r66, g64, r64, g65, r65, g67, r67, g68, r68, g69, r69, g70, r70, g71, r71, g74, r74, g75, r75, g76, r76, g77, r77, g78, r78, g79, r79, g80, r80, g81, r81, g82, r82, g83, r83, g84, r84, g85, r85, g86, r86, g87, r87, g88, r88, g89, r89, g90, r90, g91, r91, g92, r92, g93, r93, g94, r94, g95, r95, g96, r96, g97, r97, g98, r98, g99, r99, g100, r100, g101, r101, g131, r131, g132, r132, g133, r133, g134, r134, g135, r135, g136, r136, g137, r137, g138, r138, g139, r139, g140, r140, g141, r141, g142, r142, g143, r143, g144, r144, g145, r145, g157, r157, g158, r158, g159, r159, g160, r160, g161, r161, g162, r162, g163, r163, g164, r164, g165, r165, g166, r166, g167, r167, g168, r168, g169, r169, g170, r170, g171, r171, g172, r172, g173, r173, g50, r50, g54, r54, g55, r55, g56, r56, g156, r156, g174, r174, g175, r175, g176, r176, g177, r177, g178, r178, g179, r179, g180, r180, g181, r181, g182, r182, g183, r183, g184, r184, g185, r185, g186, r186, g187, r187, g188, r188, g189, r189, g190, r190, g191, r191, g192, r192, g193, r193, g194, r194, g195, r195, g196, r196, g197, r197, g198, r198, g199, r199, g200, r200, g201, r201, g202, r202, g203, r203, g204, r204, g205, r205, g206, r206, g207, r207, g208, r208, g209, r209, g210, r210, g211, r211, g212, r212, g213, r213, g214, r214, g215, r215, g216, r216, g217, r217, g218, r218, g219, r219, g220, r220, g221, r221, g222, r222, g223, r223, g224, r224, g225, r225, g226, r226, g227, r227, g228, r228, g229, r229, g230, r230, g231, r231, g232, r232, g233, r233, g234, r234, g235, r235, g236, r236, g237, r237, g238, r238, g239, r239, g240, r240, g241, r241, g242, r242, g243, r243, g244, r244, g245, r245, g246, r246, g247, r247, g248, r248, g249, r249, g250, r250, g251, r251, g252, r252, g253, r253, g254, r254, g255, r255, g256, r256, g257, r257, g258, r258, g259, r259, g260, r260, g261, r261, g262, r262, g263, r263, g264, r264, g279, r279, g280, r280, g281, r281, g282, r282, g283, r283, g284, r284, g285, r285, g286, r286, g287, r287, g288, r288, g289, r289, g290, r290, g293, r293, g294, r294, g295, r295, g291, r291, g292, r292, g298, r298, g299, r299, g300, r300, g301, r301, g302, r302, g303, r303, g304, r304, g305, r305, g296, r296, g297, r297, g306, r306, g307, r307, g308, r308, g311, r311, g312, r312, g313, r313, g309, r309, g310, r310, g314, r314, g315, r315, g316, r316, g317, r317, g318, r318, g319, r319, g321, r321, g322, r322, g320, r320, g323, r323, g324, r324, g326, r326, g327, r327, g325, r325, g328, r328, g329, r329]
unbuilt: []
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records, in the final
layout and no other — as the facts of design model v5 (`docs/reference/design-model.md`), and prints what the model refuses,
each rule by its code and its plain label. It also writes the generated decisions index, lists the rules, and traces
a requirement to why it exists. It does not edit the spec, the work or the records, and it verifies one bounded
context: product-level artifacts are read only where the files contain them.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- `scripts/model.lp` is design model v5's graph in clingo; facts use its relation names. Each rule's plain label is a
  fact `label("<code>", "<label>")` beside the rule, the one place it is written; `check` and `rules` read the labels
  from the solve, and a unit test fails when a relation has no label or two.
- `model` reads, under `--root` (default the current directory), only `spec/index.md`, `spec/universal.md`,
  `spec/restated.json`, `spec/capabilities/*.md`, every `*.feature` under `features/`, every `spec/decisions/*.md` but
  `index.md` and `README.md`, `.shop/requests/*.md`, the `source` of the frozen `.shop/work/*/initiative.md` and
  `.shop/work/requests/*.md` (as citations of observations), `.shop/records/observations.md` and any other Markdown under `.shop/records/` whose frontmatter has an `id`.
- References: `<name>#r<n>` or `capability/<name>#r<n>` is a requirement of `capability/<context path>/<name>`;
  `<capability>#r<a>-r<b>` in a list is every id from a to b; `<cap>#r<n>@0.29` is resolved through
  `spec/restated.json`. A node is `<kind>/<context path>/<name>` or `<kind>/<name>`, and a bare `<name>` only in a
  field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) or the capability part of a
  reference. A decision's `source`, and not its `by`, is a list of ids.
- A `quote-<n>` in a decision's `source` names the person's words kept as `.shop/quotes/<n>.md`, and resolves when that
  file exists.
- The glossary of `spec/index.md` (and each capability's `## Terms`) is read by `spec_lexicon` where the index is
  codified; a term is `term/<context path>/<term>`, and each word after `Not:` a word it avoids. A requirement or a
  scenario mentions a term or avoided word when it contains it as a whole word, whatever its case, with a plural "s"
  allowed, outside code spans, double-quoted strings and `@` tags.
- A scenario's `@g<n>` tag names the group that generates it, and its `@r<n>` tags the group's requirements.
- Output: `<code>  <label>  (<count>)` above a violated relation's rows; `warning <code>  <label>  (<count>)`;
  `rules` prints `<code>  <label>`, the violations first and then the warnings. `--json` adds `"labels": {code: label}`
  for the codes it prints, and `check --json` exits as it would without `--json`.
- Without `--json`, `model check` ends with the counts of violations, warnings, unresolved references and file
  problems. `--limit <n>` (default 10) prints at most n rows of each violated relation and how many more there are.
- If `import clingo` fails, `model check` tries again, once, under the first interpreter that has clingo of
  `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`,
  `/usr/local/bin/python3` and `/usr/bin/python3`, in that order; with none, it names each one it tried.
- An initiative may be `done` when its parts are closed: a `formulated` capability-proposal, an `approved`
  glossary-proposal and any `withdrawn` part count as closed.
- `model facts` prints the facts, one a line in clingo's syntax, using only the standard library.
- `model decisions` writes `spec/decisions/index.md` listing every decision in `spec/decisions/` that has an `id`,
  with its summary, status, what it supersedes and when to revisit it, each linked to its file; `--check` says
  whether the file is current. `model why <capability>#r<n>` prints the requirement's text (or that no capability has
  it), each capability-proposal that adds, changes or removes it in date order with its status and date, the
  `part_of` chain to its initiative and the initiative's sources; given an argument that is not a requirement
  reference it exits 2.
- Exit code: 0 success; 1 a violation, unresolved reference or file problem found, or a decisions index that is
  not current; 2 no interpreter has clingo, or bad usage.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is verified together with this one.

## Dropped
- r18@0.29: the reading of a range is `model`'s implementation, kept under Implementation, may change.
- r19@0.29: the files `model` reads are its implementation, kept under Implementation, may change.
- r20@0.29: a scenario's tags are read as design model v5's generates (C4, C6), kept under Implementation, may change.
- r21@0.29: the reading of a reference is `model`'s implementation, kept under Implementation, may change.
- r43@0.29: the reading of a node's id is `model`'s implementation, kept under Implementation, may change.
- r51@0.29: what counts as a mention is `model`'s implementation, kept under Implementation, may change.
- r64@0.29: the reading of a decision's source is `model`'s implementation, kept under Implementation, may change.
- r105@0.29: restated U3 (a refused command exits with an error and changes nothing).
- r33@0.29: restated U8 (`--json` prints one JSON object), for `model check`.
- r108@0.29: restated U8 (`--json` prints one JSON object), for `model why`.
- r109@0.29: restated U8 (`--json` prints one JSON object), for `model rules`.
- r6@0.29: retired with design-model-check#r8 in 0.31.0 (the-old-workflow-retired).
- r7@0.29: retired with design-model-check#r9 in 0.31.0 (the-old-workflow-retired).
- r10@0.29: retired with design-model-check#r12 in 0.31.0 (the-old-workflow-retired).
- r16@0.29: retired with design-model-check#r53 in 0.31.0 (the-old-workflow-retired).
- r17@0.29: retired with design-model-check#r53 in 0.31.0 (the-old-workflow-retired).
- r22@0.29: retired with design-model-check#r31 in 0.31.0 (the-old-workflow-retired).
- r23@0.29: retired with design-model-check#r32 in 0.31.0 (the-old-workflow-retired).
- r24@0.29: retired with design-model-check#r33 in 0.31.0 (the-old-workflow-retired).
- r34@0.29: retired with design-model-check#r13 in 0.31.0 (the-old-workflow-retired).
- r35@0.29: retired with design-model-check#r14 in 0.31.0 (the-old-workflow-retired).
- r36@0.29: retired with design-model-check#r45 in 0.31.0 (the-old-workflow-retired).
- r46@0.29: retired with design-model-check#r37 in 0.31.0 (the-old-workflow-retired).
- r59@0.29: retired with design-model-check#r15 in 0.31.0 (the-old-workflow-retired).
- r66@0.29: retired with design-model-check#r34 in 0.31.0 (the-old-workflow-retired).
- r106@0.29: retired with design-model-check#r26 in 0.31.0 (the-old-workflow-retired).
- r110@0.29: retired with design-model-check#r27 in 0.31.0 (the-old-workflow-retired).
- r113@0.29: retired with design-model-check#r16 in 0.31.0 (the-old-workflow-retired).
- r114@0.29: retired with design-model-check#r17 in 0.31.0 (the-old-workflow-retired).
- r118@0.29: retired with design-model-check#r29 in 0.31.0 (the-old-workflow-retired).
- r119@0.29: retired with design-model-check#r18 in 0.31.0 (the-old-workflow-retired).
- r121@0.29: retired with design-model-check#r21 in 0.31.0 (the-old-workflow-retired).
- r122@0.29: retired with design-model-check#r35 in 0.31.0 (the-old-workflow-retired).
- r123@0.29: retired with design-model-check#r46 in 0.31.0 (the-old-workflow-retired).
- r124@0.29: retired with design-model-check#r39 in 0.31.0 (the-old-workflow-retired).
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g50 | decisions#g16 |
| r50 | decisions#r16 |
| g54 | checking#g1 |
| r54 | checking#r1 |
| g55 | checking#g2 |
| r55 | checking#r2 |
| g56 | records#g1 |
| r56 | records#r1 |
| g156 | consistency#g1 |
| r156 | consistency#r1 |
| g174 | checking#g3 |
| r174 | checking#r3 |
| g175 | checking#g4 |
| r175 | checking#r4 |
| g176 | checking#g5 |
| r176 | checking#r5 |
| g177 | checking#g6 |
| r177 | checking#r6 |
| g178 | checking#g7 |
| r178 | checking#r7 |
| g179 | checking#g8 |
| r179 | checking#r8 |
| g180 | checking#g9 |
| r180 | checking#r9 |
| g181 | checking#g10 |
| r181 | checking#r10 |
| g182 | checking#g11 |
| r182 | checking#r11 |
| g183 | checking#g12 |
| r183 | checking#r12 |
| g184 | checking#g13 |
| r184 | checking#r13 |
| g185 | checking#g14 |
| r185 | checking#r14 |
| g186 | checking#g15 |
| r186 | checking#r15 |
| g187 | checking#g16 |
| r187 | checking#r16 |
| g188 | checking#g17 |
| r188 | checking#r17 |
| g189 | checking#g18 |
| r189 | checking#r18 |
| g190 | checking#g19 |
| r190 | checking#r19 |
| g191 | checking#g20 |
| r191 | checking#r20 |
| g192 | checking#g21 |
| r192 | checking#r21 |
| g193 | checking#g22 |
| r193 | checking#r22 |
| g194 | decisions#g17 |
| r194 | decisions#r17 |
| g195 | checking#g23 |
| r195 | checking#r23 |
| g196 | checking#g24 |
| r196 | checking#r24 |
| g197 | checking#g25 |
| r197 | checking#r25 |
| g198 | checking#g26 |
| r198 | checking#r26 |
| g199 | checking#g27 |
| r199 | checking#r27 |
| g200 | checking#g28 |
| r200 | checking#r28 |
| g201 | checking#g29 |
| r201 | checking#r29 |
| g202 | decisions#g18 |
| r202 | decisions#r18 |
| g203 | decisions#g19 |
| r203 | decisions#r19 |
| g204 | records#g2 |
| r204 | records#r2 |
| g205 | reading#g1 |
| r205 | reading#r1 |
| g206 | reading#g2 |
| r206 | reading#r2 |
| g207 | checking#g30 |
| r207 | checking#r30 |
| g208 | checking#g31 |
| r208 | checking#r31 |
| g209 | reading#g3 |
| r209 | reading#r3 |
| g210 | reading#g4 |
| r210 | reading#r4 |
| g211 | reading#g5 |
| r211 | reading#r5 |
| g212 | reading#g6 |
| r212 | reading#r6 |
| g213 | reading#g7 |
| r213 | reading#r7 |
| g214 | checking#g32 |
| r214 | checking#r32 |
| g215 | checking#g33 |
| r215 | checking#r33 |
| g216 | reading#g8 |
| r216 | reading#r8 |
| g217 | checking#g34 |
| r217 | checking#r34 |
| g218 | consistency#g2 |
| r218 | consistency#r2 |
| g219 | checking#g35 |
| r219 | checking#r35 |
| g220 | checking#g36 |
| r220 | checking#r36 |
| g221 | checking#g37 |
| r221 | checking#r37 |
| g222 | checking#g38 |
| r222 | checking#r38 |
| g223 | checking#g39 |
| r223 | checking#r39 |
| g224 | checking#g40 |
| r224 | checking#r40 |
| g225 | checking#g41 |
| r225 | checking#r41 |
| g226 | checking#g42 |
| r226 | checking#r42 |
| g227 | checking#g43 |
| r227 | checking#r43 |
| g228 | checking#g44 |
| r228 | checking#r44 |
| g229 | reading#g9 |
| r229 | reading#r9 |
| g230 | reading#g10 |
| r230 | reading#r10 |
| g231 | reading#g11 |
| r231 | reading#r11 |
| g232 | reading#g12 |
| r232 | reading#r12 |
| g233 | reading#g13 |
| r233 | reading#r13 |
| g234 | reading#g14 |
| r234 | reading#r14 |
| g235 | reading#g15 |
| r235 | reading#r15 |
| g236 | reading#g16 |
| r236 | reading#r16 |
| g237 | reading#g17 |
| r237 | reading#r17 |
| g238 | reading#g18 |
| r238 | reading#r18 |
| g239 | reading#g19 |
| r239 | reading#r19 |
| g240 | reading#g20 |
| r240 | reading#r20 |
| g241 | reading#g21 |
| r241 | reading#r21 |
| g242 | reading#g22 |
| r242 | reading#r22 |
| g243 | reading#g23 |
| r243 | reading#r23 |
| g244 | reading#g24 |
| r244 | reading#r24 |
| g245 | reading#g25 |
| r245 | reading#r25 |
| g246 | checking#g45 |
| r246 | checking#r45 |
| g247 | consistency#g3 |
| r247 | consistency#r3 |
| g248 | consistency#g4 |
| r248 | consistency#r4 |
| g249 | consistency#g5 |
| r249 | consistency#r5 |
| g250 | consistency#g6 |
| r250 | consistency#r6 |
| g251 | consistency#g7 |
| r251 | consistency#r7 |
| g252 | reading#g26 |
| r252 | reading#r26 |
| g253 | consistency#g8 |
| r253 | consistency#r8 |
| g254 | reading#g27 |
| r254 | reading#r27 |
| g255 | reading#g28 |
| r255 | reading#r28 |
| g256 | reading#g29 |
| r256 | reading#r29 |
| g257 | reading#g30 |
| r257 | reading#r30 |
| g258 | reading#g31 |
| r258 | reading#r31 |
| g259 | reading#g32 |
| r259 | reading#r32 |
| g260 | consistency#g9 |
| r260 | consistency#r9 |
| g261 | consistency#g10 |
| r261 | consistency#r10 |
| g262 | consistency#g11 |
| r262 | consistency#r11 |
| g263 | consistency#g12 |
| r263 | consistency#r12 |
| g264 | consistency#g13 |
| r264 | consistency#r13 |
| g279 | reading#g33 |
| r279 | reading#r33 |
| g280 | consistency#g14 |
| r280 | consistency#r14 |
| g281 | reading#g34 |
| r281 | reading#r34 |
| g282 | reading#g35 |
| r282 | reading#r35 |
| g283 | reading#g36 |
| r283 | reading#r36 |
| g284 | reading#g37 |
| r284 | reading#r37 |
| g285 | reading#g38 |
| r285 | reading#r38 |
| g286 | decisions#g20 |
| r286 | decisions#r20 |
| g287 | checking#g46 |
| r287 | checking#r46 |
| g288 | consistency#g15 |
| r288 | consistency#r15 |
| g289 | consistency#g16 |
| r289 | consistency#r16 |
| g290 | consistency#g17 |
| r290 | consistency#r17 |
| g293 | reading#g39 |
| r293 | reading#r39 |
| g294 | consistency#g18 |
| r294 | consistency#r18 |
| g295 | reading#g40 |
| r295 | reading#r40 |
| g291 | reading#g41 |
| r291 | reading#r41 |
| g292 | consistency#g19 |
| r292 | consistency#r19 |
| g298 | reading#g42 |
| r298 | reading#r42 |
| g299 | reading#g43 |
| r299 | reading#r43 |
| g300 | reading#g44 |
| r300 | reading#r44 |
| g301 | consistency#g20 |
| r301 | consistency#r20 |
| g302 | consistency#g21 |
| r302 | consistency#r21 |
| g303 | reading#g45 |
| r303 | reading#r45 |
| g304 | reading#g46 |
| r304 | reading#r46 |
| g305 | reading#g47 |
| r305 | reading#r47 |
| g296 | reading#g48 |
| r296 | reading#r48 |
| g297 | consistency#g22 |
| r297 | consistency#r22 |
| g306 | reading#g49 |
| r306 | reading#r49 |
| g307 | reading#g50 |
| r307 | reading#r50 |
| g308 | reading#g51 |
| r308 | reading#r51 |
| g311 | reading#g52 |
| r311 | reading#r52 |
| g312 | reading#g53 |
| r312 | reading#r53 |
| g313 | reading#g54 |
| r313 | reading#r54 |
| g309 | reading#g55 |
| r309 | reading#r55 |
| g310 | consistency#g23 |
| r310 | consistency#r23 |
| g314 | consistency#g24 |
| r314 | consistency#r24 |
| g315 | consistency#g25 |
| r315 | consistency#r25 |
| g316 | consistency#g26 |
| r316 | consistency#r26 |
| g317 | reading#g56 |
| r317 | reading#r56 |
| g318 | reading#g57 |
| r318 | reading#r57 |
| g319 | reading#g58 |
| r319 | reading#r58 |
| g321 | consistency#g27 |
| r321 | consistency#r27 |
| g322 | consistency#g28 |
| r322 | consistency#r28 |
| g320 | consistency#g29 |
| r320 | consistency#r29 |
| g323 | consistency#g30 |
| r323 | consistency#r30 |
| g324 | checking#g47 |
| r324 | checking#r47 |
| g326 | reading#g59 |
| r326 | reading#r59 |
| g327 | reading#g60 |
| r327 | reading#r60 |
| g325 | reading#g61 |
| r325 | reading#r61 |
| g328 | consistency#g31 |
| r328 | consistency#r31 |
| g329 | consistency#g32 |
| r329 | consistency#r32 |
