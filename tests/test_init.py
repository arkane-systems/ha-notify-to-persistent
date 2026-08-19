"""Tests for integration setup/unload."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.notify_to_persistent.const import DOMAIN


async def _setup_entry(hass: HomeAssistant) -> MockConfigEntry:
    entry = MockConfigEntry(domain=DOMAIN, data={}, unique_id=DOMAIN)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_setup_entry_creates_single_notify_entity(hass: HomeAssistant) -> None:
    """Setting up the entry creates exactly one notify entity and loads."""
    entry = await _setup_entry(hass)

    assert entry.state is ConfigEntryState.LOADED

    notify_states = [
        state for state in hass.states.async_all() if state.entity_id.startswith("notify.")
    ]
    assert len(notify_states) == 1


async def test_unload_entry(hass: HomeAssistant) -> None:
    """Unloading the entry marks the notify entity unavailable and unloads cleanly."""
    entry = await _setup_entry(hass)
    notify_states = [
        state for state in hass.states.async_all() if state.entity_id.startswith("notify.")
    ]
    entity_id = notify_states[0].entity_id

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
    assert hass.states.get(entity_id).state == STATE_UNAVAILABLE
