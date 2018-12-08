"""Helpers used by Home Assistant CLI (hass-cli)."""
import contextlib
from http.client import HTTPConnection
import json
import logging
from typing import Any, Dict, Generator, cast

import click
from homeassistant_cli.config import Configuration
import requests
from requests.models import Response
import yaml


def raw_format_output(output: str, data: Dict[str, Any]) -> str:
    """Format the raw output."""
    if output == 'json':
        try:
            return json.dumps(data, indent=2, sort_keys=False)
        except ValueError:
            return str(data)
    elif output == 'yaml':
        try:
            return cast(str, yaml.safe_dump(data, default_flow_style=False))
        except ValueError:
            return str(data)
    # todo fix this so gets a jsonpath list to transpose data
    else:
        raise ValueError(
            "Output Format was {}, expected either 'json' or 'yaml'".format(
                output
            )
        )


def format_output(ctx: Configuration, data: Dict[str, Any]) -> str:
    """Format dict to defined output."""
    return raw_format_output(ctx.output, data)


def req_raw(
    ctx: Configuration, method: str, endpoint: str, *args: Any
) -> Response:
    """Use REST API to get details."""
    url = '{}/api/{}'.format(ctx.server, endpoint)
    headers = {
        'Authorization': 'Bearer {}'.format(ctx.token),
        'content-type': 'application/json',
    }

    if method == 'get':
        response = requests.get(url, headers=headers, timeout=ctx.timeout)
        return response

    if method == 'post':
        if args and args[0]:
            payload = json.loads(  # pylint: disable=no-value-for-parameter
                *args
            )
            response = requests.post(
                url, headers=headers, json=payload, timeout=ctx.timeout
            )
        else:
            response = requests.post(url, headers=headers, timeout=ctx.timeout)

        return response

    if method == 'delete':
        response = requests.delete(url, headers=headers, timeout=ctx.timeout)
        return response

    raise ValueError("Unsupported method " + method)


def req(
    ctx: Configuration, method: str, endpoint: str, *args: Any
) -> Dict[str, Any]:
    """Create a request."""
    resp = req_raw(ctx, method, endpoint, *args)

    if resp:
        resp.raise_for_status()
        return cast(Dict[str, Any], resp.json())

    click.echo("Got empty response from server")

    return {}


def debug_requests_on() -> None:
    """Switch on logging of the requests module."""
    HTTPConnection.set_debuglevel(cast(HTTPConnection, HTTPConnection), 1)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def debug_requests_off() -> None:
    """Switch off logging of the requests module.

    Might have some side-effects.
    """
    HTTPConnection.set_debuglevel(cast(HTTPConnection, HTTPConnection), 1)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False


@contextlib.contextmanager
def debug_requests() -> Generator:
    """Yieldable way to turn on debugs for requests.

    with debug_requests(): <do things>
    """
    debug_requests_on()
    yield
    debug_requests_off()
