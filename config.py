# Most of this taken from Redowan Delowar's post on configurations with Pydantic
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
import logging
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("uvicorn")


class BaseConfig(BaseSettings):
    ENV: Optional[str] = "local"
    APP_ENV: str
    APP_NAME: str
    PORT: int = 8080
    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = None
    SWAGGER_USER: str
    SWAGGER_PASS: str
    TITLE: str = "API_Template"
    MONGO_MODEL_DB: str
    MONGO_MODEL_COLLECTION: str = "core"
    MAX_LIMIT: int = 10
    MONGODB_URI: str
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin123"
    POSTGRES_DB: str = "core"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    OLLAMA_URL: str = "http://ollama:11434/api/generate"
    MODEL_NAME: str = "llama2-mini"
    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):

    MONGODB_URI: Optional[str] = None
    MONGO_MODEL_COLLECTION: Optional[str] = None
    MONGO_MODEL_DB: Optional[str] = None
    REDIS_URL: Optional[str] = None


class DevConfig(GlobalConfig):
    MONGODB_URI: str = "mongodb://mongo:27017"
    MONGO_MODEL_COLLECTION: str
    MONGO_MODEL_DB: str
    REDIS_URL: str = "redis://redis:6379/0"
    model_config = SettingsConfigDict()


class ProdConfig(GlobalConfig):

    model_config = SettingsConfigDict()


class TestConfig(GlobalConfig):

    model_config = SettingsConfigDict()


@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"local": DevConfig, "production": ProdConfig, "test": TestConfig}
    logger.info(f"Active mode {env_state}")
    return configs[env_state]()


config = get_config(BaseConfig().ENV)
