---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-analysis-tools
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [analysis-tools]
adds: [analysis-tools#r59, analysis-tools#r60, analysis-tools#r61, analysis-tools#r62, analysis-tools#r63, analysis-tools#r64, analysis-tools#r65, analysis-tools#r66, analysis-tools#r67, analysis-tools#r68, analysis-tools#r69, analysis-tools#r70, analysis-tools#r71, analysis-tools#r72, analysis-tools#r73, analysis-tools#r74, analysis-tools#r75]
changes: []
removes: [analysis-tools#r49, analysis-tools#r17, analysis-tools#r3, analysis-tools#r4, analysis-tools#r6, analysis-tools#r7, analysis-tools#r56, analysis-tools#r53, analysis-tools#r54, analysis-tools#r55, analysis-tools#r57, analysis-tools#r16, analysis-tools#r51]
date: 2026-10-29
---

# analysis-tools

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- analysis-tools r53, r54, r55, r56 (removed; r56's replacement is r71, r53-r55 have none): the four `--json` lines for `tools map`, `tests-of`, `untested` and `refs` go because JSON is now the default (q25 line 1). r71 keeps `map`'s commit and test count in the JSON object; nothing says what `tests-of`, `untested` and `refs` hold in theirs, beyond the kept r9, r13, r14 ('print ...'), read under r59. Readings: (a) as drafted: r53-r55 retired with no replacement, r9, r13, r14 kept and read as the content of the JSON object (RECOMMENDED, fewest changes); (b) redraft r9, r13, r14 as 'shall give ... in its JSON object' (the tests with their count and the map's commit; the functions with their count and the commit; the references and the summary counts).
- analysis-tools r68 (added, replacing r4): `tools probe --log` gives its one line `Probe: tools -> ...` inside a field of the JSON object, for a researcher's notes. q25 names text only for the SessionStart hook, Gherkin and `model rules`. Readings: (a) keep r68 as drafted, the line in a field (RECOMMENDED: researchers paste it into notes); (b) retire r4 with no replacement, and `--log` goes (the probe fields of the JSON object give the same).
- analysis-tools r61-r65, r67, r69, r70, r72, r74, r75 (added, replacing the exit parts of r49, r17, r3, r6, r7, r57, r16, r51): refusals, missing tools and found faults now give `ok` false with exit 0, and a crash exits 1 (q25 lines 2-3). Readings: (a) as drafted, each specific line says `ok` false (RECOMMENDED, each line checkable alone); (b) only r61 and r64 state `ok`, the specific lines drop 'with `ok` false' and keep what the JSON object names.
- analysis-tools Implementation (changed, no Behaviour line): `--json` on `tools map`, `tests-of`, `untested`, `refs` is gone with r53-r56. When given now: (a) refused as an unknown option (RECOMMENDED: a flag that changes nothing hides a stale caller); (b) accepted and ignored.
- analysis-tools draft file: the writer could not write `analysis-tools.md` under the round-2 drafts path (a hook refused it); its full content, with r59-r75 and the removals, is only in `round-2/writer.reply.md`. Readings: (a) approve the lines as shown, to be written from the reply before the apply round (RECOMMENDED); (b) have the integrate round redo analysis-tools.
