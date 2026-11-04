"""The grammar tools: GF 3.12 and the pinned pgf and clingo wheels, installed and probed (design §11)."""
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

GF_VERSION = "3.12"
GF_URL = ("https://github.com/GrammaticalFramework/gf-core/releases/download/release-3.12/"
          "gf-3.12-ubuntu-24.04.deb")
GF_SHA256 = "17aa5452b713f1e00a0755a1bad998a926acbffb96eefde2c3800ca72536b4d8"
WHEELS = {"pgf": "1.1", "clingo": "5.8.2"}
PARSE = "requirements cannot be parsed: `work request` and `model check` refuse"
LOGIC = "requirements cannot be logic-checked: `model logic` refuses"
WITHOUT = {"gf": PARSE, "pgf": PARSE, "clingo": LOGIC}
BY_HAND = "build GF 3.12 by hand and set $SHOPSYSTEM_GF to its gf"
VERSIONS = ("import json, sys\nfrom importlib import metadata\nout = {}\n"
            "for name in sys.argv[1:]:\n    try:\n        out[name] = metadata.version(name)\n"
            "    except metadata.PackageNotFoundError:\n        out[name] = None\n"
            "out['virtualenv'] = sys.prefix != sys.base_prefix\nprint(json.dumps(out))\n")
WRAPPER = '#!/bin/sh\nLD_LIBRARY_PATH=%s${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} exec %s "$@"\n'


class Refused(Exception):
    pass


def gf_home(environ=None):
    """Where `tools install` puts GF: ${XDG_DATA_HOME:-~/.local/share}/shopsystem-bdd/gf-3.12."""
    environ = os.environ if environ is None else environ
    data = environ.get("XDG_DATA_HOME") or os.path.join(environ.get("HOME") or os.path.expanduser("~"),
                                                        ".local", "share")
    return pathlib.Path(data) / "shopsystem-bdd" / ("gf-" + GF_VERSION)


