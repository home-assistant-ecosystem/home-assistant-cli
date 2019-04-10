"""Tests file for Home Assistant CLI (hass-cli)."""
import requests_mock

import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli


def test_entity_completion(basic_entities_text) -> None:
    """Test completion for entities."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/states',
            text=basic_entities_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['entity', 'get'])
        result = autocompletion.entities(  # type: ignore
            cfg, ["entity", "get"], ""
        )
        assert len(result) == 3

        resultdict = dict(result)

        assert "sensor.one" in resultdict
        assert resultdict['sensor.one'] == 'friendly long name'


def test_service_completion(default_services_text) -> None:
    """Test completion for services."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/services',
            text=default_services_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['service', 'list'])

        result = autocompletion.services(  # type: ignore
            cfg, ["service", "list"], ""
        )
        assert len(result) == 12

        resultdict = dict(result)

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

        result = autocompletion.events(  # type: ignore
            cfg, ["events", "list"], ""
        )
        assert len(result) == 11

        resultdict = dict(result)

        assert "component_loaded" in resultdict
        assert resultdict["component_loaded"] == ""


def test_area_completion(default_events_text) -> None:
    """Test completion for Area."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/events',
            text=default_events_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['events', 'list'])

        result = autocompletion.events(  # type: ignore
            cfg, ["events", "list"], ""
        )
        assert len(result) == 11

        resultdict = dict(result)

        assert "component_loaded" in resultdict
        assert resultdict["component_loaded"] == ""
