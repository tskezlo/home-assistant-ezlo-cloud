"""Config flow for Ezlo HA Cloud."""

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import callback

from .const import DOMAIN
from .options_flow import EzloOptionsFlowHandler  # Import options flow

_LOGGER = logging.getLogger(__name__)


class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Ezlo HA Cloud."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step of the config flow."""
        # """Initial setup form."""
        errors = {}

        if user_input is not None:
            try:
                await self.async_set_unique_id("user_authentication")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Ezlo HA Cloud", data=user_input)
            except config_entries.ConfigEntryError:
                errors["base"] = "already_configured"
            except Exception as e:  # noqa: BLE001
                errors["base"] = str(e)

        data_schema = vol.Schema(
            {
                vol.Required("username"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> EzloOptionsFlowHandler:
        """Enable the 'Configure' and 'Login' buttons in the UI."""
        return EzloOptionsFlowHandler(config_entry)
