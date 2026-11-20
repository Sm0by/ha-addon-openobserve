# OpenObserve

[OpenObserve](https://github.com/openobserve/openobserve) stores and searches logs, metrics and traces. Applications send data via OpenTelemetry (OTLP) over HTTP or gRPC.

The app runs OpenObserve in single-node mode. All data is stored in the app's own storage (`/data/openobserve`).

## Installation

1. Add the repository `https://github.com/Sm0by/ha-addon-openobserve` under **Settings → Apps → App Store → ⋮ → Repositories**.
2. Install **OpenObserve**.
3. Set `root_email` and `root_password` on the **Configuration** tab.
4. Start the app and open the web interface (`http://<home-assistant>:5080/web/`).
5. Optional: turn on **Watchdog** on the **Info** tab. Home Assistant then restarts the app when its health check (`/healthz`) fails.

## Configuration

| Option | Description |
|---|---|
| `root_email` | Email of the administrator. Required. |
| `root_password` | Password of the administrator. Required. 8–128 characters with at least one lowercase letter, one uppercase letter, one digit and one special character, otherwise OpenObserve does not start. |
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

### Alerts to devices in your network

OpenObserve blocks alert destinations, webhooks and other outgoing requests to private network addresses (protection against server-side request forgery). To send alerts to a device in your network, for example a webhook of Home Assistant, allow its address:

```yaml
- name: ZO_SSRF_ALLOWED_CIDRS
  value: "192.168.1.10/32"
```

Several addresses or networks are separated by commas. `ZO_SSRF_ALLOWED_HOSTS` does the same for host names. Restart the app after changing them.

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

The OpenTelemetry specification encodes the space as `%20`, but some exporters do not decode it. If you get `401 Unauthorized`, write a plain space instead.

### Logs and events of Home Assistant

The [Remote Logger](https://remote-logger.rhizomatics.org.uk) integration (HACS) sends the logs and selected events of Home Assistant via OTLP. Use the OTLP/HTTP endpoint and the authorization header from above.

## Backups

The app uses cold backups: Home Assistant stops OpenObserve during a backup so the database and write-ahead log are consistent. Large amounts of data make backups bigger; lower `retention_days` if needed.

## Resources

OpenObserve uses up to half of the available memory for in-memory tables by default. On small devices limit this with `env_vars`, e.g. `ZO_MEM_TABLE_MAX_SIZE` (see the list of variables for the unit) or enable `ZO_MEMORY_CIRCUIT_BREAKER_ENABLED`.

## Ports

| Port | Use |
|---|---|
| 5080/tcp | Web interface, HTTP API and OTLP/HTTP |
| 5081/tcp | OTLP/gRPC |

## License

The app contains the unmodified official OpenObserve binary, licensed under the [GNU Affero General Public License v3.0](https://github.com/openobserve/openobserve/blob/main/LICENSE). The license text and the link to the source code of the included version are in the app under `/usr/share/doc/openobserve/`. The files of the app itself are under the MIT License.

This app is a community project and not affiliated with OpenObserve Inc. or the Home Assistant project.
