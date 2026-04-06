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
    PARAM_POW,
    PARAM_QUIET,
    PARAM_FAST_HT_WTER,
    PARAM_EMEGCY,
    PARAM_ASS_HT,
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
    """Base switch for writable boolean-ish parameters."""

    _attr_translation_key = None
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
    def is_on(self) -> bool | None:
        """Return switch state."""
        value = (self.coordinator.data or {}).get(self._param_key)
        if value is None:
            return None
        try:
            return bool(int(value))
        except (TypeError, ValueError):
            return bool(value)

    async def async_turn_on(self, **kwargs: object) -> None:
        """Turn on."""
        await self._client.async_set({self._param_key: 1})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: object) -> None:
        """Turn off."""
        await self._client.async_set({self._param_key: 0})
        await self.coordinator.async_request_refresh()


class GreeVersatiPowerSwitch(GreeVersatiBaseSwitch):
    """Power control switch."""

    _attr_translation_key = "power_control"

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
            unique_id_key="power_switch",
        )


class GreeVersatiQuietSwitch(GreeVersatiBaseSwitch):
    """Quiet mode switch."""

    _attr_translation_key = "quiet_mode"

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
            unique_id_key="quiet_switch",
        )


class GreeVersatiFastHotWaterSwitch(GreeVersatiBaseSwitch):
    """Fast hot water switch."""

    _attr_translation_key = "fast_hot_water"

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
            unique_id_key="fast_hot_water_switch",
        )


class GreeVersatiEmergencySwitch(GreeVersatiBaseSwitch):
    """Emergency mode switch."""

    _attr_translation_key = "emergency_mode"

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
            unique_id_key="emergency_switch",
        )


class GreeVersatiAuxHeaterSwitch(GreeVersatiBaseSwitch):
    """Aux heater switch."""

    _attr_translation_key = "aux_heater"

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
            unique_id_key="aux_heater_switch",
        )
