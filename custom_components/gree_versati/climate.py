from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import GreeVersatiProtocolClient
from .constants import (
    CONF_DEVICE_ID,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DATA_ENTRIES,
    PARAM_CO_WAT_OUT_TEM_SET,
    PARAM_HE_WAT_OUT_TEM_SET,
    PARAM_MOD,
    PARAM_POW,
)
from .coordinator import GreeVersatiCoordinator
from .entity import GreeVersatiEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    runtime_data = hass.data[entry.domain][DATA_ENTRIES][entry.entry_id]

    async_add_entities(
        [
            GreeVersatiClimate(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            )
        ]
    )


class GreeVersatiClimate(GreeVersatiEntity, ClimateEntity):
    _attr_translation_key = "climate_control"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        client: GreeVersatiProtocolClient,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            PARAM_MOD,
            unique_id_key="climate",
        )
        self._client = client

    @property
    def hvac_mode(self) -> HVACMode:
        power = (self.coordinator.data or {}).get(PARAM_POW)
        mod = (self.coordinator.data or {}).get(PARAM_MOD)

        try:
            if int(power) == 0:
                return HVACMode.OFF
        except (TypeError, ValueError):
            return HVACMode.OFF

        try:
            mod = int(mod)
        except (TypeError, ValueError):
            return HVACMode.OFF

        if mod == 5:
            return HVACMode.COOL
        if mod == 1:
            return HVACMode.HEAT

        return HVACMode.OFF

    @property
    def target_temperature(self) -> float | None:
        data = self.coordinator.data or {}
        if self.hvac_mode == HVACMode.COOL:
            value = data.get(PARAM_CO_WAT_OUT_TEM_SET)
        else:
            value = data.get(PARAM_HE_WAT_OUT_TEM_SET)

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @property
    def current_temperature(self) -> float | None:
        data = self.coordinator.data or {}
        hi = data.get("AllOutWatTemHi")
        lo = data.get("AllOutWatTemLo")

        try:
            return (int(hi) - 100) + (int(lo) / 10)
        except (TypeError, ValueError):
            return None

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            await self._client.async_set({PARAM_POW: 0})
        elif hvac_mode == HVACMode.HEAT:
            await self._client.async_set({PARAM_POW: 1, PARAM_MOD: 1})
        elif hvac_mode == HVACMode.COOL:
            await self._client.async_set({PARAM_POW: 1, PARAM_MOD: 5})

        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs) -> None:
        temperature = kwargs.get("temperature")
        if temperature is None:
            return

        if self.hvac_mode == HVACMode.COOL:
            await self._client.async_set({PARAM_CO_WAT_OUT_TEM_SET: int(round(temperature))})
        else:
            await self._client.async_set({PARAM_HE_WAT_OUT_TEM_SET: int(round(temperature))})

        await self.coordinator.async_request_refresh()
