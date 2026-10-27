"""The reading of requests by scripts/model: .shop/work/requests/q<n>.md, in the form `work request` writes (r19, r112)."""

import re

from model_parse import as_list, frontmatter, section
from model_work import WORK

REQUESTS = "requests"
SECTIONS = {"Lines", "Outcomes", "Questions", "Answers", "Resolution"}


class RequestReading:
    """Model's reading of .shop/work/requests/."""

    def read_requests(self):
        for path in sorted((self.root / WORK / REQUESTS).glob("*.md")):
            data, body = frontmatter(path.read_text())
            where = self.rel(path)
            wrong = self.request_form(data, body, path)
            if wrong:
                self.problems.append(f"{where}: not the form `work request` writes: {wrong}")
                continue
            self.check_id(data["id"], "request", where)
            self.node(data["id"], "request")
            self.status(data["id"], "request", data["status"], path)
            self.unread(data, path)
            self.request_links(data, body, where)

    def request_links(self, data, body, where):
        """The asker, the part_of and source (request-only relations, not the parts' and initiatives'), the resolution."""
        ident = data["id"]
        self.fact("asker", ident, str(data["asker"]).strip())
        for rel, key in (("req_part_of", "part_of"), ("req_source", "source")):
            for ref in as_list(data.get(key)):
                self.fact(rel, ident, self.qualify(ref))
                if rel == "req_part_of" and str(ref).startswith("job-thread/"):
                    self.fact("req_thread", ident)
        for ref in as_list(data.get("raised_for")):
            if str(ref).startswith("request/"):     # the kind is judged from the id
                self.fact("req_raised_for", ident, self.qualify(ref))
        for line in section(body, "Resolution"):
            m = re.match(r"^\d+\.\s+(\S+)", line)
            if m:
                req = self.resolve_req(m.group(1), where)
                if req:
                    self.fact("resolution", ident, req)

    def request_form(self, data, body, path):
        """What keeps a request from being of the form requests' Implementation gives, or None."""
        ident = str(data.get("id", ""))
        if not re.fullmatch(r"q\d+", path.stem) or ident.rsplit("/", 1)[-1] != path.stem:
            return "its file is named q<n>.md, the q<n> of its id"
        if data.get("kind") != "request":
            return "kind is not request"
        for key in ("asker", "status"):
            if not data.get(key):
                return f"no {key}"
        raised = data.get("raised_for") and str(data["asker"]).strip() != "internal"
        if not (data.get("part_of") or data.get("source") or raised):
            return "neither part_of nor source"
        if data.get("turn") not in ("asker", "upstream"):
            return "turn is not asker or upstream"
        sections = [l[3:].strip() for l in body.splitlines() if l.startswith("## ")]
        if "Lines" not in sections:
            return "no '## Lines' section"
        other = [s for s in sections if s not in SECTIONS]
        if other:
            return f"a section other than {', '.join(sorted(SECTIONS))}: {other[0]}"
        return None
