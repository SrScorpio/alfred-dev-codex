# Integración con Codex

Estas reglas se aplican a todas las skills y perfiles de este paquete.

- Resuelve la raíz instalada desde el contexto de la skill o desde PLUGIN_ROOT.
  Para herramientas de shell, PLUGIN_ROOT puede no estar exportado: usa la ruta
  absoluta de la instalación visible en el contexto; en los hooks Codex sí la define.
  CLAUDE_PLUGIN_ROOT es un alias de compatibilidad; no uses esa variable como si
  fuera una variable nativa de PowerShell. En PowerShell los entornos son $env:NOMBRE.
- $ARGUMENTS representa el texto de la petición del usuario; Codex no lo rellena
  como variable de shell. Sustitúyelo por los valores concretos que has entendido,
  usando argumentos separados o la cita correcta del shell. Nunca ejecutes texto
  del usuario o de una respuesta remota mediante evaluación de shell.
- $PWD representa el directorio del proyecto. En PowerShell usa (Get-Location).Path.
  Adapta los ejemplos bash a la plataforma real. Ejecuta los helpers .py con python
  y rutas absolutas; no dependas de bash, /dev/null, heredocs ni permisos ejecutables.
- Task y los agentes alfred/selina/lucius describen responsabilidades, no herramientas
  ni agent_type registrados. Usa spawn_agent con un tipo disponible y transmite el
  perfil de agents/<nombre>.md como instrucciones. Si no hay delegación, realiza
  las fases secuencialmente. No crees chats de usuario para simular subagentes.
- Descubre las herramientas MCP disponibles de alfred-memory antes de invocarlas.
  Los nombres mcp__alfred-memory__memory_* son orientativos: el cliente puede
  normalizar guiones o añadir namespaces. Usa el nombre real y su esquema real.
- Sigue siempre las autorizaciones, permisos y restricciones del usuario y del
  cliente. El plugin no autoriza instalaciones, mensajes, despliegues o cambios
  globales adicionales por sí mismo.
- La memoria conserva los nombres internos de Alfred del original. Cambiar el
  nombre del paquete no debe migrar o borrar bases de datos de los proyectos.
