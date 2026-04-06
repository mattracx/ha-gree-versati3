from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode
from .entity import GreeVersatiEntity

class GreeVersatiClimate(GreeVersatiEntity, ClimateEntity):

    def __init__(self, coordinator, device_id, client):
        super().__init__(coordinator, device_id)
        self._client = client

    @property
    def hvac_mode(self):
        mod = self.coordinator.data.get("Mod")
        if mod == 1:
            return HVACMode.COOL
        elif mod == 2:
            return HVACMode.HEAT
        return HVACMode.OFF

    async def async_set_hvac_mode(self, mode):
        mapping = {
            HVACMode.COOL: 1,
            HVACMode.HEAT: 2,
            HVACMode.OFF: 0,
        }
        await self._client.set_param("Mod", mapping[mode])

    @property
    def target_temperature(self):
        if self.hvac_mode == HVACMode.COOL:
            return self.coordinator.data.get("CoWatOutTemSet")
        return self.coordinator.data.get("HeWatOutTemSet")

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")

        if self.hvac_mode == HVACMode.COOL:
            await self._client.set_param("CoWatOutTemSet", int(temp))
        else:
            await self._client.set_param("HeWatOutTemSet", int(temp))
