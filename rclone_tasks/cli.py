from rclone_tasks.task import Task
from pathlib import Path
import logging
import argparse
import subprocess
import re


def setup_logging(log_path: Path):
    """Configura el sistema de logging."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        filemode="a",
        format="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s - %(message)s",
        datefmt="%d-%m-%Y %I:%M:%S %p",
        level=logging.INFO,
        encoding="utf-8",
    )
    return logging.getLogger(__name__)


def validate_task(task: Task):
    """Valida la configuración de la tarea antes de ejecutarla."""
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
            not re.match(r"^.*:", task.remote_dir),
            f"El directorio remoto {task.remote_dir} no es válido.",
        ),
        (
            task.path_exclude_file and not task.path_exclude_file.exists(),
            f"El archivo de exclusión {task.path_exclude_file} no existe.",
        ),
    ]
    return [msg for condition, msg in errors if condition]


def build_rclone_command(task: Task):
    """Construye el comando de rclone a ejecutar."""
    logger = logging.getLogger(__name__)
    command = [
        str(task.path_rclone),
        "sync",
        str(task.local_dir),
        task.remote_dir,
        "--verbose",
        "--progress",
        "--log-file",
        str(task.path_log_file),
    ]

    if task.path_exclude_file:
        command.extend(["--exclude-from", str(task.path_exclude_file)])
    if task.backup_dir:
        command.extend(["--backup-dir", task.backup_dir])
    if task.extra_command:
        extra_commands = task.extra_command.strip().split(",")
        for cmd in extra_commands:
            try:
                option, value = cmd.split()
                command.extend([option, value])
            except ValueError:
                logger.warning(f"Ignorando comando mal formado: {cmd}")

    return command


def execute_task(task: Task):
    """Ejecuta la tarea de sincronización con rclone."""
    logger = logging.getLogger(__name__)
    logger.info("-" * 75)

    errors = validate_task(task)
    if errors:
        list(map(logger.error, errors))
        return

    try:
        logger.info(f"Procesando la tarea {task.task_path}...")
        command = build_rclone_command(task)
        logger.info(f"Ejecutando comando: {' '.join(command)}")

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar rclone: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sincroniza archivos con rclone.")
    parser.add_argument(
        "--tasks-dir", type=str, default="tasks", help="Directorio de tareas."
    )
    parser.add_argument(
        "--log-script", type=str, default="logs/script.log", help="Log del script."
    )
    args = parser.parse_args()

    logger = setup_logging(Path(args.log_script))

    logger.info("------ Inicio del script ------")

    tasks_dir = Path(args.tasks_dir)
    if not tasks_dir.exists():
        logger.error(f"El directorio de tareas {tasks_dir} no existe.")
        exit(1)

    for file in tasks_dir.glob("*.txt"):
        task = Task.from_filepath(file)
        execute_task(task)