def gf_version(binary):
    """The version `<binary> --version` gives, as '3.12.0', or None when it is no Grammatical Framework."""
    try:
        done = subprocess.run([str(binary), "--version"], stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    found = re.search(r"Grammatical Framework \(GF\) version (\S+)", done.stdout)
    return found.group(1) if found else None


def gf_binary(environ=None):
    """GF's binary: $SHOPSYSTEM_GF, the install path, then a `gf` on PATH that says it is Grammatical Framework.

    The PATH lookup runs no shell, so a shell's `gf` alias (git fetch) never answers."""
    environ = os.environ if environ is None else environ
    if environ.get("SHOPSYSTEM_GF"):
        return environ["SHOPSYSTEM_GF"]
    installed = gf_home(environ) / "bin" / "gf"
    if os.access(installed, os.X_OK):
        return str(installed)
    on_path = shutil.which("gf", path=environ.get("PATH", os.defpath))
    if on_path and gf_version(on_path):
        return on_path
    return None


def check_platform(system=None, machine=None):
    system = system or platform.system()
    machine = machine or platform.machine()
    if system != "Linux" or machine not in ("x86_64", "AMD64"):
        raise Refused("the grammar tools are not supported on %s %s: GF 3.12 and pgf 1.1 are installed for "
                      "Linux x86_64 only; %s" % (system, machine, BY_HAND))


def versions(python):
    done = subprocess.run([python, "-c", VERSIONS, *WHEELS], capture_output=True, text=True)
    if done.returncode:
        raise Refused("%s does not run: %s" % (python, done.stderr.strip()[-300:]))
    return json.loads(done.stdout)


def probed(python=None, environ=None):
    """{"gf": version|None, "pgf": …, "clingo": …} for the interpreter running the scripts."""
    found = versions(python or sys.executable)
    binary = gf_binary(environ)
    grammar = {"gf": gf_version(binary) if binary else None}
    grammar.update((name, found[name]) for name in WHEELS)
    return grammar, binary


def probe_lines(grammar, binary):
    lines = ["grammar:"]
    for name, version in grammar.items():
        if version is None:
            lines.append("  %s missing: %s" % (name, WITHOUT[name]))
        else:
            lines.append("  %s %s" % (name, version) + (" (%s)" % binary if name == "gf" else ""))
    return lines


def install_wheels(python=None):
    """Each pinned wheel not at its pin, installed with pip (with --user outside a virtualenv)."""
    python = python or sys.executable
    found = versions(python)
    for name, pin in WHEELS.items():
        if found[name] == pin:
            print("%s %s already installed" % (name, pin))
            continue
        command = [python, "-m", "pip", "install"] + ([] if found["virtualenv"] else ["--user"]) + \
            ["%s==%s" % (name, pin)]
        done = subprocess.run(command, capture_output=True, text=True)
        if "externally-managed" in done.stderr or "externally managed" in done.stderr:
            raise Refused("pip refuses to install %s into %s: it is externally managed. The grammar wheels go into "
                          "the interpreter running tools (not --python): run tools with one pip may install into, "
                          "such as a virtualenv's python" % (name, python))
        if done.returncode:
            raise Refused("%s %s did not install: %s\n  %s" % (name, pin, " ".join(command),
                                                               "\n  ".join(done.stderr.strip().splitlines()[-4:])))
        print("%s %s installed" % (name, pin))


def download(url, into):
    try:
        with urllib.request.urlopen(url, timeout=120) as response, open(into, "wb") as out:
            shutil.copyfileobj(response, out)
    except OSError as why:
        raise Refused("GF could not be downloaded from %s: %s; or %s" % (url, why, BY_HAND))


def install_gf(target=None, url=GF_URL, sha256=GF_SHA256, which=shutil.which):
    """GF at <target> (the install path): downloaded, its sha256 checked, unpacked with dpkg-deb, wrapped."""
    target = pathlib.Path(target or gf_home())
    version = gf_version(target / "bin" / "gf")
    if version and version.startswith(GF_VERSION):
        print("gf %s already installed" % GF_VERSION)
        return
    if not which("dpkg-deb"):
        raise Refused("dpkg-deb is needed to unpack GF and is not on PATH (there is no other unpacker): install it, "
                      "or %s" % BY_HAND)
    target.parent.mkdir(parents=True, exist_ok=True)
    work = pathlib.Path(tempfile.mkdtemp(prefix=".gf-", dir=target.parent))
    try:
        deb = work / "gf.deb"
        download(url, deb)
        digest = hashlib.sha256(deb.read_bytes()).hexdigest()
        if digest != sha256:
            raise Refused("the download from %s has sha256 %s, not %s: nothing is installed" % (url, digest, sha256))
        root = work / "gf"
        done = subprocess.run(["dpkg-deb", "-x", str(deb), str(root)], capture_output=True, text=True)
        if done.returncode:
            raise Refused("dpkg-deb could not unpack %s: %s" % (url, done.stderr.strip()[-300:]))
        write_wrapper(root, target)
        deb.unlink()
        if target.exists():
            shutil.rmtree(target)
        os.rename(root, target)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if not (gf_version(target / "bin" / "gf") or "").startswith(GF_VERSION):
        raise Refused("GF was unpacked to %s but its bin/gf does not say version %s" % (target, GF_VERSION))
    print("gf %s downloaded" % GF_VERSION)


def write_wrapper(root, target):
    """bin/gf: runs <target>/usr/bin/gf with its libraries on LD_LIBRARY_PATH (paths as they are once moved)."""
    libs = [target / "usr" / "lib"] + sorted(target / "usr" / "lib" / path.name
                                             for path in (root / "usr" / "lib").glob("*-ghc-*") if path.is_dir())
    (root / "bin").mkdir(exist_ok=True)
    wrapper = root / "bin" / "gf"
    wrapper.write_text(WRAPPER % (":".join(map(str, libs)), target / "usr" / "bin" / "gf"))
    wrapper.chmod(0o755)


def install():
    """`tools install`'s grammar part: the platform checked, the wheels and GF installed. Raises Refused."""
    check_platform()
    install_wheels()
    install_gf()
