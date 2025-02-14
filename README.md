# Scripts de Sincronización de Carpetas Específicas con Rclone

Este script de Python automatiza la sincronización de carpetas entre ubicaciones locales y remotas utilizando [Rclone](https://rclone.org/). Permite definir múltiples tareas de sincronización a través de archivos de configuración simples, facilitando la gestión de copias de seguridad y la sincronización de datos.

La ventaja de usar este script es la facilidad de configurar multiples "tareas de sincronizacion" a traves de archivos de texto simple. Este Script lee y ejecuta todas las tareas en lote desde el directorio `tasks`

<!-- Entiendase que una "tarea de sincronización" es un archivo que contiene la configuración específica para sincronizar un directorio local con un remoto utilizando Rclone -->

## Requisitos Previos

Antes de ejecutar el script, se debe tener lo siguiente configurado:

1. **Instalar Rclone**

   - Descarga la última versión desde [Rclone Downloads](https://rclone.org/downloads/).
   - Extrae el archivo en una carpeta, por ejemplo: `C:\rclone`.

2. **Autenticación con Google Drive:**

   - Ejecuta `rclone.exe config` desde la línea de comandos (CMD) para configurar tu cuenta de Google Drive. Sigue las instrucciones para autenticar tu cuenta.
   - Asegúrate de completar el proceso y recuerda el nombre del remoto especificado, ya que necesitarás usar este nombre en el siguiente paso.

3. **Configurar archivos de "tareas de sincronizacion"**
   Crea un archivo `.txt` para cada tarea en la carpeta de tareas (por defecto, `tasks`) con la siguiente configuración en formato clave-valor:

   ```plaintext
   local_dir=/ruta/al/directorio/local
   remote_dir=remote:nombre_remoto
   backup_dir=/ruta/al/directorio/backup
   path_rclone=/ruta/al/ejecutable/rclone
   path_log_file=/ruta/al/archivo/de/log
   path_exclude_file=/ruta/al/archivo/de/exclusiones
   ```

   **Parámetros de Configuración**

   - **`local_dir`**: Ruta absoluta al directorio local que será sincronizado.
   - **`remote_dir`**: Nombre del remoto configurado en Rclone seguido de la ruta donde se almacenarán los datos.  
     Ejemplo: `mi_remoto:/carpeta/destino`.
   - **`backup_dir`**: Carpeta remota para almacenar archivos eliminados durante la sincronización.  
     Ejemplo: `mi_remoto:/carpeta/backup`.
   - **`path_rclone`**: Ruta al ejecutable de Rclone.  
     Ejemplo: `C:\rclone\rclone.exe`.
   - **`path_log_file`**: Ruta del archivo de log generado por Rclone. Este archivo guarda detalles sobre la ejecución de la tarea.  
     Ejemplo: `C:\logs\rclone.log`.
   - **`path_exclude_file`**: (Opcional) Archivo que contiene patrones para excluir archivos o carpetas durante la sincronización.  
     Ejemplo: `config\excludes.txt`
     ```text
     *.tmp
     /CarpetaTemporal/*
     archivo_a_excluir.txt
     ```

   **Ejemplo de un archivo de tarea de sincronizacion Completo**

   ```text
   local_dir=D:\github Leo
   remote_dir=leo:/rclone/github Leo
   backup_dir=leo:/rclone/backup
   path_rclone=C:\rclone-v1.68.2-windows-amd64\rclone.exe
   path_exclude_file=config\excludes.txt
   ```

   Este ejemplo realizará una copia de seguridad de los archivos de la carpeta local `D:\github Leo`, utilizando el nombre del remoto de rclone llamada `leo`. Los archivos se sincronizarán en una carpeta de Google Drive llamada `rclone/github Leo`. Los archivos dentro de la carpeta local especificados en el archivo `path_exclude_file` no serán sincronizados. Además, los archivos eliminados localmente después de ejecutar el script serán movidos a una carpeta remota denominada `rclone/backup` durante la siguiente ejecución.

<!-- ## Cómo usar el script

1.  **Ejecutar manualmente**

    Abre una terminal, navega a la carpeta donde está el script de Python \`run.py\` y ejecuta:

    ```cmd
    python run.py [--tasks-dir <ruta_del_directorio_de_tareas>]
    ```

    Si no se especifica \`--tasks-dir\`, el script buscará los archivos de configuración en el directorio \`tasks\` ubicado en el mismo directorio que el script.

    Si se produce algún error durante la ejecución, revisa los archivos de log (\`script.log\` y el log específico de Rclone para la tarea correspondiente) para obtener más información.

2.  **Configurar como Tarea Programada en Windows**
    Si deseas que el script se ejecute automáticamente en intervalos regulares, puedes configurarlo como una tarea en el Programador de Tareas de Windows:

    - Abre el **Programador de Tareas** (Task Scheduler).
    - Crea una nueva tarea básica y selecciona **Iniciar un programa** como acción.
    - Indica la ruta del script `python <ruta_completa_del_script>`.
    - Define la frecuencia y el horario de ejecución según tus necesidades.

3.  **Ejecución Automática del script usando el Programador de Tareas de Windows**

    Para ejecutar el script automáticamente de forma regular:

    1.  Abre el **Programador de Tareas**.

    2.  Haz clic en "Crear tarea básica...".

    3.  Ponle un nombre (ej. "Sincronización Rclone") y una descripción.

    4.  Elige la frecuencia (diaria, semanal, etc.).

    5.  Selecciona "Iniciar un programa".

    6.  **Configura el programa y los argumentos:**

        - **Si Python _está_ en las variables del sistema (PATH):**

          - **Programa/script:** `python` (o `py`)
          - **Agregar argumentos:** `D:\scripts\rclone_sync\run.py`

        - **Si Python _NO está_ en las variables del sistema o usas un entorno virtual específico:**

          - **Programa/script:** `C:\ruta\completa\a\python.exe` (ej. `C:\Python39\python.exe` o la de tu entorno virtual)
          - **Agregar argumentos:** `D:\scripts\rclone_sync\run.py`

          Puedes encontrar la ruta completa a Python ejecutando `where python` en la terminal.

    7.  Revisa la configuración y finaliza. Revisa los logs (`script.log` y los de Rclone) si hay problemas.

## Notas sobre los logs

1. **Log del script (`script.log`)**
   - Registra las actividades y errores generales del script en Python.
2. **Log de Rclone (`path_log_file`)**
   - Contiene información detallada de cada tarea ejecutada por Rclone. -->
