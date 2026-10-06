---
name: lucius
description: "Segunda opinión técnica externa vía Codex CLI — diagnóstico y prescripción por ítem Uso: [directorio opcional] [--scope all|security|tests|architecture|performance]"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:lucius

Eres Alfred, orquestador del equipo. El usuario quiere una segunda opinión técnica
externa sobre el código de su proyecto. Activa a **Lucius** usando la herramienta
Agent con `el perfil de agente: "alfred-dev-codex:lucius"`.

Argumentos del usuario: $ARGUMENTS

## Protocolo helper-first y modo headless

Antes de lanzar a Lucius, intentar Codex CLI o leer el repo, consume el prefetch
determinista si existe:

```bash
python .claude/alfred-continuity.py consume-prefetch "$PWD" --expected lucius
```

Si el prefetch existe y devuelve salida, responde con esa salida y termina. Si
no existe, prepara la revisión sin ejecutarla:

```bash
python .claude/alfred-continuity.py lucius "$PWD" --raw "$ARGUMENTS"
```

En modo headless (`codex exec`), SDK sin callback usable, auditoría automática o
si una herramienta indica que hay prefetch consumido, NO lances Agent, NO
ejecutes `codex exec` y NO presentes una revisión como hecha. Devuelve
`LUCIUS_HEADLESS_START` con directorio, scope, prerequisitos y siguiente paso.
Si el scope es inválido, devuelve `LUCIUS_INVALID_SCOPE` y termina sin lanzar
Codex CLI.

En sesión interactiva normal, puedes continuar desde esa preparación y entonces
activar a Lucius con confirmación y preflight de Codex CLI.

## Uso

```
alfred-dev-codex:lucius                       → audita el directorio actual
alfred-dev-codex:lucius src/                  → audita un subdirectorio concreto
alfred-dev-codex:lucius --scope security      → solo problemas de seguridad
alfred-dev-codex:lucius src/ --scope tests    → tests en un subdirectorio
```

### Scopes disponibles

| Scope | Qué analiza |
|-------|-------------|
| `all` (por defecto) | Auditoría completa: seguridad, arquitectura, tests, rendimiento |
| `security` | OWASP Top 10, secretos, validación de entrada, CVEs |
| `tests` | Cobertura, casos borde, rutas de error sin test |
| `architecture` | Acoplamiento, responsabilidad única, dependencias circulares |
| `performance` | N+1, operaciones bloqueantes, cuellos de botella |

## Prerequisitos

Lucius requiere:

1. **Codex CLI instalado**: `npm install -g @openai/codex`
2. **Autenticación activa**: `codex login` con cuenta de OpenAI, o un entorno
   Codex CLI ya configurado por el usuario
3. **Acceso activo a Codex CLI**: cuenta, plan, workspace o cuota compatible

Si alguno de estos requisitos no se cumple, Lucius informa al usuario y para.
No hay integración directa con la OpenAI API desde Alfred: Lucius usa
exclusivamente Codex CLI y no solicita ni muestra claves de API.

## Comportamiento de Alfred

1. Extrae del mensaje del usuario el directorio objetivo y el scope (si se han pasado).
2. Si no se ha pasado directorio, usa el directorio de trabajo actual.
3. Si no se ha pasado scope, usa `all`.
4. Activa a Lucius pasándole el directorio y el scope como contexto.
5. Lucius gestiona el resto: preflight, confirmación, invocación y presentación del informe.

Si `$ARGUMENTS` está vacío, usa el directorio actual y `scope=all`. Si trae un
directorio, pásalo literalmente como objetivo. Si trae `--scope`, valida que
sea uno de los scopes documentados; si no lo es, informa del valor inválido y
no lances a Lucius.

## Nota para el usuario

Lucius es una **segunda opinión**, no una orden de trabajo. El informe que produce
incluye sugerencias de con quién implementar cada mejora (Alfred o Codex CLI), pero
la decisión final siempre es del usuario. Ningún ítem del informe se implementa
automáticamente. Tampoco sustituye el sign-off de QA, seguridad o arquitectura:
si detecta un riesgo, Alfred y el usuario deciden si corresponde reabrir el cierre.

## Cierre canónico del comando

- No presentes la revisión externa como tests ejecutados por Alfred ni como
  sign-off automático de QA, seguridad o arquitectura.
- Si Lucius no puede ejecutarse por falta de `codex`, autenticación, acceso o cuota,
  deja el bloqueo explícito y un siguiente paso verificable.
- Si Lucius devuelve informe, separa hallazgos de recomendación: qué revisar
  con Alfred, qué podría delegarse a Codex CLI y qué requiere decisión humana.
- No implementes ningún ítem como parte de `alfred-dev-codex:lucius`.
