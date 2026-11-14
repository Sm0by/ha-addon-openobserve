# Changelog

## 0.1.2

- Update OpenObserve to v1.2.0-rc2 (release candidate, to test the MCP endpoint)
- Make a backup before updating: v1.2.0 migrates the database, going back to 0.1.1 needs the backup

## 0.1.1

- Check the password rules of OpenObserve before starting, with a clear error instead of a crash
- Register the service under `user-bundles.d` (removes the s6-overlay deprecation warning)
- Document the watchdog and the password rules

## 0.1.0

- First version with OpenObserve v1.1.2 (amd64, aarch64)
- Options for administrator, retention, log level, telemetry, web URL and additional `ZO_*` variables
- Docker health check via `/healthz`, cold backups
