"""`--work-item <name>`: run only the scenarios tagged with a requirement the work-item accepts. The option is the
plugin's own pytest plugin, scripts/work_items.py, the one `work run` loads in a repository it delivers."""
import pathlib
import sys

SCRIPTS = str(pathlib.Path(__file__).parent / "scripts")
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

pytest_plugins = ["work_items"]
