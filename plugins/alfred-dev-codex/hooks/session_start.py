#!/usr/bin/env python3
# SessionStart (fail-open): inyecta el briefing de Alfred como additionalContext.
# Port multiplataforma (sin bash) del session-start.sh original.
from __future__ import annotations

import json
import os
import sys

FALLBACK = "## Como hablarle a Alfred\n\nSi el usuario describe trabajo, un bug, retomar, entregar o preguntar que toca sin invocar una skill,\nactua como la skill alfred-dev-codex:alfred: elige la ruta y ejecutala. No ofrezcas el catalogo.\n\nRuta principal: alfred-dev-codex:alfred. Flujos: alfred-dev-codex:feature, alfred-dev-codex:quick, alfred-dev-codex:fix,\nalfred-dev-codex:spike, alfred-dev-codex:audit, alfred-dev-codex:ship. Estado: alfred-dev-codex:progress. Continuar: alfred-dev-codex:retomar.\n\nSi hay colaboracion multi-agente disponible, usala para fases en paralelo (spawn_agent con los perfiles\nde agents/<nombre>.md del plugin). No reescribas la configuracion global del agente.\n\n## Briefing\n\nNo hay sesion abierta. Pregunta que quiere hacer o mapea el repo si es brownfield."


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)
    project_dir = os.getcwd()
    context = ""
    try:
        from core.session_brief import render_session_start_context
        context = render_session_start_context(project_dir)
    except Exception as exc:
        print("[session-start] aviso: " + str(exc), file=sys.stderr)
    if not context or not context.strip():
        context = FALLBACK
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }, ensure_ascii=False))
    return 0


try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
except Exception:
    pass


if __name__ == "__main__":
    raise SystemExit(main())
