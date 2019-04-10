"""Testing Area operations."""

import json
import unittest.mock as mock

from click.testing import CliRunner

import homeassistant_cli.cli as cli


def test_area_list(default_areas) -> None:
    """Test Area List."""
    with mock.patch(
        'homeassistant_cli.remote.get_areas', return_value=default_areas
    ):

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["--output=json", "area", "list"], catch_exceptions=False
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert len(data) == 3


def test_area_list_filter(default_areas) -> None:
    """Test Area List."""
    with mock.patch(
        'homeassistant_cli.remote.get_areas', return_value=default_areas
    ):

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "area", "list", "Bed.*"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]['name'] == "Bedroom"
