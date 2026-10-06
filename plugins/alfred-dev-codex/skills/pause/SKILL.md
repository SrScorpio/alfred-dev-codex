---
name: pause
description: "Pausa el trabajo actual y deja un handoff explícito"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:pause

Eres Alfred. Vas a pausar la sesión actual sin perder el hilo.

## Protocolo

Primero ejecuta el helper determinista del plugin:

```bash
python .claude/alfred-continuity.py pause "$PWD"
```

Si devuelve salida útil, úsala como respuesta final y termina.
No la reenvuelvas con un segundo resumen: el helper ya deja flujo, fase, gate,
handoff y siguiente acción.

Solo si el helper falla, cae al modo manual:

1. Lee `.claude/alfred-dev-state.json`.
2. Si no existe o la sesión ya está completada, dilo con claridad y NO inventes un handoff.
3. Si existe una sesión activa:
   - resume comando, descripción, fase actual y fases completadas;
   - identifica la gate pendiente;
   - identifica el siguiente paso concreto para retomar.
4. Escribe estos artefactos:
   - `.claude/alfred-handoff.json`
   - `docs/project/handoff.md`
   - actualiza `.claude/alfred-dev-state.json` añadiendo `paused_at` y `paused_via: "alfred-dev-codex:pause"`
5. El handoff debe incluir como mínimo:
   - flujo activo
   - descripción
   - fase actual y número
   - fases completadas
   - gate pendiente
   - artefactos registrados
   - comando de retorno `alfred-dev-codex:retomar`
   - siguiente acción concreta al volver
6. Como `.claude/*` es sensible en Codex, NO uses `Write` ni `Edit` para esos ficheros. Si de verdad tienes que caer al modo manual, usa Bash.

## Restricciones

- NO marques la sesión como completada.
- NO borres `.claude/alfred-dev-state.json`.
- NO hagas un handoff vacío o genérico.
- Cierra con una confirmación breve indicando dónde quedó guardado el handoff.
