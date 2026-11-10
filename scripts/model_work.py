"""The reading of scripts/model for decisions and records, and of the frozen `.shop/work/` only the `source` ids its
initiatives and requests cite (plan 9, D5, D6): a part of Model (model_facts)."""

import re
from pathlib import Path

import model_decisions
import shop_frozen
from model_parse import as_list, decision_files, frontmatter, scalar

STATUSES = {     # design model v5's lifecycles of what is still read (GF conversion design §7.1: C13, C14)
    "request": {"open", "awaiting-asker", "awaiting-upstream", "accepted", "refused", "delivered", "withdrawn"},
    "design-decision": {"proposed", "accepted", "rejected", "superseded"},
}
# The kinds of plugin 1.x's queue, frozen under .shop/work/ (plan 9, D5): a reference to one is history, never resolved.
FROZEN_KINDS = {"initiative", "work-item", "capability-proposal", "glossary-proposal", "job-proposal", "map-proposal",
                "vision-proposal", "map-escalation"}
RECORD_KINDS = {"observation", "measurement", "review-finding", "decision-argument", "initiative-archive",
                "design", "analysis"}     # design and analysis are history (C21)
HISTORY = {"design": "record", "analysis": "record"}     # their ids are record/<path>/<name>
WORK = Path(".shop") / "work"
RECORDS = Path(".shop") / "records"


class WorkReading:
    """Model's reading of spec/decisions/, .shop/records/ and the frozen .shop/work/'s citations."""

    def read_decisions(self):
        for path in decision_files(self.root):
            data, body = frontmatter(path.read_text())
            self.unread(data, path)
            if not any(l.startswith("## ") and l[3:].strip() == "Decision" for l in body.splitlines()):
                self.problems.append(f"{self.rel(path)}: no '## Decision' section")
            d = data.get("id")
            if not d:
                self.problems.append(f"{self.rel(path)}: no frontmatter id")
                continue
            self.check_id(d, "design-decision", self.rel(path))
            self.node(d, "design-decision")
            if data.get("status") is not None:      # C14; a decision with no status is read as before
                self.status(d, "design-decision", data["status"], path)
            if data.get("summary"):
                self.fact("summary", d, data["summary"])
            for old in as_list(data.get("supersedes")):
                old = self.qualify(old, "design-decision")
                self.fact("supersedes", d, old)
                self.want(old, "design-decision", self.rel(path))
            for s in as_list(data.get("source")):       # ids only; the free text is `by`, which is not read (r64)
                self.want(self.qualify(s), None, self.rel(path))
            if data.get("revisit_signal"):
                self.fact("revisit_signal", d, self.qualify(data["revisit_signal"]))   # "requests" stays as written
            self.read_tier(d, data, self.rel(path))

    def read_tier(self, d, data, where):
        """tier/2, enforced_test/2 and enforced_req/2 (decision-tiers D2); an entry of the wrong form is a file problem."""
        tier, (tests, reqs) = data.get("tier"), model_decisions.split(as_list(data.get("enforced_by")))
        self.problems += [f"{where}: {p}" for p in model_decisions.wrong(self.root, tier, tests, reqs)]
        if tier in model_decisions.TIERS:
            self.fact("tier", d, tier)
        for t in tests:
            self.fact("enforced_test", d, t)
        for q in filter(None, (self.resolve_req(ref, where) for ref in reqs)):
            self.fact("enforced_req", d, q)
            self.want(q, "requirement", where)
        self.read_routes(d, data, where)

    def read_routes(self, d, data, where):
        """route/2, a decision's `verified_by` (v_d9 names one outside the four), and decision_rests_on/2, each id it rests on;
        a bare `U<n>` is the universal condition (b129)."""
        for r in as_list(data.get("verified_by")):
            self.fact("route", d, str(r).strip())
        for ref in as_list(data.get("rests_on")):
            ref = str(ref).strip()
            ref = self.qualify(ref.lower() if re.fullmatch(r"U\d+", ref) else ref, "universal-condition")
            self.fact("decision_rests_on", d, ref)
            self.want(ref, None, where)

    def read_records(self):
        obs = self.root / RECORDS / "observations.md"
        if obs.exists():
            current = None
            for line in obs.read_text().splitlines():
                if line.startswith("## "):
                    current = line[3:].strip()
                    self.check_id(current, "observation", self.rel(obs))
                    self.node(current, "observation")
                elif current:
                    m = re.match(r"^about:\s*(.+)$", line.strip())
                    if m:
                        a = self.qualify(scalar(m.group(1)))
                        self.fact("about", current, a)
                        self.want(a, None, self.rel(obs))
        for path in sorted((self.root / RECORDS).rglob("*.md")):
            if path == obs:
                continue
            data, _ = frontmatter(path.read_text())
            if not data.get("id"):
                continue
            self.unread(data, path)
            kind = data.get("kind")
            if kind not in RECORD_KINDS:
                self.problems.append(f"{self.rel(path)}: kind {kind!r} is not a record kind")
                continue
            self.check_id(data["id"], HISTORY.get(kind, kind), self.rel(path))
            self.node(data["id"], kind)
            for a in as_list(data.get("about")):
                a = self.qualify(a)
                self.fact("about", data["id"], a)
                self.want(a, None, self.rel(path))

    def read_work(self):
        """cited(O) for each id a frozen initiative or request names in its `source` (D6): no node, part or reference
        of the frozen queue is read."""
        for ident in sorted(shop_frozen.sources(self.root)):
            head, _, rest = ident.partition("/")
            self.fact("cited", f"{head}/{self.path}/{rest}" if self.path and "/" not in rest else ident)

    def status(self, ident, kind, value, path):
        if value is None:
            self.problems.append(f"{self.rel(path)}: no status")
            return
        allowed = STATUSES.get(kind)
        if allowed and value not in allowed:
            self.problems.append(f"{self.rel(path)}: status {value!r} is not one of {', '.join(sorted(allowed))}")
        self.fact("status", ident, value)
