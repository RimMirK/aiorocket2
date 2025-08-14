from typing import Any, Mapping, Optional

__all__ = [
    "xRocketAPIError"
]

class xRocketAPIError(Exception):
    """
    High-level API error that always carries the raw API payload and (if available) HTTP status.

    Attributes:
        message: Human-readable error message.
        payload: Raw JSON payload returned by the API.
        status: HTTP status code (if known).
    """

    def __init__(self, payload: Mapping[str, Any], status: Optional[int] = None) -> None:
        self.payload = dict(payload)
        self.status = status
        self.message = payload.get("message")
        super().__init__(self.message)
    
    def __str__(self):
        return f"API says: {self.message or '~'}\nStatus: {self.status}\nPayload: {self.payload!r}"
