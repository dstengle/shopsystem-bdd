---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-91/review-1
kind: review
batch: batch-91
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/114
head: 449028e25550bac7ab7d1466c11315abaf1c00c6
range: c6690acfddef9d46d65130044a62637fe1ffda5a..449028e25550bac7ab7d1466c11315abaf1c00c6
result: fix-now
---

# batch-91 review 1

## Verdict

The batch builds both of b587's lines. `spec obtain` keeps the upstream's published contract under `provider/` in one commit and keeps no context request (checking#r81). An upstream with no contract is refused, naming the bounded context (checking#r82). All runs exit 0 at the head, `features generate --check` among them. The change is within the size limit, and every new module has a row in the module map. One finding to fix: a refusal that no line asks for. The rest are observations.

## Findings

### f1 Minor fix now: `spec obtain` refuses a second contract at the same place, and no line asks for that
- item: b587
- where: scripts/contract_obtain.py:197
The two lines ask only to keep the contract (r81) and to refuse an upstream with no contract (r82). The capability file has no Implementation section. Even so, `obtain` has two behaviours of its own that a caller can see:

```python
        if target.read_text(encoding="utf-8") == text:
            print("kept already %s" % rel)
            return 0
        raise Refused("{names} is kept already as another contract: an obtained contract is never edited",
                      reason="contract already obtained", names=["contract:%s" % rel])
```

The refusal reason `contract already obtained` is also missing from the model: `spec/model/specification.md` declares only `refused: bounded context with no contract` for `obtain`. So the change adds a refusal that neither the lines nor the model have. Decision 0117 says only that `provider/<upstream>/<version>/` is written only by obtaining. That does not forbid obtaining again over it.

Fix, one of two ways. Either drop the refusal and let obtaining write the upstream's bytes again (obtaining is the only writer). Or give the refusal a line and a declared reason on b587 through `work line` and `work batch amend`, so the line, the model and the code agree.

### f2 Minor observation: a badly formed id is refused under the wrong reason
- item: b587
- where: scripts/contract_obtain.py:191
An id that does not start with `bounded-context/` is refused with `reason="bounded context with no contract"`, but nothing was checked about whether it has a contract. The check is also redundant. `request_gh.repo_of` (scripts/request_gh.py:45-49) already refuses any id that has no `github:` bullet under `## Upstreams`, naming it. I verified this by reading `repo_of`. The check can go, or it can carry its own reason.

### f3 Minor observation: a missing or unreadable repository is reported as "has no contract"
- item: b587
- where: scripts/contract_obtain.py:149
`_api` treats any gh failure whose first stderr line holds `404` or `Not Found` as "this file is not there". GitHub also answers 404 for a repository that does not exist and for a private repository the account cannot read. In both cases `published` then refuses with "the bounded context ... has no contract", which is the wrong diagnosis when the `github:` value is wrong or access is missing. To reproduce: set the upstream's `github:` to a repository that does not exist and run `spec obtain`. A cheap fix is to check the repository first (`gh api repos/<r>`) before reading `.shop/contracts`.

### f4 Minor observation: two upstreams whose ids end in the same word share one folder
- item: b587
- where: scripts/contract_obtain.py:195
`<upstream>` is only the last part of the id (`context.rsplit("/", 1)[-1]`). Take `bounded-context/a.org/x/inventory` and `bounded-context/b.org/y/inventory`. Their contracts at one version land on the same `provider/inventory/<v>/contract.toml`. The second obtain is either refused as "another contract" or reported as `kept already`, even though it is a different upstream's contract. Decision 0123 has an adapter "hold its providers" under `adapters/<port>-<provider>/`. This change writes `provider/` at the root of the repository instead. Whoever builds the adapter spec should settle that place.

### f5 Minor observation: "byte for byte" does not hold for CRLF files
- item: b587
- where: scripts/batch_gh.py:18
`batch_gh.gh` runs gh with `text=True`, which turns `\r\n` into `\n`. A contract that the upstream keeps with CRLF line endings is therefore not kept byte for byte, which the docstring, the docs and the module map all claim. Contracts that `spec publish` writes have LF endings, so no client hits this today.
