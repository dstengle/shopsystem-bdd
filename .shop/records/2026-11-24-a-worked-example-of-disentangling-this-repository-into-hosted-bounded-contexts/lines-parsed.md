| id | context | line | parses | note |
|---|---|---|---|---|
| E1 | execution (core) | While an assignment is in a batch, when the person merges the proposed change of the batch, the batches service shall fulfil the assignment and set the status of the batch to `merged`. | yes |  |
| E2 | execution (core) | While an assignment is in a batch, when the person abandons the batch, the batches service shall relinquish the assignment. | yes |  |
| E3 | execution (core) | When the person opens a batch, the batches service shall claim an assignment. | yes |  |
| E4 | execution (core) | If the work supply refuses a claim for an assignment, then the batches service shall keep no task of the assignment. | yes |  |
| E5 | execution (core) | While a task of an assignment is `running`, when the person parks the assignment, the batches service shall defer the assignment. | yes |  |
| E6 | execution (core) | When the person merges the proposed change of a batch, the batches service shall fulfil every assignment in the batch. | yes |  |
| P1 | supply (port) | When the batches service claims an assignment, the work supply shall complete the request. | yes |  |
| P2 | supply (port) | While a batch holds an assignment, if the batches service claims the assignment, then the work supply shall refuse the request. | yes |  |
| P3 | supply (port) | When the batches service fulfils an assignment, the work supply shall complete the request. | yes |  |
| T1 | tracking (upstream) | While an item is `ready` and the item meets the readiness bar, when a session allocates the item, the backlog service shall set the status of the item to `in-batch`. | yes |  |
| T2 | tracking (upstream) | While an item is `ready` and the item does not meet the readiness bar, if a session allocates the item, then the backlog service shall refuse the request and set the status of the item to `shaped`. | yes |  |
| T3 | tracking (upstream) | While an item is `in-batch`, when a session discharges the item, the backlog service shall set the status of the item to `delivered`. | yes |  |
| T4 | tracking (upstream) | While an item is `in-batch`, when a session restores the item, the backlog service shall set the status of the item to `ready`. | yes |  |
