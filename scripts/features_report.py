"""scripts/features' reports on feature files: count, list and deprecated."""
import json

from features_gherkin import REQ_TAG, natural


def cmd_count(args, files):
    counts, total = {}, 0
    for _, f in files:
        for sc in f.scenarios:
            for tags in f.rows(sc):
                total += 1
                for t in tags:
                    counts[t] = counts.get(t, 0) + 1
    for t in sorted(counts, key=natural):
        print(t, counts[t])
    print("total", total)
    return 0


def cmd_list(args, files):
    want = args.tag.lstrip("@") if args.tag else None
    hits = [(p, sc.title) for p, f in files for sc in f.scenarios
            if (want in f.effective_tags(sc) if want else args.title in sc.title)]
    if args.json:
        print(json.dumps({"scenarios": [{"file": path, "title": title} for path, title in hits]}))
        return 0
    for path, title in hits:
        print("%s: %s" % (path, title))
    return 0


def deprecated_entry(titles, path, f, sc):
    """One deprecated scenario for --json: what it is deprecated for, and the file and @r<n> tags of the scenario with that title."""
    wanted = [s[len("Deprecated for:"):].strip() for s in f.description(sc) if s.startswith("Deprecated for:")]
    target = wanted[0] if wanted else None
    replacement = None
    if target and target != "removal" and target in titles:
        tpath, tf, ts = titles[target][0]
        replacement = {"file": tpath, "tags": sorted((t for t in tf.effective_tags(ts) if REQ_TAG.match(t)), key=natural)}
    return {"file": path, "title": sc.title, "deprecated_for": target, "replacement": replacement}


def cmd_deprecated(args, files):
    titles = {}
    for p, f in files:
        for sc in f.scenarios:
            titles.setdefault(sc.title, []).append((p, f, sc))
    found = [(p, f, sc) for p, f in files for sc in f.scenarios if "deprecated" in sc.tags]
    if args.json:
        print(json.dumps({"deprecated": [deprecated_entry(titles, p, f, sc) for p, f, sc in found]}))
        return 0
    for path, f, sc in found:
        wanted = [s[len("Deprecated for:"):].strip() for s in f.description(sc) if s.startswith("Deprecated for:")]
        target = wanted[0] if wanted else None
        if target == "":
            print("%s: %s | the Deprecated for: line is empty" % (path, sc.title))
            continue
        if target is None:
            where = "no Deprecated for: line"
        elif target == "removal":
            where = "deprecated for removal"
        elif target not in titles:
            where = "no scenario has that title"
        else:
            shown = []
            for tpath, tf, ts in titles[target]:
                tags = sorted((t for t in tf.effective_tags(ts) if REQ_TAG.match(t)), key=natural)
                shown.append("%s %s" % (tpath, " ".join("@" + t for t in tags)) if tags else (tpath, None))
            if len(shown) == 1 and isinstance(shown[0], tuple):
                where = "the replacement has no @r<n> tag"
            else:
                where = "; ".join(x if isinstance(x, str) else "%s has no @r<n> tag" % x[0] for x in shown)
        print("%s: %s | for: %s | %s" % (path, sc.title, target or "-", where))
    if not found:
        print("none deprecated")
    return 0
