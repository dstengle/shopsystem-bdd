---
id: design-decision/commands-and-agents-answer-in-json
summary: "Every command of the plugin gives one JSON object on stdout, holding `ok` and the fields its capability names, and exits successfully but on a crash on an error it does not handle; every agent replies to its caller with one JSON object of one shape: outcome, summary, files, questions."
date: 2026-10-28
status: proposed
supersedes: [design-decision/query-commands-answer-in-their-output, design-decision/exits-are-successful-or-errors]
source: [request/q25, design-decision/query-commands-answer-in-their-output, design-decision/exits-are-successful-or-errors]
by: "the person, 2026-10-28, accepting q25's lines and answering its questions"
---

# 0074. Commands and agents answer in JSON

## Context

q25 asked whether every command gives JSON by default or only some, whether the commands that print text for a reader or a hook keep a text form, whether check-like commands keep a non-zero exit when they find something, and whether an agent's JSON is its reply or its `result.json`, in a shape per agent or one for all.

## Decision

Every command of the plugin (`work`, `work run`, `measure`, `features`, `model`, `tools`, `migrate`) gives its output as one JSON object on stdout by default. A command that gives text for a reader or a hook (the SessionStart hook's text, Gherkin, `model rules`) gives that text inside a field of the object. Each command's JSON shape is named in its capability: the object always holds `ok`, true when the command did what it was asked and found nothing failing, false when it refused, found a fault, found what it checks for or left a question for the person, with what it found and why.

Every command exits successfully, check-like commands included, whatever it finds; it exits with an error only when it crashes on an error it does not handle. `work run` and the suite read `ok` in place of an exit code, and a check's work is complete when its JSON object holds `ok` true. A Behaviour line, and the scenario that formulates it, still says a command exits successfully or exits with an error, never an exit code; the codes (0, and 1 on a crash) are Implementation.

The reply a session started as an agent gives its caller is one JSON object, in one shape for every agent: its outcome, its summary, the files it names and its questions. `result.json` is JSON already and is unchanged.

## Alternatives

- Every command, check-like ones included, exits successfully but on a crash, and is read by `ok` (chosen).
- Only the commands that refuse or ask the person exit successfully, check-like commands keeping a non-zero exit when they find something: not chosen.
- Text commands keep a text form, by a flag or as their only output: not chosen; their text goes inside a field of the JSON object.
- A JSON shape per agent, or `result.json` as the agent's JSON: not chosen; one reply shape for every agent.
