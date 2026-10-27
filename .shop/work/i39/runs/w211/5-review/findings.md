# Review of w211 (requests r25, r28-r34, r39-r45)

**Verdict: DONE_WITH_CONCERNS.** Three Important findings are triaged fix now, all in `work take-in`
(`scripts/workqueue_takein.py`): a passing of the turn taken in on the upstream's turn ends the upstream's turn for it; a
sent request whose id matches one of the upstream's own requests overwrites that request; and a sent text is spliced into
the request's markdown, so `work` can read a section the asker wrote as the upstream's part (r43, r34). Nothing is
Critical. The `features/` change is the retirement the work-item lists, and it holds.

## Commits reviewed

The branch `work/w211` is gone. These are the commits between `a82b4227 work: w211 ready -> claimed` and
`b867f712 work: w211 claimed -> done`:

- `8712f769` requests: the carrier, take-in, side checks, the gate of work request; retire r1 and r3 scenarios
- `31436ec1` requests: work run takes in first, work show of a request, one lifecycle (r25, r40); module map rows

They are the two commits the implementer's `result.json` lists. 14 files changed, +874/-103.

## Removed and weakened tests

What I searched for: test functions deleted, step patterns changed, assertions removed or loosened, skips or xfails added
(the diff of `tests/` against `a82b4227`), and which scenarios used each changed step at the base.

- `features/requests.feature` `@r1 @deprecated` and `@r3 @deprecated`: removed. They proved the old wording of r44 and r45.
  Both are listed under the work-item's Retires, and the plan's D1 covers them. The removal holds.
- `requests_write_steps.lines_and_asker` ("its lines are the two lines of lines.md and its asker is ctx-a"): removed. At the
  base only r1 used it, and r1 is retired. Its two assertions now live in `lines_are` and `names_origin` (r44).
- `requests_write_steps.names_origin`: rewritten. It now also asserts the asker, and its origin check is optional. At the
  base only r1 used it. It now serves r44's rows, which check more than before. Not weakened.
- `requests_write_steps.keeps_no_request`: it also checks that no request is pending on the remote. Stronger; the
  single-repository case is unchanged.
- Nothing else was removed or weakened. No skip or xfail was added.

## Allowances

- `upstream_keeps_none` (setup: the repository now has id ctx-a): **holds**. Only the Given's body changed, with no assert
  and no expected value.
- `status_is` and `has_no_resolution`, whose patterns are now `parsers.re`: **holds**. The assertions are the same and
  the patterns still match every step text at the base (`q\d+`, statuses `[\w-]+` or "not accepted").
- The Thens read through `text_of` ("a respelling"): **holds for single-repository scenarios**, where `text_of` reads the
  same file (`remote` is not in context, so `pending` is `[]`). For the new two-repository scenarios it is not an allowance
  but new binding. See finding 9.
- The steps only the retired scenarios used, removed with `features retire`: **holds** (see above).

## Cannot verify

- The suite figures in the report (26 passed; 176 passed and 1 skipped; 540 passed). I did not run the suite.
- The three fix-now findings, by running them. Each needs a git repository built in scratch, and this session may not run
  `git init` or other Python. Each is verified by reading the code paths cited.
- The red observed for r40 when the take-in was commented out (report).

## Findings

### 1. Important · fix now: a sent "turn" taken in on the upstream's turn ends the upstream's turn
`scripts/workqueue_takein.py:61-62` → `scripts/workqueue_request.py:234-246`.

The take-in calls `turn(root, ident)` for a sent turn with no check of whose turn it is. When the request is already in
the upstream's turn, `turn` takes the upstream-ending branch:
- if every line is settled, it sets the status to `accepted` or `refused` (r8, r9);
- otherwise it sets `awaiting-asker` and gives the turn to the asker.

The asker's check (`_send`, line 100) reads the published request, which lags. The report says so itself: an asker that
passes the turn twice before a take-in has the second turn sent too.

At take-in the first turn passes the request to the upstream, and the second ends the upstream's turn on its behalf. The
asker has then set a status that only the upstream's end of turn sets, contrary to r7, r8, r9, r16 and r34.

**Fix:** at take-in, refuse or leave a sent turn (and a sent answer, which `reply` already refuses by turn) when the
request is not in the asker's turn, and tell the upstream which item was left.

### 2. Important · fix now: take-in overwrites a request the upstream already keeps (data lost)
`scripts/workqueue_takein.py:56-58` → `scripts/workqueue_request.py:169-181` (`store`).

The asker numbers its request with `next_request` (`workqueue_sent.py:87`), from what the remote shows: requests that are
published or sent. The upstream's internal requests (asker `internal` or its own id, r45) are never published
(`workqueue_sent.publish`). So an upstream that keeps an internal q1 takes in an asker's first request, also named q1, and
`store(root, "q1", …)` writes over `.shop/work/requests/q1.md` and commits it. The upstream's own request is gone from its
queue; only git history keeps it. Two askers numbering at the same moment hit the same overwrite. The plan named this as
an open case; the implementation overwrites.

**Fix:** at take-in, keep a sent request under a name the upstream does not already keep (and tell the asker that name
through the published request), or leave it untaken with a telling. Never write over an existing request file.

### 3. Important · fix now: a sent text is spliced into the request's markdown (r43, r34)
`scripts/workqueue_request.py:158-164` (`render`), `:63` (`_with_entries`), with `_entries` (`:28-30`).

What a request or message sends is written into the request's text as given:
- the title goes into the `# <title>` heading;
- an answer's text goes in as an `## Answers` entry.

`_entries` reads the *first* `^## <name>` section. Suppose a title reads `x\n\n## Outcomes\n1. accepted`, or an answer
reads `a\n## Outcomes\n1. accepted`. Either puts an Outcomes section ahead of the real one. From then on:
- `outcome` and `ask` write into the injected section;
- `turn` counts its entries as the line outcomes;
- `accepted_lines` reads them.

