"""Tests file for Home Assistant CLI (hass-cli)."""
from typing import cast

import requests_mock

import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli
from homeassistant_cli.config import Configuration


def test_entity_completion(basic_entities_text) -> None:
    """Test completion for entities."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/states',
            text=basic_entities_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['entity', 'get'])
        result = autocompletion.entities(
            cast(cfg, Configuration), ["entity", "get"], ""  # type: ignore
        )
        assert len(result) == 3

        resultdict = {x.value: x.help for x in result}

        assert "sensor.one" in resultdict
        assert resultdict['sensor.one'] == 'friendly long name [on]'


def test_service_completion(default_services_text) -> None:
    """Test completion for services."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/services',
            text=default_services_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['service', 'list'])

        result = autocompletion.services(
            cfg, ["service", "list"], ""  # type: ignore
        )
        assert len(result) == 12

        resultdict = {x.value: x.help for x in result}

        assert "group.remove" in resultdict
        val = resultdict["group.remove"]
        assert val == "Remove a user group."


def test_event_completion(default_events_text) -> None:
    """Test completion for events."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/events',
            text=default_events_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['events', 'list'])

        result = autocompletion.events(
            cfg, ["events", "list"], ""  # type: ignore
        )
        assert len(result) == 11

        resultdict = {x.value: x.help for x in result}

        assert "component_loaded" in resultdict
        assert resultdict["component_loaded"] is None


def test_area_completion(default_areas_text) -> None:
    """Test completion for Area."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/areas',
            text=default_areas_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['area', 'list'])

        result = autocompletion.areas(
            cfg, ["area", "list"], ""  # type: ignore
        )
        assert len(result) == 3

        resultdict = {x.value: x.help for x in result}

        assert "Bedroom" in resultdict
        assert resultdict["Bedroom"] == "3"
