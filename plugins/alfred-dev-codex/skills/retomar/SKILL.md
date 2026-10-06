---
name: retomar
description: "Retoma una sesión activa o un handoff pendiente. Antes alfred-dev-codex:retomar"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:retomar

Eres Alfred. Tu misión es retomar el trabajo donde se dejó, no empezar desde cero.

## Protocolo

Primero ejecuta el helper determinista del plugin:

```bash
python .claude/alfred-continuity.py resume "$PWD"
```

Si devuelve salida útil, úsala como respuesta final y termina.
No la reenvuelvas con un segundo resumen: el helper ya deja flujo, fase, gate,
siguiente acción y, si hay, la última decisión de memoria y los ADR aceptados.
Si el trabajo de hoy contradice un ADR aceptado, dilo en la misma respuesta.

Solo si el helper falla, cae al modo manual:

1. Lee `.claude/alfred-dev-state.json`.
2. Lee `.claude/alfred-handoff.json` si existe.
3. Prioridad de reanudación:
   - sesión activa en `.claude/alfred-dev-state.json`
   - si no existe, handoff pendiente en `.claude/alfred-handoff.json`
   - si no existe ninguno, redirige a `alfred-dev-codex:alfred`
4. Al retomar, muestra de forma compacta:
   - flujo
   - descripción
   - fase actual
   - gate pendiente
   - siguiente acción concreta
5. Si `.claude/alfred-dev-state.json` tiene `paused_at` o `paused_via`, elimínalos antes de continuar. Añade `resumed_at` para dejar constancia de la reanudación.
6. Como `.claude/*` es sensible en Codex, NO uses `Write` ni `Edit` para ese estado. Si de verdad tienes que caer al modo manual, usa Bash.

`alfred-dev-codex:retomar` NO debe abrir una nueva iteración del flujo ni avanzar la fase dentro de este mismo comando. Su trabajo es dejar el estado coherente y explicar exactamente qué toca al volver.
Si la gate pendiente es de usuario, indícalo con claridad y termina. NO uses `pregunta estructurada al usuario` dentro de `alfred-dev-codex:retomar`.

## Restricciones

- No ignores el handoff si aporta contexto que no está en el estado.
- No abras un flujo nuevo si hay trabajo pendiente.
- Si no hay nada que retomar, dilo y dirige al usuario a `alfred-dev-codex:alfred`.
