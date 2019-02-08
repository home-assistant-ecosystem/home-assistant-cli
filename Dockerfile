FROM python:3.7-alpine
LABEL maintainer="Max Rydahl Andersen <max@xam.dk>"

WORKDIR /usr/src/app

COPY . .

# install build dependencies & home-assistant cli
RUN apk add --no-cache --virtual build-dependencies gcc musl-dev \
    && pip3 install --no-cache-dir --editable . \
    && apk del build-dependencies

ENTRYPOINT ["hass-cli"]
