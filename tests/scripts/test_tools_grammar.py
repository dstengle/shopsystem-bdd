"""tools_grammar: GF and the pinned pgf and clingo wheels, installed and probed (design §11.1-§11.2)."""
import hashlib
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import tools_grammar

GF_SCRIPT = "#!/bin/sh\necho 'Grammatical Framework (GF) version %s'\necho 'Built on linux/x86_64'\n"
# a stand-in interpreter: answers the versions its config gives and logs each pip call
PYTHON = r"""#!%s
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
config = json.load(open(os.path.join(here, "config.json")))
args = sys.argv[1:]
if args[:1] == ["-c"]:
    out = {name: config["versions"].get(name) for name in args[2:]}
    print(json.dumps(dict(out, virtualenv=config["venv"])))
    sys.exit(0)
if args[:3] == ["-m", "pip", "install"]:
    with open(os.path.join(here, "pip.log"), "a") as log:
        log.write(" ".join(args[3:]) + "\n")
    if config.get("pip_error"):
        sys.stderr.write(config["pip_error"])
        sys.exit(1)
    sys.exit(0)
sys.exit(3)
""" % sys.executable


def stub_gf(path, version="3.12.0"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(GF_SCRIPT % version)
    path.chmod(0o755)
    return path


class GrammarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)

    def deb(self):
        """A .deb laid out as GF's is: usr/bin/gf and a ghc library directory under usr/lib."""
        root = self.tmp / "pkg"
        stub_gf(root / "usr" / "bin" / "gf")
        (root / "usr" / "lib" / "x86_64-linux-ghc-9.6.7").mkdir(parents=True)
        (root / "DEBIAN").mkdir()
        (root / "DEBIAN" / "control").write_text(
            "Package: gf\nVersion: 3.12\nArchitecture: amd64\nMaintainer: t <t@t>\nDescription: t\n")
        deb = self.tmp / "gf.deb"
        subprocess.run(["dpkg-deb", "--build", str(root), str(deb)], check=True, capture_output=True)
        return deb, hashlib.sha256(deb.read_bytes()).hexdigest()

    def install_gf(self, **kwargs):
        out = io.StringIO()
        with redirect_stdout(out):
            tools_grammar.install_gf(**kwargs)
        return out.getvalue()

    def test_gf_is_downloaded_checked_unpacked_and_wrapped(self):
        deb, digest = self.deb()
        target = self.tmp / "data" / "gf-3.12"
        out = self.install_gf(target=target, url=deb.as_uri(), sha256=digest)
        self.assertEqual(out, "gf 3.12 downloaded\n")
        wrapper = target / "bin" / "gf"
        self.assertTrue(os.access(wrapper, os.X_OK))
        text = wrapper.read_text()
        self.assertIn("LD_LIBRARY_PATH=", text)
        self.assertIn(str(target / "usr" / "lib" / "x86_64-linux-ghc-9.6.7"), text)
        self.assertEqual(tools_grammar.gf_version(wrapper), "3.12.0")

    def test_a_second_install_is_a_no_op(self):
        deb, digest = self.deb()
        target = self.tmp / "gf-3.12"
        self.install_gf(target=target, url=deb.as_uri(), sha256=digest)
        out = self.install_gf(target=target, url=(self.tmp / "gone.deb").as_uri(), sha256=digest)
        self.assertEqual(out, "gf 3.12 already installed\n")

    def test_a_wrong_digest_is_refused_and_nothing_is_installed(self):
        deb, _digest = self.deb()
        target = self.tmp / "gf-3.12"
        with self.assertRaises(tools_grammar.Refused) as raised:
            self.install_gf(target=target, url=deb.as_uri(), sha256="0" * 64)
        self.assertIn("sha256", str(raised.exception))
        self.assertIn("0" * 64, str(raised.exception))
        self.assertFalse(target.exists())
        self.assertEqual([p.name for p in self.tmp.iterdir() if p.name.startswith(".gf")], [])

    def test_without_dpkg_deb_the_install_names_it_and_shopsystem_gf(self):
        deb, digest = self.deb()
        with self.assertRaises(tools_grammar.Refused) as raised:
            self.install_gf(target=self.tmp / "gf-3.12", url=deb.as_uri(), sha256=digest, which=lambda name: None)
        self.assertIn("dpkg-deb", str(raised.exception))
        self.assertIn("$SHOPSYSTEM_GF", str(raised.exception))

    def test_an_unsupported_platform_is_refused_naming_shopsystem_gf(self):
        for system, machine in (("Darwin", "arm64"), ("Linux", "aarch64"), ("Windows", "AMD64")):
            with self.assertRaises(tools_grammar.Refused) as raised:
                tools_grammar.check_platform(system, machine)
            self.assertIn("$SHOPSYSTEM_GF", str(raised.exception))
            self.assertIn("not supported", str(raised.exception))
        tools_grammar.check_platform("Linux", "x86_64")

    def test_the_install_path_follows_xdg_data_home(self):
        self.assertEqual(tools_grammar.gf_home({"XDG_DATA_HOME": "/d"}), pathlib.Path("/d/shopsystem-bdd/gf-3.12"))
        self.assertEqual(tools_grammar.gf_home({"HOME": "/h"}), pathlib.Path("/h/.local/share/shopsystem-bdd/gf-3.12"))

    def python(self, versions, venv=False, pip_error=""):
        where = self.tmp / "py"
        where.mkdir()
        (where / "config.json").write_text(json.dumps({"versions": versions, "venv": venv, "pip_error": pip_error}))
        (where / "python").write_text(PYTHON)
        (where / "python").chmod(0o755)
        return where / "python"

    def pip_log(self):
        log = self.tmp / "py" / "pip.log"
        return log.read_text().splitlines() if log.exists() else []

    def test_the_wheels_are_installed_at_their_pins_and_a_present_one_is_left(self):
        python = self.python({"pgf": "1.1", "clingo": "5.7.0"})
        out = io.StringIO()
        with redirect_stdout(out):
            tools_grammar.install_wheels(str(python))
        self.assertEqual(out.getvalue().splitlines(), ["pgf 1.1 already installed", "clingo 5.8.2 installed"])
        self.assertEqual(self.pip_log(), ["--user clingo==5.8.2"])

    def test_in_a_virtualenv_the_wheels_go_in_without_user(self):
        python = self.python({}, venv=True)
        with redirect_stdout(io.StringIO()):
            tools_grammar.install_wheels(str(python))
        self.assertEqual(self.pip_log(), ["pgf==1.1", "clingo==5.8.2"])

    def test_an_externally_managed_interpreter_is_refused_naming_python(self):
        python = self.python({}, pip_error="error: externally-managed-environment\n")
        with self.assertRaises(tools_grammar.Refused) as raised, redirect_stdout(io.StringIO()):
            tools_grammar.install_wheels(str(python))
        self.assertIn("--python", str(raised.exception))
        self.assertIn("externally managed", str(raised.exception))

    def test_gf_is_found_in_shopsystem_gf_then_the_install_then_path(self):
        named = stub_gf(self.tmp / "named" / "gf")
        installed = stub_gf(self.tmp / "data" / "shopsystem-bdd" / "gf-3.12" / "bin" / "gf")
        on_path = stub_gf(self.tmp / "path" / "gf")
        env = {"SHOPSYSTEM_GF": str(named), "XDG_DATA_HOME": str(self.tmp / "data"), "PATH": str(on_path.parent)}
        self.assertEqual(tools_grammar.gf_binary(env), str(named))
        del env["SHOPSYSTEM_GF"]
        self.assertEqual(tools_grammar.gf_binary(env), str(installed))
        env["XDG_DATA_HOME"] = str(self.tmp / "nothing")
        self.assertEqual(tools_grammar.gf_binary(env), str(on_path))

    def test_a_gf_on_path_that_is_not_grammatical_framework_is_not_used(self):
        other = self.tmp / "path" / "gf"
        other.parent.mkdir()
        other.write_text("#!/bin/sh\necho 'git fetch'\n")
        other.chmod(0o755)
        env = {"XDG_DATA_HOME": str(self.tmp / "nothing"), "PATH": str(other.parent)}
        self.assertIsNone(tools_grammar.gf_binary(env))

    def tools(self, *args, env=None):
        environ = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_GF", "VIRTUAL_ENV", "PYTEST_ADDOPTS")}
        environ.update(env or {})
        (self.tmp / "project").mkdir(exist_ok=True)
        (self.tmp / "project" / "pytest.ini").write_text("[pytest]\n")
        return subprocess.run([sys.executable, str(SCRIPTS / "tools"), "--python", sys.executable, *args],
                              cwd=self.tmp / "project", capture_output=True, text=True, env=environ)

    def test_probe_json_gives_the_grammar_block(self):
        stub_gf(self.tmp / "data" / "shopsystem-bdd" / "gf-3.12" / "bin" / "gf")
        done = self.tools("probe", "--json", env={"XDG_DATA_HOME": str(self.tmp / "data")})
        found = json.loads(done.stdout)
        self.assertEqual(found["python"], sys.executable)
        self.assertIn("ruff", found["tools"])
        self.assertEqual(found["grammar"]["gf"], "3.12.0")
        self.assertEqual(set(found["grammar"]), {"gf", "pgf", "clingo", "gf-rgl"})

    def test_probe_prints_a_grammar_block_naming_what_a_missing_tool_stops(self):
        done = self.tools("probe", env={"XDG_DATA_HOME": str(self.tmp / "nothing"), "PATH": "/usr/bin:/bin"})
        lines = done.stdout.splitlines()
        block = lines[lines.index("grammar:") + 1:]
        self.assertEqual([line.split()[0] for line in block], ["gf", "pgf", "clingo", "gf-rgl"])
        self.assertIn("  gf missing: requirements cannot be parsed: `work request` and `model check` refuse", block)
        self.assertEqual(done.returncode, 1)

    def test_probe_json_says_null_for_a_missing_gf(self):
        done = self.tools("probe", "--json", env={"XDG_DATA_HOME": str(self.tmp / "nothing"), "PATH": "/usr/bin:/bin"})
        self.assertIsNone(json.loads(done.stdout)["grammar"]["gf"])

    def rgl_tarball(self):
        """A gf-rgl release tarball laid out as the real one: gf-rgl-<release>/src/, one small module of each built."""
        root = self.tmp / "tarball" / ("gf-rgl-" + tools_grammar.RGL_RELEASE)
        (root / "src" / "prelude").mkdir(parents=True)
        (root / "src" / "prelude" / "Prelude.gf").write_text("resource Prelude = { oper SS : Type = {s : Str} ; }\n")
        for module in tools_grammar.RGL_MODULES:
            path = root / "src" / (module + ".gf")
            path.parent.mkdir(exist_ok=True)
            (path.parent / (path.stem + "Abs.gf")).write_text("abstract %sAbs = { cat C ; }\n" % path.stem)
            path.write_text("concrete %s of %sAbs = open Prelude in { lincat C = SS ; }\n" % (path.stem, path.stem))
        archive = self.tmp / "rgl.tar.gz"
        subprocess.run(["tar", "czf", str(archive), "-C", str(root.parent), root.name], check=True)
        return archive, hashlib.sha256(archive.read_bytes()).hexdigest()

    def install_rgl(self, **kwargs):
        gf = tools_grammar.gf_binary()
        self.assertTrue(gf, "no gf: run `python3 scripts/tools install`")
        out = io.StringIO()
        with redirect_stdout(out):
            tools_grammar.install_rgl(gf=gf, **kwargs)
        return out.getvalue()

    def test_the_rgl_is_downloaded_checked_and_built_then_found(self):
        archive, digest = self.rgl_tarball()
        target = tools_grammar.rgl_home({"XDG_DATA_HOME": str(self.tmp / "data")})
        self.assertIsNone(tools_grammar.rgl_path({"XDG_DATA_HOME": str(self.tmp / "data")}))
        out = self.install_rgl(target=target, url=archive.as_uri(), sha256=digest)
        self.assertEqual(out, "gf-rgl 20250812 built\n")
        for part in ("prelude/Prelude.gfo", "present/AllEng.gfo", "alltenses/AllEng.gfo", "alltenses/TryEng.gfo"):
            self.assertTrue((target / part).is_file(), part)
        self.assertEqual(tools_grammar.rgl_path({"XDG_DATA_HOME": str(self.tmp / "data")}), str(target))
        out = self.install_rgl(target=target, url=(self.tmp / "gone.tar.gz").as_uri(), sha256=digest)
        self.assertEqual(out, "gf-rgl 20250812 already installed\n")

    def test_an_rgl_download_with_a_wrong_digest_is_refused_and_nothing_is_installed(self):
        archive, _digest = self.rgl_tarball()
        target = self.tmp / "gf-rgl-20250812"
        with self.assertRaises(tools_grammar.Refused) as raised:
            self.install_rgl(target=target, url=archive.as_uri(), sha256="0" * 64)
        self.assertIn("0" * 64, str(raised.exception))
        self.assertFalse(target.exists())
        self.assertEqual([p.name for p in self.tmp.iterdir() if p.name.startswith(".gf-rgl")], [])

    def test_an_rgl_module_gf_cannot_compile_is_refused_naming_it(self):
        self.rgl_tarball()
        source = self.tmp / "tarball" / ("gf-rgl-" + tools_grammar.RGL_RELEASE)
        (source / "src" / "api" / "TryEng.gf").write_text("concrete TryEng of Nothing = {}\n")
        with self.assertRaises(tools_grammar.Refused) as raised:
            self.install_rgl(target=self.tmp / "gf-rgl-20250812", source=str(source))
        self.assertIn("TryEng.gf", str(raised.exception))
        self.assertFalse((self.tmp / "gf-rgl-20250812").exists())

    def test_nothing_imports_telingo_or_the_old_solver(self):
        root = pathlib.Path(__file__).resolve().parents[2]
        files = list((root / "scripts").glob("*.py")) + [root / "scripts" / n for n in ("tools", "model", "features")]
        pattern = r"^\s*(import|from)\s+(telingo|spec_engine|spec_logic\b|spec_logic_np|spec_trace\b)"
        bad = sorted(p.name for p in files if re.search(pattern, p.read_text(), re.MULTILINE))
        self.assertEqual(bad, [])
        self.assertFalse((root / "grammar" / "background.lp").exists() or (root / "grammar" / "cone.lp").exists())


if __name__ == "__main__":
    unittest.main()
