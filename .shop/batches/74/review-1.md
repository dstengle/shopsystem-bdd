---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-74/review-1
kind: review
batch: batch-74
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/98
head: 65c3f3eab258bb8c4c8afa636cdc37f6004325de
range: 967e36f983bf9e0f14f5f3144c3fee0c56ea0f74..65c3f3eab258bb8c4c8afa636cdc37f6004325de
result: fix-now
---

# batch-74 review 1

## Verdict

The batch builds r57, r59 and r60. It builds r58 only in a context with a domain model. Without one, `work accept` writes a term bullet the lexicon cannot read, and the scenario passes only because it checks the item's text. One finding to fix, and one failing check to fix.

## Findings

### f1 Important fix now: without a domain model, an accepted term proposal writes a term bullet the lexicon cannot read
- item: b42
- where: scripts/request_terms.py:101
In a context with no `spec/model/`, `into_item` appends each vocabulary entry as it stands to the capability block's `terms`, for example `- **shelf** (noun) → object shelf. A place ...`. A capability block's term bullets are read by `spec_lexicon.ENTRY`, which requires `- **<term>** (<part of speech>): <text>`. A bullet with `→` and no `:` reads as no entry. `work line --term` refuses this exact bullet for that reason:

```
if spec_lexicon.entry(bullet, capability) is None:
    raise Refused("work line: the term bullet %s is not a term entry `- **<term>** (<part of speech>): "
```

(scripts/backlog_lines.py:149-151). So the item does not hold the term as a term, which r58 asks for: "keep an item that holds every term that the term proposal concerns". The bullet is also a lexicon problem for the readiness bar once the item is checked.

The r58 scenario takes this path: readiness_world's `codify` writes a spec with no `spec/model/`. Its Then only looks for the substring `**shelf2**` in the item file (tests/scenarios/requests_handlers_terms.py:182), so it passes. tests/scripts/test_request_terms.py:56-61 asserts the unreadable bullet as the expected result.

Fix: in the branch without a domain model, write each entry in the capability term form (`- **<word>** (<part of speech>): <definition>`, checked with `spec_lexicon.entry`), or refuse the accept naming the proposal. Then make the scenario's Then and the unit test check that the item's block holds a term entry the lexicon reads.

### f2 Minor fix now: `tools check` fails at Head; vulture flags backlog_lines.py's re-exported `ids`
- item: b42
- where: scripts/backlog_lines.py:31
`tools check --base` exited 1 at Head and 0 at the base:

```
== vulture ==
scripts/backlog_lines.py:24: unused import 'ids' (90% confidence)
```

The import has been there all along. It carries `# noqa: F401`, which ruff honours and vulture does not. It shows up now because renaming `_block` to `block_of` puts backlog_lines.py among the files the check reads. Fix: get the review check back to exit 0. Either mark the re-export so vulture reads it as used (for example list it in `__all__`, or add a whitelist entry), or reach `_block` without renaming it in backlog_lines.py.

### f3 Minor observation: an entry whose definition contains " - **" is split into two entries
- item: b42
- where: scripts/request_terms.py:31
`entries` splits on `\s+(?=- \*\*)`. A definition that quotes another bullet, such as `... like - **book** (noun) ...`, is cut in two. Then `check` either refuses a proposal that conforms, or keeps two entries where one was meant. No client sends this today. Reproduction: `request_terms.entries("- **shelf** (noun) → object shelf. Unlike - **book** (noun) here.")` gives two entries.

### f4 Minor observation: a line given to `work propose` that opens with "- **" is treated as a term proposal
- item: b42
- where: scripts/request_terms.py:22
`is_proposal` tells a term proposal from a requirement only by the prefix `- **`. A line given through `work propose --line` with that prefix skips grammar 4 at `work outcome` and is checked against the vocabulary-entry form instead. At `work accept` it becomes terms, not a requirement. Nothing sends such a line today. A field on the line, or the `suggest` step that kept it, would tell the two apart without guessing.
