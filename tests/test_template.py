"""Tests file for hass-cli template."""

from click.testing import CliRunner
import homeassistant_cli.cli as cli
import pytest


def test_basic_template(basic_entities_text) -> None:
    """Test entities can be listed."""
    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        ["template", "--local", "tests/fixtures/basic_local_template.ji2"],
        catch_exceptions=False,
    )

    assert result.output == "Testing basic template 42\n"


def test_data() -> None:
    """Test entities can be listed."""
    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        [
            "template",
            "--local",
            "tests/fixtures/var_template.ji2",
            "tests/fixtures/var_data.yaml",
        ],
        catch_exceptions=False,
    )

    assert result.output == "Resolve avalue\n"


@pytest.mark.slow
def test_server_template(starthomeassistant, basic_entities_text) -> None:
    """Test entities can be listed."""
    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        [
            "--password",
            "hasscli",
            "template",
            "tests/fixtures/basic_template.ji2",
        ],
        catch_exceptions=False,
    )

    assert result.output == "Testing basic template Sun.\n"
