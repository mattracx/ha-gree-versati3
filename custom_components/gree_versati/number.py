from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import GreeVersatiProtocolClient
from .constants import (
    CONF_DEVICE_ID,
    CO_WAT_OUT_TEMP_SET_STEP,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DATA_ENTRIES,
    HE_WAT_OUT_TEMP_SET_STEP,
    MAX_CO_WAT_OUT_TEMP_SET,
    MAX_HE_WAT_OUT_TEMP_SET,
    MAX_WAT_BOX_TEMP_SET,
    MIN_CO_WAT_OUT_TEMP_SET,
    MIN_HE_WAT_OUT_TEMP_SET,
    MIN_WAT_BOX_TEMP_SET,
    PARAM_CO_WAT_OUT_TEM_SET,
    PARAM_HE_WAT_OUT_TEM_SET,
    PARAM_WAT_BOX_TEM_SET,
    WAT_BOX_TEMP_SET_STEP,
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
            GreeVersatiHeatingOutletSetpointNumber(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
            GreeVersatiCoolingOutletSetpointNumber(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
            GreeVersatiWatBoxSetpointNumber(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
        ]
    )


class GreeVersatiSetpointNumber(GreeVersatiEntity, NumberEntity):
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = "box"

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        client: GreeVersatiProtocolClient,
        param_key: str,
        unique_id_key: str,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            param_key,
            unique_id_key=unique_id_key,
        )
        self._client = client
        self._param_key = param_key

    @property
    def native_value(self) -> float | None:
        value = (self.coordinator.data or {}).get(self._param_key)
        if value in (None, "", "null"):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        await self._client.async_set({self._param_key: int(round(value))})
        await self.coordinator.async_request_refresh()


class GreeVersatiHeatingOutletSetpointNumber(GreeVersatiSetpointNumber):
    _attr_translation_key = "he_wat_out_tem_set"
    _attr_icon = "mdi:radiator"
    _attr_native_min_value = MIN_HE_WAT_OUT_TEMP_SET
    _attr_native_max_value = MAX_HE_WAT_OUT_TEMP_SET
    _attr_native_step = HE_WAT_OUT_TEMP_SET_STEP

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        client: GreeVersatiProtocolClient,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            client,
            PARAM_HE_WAT_OUT_TEM_SET,
            unique_id_key="heating_water_outlet_setpoint",
        )


class GreeVersatiCoolingOutletSetpointNumber(GreeVersatiSetpointNumber):
    _attr_translation_key = "co_wat_out_temp_set"
    _attr_icon = "mdi:snowflake-thermometer"
    _attr_native_min_value = MIN_CO_WAT_OUT_TEMP_SET
    _attr_native_max_value = MAX_CO_WAT_OUT_TEMP_SET
    _attr_native_step = CO_WAT_OUT_TEMP_SET_STEP

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        client: GreeVersatiProtocolClient,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            client,
            PARAM_CO_WAT_OUT_TEM_SET,
            unique_id_key="cooling_water_outlet_setpoint",
        )


class GreeVersatiWatBoxSetpointNumber(GreeVersatiSetpointNumber):
    _attr_translation_key = "wat_box_tem_set"
    _attr_icon = "mdi:water-boiler"
    _attr_native_min_value = MIN_WAT_BOX_TEMP_SET
    _attr_native_max_value = MAX_WAT_BOX_TEMP_SET
    _attr_native_step = WAT_BOX_TEMP_SET_STEP

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        client: GreeVersatiProtocolClient,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            client,
            PARAM_WAT_BOX_TEM_SET,
            unique_id_key="water_box_temperature_setpoint",
        )
