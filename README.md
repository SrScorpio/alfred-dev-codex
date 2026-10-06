# Alfred Dev para Codex

> **Este proyecto es un port y no existiría sin el trabajo original de [alfred-dev](https://github.com/686f6c61/alfred-dev), creado por [686f6c61](https://github.com/686f6c61).** El concepto, los agentes y sus personalidades, los flujos de ingeniería, las comprobaciones de calidad y la documentación viva proceden de su obra. El mérito del diseño original corresponde a su autor.

El diseño de Alfred, sus flujos de ingeniería, perfiles, memoria y herramientas proceden del proyecto original. Este repositorio mantiene el crédito y la licencia MIT del autor y adapta su integración con Claude Code al entorno de Codex.

La adaptación se publica como **`alfred-dev-codex`** y parte de alfred-dev **0.7.0**. No es una distribución oficial del autor original ni tiene afiliación con OpenAI. Los cambios de upstream no se incorporan automáticamente: requieren revisar y adaptar la integración.

## Qué ofrece

Alfred organiza el trabajo de desarrollo en fases: comprender el proyecto, definir el cambio, implementarlo, comprobarlo y preparar su entrega. Incluye:

- **29 skills** para desarrollo, revisión, seguridad, documentación y continuidad.
- **10 perfiles de agente** con responsabilidades de producto, arquitectura, desarrollo, QA, seguridad, operaciones y documentación.
- **Memoria local mediante MCP**, con 15 herramientas `memory_*`.
- **Hooks** para contexto de sesión, captura de actividad y comprobaciones de secretos, comandos peligrosos y evidencias.
- **Companion visual de Selina**, para los flujos que necesitan trabajar sobre la presentación de una interfaz.

Los perfiles guían a los subagentes disponibles en Codex. Su uso depende de las capacidades que ofrezca el cliente; no registran nuevos tipos de agente.

## Requisitos

- Codex con soporte para plugins y catálogos de plugins.
- **Python 3.11 o superior**, disponible mediante `python`.
- Git y la CLI de GitHub (`gh`) para los flujos que trabajan con repositorios y GitHub.
- Node.js para el companion visual de Selina.
- La CLI de Codex para las revisiones de Lucius que la utilizan.

El servidor de memoria se ejecuta en tu equipo. Este paquete no proporciona un servidor remoto para ChatGPT web o móvil. Las herramientas adicionales, como Docker o SonarQube, solo son necesarias para los flujos que las invocan.

## Instalación

Este repositorio incluye un catálogo con un único plugin. El catálogo facilita encontrar e instalar el paquete; no implica su inclusión en un directorio oficial de complementos.

Registra el repositorio y añade el plugin:

```text
codex plugin marketplace add SrScorpio/alfred-dev-codex
codex plugin add alfred-dev-codex@alfred-dev-codex
```

Si prefieres usar una copia local:

```text
git clone https://github.com/SrScorpio/alfred-dev-codex.git
codex plugin marketplace add <ruta-absoluta-del-repositorio>
codex plugin add alfred-dev-codex@alfred-dev-codex
```

Sustituye `<ruta-absoluta-del-repositorio>` por la carpeta clonada y utiliza comillas si contiene espacios. Después de instalar, sigue las indicaciones del cliente para cargar el plugin y revisa la definición de sus hooks antes de concederles confianza. Su ejecución requiere soporte y autorización del cliente.

**Estado de instalación:** el paquete y sus componentes se han probado localmente, pero todavía falta verificar la instalación y una sesión completa dentro de Codex. Consulta el [informe de revisión](plugins/alfred-dev-codex/REVIEW.md) para conocer el alcance exacto.

## Primer uso

En el proyecto donde quieras trabajar, pide a Codex que use una skill de Alfred, por ejemplo:

```text
Usa alfred-dev-codex:map-codebase para explorar este proyecto.
Usa alfred-dev-codex:alfred para organizar esta tarea.
Usa alfred-dev-codex:feature para implementar esta funcionalidad.
Usa alfred-dev-codex:progress para consultar el estado del trabajo.
```

Son instrucciones dirigidas a Codex, no comandos de terminal. Los comandos de Claude Code se han convertido en skills; no debes asumir que funcionan como slash commands.

### Skills incluidas

| Área | Skills |
| --- | --- |
| Coordinación y continuidad | `alfred`, `ajustes`, `progress`, `pause`, `retomar`, `update` |
| Desarrollo y exploración | `discuss`, `feature`, `fix`, `quick`, `spike`, `map-codebase`, `uat` |
| Revisión y entrega | `audit`, `lucius`, `ship`, `pr-workflow`, `sync-github`, `sonarqube` |
| Seguridad | `compliance-check`, `evaluate-dependency`, `incident-response`, `sbom-generate`, `threat-model` |
| Memoria, documentación y diseño | `memory`, `memory-ui`, `sync-project-docs`, `write-adr`, `style-direction` |

### Perfiles de agente

`alfred`, `architect`, `devops-engineer`, `lucius`, `product-owner`, `qa-engineer`, `security-officer`, `selina`, `senior-dev` y `tech-writer`.

## Adaptación a Codex

La adaptación conserva los flujos del original y cambia los puntos de integración con el cliente:

- Los comandos se publican como skills con el prefijo `alfred-dev-codex`.
- Los arranques que dependían de Bash disponen de helpers Python y variantes para Windows.
- Los perfiles se transmiten como instrucciones a los mecanismos de delegación disponibles.
- Las herramientas MCP se descubren usando sus nombres reales en el cliente.
- Las instrucciones de actualización evitan reemplazar esta adaptación por el paquete de Claude Code.

Se mantienen algunos nombres internos `.claude/` del original para conservar el formato de configuración, memoria y estado. El nombre público del plugin es `alfred-dev-codex`.

Consulta [CODEX-COMPATIBILITY.md](plugins/alfred-dev-codex/CODEX-COMPATIBILITY.md) para los detalles de variables, rutas, PowerShell, delegación y permisos.

## Estructura del repositorio

```text
.agents/plugins/marketplace.json   Catálogo de instalación
plugins/alfred-dev-codex/          Paquete del plugin
  plugin.json                    Manifiesto
  .codex-plugin/                 Integración con Codex
  skills/                        29 skills
  agents/                        10 perfiles
  hooks/                         Hooks y guardas
  core/                          Motor de Alfred
  mcp/                           Servidor de memoria local
  templates/                     Plantillas
  visual/                        Companion visual
```

## Validación y límites

Puedes ejecutar las pruebas reproducibles del paquete desde la raíz del repositorio:

```text
python -m unittest discover -s tests -v
```

Comprueban la identidad del catálogo, los manifiestos, la sintaxis Python, los lanzadores y el comportamiento de los guardas con entradas de Codex. Estas seis pruebas pasan en el entorno local de preparación.

La revisión local comprobó manifiestos, frontmatter, rutas, sintaxis Python, arranque de sesión, guardas y memoria MCP. La suite seleccionada del motor, adaptada a los nombres y rutas del port, dio **239 pruebas correctas y 5 omitidas** por expectativas de permisos POSIX que no se aplican igual en Windows.

Esto no certifica una sesión completa dentro de Codex. Tampoco se han validado todos los servicios externos, despliegues o revisiones remotas. El [informe de revisión](plugins/alfred-dev-codex/REVIEW.md) documenta la evidencia y lo pendiente.

Los hooks complementan las comprobaciones del cliente; no sustituyen sus permisos ni autorizan por sí mismos mensajes, instalaciones o despliegues. La memoria es local al proyecto y debe tratarse como parte de sus datos.

## Actualizaciones y problemas

Los errores de integración con Codex pueden comunicarse en los [issues de este repositorio](https://github.com/SrScorpio/alfred-dev-codex/issues). Incluye el sistema operativo, versión de Codex y pasos para reproducir el problema, sin compartir secretos ni datos privados del proyecto.

Las nuevas versiones del original requieren una revisión de compatibilidad. No hay sincronización automática con upstream.

## Créditos y licencia

- **Autor original:** [686f6c61](https://github.com/686f6c61).
- **Proyecto original:** [alfred-dev](https://github.com/686f6c61/alfred-dev), diseñado para Claude Code. Su documentación es la referencia para los conceptos y flujos de Alfred; sus instrucciones de instalación corresponden al cliente original.
- **Documentación original:** [alfred-dev.com](https://alfred-dev.com/).
- **Adaptación a Codex:** [SrScorpio](https://github.com/SrScorpio).
- **Adaptación hermana para VS Code:** [alfred-dev-vscode](https://github.com/SrScorpio/alfred-dev-vscode).

Distribuido bajo **MIT**. Se conserva la [licencia del proyecto original](plugins/alfred-dev-codex/LICENSE) y sus avisos de autoría. La publicación de esta adaptación no implica respaldo o participación del creador original.

| Procedencia | Trabajo |
| --- | --- |
| Proyecto original de 686f6c61 | Concepto de Alfred, roles y personalidades, flujos, motor, memoria, herramientas, guardas y plantillas |
| Adaptación de SrScorpio | Empaquetado para Codex, conversión de comandos a skills, integración de hooks y MCP, compatibilidad de lanzadores e instrucciones y catálogo de instalación |

Es una adaptación independiente, no un fork técnico de GitHub. No existe afiliación ni patrocinio del autor original y la integración de cambios de upstream se realiza mediante revisión manual.

Más detalles de procedencia en [UPSTREAM.md](UPSTREAM.md). El aviso MIT original se conserva también en [LICENSE](LICENSE), en la raíz del repositorio.
