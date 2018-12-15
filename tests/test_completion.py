"""Tests file for Home Assistant CLI (hass-cli)."""
import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli
import requests_mock


def test_entity_completion(basic_entities_text) -> None:
    """Test completion for entities."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/states',
            text=basic_entities_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['entity', 'get'])

        result = autocompletion.entities(cfg, "entity get", "")
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

        cfg = cli.cli.make_context('hass-cli', ['service', 'get'])

        result = autocompletion.services(cfg, "service get", "")
        assert len(result) == 121

        resultdict = dict(result)

        assert "automation.reload" in resultdict
        assert (
            resultdict["automation.reload"]
            == "Reload the automation configuration."
        )


def test_event_completion(default_events_text) -> None:
    """Test completion for events."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/events',
            text=default_events_text,
            status_code=200,
        )

        cfg = cli.cli.make_context('hass-cli', ['service', 'get'])

        result = autocompletion.events(cfg, "events get", "")
        assert len(result) == 11

        resultdict = dict(result)

        assert "component_loaded" in resultdict
        assert resultdict["component_loaded"] == ""
