"""Tests for the config flow."""
from __future__ import annotations

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.notify_to_persistent.const import DOMAIN


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """The first attempt to add the integration creates the entry immediately."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == "Notify to Persistent"
    assert result["data"] == {}


async def test_user_flow_aborts_on_second_instance(hass: HomeAssistant) -> None:
    """A second attempt to add the integration aborts as already_configured."""
    existing = MockConfigEntry(domain=DOMAIN, data={}, unique_id=DOMAIN)
    existing.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "already_configured"
