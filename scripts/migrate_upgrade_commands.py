"""The old command lines of an upgrade (b632, upgrades#r44; decision 0132), planned on every upgrade from a release
before the plugin's, tied to no release as the scenario conftest's is (migrate_upgrade_conftest): in a consumer's
instructions files, and no other file (the hooks of `.claude/settings.json`, `CLAUDE.md`, `.shop/delivery.toml`'s
`[batch] tests` and `[review] checks`, the pages under `docs/`), each command that runs `work`, `spec`, `model`,
`measure`, `migrate`, `tools` or `features` by its old name rewritten to `shop <name>` (`model`, spec's alias, to
`shop spec`), in the upgrade's one commit. A command is a name in a command's place followed by an argument: at the
start of a shell command (a hook's or a setting's string, a line of a shell fence, an inline code span) or after
`&&`, `||`, `;`, `|`, `(` or `$(`; or the plugin's script `${CLAUDE_PLUGIN_ROOT}/scripts/<name>`. A name that is only
mentioned (in prose, alone in a code span, a path such as `spec/`) is left alone, and a line already of `shop` is
no command of the old name, so the rewrite is idempotent."""
import re
import subprocess

from migrate_upgrade_ids import Changes

NAMES = ("work", "spec", "model", "measure", "migrate", "tools", "features")
SETTINGS, CLAUDE, DELIVERY = ".claude/settings.json", "CLAUDE.md", ".shop/delivery.toml"
_NAME = "(%s)" % "|".join(NAMES)
BARE = re.compile(r"(^|&&|\|\||[;|(]|\$\()(\s*)" + _NAME + r"(?=[ \t]+[-\w\"'$])", re.MULTILINE)
SCRIPT = re.compile(r"(\$\{?CLAUDE_PLUGIN_ROOT\}?/scripts/)" + _NAME + r"(\\?[\"']?)(?=[ \t])")
SHELLS = ("", "console", "bash", "sh", "shell", "zsh", "terminal")
FENCE = re.compile(r"^\s*(```+|~~~+)\s*([\w-]*)")
SPAN = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
STRING = re.compile(r'"((?:[^"\\]|\\.)*)"')
COMMAND = re.compile(r'("command"\s*:\s*)"((?:[^"\\]|\\.)*)"')


def _subcommand(name):
    return "spec" if name == "model" else name


def shell(text):
    """A shell command with each old command run as `shop <name>`."""
    text = BARE.sub(lambda m: "%s%sshop %s" % (m.group(1), m.group(2), _subcommand(m.group(3))), text)
    return SCRIPT.sub(lambda m: "%sshop%s %s" % (m.group(1), m.group(3), _subcommand(m.group(2))), text)


def settings(text):
    """`.claude/settings.json`: each hook's command string."""
    return COMMAND.sub(lambda m: '%s"%s"' % (m.group(1), shell(m.group(2))), text)


def delivery(text):
    """`.shop/delivery.toml`: the strings of `[batch] tests` and `[review] checks`, an array over lines among them."""
    out, table, open_array = [], None, False
    for line in text.splitlines(keepends=True):
        header = re.match(r"^\s*\[([^\]]+)\]\s*$", line)
        if header and not open_array:
            table = header.group(1).strip()
            out.append(line)
            continue
        key = re.match(r"^\s*(\w+)\s*=\s*(.*)$", line)
        if key and not open_array:
            ours = (table, key.group(1)) in (("batch", "tests"), ("review", "checks"))
            open_array = ours and key.group(2).lstrip().startswith("[") and "]" not in key.group(2)
            out.append(STRING.sub(lambda m: '"%s"' % shell(m.group(1)), line) if ours else line)
            continue
        if open_array:
            out.append(STRING.sub(lambda m: '"%s"' % shell(m.group(1)), line))
            open_array = "]" not in line
            continue
        out.append(line)
    return "".join(out)


def markdown(text):
    """`CLAUDE.md` and a page under `docs/`: each line of a shell fence (after a `$ ` prompt) and each inline code
    span outside a fence; a fence of another language left alone."""
    out, fence = [], None
    for line in text.splitlines(keepends=True):
        opened = FENCE.match(line)
        if fence is None and opened:
            fence = (opened.group(1), opened.group(2).lower() in SHELLS)
            out.append(line)
        elif fence is not None and opened and opened.group(1).startswith(fence[0]) and not opened.group(2):
            fence = None
            out.append(line)
        elif fence is not None:
            prompt = re.match(r"^(\s*(?:\$\s+)?)(.*)$", line, re.DOTALL)
            out.append(prompt.group(1) + shell(prompt.group(2)) if fence[1] else line)
        else:
            out.append(SPAN.sub(lambda m: m.group(1) + shell(m.group(2)) + m.group(1), line))
    return "".join(out)


def tracked(root):
    """The instructions files git tracks, each with its rewrite."""
    listed = subprocess.run(["git", "ls-files", "-z", "--", SETTINGS, CLAUDE, DELIVERY, "docs"], cwd=root,
                            capture_output=True, text=True, check=True).stdout.split("\0")
    rewrites = {SETTINGS: settings, CLAUDE: markdown, DELIVERY: delivery}
    for rel in listed:
        if rel in rewrites:
            yield rel, rewrites[rel]
        elif rel.startswith("docs/") and rel.endswith(".md"):
            yield rel, markdown


def plan(root):
    changes = Changes()
    changes.notes = []
    for rel, rewrite in tracked(root):
        path = root / rel
        if not path.is_file():
            continue
        with open(path, newline="") as handle:
            text = handle.read()
        new = rewrite(text)
        if new != text:
            changes.texts[rel] = new
            changes.notes.append("%s: its old command lines rewritten to shop <name>" % rel)
    return changes
