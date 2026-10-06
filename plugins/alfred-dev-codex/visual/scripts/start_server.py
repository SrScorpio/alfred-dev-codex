#!/usr/bin/env python3
# Port multiplataforma (sin bash) del start-server.sh del companion visual de Selina.
# Uso: python start_server.py [--project-dir RUTA] [--host H] [--url-host H] [--foreground|--background]
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_CJS = os.path.join(SCRIPT_DIR, "server.cjs")


def fail(message):
    print(json.dumps({"type": "error", "message": message}, ensure_ascii=False))
    raise SystemExit(1)


def wait_for_start(proc, log_file):
    for _ in range(50):
        time.sleep(0.1)
        if proc.poll() is not None:
            return None
        try:
            with open(log_file, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if "server-started" in line:
                        try:
                            return json.loads(line)
                        except ValueError:
                            continue
        except OSError:
            pass
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default="")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--url-host", default="")
    parser.add_argument("--foreground", action="store_true")
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args()

    node = shutil.which("node")
    if not node:
        fail("Node.js no esta en PATH")
    if not os.path.isfile(SERVER_CJS):
        fail("No se encontro server.cjs en " + SCRIPT_DIR)

    timestamp = int(time.time())
    token = uuid.uuid4().hex[:8]
    if args.project_dir:
        session_dir = os.path.join(args.project_dir, ".alfred-dev", "visual",
                               str(os.getpid()) + "-" + str(timestamp) + "-" + token)
    else:
        session_dir = os.path.join(tempfile.gettempdir(), "alfred-visual-" + str(os.getpid()) + "-" + str(timestamp) + "-" + token)
    content_dir = os.path.join(session_dir, "content")
    state_dir = os.path.join(session_dir, "state")
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(state_dir, exist_ok=True)
    pid_file = os.path.join(state_dir, "server.pid")
    log_file = os.path.join(state_dir, "server.log")

    env = dict(os.environ)
    env["ALFRED_VISUAL_DIR"] = session_dir
    env["ALFRED_VISUAL_HOST"] = args.host
    if args.url_host:
        env["ALFRED_VISUAL_URL_HOST"] = args.url_host

    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0x08)
    if args.foreground or (os.name == "nt" and not args.background):
        creationflags = 0

    with open(log_file, "ab") as log_fh:
        proc = subprocess.Popen([node, SERVER_CJS], stdout=log_fh, stderr=subprocess.STDOUT,
                                  env=env, creationflags=creationflags)
    with open(pid_file, "w", encoding="utf-8") as fh:
        fh.write(str(proc.pid))

    started = wait_for_start(proc, log_file)
    if started is None:
        try:
            proc.kill()
        except Exception:
            pass
        fail("El servidor no arranco en 5 segundos")
    started["session_dir"] = session_dir
    started["pid_file"] = pid_file
    print(json.dumps(started, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
