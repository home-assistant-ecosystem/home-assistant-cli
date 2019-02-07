FROM python:3.7-alpine

RUN apk add --no-cache --virtual build-dependencies gcc musl-dev
RUN pip3 install --no-cache-dir homeassistant-cli==0.4.4
RUN apk del build-dependencies