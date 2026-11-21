---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-21-a-plan-to-publish-contracts-between-bounded-contexts
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-21
---

# A plan to publish contracts between bounded contexts

## 4. Publishing contracts between contexts

**What already works**, tested in `contracts/down-skeptic/`:
- A downstream copy of the upstream spec parses an upstream request: `request(e1, journal.write, …)` with `param(e1, title, some)`.
- `spec logic` finds L1 across the two contexts (`journal#r3 completes the request and notes#r2 refuses the request`, 235 ms) and L8.
- `features generate` writes both features (96 ms).

**What blocks:**
- **The copy is read as the downstream's own.** `spec check` reports `id 'capability/example.org/notes/notes-cli/notes' is not '…/journal/notes'`, and v_s3 until features are generated.
- **Every upstream operation would raise v_a1** in a downstream with its own `cli.toml` (`adapter_cli_check.py:60`, read only).
- **Packs carry no operations** (`spec_rgl_vocab.py:143-144`). So vocabulary-only packs are rejected: upstream verbs would read as plain events.
- **There is no outbound request construct.** "shall add a note with the title" is refused at `with`, and "shall request the notes service" at `request`.
- **The refusal does not say a verb is outside the contract.** "archives" is refused only because the word is not in the vocabulary. A verb that is in the vocabulary but names no upstream operation would parse silently. So a check is needed that a trigger's verb names an upstream operation.

**Approaches weighed:**
1. A vocabulary-only pack. Rejected: it carries no operations.
2. Copying the spec as the downstream's own. Breaks on capability ids and v_a1.
3. **Recommended:** a published contract, the file layout of b348's existing `contract` object.
   - b348's `holds` relation already lists the parts: domain model, terms, requirements, decisions, data schemas, interface contract. New content: `operations.json`, `contract.toml`, and the logical forms.
   - The downstream reads it as an upstream layer that is excluded from v_a1. Choose between that exclusion and a v_a8 rule, not both.
   - Downstream reliance lines that trigger a verb naming no upstream operation are flagged "not in the contract → raise a request". That falls back to the existing `work request` / `work propose` flow.

**Items in order:**
1. Two `work decision`s: the contract file format, and that an upstream layer is read but not owned.
2. Read the upstream layer: capability ids accepted, v_s3 handled, v_a1 skipped. **This is the first build item.**
3. Reliance capabilities with a grouping report, plus the check that a trigger verb names an upstream operation.
4. b348 (publish, fetch, obtain: r1–r17), with a new line extending r15 to refuse publishing while v_a problems stand. Withdraw b28 into b348; its notes ask for exactly this.
5. `work propose --requirement <cap>#r<n>`, size XS. `work request --from` already means the asker, and `work propose --line` already carries lines.
6. Docs and a two-context example.

Completion:
- the outbound request construct;
- b426, b358, b357 (core driver, handlers keyed on operations, the envelope on every command);
- b366, b355, b380 (HTTP port);
- reliance scenarios against the pinned port;
- `compat.lp` with `spec contract diff`;
- consumer-driven checking.


## Its items, not filed until the person's review

