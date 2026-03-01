from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up EZVIZ HP7 switches."""
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    serial = data["serial"]

    async_add_entities([EzvizHp7ChimeSwitch(api, serial)])


class EzvizHp7ChimeSwitch(SwitchEntity):
    """Switch entity to enable/disable monitor chime sound."""

    _attr_has_entity_name = True

    def __init__(self, api, serial: str):
        self._api = api
        self._serial = serial
        self._attr_translation_key = "chime_sound"
        self._attr_unique_id = f"{DOMAIN}_{serial}_chime_sound"
        self._attr_is_on = True

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._serial)},
            name=f"EZVIZ HP7 ({self._serial})",
            manufacturer="EZVIZ",
            model="HP7",
        )

    async def async_turn_on(self, **kwargs) -> None:
        """Enable monitor chime sound."""
        ok = await self.hass.async_add_executor_job(
            self._api.enable_chime, self._serial
        )
        if ok:
            self._attr_is_on = True
            self.async_write_ha_state()
        _LOGGER.log(
            logging.INFO if ok else logging.ERROR,
            "EZVIZ HP7: 'Enable Chime' %s.",
            "OK" if ok else "FAILED",
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Disable monitor chime sound."""
        ok = await self.hass.async_add_executor_job(
            self._api.disable_chime, self._serial
        )
        if ok:
            self._attr_is_on = False
            self.async_write_ha_state()
        _LOGGER.log(
            logging.INFO if ok else logging.ERROR,
            "EZVIZ HP7: 'Disable Chime' %s.",
            "OK" if ok else "FAILED",
        )
