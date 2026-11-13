"""Authenticated export endpoints; no anonymous or separate webhook secret."""

from http import HTTPStatus

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.components.http.const import KEY_HASS, KEY_HASS_USER

from .const import API_VERSION, DOMAIN
from .hub import EntityConflictError, validate_payload


class HAHealthBridgeInfoView(HomeAssistantView):
    """Advertise registration only while the integration is loaded."""

    url = "/api/ha_health_bridge/info"
    name = "api:ha_health_bridge:info"
    requires_auth = True

    async def get(self, request: web.Request) -> web.Response:
        """Return capabilities without any Apple Health data."""
        if DOMAIN not in request.app[KEY_HASS].data:
            return self.json_message(
                "Integration not configured", HTTPStatus.SERVICE_UNAVAILABLE
            )
        return self.json({"api_version": API_VERSION, "registered_entities": True})


class HAHealthBridgeStateView(HomeAssistantView):
    """Accept a single numeric sensor export and return its registry identity."""

    url = "/api/ha_health_bridge/states"
    name = "api:ha_health_bridge:states"
    requires_auth = True

    async def post(self, request: web.Request) -> web.Response:
        """Require admin access because this API creates registered entities."""
        user = request.get(KEY_HASS_USER)
        if user is None or not user.is_admin:
            return self.json_message("Administrator required", HTTPStatus.FORBIDDEN)
        hub = request.app[KEY_HASS].data.get(DOMAIN)
        if hub is None:
            return self.json_message(
                "Integration not configured", HTTPStatus.SERVICE_UNAVAILABLE
            )
        if request.content_length is not None and request.content_length > 65536:
            raise web.HTTPRequestEntityTooLarge(
                max_size=65536, actual_size=request.content_length
            )
        try:
            payload = validate_payload(await request.json())
        except ValueError, TypeError, OverflowError:
            return self.json_message(
                "Invalid Apple Health export", HTTPStatus.BAD_REQUEST
            )
        try:
            receipt = await hub.async_upsert(payload)
        except EntityConflictError:
            return self.json_message(
                "Entity ID belongs to another source", HTTPStatus.CONFLICT
            )
        except RuntimeError:
            return self.json_message(
                "Sensor platform not ready", HTTPStatus.SERVICE_UNAVAILABLE
            )
        return self.json(receipt)
