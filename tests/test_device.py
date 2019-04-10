"""Testing Device operations."""

import json
import unittest.mock as mock

from click.testing import CliRunner

import homeassistant_cli.cli as cli


def test_device_list(default_devices) -> None:
    """Test Device List."""
    with mock.patch(
        'homeassistant_cli.remote.get_devices', return_value=default_devices
    ):

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "device", "list"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert len(data) == 23


def test_device_list_filter(default_devices) -> None:
    """Test Device List."""
    with mock.patch(
        'homeassistant_cli.remote.get_devices', return_value=default_devices
    ):

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "device", "list", "table"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert len(data) == 2
        assert data[0]['name'] == "Kitchen table left"
        assert data[1]['name'] == "Kitchen table right"


def test_device_assign(default_areas, default_devices) -> None:
    """Test basic device assign."""
    with mock.patch(
        'homeassistant_cli.remote.get_devices', return_value=default_devices
    ):
        with mock.patch(
            'homeassistant_cli.remote.get_areas', return_value=default_areas
        ):
            with mock.patch(
                'homeassistant_cli.remote.assign_area',
                return_value={'success': True},
            ):

                runner = CliRunner()
                result = runner.invoke(
                    cli.cli,
                    ["device", "assign", "Kitchen", "Kitchen table left"],
                    catch_exceptions=False,
                )
                print(result.output)
                assert result.exit_code == 0
                expected = (
                    "Successfully assigned 'Kitchen'"
                    " to 'Kitchen table left'\n"
                )
                assert result.output == expected