- Contract decisions: the published contract's file layout, and an upstream layer that is read but not owned | Two `work decision`s, the first step of the contracts plan. The layout of b348's `contract` object (`operations.json`, `contract.toml`, logical forms, terms, requirements). An upstream layer is parsed and checked but never renumbered, generated or adapted by the downstream. | 4/3/XS
- spec reads an upstream contract as a layer, not as the downstream's own | The one blocker the two-context test showed. A copied upstream gives a capability-id file problem and v_s3, and by code read every upstream operation raises v_a1 (`adapter_cli_check.py:60`). Read `spec/upstreams/<id>/` as a layer that brings operations (packs carry none, `spec_rgl_vocab.py:143-144`), excluded from v_a1 and from feature generation. | 4/3/M
- Reliance lines checked against the upstream's operations | A downstream line whose trigger verb names no upstream operation, or that is not entailed by the contract, is flagged "not in the contract: raise a request", with a report grouping reliance lines by operation. Today an unknown verb ("archives") is refused only as an unknown word, and a known verb with no operation parses silently. | 3/3/M
- work propose --requirement <cap>#r<n> | Takes a live line into a request by its id. `work request --from` already means the asker, and `work propose --line` already carries text. | 2/2/XS
- Outbound request construct | A response that requests an upstream operation with parameters ("shall request the notes service to add a note with the title") is refused at `with` and at `request`. Add the construct to grammar 4, the logical form and facts, so downstream lines can state what they call. | 3/2/M
- spec contract diff with compat.lp | Classify a new contract version against the old one (breaking or compatible, per operation, parameter, outcome and requirement) and name the downstream lines each change affects. | 2/1/M
- Docs and a two-context example of a published contract | A notes upstream and a journal downstream under `docs/examples/`, walking through publish, obtain, reliance lines and the fallback request, checked by `test_docs`. | 2/1/S
- Existing items to use rather than file:
  - b348: implement it for publish, fetch and obtain, and add the r15 extension above.
  - b28: withdraw into b348.
  - b447: merge b351 into it.
  - b350 and b446: withdraw one of them.
  - b44, b48, b355: give them lines or move them back to idea.
  - b281: add the details of a merge.
  - b394: no remote or gh.
  - b341: second capability block.

## The verified contracts report

# How to publish contracts between bounded contexts (skeptic's corrected version)

I re-ran the four claims the recommendation stands on: parsing against the upstream's vocabulary, L1 and L8 across both contexts, the refusals that motivate steps 8 and 7, and what operations a pack can carry. All four held, with two corrections to how they were read. Separately, the item table overlaps existing items and commands more than the report said. Steps 4, 5 and 7 need to be re-scoped, and the ranking needs to change.

**How I tested.** I copied the scratch downstream to `/tmp/claude-1000/-home-vscode-shopsystem-bdd/d0999860-a5ec-42eb-b649-f0728fe0f332/scratchpad/wf-next/contracts/down-skeptic` (it has no git remote) and re-added journal r3 there. All tools ran from `main`'s `scripts/`. Nothing was written in the repository, and no `work batch` command was run.

## 1. What exists today

- **Sizes held** (verified):
  - `spec/adapters/cli.toml` has 1031 lines.
  - `grammar/packs/request.md` has 30 lines.
  - `spec/capabilities/*.md` has 410 live lines (`grep -c '^- \[r[0-9]*\]'`).
  - `grammar/corpus/spec` is 158K.
- **Ports held** (verified):
  - v_a1 to v_a4 are computed in Python, in `scripts/adapter_cli_check.py:53-78`. The v_a1 loop is at line 60, `set(ops) - set(contract.operations) - set(contract.unexposed)`.
  - In `scripts/model.lp`, v_a3 and v_a4 only pass through `adapter_problem`. v_a5 is a clingo rule at :450 and v_a6 at :454.
  - The rest-contract record holds `generate_schemas.py`, `http-adapter.openapi.yaml`, `check_adapters.py` and `schemas/`.
- **Decisions held** (verified). The files exist: 0084, 0092, 0097, 0098, 0099, 0101, 0103, 0104, 0107, 0110, 0111. Two wordings needed fixing:
  - 0099's file is named "github-issues-carry-context-requests". The "replaceable driven port" wording is in its summary.
  - 0107 says "the grammar is no part of a context", not "the grammar is the same in every context".
- **Backlog statuses held** (verified with `work names`):
  - b28 "Tell another context what this context can do" (idea)
  - b348 "A bounded context asks another for its context: its glossary, capabilities and lines, without a request for new behaviour" (idea)
  - b42 "Negotiate new glossary terms between contexts and with the product" (shaped)
  - b355 "the adapter contract commands: write spec/adapters/<port>.toml's operation tables by command" (shaped)
  - b357 "the envelope on every command: every command prints the response envelope under --json and calls its core function by business name, not only those a scenario requests" (idea)
  - b358 "the scenario handlers keyed on the operations: requested.legacy's re-keying replaced by handlers keyed on (WhenRequests, <service>.<operation>) that drive through driver_cli and check the envelope" (idea)
  - b366 "data schemas made from the domain model and the HTTP adapter's OpenAPI document checked against it, as plugin commands" (idea)
  - b380 "batch_start.unlay_lines re-annotates the adapter contract" (idea)
  - b426 "A core driver runs the generated scenarios against the service's operations in process, not through a port adapter" (idea)
  - b445 "The readiness bar's copy reaches the adapter's program, so v_a3 does not fire before and after every lay" (idea)
  - b13 "An item proposes a new capability or a glossary term" (idea)
