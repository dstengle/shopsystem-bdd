# Audit: grammar 4 on migration-tools, telemetry, batch-measurement (b156)

Sources: the 39 grammar-4 lines on b156 (migration-tools r26-r55, telemetry r5-r8, batch-measurement r23-r27). They replace every live line of the three capabilities. spec/ still holds only the codified-1 lines, and no other item has added grammar-4 lines here. I also used phase 3's d.tsv candidates and its section "What the candidate form cannot say". To check each line, I laid b156 over a copy of spec/ (`backlog_lines.lay`) and ran `model parse --form` on all 39 lines. Every line parses to one form (forms.txt). work ready still refuses g28/g29, which is b236 (features generate picks the wrong frame of supersede).

## Counts

| verdict | lines |
|---|---|
| fine | 4 (migration-tools r26, r27, r38; telemetry r7) |
| distortion | 30 |
| coined | 4 (migration-tools r31, r32, r33; telemetry r5) |
| unsayable | 1 (migration-tools r30) |

The rewording did take out the coined adjectives (unmigrated, ledgered, idle, shopless and the rest). But most of them were swapped for a different kind of workaround: a value that stands in for a comparison, a verb that does the same, or a proper noun that stands in for a string.

## Missing constructs (one line can lack several)

| construct | lines | where |
|---|---|---|
| COMPARE on ordered versions (release before/after X, equal to or newer than the plugin's own) | 16 | migration-tools r36, r39-r48, r51-r55 |
| QUOTED CONSTANT (a printed string or a fixed literal, as opposed to a parameter) | 6 | r37, r41, r44, r46, r50, r55 |
| VALUE SET ("status is one of …", or open/live) | 4 | r48, r52-r54 |
| COUNT as a noun phrase ("the number of Ks") | 4 | batch-measurement r23-r25, r27 |
| AGGREGATE (max+1, sum over rows, count by grade) | 4 | r31, r32; telemetry r6; batch-measurement r27 |
| ANOTHER (a distinct second referent of the same kind) | 2 | r28, r29 |
| PLURAL / EACH-ITS in a trigger ("on two batches … the measurement of each") | 2 | telemetry r8, batch-measurement r26 |
| ARITHMETIC (ratio, second over first) | 2 | telemetry r8, batch-measurement r26 |
| DEFAULT (a value an absent thing is taken to have) | 2 | r37, r43 |
| WORD SENSE (gloss widens a common word) | 2 | r34, r35 |
| ATTRIBUTE ON A RELATION ("supersedes in part") | 1 | r30 |
| COUNTERFACTUAL / plan state ("would relocate") | 1 | r33 |
| NP LIST hidden in a noun | 1 | telemetry r5 |
| NECESSITY / disjoint states (needed to say "print nothing") | 1 | r49 |
| REFLEXIVE (compare a measurement with itself) | 1 | batch-measurement r27 |

The release attribute alone accounts for 16 of the 30 distortions. Its values `0.23.1`, `0.24.0`, `0.29.0` and `1.0.0` each stand for a range of releases, and `own` and `newer` stand for comparisons with the plugin's own release. The lines mean what they should only because of the glosses on those values. Then **lack** ("a repository is on a release before the release of an upgrade step") is a state verb that stands in for a comparison. This is exactly the bend the person ruled out.

## Worst examples

1. **r55** (was unframed): "While this repository lacks the verb-frames step and this repository does not lack the simplified-workflow step, …". The line is meant to say "release after 1.0.0 and before 3.0.0". Here it is said as a double negation over proper-noun steps and a coined verb. In the form, `spec/index.md` and `v_t11` are parameters, so the line reads "rewrite any file and print any code".
2. **r30** (was qualified): its response is word for word the same as r29's. The rule that is specific to "in part" (supersedes keeps only the id, and the superseded entry's decision stands alone) is not said at all. The qualifier is attached to the entry rather than to the supersedes relation. Unsayable.
3. **telemetry r8 / batch-measurement r26**: "on batches" / "on measurements" parse as a single referent (`run(…, on: x3)`). So "compare two things side by side" becomes "print the measurement of one thing and a ratio". The plural is lost without a warning, which comes close to the anti-goal of a line with two meanings where one is picked silently.
4. **r33** (was conflicting): "destination" is glossed "the path `migrate run` relocates a file to or writes a file at". The counterfactual "would relocate" has moved into a noun. The line is correct only through that gloss.
5. **telemetry r5**: "every figure of the batch". Figure is glossed as the four figures that `measure batch` gives, so the list has left the line and the definition is circular.
6. **r44**: `@deprecated` is a parameter in the form, so the rule reads "a scenario that has any tag".
7. **r31, r32**: "next number" and "next id" hide one-above-the-highest (an aggregate) inside a noun.

## Fixable by rewording alone

- **r34, r35**: say "an uncommitted change" instead of the widened "untracked file".
- **telemetry r5**: give the four figures as attributes of the batch and list them in the line (grammar 4 has lists). Then drop "figure".
- **telemetry r8, batch-measurement r26**: "on two batches … the measurement of each of the batches". Call 4's "each of the Ks" and the count "two" exist. The ratio still needs arithmetic.
- **r48**: tie the initiatives to this repository ("no initiative of this repository …").
- **r52**: "a frozen request whose asker is not this bounded context" in place of the glossed noun "peer request".
- **r37**: possibly as a necessity line ("a repository that has a shop directory and no plugin version file always has the release `0.23.1`"), if the attribute's order allows it. That would also remove the proper noun "the first release".
- **batch-measurement r23-r25**: plural nouns help partly ("a measurement that gives a round trip of a stage"). Printing *the number* of round trips still needs a COUNT noun phrase.

Rewording cannot fix these, because each needs a construct: ordered versions (16 lines), quoted constants (6), value sets (4, unless "or" in While can be used), aggregates and arithmetic (6), "another" (2), relation attributes (1), the counterfactual (1), and the disjointness that "print nothing" needs (1). Ordered versions in the time/compare atoms (`cmp` with an attribute's declared order, as design §6.2 already shows for release) would fix the most lines for one construct. It would also let `lack` and the range-like values be retired.
