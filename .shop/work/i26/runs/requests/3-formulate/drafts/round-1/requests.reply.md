## Coverage

| id | line | scenario |
|---|---|---|
| r1 | "When `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>` or with `--thread <id>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id." | request with <given> writes an open request in the upstream's turn with the lines, asker and <where from> given, and prints its id (unchanged) |
| r19 | "Where `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request." | request with --delegation writes the delegation given in the request (unchanged) |
| r2 | "If a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), then `work request` shall refuse, naming the line, and change nothing." | request with a line that <fault> is refused, naming the line, and nothing changes (unchanged) |
| r3 | "If `work request` is run with neither `--source` nor `--thread`, then `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing." | request with neither --source nor --thread is refused, and nothing changes (unchanged) |
| r4 | "`work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question." | outcome writing a line outcome leaves the request's lines and answers as the asker wrote them (changed) |
| r5 | "`work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run." | the asker answering a question leaves the request's questions and line outcomes as they were and writes no resolution (changed) |
| r15 | "When `work outcome <request> <n> <outcome>` is run in the upstream's turn, `work` shall write `<outcome>` as the line outcome of line n." | outcome in the upstream's turn writes the outcome given as the line outcome of the line named (unchanged) |
| r20 | "When the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request." | the upstream asking a question on a line in its turn writes the question in the request (new) |
| r21 | "When the asker answers a question on a request in its turn, `work` shall write the answer in the request." | the asker answering a question in its turn writes the answer in the request (new) |
| r16 | "If a side runs a command other than `work resolve` that writes a part of a request in the other side's turn, then `work` shall refuse, because it is the other side's turn, and change nothing." | a side writing a part of a request in the other side's turn is refused, and nothing changes (unchanged) |
| r7 | "When `work turn <request>` is run, `work` shall pass the request's turn to the other side." | turn passes the request's turn from the <side> to the <other side> (unchanged) |
| r17 | "When `work turn` passes a request's turn to its asker with a line that has no line outcome or a line outcome other than accepted, refused or withdrawn, `work` shall set the request's status to `awaiting-asker`." | turn passing a request to its asker with a line that has <line 2> sets the request's status to awaiting-asker (unchanged) |
| r18 | "When `work turn` passes a request's turn to its upstream, `work` shall set the request's status to `awaiting-upstream`." | turn passing a request to its upstream sets the request's status to awaiting-upstream (unchanged) |
| r8 | "When the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome accepted, refused or withdrawn and at least one line the line outcome accepted, `work` shall set the request's status to `accepted`." | the upstream ending its turn with every line accepted, refused or withdrawn and one accepted sets the status to accepted; the upstream ending its turn on a delivered request with every line accepted leaves the status delivered (unchanged) |
| r9 | "When the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`." | the upstream ending its turn with every line refused or withdrawn sets the status to refused (unchanged) |
| r10 | "When `work resolve <request>` is run on an `accepted` request with each accepted line's requirement id and the version that holds it, whichever side's turn it is, `work` shall write them as the request's resolution." | resolve on an accepted request in the asker's turn writes each accepted line's requirement id and version as the resolution (unchanged) |
| r11 | "When `work resolve` writes a request's resolution, `work` shall set the request's status to `delivered`." | resolve writing a request's resolution sets the request's status to delivered (unchanged) |
| r12 | "When `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch." | a change to a request commits the request on the current branch (changed; the representative action is now the upstream asking a question) |
| r13 | "When `work show` is run, `work` shall print each request with its status and whose turn it is." | show prints each request with its status and whose turn it is (unchanged) |
| r14 | "When `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names." | status with no initiative prints, with its date, each observation no initiative's or request's source names (unchanged) |

## Questions

None. No changed or new line admits two readings.

## Cases no line mentions (no scenario written)

- Whether the upstream asking a question on a line also gives that line the line outcome question, or whether a question and the line outcome question are independent of each other.
- Which question an answer answers when a request holds more than one question. No Behaviour line says (only Implementation's "the n-th answering the n-th").
- The asker answering when the request holds no question, or holds more answers than questions.
- The upstream asking a question on a line number the request does not have.
- Whether the asker may ask a question, or the upstream answer one. r20 and r21 give each side only one of the two.
- Asking or answering out of turn: r16 covers it only if asking or answering counts as "a command ... that writes a part of a request". r20 and r21 name no command.
- Asking or answering a question on a request that is `delivered`, `refused` or `withdrawn`.
- An empty question or an empty answer.

## Drafts

- /tmp/work-run-i26-oc_xbi0g/requests-3-formulate/.shop/scratch/3-formulate/drafts/round-1/requests.feature
- /tmp/work-run-i26-oc_xbi0g/requests-3-formulate/.shop/scratch/3-formulate/drafts/round-1/requests.reply.md
