FROM python:3.11-alpine
LABEL maintainer="Fabian Affolter <fabian@affolter-engineering.ch>"

WORKDIR /usr/src/app

COPY . .

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev\
    &&  rm -rf /var/cache/apk/*

RUN pip3 install --upgrade pip; pip3 install --no-cache-dir -e .

ENTRYPOINT ["hass-cli"]
