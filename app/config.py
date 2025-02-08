from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    database_hostname: str = Field(...)
    database_port: int = Field(...)
    database_username: str = Field(...)
    database_password: str = Field(...)
    database_name: str = Field(...)
    secret_key: str = Field(...)
    algorithm: str = Field(...)
    access_token_expire_minutes: int = Field(...)

    

    class Config():
        env_file = ".env"
    

settings = Settings() # type: ignore



