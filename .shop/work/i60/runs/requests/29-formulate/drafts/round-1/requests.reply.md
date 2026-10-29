I wrote one new scenario for r72 and raised no questions.

## Coverage

| line | scenario | tag |
|---|---|---|
| [r72] | a session the person gives a delegation for a request writes it, in the same reply, through delegate as the person's words with the date | @r72 |

## How the scenario reads r72

- The response: in its reply to the person's message, the session runs `work delegate`, giving q1 and the delegation `'The person, 2026-10-29: "answer any question on line 1"'`. When that reply ends, the request holds that delegation.
- It reuses these steps from r65, r66 and r71:
  - "a request q1 from the asker ctx-a whose turn is the upstream's, with one line that has no line outcome"
  - "q1 holds no delegation"
  - "q1's delegation is ..."
  - "`work delegate`, giving q1 and the delegation ..."
- The only new step is the When step: the person tells a session, on a date, a delegation for q1.
- The text `The person, <date>: "<words>"` follows the example in the brief. r72 itself does not fix this format; it says only "the person's words with the date". So the scenario pins this one format.

## Questions

None. r72 has one reading here. "The date" is the day the person gives the delegation. Since the session writes it in the same reply, that is also the day it is written.

## Cases no line mentions

- A reply that runs past midnight: the date the person gave the delegation and the date `work delegate` runs are then different days. r72 does not say which one is written.
- The format of the person's words with the date. If the steps need a fixed text, that text is a line r72 does not give.
- The person gives a delegation for a request that is `delivered`, `refused` or `withdrawn`. `work delegate` refuses it (r68), and no line says what the session then does in its reply.
- The person's words are empty. `work delegate` refuses them (r67), and no line says what the session tells the person.
- The person gives a delegation in a session that is not in the upstream's repository. r70 covers whose turn it is, but no line covers which side's session writes it.

## Drafts

- /tmp/work-run-i60-bt1kpp_i/requests-29-formulate/.shop/scratch/29-formulate/drafts/round-1/requests.feature
- /tmp/work-run-i60-bt1kpp_i/requests-29-formulate/.shop/scratch/29-formulate/drafts/round-1/requests.reply.md
