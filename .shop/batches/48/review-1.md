---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-48/review-1
kind: review
batch: batch-48
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/72
head: bf6b1ea134b110b30f5c5ab43afb3bc153ca63ba
range: 6f10a4c2b6cde2b32b828f0ece9638f864222ed0..bf6b1ea134b110b30f5c5ab43afb3bc153ca63ba
result: fix-now
---

# batch-48 review 1

## Verdict

All five items are built, and each requirement line has its generated scenario and a handler that drives it. One thing must be fixed: the batch makes `tools check` fail. It exits 1 at Head and exited 0 at the base. The three problems it reports are in files that b368 and b369 changed. The change is also over the size limit. The other findings are hardening and do not hold the merge.

## Findings

### f1 Important fix now: `tools check` fails on b368's files (ruff I001, SIM401)
- item: b368
- where: tests/scenarios/checking_handlers_annotate.py:18
`python3 scripts/tools check --base 6f10a4c2b` exits 1 at Head and exited 0 at the base. Ruff reports two problems in files b368 changed:

```
scripts/adapter_cli_check.py:13:1: I001 [*] Import block is un-sorted or un-formatted
tests/scenarios/checking_handlers_annotate.py:18:5: SIM401 Use `sys.modules.get("shop_work_queue_world", None)` instead of an `if` block
```

b368 changed `scripts/adapter_cli_check.py` (the `-B` flag in `read_program`), which brought it into the check's range. The import block at line 13 is not formatted the way ruff's isort wants. `checking_handlers_annotate.py` is new in b368. Fix: in `checking_handlers_annotate.py`, write `W = sys.modules.get("shop_work_queue_world")`. In `adapter_cli_check.py`, reformat the import block (`ruff check --fix` handles I001). Then run `tools check --base <forked_from>` and confirm it exits 0.

### f2 Important fix now: `tools check` fails on b369's spec_catalogued (vulture: unused `stamp`)
- item: b369
- where: scripts/spec_catalogued.py:14
`tools check` also exits 1 on this vulture warning, which the base did not have:

```
scripts/spec_catalogued.py:14: unused variable 'stamp' (100% confidence)
```

`_codes(path, stamp)` takes the file's mtime only so that `functools.cache` keys on it, and the body never reads it. Fix: make the argument visibly used, or name it so vulture skips it, for example with a whitelist entry or a name starting with `_` if the project's vulture setup ignores those. Keep the cache keyed on the mtime, so that `spec parse` still sees an edited catalogue in the same process.

### f3 Minor observation: the change is over the review size limit
- item: -
- where: -
`## Size` reports 73 files, +2671 -1919 against a limit of 1000 changed lines. Most of it comes from two items:
- **b369:** retiring reading r1-r61 removes about 590 lines of `features/reading.feature`, about 230 lines of `spec/capabilities/reading.md` and most of `grammar/corpus/spec/reading.md`, and adds `parsing.feature` and its corpus.
- **b368:** annotating `spec/adapters/cli.toml` adds about 1000 lines of `requirements = [...]`.

### f4 Minor observation: a readiness test was removed with the items it checked
- item: b334
- where: tests/scripts/test_readiness_lay_model.py:89
Commits 21e7f8747 (b334) and 62141fa94 (b369) delete `test_the_ready_items_reworded_for_the_migrated_spec_meet_the_readiness_bar`, which was parametrized over b309, b318 and b334. All three items are now laid in this batch's `spec/`, so the bar could no longer pass them on this tree. I read the deletion as the end of a one-off check, not a weakened test. It is recorded here because it is a deleted test: if the readiness bar should still be exercised on a migrated spec, that needs a fixture item of its own.

### f5 Minor observation: retiring reading r1-r61 drops the scenario coverage of many refusals that still exist
- item: b369
- where: tests/scenarios/design_model_check_worlds.py:208
The b369 shaping note says to retire every reading line, and only the general ones are restated in parsing. The code still makes these refusals:
- a verb with no object or no recipient (`spec_refusal4`)
- a passive
- a verb whose aspect is wrong for its clause (`misaspected`)
- a duration with no unit
- an order in a While clause, a trigger or a forbidden act
- a state verb in a response that names the response and not the trigger (old r58)

Their world rows (`objectless`, `recipientless`, `agentless`, `misaspected`, `unitless`, ...) are removed from `TABLE`, so no scenario drives them now. Some may still be covered by `tests/scripts/` tests, but I did not check each one. In addition, `spec/model/specification.md` narrows `language.parse`'s declared refusals to the five parsing states, while `spec parse` still refuses for reasons outside that list (for example "term out of its frame" and "order out of place").

### f6 Minor observation: `reading` survives beside `parsing`, against b369's note
- item: b369
- where: spec/capabilities/reading.md:9
b369's note says the emptied `reading.md` and its feature, tests and handlers are to be removed or moved to parsing. Because b334 adds reading#r62, `reading` stays a live capability with one line and the same `specifies: service language: parse, look up` as `parsing` (which specifies `language: parse`). `reading_handlers_order.py` serves both capabilities. A later item could move r62 into parsing, with a new id, and retire `reading`.

### f7 Minor observation: `spec annotate` can write a requirement twice when its line is wrapped
- item: b368
- where: scripts/adapter_annotate.py:67
The duplicate check compares the raw text, `(ident, text) not in out[...]`, but what is stored is the whitespace-normalised text, `" ".join(text.split())`. A requirement whose line wraps across lines in its capability file and that yields two `requester` facts for one operation (for example a trigger on each of "two Ks") would be appended twice. I did not find such a line in this repository's `cli.toml`. Fix: compare the normalised text, or compare by id only.

### f8 Minor observation: holds-exactly's Given now applies to other "no K in y" shapes too
- item: b309
- where: scripts/spec_steps4_boxes.py:49
`spec_steps4_counter.excluded` now runs before `no(...)` for every precondition "no" box of one K that has a single `in` link and only `not` boxes inside. That includes a plain "no file in the worktree whose version is not `2.0.0`", which is not holds-exactly. For such a line the generated Givens change from "the worktree holds no such file" to "a file f, whose version is another value, that the worktree does not hold". The second is weaker: it no longer says the precondition holds. No current feature changed (`features generate --check` exits 0). Restricting `excluded` to the only-half that b309's every-half sits beside would keep the old Given for other lines.
