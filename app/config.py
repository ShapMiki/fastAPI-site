from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Optional

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: Optional[str] = None
    image_scr: str
    hour_zone: int
    secret_key_for_jwt: str
    algorithm_for_jwt: str
    domain: str
    web_path: str

    @model_validator(mode="before")
    @classmethod
    def set_database_url(cls, values):
        values['DATABASE_URL'] = f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASSWORD']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        return values

    class Config:
        env_file = ".env"

settings = Settings()