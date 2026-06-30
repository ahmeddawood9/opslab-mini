import os
from datetime import UTC, datetime
from functools import lru_cache


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "opslab-mini")
        self.app_version = os.getenv("APP_VERSION", "0.1.0")
        self.app_env = os.getenv("APP_ENV", "dev")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./opslab.db")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def version_payload(self) -> dict[str, str]:
        return {
            "app_name": self.app_name,
            "version": self.app_version,
            "environment": self.app_env,
            "timestamp": datetime.now(UTC).isoformat(),
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
