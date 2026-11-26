---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-131/review-2
kind: review
batch: batch-131
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/154
head: 28732cdbe4d817447d43857514024fd06f4c524e
range: 51c1f499efd61c8a0df348a94432db0a1aaf43a1..28732cdbe4d817447d43857514024fd06f4c524e
result: clean
---

# batch-131 review 2

## Verdict

The fix builds what f1 asked for. With no version, `spec publish` now moves past every version already deposited, so the 1.6, 1.5, no-version sequence keeps `1.7`. I found nothing new to fix; there is one observation about the module map.

## Findings

### f7 Minor observation: the module map's row of contract_publish still gives the old default
- item: b636
- where: CLAUDE.md:1
The `scripts/contract_publish.py` row of the module map says the default version is `no version: the published one's last number one more, else 1.0.0`. It does not mention that the default now moves past each version already deposited. The module docstring (scripts/contract_publish.py:7-8) was updated in 43ccdadb9 to say this, but the map row was not. So the map no longer fully describes the module's concern. Fix: add "raised past each version deposited already" to the row.

## Earlier findings
- f1: fixed
