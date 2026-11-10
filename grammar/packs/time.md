# time

The time pack (the CNL 4 design, section 4.4, I16): the words of time as domain data and as a trigger. A bounded
context imports it with `imports: [cli, time]` in the frontmatter of `spec/index.md`; a word of its own spelled the
same is marked `Redefines: time.` A context's own moments are kinds of moment ("a deadline", Kind of: moment).

The base grammar says the rest (grammar/language.md, "Time"): "after" and "before" between two moments, "within the
last" and a duration, the perfect of an action verb ("has ended") as history, and "since" a moment after it; "the
newest" and "the oldest" of a kind. A duration is a number and a unit of this pack: "7 days", "one hour"; a number
with no unit where a duration is due is refused.

## Glossary

- **moment** (noun): a point in time, a code (`2026-11-10`) or a moment of a thing.
- **duration** (noun): a length of time, a number and a unit.
- **unit** (noun): what a duration is counted in.
- **second** (noun): a unit of one second. Kind of: unit.
- **minute** (noun): a unit of sixty seconds. Kind of: unit.
- **hour** (noun): a unit of sixty minutes. Kind of: unit.
- **day** (noun): a unit of twenty-four hours. Kind of: unit.
- **week** (noun): a unit of seven days. Kind of: unit.
- **schedule** (noun): a moment that comes again, as each day at nine. Kind of: moment.
- **clock** (noun): the agent that tells the time. Kind of: agent. This: the clock of the run.
- **reach** (verb, action): the clock comes to a moment. Frame: clock reaches moment.
