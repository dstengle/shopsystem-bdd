"""An integrate round's change list (capability supervision r92, r96): read from the round's result, checked for its form,
and written as one `drafted` capability-proposal for each capability it names. Standard library only; a part of
supervise.Run."""
import datetime

FIELDS = ("adds", "changes", "removes")


class BadChanges(ValueError):
    """A change list that is not of the form the integrate round's brief gives."""


def entries(data):
    """The entries of the result's `changes`, each {"capability": name, "adds": [...], "changes": [...], "removes": [...]};
    an empty list when the result gives none. BadChanges when `changes` is not a list of such entries."""
    changes = data.get("changes")
    if changes in (None, []):
        return []
    if not isinstance(changes, list):
        raise BadChanges("its `changes` is not a list of entries")
    found = []
    for each in changes:
        if not isinstance(each, dict) or not isinstance(each.get("capability"), str) or not each["capability"].strip():
            raise BadChanges("an entry of its `changes` names no `capability`")
        one = {"capability": each["capability"].strip()}
        for field in FIELDS:
            ids = each.get(field, [])
            if not isinstance(ids, list) or not all(isinstance(i, str) and i.strip() for i in ids):
                raise BadChanges("the `%s` of its entry for %s is not a list of ids" % (field, one["capability"]))
            one[field] = [i.strip() for i in ids]
        found.append(one)
    return found


class Changes:
    """The part of supervise.Run that writes the proposals of a change list."""

    def unknown(self, found, stage):
        """The capabilities `found` names that neither spec/capabilities/ nor a kept draft of the integrate round's stage
        directory `stage` has (r107), in the order named."""
        held = {p.stem for p in (self.root / "spec" / "capabilities").glob("*.md")}
        held |= {p.stem for p in stage.glob("drafts/round-*/spec/capabilities/*.md")}
        return [one["capability"] for one in found if one["capability"] not in held]

    def kept_path(self, stage):
        """The integrate round's kept drafts directory with the highest round number, relative to the repository with a
        trailing slash (r108); the stage directory itself when the round kept none."""
        rounds = [p for p in stage.glob("drafts/round-*") if p.name.split("-")[-1].isdigit()]
        best = max(rounds, key=lambda p: int(p.name.split("-")[-1]), default=None)
        return self.rel(best or stage) + ("/" if best else "")

    def write_proposals(self, found, stage_dir):
        """One file a capability in the initiative's directory, `drafted`, naming `stage_dir`, the path of the round's
        kept drafts; the paths written."""
        text = (self.dir / "initiative.md").read_text()
        ident = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("id:")), "")
        prefix = ident.split("/", 1)[1].rsplit("/", 1)[0] if "/" in ident else ""
        merged = {}
        for each in found:     # the entries that name one capability are one proposal's lists, in the order first named
            one = merged.setdefault(each["capability"], {"capability": each["capability"], **{f: [] for f in FIELDS}})
            for field in FIELDS:
                one[field] += [i for i in each[field] if i not in one[field]]
        written = []
        for one in merged.values():
            path = self.dir / (one["capability"] + ".md")
            lists = "".join("%s: [%s]\n" % (f, ", ".join(one[f])) for f in FIELDS)
            path.write_text("---\nid: capability-proposal/%s/%s-%s\nkind: capability-proposal\npart_of: %s\nstatus: drafted\n"
                            "argues: [%s]\n%sdate: %s\n---\n\n# %s\n\nThe drafts of this proposal are in %s.\n" % (
                                prefix, self.dir.name, one["capability"], ident, one["capability"], lists,
                                datetime.date.today().isoformat(), one["capability"], stage_dir))
            written.append(path)
        return written
