"""Tests file for Home Assistant CLI (hass-cli)."""
import json
import re

from click.testing import CliRunner
import homeassistant_cli.cli as cli
import requests_mock

VALID_INFO = """[{
    "attributes": {
      "auto": true,
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
    "state": "on"
  },
  {
    "attributes": {
      "event_data": 1002,
      "event_received": "2018-12-05 13:17:51.905847"
    },
    "context": {
      "id": "b0e24511a0fd4eb69ab5afeac0082993",
      "user_id": "2b0f58a02c35408c86e9e34f1d6e141d"
    },
    "entity_id": "sensor.deconz_event",
    "last_changed": "2018-12-05T12:17:52.434229+00:00",
    "last_updated": "2018-12-05T12:17:52.434229+00:00",
    "state": "small_bathroom_switch"
  },
  {
    "attributes": {
      "message": "Login attempt or request",
      "title": "Login attempt failed"
    },
    "context": {
      "id": "61869ff42b61450980a5a394ee7b71bf",
      "user_id": null
    },
    "entity_id": "persistent_notification.httplogin",
    "last_changed": "2018-12-01T18:26:19.453513+00:00",
    "last_updated": "2018-12-01T18:26:19.453513+00:00",
    "state": "notifying"
  }
]
"""

SINGLE_ENTITY = """
{
  "attributes": {
    "auto": true,
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
  "state": "on"
}
"""

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


def test_entity_list():
    """Test entities can be listed."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/states",
            text=VALID_INFO,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["entity", "list"], catch_exceptions=False
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert json.loads(VALID_INFO) == data
        assert len(data) == 3


def test_entity_get() -> None:
    """Test basic get of entity."""
    with requests_mock.Mocker() as mock:
        mock.get(
            re.compile("http://localhost:8123/api/states"),
            text=SINGLE_ENTITY,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["entity", "get", "group.all_remotes"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert data["entity_id"] == "group.all_remotes"


def test_entity_edit():
    """Test basic edit of state."""
    with requests_mock.Mocker() as mock:
        get = mock.get(
            re.compile("http://localhost:8123/api/states"),
            text=SINGLE_ENTITY,
            status_code=200,
        )
        post = mock.post(
            re.compile("http://localhost:8123/api/states"),
            text=EDITED_ENTITY,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["entity", "edit", "group.all_remotes", "myspecialstate"],
            catch_exceptions=False,
        )

        assert result.exit_code == 0

        assert get.call_count == 1
        assert post.call_count == 1
        assert post.request_history[0].json()['state'] == 'myspecialstate'
