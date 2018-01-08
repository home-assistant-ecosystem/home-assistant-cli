"""Status plugin for Home Assistant CLI (hass-cli)."""
import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import timestamp, req


@click.command('status')
@pass_context
def cli(ctx):
    """Show the status of an instance."""
    import homeassistant.remote as remote
    config = remote.get_config(ctx.api)
    events = event_counter(ctx.api)

    ctx.log('Status of %s - %s - %s', ctx.host, config['location_name'],
            config['version'])

    status = []
    status.append(['Components', len(config['components'])])
    status.append(['Events', events.get('events')])
    status.append(['Listener count', events.get('total')])
    status.append(['Services', services_counter(ctx.api)])
    status.append(['Entities', entities_counter(ctx.api)])

    ctx.table(status)
    ctx.vlog('Details of %s, Created: %s', ctx.host, timestamp())

def event_counter(api):
    """Count all present events."""
    import homeassistant.remote as remote

    count_events = count_listeners = 0
    events = remote.get_event_listeners(api)

    for event in events:
        count_events = count_events + 1
        count_listeners = count_listeners + event['listener_count']

    return {'events': count_events, 'total': count_listeners}

def services_counter(api):
    """Count all available services."""
    import homeassistant.remote as remote

    return len(remote.get_services(api))

def entities_counter(api):
    """Count all entities."""
    import homeassistant.remote as remote

    return len(remote.get_states(api))
