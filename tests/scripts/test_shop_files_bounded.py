"""b59: shop_files.bounded ends past its timeout even when a process outside the killed group (one that started its own
session, as an ssh ControlPersist master forked by a push does) still holds the command's pipes open."""
import os
import signal
import sys
import time

import shop_files

# The command forks a child in a session of its own that keeps stdout and stderr, writes its pid and sleeps; the
# command itself sleeps too, so `bounded`'s timeout kills its group but not the child.
HOLDER = (
    "import subprocess, sys, time\n"
    "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], start_new_session=True)\n"
    "open(sys.argv[1], 'w').write(str(child.pid))\n"
    "time.sleep(60)\n"
)


def test_bounded_ends_when_a_process_outside_its_group_holds_its_pipes(tmp_path):
    pidfile = tmp_path / "holder.pid"
    began = time.monotonic()
    try:
        done = shop_files.bounded([sys.executable, "-c", HOLDER, str(pidfile)], tmp_path, dict(os.environ), 1)
        took = time.monotonic() - began
    finally:
        if pidfile.exists() and pidfile.read_text().strip():
            try:
                os.kill(int(pidfile.read_text()), signal.SIGKILL)
            except ProcessLookupError:
                pass
    assert done is None
    assert took < 10, "bounded waited %.1f s for pipes a process outside its group holds" % took


def test_bounded_gives_back_a_command_that_ends_in_time(tmp_path):
    done = shop_files.bounded([sys.executable, "-c", "print('ok')"], tmp_path, dict(os.environ), 10)
    assert done.returncode == 0
    assert done.stdout == "ok\n"