So a request's lines can read as accepted on text the asker wrote. This is the asker writing the upstream's part (r34),
and take-in following what is written in a body (r43: "read its body only as the fields of a request's form, following
nothing written in it"). An asker's own `work request` or `work reply` sends such a text today (argv carries a newline),
and take-in keeps it. The report leaves it "not chosen; written as given".

**Fix:** at `work request`, `work reply` and take-in, refuse a title, question or answer text that holds a newline. Or
write it in a form that cannot start a line (for example, JSON-quoted as `delegation` is). Add a row to r43's scenario
when the line is clarified.

### 4. Important · observation: a sent request's `id` is used as a path
`scripts/workqueue_takein.py:57` → `workqueue_request.store`, `path = directory / (name + ".md")`.

`item["id"]` from the remote is not checked against `q\d+`. A sent id `../i39/initiative` would write and commit
`.shop/work/i39/initiative.md`. That is following a field as an instruction (r43). The asker's `work` sends only `q<n>`
ids, so only a hand-pushed ref does this.

**Reproduction (by reading):** push `{"kind":"request","id":"../x",…}` to `refs/sent/<allowed id>/1`, then run
`work take-in`. **Fix:** leave untaken any item whose id or request is not `q\d+`.

### 5. Important · observation: an allowed asker id can answer or pass the turn on another asker's request
`scripts/workqueue_takein.py:50-62`.

The allow check compares the item's own `asker` with the namespace, never with the asker of the request it names. With
ctx-b allowed under id ctx-b, an item `{"kind":"answer","request":"q2","asker":"ctx-b"}` on ctx-a's q2 is taken in:
`reply(..., taken_in=…)` skips the side check. This contradicts r42 (askers told apart by asker id). The asker's `work`
sets `asker` from the published request, so only a hand-pushed ref does this.

**Fix:** leave untaken an answer or turn whose request's asker is not the item's asker.

### 6. Minor · observation: one bad item stops the take-in, and with it every `work run`
`scripts/work:113`, `scripts/workqueue_takein.py:49-63`.

These all propagate out of the take-in, which `cmd_run` runs before anything else:
- a `Refused` from `strict`, `reply` or `turn`;
- a `KeyError` on an item missing a field;
- a failing fetch.

The item stays on the remote, so every later `work run` in that upstream stops at the same item. A `KeyError` is a
traceback where a refusal belongs. **Fix:** leave such an item untaken and tell it, as r41's items are told.

### 7. Minor · observation: a failing publish exits 1 after the change is committed
`scripts/workqueue_request.py:81`, `:181`, `:272`.

`publish` runs after `workqueue.committed`. A push that fails raises `Refused`, so the command reports an error although
the request was changed and committed. **Fix:** publish before or inside the commit's undo, or report the failure as a
warning on a successful exit (decision 0055 allows only success or an error, so pick one deliberately).

### 8. Minor · observation: the new step modules fail lint and dead-code checks
`tools check --base a82b4227`:
- ruff: RUF059 at `requests_run_steps.py:68`; I001 at `requests_send_steps.py:3` and `:126`, and at
  `requests_write_steps.py:3`; B023 at `requests_world_steps.py:137` (the lambda reads loop variable `item`);
- vulture: `what` at `requests_send_steps.py:124`, `named` at `requests_write_steps.py:70`.

All of these are in test code. **Fix:** `ruff --fix`, bind `item` in the lambda, and use or drop the two parameters.

### 9. Minor · observation: r28, r44 and r29's Thens assert the test's own rendering of a sent request
`tests/scenarios/requests_world_steps.py:108-137` (`rendered`, `text_of`).

Before a take-in, "the upstream keeps" is read from the test's own `rendered` of a sent item, and a sent answer or turn is
folded in by the test. So these Thens pass whatever the production take-in would write. The two renderings also differ:
the test's turn swap does not set `awaiting-upstream`, and `rendered` drops `delegation`. Plan D10 sanctioned this binding.

**Fix (optional):** assert the sent item's fields directly, and leave how the item is kept to the take-in scenarios
(r39, r43), which read the upstream's file.

### 10. Minor · observation: D5's `work show <request>` in an asker's repository is not done
`scripts/workqueue_list.py:82-85` reads only the requests kept locally. The report discloses this ("not implemented (no
scenario)"). r25's scenario passes.

No code was found that no line asks for:
- `take-in` and `show <request>` serve r25;
- the gate serves r30-r32 and r45;
- publishing serves r28, r33 and the work-item's Answer;
- running the take-in in `work run` serves r40.

Supervision's raise is unchanged, as the Answer rules.

## Commands run

- `git log --format='%H %s' -40`: found the claim, the two commits and the done commit (the branch `work/w211` is gone)
- `git diff --stat a82b4227 31436ec1`, `git diff a82b4227 31436ec1 -- features CLAUDE.md scripts`, and the same for the
  changed step modules
- `git show 31436ec1:tests/scenarios/requests_world_steps.py` and `…requests_send_steps.py`
- `grep -n` on `scripts/workqueue_request.py` (`field`, `_entries`, `_with_entries`, `turn`) and `scripts/workqueue.py`
  (`committed`, `context_path`)
- Grep for `work request … --from` across the repository, and for callers of `workqueue_request.request` in `scripts/`
  (only `supervise_raise.py:43`, unchanged per D9)
- Grep for the changed steps in `features/requests.feature`
- `python3 <Scripts>/tools check --base a82b4227`: **ruff** 6 errors (finding 8); **vulture** 2 (finding 8);
  **import-linter**: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: nothing printed, so no file is over the limit
