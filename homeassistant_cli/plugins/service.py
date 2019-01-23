"""Service plugin for Home Assistant CLI (hass-cli)."""
import logging
import re as reg
import sys
from typing import Any, Dict, Pattern  # noqa: F401

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output, to_attributes
import homeassistant_cli.remote as api

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

    result = {}  # type: Dict[str,Any]
    if servicefilter == ".*":
        result = services
    else:
        servicefilterre = reg.compile(servicefilter)  # type: Pattern

        for domain in services:
            domain_name = domain['domain']  # type: ignore
            domaindata = {}
            servicesdict = domain['services']  # type: ignore
            servicedata = {}
            for service in servicesdict:
                if servicefilterre.search(
                    "{}.{}".format(domain_name, service)
                ):
                    servicedata[service] = servicesdict[  # type: ignore
                        service
                    ]

                if servicedata:
                    domaindata["services"] = servicedata
                    result[domain_name] = domaindata

    ctx.echo(format_output(ctx, result))  # type: ignore


@cli.command('call')
@click.argument(  # type: ignore
    'service', required=True, autocompletion=autocompletion.services
)
@click.option(
    '--arguments', help="Comma separated key/value pairs to use as arguments"
)
@pass_context
def call(ctx: Configuration, service, arguments):
    """Call a service."""
    ctx.auto_output('data')
    _LOGGING.debug("service call <start>")
    parts = service.split(".")
    if len(parts) != 2:
        _LOGGING.error("Service name not following <domain>.<service> format.")
        sys.exit(1)

    _LOGGING.debug("Convert arguments %s to dict", arguments)
    data = to_attributes(arguments)

    _LOGGING.debug("service call_service")

    result = api.call_service(ctx, parts[0], parts[1], data)

    _LOGGING.debug("Formatting ouput")
    ctx.echo(format_output(ctx, result))  # type: ignore
