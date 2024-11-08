"""Valve platform for TRV valve."""
from homeassistant.components.valve import ValveEntity, ValveEntityFeature

from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import VALVE
from .entity import TrvValveEntity

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([TrvValve(coordinator, entry)])


# Configuration and options
CONF_CLIMATE = "climate"
CONF_OPEN_TEMP = "open_temperature"
CONF_CLOSE_TEMP = "close_temperature"

class TRVValve(TrvValveEntity, ValveEntity):

    _attr_supported_features = ValveEntityFeature(
        ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE
    )
    _attr_reports_position = False


    async def async_open_valve(self) -> None:
        await self._hass.services.async_call("climate", "turn_on", {"entity_id": self._climate})
        #await self._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hass.services.async_call("climate", "set_temperature", {"entity_id": self._climate, "temperature": self._open_temp})
        self.__attr_is_closed = False
        self._attr_icon = "mdi:valve-open"
        self._attr_icon_color = "on"
        self.schedule_update_ha_state()

    async def async_close_valve(self) -> None:
        await self._hass.services.async_call("climate", "turn_on", {"entity_id": self._climate})
        #await self._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hass.services.async_call("climate", "set_temperature", {"entity_id": self._climate, "temperature": self._close_temp})
        self.__attr_is_closed = True
        self._attr_icon = "mdi:valve-closed"
        self._attr_icon_color = "red"
        self.schedule_update_ha_state()

    def __init__(self, hass, name, climate, open_temp, close_temp):
        self._attr_unique_id = "trvvalve_" + name
        self._attr_icon = "mdi:valve"
        self._name = name
        self._climate = climate
        self._open_temp = open_temp
        self._close_temp = close_temp
        self._hass = hass
