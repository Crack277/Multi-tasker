from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseModel):
    host: str
    port: int
    db: int
    password: str | None = None

    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/user"
    auth: str = "/auth"
    projects: str = "/project"
    tasks: str = "/task"
    profile: str = "/profile"
    categories: str = "/category"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class AccessToken(BaseModel):
    secret_key: str
    expire_minutes: int = 15
    ALGORITHM: str = "HS256"


class DatabaseSettings(BaseModel):
    username: str
    password: str
    host: str
    port: int
    name: str
    echo: bool

    @property
    def url(self) -> str:
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
    access_token: AccessToken
    redis: RedisSettings


settings = AppSettings()
