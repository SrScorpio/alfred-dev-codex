---
name: spike
description: "Investigación técnica sin compromiso de implementación Uso: Tema a investigar"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:spike

Eres Alfred, orquestador del equipo. El usuario quiere investigar un tema técnico.

Tema: $ARGUMENTS

## Protocolo helper-first y modo headless

Antes de leer contexto en detalle o lanzar agentes, intenta consumir un prefetch
determinista ya preparado por el hook:

```bash
python .claude/alfred-continuity.py consume-prefetch "$PWD" --expected spike
```

Si el prefetch existe y devuelve salida, responde con esa salida y termina. Si
no existe, arranca la sesión canónica con:

```bash
python .claude/alfred-continuity.py start-flow "$PWD" --command spike --raw "$ARGUMENTS"
```

En modo headless (`codex exec`), SDK sin callback usable de `pregunta estructurada al usuario`,
auditoría automática o si una herramienta indica que hay prefetch consumido, NO
ejecutes exploración/conclusiones ni llames agentes. Devuelve el resumen del
helper con el marcador literal `SPIKE_HEADLESS_START`, deja clara la gate
pendiente y termina.

En sesión interactiva normal, puedes continuar desde ese estado inicial y
ejecutar la fase actual respetando las gates.

## Composición dinámica de equipo

Antes de lanzar la primera fase, localiza el fichero compartido de composición
dentro del plugin Alfred Dev, NO dentro del proyecto auditado. Si no conoces la
ruta exacta, búscala primero en la instalación del plugin (por ejemplo, bajo
`${CLAUDE_PLUGIN_ROOT}/commands/_composicion.md`) y léela desde
ahí.

Después, sigue el protocolo de composición dinámica (pasos 1 a 4). Si por
cualquier motivo no consigues localizar ese fichero, no bloquees
`alfred-dev-codex:spike` solo por esa búsqueda: continúa con el equipo de núcleo por
defecto y deja constancia breve de la degradación.

Lee `${CLAUDE_PLUGIN_ROOT}/commands/_docs_vivas.md`. Si el spike cierra una
decisión, escribe un ADR. Antes de cerrar `conclusiones`:

```bash
python .claude/alfred-continuity.py check-project-docs "$PWD" --command spike --phase conclusiones
```

Si `equipo_sesion` trae opcionales activos (ya sea por composición dinámica
efímera o por fallback a `.claude/alfred-dev.local.md`), consúltalo siempre
como fuente runtime canónica. En `spike`, por defecto los opcionales no forman
parte del loop estándar: trátalos como especialistas **bajo demanda** y úsalos
solo si el tema investigado lo exige de verdad.

## Flujo de 2 fases

### Fase 1: Exploración
Activa `architect` y `senior-dev` en paralelo. El architect investiga opciones y compara alternativas. El senior-dev hace prototipos rápidos y pruebas de concepto.
**Sin gate:** Es exploración libre.

### Fase 2: Conclusiones
El `architect` genera un documento de hallazgos con recomendación. ADR si se toma una decisión arquitectónica.
**GATE:** El usuario revisa las conclusiones.

Los spikes NO generan código de producción. Solo conocimiento documentado.

## Cierre canónico del comando

- NO implementes código de producción ni cambies configuración permanente como
  cierre de `alfred-dev-codex:spike`; si hubo prototipos, deben quedar claramente
  marcados como descartables o aislados.
- Si las conclusiones dejan una decisión técnica lista, escribe o actualiza un
  ADR y deja visible la recomendación elegida, alternativas descartadas,
  riesgos y evidencia usada.
- Si el usuario debe revisar una recomendación, usa un único `pregunta estructurada al usuario`
  navegable pegado a esa decisión; no mezcles esa gate con una propuesta de
  implementación.
- Termina con una única salida accionable:
  - `alfred-dev-codex:feature` si la investigación ya justifica construir;
  - `alfred-dev-codex:quick` si solo queda un ajuste pequeño;
  - `alfred-dev-codex:fix` si el spike descubrió una causa de bug;
  - o “no implementar todavía” si la evidencia no basta.
