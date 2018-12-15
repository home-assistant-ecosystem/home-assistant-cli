"""Tests file for Home Assistant CLI (hass-cli)."""
import json

from click.testing import CliRunner
import homeassistant_cli.cli as cli
import requests_mock

EDITED_ENTITY = """
{
  "attributes": {
    "auto": false,
    "entity_id": [
      "remote.tv"
    ],
    "friendly_name": "all remotes",
    "hidden": true,
    "order": 16
  },
  "context": {
    "id": "4c511277c55647eb8e7e4acf10fcd617",
    "user_id": null
  },
  "entity_id": "group.all_remotes",
  "last_changed": "2018-12-04T10:13:05.914548+00:00",
  "last_updated": "2018-12-04T10:13:05.914548+00:00",
  "state": "off"
}
"""


def test_entity_list(basic_entities_text) -> None:
    """Test entities can be listed."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/states",
            text=basic_entities_text,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["entity", "list"], catch_exceptions=False
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert json.loads(basic_entities_text) == data
        assert len(data) == 3


def test_entity_get(basic_entities_text, basic_entities) -> None:
    """Test entity get."""
    with requests_mock.Mocker() as mock:
        sensorone = next(
            x for x in basic_entities if x['entity_id'] == 'sensor.one'
        )
        mock.get(
            "http://localhost:8123/api/states/sensor.one",
            json=sensorone,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["entity", "get", "sensor.one"], catch_exceptions=False
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert "entity_id" in data
        assert data["entity_id"] == "sensor.one"


def test_entity_edit(basic_entities_text, basic_entities) -> None:
    """Test basic edit of state."""
    with requests_mock.Mocker() as mock:
        get = mock.get(
            "http://localhost:8123/api/states",
            text=basic_entities_text,
            status_code=200,
        )
        sensorone = next(
            x for x in basic_entities if x['entity_id'] == 'sensor.one'
        )
        get = mock.get(
            "http://localhost:8123/api/states/sensor.one",
            json=sensorone,
            status_code=200,
        )
        post = mock.post(
            "http://localhost:8123/api/states/sensor.one",
            text=EDITED_ENTITY,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["entity", "edit", "sensor.one", "myspecialstate"],
            catch_exceptions=False,
        )

        assert result.exit_code == 0

        assert get.call_count == 1
        assert post.call_count == 1
        assert post.request_history[0].json()['state'] == 'myspecialstate'
