import requests

from backend.utils.config import Settings


class RemoteXAPIStore:
    """Simple HTTP client for forwarding statements to an external LRS."""

    def __init__(self, settings: Settings) -> None:
        self._endpoint = settings.lrs_endpoint
        self._auth = (settings.lrs_key, settings.lrs_secret)

    def send_statement(self, statement: dict) -> None:
        if not self._endpoint:
            return
        response = requests.post(
            self._endpoint,
            json=statement,
            auth=self._auth if all(self._auth) else None,
            timeout=10,
        )
        response.raise_for_status()
