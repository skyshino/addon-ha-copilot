ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.2.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

# 递归设置s6-overlay目录权限
RUN chmod -R +x /etc/s6-overlay

# Setup base
RUN apk add --no-cache \
    coreutils \
    build-base \
    wget=1.24.5-r0 \
    python3-dev \
    py3-pip \
    gcc \
    musl \
    linux-headers \
    nginx && \
    pip install -i https://pypi.doubanio.com/simple/ uwsgi Flask qianfan websockets pyyaml
    
# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="skyshino <skyshino@gmail.com>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="skyshino" \
    org.opencontainers.image.authors="skyshino <skyshino@gmail.com>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.documentation="https://github.com/skyshino/ha_copilot/blob/main/ha-copilot/DOCS.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
