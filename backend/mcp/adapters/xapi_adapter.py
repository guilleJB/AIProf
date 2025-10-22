from backend.lrs.remote_store import RemoteXAPIStore
from backend.utils.config import get_settings


class XAPIAdapter:
    """Adapter that forwards statements to a remote LRS via xAPI."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._remote_store = RemoteXAPIStore(self._settings)

    def forward_statement(self, statement: dict) -> None:
        self._remote_store.send_statement(statement)
