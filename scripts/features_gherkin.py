"""The Gherkin reader behind scripts/features: a feature file parsed into its tags, Background and scenarios, the
feature files under a directory, and a scenario found by its title. Standard library only."""
import os
import re

STEP = re.compile(r"(Given|When|Then|And|But|\*)\s")
SCENARIO = re.compile(r"(Scenario Outline|Scenario Template|Scenario|Example):")
EXAMPLES = re.compile(r"(Examples|Scenarios):")
REQ_TAG = re.compile(r"r\d+$")


class Refused(Exception):
    pass


class Scenario:
    def __init__(self, title, start, line, tag_lines, tags):
        self.title, self.start, self.line = title, start, line
        self.tag_lines, self.tags = tag_lines, tags
        self.end = None
        self.tables = []  # (tags, row count)


class Feature:
    def __init__(self, text):
        self.lines = text.split("\n")
        self.tags, self.scenarios = [], []
        self.background = None  # (first line, end)
        self.in_doc = [False] * len(self.lines)
        self.tag_line_set = set()
        self._parse()

    def _tags(self, indexes):
        found = []
        for i in indexes:
            self.tag_line_set.add(i)
            for word in self.lines[i].split():
                if word.startswith("#"):
                    break
                found.append(word.lstrip("@"))
        return found

    def _parse(self):
        delim, pending, table = None, [], None
        for i, line in enumerate(self.lines):
            s = line.strip()
            if delim:
                self.in_doc[i] = True
                if s.startswith(delim):
                    delim = None
                continue
            if s.startswith('"""') or s.startswith("```"):
                self.in_doc[i] = True
                if s.find(s[:3], 3) < 0:
                    delim = s[:3]
                continue
            if s.startswith("@"):
                pending.append(i)
            elif s.startswith("Feature:"):
                self.tags, pending = self._tags(pending), []
            elif s.startswith("Rule:"):
                raise Refused("line %d: Rule: blocks are not supported" % (i + 1))
            elif s.startswith("Background:"):
                self.background, pending = [i + 1, None], []
            elif SCENARIO.match(s):
                if self.scenarios:
                    self.scenarios[-1].end = pending[0] if pending else i
                elif self.background:
                    self.background[1] = pending[0] if pending else i
                title = s.split(":", 1)[1].strip()
                self.scenarios.append(Scenario(
                    title, pending[0] if pending else i, i, list(pending),
                    self._tags(pending)))
                pending, table = [], None
            elif EXAMPLES.match(s):
                table = (self._tags(pending), [0])
                self.scenarios[-1].tables.append(table)
                pending = []
            elif s.startswith("|") and table:
                table[1][0] += 1
            elif s and not s.startswith("#"):
                pending = []
        for sc in self.scenarios:
            if sc.end is None:
                sc.end = len(self.lines)
        if self.background and self.background[1] is None:
            self.background[1] = len(self.lines)

    def content(self, first, last):
        return [(i, self.lines[i].strip()) for i in range(first, last)
                if self.lines[i].strip() and i not in self.tag_line_set
                and (self.in_doc[i] or not self.lines[i].strip().startswith("#"))]

    def block(self, sc):
        end = sc.end
        while end > sc.start and not self.lines[end - 1].strip():
            end -= 1
        return end

    def rows(self, sc):
        """One tag set per collected test."""
        base = set(self.tags) | set(sc.tags)
        if not sc.tables:
            return [base]
        return [base | set(t) for t, n in sc.tables for _ in range(max(n[0] - 1, 0))]

    def effective_tags(self, sc):
        return set(self.tags) | set(sc.tags) | {x for t, _ in sc.tables for x in t}

    def first_step(self, sc):
        for i, s in self.content(sc.line + 1, sc.end):
            if not self.in_doc[i] and STEP.match(s):
                return i
        return None

    def description(self, sc):
        step = self.first_step(sc)
        return [s for _, s in self.content(sc.line + 1, step if step is not None else sc.end)]

    def steps(self, sc):
        step = self.first_step(sc)
        return [] if step is None else [s for _, s in self.content(step, sc.end)]

    def background_steps(self):
        if not self.background:
            return []
        return [s for _, s in self.content(*self.background)]


def load(directory):
    found = []
    for root, _, names in sorted(os.walk(directory)):
        for name in sorted(names):
            if name.endswith(".feature"):
                path = os.path.join(root, name)
                with open(path) as handle:
                    try:
                        found.append((path, Feature(handle.read())))
                    except Refused as why:
                        raise Refused("%s: %s" % (path, why))
    return found


def locate(files, title, args=None):
    only = getattr(args, "file", None)
    if only:
        return locate_in(files, title, only, args.dir)
    hits = [(p, f, sc) for p, f in files for sc in f.scenarios if sc.title == title]
    if not hits:
        raise Refused("no scenario titled %r" % title)
    if len(hits) > 1:
        raise Refused("title %r is in several scenarios: %s" % (
            title, ", ".join(sorted({p for p, _, _ in hits}))))
    return hits[0]


def locate_in(files, title, only, directory):
    """The one scenario titled `title` in the file `only`, a file under `directory`."""
    root = os.path.realpath(directory)
    target = os.path.realpath(only)
    if os.path.commonpath([root, target]) != root:
        raise Refused("%s is outside %s" % (only, directory))
    for path, f in files:
        if os.path.realpath(path) == target:
            hits = [sc for sc in f.scenarios if sc.title == title]
            if len(hits) > 1:
                raise Refused("%s has the title %r twice" % (only, title))
            if hits:
                return path, f, hits[0]
            break
    raise Refused("%s does not have the title %r" % (only, title))


def natural(tag):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", tag)]
