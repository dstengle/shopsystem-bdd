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

    def write_proposals(self, found, stage_dir):
        """One file a capability in the initiative's directory, `drafted`; the paths written."""
        text = (self.dir / "initiative.md").read_text()
        ident = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("id:")), "")
        prefix = ident.split("/", 1)[1].rsplit("/", 1)[0] if "/" in ident else ""
        written = []
        for one in found:
            path = self.dir / (one["capability"] + ".md")
            lists = "".join("%s: [%s]\n" % (f, ", ".join(one[f])) for f in FIELDS)
            path.write_text("---\nid: capability-proposal/%s/%s-%s\nkind: capability-proposal\npart_of: %s\nstatus: drafted\n"
                            "argues: [%s]\n%sdate: %s\n---\n\n# %s\n\nThe drafts of this proposal are in %s.\n" % (
                                prefix, self.dir.name, one["capability"], ident, one["capability"], lists,
                                datetime.date.today().isoformat(), one["capability"], stage_dir))
            written.append(path)
        return written
