from pathlib import Path
import logging
from typing import Union

logger = logging.getLogger(__name__)


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
        task_path: Path,
        local_dir: Union[Path, str],
        remote_dir: str,
        path_rclone: Union[Path, str],
        backup_dir: str = None,
        path_log_file: Union[Path, str] = None,
        path_exclude_file: Path = None,
        extra_command: str = None,
    ):
        self.task_path = Path(task_path)
        self.local_dir = Path(local_dir)
        self.remote_dir = remote_dir
        self.backup_dir = backup_dir
        self.path_rclone = Path(path_rclone)
        self.path_exclude_file = Path(path_exclude_file) if path_exclude_file else None
        self.path_log_file = Path(path_log_file) if path_log_file else None
        self.extra_command = extra_command

    @classmethod
    def from_filepath(cls, config_path: Path):
        logger.info(f"Leyendo archivo de configuración: {config_path}")

        if isinstance(config_path, str):
            config_path = Path(config_path)
        elif config_path is None:
            logger.error("El path debe ser proporcionado.")
            raise ValueError("El path debe ser proporcionado.")

        if not config_path.exists():
            logger.error(f"El archivo de configuración {config_path} no existe.")
            raise FileNotFoundError(
                f"El archivo de configuración {config_path} no existe."
            )

        file = config_path.read_text()
        config = cls._parsed_content(file)[0]
        instance = cls(task_path=config_path, **config)
        logger.info(f"Instanciando tarea a partir de config_path. {instance}")
        return instance

    @classmethod
    def _parsed_content(cls, content: str) -> list[dict]:
        logger.info("Parseando contenido.")

        if not isinstance(content, str):
            raise TypeError("El contenido debe ser una cadena de texto.")

        configs = []
        config = {}
        for line in content.splitlines():
            if line == "" or line.startswith("#") or line == "\n":
                continue
            elif line.startswith("---"):
                logger.debug("Se ha encontrado un bloque de configuración.")
                configs.append(config)
                config = dict()
                continue

            key, value = line.strip().split("=", 1)
            config[key.lower().strip()] = value.strip("\"' ")
            logger.debug(f"Se ha asignado: {key.strip()}={value.strip()}")
        configs.append(config)

        return configs

    @classmethod
    def from_dict(cls, config: dict):
        if not isinstance(config, dict):
            raise TypeError("El config debe ser un diccionario.")
        instance = cls(**config)
        logger.info(f"Instanciando tarea a partir de diccionario. {instance}")
        return instance

    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if name == "path_log_file" and value is None:
            value = Path.cwd() / "logs" / f"log_{self.task_path.stem}.txt"
            value.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Se ha asignado un archivo de log por defecto: {value}")
        return value
