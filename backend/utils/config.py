from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    environment: str = Field("development", env="AIPROF_ENV")
    local_xapi_log: str = Field("data/xapi_log.jsonl", env="AIPROF_LOCAL_XAPI_LOG")

    curriculum_path: str = Field("data/curriculum", env="AIPROF_CURRICULUM_PATH")
    exercises_path: str = Field("data/exercises", env="AIPROF_EXERCISES_PATH")

    lrs_endpoint: Optional[str] = Field(None, env="AIPROF_LRS_ENDPOINT")
    lrs_key: Optional[str] = Field(None, env="AIPROF_LRS_KEY")
    lrs_secret: Optional[str] = Field(None, env="AIPROF_LRS_SECRET")

    llm_model: str = Field("gpt-4o-mini", env="AIPROF_LLM_MODEL")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def resolve_paths(self) -> None:
        Path(self.curriculum_path).mkdir(parents=True, exist_ok=True)
        Path(self.exercises_path).mkdir(parents=True, exist_ok=True)
        Path(self.local_xapi_log).parent.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.resolve_paths()
    return settings
