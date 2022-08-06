FROM python:3.9.7-slim-buster as sdist

# Get and set up Node for front-end asset building
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Needed for fetching stuff
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists/*

ARG SOURCE_COMMIT
ENV DOLPHIN_BUILD=${SOURCE_COMMIT:-unknown}
LABEL org.opencontainers.image.revision=$SOURCE_COMMIT

ARG DOLPHIN_LIGHT_BUILD
ENV DOLPHIN_LIGHT_BUILD=${DOLPHIN_LIGHT_BUILD}

RUN echo "DOLPHIN_LIGHT_BUILD=${DOLPHIN_LIGHT_BUILD}"

COPY . /usr/src/dolphin/
RUN export YARN_CACHE_FOLDER="$(mktemp -d)" \
    && cd /usr/src/dolphin \
    && python setup.py bdist_wheel \
    && rm -r "$YARN_CACHE_FOLDER" \
    && mv /usr/src/dolphin/dist /dist

# This is the image to be run
FROM python:3.9.7-slim-buster

# add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r dispatch && useradd -r -m -g dolphin dolphin

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Dispatch config params
    DOLPHIN_CONF=/etc/dolphin

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Needed for fetching stuff
    ca-certificates \
    wget gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=sdist /dist/*.whl /tmp/dist/
RUN set -x \
    && buildDeps="" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    # remove internal index when internal plugins are seperated
    && pip install -U /tmp/dist/*.whl \
    && apt-get purge -y --auto-remove $buildDeps \
    # We install run-time dependencies strictly after
    # build dependencies to prevent accidental collusion.
    # These are also installed last as they are needed
    # during container run and can have the same deps w/
    && apt-get install -y --no-install-recommends \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
VOLUME /var/lib/dolphin/files

ENTRYPOINT ["dolphin"]
CMD ["server", "start", "dolphin.main:app", "--host=0.0.0.0"]

ARG SOURCE_COMMIT
LABEL org.opencontainers.image.revision=$SOURCE_COMMIT
LABEL org.opencontainers.image.licenses="https://github.com/hale-terminal/dolphin/blob/${SOURCE_COMMIT:-master}/LICENSE"
