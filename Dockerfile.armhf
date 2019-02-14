#python 3.6 with Alpine 3.8
FROM balenalib/armv7hf-alpine-python:3.6-3.8
LABEL maintainer="Max Rydahl Andersen <max@xam.dk>"

RUN [ "cross-build-start" ]

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev\
    &&  rm -rf /var/cache/apk/*

WORKDIR /usr/src/app
COPY . .
RUN pip3 install --upgrade pip; pip3 install --no-cache-dir -e .

RUN [ "cross-build-end" ]

ENTRYPOINT ["hass-cli"]
