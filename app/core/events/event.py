from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar
from uuid import UUID, uuid4

PayloadT = TypeVar("PayloadT")


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseEvent(Generic[PayloadT]):
    payload: PayloadT
    event_id: UUID = field(default_factory=uuid4, init=False)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)

    @property
    def event_name(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict[str, Any]:
        payload_data: Any = self.payload

        if is_dataclass(payload_data):
            payload_data = asdict(payload_data)
        elif isinstance(payload_data, dict):
            payload_data = dict(payload_data)

        return {
            "event_id": str(self.event_id),
            "event_name": self.event_name,
            "occurred_at": self.occurred_at.isoformat(),
            "payload": payload_data,
        }


__all__ = ["BaseEvent", "PayloadT"]
