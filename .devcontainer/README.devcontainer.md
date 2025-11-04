# Cómo usar el Dev Container

Este repositorio incluye configuración para abrir el proyecto dentro de un Dev Container (VS Code Remote - Containers).

Requisitos previos
- Docker Desktop instalado y corriendo (Windows: usar WSL2 backend recomendado).
- VS Code con la extensión "Dev Containers" (Remote - Containers) instalada.
- Extensiones recomendadas: Python (ms-python.python), Pylance (ms-python.vscode-pylance).

Abrir el proyecto en el contenedor
1. Abre la carpeta del proyecto en VS Code.
2. Abre la paleta de comandos (Ctrl+Shift+P) y ejecuta:
   - "Dev Containers: Reopen in Container"  
   o
   - "Dev Containers: Open Folder in Container..." y selecciona la carpeta del repo.

Qué hace la configuración
- Usa la imagen oficial de devcontainers para Python (`mcr.microsoft.com/devcontainers/python:3.12`).
- Ejecuta `pip install -r requirements.txt` después de crear el contenedor (postCreateCommand).
- Instala las extensiones de VS Code configuradas automáticamente.

Después de abrir el contenedor
- El intérprete de Python de VS Code se seleccionará automáticamente (asegúrate en la esquina inferior izquierda).
- Para ejecutar el proyecto desde el contenedor puedes usar la tarea definida en `.vscode/tasks.json` o ejecutar desde la terminal integrada:

```bash
python src/main.py
```

Solución de problemas
- Si la instalación de dependencias falla, abre la terminal integrada del contenedor y ejecuta manualmente:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Si Docker no está corriendo, inicia Docker Desktop.
- En Windows, si tienes problemas con permisos de archivos en OneDrive, considera usar una carpeta fuera de OneDrive o deshabilitar la sincronización para esta carpeta.

Notas
- No puedo iniciar el contenedor desde aquí; debes ejecutar los pasos anteriores en tu máquina con Docker y VS Code.
