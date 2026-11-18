# HA Health Bridge for Home Assistant

![HA Health Bridge](custom_components/ha_health_bridge/brand/logo.png)

**Bring your Home Assistant health measurements into Apple Health.** HA Health Bridge connects the sensors you already use in Home Assistant with the Health app on your iPhone — from weight and body measurements to blood pressure and other supported health data.

**[Get the iPhone app on TestFlight](https://testflight.apple.com/join/8Mab4caQ)** · [Website (Deutsch)](https://ha-health-bridge.michelnet.ch/) · [Website (English)](https://ha-health-bridge.michelnet.ch/en/) · [Setup help](https://ha-health-bridge.michelnet.ch/en/support/)

The iPhone app is free, without ads, and available in English and German. Requires **iOS 17 or later**. It connects directly to your Home Assistant instance; no additional cloud service or MQTT broker is needed.

## Home Assistant → Apple Health

Choose which Home Assistant sensors belong in Apple Health, review the measurements, and transfer them from your iPhone.

- **Use your existing sensors:** find sources by device, area, integration, label or unit, and map them to the appropriate Apple Health data types.
- **Import values and history:** read measurements from sensor states or attributes, with unit conversion and support for counter differences. Historical measurements must still be available in Home Assistant Recorder.
- **Keep blood pressure together:** combine systolic and diastolic readings, with optional pulse, measurement time and measurement ID.
- **Review before transferring:** preview new, known and corrected measurements, then follow the results in the import reports. Stable measurement identities help avoid duplicate imports.

### Get started

1. [Install HA Health Bridge through TestFlight](https://testflight.apple.com/join/8Mab4caQ) on your iPhone.
2. Follow the setup assistant to connect to your Home Assistant instance and sign in.
3. Under **Import**, map your sensors to Apple Health data types and grant the requested Apple Health write permissions.
4. Review the import preview and start the transfer. Automatic transfers can be enabled in the app settings; iOS controls when background work runs.

**Home Assistant → Apple Health works directly through the iPhone app and does not require the integration in this repository.**

## Optional: Apple Health → Home Assistant

This repository provides the integration for the optional reverse direction. Enable export in the iPhone app to make selected Apple Health values available as Home Assistant sensors — for dashboards, history and automations.

The integration creates one device per iPhone export source and keeps stable sensor identities. Names, entity IDs, icons and areas you customize in Home Assistant remain intact when new values arrive. Latest values are stored locally and restored after a restart.

Requires **Home Assistant 2026.11 or later**.

### Install the integration

Install the [latest release](https://github.com/michelnet/ha-health-bridge/releases/latest) through HACS / the Home Assistant Marketplace:

[![Open HA Health Bridge in the Home Assistant Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=michelnet&repository=ha-health-bridge&category=integration)

Use the button above, or add `https://github.com/michelnet/ha-health-bridge` under **Settings → Marketplace** as a custom repository of type **Integration**. Install HA Health Bridge, then add **HA Health Bridge** under **Settings → Devices & services**. Follow any restart request shown by Home Assistant. Inclusion in the default Marketplace catalog requires a separate HACS review; custom-repository installation is available while that review is pending.

For manual installation, copy `custom_components/ha_health_bridge/` into your Home Assistant configuration's `custom_components/` folder, restart Home Assistant and add the integration under Devices & services.

### Configure the optional export

Enable the optional export in the iPhone app, select the Apple Health data types and allow the requested read access. Use your existing Home Assistant connection and an administrator token for this export. The app detects the integration automatically.

The authenticated endpoints are `GET /api/ha_health_bridge/info` and `POST /api/ha_health_bridge/states`. The write endpoint requires an administrator. Received definitions and latest states are saved privately under `.storage/ha_health_bridge` and restored after a restart. This creates sensor states; it does not backfill historical Recorder measurements. A normal Home Assistant backup may include these stored values.

Disable the export in the app before removing the integration. Existing Recorder history follows Home Assistant's retention settings. A new iPhone export identity can create a new source; use another prefix if a sensor ID is already taken.

## License

Copyright 2026 Thomas Michel. This integration is licensed under the
[Apache License, Version 2.0](LICENSE). This license applies to this repository.

[TestFlight](https://testflight.apple.com/join/8Mab4caQ) · [App and website](https://ha-health-bridge.michelnet.ch/) · [Releases](https://github.com/michelnet/ha-health-bridge/releases) · [Support](mailto:ha-health-bridge@michelnet.ch)
