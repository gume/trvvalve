"""Adds config flow for TRV valve."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.data_entry_flow import section
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig, EntityFilterSelectorConfig


import logging

from .const import CONF_NAME
from .const import CONF_CLIMATE
from .const import CONF_OPEN_TEMP
from .const import CONF_CLOSE_TEMP

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class TrvValveFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for trv_valve."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_config(user_input[CONF_CLIMATE])
            if valid:
                self.data = user_input.copy()
                return await self.async_step_options()
            else:
                self._errors["base"] = "wrong"

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_CLIMATE): EntitySelector(
                    EntitySelectorConfig(
                        multiple = False,
                        filter = EntityFilterSelectorConfig(domain="climate")
                    )
                )
            }), errors=self._errors
        )

    async def _test_config(self, cliamte):
        """Return true if config is valid."""
        return True

    async def async_step_options(self, user_input=None):
        errors = {}

        if user_input is not None:
            self.data.update(user_input)
            return self.async_create_entry(title=self.data[CONF_NAME], data=self.data)

        return self.async_show_form(
            step_id="options",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_OPEN_TEMP, default=35.0): vol.Coerce(float),
                    vol.Optional(CONF_CLOSE_TEMP, default=10.0): vol.Coerce(float)
                }
            ),
            errors=errors
        )