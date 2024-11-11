from os import environ, getenv
from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv

load_dotenv(".env")


class Settings(BaseModel):
    SYSTEM_API_TOKEN: SecretStr
    BOT_TOKEN: SecretStr
    MONGODB_URL: SecretStr
    MONGODB_DB: SecretStr
    LOGGING_URL: str
    LOGGING_LEVEL: str
    LOGGING_TOKEN: str

    API_PORT: int
    API_HOST: str

    ADMIN_USERNAME: SecretStr
    ADMIN_PASSWORD: SecretStr


SETTINGS = Settings(**environ)
