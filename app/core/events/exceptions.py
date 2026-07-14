from __future__ import annotations


class EventBusError(Exception):
    """Base exception for the Event Bus."""


class EventRegistrationError(EventBusError):
    """Raised when an event registration operation fails."""


class EventAlreadyRegisteredError(EventRegistrationError):
    """Raised when a listener is already registered for an event."""


class EventNotRegisteredError(EventRegistrationError):
    """Raised when attempting to unregister an unknown listener."""


class EventDispatchError(EventBusError):
    """Raised when the dispatcher cannot dispatch an event."""


__all__ = [
    "EventBusError",
    "EventRegistrationError",
    "EventAlreadyRegisteredError",
    "EventNotRegisteredError",
    "EventDispatchError",
]
