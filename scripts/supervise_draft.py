"""`work run`'s drafting (capability supervision): the work-items of a formulated capability-proposal, one a capability
with the deprecated scenarios it retires, and the work-item for the findings a kept branch review lists to fix now.
Standard library only; a part of supervise.Run. Drafting goes through workqueue.add, the function behind `work add`."""
import json
import re
from pathlib import Path

import workqueue
from features_gherkin import REQ_TAG, load, natural
from model_parse import expand

REQUIREMENT = re.compile(r"([\w-]+)#(r\d+(?:-r\d+)?)$")
WORK_ITEM = re.compile(r"\bw\d+\b")


class Drafts:
    """The part of supervise.Run that drafts work-items."""

    def nodes(self, kind):
        """(name, frontmatter) of each file of the initiative of that kind, in path order."""
        for path in sorted(self.dir.glob("*.md")):
            data, _ = workqueue.frontmatter(workqueue.read(path, self.root))
            if data.get("kind") == kind:
                yield path.stem, data

    def deprecated(self):
        """Each deprecated scenario of any feature file whose `Deprecated for:` line names one scenario: (title, the
        requirements, as capability#r<n>, its replacement carries)."""
        files = load(self.root / "features")
        titles = {}
        for path, feature in files:
            for sc in feature.scenarios:
                titles.setdefault(sc.title, []).append((path, feature, sc))
        found = []
        for _, feature in files:
            for sc in feature.scenarios:
                lines = [s[len("Deprecated for:"):].strip() for s in feature.description(sc) if s.startswith("Deprecated for:")]
                if "deprecated" in sc.tags and lines and len(titles.get(lines[0], [])) == 1:
                    path, replacement, rsc = titles[lines[0]][0]
                    tags = sorted((t for t in replacement.effective_tags(rsc) if REQ_TAG.match(t)), key=natural)
                    found.append((sc.title, ["%s#%s" % (Path(path).stem, t) for t in tags]))
        return found

    def retires(self, accepts):
        """The deprecated scenarios whose replacement carries the tag of a requirement in `accepts` (r73): (title,
        requirement) of each, once."""
        wanted = set(expand(accepts))
        return [(title, next(r for r in ids if r in wanted)) for title, ids in self.deprecated() if wanted & set(ids)]

    def draft_retires(self):
        """One work-item retiring each deprecated scenario whose replacement's work-items, those of any initiative that
        are not withdrawn, are all green, and that no work-item lists to retire already (r123). Whether it was drafted."""
        items = []
        for path in sorted((self.root / workqueue.WORK).glob("*/*.md")):
            text = workqueue.read(path, self.root)
            data, _ = workqueue.frontmatter(text)
            if data.get("kind") == "work-item" and data.get("status") != "withdrawn":
                items.append((int(re.sub(r"\D", "", path.stem) or 0), data, text))
        listed = "\n".join(section for _, _, text in items for section in text.split("\n## Retires\n")[1:])
        retiring, last = [], None
        for title, ids in self.deprecated():
            if '- "%s" (' % title in listed:
                continue
            for requirement in ids:
                holders = [(n, d) for n, d, _ in items if requirement in expand([str(a) for a in d.get("accepts") or []])]
                if holders and all(d.get("status") == "green" for _, d in holders):
                    retiring.append((title, requirement))
                    last = max(holders + ([last] if last else []), key=lambda h: h[0])
                    break
        if not retiring:
            return False
        data = last[1]
        workqueue.add(self.root, self.initiative, "retire the deprecated scenarios of %s" % self.initiative,
                      str(data.get("part_of")), str(data.get("under")), list(data.get("accepts") or []), retires=retiring)
        return True

    def draft_proposals(self):
        """One work-item for each capability a formulated capability-proposal adds or changes, accepting every
        requirement it names on that capability (r72); a capability that has one already gets none. Whether any was
        drafted."""
        have = {(str(d.get("part_of")).rsplit("/", 1)[-1], d.get("under")) for _, d in self.nodes("work-item")}
        drafted = False
        for name, data in self.nodes("capability-proposal"):
            if data.get("status") != "formulated":
                continue
            groups = {}
            for entry in list(data.get("adds") or []) + list(data.get("changes") or []):
                found = REQUIREMENT.match(str(entry))
                if found:
                    groups.setdefault(found.group(1), []).append(str(entry))
            for capability, accepts in groups.items():
                if (str(data.get("id", name)).rsplit("/", 1)[-1], capability) in have:
                    continue
                workqueue.add(self.root, self.initiative, "%s: %s" % (name, capability), str(data.get("id", name)),
                              capability, accepts, retires=self.retires(accepts))
                drafted = True
        return drafted

    def fix_work_item(self, kept):
        """One work-item for the findings to fix now that the kept branch review `kept` lists in its result (r74): under
        the capability-proposal of the work-item they name, naming the review's findings.md. Whether it was drafted."""
        try:
            result = json.loads((kept / "result.json").read_text())
        except (OSError, ValueError):
            return False
        lines = result.get("questions") if isinstance(result, dict) else None
        if not isinstance(lines, list) or not lines:
            return False
        findings = self.rel(kept / "findings.md")
        if any(d.get("findings") == findings for _, d in self.nodes("work-item")):
            return False
        concerned = {n: d for n, d in self.nodes("work-item")}
        for line in lines:
            named = WORK_ITEM.search(str(line))
            if named and named.group() in concerned:
                data = concerned[named.group()]
                workqueue.add(self.root, self.initiative,
                              "fix the findings of branch review %s of %s" % (kept.name, self.initiative),
                              str(data.get("part_of")), str(data.get("under")), list(data.get("accepts") or []),
                              findings=findings)
                return True
        return False
