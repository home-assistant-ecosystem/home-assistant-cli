"""Location plugin for Home Assistant CLI (hass-cli)."""
import logging

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output, req, req_raw

_LOGGING = logging.getLogger(__name__)


@click.group('get', hidden=True)
@pass_context
def cli(ctx):
    """List info from Home Assistant."""


@cli.command()
@click.argument(  # type: ignore
    'entity', required=False, autocompletion=autocompletion.entities
)
@pass_context
def state(ctx: Configuration, entity):
    """Get/read state from Home Assistant."""
    _LOGGING.warning("`get` is deprecated, use `entity`, `service` or `event`")

    if not entity:
        response = req_raw(ctx, 'get', 'states')
        response.raise_for_status()
        click.echo(format_output(ctx, response.json()))
    else:
        click.echo(
            format_output(ctx, req(ctx, 'get', 'states/{}'.format(entity)))
        )


@cli.command()
@pass_context
def event(ctx):
    """List events from Home Assistant."""
    click.echo(format_output(ctx, req(ctx, 'get', 'events')))


@cli.command()
@pass_context
def service(ctx):
    """List services from Home Assistant."""
    click.echo(format_output(ctx, req(ctx, 'get', 'services')))


# todo: time from/to as human delta dates


@cli.command()
@click.argument('entities', nargs=-1)
@pass_context
def history(ctx: Configuration, entities):
    """List history from Home Assistant."""
    if not entities:
        click.echo(format_output(ctx, req(ctx, 'get', 'history/period')))
    else:
        for entity in entities:
            click.echo(
                format_output(
                    ctx,
                    req(
                        ctx,
                        'get',
                        'history/period?filter_entity_id={}'.format(entity),
                    ),
                )
            )


@cli.command()
@pass_context
def error(ctx):
    """Get errors from Home Assistant."""
    click.echo(req_raw(ctx, 'get', 'error_log').text)
