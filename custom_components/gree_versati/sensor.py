"""Sensor platform for Gree Versati."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .constants import (
    CONF_DEVICE_ID,
    DATA_COORDINATOR,
    DATA_ENTRIES,
    PARAM_ALL_ERR,
    PARAM_HE_WAT_OUT_TEM_SET,
    PARAM_MOD,
    PARAM_POW,
    PARAM_TEM_UN,
    PARAM_WAT_BOX_TEM_SET,
)
from .coordinator import GreeVersatiCoordinator
from .entity import GreeVersatiEntity


@dataclass(frozen=True, kw_only=True)
class GreeVersatiSensorDescription(SensorEntityDescription):
    """Description of a Gree Versati sensor."""

    param_key: str


SENSOR_DESCRIPTIONS: tuple[GreeVersatiSensorDescription, ...] = (
    GreeVersatiSensorDescription(
        key="he_wat_out_tem_set",
        translation_key="he_wat_out_tem_set",
        param_key=PARAM_HE_WAT_OUT_TEM_SET,
    ),
    GreeVersatiSensorDescription(
        key="wat_box_tem_set",
        translation_key="wat_box_tem_set",
        param_key=PARAM_WAT_BOX_TEM_SET,
    ),
    GreeVersatiSensorDescription(
        key="tem_un",
        translation_key="tem_un",
        param_key=PARAM_TEM_UN,
    ),
    GreeVersatiSensorDescription(
        key="all_err",
        translation_key="all_err",
        param_key=PARAM_ALL_ERR,
    ),
    GreeVersatiSensorDescription(
        key="mod",
        translation_key="mod",
        param_key=PARAM_MOD,
    ),
    GreeVersatiSensorDescription(
        key="pow",
        translation_key="pow",
        param_key=PARAM_POW,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors from a config entry."""
    runtime_data = hass.data[entry.domain][DATA_ENTRIES][entry.entry_id]
    coordinator = runtime_data[DATA_COORDINATOR]
    device_id = entry.data[CONF_DEVICE_ID]
    GreeVersatiWaterInletTempSensor(coordinator, device_id),
    GreeVersatiWaterOutletTempSensor(coordinator, device_id),
    GreeVersatiRSSISensor(coordinator, device_id),
    GreeVersatiErrorSensor(coordinator, device_id),

    async_add_entities(
        GreeVersatiSensor(coordinator, device_id, description)
        for description in SENSOR_DESCRIPTIONS
    )


class GreeVersatiSensor(GreeVersatiEntity, SensorEntity):
    """Represents a generic value sensor from device parameters."""

    entity_description: GreeVersatiSensorDescription

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        description: GreeVersatiSensorDescription,
    ) -> None:
        super().__init__(coordinator, device_id, description.param_key)
        self.entity_description = description

    @property
    def native_value(self) -> str | int | float | bool | None:
        """Return raw protocol value."""
        return (self.coordinator.data or {}).get(self.entity_description.param_key)
class GreeVersatiWaterInletTempSensor(GreeVersatiEntity, SensorEntity):
    _attr_name = "Water Inlet Temperature"
    _attr_native_unit_of_measurement = "°C"

    def _handle_coordinator_update(self):
        hi = self.coordinator.data.get("AllInWatTemHi")
        lo = self.coordinator.data.get("AllInWatTemLo")

        if hi is not None and lo is not None:
            self._attr_native_value = ((hi << 8) | lo) / 10
        self.async_write_ha_state()


class GreeVersatiWaterOutletTempSensor(GreeVersatiEntity, SensorEntity):
    _attr_name = "Water Outlet Temperature"
    _attr_native_unit_of_measurement = "°C"

    def _handle_coordinator_update(self):
        hi = self.coordinator.data.get("AllOutWatTemHi")
        lo = self.coordinator.data.get("AllOutWatTemLo")

        if hi is not None and lo is not None:
            self._attr_native_value = ((hi << 8) | lo) / 10
        self.async_write_ha_state()

class GreeVersatiRSSISensor(GreeVersatiEntity, SensorEntity):
    _attr_name = "WiFi Signal"
    _attr_native_unit_of_measurement = "dBm"

    def _handle_coordinator_update(self):
        self._attr_native_value = self.coordinator.data.get("rssi")
        self.async_write_ha_state()


class GreeVersatiErrorSensor(GreeVersatiEntity, SensorEntity):
    _attr_name = "Error Code"

    def _handle_coordinator_update(self):
        self._attr_native_value = self.coordinator.data.get("AllErr")
        self.async_write_ha_state()
