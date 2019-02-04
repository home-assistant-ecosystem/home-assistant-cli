"""Tests file for hass-cli template."""

from click.testing import CliRunner
import homeassistant_cli.cli as cli


def test_basic_local_template(basic_entities_text) -> None:
    """Test entities can be listed."""

    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        ["template", "--local", "tests/fixtures/basic_local_template.ji2"],
        catch_exceptions=False,
    )

    assert result.output == "Testing basic template 42\n"


def test_basic_server_template(
    starthomeassistant, basic_entities_text
) -> None:
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
