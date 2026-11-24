# syntax=docker/dockerfile:1
ARG BUILD_FROM=ghcr.io/home-assistant/base-debian:trixie
ARG OPENOBSERVE_VERSION=v1.2.0

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

# AGPL-3.0: the license text of OpenObserve is in rootfs (kept in sync by the
# update workflow), the location of the corresponding source is written here
RUN printf '%s\n' \
        "OpenObserve ${OPENOBSERVE_VERSION}" \
        "" \
        "The binary /usr/local/bin/openobserve is the unmodified official build from" \
        "public.ecr.aws/zinclabs/openobserve:${OPENOBSERVE_VERSION}." \
        "It is licensed under the GNU Affero General Public License v3.0, see LICENSE." \
        "" \
        "Corresponding source code:" \
        "https://github.com/openobserve/openobserve/tree/${OPENOBSERVE_VERSION}" \
        > /usr/share/doc/openobserve/SOURCE

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
    org.opencontainers.image.licenses="MIT AND AGPL-3.0-only" \
    org.openobserve.version="${OPENOBSERVE_VERSION}"
