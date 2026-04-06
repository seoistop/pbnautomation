import logging
from typing import Any

import requests

from .security import decrypt_secret

logger = logging.getLogger(__name__)


class WordPressClient:
    def __init__(self, domain: str, username: str, encrypted_password: str, post_id: int):
        self.domain = domain.rstrip("/")
        self.username = username
        self.password = decrypt_secret(encrypted_password)
        self.post_id = post_id
        self.base_url = f"https://{self.domain}"
        self.auth = (self.username, self.password)

    def _ux_block_endpoint(self) -> str:
        return f"{self.base_url}/wp-json/wp/v2/ux_block/{self.post_id}"

    def fetch_content(self) -> dict[str, Any]:
        response = requests.get(self._ux_block_endpoint(), auth=self.auth, timeout=30)
        response.raise_for_status()
        return response.json()

    def update_content(self, content: str) -> dict[str, Any]:
        payload = {"content": content}
        response = requests.post(self._ux_block_endpoint(), json=payload, auth=self.auth, timeout=30)
        response.raise_for_status()
        return response.json()

    def append_anchor(self, url: str, anchor_text: str, before: str | None = None, after: str | None = None) -> dict[str, Any]:
        data = self.fetch_content()
        rendered = data.get("content", {}).get("rendered", "")
        snippet = f"{before or ''}<a href=\"{url}\" rel=\"nofollow sponsored\">{anchor_text}</a>{after or ''}"
        updated = rendered + "\n" + snippet
        logger.info("Updating %s UX block %s", self.domain, self.post_id)
        return self.update_content(updated)
