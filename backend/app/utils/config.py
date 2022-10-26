import os
from typing import Optional
from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv
import secrets

load_dotenv(find_dotenv())


class settings(BaseSettings):
    PROJECT_NAME:str = 'ATTENDANCE SYSTEM'
    SECRET_KEY: str =  secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM:str = os.environ.get("ALGORITHM")
    FIRST_SUPER_ADMIN_EMAIL: str = os.environ.get("FIRST_SUPER_ADMIN_EMAIL")
    FIRST_SUPER_ADMIN_PASSWORD: str  = os.environ.get("FIRST_SUPER_ADMIN_PASSWORD")
    LOCATION: str = os.environ.get("LOCATION")
    ADDRESS: str = os.environ.get("ADDRESS")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL")

    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return settings()


settings = get_settings()