- **b348 is further along than the report credits** (verified in `.shop/backlog/b348.md`):
  - Its `contracts` capability already has r1-r17, with publish, fetch and obtain, versions, `published` and `superseded`, refusal with no channel (r11), and refusal of a published version (r14).
  - Its model block already says a contract "holds → domain model | term | requirement | design-decision | data schema | interface contract".
  - So the contents in §3.1 are mostly b348's existing model, not new design.
  - b348's notes raise **no open format question**. The claim that step 1 "settles b348's open format question" is **struck**. Step 1(a) fills a gap b348 leaves (what the files look like); it does not answer a question someone asked.
  - r15 refuses publishing while a requirement does not conform to the grammar. It says nothing about v_a or v_p problems, so "r15 extended" is a new line, not an existing one.

## 2. The two-context test

| Probe | Result now |
|---|---|
| `spec --root . parse --form "When the person writes an entry with a title, the journal service shall add a note."` | Parses. The trigger is `request(e1, journal.write, …)` with `param(e1, title, some)`. The response is `add(e2, subject: x3, object: x4)`, a plain event. **(verified)** |
| "… shall add a note with the title." | Refused: `does not parse at with (token 18 of 21)`. **(verified)** |
| "… shall request the notes service." | Refused: `does not parse at request (token 15 of 19)`. **(verified)** |
| "When the journal service archives a note, …" | Refused at `archives (token 5 of 16)`, with `nearest words: (none)`. **(verified, but read wrongly in the report; see below)** |
| `spec logic` with r3 added (my copy) | Prints `L1 journal#r3 and notes#r2 clash: … journal#r3 completes the request and notes#r2 refuses the request`, plus an L1 between journal#r3 and r4 and the L8 below. Took 235 ms. **(verified)** |
| `spec logic` in the original copy | Prints `L8 journal#r4 says nothing other requirements do not: Then 1 by notes#r2`. It prints no `unread` line, so r5 was read and not entailed. **(verified)** |
| `features generate` | Wrote `features/journal.feature` and `features/notes.feature` in 96 ms. @r1 says "Then the journal service adds the note n1". **(verified)** |
| `spec --root . check` | **Corrected.** The original copy now shows **one** problem, not three: `file: spec/capabilities/notes.md: id 'capability/example.org/notes/notes-cli/notes' is not '…/journal/notes'`. The v_s3 findings on notes#g1-g4 go away once `features/notes.feature` is generated. So the copy-as-own breaks only on the capability id, plus v_s3 until features are generated. **(verified)** |

**Correction on "archives".** The "may follow" list is `add, change, complete, fail, keep, list, name, notify, refuse, remove, return, start, write`. That is every verb in the vocabulary, including the request pack's (complete, fail, notify, refuse) and journal's own `write`. It is not a list of the upstream's operations. The refusal only says "archive" is not a word here.

This signal does not mean "not in the contract". A verb that is in the vocabulary but names no operation would parse and read as a plain event. Telling "not in the contract" apart needs a check that a trigger verb names an upstream operation. **Step 6 has to add that check.**

**Code reads held:**
- **Packs carry no operations** (verified). At `spec_rgl_vocab.py:143-144`, operations come only from `domain_model.load(root)` when `domain_model.exists(root)`, so a vocabulary-only pack would read upstream verbs as plain events.
- **Every upstream operation would raise v_a1 in a downstream with its own `cli.toml`** (verified, read only, not run). It follows from the line-60 set difference, which subtracts only the contract's tables and `[unexposed]`.

**Five gaps.** Gaps 1, 2 and 4 held. Gap 3 (publish and obtain) is already specified by b348 r1-r17; what is missing is the implementation and the file format, not the item. Gap 5 is b426, b358 and b357.

## 3. Design

