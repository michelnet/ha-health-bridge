# HA Health Bridge for Home Assistant

![HA Health Bridge](custom_components/ha_health_bridge/brand/logo.png)

Register Apple Health values exported by the HA Health Bridge iPhone app as Home Assistant sensors, with stable unique IDs and one device per iPhone export source. Names, entity IDs, icons and areas changed in Home Assistant remain intact when new values arrive.

Requires **Home Assistant 2026.11 or later**. The optional integration supports **Apple Health → Home Assistant**. Importing Home Assistant measurements into Apple Health does not require it. No additional cloud service or MQTT broker is needed.

## Installation

Public source repository: [michelnet/ha-health-bridge](https://github.com/michelnet/ha-health-bridge). Until the first integration release is available, use the manual installation below.

After publication, add its GitHub URL under **Settings → Marketplace** as a custom repository of type **Integration**, install HA Health Bridge, then add **HA Health Bridge** under **Settings → Devices & services**. Follow any restart request shown by Home Assistant. Inclusion in the default Marketplace catalog is a separate review.

For manual installation, copy `custom_components/ha_health_bridge/` into your Home Assistant configuration's `custom_components/` folder, restart Home Assistant and add the integration under Devices & services.

## Configure and operate

Enable the optional export in the iPhone app, select the Apple Health data types and allow the requested read access. Use your existing Home Assistant connection and an administrator token for this export. The app detects the integration automatically.

The authenticated endpoints are `GET /api/ha_health_bridge/info` and `POST /api/ha_health_bridge/states`. The write endpoint requires an administrator. Received definitions and latest states are saved privately under `.storage/ha_health_bridge` and restored after a restart. This creates sensor states; it does not backfill historical Recorder measurements. A normal Home Assistant backup may include these stored values.

Disable the export in the app before removing the integration. Existing Recorder history follows Home Assistant's retention settings. A new iPhone export identity can create a new source; use another prefix if a sensor ID is already taken.

## Releases

CI runs Ruff, hassfest and HACS repository validation. Integration releases use
the same tag and manifest version. `hacs.json` uses the standard
`custom_components/` layout; no release ZIP is required. A source push does not
publish a release or add the integration to the default catalog.

## License

Copyright 2026 Thomas Michel. This integration is licensed under the
[Apache License, Version 2.0](LICENSE). This license applies to this repository.

[App and website](https://ha-health-bridge.michelnet.ch/) · [Support](mailto:ha-health-bridge@michelnet.ch) · [Marketplace publishing requirements](https://contributors.home-assistant.io/marketplace/guides/integrations/)
