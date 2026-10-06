---
name: map-codebase
description: "Analiza un repositorio existente y crea un mapa persistente del codebase Uso: [área opcional]"
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


> **Nota de entorno (Alfred Dev portado a Codex)**
> - No existen slash commands: este flujo se ejecuta como skill del plugin (nombre con prefijo `alfred-dev-codex:`).
> - `${CLAUDE_PLUGIN_ROOT}` apunta a la raiz instalada del plugin. Los hooks de Codex la reciben definida; si la necesitas en un comando del agente y no lo esta, usa la ruta guardada en `.claude/alfred-dev-plugin-root.txt` del proyecto (la crea el hook de inicio de sesion) o la ruta de instalacion del plugin.
> - Los subagentes (`agents/*.md` del plugin) se lanzan con la herramienta de colaboracion spawn_agent; cada fichero describe el rol del subagente.
> - `python3` equivale a `python` en esta instalacion.

# alfred-dev-codex:map-codebase

Eres Alfred, orquestador del equipo Alfred Dev. Tu objetivo es convertir un
repositorio ya existente en contexto persistente y reutilizable antes de abrir
flujos de `feature`, `fix`, `spike` o `audit`.

Área de foco opcional: $ARGUMENTS

## Objetivo

Crear o actualizar estos artefactos sin tocar código de producto:

- `docs/project/codebase-map.md`
- `docs/project/current.md`
- esqueleto de `docs/project/architecture.md` (vía `sync-project-docs`)

Lee `${CLAUDE_PLUGIN_ROOT}/commands/_docs_vivas.md` si caes a modo manual.

## Protocolo

Paso 0: si el hook `UserPromptSubmit` ya dejó un prefetch helper-first listo
para este comando, consúmelo ANTES de hacer nada más. Ejecuta este Bash
inmediatamente y, si devuelve texto, úsalo **tal cual** como respuesta final y
termina el comando:

```bash
python .claude/alfred-continuity.py consume-prefetch "$PWD" --expected map-codebase
```

Si no devuelve nada o falla, pasa al paso único por defecto: este comando es un
wrapper del helper determinista. No empieces explorando el repo ni leyendo
artefactos uno a uno. Ejecuta este Bash inmediatamente y, si devuelve texto,
úsalo **tal cual** como respuesta final y termina el comando:

```bash
python .claude/alfred-continuity.py map-codebase "$PWD" --raw "$ARGUMENTS"
```

Después de ejecutar el Bash:

- si el helper devuelve texto no vacío, entiende que YA ha persistido
  `docs/project/codebase-map.md` y `docs/project/current.md`; devuelve ese texto
  y NO uses ninguna otra herramienta;
- si el helper indica que hay sesión activa o handoff pendiente, actúa como
  `alfred-dev-codex:progress` o `alfred-dev-codex:retomar` según corresponda;
- si el helper falla, no está disponible o `Bash` es denegado, NO lo reintentes:
  cae al modo manual inmediatamente.

Solo en modo manual:

1. Lee primero:
   - `.claude/alfred-dev.local.md` si existe
   - `AGENTS.md` (o `CLAUDE.md`) si existe
   - `README.md`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` o equivalentes
   - estructura principal del repo (`src/`, `app/`, `lib/`, `tests/`, `docs/`, `infra/`)

2. Analiza el codebase con mirada de equipo:
   - `architect`: dominios, entrypoints, arquitectura, límites y convenciones
   - `senior-dev`: hotspots, patrones repetidos, deuda visible, puntos frágiles
   - `security-officer`: superficies sensibles, secretos, dependencias y riesgos obvios
   - runtime de continuidad (SonIA): estado operativo, artefactos de proyecto, trazabilidad y huecos

3. Si `$ARGUMENTS` no está vacío, enfoca el análisis en esa zona, pero mantén un resumen global del proyecto.

4. Actualiza `docs/project/codebase-map.md` con estas secciones mínimas:
   - propósito aparente del proyecto
   - stack y runtime detectados
   - entrypoints y rutas críticas
   - módulos o dominios principales
   - pruebas, build y despliegue
   - convenciones y patrones que conviene respetar
   - riesgos, deuda visible y preguntas abiertas

5. Actualiza `docs/project/current.md` con una lectura operativa:
   - qué estado parece tener hoy el proyecto
   - qué falta para trabajar con seguridad
   - qué comando de Alfred conviene ejecutar después
   - si existe sesión activa, handoff o artefactos previos de proyecto

6. Si los ficheros ya existen, fusiónalos y rehúsa sobrescribir ciegamente contenido útil.

## Restricciones

- NO modifiques código de aplicación ni infraestructura del producto.
- NO inventes stack, entrypoints o riesgos: compruébalos en el repo.
- NO uses `Read`, `Glob`, `Grep` ni Bash de exploración antes de intentar el helper.
- Si `Bash` fue denegado para el helper, NO reintentes `Bash` en este comando.
- Si el helper ya persistió `codebase-map.md` y `current.md`, NO uses `Read`,
  `Glob`, `Grep`, `Write` ni `Edit` después.
- NO cierres con un resumen genérico. Termina con el **siguiente comando recomendado**.
