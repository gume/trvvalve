"""Adds config flow for TRV valve."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
f
from .const import CONF_CLIMATE
from .const import CONF_OPEN_TEMP
from .const import CONF_CLOSE_TEMP
from .const import DOMAIN
from .const import PLATFORMS


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
            valid = await self._test_config(
                user_input[CONF_CLIMATE], user_input[CONF_OPEN_TEMP], user_input[CONF_CLOSE_TEMP]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_CLIMATE], data=user_input
                )
            else:
                self._errors["base"] = "something_went_wrong"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return TrvValveOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="climate",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CLIMATE): cv.string
                }
            ),
            errors=self._errors,
        )

    async def _test_config(self, cliamte, open_temp, close_temp):
        """Return true if config is valid."""
        return True


class TrvValveOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for trv_valve."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="climate",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_OPEN_TEMP, default=40.0): vol.Schema(float),
                    vol.Optional(CONF_CLOSE_TEMP, default=5.0): vol.Schema(float)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_CLIMATE), data=self.options
        )
