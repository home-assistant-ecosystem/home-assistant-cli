"""Helpers used by Home Assistant CLI (hass-cli)."""
import json
from datetime import datetime

from homeassistant_cli.const import TIMEOUT, DEFAULT_PORT

def get_services(api, domain):
    """Get a list of available services."""
    import homeassistant.remote as remote

    services = remote.get_services(api)
    for service in services:
        if service['domain'] != domain:
            continue
        return list(service['services'])

def json_output(input):
    """Format JSON output."""
    try:
        return json.dumps(input, indent=2, sort_keys=True)
    except ValueError:
        return input

def timestamp():
    """Return a timestamp."""
    return datetime.now().isoformat()

def req(method, host, password, endpoint, *args):
    """Use REST API to get details.

    This is a hack till a feature is available in the HA Python API.
    """
    import requests
    url = 'http://{}:{}/api/{}'.format(host, DEFAULT_PORT, endpoint)
    headers = {'x-ha-access': '{}'.format(password),
               'content-type': 'application/json'}

    if method == 'get':
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        return response.json()

    elif method == 'post':
        payload = json.loads(*args)
        response = requests.post(url, headers=headers, data=payload,
                                 timeout=TIMEOUT)
        return response.json()