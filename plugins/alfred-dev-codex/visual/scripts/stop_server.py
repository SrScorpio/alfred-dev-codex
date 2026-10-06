#!/usr/bin/env python3
# Port multiplataforma (sin bash) del stop-server.sh del companion visual de Selina.
# Uso: python stop_server.py <session_dir>
import json
import os
import shutil
import signal
import sys
import tempfile
import time


def status(kind, error=None):
    payload = {"status": kind}
    if error:
        payload["error"] = error
    print(json.dumps(payload, ensure_ascii=False))


def cleanup(session_dir):
    shutil.rmtree(os.path.join(session_dir, "state"), ignore_errors=True)
    if os.path.basename(session_dir).startswith("alfred-visual-"):
        shutil.rmtree(session_dir, ignore_errors=True)


def main() -> int:
    if len(sys.argv) < 2:
        status("failed", "Uso: stop_server.py <session_dir>")
        return 1
    session_dir = sys.argv[1]
    if not os.path.isdir(session_dir):
        status("not_running")
        return 0
    pid_file = os.path.join(session_dir, "state", "server.pid")
    if not os.path.isfile(pid_file):
        status("not_running")
        return 0
    try:
        with open(pid_file, encoding="utf-8") as fh:
            pid = int(fh.read().strip())
    except (OSError, ValueError):
        status("not_running")
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
    except (OSError, SystemError):
        status("not_running")
        cleanup(session_dir)
        return 0
    stopped = False
    for _ in range(20):
        time.sleep(0.1)
        try:
            os.kill(pid, 0)
        except (OSError, SystemError):
            stopped = True
            break
    if not stopped:
        try:
            os.kill(pid, signal.SIGKILL if os.name != "nt" else signal.SIGTERM)
        except (OSError, SystemError):
            pass
    status("stopped")
    cleanup(session_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
