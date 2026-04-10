from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .constants import DOMAIN


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
        model = data.get("ModelType") or "Versati 3"

        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Chiller - Heat Pump",
            "manufacturer": "Gree",
            "model": str(model),
        }
