"""Template plugin for Home Assistant CLI (hass-cli)."""

import logging
import os

import click
from jinja2 import FileSystemLoader
from jinja2.exceptions import SecurityError
from jinja2.sandbox import ImmutableSandboxedEnvironment

import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.exceptions import HomeAssistantCliError, UnsafeTemplateError

_LOGGING = logging.getLogger(__name__)

# Allowlist of environment variables accessible from templates
SAFE_ENV_VARS = frozenset({
    "HASS_SERVER",
    "LANG",
    "TZ",
})


def _safe_environ_get(key: str, default: str | None = None) -> str | None:
    """Return env var only if it is in the allowlist."""
    if key in SAFE_ENV_VARS:
        return os.environ.get(key, default)
    return default


def render(template_path, data, strict=False) -> str:
    """Render template."""
    env = ImmutableSandboxedEnvironment(
        loader=FileSystemLoader(os.path.dirname(template_path)),
        keep_trailing_newline=True,
    )
    if strict:
        from jinja2 import StrictUndefined

        env.undefined = StrictUndefined

    # Add environ global (allowlisted)
    env.globals["environ"] = _safe_environ_get

    try:
        output = env.get_template(os.path.basename(template_path)).render(data)
    except SecurityError as err:
        raise UnsafeTemplateError(
            f"Template '{os.path.basename(template_path)}' contains unsafe "
            f"operations: {err}"
        ) from None
    return output


@click.command("template")
@click.argument("template", required=True, type=click.File())
@click.argument("datafile", type=click.File(), required=False)
@click.option(
    "--local",
    default=False,
    is_flag=True,
    help="If should render template locally.",
)
@pass_context
def cli(ctx: Configuration, template, datafile, local: bool) -> None:
    """Render templates on server or locally.

    TEMPLATE - jinja2 template file
    DATAFILE - YAML file with variables to pass to rendering
    """
    variables = {}  # type: Dict[str, Any]
    if datafile:
        variables = ctx.yamlload(datafile)

    template_string = template.read()

    _LOGGING.debug("Rendering: %s Variables: %s", template_string, variables)

    try:
        if local:
            output = render(template.name, variables, True)
        else:
            output = api.render_template(ctx, template_string, variables)
    except (UnsafeTemplateError, HomeAssistantCliError) as err:
        raise click.ClickException(str(err)) from None

    ctx.echo(output)
