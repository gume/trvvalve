"""
Custom integration to integrate TRV valve with Home Assistant.

For more details about this integration, please refer to
https://github.com/gume/trvvalve
"""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .const import PLATFORMS
from .const import STARTUP_MESSAGE

from .const import CONF_NAME
from .const import CONF_CLIMATE
from .const import CONF_OPEN_TEMP
from .const import CONF_CLOSE_TEMP

from . import hub

_LOGGER: logging.Logger = logging.getLogger(__package__)

type HubConfigEntry = ConfigEntry[hub.Hub]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    _LOGGER.error(entry.data)
    entry.runtime_data = hub.Hub(hass,
        entry.data[CONF_NAME],
        entry.data[CONF_CLIMATE],
        entry.data[CONF_OPEN_TEMP],
        entry.data[CONF_CLOSE_TEMP]
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    #entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
