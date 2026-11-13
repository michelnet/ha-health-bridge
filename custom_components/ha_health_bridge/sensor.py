"""Sensors with real entity-registry identities and per-iPhone devices."""

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers import entity_platform
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Add restored entities and expose the platform's awaitable add method."""
    hub = hass.data[DOMAIN]
    hub.async_add_entities = (
        entity_platform.async_get_current_platform().async_add_entities
    )
    for record in hub.records.values():
        sensor = HAHealthBridgeSensor(record)
        hub.entities[record["unique_id"]] = sensor
    async_add_entities(list(hub.entities.values()))


class HAHealthBridgeSensor(SensorEntity):
    """A numeric Apple Health sensor whose identity never depends on its name."""

    _attr_should_poll = False

    def __init__(self, record: dict) -> None:
        self._attr_unique_id = record["unique_id"]
        self.entity_id = record["entity_id"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, record["source_id"])},
            name="HA Health Bridge " + record["source_id"][:8],
            manufacturer="HA Health Bridge",
            model="Apple Health Export",
        )
        self._accept(record)

    def _accept(self, record: dict) -> None:
        attrs = record["attributes"]
        self._attr_name = attrs.get("friendly_name", record["health_type"])
        self._attr_icon = attrs.get("icon", "mdi:heart-pulse")
        self._attr_native_unit_of_measurement = attrs.get("unit_of_measurement")
        self._attr_state_class = (
            SensorStateClass(value) if (value := attrs.get("state_class")) else None
        )
        self._attr_available = record["state"] != "unavailable"
        self._attr_native_value = (
            float(record["state"]) if self._attr_available else None
        )
        self._attr_extra_state_attributes = {
            key: value
            for key, value in attrs.items()
            if key
            not in ("friendly_name", "icon", "unit_of_measurement", "state_class")
        }

    @callback
    def async_accept(self, record: dict) -> None:
        """Publish only if HA has enabled and added this entity."""
        self._accept(record)
        if self.hass is not None and self.platform is not None:
            if self.registry_entry is None or not self.registry_entry.disabled:
                self.async_write_ha_state()
