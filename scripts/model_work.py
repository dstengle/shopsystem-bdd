"""The reading of scripts/model for decisions, records and the work under .shop/work/: a part of Model (model_facts)."""

import datetime
import re
from pathlib import Path

from model_parse import as_list, decision_files, expand, frontmatter, scalar

STATUSES = {
    "initiative": {"proposed", "started", "done", "abandoned"},
    "capability-proposal": {"drafted", "approved", "merged", "formulated", "withdrawn"},   # withdrawn: EXTENSION (r58)
    "work-item": {"drafted", "researched", "planned", "ready", "claimed", "done", "green", "awaiting-answer", "failed",
                  "withdrawn"},   # withdrawn: EXTENSION (r58); failed: design-decision/a-failed-work-item
    "request": {"open", "awaiting-asker", "awaiting-upstream", "accepted", "refused", "delivered"},
}
SETTLED = {"merged", "formulated", "withdrawn"}     # a capability-proposal that may name a retired id (r5, r23)
PART_KINDS = {"job-proposal", "map-proposal", "vision-proposal", "job-thread", "capability-proposal",
              "cross-context-request", "map-escalation", "work-item"}
RECORD_KINDS = {"observation", "measurement", "review-finding", "decision-argument", "initiative-archive"}
WORK = Path(".shop") / "work"
RECORDS = Path(".shop") / "records"


