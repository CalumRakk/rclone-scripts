@echo off
setlocal enabledelayedexpansion
set CONFIG_DIR=config

for %%F in (%CONFIG_DIR%\*.txt) do (
    echo Leyendo archivo: %%F
    for /f "tokens=1,* delims==" %%A in (%%F) do (
        set %%A=%%B
        echo Se ha asignado: %%A=%%B
    )

    :: Usando las variables leídas
    echo "Usando las variables:"
    echo LOCAL_DIR: !LOCAL_DIR!
    echo REMOTE_DIR: !REMOTE_DIR!
    echo BACKUP_DIR: !BACKUP_DIR!
    echo RCLONE_EXCLUDE_FILE: %RCLONE_EXCLUDE_FILE%
    echo RCLONE_LOG_FILE: %RCLONE_LOG_FILE%
    echo RCLONE_PATH: %RCLONE_PATH%
    
    echo Inician la operación de sincronización...
    start "" /min ^
        "%RCLONE_PATH%" sync ^
        "!LOCAL_DIR!" ^
        "!REMOTE_DIR!" ^
        --exclude-from "%RCLONE_EXCLUDE_FILE%" ^
        --verbose ^
        --progress ^
        --backup-dir !BACKUP_DIR! ^
        --log-file "%RCLONE_LOG_FILE%"

)

pause
