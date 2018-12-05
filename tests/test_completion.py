"""Tests file for Home Assistant CLI (hass-cli)."""
import requests_mock

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.config import Configuration

VALID_INFO = '''[{
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
    "entity_id": "sensor.one",
    "last_changed": "2018-12-05T12:17:52.434229+00:00",
    "last_updated": "2018-12-05T12:17:52.434229+00:00",
    "state": "small_bathroom_switch"
  },
  {
    "attributes": {
      "message": "Login attempt or request with",
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
'''


def test_entity_completion():
    with requests_mock.Mocker() as m:
        m.get('http://localhost:8123/api/states',
              text=VALID_INFO, status_code=200)

        cfg = Configuration()

        result = autocompletion.entities(cfg, "entity get", "")
        assert len(result) == 3

        result = dict(result)

        assert "group.all_remotes" in result
        assert result['group.all_remotes'] == 'all remotes'
