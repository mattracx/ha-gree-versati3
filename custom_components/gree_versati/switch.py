from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import GreeVersatiProtocolClient
from .constants import (
    CONF_DEVICE_ID,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DATA_ENTRIES,
    PARAM_ASS_HT,
    PARAM_EMEGCY,
    PARAM_FAST_HT_WTER,
    PARAM_POW,
    PARAM_QUIET,
)
from .coordinator import GreeVersatiCoordinator
from .entity import GreeVersatiEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities."""
    runtime_data = hass.data[entry.domain][DATA_ENTRIES][entry.entry_id]

    async_add_entities(
        [
            GreeVersatiPowerSwitch(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
            GreeVersatiQuietSwitch(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
            GreeVersatiFastHotWaterSwitch(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
            GreeVersatiEmergencySwitch(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
            GreeVersatiAuxHeaterSwitch(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            ),
        ]
    )


class GreeVersatiBaseSwitch(GreeVersatiEntity, SwitchEntity):
    """Base switch for writable boolean-style parameters."""

    _param_key: str

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
    def available(self) -> bool:
        """Entity is available when coordinator is available."""
        return super().available

    @property
    def is_on(self) -> bool:
        """Return switch state.

        Missing values are treated as False instead of unavailable,
        because some optional Gree params are not always returned.
        """
        value = (self.coordinator.data or {}).get(self._param_key)

        if value in (None, "", "null"):
            return False

        try:
            return bool(int(value))
        except (TypeError, ValueError):
            return bool(value)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self._client.async_set({self._param_key: 1})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self._client.async_set({self._param_key: 0})
        await self.coordinator.async_request_refresh()


class GreeVersatiPowerSwitch(GreeVersatiBaseSwitch):
    """Main power switch."""

    _attr_translation_key = "power_control"
    _attr_icon = "mdi:power"
    _attr_name = "Power"

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
            PARAM_POW,
            unique_id_key="power_control",
        )


class GreeVersatiQuietSwitch(GreeVersatiBaseSwitch):
    """Quiet mode switch."""

    _attr_translation_key = "quiet_mode"
    _attr_icon = "mdi:sleep"
    _attr_name = "Quiet mode"
    _attr_entity_registry_enabled_default = False

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
            PARAM_QUIET,
            unique_id_key="quiet_mode",
        )


class GreeVersatiFastHotWaterSwitch(GreeVersatiBaseSwitch):
    """Fast hot water switch."""

    _attr_translation_key = "fast_hot_water"
    _attr_icon = "mdi:water-boiler"
    _attr_name = "Fast hot water"
    _attr_entity_registry_enabled_default = False

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
            PARAM_FAST_HT_WTER,
            unique_id_key="fast_hot_water",
        )


class GreeVersatiEmergencySwitch(GreeVersatiBaseSwitch):
    """Emergency mode switch."""

    _attr_translation_key = "emergency_mode"
    _attr_icon = "mdi:alert"
    _attr_name = "Emergency mode"
    _attr_entity_registry_enabled_default = False

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
            PARAM_EMEGCY,
            unique_id_key="emergency_mode",
        )


class GreeVersatiAuxHeaterSwitch(GreeVersatiBaseSwitch):
    """Aux heater switch."""

    _attr_translation_key = "aux_heater"
    _attr_icon = "mdi:radiator"
    _attr_name = "Aux heater"
    _attr_entity_registry_enabled_default = False

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
            PARAM_ASS_HT,
            unique_id_key="aux_heater",
        )
