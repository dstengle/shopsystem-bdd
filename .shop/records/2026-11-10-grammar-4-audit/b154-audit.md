# Audit: grammar 4 against analysis-tools and trials (b154)

Sources: b154's reworded lines (analysis-tools r36-r67 plus the kept ids r7 and r8; trials r6-r10), main's spec (still
codified-1 for both capabilities; no other item has added grammar-4 lines to them), and phase 3's c.tsv candidates and
c.md. I laid b154 over a copy of `spec/` (`backlog_lines.lay`) and ran `model parse --form` on all 39 laid lines:
every line parses. Where a verdict depends on another wording, I parsed that wording too. Per-line results are in
`audit.tsv`, 40 rows: 39 live lines plus analysis-tools r26, which was retired with no successor.

## Counts

| Verdict | Lines | Where |
|---|---|---|
| fine | 11 | analysis r36, r7, r8, r59, r61, r62, r63, r67; trials r6, r9, r10 |
| distortion | 25 | analysis r37-r41, r43, r45-r50, r52-r58, r26, r60, r64, r66; trials r7, r8 |
| unsayable | 2 | analysis r51 (a per-file count), r65 (a default) |
| coined | 2 | analysis r42 (log line), r44 (pinned version) |

The refusals are clean: r45, r54, r55, r59, r62 and r63 all use "shall refuse the command and name X". So are the
relative clauses ("every test that executes the function", "a measurement of the trial that lists the target").
Phase 3's coined *present* is gone. Most of the distortions come from the same few missing constructs, and the same
workaround repeats across many lines.

## Missing constructs (lines that need each)

| Construct | Lines | How the lines work around it |
|---|---|---|
| EXISTS: an intransitive state, "X exists" / "has been written" | 14 (7 where it is the main fault) | "this file system holds the dot-venv interpreter", "this repository holds a coverage map". Each needs a made-up container noun with `This:` and a relation row. The item says why: an intransitive state has no translation in the logic. |
| "the number of" | 8 | count nouns: test count, run count, untested count, reference count (r49, r50, r53, r56-r58); r51 drops its count; r64 has no "number of lines". |
| A definite for the interpreter in use | 5 | r43-r46 and r66 say "the environment of **the dot-venv interpreter**". This turns phase 3's example path into the rule: the line now holds only when `.venv` exists. |
| Ordered choice (first match), with paths as constants | 5 | r37-r41: four proper nouns stand in for paths ("a path is no term id"), and each line spells out the negated predecessors. r39 still overlaps r36 (`--python`). |
| every / no inside a relative clause in a response | 3 | r56 and r57 print "the function", one referent bound in the trigger, rather than every untested function. r42 moves "names every analysis tool" into a gloss. `print every function of the Python file that no test executes` does parse, with a correct every/not box: the gap is the generator and the bar, not the grammar. |
| Intransitive *fail* | 2 | r47: `outcome` attribute, `passing`/`failing`, a two-valued attribute. r46 loses "the pip command that failed". |
| Comparison of counts ("more lines than") | 2 | the coined verb *exceed* (r64, r65). |
| Invariant with no trigger | 2 | trials r7 and r8 become "When trial-runner starts a trial, ... shall read only ...". By R9 this binds only the step after the start. |
| Output layout (under a heading, one line) | 2 | r60 drops "under"; r42 (above). |
| Default value | 1 | r65's proper noun "the default size limit", glossed "300 lines ... when --limit gives none". |
| Distribution ("for each X, its Y") | 1 | r51. |
| Reported content ("say that no test executed it") | 1 | r52 prints only the commit. The "says none" is now only in the group title. |
| A name as argument (a thing that does not exist) | 1 | r54's "a function that no Python file has" posits a function that is in no file. The original meant the named file lacks it. |
| Relative clause with its own agent ("that the plugin pins") | 1 | r44's noun "pinned version", Kind of: analysis tool. |

## Worst examples

1. **r56 / r57** (`tools untested`): the original printed every function of the file that no test executed. The
   reword prints "the function", a single referent. The narrowing came from getting past the readiness bar (the item's
   notes), not from the grammar, which parses the right line.
2. **r43-r46, r66**: "the environment of the dot-venv interpreter is `virtualenv`". Phase 3 called `.venv/bin/python`
   example data. Making it a proper noun makes the install rules silent for `venv`, `$VIRTUAL_ENV` and
   `sys.executable`.
3. **r37-r41**: four glossary proper nouns and a container noun ("file system", `This:`) build a first-match rule
   out of "holds" and "does not hold". This is exactly the structure-in-glossary the anti-goals warn against.
4. **r42**: "shall print one log line". Everything the line used to say ("Probe: tools ->", each analysis tool)
   moved into the gloss of *log line*.
5. **Count nouns**: "the test count of the function" is "the number of tests that execute the function" pressed into
   a noun. The gloss carries the restrictor.
6. **r65**: the default lives in a proper noun's gloss, and the line still says only "exit successfully".
7. **trials r7 / r8**: an invariant weakened to a triggered rule.

## What a rewording alone could fix

- **trials r7, r8**: write them as invariants. "`trial-runner` shall read only files in the target of a trial." and
  "`trial-runner` shall write only the measurement of a trial." both parse (an R5 only box, no trigger) with the
  meaning of the original lines.
- **analysis r26**: "When the person runs `tools refs --json` on an identifier that a Python file defines, `tools`
  shall print every reference to the identifier and ..." parses. Retiring r26 dropped a distinct command string.
- **r43-r46, r66**: plain glossary work, no new construct. Give *Python interpreter* a `This:` ("the Python
  interpreter `tools` runs with") and say "the environment of the Python interpreter".
- **r44**: a plain verb *pin* (plugin pins version) would let the line say "the version of `ruff` that the plugin
  pins". The coined noun goes.
- **r54**: refuse a name rather than a thing, as r59 does for identifiers. This needs a *name* kind for the
  `path:function` argument.
- **r56, r57**: the right wording already parses. What needs fixing is the generator and the bar's "no" box, not the
  wording.

Not fixable by rewording: EXISTS (14 lines), "the number of" (8), ordered choice (5), intransitive fail (2),
comparison of counts (2), default (1), distribution (1), reported content (1) and output layout (2). Each of these
needs a construct in the base grammar and its logical form. EXISTS and "the number of" are the two that recur in
both phase 3 and this audit, so both pass the design's growth rule (a construct that recurs).
