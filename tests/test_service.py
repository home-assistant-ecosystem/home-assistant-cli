"""Tests file for Home Assistant CLI (hass-cli)."""
import json

from click.testing import CliRunner
import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli
from homeassistant_cli.config import Configuration
import requests_mock

VALID_INFO = """[
    {
        "domain": "homeassistant",
        "services": {
            "check_config": {
                "description": "Check the Home Assistant configuration files\
                 for errors. Errors will be displayed in the\
                  Home Assistant log.",
                "fields": {}
            },
            "reload_core_config": {
                "description": "Reload the core configuration.",
                "fields": {}
            },
            "restart": {
                "description": "Restart the Home Assistant service.",
                "fields": {}
            },
            "stop": {
                "description": "Stop the Home Assistant service.",
                "fields": {}
            },
            "toggle": {
                "description": "Generic service to toggle devices on/off under\
                 any domain. Same usage as the light.turn_on, switch.turn_on,\
                  etc. services.",
                "fields": {
                    "entity_id": {
                        "description": "The entity_id of the device to toggle\
                         on/off.",
                        "example": "light.living_room"
                    }
                }
            },
            "turn_off": {
                "description": "Generic service to turn devices off under\
                 any domain.\
                 Same usage as the light.turn_on, switch.turn_on, etc.\
                 services.",
                "fields": {
                    "entity_id": {
                        "description": "The entity_id of the device\
                         to turn off.",
                        "example": "light.living_room"
                    }
                }
            },
            "turn_on": {
                "description": "Generic service to turn devices on under\
                 any domain.\
                 Same usage as the light.turn_on, switch.turn_on, etc.\
                  services.",
                "fields": {
                    "entity_id": {
                        "description": "The entity_id of the device to\
                         turn on.",
                        "example": "light.living_room"
                    }
                }
            },
            "update_entity": {
                "description": "Force one or more entities to update its data",
                "fields": {
                    "entity_id": {
                        "description": "One or multiple entity_ids to update.\
                         Can be a list.",
                        "example": "light.living_room"
                    }
                }
            }
        }
    }
]"""


def test_service_list() -> None:
    """Test services can be listed."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/services",
            text=VALID_INFO,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["service", "list"], catch_exceptions=False
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]['domain'] == 'homeassistant'


def test_service_completion() -> None:
    """Test completion for services."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/services',
            text=VALID_INFO,
            status_code=200,
        )

        cfg = Configuration()

        result = autocompletion.services(cfg, "service call", "turn")
        assert len(result) == 2

        resultdict = dict(result)

        assert "homeassistant.turn_on" in resultdict
