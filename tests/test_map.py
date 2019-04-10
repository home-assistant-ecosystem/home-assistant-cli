"""Tests file for hass-cli map."""
from typing import no_type_check
from unittest.mock import patch

from click.testing import CliRunner
import pytest
import requests_mock

import homeassistant_cli.cli as cli


@no_type_check
@pytest.mark.parametrize(
    "service,url",
    [
        ("openstreetmap", "https://www.openstreetmap.org"),
        ("bing", "https://www.bing.com"),
        ("google", "https://www.google.com"),
    ],
)
def test_map_services(service, url, default_entities) -> None:
    """Test map feature."""
    entity_id = 'zone.school'
    school = next(
        (x for x in default_entities if x['entity_id'] == entity_id), "ERROR!"
    )

    print(school)
    with requests_mock.Mocker() as mock, patch(
        'webbrowser.open_new_tab'
    ) as mocked_browser:
        mock.get(
            "http://localhost:8123/api/states/{}".format(entity_id),
            json=school,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "map", "--service", service, "zone.school"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0

        callurl = mocked_browser.call_args[0][0]

        assert callurl.startswith(url)
        assert str(school.get('attributes').get('latitude')) in callurl
        assert (
            str(school.get('attributes').get('longitude')) in callurl
        )  # typing: ignore
