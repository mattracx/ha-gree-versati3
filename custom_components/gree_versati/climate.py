from __future__ import annotations

import asyncio

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
)
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
    PARAM_ALL_OUT_WAT_TEM_HI,
    PARAM_ALL_OUT_WAT_TEM_LO,
    PARAM_CO_WAT_OUT_TEM_SET,
    PARAM_HE_WAT_OUT_TEM_SET,
    PARAM_MOD,
    PARAM_POW,
)
from .coordinator import GreeVersatiCoordinator
from .entity import GreeVersatiEntity

MODE_TO_HVAC: dict[int, HVACMode] = {
    1: HVACMode.HEAT,
    5: HVACMode.COOL,
}

HVAC_TO_MODE: dict[HVACMode, int] = {
    HVACMode.HEAT: 1,
    HVACMode.COOL: 5,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up climate entity."""
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
    """Climate entity for Gree Versati."""

    _attr_translation_key = "climate_control"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_icon = "mdi:heat-pump"

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
        self._changing_mode = False

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        data = self.coordinator.data or {}

        try:
            power = int(data.get(PARAM_POW, 0))
        except (TypeError, ValueError):
            power = 0

        if power == 0:
            return HVACMode.OFF

        try:
            mode = int(data.get(PARAM_MOD))
        except (TypeError, ValueError):
            return HVACMode.OFF

        return MODE_TO_HVAC.get(mode, HVACMode.OFF)

    @property
    def current_temperature(self) -> float | None:
        """Use leaving water temperature as current climate temperature."""
        data = self.coordinator.data or {}
        hi = data.get(PARAM_ALL_OUT_WAT_TEM_HI)
        lo = data.get(PARAM_ALL_OUT_WAT_TEM_LO)

        if hi in (None, "", "null") or lo in (None, "", "null"):
            return None

        try:
            return round((int(hi) - 100) + (int(lo) / 10), 1)
        except (TypeError, ValueError):
            return None

    @property
    def target_temperature(self) -> float | None:
        """Return active target temperature depending on current mode."""
        data = self.coordinator.data or {}
        mode = self.hvac_mode

        try:
            if mode == HVACMode.COOL:
                return float(data.get(PARAM_CO_WAT_OUT_TEM_SET))
            if mode == HVACMode.HEAT:
                return float(data.get(PARAM_HE_WAT_OUT_TEM_SET))
        except (TypeError, ValueError):
            return None

        return None

    @property
    def min_temp(self) -> float:
        """Return minimum target temperature depending on active mode."""
        if self.hvac_mode == HVACMode.COOL:
            return 5.0
        return 20.0

    @property
    def max_temp(self) -> float:
        """Return maximum target temperature depending on active mode."""
        if self.hvac_mode == HVACMode.COOL:
            return 25.0
        return 60.0

    @property
    def target_temperature_step(self) -> float:
        """Return target temperature step."""
        return 1.0

    async def async_set_temperature(self, **kwargs) -> None:
        """Set the correct setpoint depending on active mode."""
        temperature = kwargs.get("temperature")
        if temperature is None:
            return

        mode = self.hvac_mode

        if mode == HVACMode.COOL:
            await self._client.async_set(
                {PARAM_CO_WAT_OUT_TEM_SET: int(round(temperature))}
            )
        elif mode == HVACMode.HEAT:
            await self._client.async_set(
                {PARAM_HE_WAT_OUT_TEM_SET: int(round(temperature))}
            )
        else:
            return

        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode with fail-safe transition logic."""
        if self._changing_mode:
            return

        self._changing_mode = True
        try:
            current_mode = self.hvac_mode

            if hvac_mode == current_mode:
                return

            if hvac_mode == HVACMode.OFF:
                await self._client.async_set({PARAM_POW: 0})
                await asyncio.sleep(2)
                await self.coordinator.async_request_refresh()
                return

            if hvac_mode not in HVAC_TO_MODE:
                return

            target_mode = HVAC_TO_MODE[hvac_mode]

            if current_mode != HVACMode.OFF:
                await self._client.async_set({PARAM_POW: 0})
                await asyncio.sleep(3)
                await self.coordinator.async_request_refresh()

            await self._client.async_set({PARAM_MOD: target_mode})
            await asyncio.sleep(2)

            await self._client.async_set({PARAM_POW: 1})
            await asyncio.sleep(2)

            await self.coordinator.async_request_refresh()
        finally:
            self._changing_mode = False
