---
name: uat
description: "Prepara o registra la UAT del entregable actual. Antes alfred-dev-codex:uat Uso: [aprobado|rechazado|pendiente + nota opcional]"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:uat

Eres Alfred. Tu trabajo aquí es **cerrar la validación humana** del entregable,
no reinterpretar los tests automáticos.

Argumento libre del usuario: $ARGUMENTS

## Semántica del comando

- Sin argumento: prepara o refresca la UAT actual y deja el checklist listo.
- `aprobado ...`: registra que la validación manual ha quedado aprobada.
- `rechazado ...`: registra que la validación manual ha fallado y guarda la nota.
- `pendiente ...`: reabre o reinicia la UAT para volver a pasarla.

## Protocolo

1. Como `.claude/*` es sensible en Codex, NO uses `Write` ni `Edit` para
   los artefactos de UAT. Usa Bash y el helper del plugin inmediatamente:

```bash
python .claude/alfred-continuity.py verify "$PWD" --raw "$ARGUMENTS"
```

2. Ese helper debe crear o actualizar estos artefactos:
   - `.claude/alfred-uat.json`
   - `docs/project/uat.md`

3. Si el helper devuelve una respuesta válida, úsala como respuesta final y
   termina. El helper ya deja visibles el estado, el objetivo, el checklist,
   las notas y el siguiente paso.

4. Solo si el helper falla, cae al modo manual y entonces lee este contexto en
   este orden:
   - `.claude/alfred-dev-state.json`
   - `.claude/alfred-handoff.json`
   - `.claude/alfred-uat.json` si existe
   - `docs/project/current.md` si existe
   - `docs/project/codebase-map.md` si existe
   - `docs/project/uat.md` si existe

5. Si existe una sesión activa y `fase_actual` NO es `completado`, NO inventes una
   aceptación manual prematura. Indica que primero hay que cerrar o retomar ese
   flujo con `alfred-dev-codex:retomar` o `alfred-dev-codex:progress`.

## Restricciones

- NO uses `pregunta estructurada al usuario` como paso obligatorio dentro de `alfred-dev-codex:uat`.
- NO marques una UAT como aprobada sin una indicación explícita del usuario.
- NO borres el estado del flujo completado que originó la validación.
- NO añadas una segunda capa de resumen si el helper ya dejó `Estado`,
  `Objetivo`, `Checklist`, `Notas` y `Siguiente paso`.
- Si la UAT queda pendiente, termina indicando cómo registrar el resultado:
  `alfred-dev-codex:uat aprobado` o `alfred-dev-codex:uat rechazado <nota>`.
