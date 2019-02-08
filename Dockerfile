FROM python:3.7-alpine
LABEL maintainer="Max Rydahl Andersen <max@xam.dk>"

WORKDIR /usr/src/app

COPY . .

# install build dependencies
RUN apk add --no-cache --virtual build-dependencies gcc musl-dev

# install home-assistant-cli
RUN pip3 install --no-cache-dir --editable .

# remove build dependencies
RUN apk del build-dependencies

ENTRYPOINT ["hass-cli"]
