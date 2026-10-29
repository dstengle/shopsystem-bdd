# Plan of w232 (work-queue#r59, #r60, #r61)

## 1. What goes green

- **work-queue#r60**, "list prints each initiative and each work-item under .shop/work/ with its status" (features/work-queue.feature:127): already green in the research run (notes part 1). Under decision D1 below nothing changes for it. It must stay green.
- **work-queue#r61**, "list with --json prints each initiative and work-item with its status as one JSON object" (:138): already green in the run, and it must stay green. D1 leaves the `requests` key in place, so `gives_pairs` keeps working.
- **work-queue#r59**, "show of a request prints its status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution" (:186): **red**. The notes give these reasons:
  - Steps that are undefined, or that nothing matches: the Given at line 188 (request kept in this context, asker this context, delivered, asker's turn). The Givens at lines 189 to 191: outcomes, a question with its answer, a resolution. The `requests_steps.py:78` step needs "each found in", so it does not match line 191. The Thens at lines 194, 195, 196 and 197. At line 195, `prints_pairs` cannot match "line 1 with ...", because its `\S+` takes one word.
  - The code: `scripts/workqueue_list.py:show` (lines 82-85) prints one line, `<name> <status> <turn>`, for a request. It reads none of the sections `## Lines`, `## Outcomes`, `## Questions`, `## Answers` or `## Resolution`.
- Deprecated scenarios retired: none. The work-item has no `## Retires` section, so the @r34 and @r35 deprecated scenarios (:101 and :115) stay. Under D1 they still pass.

## 2. Where the change lands

- `scripts/workqueue_list.py`: the request branch of `show` (text) prints r59's parts: the status, whose turn it is, each line with its line outcome, each question with its answer, and the resolution (each line's requirement id and version).
- `scripts/workqueue_request.py`: a public reader of a request's sections (lines, outcomes, questions, answers, resolution) for `show` to call. It is built on the private `_entries` reader that is already there. The file has 228 lines; it stays under 300.
- `tests/scenarios/work_queue_list_steps.py`: new Given steps for feature lines 188-191 and new Then steps for lines 194-197. Update its docstring to name r59.
- `tests/scenarios/requests_flow_steps.py`: rewrite `show_prints` (lines 95-99) for show output that runs to several lines (see part 4).

Removed from the researcher's set, and why:
- `scripts/work`
- `tests/scripts/test_workqueue_list.py`
- `features/work-queue.feature`

The research gave these three as changing only under reading (b), and D1 takes reading (a).

`scripts/workqueue.py` is also removed. It is on the path but not edited: D2 puts the reader in `workqueue_request.py`, and `workqueue.py` has only 6 lines of room left.

## 3. Decisions

- **D1. Requests stay in `work list`, as text and as the JSON `requests` key.** The research left this open between (a) and (b). It is settled elsewhere:
  - **requests#r50** says "When `work list` is run, `work` shall print each request with its status and whose turn it is". The listing of requests moved to the requests capability; it was not dropped.
  - **design-decision/work-list-and-work-show-replace-work-status** says `work list` lists initiatives, requests and work-items.
  - r60/r61 are silent on requests, and do not forbid them.
  - So `listing`, the `cmd_list` help text, `gives_pairs` and `test_list_json_gives_each_request...` all stay as they are.
- **D2. The reading of a request's sections lives in `workqueue_request.py`, as one public function. `workqueue_list.show` calls it.** This rests on the CLAUDE.md module map:
  - `workqueue_request.py` holds the requests of a context.
  - `workqueue_list.py` holds `work show <target>`.
  - No module outside it calls a private `_entries`.
- **D3. The first line of `work show <request>` keeps its present form, the request's name, its status and whose turn it is.** The parts r59 adds follow on lines of their own: the lines with their outcomes, the questions with their answers, and the resolution.
  - This rests on **work-queue#r59**, which names what is printed but not the layout (the layout is Implementation).
  - It also keeps every reader of that first line working.
  - The turn is said as the asker's or the upstream's turn, so that "that it is the asker's turn" can be read from it.
- **D4. `work show <request> --json` is left as it is (the object with `request`, `status` and `turn`).** r38 is not accepted by this work-item, and r59 is about text. Widening the JSON is left to r38's work.

## 4. Tests the decisions break

- `features/requests.feature:408-413` (@r25 of requests), step `tests/scenarios/requests_flow_steps.py:show_prints` (lines 95-99). It asserts that the whole stdout of `work show <the request>`, split into words, is exactly `delivered asker` after the name.
  - Broken by r59 itself and by D3: the output now runs to several lines.
  - Rewrite: assert that the output's first line gives the request with `delivered` and the asker's turn. Leave the lines after it unchecked. That is still what the step's wording says ("prints that request with delivered and the asker's turn").
- `tests/scripts/test_workqueue_list.py:test_list_json_gives_each_request...`, the deprecated @r34 and @r35 scenarios, and `gives_pairs`: not broken, because of D1.
- I checked the notes' list of sound tests: the initiative and work-item branches of `show` (test_workqueue_list.py lines 32-55) and `requests_show_steps.py:prints_request` (no-target show). D2-D4 touch none of them.
- No test calls `show` of a request with `--json` (notes, by search), so D4 breaks nothing.

## 5. Open cases (for the implementer to name, not to choose)

- **Step matching risk.** `prints_question` is the parse pattern `it prints the question "{question}"`. It may also match line 196 ("... and the answer ..."), because a parse field can swallow `" and the answer "`. The new question-and-answer step must be the one that matches line 196. Check this when line 196 first runs red.
- A line with no line outcome yet: what show prints for it.
- A question with no answer yet.
- A request with no resolution, or one whose resolution gives only some lines.
- A request whose file lacks one of the sections altogether.
- In the upstream's repository, outcomes or questions not yet sent with the turn (requests#r53). This is not accepted here; say whether show prints them as they are.
- Where a request is kept in this context: `.shop/work/requests/q<n>.md`, as `request_with_status` writes it. The new Given at line 188 should write the same form, with the asker set to this context's name.
