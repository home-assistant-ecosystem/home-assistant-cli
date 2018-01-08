"""List plugin for Home Assistant CLI (hass-cli)."""
import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import json_output, timestamp


@click.command('list')
@click.option('--entry', '-e',
              type=click.Choice(['services', 'events', 'entities']),
              help='The entry to list.')
@pass_context
def cli(ctx, entry):
    """List various entries of an instance."""
    import homeassistant.remote as remote

    ctx.log('Available %s', entry)
    if entry == 'services':
        services = remote.get_services(ctx.api)
        for service in services:
            ctx.log(json_output(service['services']))

    if entry == 'events':
        events = remote.get_event_listeners(ctx.api)
        for event in events:
            ctx.log(event)

    if entry == 'entities':
        entities = remote.get_states(ctx.api)
        for entity in entities:
            ctx.log(entity)

    ctx.vlog('Details of %s, Created: %s', ctx.host, timestamp())