Kept as written, not re-run, with these corrections:

- **§3.1:** present it as the file layout of b348's existing `contract` object. Its `holds` relation already lists the parts. The new content is `operations.json`, `contract.toml` and the logical forms.
- **§3.3 step 4, "Not promised":** it must also flag a line whose trigger verb names no upstream operation (see the "archives" correction above). Without that, a verb that is in the vocabulary but has no operation passes as "not promised" instead of "not in the contract".
- **§3.3 step 6:** `work request --from <cap>#r<n>` **collides with an existing option.** `work request --help` shows `--from ASKER  the asker: this context, its default (r111)`. Lines also already go into a request with `work propose <request> --line "<text>"` (repeatable). What is missing is only taking a line by its id. Make it `work propose --requirement <cap>#r<n>` (or let `--line` take an id), not a new `work request` option.
- **§3.4:** step 2 (the upstream layer skips v_a1) and the new v_a8 (a port operation of an upstream area is a problem) overlap. Pick one: either the layer is excluded from the operations v_a1 reads, or v_a8 is the rule. Keep v_a8 only if the downstream can declare a port for an upstream operation at all.

## 4. Steps, corrected

| # | Item | Correction |
|---|---|---|
| 1 | Two `work decision`s | Keep. Drop "settles b348's open format question". |
| 2 | Upstream layer read | Keep it as the **first** build item. It is the one gap the test shows blocking (the capability-id file problem and v_s3; v_a1 by code read). |
| 3 | v_a1 and v_a2 into clingo, v_a7, v_a8 | Not needed for the minimum. Merge v_a8 with step 2. Run it with b366 and b355. |
| 4 | `spec contract publish` | **Not a new item: implement b348** (r1, r4, r14, r15, r17), extending its r15 with a line about v_a problems. b28 is subsumed: its notes ask for exactly this (quote-39). Withdraw it into b348 or depend b348 on it. |
| 5 | `spec contract obtain` and `fetch` | **Part of b348** (r7, r9, r10, r11, r16), not new. |
| 6 | Reliance capabilities and the grouping report | Keep, and add the "trigger verb names no upstream operation" check. |
| 7 | `work request --from …` | **Re-scope.** The `--from` name is taken. `work propose --line` already carries lines. A new item is only "`work propose` takes a requirement id". Size XS. |
| 8 | Outbound request construct | Keep. The refusal at "with" is verified. |
| 9 | Core driver, operation-keyed handlers, envelope on every command | Already filed: b426, b358, b357. |
| 10 | HTTP port | Already filed: b366, b355, b380. |
| 11 | Reliance scenarios against the pinned port | Keep. |
| 12 | `compat.lp` and `spec contract diff` | Keep. It is new, with no existing item. |
| 13 | Docs and a two-context example | Keep. |
| 14 | Consumer-driven checking | Keep, as a later step. |

**Ranking, corrected.** The evidence supports this order:

1. Step 1, then step 2. Only the capability-id check (and v_s3 before generation) blocks a copied upstream today; parsing, L1, L8 and generation already work.
2. Step 6, with the operation check.
3. b348, which is steps 4 and 5.
4. The XS `work propose --requirement` item.
5. Step 13.

The report's "minimum is steps 1-7" counts steps 4 and 5 as new work and step 7 as a new command. Both are wrong: steps 4 and 5 are an existing item (b348), and step 7 is mostly an existing command (`work propose --line`). Steps 8-12 stay as the completion, with 9 and 10 already filed.

## Alternatives weighed

Kept as written (not re-run). The rejection of vocabulary-only packs is verified (`spec_rgl_vocab.py:143-144`).

## Files

- Original scratch downstream: `/tmp/claude-1000/-home-vscode-shopsystem-bdd/d0999860-a5ec-42eb-b649-f0728fe0f332/scratchpad/wf-next/contracts/down/`. Note that its spec and feature files are untracked; it has only the `migrate init` commit.
- My re-run copy, with r3 added: `/tmp/claude-1000/-home-vscode-shopsystem-bdd/d0999860-a5ec-42eb-b649-f0728fe0f332/scratchpad/wf-next/contracts/down-skeptic/`.
