"""Valve platform for TRV valve."""
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.components.valve import ValveEntity, ValveEntityFeature


from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME
from .const import VERSION
from .const import MANUFACTURER

from . import HubConfigEntry

import logging
_LOGGER = logging.getLogger(__name__)


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


class TRVValve(ValveEntity):

    should_poll = False
    supported_features = ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE
    reports_position = False

    async def async_open_valve(self) -> None:
        climate_state = self._hub._hass.states.get(self._hub._climate)
        if climate_state is not None and "manual" in climate_state.attributes.get("preset_modes", []):
            await self._hub._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._hub._climate, "preset_mode": "manual"})
        await self._hub._hass.services.async_call("climate", "set_temperature", {"entity_id": self._hub._climate, "temperature": self._hub._open_temp})
        await self._hub._hass.services.async_call("climate", "turn_on", {"entity_id": self._hub._climate})
        self.__attr_is_closed = False
        self._attr_icon = "mdi:valve-open"
        self.schedule_update_ha_state()

    async def async_close_valve(self) -> None:
        climate_state = self._hub._hass.states.get(self._hub._climate)
        if climate_state is not None and "manual" in climate_state.attributes.get("preset_modes", []):
            await self._hub._hass.services.async_call("climate", "set_preset_mode", {"entity_id": self._climate, "preset_mode": "manual"})
        await self._hub._hass.services.async_call("climate", "set_temperature", {"entity_id": self._hub._climate, "temperature": self._hub._close_temp})
        await self._hub._hass.services.async_call("climate", "turn_off", {"entity_id": self._hub._climate})
        self.__attr_is_closed = True
        self._attr_icon = "mdi:valve-closed"
        self.schedule_update_ha_state()

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
            "manufacturer": MANUFACTURER,
        }
    
    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._hub.register_callback(self.async_write_ha_state)

        self._unsub_atsce = async_track_state_change_event(
            self._hub._hass, self._hub._climate, self._async_climate_attribute_changed
        )
        
        # Set initial state according to the climate entity
        climate_state = self._hub._hass.states.get(self._hub._climate)
        if climate_state:
            self._attr_is_closed = climate_state.state == "off"
        else:
            self._attr_is_closed = None

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._hub.remove_callback(self.async_write_ha_state)

        self._unsub_atsce()

    @callback
    async def _async_climate_attribute_changed(self, event) -> None:
        """Handle climate state and attribute changes."""
        if event.data.get("entity_id") != self._hub._climate:
            return

        new_state = event.data.get("new_state")
        if new_state is None:
            return
        hvac_action = new_state.attributes.get("hvac_action")

        off = hvac_action == "off"
        idle = hvac_action == "idle"
        self._attr_is_closed = off or idle
        self.schedule_update_ha_state()

    def __init__(self, hub) -> None:
        self._hub = hub
        super().__init__()

        self._attr_name = hub._name
        self._attr_unique_id = f"trvvalve_{hub._climate}"
        self._attr_icon = "mdi:valve"

