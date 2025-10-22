from pathlib import Path
import json
from typing import Any

from backend.utils.config import get_settings


class CurriculumAdapter:
    """Loads curriculum material from local JSON assets."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._curriculum_dir = Path(self._settings.curriculum_path)

    def fetch_curriculum(self, level: str) -> list[dict[str, Any]] | None:
        file_path = self._curriculum_dir / f"{level}.json"
        if not file_path.exists():
            return None
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
