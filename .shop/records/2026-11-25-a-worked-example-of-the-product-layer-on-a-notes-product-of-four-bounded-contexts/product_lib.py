"""Readers of the scratch compact shop for job_trace.py and product_check.py: the shop, the product layer, each hosted
context's capabilities, vocabulary, model, adapter specs and the logical forms `spec parse --form --file` prints.
Read-only; it writes nothing."""
import re
import subprocess
import tomllib
from pathlib import Path

SPEC = "/home/vscode/shopsystem-bdd/scripts/spec"


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        v = v.strip()
        out[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()] if v.startswith("[") else v
    return out


class Shop:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.toml = tomllib.loads((self.root / ".shop" / "shop.toml").read_text())
        self.product = self.root / self.toml["product"]
        self.contexts = {cid: Context(cid, self.root / p) for cid, p in self.toml["contexts"].items()}
        self.jobs = self._jobs()
        self.subdomains, self.addressed = self._domain()
        self.actors = self._actors()
        real = self.root / "realisations.toml"
        self.realisations = tomllib.loads(real.read_text()) if real.is_file() else {}

    def _jobs(self):
        text = (self.product / "jobs.md").read_text()
        jobs = {}
        for m in re.finditer(r"^## \[(j\d+)\] (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M):
            fields = {}
            for f in re.finditer(r"^- (\w+): (.*?)(?=^- \w+: |\Z)", m.group(3), re.S | re.M):
                fields[f.group(1)] = " ".join(f.group(2).split())
            for k in ("subdomains",):
                fields[k] = [x.strip() for x in fields.get(k, "").strip("[]").split(",") if x.strip()]
            fields["actors"] = [a.strip() for a in fields.get("actor", "").split(",") if a.strip()]
            jobs["job/example.org/notes/" + m.group(1)] = dict(fields, title=m.group(2))
        return jobs

    def _domain(self):
        text = (self.product / "domain.md").read_text()
        subs, addressed = {}, {}
        for row in re.findall(r"^\| (s\d+) \| (.+?) \| (\w+) \| .*\|$", text, re.M):
            subs[row[0]] = {"name": row[1], "type": row[2]}
        for row in re.findall(r"^\| (bounded-context/\S+) \| ([s\d, ]+) \| (.+?) \|$", text, re.M):
            addressed[row[0]] = {"subdomains": [s.strip() for s in row[1].split(",")], "shop": row[2]}
        return subs, addressed

    def _actors(self):
        text = (self.product / "index.md").read_text()
        actors = {}
        for m in re.finditer(r"^- \*\*(.+?)\*\* — .*?Called: (.*?)\.\n(?=- |\Z|\n)", text, re.S | re.M):
            called = {}
            for part in re.finditer(r"(.+?) \(([^)]*)\)(?:, |$)", " ".join(m.group(2).split())):
                for ctx in part.group(2).split(","):
                    called[ctx.strip()] = part.group(1).strip()
            actors[m.group(1)] = called
        return actors


class Context:
    def __init__(self, cid, root):
        self.id, self.root, self.name = cid, Path(root), cid.rsplit("/", 1)[1]
        self.caps = {}
        for f in sorted((self.root / "spec" / "capabilities").glob("*.md")):
            fm = frontmatter(f.read_text())
            self.caps[f.stem] = dict(fm, file=f, serves=fm.get("serves") or [])
        self.verbs, self.areas, self.ops = {}, {}, {}
        for f in (self.root / "spec" / "vocabulary").glob("*.md"):
            for v, op in re.findall(r"^- \*\*(.+?)\*\* \(verb, action\) → operation (\S+)\.(?:\s|$)", f.read_text(), re.M):
                self.verbs[v] = op
        for f in (self.root / "spec" / "model").glob("*.md"):
            text = f.read_text()
            fm = frontmatter(text)
            svc = None
            for line in text.splitlines():
                if line.startswith("service "):
                    svc = line.split()[1]
                    self.areas[svc] = fm.get("kind")
                m = re.match(r"  operation (\w+)\((.*?)\)(.*)", line)
                if m and svc:
                    self.ops[f"{svc}.{m.group(1)}"] = {"props": m.group(3), "area": fm.get("area"),
                                                       "kind": fm.get("kind")}
            for noun, svc2 in re.findall(r"^- \*\*(.+?)\*\* \(proper noun\) → service (\S+?)\.", "", re.M):
                pass
        self.services = {}
        for f in (self.root / "spec" / "vocabulary").glob("*.md"):
            for noun, svc in re.findall(r"^- \*\*(.+?)\*\* \(proper noun\) → service (\S+?)\.(?:\s|$)", f.read_text(), re.M):
                self.services[noun] = svc
        self._outcomes()
        self.adapters = {}
        for f in sorted((self.root / "adapters").glob("*/spec/index.md")):
            fm = frontmatter(f.read_text())
            self.adapters[fm["id"]] = dict(fm, root=f.parent.parent)
        self._forms = None

    def _outcomes(self):
        for f in (self.root / "spec" / "model").glob("*.md"):
            text = re.sub(r"\n {4,}", " ", f.read_text())
            for m in re.finditer(r"^  operation (\w+)\(.*?outcomes: (.*)$", text, re.M):
                for op, data in self.ops.items():
                    if op.endswith("." + m.group(1)) and data["area"] == frontmatter(f.read_text()).get("area"):
                        data["outcomes"] = m.group(2)
                        data["reads"] = "returned" in m.group(2) and "done" not in m.group(2)

    def forms(self):
        """{capability: [(line id, text, form)]} from spec parse --form --file, each line's id read off the file."""
        if self._forms is None:
            self._forms = {}
            for cap, data in self.caps.items():
                lines = data["file"].read_text().splitlines()
                done = subprocess.run(["python3", SPEC, "--root", str(self.root), "parse", "--form", "--file",
                                       str(data["file"].resolve())], capture_output=True, text=True)
                out = []
                for m in re.finditer(r"^(\d+): (.*?)(?=^\d+: |\Z)", done.stdout, re.S | re.M):
                    n = int(m.group(1))
                    rid = re.match(r"- \[(r\d+)\] (.*)", lines[n - 1])
                    more = []
                    for nxt in lines[n:]:
                        if not nxt.startswith("  "):
                            break
                        more.append(nxt.strip())
                    text = " ".join([rid.group(2) if rid else lines[n - 1]] + more)
                    out.append((rid.group(1) if rid else f"line{n}", text, m.group(2)))
                if done.returncode and not out:
                    out.append(("?", "", done.stdout + done.stderr))
                self._forms[cap] = out
        return self._forms


def parts(form):
    """The trigger atoms and the response atoms of a printed logical form."""
    head, _, response = form.partition("\n  response")
    return head, response


def events(section):
    """(verb, subject) of each event atom, and (operation, subject) of each request atom, of a section."""
    out = []
    for m in re.finditer(r"\b(\w+)\(e\d+, (?:(\S+?), )?subject: (x\d+)", section):
        out.append((m.group(1), m.group(2), m.group(3)))
    return out


def constants(form):
    return dict(re.findall(r"(x\d+): (?:service|agent) (the [\w ]+?|a [\w ]+?) \(constant\)", form))
