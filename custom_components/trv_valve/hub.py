"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import asyncio
import random

from homeassistant.core import HomeAssistant


class Hub:

    manufacturer = "Gume"

    def __init__(self, hass: HomeAssistant, name: str, climate: str, ot: float, ct: float) -> None:
        """Init dummy hub."""
        self._hass = hass
        self._name = name
        self._climate = climate
        self._id = name.lower()
        self._open_temp = ot
        self._close_temp = ct
        self._callbacks = set()

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)
