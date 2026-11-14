# syntax=docker/dockerfile:1
ARG BUILD_FROM=ghcr.io/home-assistant/base-debian:trixie
ARG OPENOBSERVE_VERSION=v1.2.0-rc2

# Official multi-arch image (distroless, no shell). Only the binary is taken from it.
FROM public.ecr.aws/zinclabs/openobserve:${OPENOBSERVE_VERSION} AS openobserve

FROM ${BUILD_FROM}

ARG BUILD_ARCH
ARG BUILD_VERSION
ARG OPENOBSERVE_VERSION

COPY --from=openobserve /openobserve /usr/local/bin/openobserve

# Fail the build if a shared library of the binary is missing in the base image
RUN if ldd /usr/local/bin/openobserve | grep -q "not found"; then \
        ldd /usr/local/bin/openobserve; \
        exit 1; \
    fi

COPY rootfs /
RUN chmod a+x \
        /etc/s6-overlay/s6-rc.d/openobserve/run \
        /etc/s6-overlay/s6-rc.d/openobserve/finish

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -fsS http://127.0.0.1:5080/healthz > /dev/null || exit 1

LABEL \
    io.hass.name="OpenObserve" \
    io.hass.description="Observability backend for logs, metrics and traces via OpenTelemetry (OTLP)" \
    io.hass.type="app" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.source="https://github.com/Sm0by/ha-addon-openobserve" \
    org.opencontainers.image.version="${BUILD_VERSION}" \
    org.openobserve.version="${OPENOBSERVE_VERSION}"
