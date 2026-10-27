# supervision: formulation, round 1

## Coverage

| id | line | scenario |
|---|---|---|
| supervision#r135 | "**When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation." | the lines an integrate round gives into an upstream are raised with `work request`, raised for the request the initiative fulfils and with its delegation |
| supervision#r136 | "**While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised." | none: returned as a question below |

Every other line is already formulated and stays as it is.

## Questions

- supervision#r136: "**While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised." When the initiative has more than one capability-proposal, which ones are held?
  - Reading 1: every capability-proposal the initiative's integrate round wrote is held, because the raised lines came from that round and not from one proposal.
  - Reading 2: only the capability-proposal the raised lines belong to is held, and the initiative's other proposals get their work-items. r135 does not say how raised lines are tied to one proposal, so this reading needs that link stated.

## Cases no line mentions

- r135: the request the initiative fulfils gives no delegation. Is the raised request written with no delegation, or is it refused?
- r135: one integrate round gives lines into two different upstreams, or two sets of lines into one upstream. Is that one request per upstream, or one per set of lines?
- r135: the asker the raised request is written with (`--from`) is not named.
- r135: `work request` refuses the raised request, for example because the upstream is not registered. Nothing says what `work run` does then.
- r136: a raised request that is `refused` or `withdrawn` is never `delivered`. Read literally, the proposal's work-items are never drafted, and nothing says what happens to it.
- r136: nothing says whether the work-items are drafted on the next `work run` after the raised request becomes `delivered`, or whether the current run waits for that.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/features/supervision.feature (the r135 scenario, to go after the @r92 scenarios and before @r107)