class WorkReading:
    """Model's reading of spec/decisions/, .shop/records/ and .shop/work/."""

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
            self.check_id(data["id"], kind, self.rel(path))
            self.node(data["id"], kind)
            for a in as_list(data.get("about")):
                a = self.qualify(a)
                self.fact("about", data["id"], a)
                self.want(a, None, self.rel(path))

    def check_work_item_name(self, path, where, held, ident):
        """r110: a work-item's id is the w<n> of its file name, and no two work-items hold one."""
        if not re.fullmatch(r"w\d+", path.stem) or str(ident).rsplit("/", 1)[-1] != path.stem:
            self.problems.append(f"{where}: a work-item's file is named w<n>.md, the w<n> of its id")
        elif ident in held:
            self.problems.append(f"{where}: the work-item id {path.stem} is already held by {held[ident]}")
        else:
            held[ident] = where

    def read_work(self):
        held = {}
        for idir in sorted(p for p in (self.root / WORK).glob("*") if p.is_dir() and p.name != "requests"):
            ipath = idir / "initiative.md"
            if not ipath.exists():
                self.problems.append(f"{self.rel(idir)}: no initiative.md")
                continue
            data, _ = frontmatter(ipath.read_text())
            i = data.get("id")
            if not i:
                self.problems.append(f"{self.rel(ipath)}: no frontmatter id")
                continue
            self.check_id(i, "initiative", self.rel(ipath))
            self.node(i, "initiative")
            self.status(i, "initiative", data.get("status"), ipath)
            if data.get("kind"):
                self.fact("ikind", i, data["kind"])
                if data["kind"] in ("job", "job-path"):
                    self.problems.append(f"{self.rel(ipath)}: kind {data['kind']!r} is not a kind an initiative may have")
            if data.get("priority") is not None:
                try:
                    self.fact("priority", i, int(data["priority"]))
                except ValueError:
                    self.problems.append(f"{self.rel(ipath)}: priority {data['priority']!r} is not a number")
            self.sources[i] = [self.qualify(s) for s in as_list(data.get("source"))]
            for s in self.sources[i]:
                self.fact("source", i, s)
                self.want(s, None, self.rel(ipath))
            if data.get("fulfils"):
                self.fact("fulfils", i, self.qualify(data["fulfils"], "request"))
            if data.get("date"):
                try:
                    days = (self.today - datetime.date.fromisoformat(str(data["date"]))).days
                    self.fact("age", i, days)
                    self.fact("date", i, str(data["date"]))
                except ValueError:
                    self.problems.append(f"{self.rel(ipath)}: date {data['date']!r} is not YYYY-MM-DD")
            for ppath in sorted(idir.glob("*.md")):
                if ppath.name not in ("initiative.md", "ledger.md"):
                    self.read_part(ppath, held)

    def read_part(self, path, held):
        data, _ = frontmatter(path.read_text())
        p, kind = data.get("id"), data.get("kind")
        where = self.rel(path)
        if not p or kind not in PART_KINDS:
            self.problems.append(f"{where}: needs an id and a kind among {', '.join(sorted(PART_KINDS))}")
            return
        self.check_id(p, kind, where)
        self.node(p, kind)
        self.status(p, kind, data.get("status"), path)
        self.unread(data, path)
        if data.get("part_of"):
            parent = self.qualify(data["part_of"])
            self.fact("part_of", p, parent)
            self.parents[p] = parent
            self.want(parent, None, where)
        for a in as_list(data.get("argues")):
            a = self.qualify(a, "capability")
            self.fact("argues", p, a)
            self.want(a, None, where)
        if kind == "capability-proposal":
            self.proposals[p] = data
            for rel in ("adds", "changes", "removes"):
                for ref in expand(as_list(data.get(rel))):
                    if str(ref).strip().startswith("term/"):     # a glossary term, not a requirement (r66)
                        head, _, name = str(ref).strip().rpartition("/")
                        t = self.qualify(f"{head}/{name.lower()}")      # r48: a term's id is lowercased
                        if self.nodes.get(t) != "term" and not (rel == "removes" and data.get("status") in ("merged", "formulated")):
                            self.dangling.append(f"{where}: {rel} {t}, which the glossary does not have")
                        continue
                    q = self.resolve_req(ref, where)
                    if not q:
                        continue
                    self.fact(rel, p, q)
                    if q in self.nodes:
                        continue
                    cap, n = q.rsplit("#r", 1)
                    if (cap, int(n)) in self.retired and data.get("status") in SETTLED:
                        continue                                # a merged, formulated or withdrawn proposal may name it (r5, r23)
                    if rel == "adds" and (cap, int(n)) in self.retired:
                        self.fact("req_id", q, cap, int(n))   # grammar.md's refusal table: v15c
                    elif rel != "changes":                     # changes: v15e reports it
                        self.dangling.append(f"{where}: {rel} {q}, which no capability has")
        if kind == "work-item":
            self.check_work_item_name(path, where, held, p)
            if data.get("wkind"):
                self.fact("wkind", p, data["wkind"])
            if data.get("under"):
                c = self.qualify(data["under"], "capability")
                self.fact("under", p, c)
                self.want(c, "capability", where)
            if data.get("for"):
                f = self.qualify(data["for"])
                self.fact("for", p, f)
                self.want(f, "work-item", where)
            if data.get("check"):
                self.fact("check", p, data["check"])
            for ref in expand(as_list(data.get("accepts"))):
                q = self.resolve_req(ref, where)
                if not q:
                    continue
                self.fact("accepts", p, q)                  # r106: from the field, whether or not a scenario names it
                found = [args[1] for name, args in self.facts if name == "has_sc" and args[0] == q]
                cap, _, n = q.rpartition("#r")
                exempt = (("group", [cap, "guarantees"]) in [(f, list(a)) for f, a in self.facts]
                          or (data.get("status") == "green" and (cap, int(n)) in self.retired))
                if not found and data.get("status") != "withdrawn" and not exempt:    # r27: a withdrawn one is closed (r36)
                    self.problems.append(f"{where}: accepts {q}, which no scenario names yet")
            for b in as_list(data.get("blocked_by")):
                b = self.qualify(b)
                self.fact("blocked_by", p, b)
                self.want(b, "work-item", where)
            for d in as_list(data.get("depends_on")):
                d = self.qualify(d, "capability")
                self.fact("wi_depends", p, d)
                self.want(d, "capability", where)
            for f in as_list(data.get("fileset")):
                self.fact("fileset", p, f)

    def status(self, ident, kind, value, path):
        if value is None:
            self.problems.append(f"{self.rel(path)}: no status")
            return
        allowed = STATUSES.get(kind)
        if allowed and value not in allowed:
            self.problems.append(f"{self.rel(path)}: status {value!r} is not one of {', '.join(sorted(allowed))}")
        self.fact("status", ident, value)
