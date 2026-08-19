"""Config flow for the Notify to Persistent integration.

There is nothing to configure: this integration exposes exactly one notify
entity, always. Adding it creates the single config entry immediately, with
no form to fill in. Home Assistant's unique-id mechanism is used to prevent
a second instance from being added.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN


class NotifyToPersistentConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Notify to Persistent."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the (only) step shown when the user clicks 'Add integration'."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title="Notify to Persistent", data={})
