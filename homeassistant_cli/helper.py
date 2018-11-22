"""Helpers used by Home Assistant CLI (hass-cli)."""
import contextlib
from http.client import HTTPConnection
import json
import logging

import click
import requests
import tabulate
from tabulate import tabulate
import yaml


def raw_format_output(output, data):
    """Format the raw output."""
    if output == "json":
        try:
            return json.dumps(data, indent=2, sort_keys=False)
        except ValueError:
            return input
    elif output == "yaml":
        try:
            return yaml.safe_dump(data, default_flow_style=False)
        except ValueError:
            return input
    # todo fix this so gets a jsonpath list to transpose data
    elif output == "human":
        return table(data)
    else:
        raise ValueError(
            "Output Format was {}, expected either 'json' or 'yaml'".format(
                output))


def format_output(ctx, data):
    """Format JSON to defined output."""
    return raw_format_output(ctx.output, data)


def req_raw(ctx, method, endpoint, *args):
    """Use REST API to get details."""
    url = '{}/api/{}'.format(ctx.server, endpoint)
    headers = {
        'Authorization': 'Bearer {}'.format(ctx.token),
        'content-type': 'application/json',
    }

    if method == 'get':
        response = requests.get(url, headers=headers, timeout=ctx.timeout)
        return response

    elif method == 'post':
        if args and args[0]:
            payload = json.loads(*args)
            response = requests.post(
                url, headers=headers, json=payload, timeout=ctx.timeout)
        else:
            response = requests.post(
                url, headers=headers, timeout=ctx.timeout)

        return response
    elif method == 'delete':
        response = requests.delete(url, headers=headers, timeout=ctx.timeout)
        return response
    else:
        raise ValueError("Unsupported method " + method)


def req(ctx, method, endpoint, *args):
    """Create a request."""
    resp = req_raw(ctx, method, endpoint, *args)

    resp.raise_for_status()

    if resp:
        return resp.json()
    else:
        click.echo("Got empty response from server")


def debug_requests_on():
    """Switch on logging of the requests module."""
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def debug_requests_off():
    """Switch off logging of the requests module, might be some side-effects."""
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False


@contextlib.contextmanager
def debug_requests():
    """Use with 'with'!"""
    debug_requests_on()
    yield
    debug_requests_off()


def table(elements):
    """Create a table-like output."""
    click.echo(tabulate(elements))
