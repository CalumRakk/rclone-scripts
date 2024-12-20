# Scripts de Sincronización de Carpetas Específicas con Rclone

Este script de Windows Batch automatiza la sincronización de archivos entre una carpeta local y Google Drive utilizando [Rclone](https://rclone.org/).

## Requisitos Previos

Antes de ejecutar el script, se debe tener lo siguiente configurado:

1. **Descargar e Instalar Rclone:**

   - Ve al sitio oficial de [Rclone](https://rclone.org/downloads/) y descarga la versión para Windows.
   - Descomprime el archivo descargado en una carpeta de tu elección. Por ejemplo, puedes descomprimirlo en `C:\rclone`.

2. **Autenticación con Google Drive:**

   - Ejecuta `rclone.exe config` desde la línea de comandos (CMD) para configurar tu cuenta de Google Drive. Sigue las instrucciones para autenticar tu cuenta.
   - Asegúrate de completar el proceso y guardar la configuración, ya que necesitarás usar este perfil de Google Drive dentro del script.

3. **Archivo `basic.bat`:**

   - El archivo `basic.bat` debe ser ejecutado primero para definir las variables de entorno básicas necesarias para el script. Estas variables incluyen:
     - **RCLONE_PATH**: La ruta a tu instalación de Rclone (por ejemplo, `C:\rclone\rclone.exe`).
     - **RCLONE_EXCLUDE_FILE**: Ruta a un archivo de texto que contiene los patrones de archivos o carpetas a excluir de la sincronización.
     - **RCLONE_LOG_FILE**: Ruta del archivo de log donde se registrará la actividad de sincronización.

   **Nota:** Si no tienes el archivo `basic.bat`, puedes crear uno manualmente o seguir el formato del archivo de ejemplo que se proporciona.

4. Crear el Archivo de Configuración del Perfil de Google Drive para Sincronizar una Carpeta Específica

Para sincronizar una carpeta local con Google Drive, crea un archivo de configuración (ej: `user.txt`) dentro de la carpeta `config/`. Cada archivo de configuración debe incluir las siguientes variables:

- **LOCAL_DIR**: Ruta de la carpeta local que deseas sincronizar.
  - Ejemplo: `LOCAL_DIR=D:\mis videos`
- **REMOTE_DIR**: Ruta remota en Google Drive donde se sincronizarán los archivos. **"NAME_REMOTE"** es el nombre del remote configurado previamente con `rclone.exe config`.
  - Ejemplo: `REMOTE_DIR=NAME_REMOTE:/rclone/mis videos`
- **BACKUP_DIR**: Ruta remota para almacenar las versiones anteriores de los archivos (opcional).
  - Ejemplo: `BACKUP_DIR=NAME_REMOTE:/rclone/backup`

### Ejemplo de un Archivo de Configuración Completo

```text
LOCAL_DIR=D:\mis videos
REMOTE_DIR=NAME_REMOTE:/rclone/mis videos
BACKUP_DIR=NAME_REMOTE:/rclone/backup
```

## Instrucciones para Ejecutar el Script

De esta forma, puedes sincronizar tus carpetas de forma manual o automatizada

1. **Ejecutar de Forma Manual**  
   Abre una ventana de comandos (cmd), navega al directorio donde se encuentra el script `run.bat` y ejecútalo escribiendo:

   ```cmd
   run.bat
   ```

2. **Configurar como Tarea Programada en Windows**  
   Si deseas que el script se ejecute automáticamente en intervalos regulares, puedes configurarlo como una tarea en el Programador de Tareas de Windows:
   - Abre el **Programador de Tareas** (Task Scheduler).
   - Crea una nueva tarea básica y selecciona **Iniciar un programa** como acción.
   - Indica la ruta del script `run.bat`.
   - Define la frecuencia y el horario de ejecución según tus necesidades.
