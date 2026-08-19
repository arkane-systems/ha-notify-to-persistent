"""Notify entity for the Notify to Persistent integration.

Forwards every message it receives to Home Assistant's built-in
persistent_notification.create action, so it shows up in the notification
bell. No notification_id is ever passed, so each call creates a new,
distinct persistent notification rather than overwriting a previous one.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.notify import NotifyEntity, NotifyEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Notify to Persistent entity from a config entry."""
    async_add_entities([PersistentNotifyEntity(entry)])


class PersistentNotifyEntity(NotifyEntity):
    """Notify entity that creates a persistent notification for each message."""

    _attr_supported_features = NotifyEntityFeature.TITLE
    _attr_name = "Persistent Notification"
    _attr_icon = "mdi:bell-ring"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._attr_unique_id = entry.entry_id

    async def async_send_message(self, message: str, title: str | None = None) -> None:
        """Create a persistent notification from the given message and title."""
        data: dict[str, Any] = {"message": message}
        if title is not None:
            data["title"] = title

        await self.hass.services.async_call(
            "persistent_notification", "create", data, blocking=True
        )
