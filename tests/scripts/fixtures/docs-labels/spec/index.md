---
id: bounded-context/example.org/acme/labels
title: labels
language: codified-2
imports: [cli]
---
# labels

The context of docs/recipes.md's labels: an item, the term `label` and its relation row as the recipe "Add a word to
the glossary" lays them, the verb `tag` of its frame, and the capability of "Start a new capability" with its line.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| label | of | item | many |

## Glossary
- **the person** (proper noun): the human at the terminal. Kind of: agent.
- **`work`** (proper noun): the backlog's tool. Kind of: tool.
- **item** (noun): one file of the backlog: work this bounded context may do.
- **label** (noun): a short word the person gives an item, to group it with others. Kind of: text.
- **text** (noun): words written down.
- **tag** (verb, action): a tool gives an item a label. Forms: tags, tagged. Frame: tool tags item with label.
- **commit** (verb, action): a tool records a file in git. Forms: commits, committed. Frame: tool commits item.
