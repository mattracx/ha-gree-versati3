from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .constants import (
    CONF_DEVICE_ID,
    DATA_COORDINATOR,
    DATA_ENTRIES,
    PARAM_ALL_ERR,
    PARAM_ALL_IN_WAT_TEM_HI,
    PARAM_ALL_IN_WAT_TEM_LO,
    PARAM_ALL_OUT_WAT_TEM_HI,
    PARAM_ALL_OUT_WAT_TEM_LO,
    PARAM_ASS_HT,
    PARAM_ELC_HE1_RUN_STA,
    PARAM_ELC_HE2_RUN_STA,
    PARAM_EMEGCY,
    PARAM_FAST_HT_WTER,
    PARAM_HE_WAT_OUT_TEM_SET,
    PARAM_JF_ERROR_CODE,
    PARAM_MOD,
    PARAM_MODEL_TYPE,
    PARAM_POW,
    PARAM_QUIET,
    PARAM_RSSI,
    PARAM_SY_AN_FRO_RUN_STA,
    PARAM_TEM_UN,
    PARAM_VENDER,
    PARAM_VER,
    PARAM_VERSATI_SERIES,
    PARAM_WAT_BOX_ELC_HE_RUN_STA,
    PARAM_WAT_BOX_TEM_SET,
)
from .coordinator import GreeVersatiCoordinator
from .entity import GreeVersatiEntity


@dataclass(frozen=True, kw_only=True)
class GreeVersatiSensorDescription(SensorEntityDescription):
    param_key: str


SENSOR_DESCRIPTIONS: tuple[GreeVersatiSensorDescription, ...] = (
    GreeVersatiSensorDescription(
        key="he_wat_out_tem_set",
        translation_key="he_wat_out_tem_set",
        param_key=PARAM_HE_WAT_OUT_TEM_SET,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="mdi:radiator",
    ),
    GreeVersatiSensorDescription(
        key="wat_box_tem_set",
        translation_key="wat_box_tem_set",
        param_key=PARAM_WAT_BOX_TEM_SET,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="mdi:water-boiler",
    ),
    GreeVersatiSensorDescription(
        key="tem_un",
        translation_key="tem_un",
        param_key=PARAM_TEM_UN,
        icon="mdi:thermometer",
    ),
    GreeVersatiSensorDescription(
        key="all_err",
        translation_key="all_err",
        param_key=PARAM_ALL_ERR,
        icon="mdi:alert-circle",
    ),
    GreeVersatiSensorDescription(
        key="jf_error_code",
        translation_key="jf_error_code",
        param_key=PARAM_JF_ERROR_CODE,
        icon="mdi:alert-circle-outline",
    ),
    GreeVersatiSensorDescription(
        key="mod",
        translation_key="mod",
        param_key=PARAM_MOD,
        icon="mdi:cog-refresh",
    ),
    GreeVersatiSensorDescription(
        key="pow",
        translation_key="pow",
        param_key=PARAM_POW,
        icon="mdi:power",
    ),
    GreeVersatiSensorDescription(
        key="ass_ht",
        translation_key="ass_ht",
        param_key=PARAM_ASS_HT,
        entity_registry_enabled_default=False,
        icon="mdi:heating-coil",
    ),
    GreeVersatiSensorDescription(
        key="elc_he1_run_sta",
        translation_key="elc_he1_run_sta",
        param_key=PARAM_ELC_HE1_RUN_STA,
        entity_registry_enabled_default=False,
        icon="mdi:flash",
    ),
    GreeVersatiSensorDescription(
        key="elc_he2_run_sta",
        translation_key="elc_he2_run_sta",
        param_key=PARAM_ELC_HE2_RUN_STA,
        entity_registry_enabled_default=False,
        icon="mdi:flash",
    ),
    GreeVersatiSensorDescription(
        key="wat_box_elc_he_run_sta",
        translation_key="wat_box_elc_he_run_sta",
        param_key=PARAM_WAT_BOX_ELC_HE_RUN_STA,
        entity_registry_enabled_default=False,
        icon="mdi:water-boiler",
    ),
    GreeVersatiSensorDescription(
        key="quiet",
        translation_key="quiet",
        param_key=PARAM_QUIET,
        entity_registry_enabled_default=False,
        icon="mdi:volume-low",
    ),
    GreeVersatiSensorDescription(
        key="fast_ht_wter",
        translation_key="fast_ht_wter",
        param_key=PARAM_FAST_HT_WTER,
        entity_registry_enabled_default=False,
        icon="mdi:water-boiler-alert",
    ),
    GreeVersatiSensorDescription(
        key="emegcy",
        translation_key="emegcy",
        param_key=PARAM_EMEGCY,
        entity_registry_enabled_default=False,
        icon="mdi:alert-octagon",
    ),
    GreeVersatiSensorDescription(
        key="sy_an_fro_run_sta",
        translation_key="sy_an_fro_run_sta",
        param_key=PARAM_SY_AN_FRO_RUN_STA,
        entity_registry_enabled_default=False,
        icon="mdi:snowflake-alert",
    ),
    GreeVersatiSensorDescription(
        key="rssi",
        translation_key="rssi",
        param_key=PARAM_RSSI,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:wifi",
    ),
    GreeVersatiSensorDescription(
        key="versati_series",
        translation_key="versati_series",
        param_key=PARAM_VERSATI_SERIES,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:label",
    ),
    GreeVersatiSensorDescription(
        key="model_type",
        translation_key="model_type",
        param_key=PARAM_MODEL_TYPE,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:identifier",
    ),
    GreeVersatiSensorDescription(
        key="ver",
        translation_key="ver",
        param_key=PARAM_VER,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:chip",
    ),
    GreeVersatiSensorDescription(
        key="vender",
        translation_key="vender",
        param_key=PARAM_VENDER,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:factory",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    runtime_data = hass.data[entry.domain][DATA_ENTRIES][entry.entry_id]
    coordinator = runtime_data[DATA_COORDINATOR]
    device_id = entry.data[CONF_DEVICE_ID]

    entities = [
        *(
            GreeVersatiSensor(coordinator, device_id, description)
            for description in SENSOR_DESCRIPTIONS
        ),
        GreeVersatiWaterInTemperatureSensor(coordinator, device_id),
        GreeVersatiWaterOutTemperatureSensor(coordinator, device_id),
        GreeVersatiWaterDeltaTSensor(coordinator, device_id),
    ]

    async_add_entities(entities)


class GreeVersatiSensor(GreeVersatiEntity, SensorEntity):
    entity_description: GreeVersatiSensorDescription

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
        description: GreeVersatiSensorDescription,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            description.param_key,
            unique_id_key=description.key,
        )
        self.entity_description = description

    @property
    def translation_key(self) -> str | None:
        return self.entity_description.translation_key

    @property
    def native_value(self):
        value = (self.coordinator.data or {}).get(self.entity_description.param_key)
        if value in (None, "", "null"):
            return None
        return value


class GreeVersatiWaterInTemperatureSensor(GreeVersatiEntity, SensorEntity):
    _attr_translation_key = "water_in_temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer-chevron-down"

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            "water_in_temperature",
            unique_id_key="water_in_temperature",
        )

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        hi = data.get(PARAM_ALL_IN_WAT_TEM_HI)
        lo = data.get(PARAM_ALL_IN_WAT_TEM_LO)

        if hi in (None, "", "null") or lo in (None, "", "null"):
            return None

        try:
            return round((int(hi) - 100) + (int(lo) / 10), 1)
        except (TypeError, ValueError):
            return None


