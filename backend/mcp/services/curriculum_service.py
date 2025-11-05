from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Optional

from backend.mcp.schemas import CurriculumModule
from backend.utils.config import Settings, get_settings


class CurriculumNotFoundError(LookupError):
    """Raised when a curriculum level or module cannot be located."""


class CurriculumService:
    """Loads curriculum modules from JSON assets and allows filtering."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self._settings = settings or get_settings()
        self._curriculum_dir = Path(self._settings.curriculum_path)

    def list_modules(self, level: str, subject: str | None = None) -> list[CurriculumModule]:
        modules = _load_level_modules(self._curriculum_dir, level)
        filtered = (
            module for module in modules if subject is None or module.subject == subject
        )
        modules_list = list(filtered)
        if not modules_list:
            raise CurriculumNotFoundError(
                f"No curriculum modules found for level='{level}' subject='{subject}'"
            )
        return modules_list

    def get_module(self, level: str, module_id: str) -> CurriculumModule:
        modules = _load_level_modules(self._curriculum_dir, level)
        for module in modules:
            if module.id == module_id:
                return module
        raise CurriculumNotFoundError(
            f"Module '{module_id}' not found for level '{level}'"
        )


@lru_cache(maxsize=32)
def _load_level_modules(curriculum_dir: Path, level: str) -> tuple[CurriculumModule, ...]:
    file_path = curriculum_dir / f"{level}.json"
    if not file_path.exists():
        raise CurriculumNotFoundError(f"Curriculum file not found for level '{level}'")
    with file_path.open("r", encoding="utf-8") as handle:
        data: Iterable[dict[str, Any]] = json.load(handle)
    return tuple(CurriculumModule.parse_obj(item) for item in data)
