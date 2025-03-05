import logging
import os
import subprocess

import uvicorn

from fastapi_server.config import Environment
from fastapi_server.utils.logging import AppLogger

logger = AppLogger().get_logger()


def alembic_upgrade():
    cmd = "alembic upgrade head"
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        # Log the output if needed
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Alembic upgrade failed!")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")
        raise


def run_server():
    config = uvicorn.Config(
        "master_server.server:app",
        host="0.0.0.0",
        port=1140,
        log_config="./config.ini",
        loop="uvloop",
    )

    if os.getenv("ENVIRONMENT") == Environment.DEVELOPMENT.value:
        config.log_level = logging.DEBUG
        config.reload = True

    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    try:
        alembic_upgrade()
    except subprocess.CalledProcessErrorpu:
        print("Server start aborted due to Alembic upgrade failure.")
        exit(1)

    run_server()
