"""Valve platform for TRV valve."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.valve import ValveEntity, ValveEntityFeature


from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME
from .const import VERSION

from . import HubConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    hub = config_entry.runtime_data
    async_add_entities([TRVValve(hub)])


# Configuration and options
CONF_CLIMATE = "climate"
CONF_OPEN_TEMP = "open_temperature"
CONF_CLOSE_TEMP = "close_temperature"


class TRVValveEntity(Entity):

    should_poll = False

    def __init__(self, hub):
        self._hub = hub

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self._hub.hub_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }
    
    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._hub.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._hub.remove_callback(self.async_write_ha_state)


class TRVValve(TRVValveEntity, ValveEntity):

    should_poll = False
    supported_features = ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE
    reports_position = False

    async def async_open_valve(self) -> None:
        await self._hub._hass.services.async_call("climate", "turn_on", {"entity_id": self._hub._climate})
        #await self._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hub._hass.services.async_call("climate", "set_temperature", {"entity_id": self._hub._climate, "temperature": self._hub._open_temp})
        self.__attr_is_closed = False
        self._attr_icon = "mdi:valve-open"
        self._attr_icon_color = "on"
        self.schedule_update_ha_state()

    async def async_close_valve(self) -> None:
        await self._hub._hass.services.async_call("climate", "turn_on", {"entity_id": self._hub._climate})
        #await self._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hub._hass.services.async_call("climate", "set_temperature", {"entity_id": self._hub._climate, "temperature": self._hub._close_temp})
        self.__attr_is_closed = True
        self._attr_icon = "mdi:valve-closed"
        self._attr_icon_color = "red"
        self.schedule_update_ha_state()

    def __init__(self, hub) -> None:
        self._hub = hub
        super().__init__(hub)

        self._attr_name = hub._name
        self._attr_unique_id = f"trvvalve_{hub._climate}"
        self._attr_icon = "mdi:valve"
