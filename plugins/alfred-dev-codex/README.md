# alfred-dev-codex

Adaptación local para Codex de [alfred-dev](https://github.com/686f6c61/alfred-dev),
basada en la versión 0.7.0. Conserva las 29 skills, los 10 perfiles de agente,
el servidor MCP de memoria con 15 herramientas y los flujos de desarrollo originales.
La identidad del paquete es **alfred-dev-codex**.

## Uso

Una vez instalado en un cliente compatible, pide por ejemplo:

- Usa alfred-dev-codex:alfred para empezar esta tarea.
- Usa alfred-dev-codex:map-codebase para explorar el proyecto.
- Usa alfred-dev-codex:progress para consultar su estado.

El ZIP contiene una sola carpeta alfred-dev-codex, incluidos los archivos ocultos
de compatibilidad. El paquete se entrega sin instalar. No incluye un catálogo
de distribución adicional.

## Requisitos y alcance

Python 3.11 o superior, disponible como python. Node.js es necesario para la
vista visual de Selina; git y gh se usan en los flujos que trabajan con GitHub.
Lucius necesita una instalación de la CLI de Codex.

Es un plugin local: el servidor MCP se ejecuta en el equipo donde trabaja Codex.
Subir el archivo a una cuenta no convierte este proceso local en un servidor
disponible en ChatGPT web o móvil.

Los comandos de Claude Code se adaptaron a skills; los scripts de arranque en
bash se sustituyeron por Python; los perfiles se usan como instrucciones para
los subagentes disponibles en Codex. No son tipos de agente registrados.
Las instrucciones específicas del cliente están en CODEX-COMPATIBILITY.md.

Se conservan los nombres internos .claude/alfred-dev.local.md y otros archivos
de estado del original para mantener el formato de memoria y configuración.
La identidad visible y los prefijos de skills usan alfred-dev-codex.

Los hooks requieren que el cliente soporte su ejecución y que el usuario revise
y confíe en su definición al instalar. La comprobación de ficheros y pruebas
locales no sustituye una prueba de carga completa dentro de Codex.

## Actualizaciones y autoría

El repositorio original sigue dirigido a Claude Code. Las actualizaciones
requieren adaptar de nuevo sus cambios, no reemplazar esta carpeta con el original.
Autor original: 686f6c61. Se conserva la licencia MIT y sus avisos originales.
