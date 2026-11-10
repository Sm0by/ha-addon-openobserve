# OpenObserve

[OpenObserve](https://github.com/openobserve/openobserve) stores and searches logs, metrics and traces. Applications send data via OpenTelemetry (OTLP) over HTTP or gRPC.

The app runs OpenObserve in single-node mode. All data is stored in the app's own storage (`/data/openobserve`).

## Installation

1. Add the repository `https://github.com/Sm0by/ha-addon-openobserve` under **Settings → Apps → App Store → ⋮ → Repositories**.
2. Install **OpenObserve**.
3. Set `root_email` and `root_password` on the **Configuration** tab.
4. Start the app and open the web interface (`http://<home-assistant>:5080/web/`).

## Configuration

| Option | Description |
|---|---|
| `root_email` | Email of the administrator. Required. |
| `root_password` | Password of the administrator. Required. |
| `retention_days` | Data older than this is deleted (3–3650 days, default 30). |
| `log_level` | Log level of OpenObserve (`error`, `warn`, `info`, `debug`, `trace`). |
| `telemetry` | Send anonymous usage data to the OpenObserve developers (default off). |
| `web_url` | Optional. URL under which the web interface is reached, used for links in alerts. |
| `env_vars` | Optional. Further OpenObserve settings as `ZO_*` environment variables, see the [list of variables](https://openobserve.ai/docs/administration/configuration/environment-variables/). |

**Note:** `root_email` and `root_password` only take effect on the first start, when the administrator is created. Changing them later does not change the existing account. Change the password in the web interface instead.

Example for `env_vars`:

```yaml
- name: ZO_INGEST_ALLOWED_UPTO
  value: "24"
```

## Sending data (OTLP)

| Protocol | Endpoint |
|---|---|
| OTLP/HTTP | `http://<home-assistant>:5080/api/default` (the exporter appends `/v1/traces`, `/v1/logs`, `/v1/metrics`) |
| OTLP/gRPC | `<home-assistant>:5081` |

`default` is the organization. Authentication uses HTTP Basic with email and password (or the ingestion token shown in the web interface under **Data Sources**):

```
Authorization: Basic <base64 of email:password>
```

For gRPC also send the header `organization: default`.

Example with the standard OpenTelemetry environment variables:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://homeassistant.local:5080/api/default
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_HEADERS=Authorization=Basic%20<base64>
```

## Backups

The app uses cold backups: Home Assistant stops OpenObserve during a backup so the database and write-ahead log are consistent. Large amounts of data make backups bigger; lower `retention_days` if needed.

## Resources

OpenObserve uses up to half of the available memory for in-memory tables by default. On small devices limit this with `env_vars`, e.g. `ZO_MEM_TABLE_MAX_SIZE` (see the list of variables for the unit) or enable `ZO_MEMORY_CIRCUIT_BREAKER_ENABLED`.

## Ports

| Port | Use |
|---|---|
| 5080/tcp | Web interface, HTTP API and OTLP/HTTP |
| 5081/tcp | OTLP/gRPC |
