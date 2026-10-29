## Coverage

| id | line | scenario |
|---|---|---|
| r211 | "**When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started." | Scenario Outline: `work run` reads the delegation the request has when it reads it, the delegation given <when> the initiative started (Examples: before, after) |

Every other line of spec/capabilities/supervision.md already has its scenario in features/supervision.feature. This draft adds only r211.

## Questions

None. r211 has only one reading.

## Cases no line mentions (no scenario written)

- A request whose delegation is replaced with different words while the initiative is under way. The line does not say whether a question already given to a session under the old words is answered again under the new ones.
- A request that has a delegation when the initiative starts and none later. The line does not say whether questions still waiting are then left for the person.
- A delegation given while a `work run` is already running. The line does not say whether "at that moment" means each time a question is given to a session, or once when the run starts.
- No line names a command that gives or changes a request's delegation after the request is written. requests r19 only writes it at `work request`, so the step "given after i1 started" names a state of the world, not a command.

## Drafts

- /tmp/work-run-i60-sk55gsmk/supervision-5-formulate/.shop/scratch/5-formulate/round-1/supervision.feature
