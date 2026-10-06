---
name: update
description: Comprobar novedades del repositorio original y planificar una actualización del port alfred-dev-codex sin reemplazarlo por código de Claude Code.
---

> **Integración con Codex:** sigue `CODEX-COMPATIBILITY.md` en la raíz instalada antes de ejecutar este flujo. `$ARGUMENTS` es el texto de la petición, no una variable de shell; resuelve la raíz y adapta los ejemplos a PowerShell cuando corresponda. Los perfiles de agente son instrucciones para subagentes disponibles y los nombres MCP deben descubrirse en el cliente.


# Actualizar alfred-dev-codex

Lee la versión del plugin.json de esta instalación. Consulta, si hay acceso de red,
la última release de https://github.com/686f6c61/alfred-dev y compara sus versiones
como tuplas numéricas, sin ejecutar texto recibido de GitHub.

Este paquete es una adaptación local: una release del original no constituye
una actualización compatible con Codex. Muestra las novedades y explica qué
componentes necesitan volver a portarse. Si el usuario pide actualizar, descarga
la versión fuente en una carpeta temporal, compara contra la base original,
adapta los cambios conservando las correcciones de Codex y las decisiones locales,
y valida manifiestos, instrucciones, hooks y memoria antes de empaquetar.

Entrega una carpeta alfred-dev-codex y su ZIP. No sobrescribas una instalación
activa ni ejecutes git pull sobre este paquete como sustituto de la adaptación.
Instala o recarga el resultado únicamente cuando el usuario lo solicite.
