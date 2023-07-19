from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int

    class Config:
        env_file = ".env"
