---
id: model/example.org/notes/accounts/notebook
area: notebook
kind: port
imports: [accounts]
---

# notebook

## Purpose

What accounts needs of the notebook: the allowance a subscription gives, granted and taken back.

```model
service notebook
  operation entitle(subscription)
    outcomes: done | refused: no allowance
```
