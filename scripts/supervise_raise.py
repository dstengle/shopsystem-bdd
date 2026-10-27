"""`work run`'s raising of the lines an integrate round gives into an upstream (capability supervision r135, r136): each
entry of the result's `requests` is written as a request in the upstream's repository with `work request`'s own function,
raised for the request the initiative fulfils and with its delegation; each is recorded in
.shop/work/<initiative>/raised.jsonl, tied to the round's kept drafts. A capability-proposal written by such a round is
held while any request raised with it is not delivered. Standard library only; a part of supervise.Run."""
import json

import workqueue
import workqueue_request
from workqueue import Refused

RECORD = "raised.jsonl"


class Raises:
    """The part of supervise.Run that raises an integrate round's lines and reads whether they are delivered."""

    def upstream_root(self, ident):
        """The repository of the upstream `ident`: the directory above its published spec, else None."""
        return next((path.parent for found, path in self.upstreams() if found == ident), None)

    def raise_requests(self, data, stage, kept):
        """Raise each entry of the integrate result's `requests` that has lines; the record lines written (not yet on
        disk) as one text. `stage` is the round's stage directory in the main checkout, `kept` its drafts path as the
        proposals name it. Refused, naming the upstream and work's reason, when one cannot be raised."""
        given = data.get("requests")
        entries = [e for e in given if isinstance(e, dict) and e.get("lines")] if isinstance(given, list) else []
        if not entries:
            return ""
        me, _ = workqueue.frontmatter((self.root / "spec" / "index.md").read_text())
        fulfils = workqueue.frontmatter((self.dir / "initiative.md").read_text())[0].get("fulfils")
        asked = str(fulfils).rsplit("/", 1)[-1] if fulfils else None
        delegation = self.delegation()
        record = ""
        for number, each in enumerate(entries, 1):
            upstream = each.get("upstream")
            where = self.upstream_root(upstream)
            try:
                if where is None:
                    raise Refused("%s is not an upstream of spec/index.md" % upstream)
                lines = stage / ("request-lines-%d.md" % number)
                lines.write_text("".join("%s\n" % l for l in each["lines"]))
                request = workqueue_request.request(
                    where, "%s: what %s needs of %s" % (self.initiative, self.initiative, upstream.rsplit("/", 1)[-1]),
                    me.get("id"), str(lines), [], None, delegation, raised_for=asked)
            except Refused as why:
                raise Refused("the raise of the lines of %s into %s failed: %s" % (self.initiative, upstream, why)) from None
            record += json.dumps({"upstream": upstream, "request": request, "initiative": self.initiative,
                                  "status": "open", "round": kept}) + "\n"
        return record

    def write_record(self, text):
        """Append `text` to the initiative's record of raised requests; the path written, relative, as the round's commit
        takes it; an empty list when there is nothing to record."""
        if not text:
            return []
        path = self.dir / RECORD
        workqueue.append(path, text.encode())
        return [self.rel(path)]

    def arrived(self, record):
        """Whether the request a record line names reads as delivered in its upstream; one that cannot be read does not."""
        where = self.upstream_root(record.get("upstream"))
        try:
            path = workqueue_request.path_of(where, str(record.get("request")))
            return workqueue_request.field(workqueue.read(path, where), "status") == "delivered"
        except (Refused, OSError, TypeError):
            return False

    def waits(self, proposal):
        """Whether the capability-proposal file `proposal` waits (r136): its text names the drafts of an integrate round
        that raised a request not read as delivered."""
        path = self.dir / RECORD
        if not path.is_file():
            return False
        text = proposal.read_text()
        for line in path.read_text().splitlines():
            try:
                one = json.loads(line)
            except ValueError:
                continue
            if isinstance(one, dict) and one.get("round") and ("in %s." % one["round"]) in text and not self.arrived(one):
                return True
        return False
