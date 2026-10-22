"""scripts/features' edits of feature files: tag, move, deprecate and retire. Every edit is checked to parse before
any file is written."""
import os
import sys

from features_gherkin import REQ_TAG, Feature, Refused, locate


def usage_error(message):
    sys.stderr.write("features: error: %s\n" % message)
    return 2


def indent_of(line):
    return line[:len(line) - len(line.lstrip())]


def write_checked(edits):
    """edits: {path: lines}. Validate every file parses, then write."""
    texts = {p: "\n".join(lines) for p, lines in edits.items()}
    for path, text in texts.items():
        try:
            Feature(text)
        except Refused as why:
            raise Refused("%s: the edit would leave it unreadable: %s" % (os.path.relpath(path), why))
    for path, text in texts.items():
        with open(path, "w") as handle:
            handle.write(text)


def cmd_tag(args, files):
    path, f, sc = locate(files, args.title, args)
    if not REQ_TAG.match(args.tag):
        sys.exit(usage_error("tag must look like r<n>"))
    lines = list(f.lines)
    placed = False
    for i in sc.tag_lines:  # r51: the first @r<m> becomes @r<n>, any other @r<m> goes
        words = lines[i].split()
        kept = []
        for word in words:
            if word.startswith("@") and REQ_TAG.match(word[1:]):
                if placed:
                    continue
                word, placed = "@" + args.tag, True
            kept.append(word)
        if kept != words:
            lines[i] = indent_of(lines[i]) + " ".join(kept) if kept else None
    lines = [line for line in lines if line is not None]
    if not placed and sc.tag_lines:
        last = sc.tag_lines[-1]
        lines[last] = lines[last].rstrip() + " @" + args.tag
    elif not placed:
        text = lines[sc.line]
        lines[sc.line] = indent_of(text) + "@" + args.tag + "\n" + text
    write_checked({path: lines})
    return 0


def cmd_move(args, files):
    path, f, sc = locate(files, args.title, args)
    dest = args.to
    root = os.path.realpath(args.dir)
    if os.path.commonpath([root, os.path.realpath(dest)]) != root:  # r35
        raise Refused("%s is outside %s: %r stays in %s" % (dest, args.dir, args.title, path))
    if not os.path.isfile(dest):
        raise Refused("%s does not exist" % dest)
    if os.path.abspath(dest) == os.path.abspath(path):
        raise Refused("%s is the scenario's own file" % dest)
    end = f.block(sc)
    block = f.lines[sc.start:end]
    if args.inline_background:
        step = f.first_step(sc)
        if step is not None:
            line = f.lines[step]
            indent = line[:len(line) - len(line.lstrip())]
            at = step - sc.start
            block[at:at] = [indent + s for s in f.background_steps()]
    if args.keep_feature_tags:
        with open(dest) as handle:
            have = set(Feature(handle.read()).tags)
        keep = ["@" + t for t in f.tags if t not in have]
        if keep:
            text = block[sc.line - sc.start]
            block.insert(sc.line - sc.start, text[:len(text) - len(text.lstrip())] + " ".join(keep))
    source = f.lines[:sc.start] + f.lines[sc.end:]
    if sc.start > 0 and not f.lines[sc.start - 1].strip() and sc.end >= len(f.lines):
        while source and not source[-1].strip():
            source.pop()
        source.append("")
    with open(dest) as handle:
        target = handle.read().split("\n")
    while target and not target[-1].strip():
        target.pop()
    target += [""] + block + [""]
    write_checked({path: source, dest: target})
    return 0


def cmd_deprecate(args, files):
    path, f, sc = locate(files, args.title, args)
    if not args.removal and any(c in args.deprecated_for for c in "\r\n"):
        raise Refused("the new title must be one line: %r" % args.deprecated_for)
    if "deprecated" in sc.tags:
        raise Refused("%r is already deprecated" % args.title)
    lines = list(f.lines)
    text = lines[sc.line]
    lines[sc.line] = text.rstrip() + " (deprecated)"
    after = next((lines[i] for i in range(sc.line + 1, sc.end) if lines[i].strip()), None)
    inner = indent_of(after) if after is not None else indent_of(text) + "  "
    lines.insert(sc.line + 1, inner + "Deprecated for: " + ("removal" if args.removal else args.deprecated_for))
    if sc.tag_lines:
        last = sc.tag_lines[-1]
        lines[last] = lines[last].rstrip() + " @deprecated"
    else:
        lines.insert(sc.line, indent_of(text) + "@deprecated")
    write_checked({path: lines})
    print("%s: %s (deprecated)" % (path, args.title))
    return 0


def cmd_retire(args, files):
    path, f, sc = locate(files, args.title, args)
    if "deprecated" not in sc.tags:
        raise Refused("%r is not tagged @deprecated: only a deprecated scenario is retired here" % args.title)
    lines = f.lines[:sc.start] + f.lines[sc.end:]
    if sc.end >= len(f.lines):
        while lines and not lines[-1].strip():
            lines.pop()
        lines.append("")
    write_checked({path: lines})
    return 0
