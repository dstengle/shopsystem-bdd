"""`work run`'s drafting (capability supervision): the work-items of a formulated capability-proposal, one a capability
with the deprecated scenarios it retires, and the work-item for the findings a kept branch review lists to fix now.
Standard library only; a part of supervise.Run. Drafting goes through workqueue.add, the function behind `work add`."""
import json
import re

import workqueue
from features_gherkin import Feature
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

    def retires(self, capability, accepts):
        """The deprecated scenarios of features/<capability>.feature that carry the tag of a requirement in `accepts`
        (r73): (title, tag) of each."""
        path = self.root / "features" / (capability + ".feature")
        if not path.is_file():
            return []
        wanted = {a.split("#", 1)[1] for a in expand(accepts)}
        feature = Feature(path.read_text())
        return [(sc.title, tag) for sc in feature.scenarios if "deprecated" in sc.tags
                for tag in sc.tags if tag in wanted]

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
                              capability, accepts, retires=self.retires(capability, accepts))
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
