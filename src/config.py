from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Jwt_Token(BaseModel):
    secret_key: str
    expire_time: int = 15 # minute
    ALGORITHM: str = "HS256"


class DatabaseSettings(BaseModel):
    username: str
    password: str
    host: str
    port: int
    name: str
    echo: bool

    @property
    def url(self):
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    host: str
    port: int
    db: DatabaseSettings
    api: ApiPrefix = ApiPrefix()
    access_token: Jwt_Token

settings = AppSettings()
