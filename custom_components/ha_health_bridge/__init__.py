"""Registered Home Assistant sensors for the HA Health Bridge iPhone app."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api import HAHealthBridgeInfoView, HAHealthBridgeStateView
from .const import DOMAIN
from .hub import HAHealthBridgeHub

PLATFORMS = [Platform.SENSOR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register authenticated views, also while the entry is unloaded."""
    hass.http.register_view(HAHealthBridgeInfoView())
    hass.http.register_view(HAHealthBridgeStateView())
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Load saved entity definitions before forwarding sensor setup."""
    hub = HAHealthBridgeHub(hass)
    await hub.async_load()
    hass.data[DOMAIN] = hub
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entities without removing their registry identities."""
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data.pop(DOMAIN, None)
        return True
    return False


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove this integration's saved payloads when explicitly removed."""
    from homeassistant.helpers.storage import Store

    from .const import STORAGE_VERSION

    await Store(hass, STORAGE_VERSION, DOMAIN).async_remove()
