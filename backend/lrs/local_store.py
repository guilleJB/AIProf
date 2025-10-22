import json
from pathlib import Path
from typing import Any

from backend.utils.config import Settings


class LocalXAPIStore:
    """Persist statements locally for development purposes."""

    def __init__(self, settings: Settings) -> None:
        self._log_path = Path(settings.local_xapi_log)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

    def save_statement(self, statement: dict[str, Any]) -> None:
        log_entry = json.dumps(statement, ensure_ascii=False)
        with self._log_path.open("a", encoding="utf-8") as handle:
            handle.write(log_entry + "\n")
