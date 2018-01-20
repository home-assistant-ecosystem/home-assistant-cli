"""Service plugin for Home Assistant CLI (hass-cli)."""
import click
import ast

from homeassistant_cli.cli import pass_context

def print_service(ctx, serv):
    ctx.log("Domain '%s'", serv['domain'])
    for service, data in serv['services'].items():
        ctx.log("  * %s: %s", service, data.get("description", "desc missing"))
        for field, field_data in data["fields"].items():
            ctx.vlog("    - %s (%s)", field, field_data.get("description", "desc missing"))
            ctx.vlog("      Example: %s", field_data.get("example", "example missing"))

    ctx.log("")

@click.command('service')
@click.argument('domain', required=False)
@click.argument('service', required=False)
@click.argument('data', required=False)
@pass_context
def cli(ctx, domain, service, data):
    """Query and call services."""
    import homeassistant.remote as remote

    # If no service is given, we want to either print all services
    # from the given domain, or everything if no domain is given
    if service is None and data is None:
        for serv in remote.get_services(ctx.api):
            if domain is not None and domain != serv['domain']:
                continue

            print_service(ctx, serv)
        return

    if data is not None:
        data = ast.literal_eval(data)

    ctx.log("Calling %s.%s with data %s", domain, service, data)
    res = remote.call_service(ctx.api, domain, service, data)
    ctx.log("Return value: %s", res)
