---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-9/review-4
kind: review
batch: batch-9
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/24
head: 41e0d381fe89a4c0a13986aaefacd33f41dededb
range: 4eec885d253a0d8b2d4ddbcfb859a19a7e3e2ba5..41e0d381fe89a4c0a13986aaefacd33f41dededb
result: clean
---

# batch-9 review 4

## Verdict

The fix for f6 works. A post that GitHub accepts but whose URL commit git then refuses is now refused with the URL and how to record it. `work sync` records the post, and running the same command again records it without posting a second comment or opening a second issue. The new tests cover both the comment and the issue path. All runs exit 0 at `Head:`. This review adds no `fix now` finding, only two observations.

## Findings

### f7 Minor observation: a failing close hides the refusal that names the unrecorded comment
- item: b36
- where: scripts/request_post.py:141
The close now sits in a `finally` block, so it runs even after the URL commit is refused. If `gh issue close` also fails, its `Refused` replaces the one that `not_recorded` built. The person then never sees the posted comment's URL or the `work sync` advice. Reproduction: run a closing step (one with `posted.close`) with the URL commit refused and the stand-in gh failing on `issue close`. stderr shows only the close failure. Fix: catch the close's failure inside the `except Refused as why` branch and add it to the `not_recorded` message.

```python
    try:
        shop_files.committed(root, rels[:1], "%s: posted" % message, lambda: path.write_text(final))
    except Refused as why:
        raise Refused(not_recorded(why, "the comment", said)) from None
    finally:
        if posted.close:
            request_gh.close(root, url, posted.command)
```

### f8 Minor observation: every post now reads the issue first, and a matching body counts as already posted
- item: b36
- where: scripts/request_post.py:153
`committed` now calls `unrecorded` (`gh issue view`) before every comment. A failed view now puts the record back and refuses a step that could have been posted. Any comment the record does not hold whose body matches, after `strip()`, is taken as this step's earlier post. That includes a comment from the other side that has not been synced yet. Today the two sides' bodies differ, so no client hits this. I checked that `request_gh.view` gives back each comment as (URL, body) and that `listed` asks for up to 200 open issues, so `orphan_issue` and `adopted` still find an orphan issue on a busy repository.

## Earlier findings
- f6: fixed
