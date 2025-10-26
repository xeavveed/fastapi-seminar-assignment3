from pydantic_settings import BaseSettings, SettingsConfigDict
from wapang.settings import SETTINGS


class DatabaseSettings(BaseSettings):
    dialect: str
    driver: str
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="DB_",
        env_file=SETTINGS.env_file,
        extra='ignore'
    )


DB_SETTINGS = DatabaseSettings()