from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import GreeVersatiProtocolClient
from .constants import (
    CONF_DEVICE_ID,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DATA_ENTRIES,
    MODE_OPTIONS,
    PARAM_MOD,
)
from .coordinator import GreeVersatiCoordinator
from .entity import GreeVersatiEntity

_LABEL_BY_MODE = {value: key for key, value in MODE_OPTIONS.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    runtime_data = hass.data[entry.domain][DATA_ENTRIES][entry.entry_id]

    async_add_entities(
        [
            GreeVersatiModeSelect(
                runtime_data[DATA_COORDINATOR],
                entry.data[CONF_DEVICE_ID],
                runtime_data[DATA_CLIENT],
            )
        ]
    )


class GreeVersatiModeSelect(GreeVersatiEntity, SelectEntity):
    _attr_translation_key = "mode_control"
    _attr_icon = "mdi:tune-variant"

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
            unique_id_key="mode_control",
        )
        self._client = client
        self._attr_options = list(MODE_OPTIONS.keys())

    @property
    def current_option(self) -> str | None:
        value = (self.coordinator.data or {}).get(PARAM_MOD)
        try:
            return _LABEL_BY_MODE.get(int(value))
        except (TypeError, ValueError):
            return None

    async def async_select_option(self, option: str) -> None:
        if option not in MODE_OPTIONS:
            return
        await self._client.async_set({PARAM_MOD: MODE_OPTIONS[option]})
        await self.coordinator.async_request_refresh()
