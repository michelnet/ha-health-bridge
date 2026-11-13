"""Validate exports and retain stable identities across HA restarts."""

import asyncio
import json
import math
import re
from copy import deepcopy
from uuid import UUID

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.storage import Store

from .const import DOMAIN, STORAGE_VERSION


class EntityConflictError(ValueError):
    """A requested entity ID is owned by another source or integration."""


def validate_payload(raw: object) -> dict:
    """Accept only a bounded numeric Apple Health export with a consistent identity."""
    if not isinstance(raw, dict):
        raise ValueError("Invalid payload")
    required = ("entity_id", "source_id", "unique_id", "health_type", "state")
    if not all(isinstance(raw.get(key), str) for key in required):
        raise ValueError("Missing export fields")
    if not re.fullmatch(r"sensor\.[a-z0-9_]{1,200}", raw["entity_id"]):
        raise ValueError("Invalid entity ID")
    source = str(UUID(raw["source_id"]))
    health_type = raw["health_type"]
    if not re.fullmatch(r"HK[A-Za-z0-9]{1,150}", health_type):
        raise ValueError("Invalid Apple Health type")
    unique_id = f"{source}_{health_type}"
    if raw["unique_id"] != unique_id:
        raise ValueError("Inconsistent unique ID")
    state = raw["state"]
    if len(state) > 255 or (state != "unavailable" and not math.isfinite(float(state))):
        raise ValueError("Invalid state")
    attrs = raw.get("attributes")
    if not isinstance(attrs, dict):
        raise ValueError("Invalid attributes")
    # This endpoint accepts a small export, never a historical dataset.
    if len(json.dumps(attrs, allow_nan=False).encode()) > 32768:
        raise ValueError("Attributes too large")
    for name in ("friendly_name", "icon", "unit_of_measurement"):
        if name in attrs and (
            not isinstance(attrs[name], str) or len(attrs[name]) > 255
        ):
            raise ValueError("Invalid sensor metadata")
    if attrs.get("state_class") not in (None, "measurement", "total_increasing"):
        raise ValueError("Invalid state class")
    attrs = deepcopy(attrs)
    attrs.update(
        ha_health_bridge_export=True,
        ha_health_bridge_source_id=source,
        unique_id=unique_id,
        health_type=health_type,
    )
    return {
        **{key: raw[key] for key in required},
        "source_id": source,
        "attributes": attrs,
    }


class HAHealthBridgeHub:
    """Serialize registration and persist the last accepted export per identity."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.records: dict[str, dict] = {}
        self.entities: dict = {}
        self.async_add_entities = None
        self._store = Store(hass, STORAGE_VERSION, DOMAIN, private=True)
        self._lock = asyncio.Lock()

    async def async_load(self) -> None:
        """Restore definitions independently of the iPhone's next update."""
        if saved := await self._store.async_load():
            self.records = {
                record["unique_id"]: record
                for raw in saved.get("records", [])
                for record in [validate_payload(raw)]
            }

    async def async_upsert(self, record: dict) -> dict:
        """Update by unique ID, preserving user-defined entity IDs and settings."""
        from .sensor import HAHealthBridgeSensor

        async with self._lock:
            if self.async_add_entities is None:
                raise RuntimeError("Sensor platform is not ready")
            unique_id = record["unique_id"]
            registry = er.async_get(self.hass)
            existing_id = registry.async_get_entity_id("sensor", DOMAIN, unique_id)
            adopt_legacy = None
            if existing_id is None:
                proposed = record["entity_id"]
                if registry.async_get(proposed):
                    raise EntityConflictError("Entity ID already registered")
                if current := self.hass.states.get(proposed):
                    attrs = current.attributes
                    if (
                        attrs.get("ha_health_bridge_export") is not True
                        or attrs.get("health_type") != record["health_type"]
                        or attrs.get("ha_health_bridge_source_id")
                        not in (None, record["source_id"])
                    ):
                        raise EntityConflictError("Entity ID already in use")
                    # Adopt only an unregistered, matching legacy REST state.
                    # Recorder history belongs to the unchanged entity ID.
                    adopt_legacy = proposed
            stored = dict(self.records)
            stored[unique_id] = record
            await self._store.async_save({"records": list(stored.values())})
            self.records = stored
            if adopt_legacy is not None:
                self.hass.states.async_remove(adopt_legacy)
            if sensor := self.entities.get(unique_id):
                sensor.async_accept(record)
            else:
                sensor = HAHealthBridgeSensor(record)
                self.entities[unique_id] = sensor
                await self.async_add_entities([sensor])
            entity_id = registry.async_get_entity_id("sensor", DOMAIN, unique_id)
            if entity_id is None:
                raise RuntimeError("Entity registration failed")
            return {"unique_id": unique_id, "entity_id": entity_id, "registered": True}
