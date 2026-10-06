# Revisión de alfred-dev-codex

Revisión del 6 de octubre de 2026, antes de instalar.

## Cambios verificados

Identidad alfred-dev-codex sincronizada en los manifiestos, prefijos de skills,
instrucciones y carpeta. Metadatos OpenAI bajo extensions.com.openai.interface.
ZIP con una sola carpeta del plugin y sus archivos ocultos.

Lanzadores de hooks con comandos completos, rutas entre comillas y variantes
PowerShell. Secretos y actividad compatibles con apply_patch usando el campo
canónico tool_input.command. Rutas de SonarQube corregidas. Helpers visuales con
Python explícito y raíz instalada. Lucius incluye variante PowerShell. Variables
de ejemplo, perfiles de agente y descubrimiento MCP documentados para Codex.
Las recomendaciones de resume/next/search se redirigen a las skills publicadas
retomar/progress/memory. Las actualizaciones no reemplazan el port con upstream.

## Evidencia

- Validación de propiedades obligatorias y permitidas del esquema del manifiesto,
  identidad, versiones y metadatos; YAML real de las 29 skills y 10 perfiles.
- Todos los archivos Python pasan análisis sintáctico.
- Regresión de hooks: parches canónicos con y sin secretos, captura de actividad,
  bloqueo de comandos peligrosos y comprobación de lanzadores.
- Ejecución real de SessionStart con los comandos Windows desde un proyecto
  temporal cuya ruta contiene espacios; wrapper y contexto JSON correctos.
- MCP: inicialización, listado de 15 herramientas y llamada real memory_stats
  con base de datos dentro de un proyecto temporal.
- Suite seleccionada de memoria, orquestación, personalidad y configuración:
  244 casos, 239 pasan y 5 omitidos por asumir permisos POSIX 0600 en Windows.
  Las expectativas de nombres y separadores de ruta se adaptaron al port;
  los tests se ejecutan en una copia temporal, sin instalar el plugin.
- ZIP verificado por lista, bytes y CRC; sin cachés ni datos de prueba.

## Alcance pendiente

No se ha probado la instalación y carga del paquete dentro de Codex ni una
sesión de trabajo completa. Tampoco se ejecutaron despliegues, Docker/SonarQube,
autenticación de GitHub ni una auditoría externa de Lucius.

El chequeo de permisos del original espera POSIX 0600. Windows utiliza ACL:
memory_health puede mostrar una advertencia aunque la memoria funcione.
Esta revisión no certifica las ACL ni modifica permisos del usuario.

El MCP es local y requiere Python. El ZIP no proporciona un servicio remoto
para ChatGPT web o móvil. Los hooks requieren soporte y confianza del cliente.
