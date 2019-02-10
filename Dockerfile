FROM python:3.6-alpine
LABEL maintainer="Max Rydahl Andersen <max@xam.dk>"

WORKDIR /usr/src/app

COPY . .

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev\
    &&  rm -rf /var/cache/apk/*

RUN pip3 install --upgrade pip; pip3 install --no-cache-dir -e .

ENTRYPOINT ["hass-cli"]
