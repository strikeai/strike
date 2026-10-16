"""Client for the hosted Strike API."""

from __future__ import annotations

import os
from typing import Any

import httpx

__version__ = "0.1.1"

_DEFAULT_URL = "https://strike-ai.eu"


class Client:
    """Call ``POST /v1/systemone`` on the hosted Strike API."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("STRIKE_API_KEY", "")
        self.base_url = (base_url or os.environ.get("STRIKE_API_URL", _DEFAULT_URL)).rstrip("/")
        self.timeout = timeout

    def decide(
        self,
        state: Any,
        questions: dict[str, Any],
        *,
        model: str = "strike-1",
        options: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"model": model, "state": state, "questions": questions}
        if options:
            body["options"] = options
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        response = httpx.post(
            f"{self.base_url}/v1/systemone",
            json=body,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
