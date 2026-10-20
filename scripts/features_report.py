"""scripts/features' reports on feature files: count, list, verify-moved and deprecated."""
from features_gherkin import REQ_TAG, load, natural


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
    for path, title in hits:
        print("%s: %s" % (path, title))
    return 0 if hits else 1


def summarise(files):
    by_title = {}
    for _, f in files:
        for sc in f.scenarios:
            by_title.setdefault(sc.title, []).append((f, sc))
    return by_title


def cmd_verify(args, files):
    before = summarise(load(args.from_dir))
    after = summarise(files)
    out = []
    for label, side in (("before", before), ("after", after)):
        out += ["duplicate title %s: %s" % (label, t) for t in sorted(side) if len(side[t]) > 1]
    out += ["missing: " + t for t in sorted(set(before) - set(after))]
    out += ["added: " + t for t in sorted(set(after) - set(before))]
    matched = 0
    for title in sorted(set(before) & set(after)):
        if len(before[title]) > 1 or len(after[title]) > 1:
            continue
        (bf, bs), (af, a_s) = before[title][0], after[title][0]
        differs = []
        if bf.effective_tags(bs) != af.effective_tags(a_s):
            differs.append("tags")
        if bf.description(bs) != af.description(a_s):
            differs.append("description")
        if bf.background_steps() + bf.steps(bs) != af.background_steps() + af.steps(a_s):
            differs.append("steps")
        if differs:
            out.append("changed: %s (%s)" % (title, ", ".join(differs)))
        else:
            matched += 1
    if out:
        print("\n".join(out))
        return 1
    print("%d scenarios match" % matched)
    return 0


def cmd_deprecated(args, files):
    titles = {}
    for p, f in files:
        for sc in f.scenarios:
            titles.setdefault(sc.title, []).append((p, f, sc))
    found = [(p, f, sc) for p, f in files for sc in f.scenarios if "deprecated" in sc.tags]
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
