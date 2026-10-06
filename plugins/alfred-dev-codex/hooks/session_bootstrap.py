#!/usr/bin/env python3
# SessionStart (fail-open): prepara artefactos locales del proyecto.
# Port multiplataforma (sin bash) del session-bootstrap.sh original.
from __future__ import annotations

import json
import os
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

WRAPPER_TEMPLATE = "#!/usr/bin/env python3\nimport os\nimport sys\nfrom pathlib import Path\n\nEMBEDDED_PLUGIN_ROOT = {{ROOT}}\nPLUGIN_NAME = \"alfred-dev\"\n\n\ndef _valid_root(path):\n    if not path:\n        return None\n    root = Path(path).expanduser()\n    try:\n        root = root.resolve()\n    except OSError:\n        root = root.absolute()\n    if (root / \"core\" / \"continuity.py\").is_file():\n        return str(root)\n    return None\n\n\ndef _resolve_plugin_root():\n    candidates = [\n        os.environ.get(\"CLAUDE_PLUGIN_ROOT\"),\n        os.environ.get(\"ALFRED_DEV_PLUGIN_ROOT\"),\n        os.environ.get(\"PLUGIN_ROOT\"),\n        EMBEDDED_PLUGIN_ROOT,\n    ]\n    for candidate in candidates:\n        resolved = _valid_root(candidate)\n        if resolved:\n            return resolved\n    sys.stderr.write(\"[Alfred Dev] No se pudo resolver la instalacion activa del plugin.\\n\")\n    raise SystemExit(2)\n\n\nPLUGIN_ROOT = _resolve_plugin_root()\nif PLUGIN_ROOT not in sys.path:\n    sys.path.insert(0, PLUGIN_ROOT)\n\nfrom core.continuity import main\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n"


def _plugin_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    project_dir = os.getcwd()
    root = _plugin_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    local_dir = os.path.join(project_dir, ".claude")
    os.makedirs(local_dir, exist_ok=True)
    with open(os.path.join(local_dir, "alfred-dev-plugin-root.txt"), "w", encoding="utf-8") as fh:
        fh.write(root)
    local_config = os.path.join(local_dir, "alfred-dev.local.md")
    memory_db = os.path.join(local_dir, "alfred-memory.db")
    wrapper = os.path.join(local_dir, "alfred-continuity.py")
    try:
        from core.config_loader import ensure_bootstrap_local_config
        ensure_bootstrap_local_config(local_config)
    except Exception:
        pass
    memory_enabled = False
    try:
        from core.memory_config import is_memory_enabled
        memory_enabled = bool(is_memory_enabled(project_dir))
    except Exception:
        pass
    if memory_enabled and not os.path.isfile(memory_db):
        try:
            from core.memory import MemoryDB
            MemoryDB(memory_db).close()
        except Exception as exc:
            print("[Alfred Dev] Aviso: no se pudo crear la BD de memoria: " + str(exc), file=sys.stderr)
    try:
        source = WRAPPER_TEMPLATE.replace("{{ROOT}}", repr(root))
        with open(wrapper, "w", encoding="utf-8") as fh:
            fh.write(source)
        try:
            os.chmod(wrapper, 0o755)
        except OSError:
            pass
    except Exception as exc:
        print("[Alfred Dev] Aviso: no se pudo preparar el wrapper de continuidad: " + str(exc), file=sys.stderr)
    if memory_enabled and os.path.isfile(memory_db):
        try:
            from core.memory import MemoryDB
            db = MemoryDB(memory_db)
            if db.get_active_iteration() is None:
                iteration_id = db.start_iteration(command="session", description="Sesion de trabajo general")
                db.log_event(event_type="session_started", payload={"source": "session-bootstrap.py"}, iteration_id=iteration_id)
            db.close()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
