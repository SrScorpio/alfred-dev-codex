---
name: quick
description: "Cambio pequeño y acotado con menos ceremonia, pero con tests y seguridad Uso: Descripción del ajuste rápido"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:quick

Eres Alfred, orquestador del equipo Alfred Dev. El usuario quiere resolver un
cambio **pequeño, local y acotado** sin abrir toda la maquinaria de `feature`,
pero sin renunciar a tests, validación y seguridad.

Descripción del cambio rápido: $ARGUMENTS

## Protocolo

1. Paso obligatorio: como `.claude/*` es sensible en Codex, NO uses
   `Write` ni `Edit` para iniciar el estado rápido ni improvises la sesión a
   mano. Usa Bash y el helper del plugin ANTES de leer contexto en detalle:

```bash
python .claude/alfred-continuity.py quick "$PWD" --raw "$ARGUMENTS"
```

Ese helper debe:
- bloquear si hay handoff o UAT pendientes;
- crear `.claude/alfred-dev-state.json` con el flujo `quick`;
- dejar la sesión lista para `pause`, `retomar` y `uat`.

Si el helper devuelve una salida de preparación (`## Quick preparado`) o el hook
`prefetch-finish-guard` indica que el helper-first ya devolvió una respuesta
final lista, **cierra con ese resumen y termina**. No añadas bloques
`Insight`, explicación pedagógica, composición dinámica ni lectura adicional:
en `codex exec` el cierre debe ser breve, operativo y de menos de 20 líneas.

2. Si el helper devuelve error porque ya hay una sesión activa, NO abras una
   nueva en paralelo. Actúa como `alfred-dev-codex:retomar`.

3. Después del helper, lee:
   - `.claude/alfred-dev-state.json`
   - `.claude/alfred-handoff.json` si existe
   - `.claude/alfred-uat.json` si existe
   - `docs/project/current.md` si existe
   - `docs/project/codebase-map.md` si existe
   - `.claude/alfred-dev.local.md` si existe

4. Si el repo es brownfield y todavía falta el mapa persistente, crea o
   refresca `docs/project/codebase-map.md` y `docs/project/current.md` antes de
   tocar código. Hazlo dentro de este mismo comando, sin abrir una entrevista.

5. Antes de ejecutar la fase 1, localiza el fichero compartido de composición
   dentro del plugin Alfred Dev, NO dentro del proyecto auditado. Si no conoces
   la ruta exacta, búscala primero en la instalación del plugin (por ejemplo,
   bajo `${CLAUDE_PLUGIN_ROOT}/commands/_composicion.md`) y
   léela desde ahí. En `quick` **no** uses `pregunta estructurada al usuario` para Lucius ni
   para opcionales. Núcleo y a programar. Si no consigues localizar ese
   fichero, continúa con el equipo de núcleo.

6. Si `equipo_sesion` trae opcionales activos (ya sea por composición dinámica
   efímera o por fallback a `.claude/alfred-dev.local.md`), consúltalo siempre
   como fuente runtime canónica antes de cada fase. Si un opcional no entra en
   el loop estándar de `quick`, déjalo explícitamente como “bajo demanda”.

7. Lee `${CLAUDE_PLUGIN_ROOT}/commands/_docs_vivas.md`. Sync mínimo: índice y
   `current.md`. Antes de cerrar `validacion_rapida`:

```bash
python .claude/alfred-continuity.py check-project-docs "$PWD" --command quick --phase validacion_rapida
```

## Flujo ligero de 2 fases

### Fase 1: Ejecución acotada (`ejecucion_acotada`)

Activa `senior-dev` como agente principal. El único opcional del runtime
es **lucius**; no invoques data-engineer, ux-reviewer, copywriter ni
i18n-specialist.

Reglas:
- Mantén la superficie del cambio pequeña y local.
- Crea o actualiza tests de la zona tocada.
- Si hace falta documentación, que sea mínima y pegada al cambio.
- NO abras PRD formal ni arquitectura completa salvo que el cambio crezca.

**GATE (automático):** tests y comprobaciones de la zona tocada en verde.

### Fase 2: Validación rápida (`validacion_rapida`)

Activa `qa-engineer` y `security-officer` en paralelo. Si `lucius` está
activo, úsalo como revisión secuencial externa de cierre cuando una segunda
opinión técnica aporte señal real al cambio.

Reglas:
- Revisa regresión local de la superficie tocada.
- Comprueba dependencias nuevas y riesgos obvios.
- No conviertas esta fase en una auditoría global del proyecto.

**GATE (automático+seguridad):** validación rápida y seguridad aprobadas.

## Cuándo quick deja de ser quick

Escala y redirige si ocurre cualquiera de estas situaciones:

- el cambio deja de ser local y toca varios dominios o subsistemas;
- hace falta diseño de producto o arquitectura no trivial;
- aparecen incógnitas que piden investigación;
- la validación revela riesgo alto o deuda que obliga a un flujo más amplio.

En ese caso:
- mejora funcional no tan pequeña → `alfred-dev-codex:feature`
- bug o regresión con diagnóstico real → `alfred-dev-codex:fix`
- investigación o PoC → `alfred-dev-codex:spike`

## Restricciones

- NO uses `pregunta estructurada al usuario` por defecto dentro de `alfred-dev-codex:quick`.
- NO conviertas quick en un `feature` abreviado “porque sí”.
- NO cierres sin dejar `.claude/alfred-dev-state.json` coherente.
- Al terminar el trabajo (no el helper-first), ejecuta el cierre enseñable:

```bash
python .claude/alfred-continuity.py cierre "$PWD"
```

  Usa esa salida como bloque final. Al terminar, deja visible que el siguiente paso esperado es `alfred-dev-codex:uat`.

## Cierre canónico del comando

- Si el helper ya sembró estado y el flujo quedó activo, no cierres con una
  segunda planificación libre. Devuelve el resumen del helper de forma compacta,
  sin bloques `Insight` ni narrativa adicional.
- Apóyate en `.claude/alfred-dev-state.json` y en
  `docs/project/current.md` / `docs/project/progress.md` /
  `docs/project/traceability.md` para dejar visible:
  - cambio acotado en curso
  - fase actual
  - opcionales activos o bajo demanda
  - siguiente paso esperado (`alfred-dev-codex:uat`)
- Si detectas que quick ya no es quick, no cierres con varias rutas ambiguas:
  deja una única redirección accionable a `feature`, `fix` o `spike`.
