from __future__ import annotations

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .constants import DOMAIN, PARAM_MAC


class GreeVersatiEntity(CoordinatorEntity):
    """Base entity for Gree Versati."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_id: str,
        param_key: str,
        *,
        unique_id_key: str | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._device_id = device_id
        self._param_key = param_key
        self._attr_unique_id = f"{device_id}_{unique_id_key or param_key}"

    @property
    def device_info(self) -> dict:
        data = self.coordinator.data or {}

        model_type = data.get("ModelType")
        mac = data.get(PARAM_MAC)

        connections = set()
        if isinstance(mac, str) and mac:
            # Normalize to lower-case colon-separated MAC
            normalized_mac = mac.strip().lower().replace("-", ":")
            connections.add((CONNECTION_NETWORK_MAC, normalized_mac))

        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "connections": connections,
            "name": "Chiller - Heat Pump",
            "manufacturer": "Gree",
            "model": "Versati 3" if not model_type else f"Versati 3 ({model_type})",
        }