class GreeVersatiWaterOutTemperatureSensor(GreeVersatiEntity, SensorEntity):
    _attr_translation_key = "water_out_temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer-chevron-up"

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            "water_out_temperature",
            unique_id_key="water_out_temperature",
        )

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}
        hi = data.get(PARAM_ALL_OUT_WAT_TEM_HI)
        lo = data.get(PARAM_ALL_OUT_WAT_TEM_LO)

        if hi in (None, "", "null") or lo in (None, "", "null"):
            return None

        try:
            return round((int(hi) - 100) + (int(lo) / 10), 1)
        except (TypeError, ValueError):
            return None


class GreeVersatiWaterDeltaTSensor(GreeVersatiEntity, SensorEntity):
    _attr_translation_key = "water_delta_t"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:delta"

    def __init__(
        self,
        coordinator: GreeVersatiCoordinator,
        device_id: str,
    ) -> None:
        super().__init__(
            coordinator,
            device_id,
            "water_delta_t",
            unique_id_key="water_delta_t",
        )

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data or {}

        in_hi = data.get(PARAM_ALL_IN_WAT_TEM_HI)
        in_lo = data.get(PARAM_ALL_IN_WAT_TEM_LO)
        out_hi = data.get(PARAM_ALL_OUT_WAT_TEM_HI)
        out_lo = data.get(PARAM_ALL_OUT_WAT_TEM_LO)

        if (
            in_hi in (None, "", "null")
            or in_lo in (None, "", "null")
            or out_hi in (None, "", "null")
            or out_lo in (None, "", "null")
        ):
            return None

        try:
            tin = (int(in_hi) - 100) + (int(in_lo) / 10)
            tout = (int(out_hi) - 100) + (int(out_lo) / 10)
            return round(tout - tin, 1)
        except (TypeError, ValueError):
            return None
