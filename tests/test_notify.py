"""Tests for the notify.py platform."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_mock_service,
)

from custom_components.notify_to_persistent.const import DOMAIN


async def _setup_entry(hass: HomeAssistant) -> str:
    """Set up the integration and return its notify entity_id."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, unique_id=DOMAIN)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    notify_states = [
        state for state in hass.states.async_all() if state.entity_id.startswith("notify.")
    ]
    assert len(notify_states) == 1
    return notify_states[0].entity_id


async def test_send_message_creates_persistent_notification_with_title(
    hass: HomeAssistant,
) -> None:
    """Sending a message with a title calls persistent_notification.create with both."""
    entity_id = await _setup_entry(hass)
    calls = async_mock_service(hass, "persistent_notification", "create")

    await hass.services.async_call(
        "notify",
        "send_message",
        {"entity_id": entity_id, "message": "The garage door is open.", "title": "Garage Alert"},
        blocking=True,
    )

    assert len(calls) == 1
    assert calls[0].data == {
        "message": "The garage door is open.",
        "title": "Garage Alert",
    }


async def test_send_message_without_title_omits_title_key(hass: HomeAssistant) -> None:
    """Sending a message with no title omits the title key entirely."""
    entity_id = await _setup_entry(hass)
    calls = async_mock_service(hass, "persistent_notification", "create")

    await hass.services.async_call(
        "notify",
        "send_message",
        {"entity_id": entity_id, "message": "Hello"},
        blocking=True,
    )

    assert len(calls) == 1
    assert calls[0].data == {"message": "Hello"}


async def test_repeated_send_message_creates_separate_notifications(
    hass: HomeAssistant,
) -> None:
    """Each call to send_message results in its own create call (no shared id)."""
    entity_id = await _setup_entry(hass)
    calls = async_mock_service(hass, "persistent_notification", "create")

    await hass.services.async_call(
        "notify", "send_message", {"entity_id": entity_id, "message": "First"}, blocking=True
    )
    await hass.services.async_call(
        "notify", "send_message", {"entity_id": entity_id, "message": "Second"}, blocking=True
    )

    assert len(calls) == 2
    assert "notification_id" not in calls[0].data
    assert "notification_id" not in calls[1].data
