from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Descripción del paquete"

setup(
    name="rclone_tasks",
    version="0.2.0",
    author="Leo",
    author_email="leocasti2@gmail.com",
    description="Script para gestionar tareas de sincronización con Rclone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/rclone_tasks",
    packages=find_packages(),
    py_modules=["rclone_tasks"],
    python_requires=">=3.7",
    entry_points={
        # rclone-tasks será el comando, rclone_tasks es el módulo, main la función a ejecutar
        "console_scripts": [
            "rclone-tasks = rclone_tasks.cli:main",
        ],
    },
    include_package_data=True,
)
