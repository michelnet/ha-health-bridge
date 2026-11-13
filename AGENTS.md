# HA Health Bridge — Home Assistant integration

This repository owns `custom_components/ha_health_bridge`, installation metadata
and integration releases for Home Assistant 2026.11+.

GitHub repository: `michelnet/ha-health-bridge`, public. This integration builds
independently. Keep the repository limited to distributable integration sources.

Do not include personal filesystem paths or external workspace layouts in
source files, documentation, commit messages or generated artifacts.

## Working agreements

- Respond to the user in German. Keep `translations/en.json` and `de.json` aligned.
- Preserve domain `ha_health_bridge`, API version and stable source/unique IDs.
- Protect existing entity IDs, user names/icons/areas, disabled states and stored
  values across updates and reloads. The write API requires administrator access.
- Use fictional test data. Never commit tokens, `.storage` contents, health
  records or local certificates. Keep generated ZIPs and virtualenvs ignored.
- Preserve the approved `brand/` assets.
- Match the integration manifest version to the integration's GitHub release tag.
  The iPhone app has an independent version. Marketplace installs use the standard
  `custom_components/` layout, without `zip_release`.

## Validation

CI runs Ruff against the component, official hassfest and HACS repository
validation. Keep documentation bundles, examples and local development files
out of version control. Checks do not establish a catalog listing, a published
release or a real iPhone transfer.
