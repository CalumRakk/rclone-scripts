from rclone_tasks.task import Task
from pathlib import Path
import logging
import argparse
import subprocess
import re

parser = argparse.ArgumentParser(description="Sincroniza archivos con rclone.")
parser.add_argument(
    "--tasks-dir", type=str, default="tasks", help="Directorio de tareas."
)
parser.add_argument(
    "--log-script", type=str, default="logs/script.log", help="Log del script."
)
args = parser.parse_args()

path_script_log = Path(args.log_script)
if not path_script_log.parent.exists():
    path_script_log.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=path_script_log,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s - %(message)s",
    datefmt="%d-%m-%Y %I:%M:%S %p",
    level=logging.INFO,
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


def main(task: Task):
    logger.info("".join(["-" for i in range(75)]))
    errors = [
        (
            not task.local_dir.exists(),
            f"El directorio local {task.local_dir} no existe.",
        ),
        (
            not task.path_rclone.exists(),
            f"El ejecutable de rclone {task.path_rclone} no existe.",
        ),
        (
            not re.match("^.*:", task.remote_dir),
            f"El directorio remoto {task.remote_dir} no es válido.",
        ),
        (
            task.path_exclude_file is not None and not task.path_exclude_file.exists(),
            f"El archivo de exclusión {task.path_exclude_file} no existe.",
        ),
    ]
    errors = [message for condition, message in errors if condition]
    if errors:
        [logger.error(msg) for msg in errors]
        return

    try:
        logger.info(f"Procesando la tarea {task.task_path}...")
        command = [
            f"{task.path_rclone}",
            "sync",
            f"{task.local_dir}",
            task.remote_dir,
            "--verbose",
            "--progress",
            "--log-file",
            f"{task.path_log_file}",
        ]
        if task.path_exclude_file is not None:
            logger.info(f"Usando el archivo de exclusión: {task.path_exclude_file}")
            command.append(f"--exclude-from")
            command.append(str(task.path_exclude_file))
        if task.backup_dir is not None:
            logger.info(f"Usando el directorio de respaldo: {task.backup_dir}")
            command.append(f"--backup-dir")
            command.append(task.backup_dir)
        if task.extra_command is not None:
            logger.info(f"Usando los comandos extras: {task.extra_command}")
            comms = task.extra_command.strip().split(",")
            for i in comms:
                com, value = i.split()
                command.append(com)
                command.append(value)

        logger.info(f"Ejecutando comando: {' '.join(command)}")
        subprocess.run(
            command,
            shell=True,
            check=True,
        )

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar rclone: {e}")


if __name__ == "__main__":
    logger.info("-------------------- Inicio del script --------------------")
    tasks_dir = Path(args.tasks_dir)
    if not tasks_dir.exists():
        logger.error(f"El directorio de tareas {tasks_dir} no existe.")
        exit()
    for file in Path(tasks_dir).glob("*.txt"):
        task = Task.from_filepath(file)
        main(task)
