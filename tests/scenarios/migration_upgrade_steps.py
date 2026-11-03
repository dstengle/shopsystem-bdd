"""What is left of migration-tools' upgrade steps: the plugin's root, which requests_session_steps.py imports as
PLUGIN. migration-tools' scenarios run through migration_tools_handlers.py; this module goes when nothing imports it."""
import pathlib

PLUGIN = pathlib.Path(__file__).resolve().parents[2]
