"""An integrate or apply round's change list (capability supervision r92, r96, r107, r114): read from the round's result, checked for its form,
and written as one `drafted` capability-proposal for each capability it names and, for its glossary entries, one `drafted`
glossary-proposal (r171). Standard library only; a part of
supervise.Run."""
import datetime
import re

import workqueue

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
        glossary = isinstance(each, dict) and each.get("glossary") is True and "capability" not in each
        if not glossary and (not isinstance(each, dict) or not isinstance(each.get("capability"), str)
                             or not each["capability"].strip()):
            raise BadChanges("an entry of its `changes` names no `capability`")
        one = {"capability": None, "glossary": True} if glossary else {"capability": each["capability"].strip()}
        for field in FIELDS:
            ids = each.get(field, [])
            if not isinstance(ids, list) or not all(isinstance(i, str) and i.strip() for i in ids):
                raise BadChanges("the `%s` of its entry for %s is not a list of ids" % (field, one["capability"] or "the glossary"))
            one[field] = [i.strip() for i in ids]
        found.append(one)
    return found


class Changes:
    """The part of supervise.Run that writes the proposals of a change list."""

    def unknown(self, found, stage, runs=False):
        """The capabilities `found` names that neither spec/capabilities/ nor a kept draft of the integrate round's stage
        directory `stage` has (r107), in the order named; with `runs`, `stage` holds the stage directories of rounds and
        the drafts of all of them count (an apply round's list)."""
        held = {p.stem for p in (self.root / "spec" / "capabilities").glob("*.md")}
        held |= {p.stem for p in stage.glob(("*/" if runs else "") + "drafts/round-*/spec/capabilities/*.md")}
        return [one["capability"] for one in found if not one.get("glossary") and one["capability"] not in held]

    def kept_path(self, stage):
        """The integrate round's kept drafts directory with the highest round number, relative to the repository with a
        trailing slash (r108); the stage directory itself when the round kept none."""
        rounds = [p for p in stage.glob("drafts/round-*") if p.name.split("-")[-1].isdigit()]
        best = max(rounds, key=lambda p: int(p.name.split("-")[-1]), default=None)
        return self.rel(best or stage) + ("/" if best else "")

    def rewrite_lists(self, name, found):
        """The `adds`, `changes` and `removes` of the capability-proposal `name`, each replaced by what the entries of
        `found` naming its capability give; a list they give nothing for becomes empty (r114)."""
        path = self.dir / (name + ".md")
        lists = {f: [] for f in FIELDS}
        text = path.read_text()
        argues = next((l.split(":", 1)[1].strip().strip("[]") for l in text.splitlines() if l.startswith("argues:")), "")
        for each in found:
            if each["capability"] == argues:
                for field in FIELDS:
                    lists[field] += [i for i in each[field] if i not in lists[field]]
        end = text.find("\n---", 4)
        head = "\n".join(l for l in text[:end].split("\n") if l.split(":")[0] not in FIELDS)
        path.write_text(head + "\n" + "\n".join("%s: [%s]" % (f, ", ".join(lists[f])) for f in FIELDS) + text[end:])

    def proposal_for(self, capability):
        """The initiative's capability-proposal that argues `capability`, as a path, else None."""
        for path in sorted(self.dir.glob("*.md")):
            text = path.read_text()
            if "\nkind: capability-proposal\n" in text and re.search(r"(?m)^argues: \[%s\]$" % re.escape(capability), text):
                return path
        return None

    def merge_lists(self, name, one):
        """The round's ids for the capability of the proposal `name` (a held proposal the round was not started for)
        appended to its `adds`, `changes` and `removes`, after the ids it holds."""
        path = self.dir / (name + ".md")
        text = path.read_text()
        lists, _ = workqueue.frontmatter(text)
        for field in FIELDS:
            mine = list(lists.get(field) or [])
            mine += [i for i in one[field] if i not in mine]
            text = re.sub(r"(?m)^%s:.*$" % field, lambda _: "%s: [%s]" % (field, ", ".join(mine)), text, count=1)
        path.write_text(text)

    def write_proposals(self, found, stage_dir, own=None):
        """One file a capability in the initiative's directory, `drafted`, naming `stage_dir`, the path of the round's
        kept drafts; the paths written. A capability the initiative has a proposal for has that proposal rewritten in
        place: its lists and its drafts path replaced, its status left to the move (r142, r148). When that proposal is
        not `own`, the one the round was started for, the round's ids are merged into its lists instead."""
        text = (self.dir / "initiative.md").read_text()
        ident = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("id:")), "")
        prefix = ident.split("/", 1)[1].rsplit("/", 1)[0] if "/" in ident else ""
        merged = {}
        for each in (e for e in found if not e.get("glossary")):     # the entries that name one capability are one proposal's lists, in the order first named
            one = merged.setdefault(each["capability"], {"capability": each["capability"], **{f: [] for f in FIELDS}})
            for field in FIELDS:
                one[field] += [i for i in each[field] if i not in one[field]]
        written = []
        for one in merged.values():
            held = self.proposal_for(one["capability"])
            if held:     # r148: a proposal drafted anew is rewritten, never a second one beside it
                if held.stem != own:     # the round did not write this proposal's drafts: its drafts path stays
                    self.merge_lists(held.stem, one)
                    written.append(held)
                    continue
                self.rewrite_lists(held.stem, [one])
                text = held.read_text()
                said = "The drafts of this proposal are in %s." % stage_dir
                held.write_text(re.sub(r"The drafts of this proposal are in \S+?\.(?=\s|$)", lambda _: said, text)
                                if "The drafts of this proposal are in" in text else text.rstrip("\n") + "\n\n" + said + "\n")
                written.append(held)
                continue
            path = self.dir / (one["capability"] + ".md")
            lists = "".join("%s: [%s]\n" % (f, ", ".join(one[f])) for f in FIELDS)
            path.write_text("---\nid: capability-proposal/%s/%s-%s\nkind: capability-proposal\npart_of: %s\nstatus: drafted\n"
                            "argues: [%s]\n%sdate: %s\n---\n\n# %s\n\nThe drafts of this proposal are in %s.\n" % (
                                prefix, self.dir.name, one["capability"], ident, one["capability"], lists,
                                datetime.date.today().isoformat(), one["capability"], stage_dir))
            written.append(path)
        terms = {f: [] for f in FIELDS}
        for each in (e for e in found if e.get("glossary")):     # r171: the glossary's entries are one proposal's lists
            for field in FIELDS:
                terms[field] += [i for i in each[field] if i not in terms[field]]
        if any(e.get("glossary") for e in found):
            path = self.dir / "glossary.md"
            path.write_text("---\nid: glossary-proposal/%s/%s-glossary\nkind: glossary-proposal\npart_of: %s\nstatus: drafted\n%sdate: %s\n"
                            "---\n\n# glossary\n\nThe drafts of this proposal are in %s.\n" % (
                                prefix, self.dir.name, ident, "".join("%s: [%s]\n" % (f, ", ".join(terms[f])) for f in FIELDS),
                                datetime.date.today().isoformat(), stage_dir))
            written.append(path)
        return written
