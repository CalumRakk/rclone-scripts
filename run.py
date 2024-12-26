import subprocess
from pathlib import Path
import logging
from typing import Union
import argparse

parser = argparse.ArgumentParser(description="Sincroniza archivos con rclone.")
parser.add_argument(
    "--tasks-dir", type=str, default="tasks", help="Directorio de tareas."
)
args = parser.parse_args()

tasks_dir = Path(args.tasks_dir)

if not tasks_dir.exists():
    raise FileNotFoundError(f"El directorio de tareas {tasks_dir} no existe.")

path_script_log = Path("logs/script.log")
path_script_log.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=path_script_log,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s - %(message)s",
    datefmt="%d-%m-%Y %I:%M:%S %p",
    level=logging.DEBUG,
    encoding="utf-8",
)
logger = logging.getLogger(__name__)
logger.info("Inicio del script")


def check_file(path: Union[Path, str]) -> Path:
    """Verifica si el archivo existe."""
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"El archivo {path} no existe.")
    return path


class Task:
    def __init__(
        self,
        path: Path,
        local_dir: Union[Path, str],
        remote_dir: str,
        backup_dir: str,
        path_rclone: Union[Path, str],
        path_log_file: Union[Path, str] = None,
        path_exclude_file: Path = None,
    ):
        self.path = check_file(path)
        self.local_dir = check_file(local_dir)
        self.remote_dir = remote_dir
        self.backup_dir = backup_dir
        self.path_rclone = check_file(path_rclone)
        self.path_exclude_file = path_exclude_file
        self.path_log_file = path_log_file

        logger.info(f"Configuración de la tarea: {self.__dict__}")

    @classmethod
    def from_filepath(cls, config_path: Path):
        logger.info(f"Leyendo archivo de configuración: {config_path}")

        if isinstance(config_path, str):
            config_path = Path(config_path)

        file = config_path.read_text()
        config = {}
        for line in file.splitlines():
            if not "=" in line or line == "" or line.startswith("#") or line == "\n":
                continue
            key, value = line.strip().split("=", 1)
            config[key.lower().strip()] = value.strip()
            logger.info(f"Se ha asignado: {key.strip()}={value.strip()}")

        return cls(path=config_path, **config)

    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if name == "path_log_file" and value is None:
            value = Path.cwd() / "logs" / f"log_{self.path.stem}.txt"
            value.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Se ha asignado un archivo de log por defecto: {value}")
        elif name == "path_exclude_file" and value is not None:
            value = Path(value)
            if not value.exists():
                logger.warning(f"El archivo de exclusión {value} no existe.")
                raise FileNotFoundError(f"El archivo {value} no existe.")
        return value


for file in Path(tasks_dir).glob("*.txt"):
    config = Task.from_filepath(file)
    try:
        command = [
            f"{config.path_rclone}",
            "sync",
            f"{config.local_dir}",
            config.remote_dir,
            "--verbose",
            "--progress",
            "--backup-dir",
            config.backup_dir,
            "--log-file",
            f"{config.path_log_file}",
        ]
        if config.path_exclude_file is not None:
            logger.info(f"Usando el archivo de exclusión: {config.path_exclude_file}")
            command.append(f"--exclude-from")
            command.append(str(config.path_exclude_file))

        subprocess.run(
            command,
            shell=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar rclone: {e}")

logger.info("Fin del script")
