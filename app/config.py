import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = "./.env"
load_dotenv(dotenv_path)


class Config:
    """Конфигурация приложения."""

    # app
    APP_NAME = os.environ.get("APP_NAME", "fastapi_osm")
    DEBUG = os.environ.get("DEBUG", False) in {"True", "true", "1", True}
    RELOAD = os.environ.get("RELOAD", False) in {"True", "true", "1", True}
    APP_HOST = os.environ.get("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.environ.get("APP_PORT", "8000"))
    BASE_DIR = Path(__file__).resolve().parent

    # database
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    DB_DATABASE = os.environ["DB_DATABASE"]
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"  # noqa E501

    # api dadata
    API_KEY = os.environ["API_KEY"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    DADATA_URL = os.environ["DADATA_URL"]
