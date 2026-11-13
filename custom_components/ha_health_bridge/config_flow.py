"""Enable the authenticated local export endpoint."""

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class HAHealthBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """One endpoint per Home Assistant; iPhones have separate source identities."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Show setup information; no additional credentials are stored here."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title="HA Health Bridge", data={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
