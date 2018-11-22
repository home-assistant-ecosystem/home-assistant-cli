"""Location plugin for Home Assistant CLI (hass-cli)."""
import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
import homeassistant_cli.const as const
from homeassistant_cli.helper import (
    debug_requests_on, format_output, req, req_raw)


@click.group('get')
@pass_context
def cli(ctx):
    """list info from Home Assistant"""


@cli.command()
@click.argument('entity', required=False,
                autocompletion=autocompletion.entities)
@pass_context
def state(ctx, entity):
    """Get/read state from Home Assistant."""
    if not entity:
        response = req_raw(ctx, 'get', 'states')
        response.raise_for_status
        click.echo(format_output(ctx, r.json()))
    else:
        click.echo(format_output(ctx, req(
            ctx, 'get', 'states/{}'.format(entity))))


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


@cli.command()
@click.argument('entities', nargs=-1) ## do time from/to as human delta dates
@pass_context
def history(ctx, entities):
    """List history from Home Assistant."""
    if not entities:
        click.echo(format_output(ctx, req(ctx, 'get', 'history/period')))
    else:
        for entity in entities:
            click.echo(format_output(
                ctx, req(ctx, 'get',
                         'history/period?filter_entity_id={}'.format(entity))))


@cli.command()
@pass_context
def error(ctx):
    """Get errors from Home Assistant."""
    click.echo(req_raw(ctx, 'get', 'error_log').text)
