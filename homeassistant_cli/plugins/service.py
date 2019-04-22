"""Service plugin for Home Assistant CLI (hass-cli)."""
import logging
import re as reg
import sys
from typing import Any, Dict, List, Pattern  # noqa: F401

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

    result = []  # type: List[Dict[Any,Any]]
    if servicefilter == ".*":
        result = services
    else:
        result = services
        servicefilterre = reg.compile(servicefilter)  # type: Pattern

        domains = []
        for domain in services:
            domain_name = domain['domain']
            domaindata = {}
            servicesdict = domain['services']
            servicedata = {}
            for service in servicesdict:
                if servicefilterre.search(
                    "{}.{}".format(domain_name, service)
                ):
                    servicedata[service] = servicesdict[service]

            if servicedata:
                domaindata["services"] = servicedata
                domaindata["domain"] = domain_name
                domains.append(domaindata)
        result = domains

    flattenresult = []  # type: List[Dict[str,Any]]
    for domain in result:
        for service in domain['services']:
            item = {}
            item['domain'] = domain['domain']
            item['service'] = service
            item = {**item, **domain['services'][service]}
            flattenresult.append(item)

    cols = [
        ('DOMAIN', 'domain'),
        ('SERVICE', 'service'),
        ('DESCRIPTION', 'description'),
    ]
    ctx.echo(
        format_output(
            ctx, flattenresult, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('call')
@click.argument(  # type: ignore
    'service', required=True, autocompletion=autocompletion.services
)
@click.option(
    '--arguments', help="Comma separated key/value pairs to use as arguments."
)
@pass_context
def call(ctx: Configuration, service, arguments):
    """Call a service."""
    ctx.auto_output('data')
    _LOGGING.debug("service call <start>")
    parts = service.split(".")
    if len(parts) != 2:
        _LOGGING.error("Service name not following <domain>.<service> format")
        sys.exit(1)

    _LOGGING.debug("Convert arguments %s to dict", arguments)
    data = to_attributes(arguments)

    _LOGGING.debug("service call_service")

    result = api.call_service(ctx, parts[0], parts[1], data)

    _LOGGING.debug("Formatting output")
    ctx.echo(format_output(ctx, result))
