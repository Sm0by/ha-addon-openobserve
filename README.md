<p align="center">
  <img src="openobserve/logo.png" alt="OpenObserve for Home Assistant" width="400">
</p>

# OpenObserve app for Home Assistant

[![CI](https://github.com/Sm0by/ha-addon-openobserve/actions/workflows/ci.yaml/badge.svg)](https://github.com/Sm0by/ha-addon-openobserve/actions/workflows/ci.yaml)
[![Release](https://img.shields.io/github/v/release/Sm0by/ha-addon-openobserve)](https://github.com/Sm0by/ha-addon-openobserve/releases)
![amd64](https://img.shields.io/badge/amd64-yes-green)
![aarch64](https://img.shields.io/badge/aarch64-yes-green)

Runs [OpenObserve](https://github.com/openobserve/openobserve) as a Home Assistant app: one place to store, search and chart logs, metrics and traces. Anything that speaks OpenTelemetry (OTLP) can send data to it, over HTTP or gRPC.

- Single-node OpenObserve, data stays in the app's own storage and is part of Home Assistant backups
- OTLP/HTTP on port 5080, OTLP/gRPC on port 5081
- Web interface for search, dashboards and alerts
- Retention, log level and any further `ZO_*` setting configurable in the app options

## Installation

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FSm0by%2Fha-addon-openobserve)

Or by hand:

1. In Home Assistant open **Settings → Apps → App Store**.
2. Open the menu (⋮) → **Repositories** and add `https://github.com/Sm0by/ha-addon-openobserve`.
3. Install **OpenObserve**, set the administrator email and password on the **Configuration** tab and start it.

Setup, sending data and resource tips are in the [documentation](openobserve/DOCS.md).

## Requirements

- Home Assistant OS or Supervised on amd64 or aarch64 (e.g. Raspberry Pi 4/5 with 64-bit OS)
- OpenObserve uses up to half of the memory for in-memory tables by default; see [Resources](openobserve/DOCS.md#resources) for small devices

## Known limitations

- No Ingress: the web interface is opened on port 5080, not in the Home Assistant sidebar.
- No TLS: ports 5080 and 5081 speak plain HTTP and gRPC in your network. Close them on the **Network** tab if you do not need them from other devices, or put a reverse proxy with TLS in front.

## Support

Bugs and ideas: [GitHub issues](https://github.com/Sm0by/ha-addon-openobserve/issues).

## License

The files in this repository are under the [MIT License](LICENSE). The app image contains the unmodified OpenObserve binary, which is licensed under the [GNU AGPL v3](https://github.com/openobserve/openobserve/blob/main/LICENSE). This project is not affiliated with OpenObserve Inc. or the Home Assistant project.
