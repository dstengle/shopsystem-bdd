---
id: vocabulary/missingmass.io/shopsystem/shopsystem-bdd/measurement
area: measurement
---

# The words of measurement

## Terms

- **compaction** (noun) → object compaction. Claude Code's replacement of a session's earlier messages by a summary, recorded in its transcript.
- **defect** (noun) → object defect. A file of a batch that records a fault in the behaviour of the repository's code, with its reproduction, found by a review or after a merge.
- **stage row** (noun) → object stage row. The figures a measurement gives for one logged stage: its work-item, stage, agent, session and turns.
- **total row** (noun) → object total row. The sums of the figures of a measurement.
- **round trip** (noun) → object round trip. One request of a session to its model and the reply.
- **session row** (noun) → object session row. The figures a measurement gives for one session: its tokens, round trips, tool uses, dispatches and compactions.
- **tool use** (noun) → object tool use. One call of a tool by a session.
- **wall time** (noun) → object wall time. The time from the start of a batch to its close.
- **session time** (noun) → object session time. The time the sessions of a batch spent on it.
- **token** (noun) → object token. A unit of the text a model of a session reads or writes.
- **role** (noun) → object role. What a session did in a batch: planning, implementing, review or fixing.
- **cost** (noun) → object cost. What the tokens of a role cost.
- **ratio** (noun) → object ratio. A figure of the second of two measurements divided by the same figure of the first.
- **reply** (noun) → object reply. The message a dispatch gives back to the session that started it. Plural: replies.
- **include** (verb, state) → relation measurement.includes. A measurement holds a figure or a name. Forms: includes, included. Frame: <measurement> includes <thing>.
- **measure** (verb, action) → operation measurement.measure. Forms: measures, measured. Frame: <actor> measures <batch>.
- **report** (verb, action) → operation measurement.report. Forms: reports, reported. Frame: <actor> reports <defect> in <item>.
- **view** (verb, action) → operation measurement.view. Forms: views, viewed. Frame: <actor> views <measurement>.
- **compare** (verb, action) → operation measurement.compare. Forms: compares, compared. Frame: <actor> compares <measurement>. Frame: <actor> compares <batch>.
- **conduct** (verb, action) → operation measurement.conduct. Forms: conducts, conducted. Frame: <actor> conducts <trial>.
- **the measurement service** (proper noun) → service measurement.
- **hand** (verb, action) → operation measurement.hand. Forms: hands, handed. Frame: <actor> hands <trial> to <session>.
- **compare** (verb, action) → operation measurement.compare. Forms: compares, compared. Frame: <actor> compares <batch> with <batch>. Frame: <actor> compares <measurement> with <measurement>.
- **test run** (noun) → object test run. One run of the tests of a batch when `work` finishes a task of the batch or submits the batch.
- **duration** (noun) → object duration. The time a thing took from its start to its end.
- **opening time** (noun) → object opening time. The time `work` takes to open a batch: its readiness check of the items again, its lay of their lines and its run of their scenarios.
