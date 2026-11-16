---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-16-backlog-triage
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-16
---

# Backlog triage

The person, 2026-11-16, wants the session to work through the backlog on its own ("You can merge when you need to. Do releases when you need to. Make the calls when I'm not available."), starting with a triage. Six fresh agents each took a slice of the 189 open items (ideas, shaped, needs-input) and checked each against main at plugin 0.35.1: the code, the spec, the delivered items, git log, and where cheap a command on a scratch copy of spec/. Each item got one verdict: withdraw (with evidence written into its notes), merge into another item, shape, chore (work with no behaviour a scenario checks), or needs the person. An agent withdrew an item only with evidence and changed nothing else.

## Outcome

- **Withdrawn, 51:** 46 with evidence (delivered, obsolete with the old grammars, or duplicate): b2, b4, b7, b9, b11, b12, b16, b33 (slice 1); b53, b61, b62, b66, b74, b88, b89, b90, b91, b92 (2); b94, b95, b96, b97, b98, b100, b104, b105, b108, b112, b165, b178, b180 (3); b182, b184, b188, b200, b201, b208, b209, b210, b211, b212, b223 (4); b225, b226, b227, b245 (5). And 5 merged: b311 into b286, b312 into b300, b313 into b292, b195 into b190, b70 into b68.
- **Needs the person, 19:** b3, b20, b24, b27, b28, b32, b50, b64, b101, b102, b124, b127, b172, b179, b181, b185, b228, b241, b294.
- **Shape, about 60:** behaviour lines can state. Notable: b310 (a reproducible crash of the unread check on "every K is not v" in a While, which can break `work ready`), b303 (migrate upgrade records the version; must retire migration-tools r81), b300/b301/b302 (orders on any act), b203 (worse than written: `work line --universal` with no universal.md writes a `codified-1` marker the tools now refuse), b206 (half done: adjectives of base or pack kinds still give v_t4), b14 and b271 (rewording or dropping lines), b65, b77, b306.
- **Chore, about 45:** docs, skills, module-map rows, test fixes, refactors. Notable: b256 (under pytest-bdd 9 unbuilt scenarios silently stop being xfails), b224/b179 (`model decisions --check` fails today: 3 of 9 check decisions run vocab.py and exit 5), b34 (batch-implementer agent), b248, b289, b75 (batch brief rules), b250-b255 (docs review leftovers).

## Clusters worth one item or one batch each

- Requests on top of b26: b5, b6, b38, b39, b40, b17; request_post.committed's close and view: b68 (b70 in), b71.
- model logic's precision: b232 (missed L1), b233, b314 (false L1s), b187, b192.
- Translation gaps that b306 would catch: b309, b310, b315; b308 (research) before b306's design.
- Counter-examples extending b273: b277, b294, b296, b229.
- Batch workflow: b279, b173 (the same fault: the brief's checks run the base's scripts), b280, b69 (reopen a batch), b281, b282, b289, b304, b72, b194.
- Time and modality in model logic: b190 (b195 in), b191, b196, b189.
- Decisions: b172, b179, b204, b207, b224.
- Contract and docstring drift: b110, b167, b177; module-map rows: b54, b183, b193, b292 (b313 in), which argues for b50's check that every row matches its module.
- Retirement and history: b101, b102.
- Glossary clean-up: b23, b242, b213.

## Defects of delivered items found

b310 (b272/b307's unread reading), b309 and b315 (b274/b297), b290 and b291 (b287/b288), b228 (b216: the glossary's own example "set its status" is refused), b229 and b277 (b273), b230, b232, b233 (b197/b240), b163 (b128), b168, b173, b68 and b71 (b36).

## Dead code seen, unconfirmed

tests/scenarios/design_model_check_handlers_conditions.py's codified-1 branches of `requirement` (untested, avoiding, unparsed, withholding) match no feature step; tests/scenarios/backlog_handlers_upstream.py:50 `refused_naming_task` is unreachable since b61's key is never looked up. vulture cannot see decorator-registered handlers.

The per-item tables (verdict, proposed rating, evidence) are in the session transcript of 2026-11-16; each withdrawn item carries its evidence in its own notes.
