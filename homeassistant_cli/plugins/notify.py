"""Notify plugin for Home Assistant CLI (hass-cli)."""
import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import get_services, timestamp

@click.command('list')
@click.option('--service', '-s',
              help='The service to send the notification.')
@click.option('--persist', is_flag=True)
@click.option('--title', '-t',
              type=click.STRING,
              help='The title of the notification.')
@click.option('--message', '-m',
              type=click.STRING,
              help='The message of the notification.')
@click.option('--notification_id', '-n',
              type=click.STRING,
              help='Target ID of the notification.')
@pass_context
def cli(ctx, service, persist, title, message, notification_id):
    """Send a notification with a given service."""
    import homeassistant.remote as remote

    domain = 'notify'
    data = {"title": title,
            "message": message}

    if service and not persist:
        if service in get_services(ctx.api, domain):
            remote.call_service(ctx.api, domain, service, data)
            ctx.vlog('Notification sent with %s at %s', service, timestamp())
            ctx.vlog('Title %s, Message: %s', title, message)
        else:
            ctx.log('Service %s is not available', service)

    if persist and not service:
        if notification_id:
            data['notification_id'] = notification_id
        if 'create' in get_services(ctx.api, 'persistent_notification'):
            remote.call_service(ctx.api, 'persistent_notification',
                                'create', data)
            ctx.vlog('Persistent Notification created on %s at %s', ctx.host,
                     timestamp())
            ctx.vlog('Title %s, Message: %s', title, message)
        else:
            ctx.log('Service %s is not available', 'persistent_notification')
