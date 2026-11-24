# Changelog

## 0.2.2

- Update OpenObserve from v1.2.0-rc2 to v1.2.0 ([release notes](https://github.com/openobserve/openobserve/releases/tag/v1.2.0))

## 0.2.1

- Ship the license text of OpenObserve (AGPL-3.0) and the link to its source code in the app (`/usr/share/doc/openobserve/`)
- New icon and logo without elements of the Home Assistant logo
- Document how to allow alerts to devices in your network (`ZO_SSRF_ALLOWED_CIDRS`)

## 0.2.0

- Install a prebuilt image from the GitHub Container Registry instead of building the app on the device
- Add an icon and a logo

## 0.1.2

- Update OpenObserve to v1.2.0-rc2 (release candidate of the next OpenObserve version)
- Make a backup before updating: v1.2.0 migrates the database, going back to 0.1.1 needs the backup

## 0.1.1

- Check the password rules of OpenObserve before starting, with a clear error instead of a crash
- Register the service under `user-bundles.d` (removes the s6-overlay deprecation warning)
- Document the watchdog and the password rules

## 0.1.0

- First version with OpenObserve v1.1.2 (amd64, aarch64)
- Options for administrator, retention, log level, telemetry, web URL and additional `ZO_*` variables
- Docker health check via `/healthz`, cold backups
