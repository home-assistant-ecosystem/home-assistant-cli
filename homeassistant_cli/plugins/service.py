"""Service plugin for Home Assistant CLI (hass-cli)."""
import logging
import re as reg
import sys
from typing import Any, Dict, List, Pattern  # noqa: F401

import click

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api
from homeassistant_cli.helper import argument_callback

_LOGGING = logging.getLogger(__name__)


@click.group('service')
@pass_context
def cli(ctx):
    """Call and work with services."""


@cli.command('list')
@click.argument('servicefilter', default=".*", required=False)
@pass_context
def list_cmd(ctx: Configuration, servicefilter):
    """Get list of services."""
    ctx.auto_output('table')
    services = api.get_services(ctx)
    service_filter = servicefilter

    result = []  # type: List[Dict[Any,Any]]
    if service_filter == ".*":
        result = services
    else:
        result = services
        service_filter_re = reg.compile(service_filter)  # type: Pattern

        domains = []
        for domain in services:
            domain_name = domain['domain']
            domain_data = {}
            services_dict = domain['services']
            service_data = {}
            for service in services_dict:
                if service_filter_re.search(
                    "{}.{}".format(domain_name, service)
                ):
                    service_data[service] = services_dict[service]

            if service_data:
                domain_data["services"] = service_data
                domain_data["domain"] = domain_name
                domains.append(domain_data)
        result = domains

    flatten_result = []  # type: List[Dict[str,Any]]
    for domain in result:
        for service in domain['services']:
            item = {}
            item['domain'] = domain['domain']
            item['service'] = service
            item = {**item, **domain['services'][service]}
            flatten_result.append(item)

    cols = [
        ('DOMAIN', 'domain'),
        ('SERVICE', 'service'),
        ('DESCRIPTION', 'description'),
    ]
    ctx.echo(
        format_output(
            ctx, flatten_result, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('call')
@click.argument(
    'service',
    required=True,
    shell_complete=autocompletion.services,  # type: ignore
)
@click.option(
    '--arguments', help="""Comma separated key/value pairs to use as arguments.
if string is -, the data is read from stdin, and if it starts with the letter @
the rest should be a filename from which the data is read""",
    callback=argument_callback,
    expose_value=False
)
@click.option(
    '--json', help="""Json string to use as arguments.
if string is -, the data is read from stdin, and if it starts with the letter @
the rest should be a filename from which the data is read""",
    callback=argument_callback,
    expose_value=False
)
@click.option(
    '--yaml', help="""Yaml string to use as arguments.
if string is -, the data is read from stdin, and if it starts with the letter @
the rest should be a filename from which the data is read""",
    callback=argument_callback,
    expose_value=False
)
@pass_context
def call(ctx: Configuration, service, data=None):
    """Call a service."""
    ctx.auto_output('data')
    _LOGGING.debug("service call <start>")
    parts = service.split(".")
    if len(parts) != 2:
        _LOGGING.error("Service name not following <domain>.<service> format")
        sys.exit(1)

    _LOGGING.debug("calling %s.%s(%s)", parts[0], parts[1], data)

    result = api.call_service(ctx, parts[0], parts[1], data)

    _LOGGING.debug("Formatting output")
    ctx.echo(format_output(ctx, result))
