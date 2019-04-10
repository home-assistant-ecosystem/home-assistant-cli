"""
Basic API to access remote instance of Home Assistant.

If a connection error occurs while communicating with the API a
HomeAssistantCliError will be raised.
"""
import asyncio
import collections
from datetime import datetime
import enum
import json
import logging
from typing import Any, Callable, Dict, List, Optional, cast
import urllib.parse
from urllib.parse import urlencode

import aiohttp
import requests

from homeassistant_cli.config import Configuration, resolve_server
from homeassistant_cli.exceptions import HomeAssistantCliError
import homeassistant_cli.hassconst as hass

_LOGGER = logging.getLogger(__name__)

# Copied from aiohttp.hdrs
CONTENT_TYPE = 'Content-Type'
METH_DELETE = 'DELETE'
METH_GET = 'GET'
METH_POST = 'POST'


class APIStatus(enum.Enum):
    """Representation of an API status."""

    OK = "ok"
    INVALID_PASSWORD = "invalid_password"
    CANNOT_CONNECT = "cannot_connect"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        """Return the state."""
        return self.value  # type: ignore


def restapi(
    ctx: Configuration, method: str, path: str, data: Optional[Dict] = None
) -> requests.Response:
    """Make a call to the Home Assistant REST API."""
    if data is None:
        data_str = None
    else:
        data_str = json.dumps(data, cls=JSONEncoder)

    if not ctx.session:
        ctx.session = requests.Session()
        ctx.session.verify = not ctx.insecure
        if ctx.cert:
            ctx.session.cert = ctx.cert

        _LOGGER.debug(
            "Session: verify(%s), cert(%s)",
            ctx.session.verify,
            ctx.session.cert,
        )

    headers = {CONTENT_TYPE: hass.CONTENT_TYPE_JSON}  # type: Dict[str, Any]

    if ctx.token:
        headers["Authorization"] = "Bearer {}".format(ctx.token)
    if ctx.password:
        headers["x-ha-access"] = ctx.password

    url = urllib.parse.urljoin(resolve_server(ctx) + path, "")

    try:
        if method == METH_GET:
            return requests.get(url, params=data_str, headers=headers)

        return requests.request(method, url, data=data_str, headers=headers)

    except requests.exceptions.ConnectionError:
        raise HomeAssistantCliError("Error connecting to {}".format(url))

    except requests.exceptions.Timeout:
        error = "Timeout when talking to {}".format(url)
        _LOGGER.exception(error)
        raise HomeAssistantCliError(error)


def wsapi(
    ctx: Configuration,
    frame: Dict,
    callback: Optional[Callable[[Dict], Any]] = None,
) -> Optional[Dict]:
    """Make a call to Home Assistant using WS API.

    if callback provided will keep listening and call
    on every message.

    If no callback return data returned.
    """
    loop = asyncio.get_event_loop()

    async def fetcher() -> Optional[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                resolve_server(ctx) + "/api/websocket"
            ) as wsconn:

                await wsconn.send_str(
                    json.dumps({'type': 'auth', 'access_token': ctx.token})
                )

                frame['id'] = 1

                await wsconn.send_str(json.dumps(frame))

                while True:
                    msg = await wsconn.receive()
                    if msg.type == aiohttp.WSMsgType.ERROR:
                        break
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.TEXT:
                        mydata = json.loads(msg.data)  # type: Dict

                        if callback:
                            callback(mydata)
                        elif mydata['type'] == 'result':
                            return mydata
        return None

    result = loop.run_until_complete(fetcher())
    return result


class JSONEncoder(json.JSONEncoder):
    """JSONEncoder that supports Home Assistant objects."""

    # pylint: disable=method-hidden
    def default(self, o: Any) -> Any:
        """Convert Home Assistant objects.

        Hand other objects to the original method.
        """
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, set):
            return list(o)
        if hasattr(o, "as_dict"):
            return o.as_dict()

        return json.JSONEncoder.default(self, o)


def get_areas(ctx: Configuration) -> List[Dict[str, Any]]:
    """Return all areas."""
    frame = {'type': hass.WS_TYPE_AREA_REGISTRY_LIST}

    areas = cast(Dict, wsapi(ctx, frame))[
        'result'
    ]  # type: List[Dict[str, Any]]

    return areas


def find_area(ctx: Configuration, id_or_name: str) -> Optional[Dict[str, str]]:
    """Find area first by id and if no match by name."""
    areas = get_areas(ctx)

    area = next((x for x in areas if x['area_id'] == id_or_name), None)
    if not area:
        area = next((x for x in areas if x['name'] == id_or_name), None)

    return area


def create_area(ctx: Configuration, name: str) -> Dict[str, Any]:
    """Create area."""
    frame = {'type': hass.WS_TYPE_AREA_REGISTRY_CREATE, 'name': name}

    return cast(Dict[str, Any], wsapi(ctx, frame))


def delete_area(ctx: Configuration, area_id: str) -> Dict[str, Any]:
    """Delete area."""
    frame = {'type': hass.WS_TYPE_AREA_REGISTRY_DELETE, 'area_id': area_id}

    return cast(Dict[str, Any], wsapi(ctx, frame))


def rename_area(
    ctx: Configuration, area_id: str, new_name: str
) -> Dict[str, Any]:
    """Rename area."""
    frame = {
        'type': hass.WS_TYPE_AREA_REGISTRY_UPDATE,
        'area_id': area_id,
        'name': new_name,
    }

    return cast(Dict[str, Any], wsapi(ctx, frame))


def rename_entity(
    ctx: Configuration,
    entity_id: str,
    new_id: Optional[str],
    new_name: Optional[str],
) -> Dict[str, Any]:
    """Rename entity."""
    frame = {
        'type': hass.WS_TYPE_ENTITY_REGISTRY_UPDATE,
        'entity_id': entity_id,
    }

    if new_name:
        frame['name'] = new_name
    if new_id:
        frame['new_entity_id'] = new_id

    return cast(Dict[str, Any], wsapi(ctx, frame))


def assign_area(
    ctx: Configuration, device_id: str, area_id: str
) -> Dict[str, Any]:
    """Assign area."""
    frame = {
        'type': hass.WS_TYPE_DEVICE_REGISTRY_UPDATE,
        'area_id': area_id,
        'device_id': device_id,
    }

    return cast(Dict[str, Any], wsapi(ctx, frame))


def get_health(ctx: Configuration) -> Dict[str, Any]:
    """Get system Health."""
    frame = {'type': 'system_health/info'}

    info = cast(Dict[str, Dict[str, Any]], wsapi(ctx, frame))['result']

    return info


def get_devices(ctx: Configuration) -> List[Dict[str, Any]]:
    """Return all devices."""
    frame = {'type': hass.WS_TYPE_DEVICE_REGISTRY_LIST}

    devices = cast(Dict[str, List[Dict[str, Any]]], wsapi(ctx, frame))[
        'result'
    ]

    return devices


def get_entities(ctx: Configuration) -> List[Dict[str, Any]]:
    """Return all entities."""
    frame = {'type': hass.WS_TYPE_ENTITY_REGISTRY_LIST}

    devices = cast(Dict[str, List[Dict[str, Any]]], wsapi(ctx, frame))[
        'result'
    ]

    return devices


def get_entity(ctx: Configuration, entity_id: str) -> List[Dict[str, Any]]:
    """Return id."""
    frame = {'type': hass.WS_TYPE_ENTITY_REGISTRY_GET, 'entity_id': entity_id}

    result = cast(Dict[str, List[Dict[str, Any]]], wsapi(ctx, frame))

    return result['id']


def validate_api(ctx: Configuration) -> APIStatus:
    """Make a call to validate API."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API)

        if req.status_code == 200:
            return APIStatus.OK

        if req.status_code == 401:
            return APIStatus.INVALID_PASSWORD

        return APIStatus.UNKNOWN

    except HomeAssistantCliError:
        return APIStatus.CANNOT_CONNECT


def get_info(ctx: Configuration) -> Dict[str, Any]:
    """Get basic info about the Home Assistant instance."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_DISCOVERY_INFO)

        req.raise_for_status()

        return (
            cast(Dict[str, Any], req.json()) if req.status_code == 200 else {}
        )

    except (HomeAssistantCliError, ValueError):
        raise HomeAssistantCliError("Unexpected error retrieving information")
        # ValueError if req.json() can't parse the json


def get_events(ctx: Configuration) -> Dict[str, Any]:
    """Return all events."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_EVENTS)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting events: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())

    raise HomeAssistantCliError(
        "Error while getting all events: {}".format(req.text)
    )


def get_history(
    ctx: Configuration,
    entities: Optional[List] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> List[Dict[str, Any]]:
    """Return History."""
    try:
        if start_time:
            method = hass.URL_API_HISTORY_PERIOD.format(start_time.isoformat())
        else:
            method = hass.URL_API_HISTORY

        params = collections.OrderedDict()  # type: Dict[str, str]

        if entities:
            params["filter_entity_id"] = ",".join(entities)
        if end_time:
            params["end_time"] = end_time.isoformat()

        if params:
            method = "{}?{}".format(method, urlencode(params))

        req = restapi(ctx, METH_GET, method)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting history: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(List[Dict[str, Any]], req.json())

    raise HomeAssistantCliError(
        "Error while getting all events: {}".format(req.text)
    )


def get_states(ctx: Configuration) -> List[Dict[str, Any]]:
    """Return all states."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_STATES)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting state: {}".format(ex)
        )

    if req.status_code == 200:
        data = req.json()  # type: List[Dict[str, Any]]
        return data

    raise HomeAssistantCliError(
        "Error while getting all states: {}".format(req.text)
    )


def get_raw_error_log(ctx: Configuration) -> str:
    """Return the error log."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_ERROR_LOG)
        req.raise_for_status()
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting error log: {}".format(ex)
        )

    return req.text


def get_config(ctx: Configuration) -> Dict[str, Any]:
    """Return the running configuration."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_CONFIG)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting configuration: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, str], req.json())

    raise HomeAssistantCliError(
        "Error while getting all configuration: {}".format(req.text)
    )


def get_state(ctx: Configuration, entity_id: str) -> Optional[Dict[str, Any]]:
    """Get entity state. If ok, return dictionary with state.

    If no entity found return None - otherwise excepton raised
    with details.
    """
    try:
        req = restapi(
            ctx, METH_GET, hass.URL_API_STATES_ENTITY.format(entity_id)
        )
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting state: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())
    if req.status_code == 404:
        return None

    raise HomeAssistantCliError(
        "Error while getting Entity {}: {}".format(entity_id, req.text)
    )


def remove_state(ctx: Configuration, entity_id: str) -> bool:
    """Call API to remove state for entity_id.

    If success return True, if could not find the entity return False.
    Otherwise raise exception with details.
    """
    try:
        req = restapi(
            ctx, METH_DELETE, hass.URL_API_STATES_ENTITY.format(entity_id)
        )

        if req.status_code == 200:
            return True
        if req.status_code == 404:
            return False
    except HomeAssistantCliError:
        raise HomeAssistantCliError("Unexpected error removing state")

    raise HomeAssistantCliError(
        "Error removing state: {} - {}".format(req.status_code, req.text)
    )


def set_state(
    ctx: Configuration, entity_id: str, data: Dict
) -> Dict[str, Any]:
    """Set/update state for entity id."""
    try:
        req = restapi(
            ctx, METH_POST, hass.URL_API_STATES_ENTITY.format(entity_id), data
        )
    except HomeAssistantCliError as exception:
        raise HomeAssistantCliError(
            "Error updating state for entity {}: {}".format(
                entity_id, exception
            )
        )

    if req.status_code not in (200, 201):
        raise HomeAssistantCliError(
            "Error changing state for entity {}: {} - {}".format(
                entity_id, req.status_code, req.text
            )
        )
    return cast(Dict[str, Any], req.json())


def render_template(ctx: Configuration, template: str, variables: Dict) -> str:
    """Render template."""
    data = {"template": template, "variables": variables}

    try:
        req = restapi(ctx, METH_POST, hass.URL_API_TEMPLATE, data)
    except HomeAssistantCliError as exception:
        raise HomeAssistantCliError(
            "Error applying template: {}".format(exception)
        )

    if req.status_code not in (200, 201):
        raise HomeAssistantCliError(
            "Error applying template: {} - {}".format(
                req.status_code, req.text
            )
        )
    return req.text


def get_event_listeners(ctx: Configuration) -> Dict:
    """List of events that is being listened for."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_EVENTS)

        return req.json() if req.status_code == 200 else {}  # type: ignore

    except (HomeAssistantCliError, ValueError):
        # ValueError if req.json() can't parse the json
        _LOGGER.exception("Unexpected result retrieving event listeners")

        return {}


def fire_event(
    ctx: Configuration, event_type: str, data: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Fire an event at remote API."""
    try:
        req = restapi(
            ctx, METH_POST, hass.URL_API_EVENTS_EVENT.format(event_type), data
        )

        if req.status_code != 200:
            _LOGGER.error(
                "Error firing event: %d - %s", req.status_code, req.text
            )

        return cast(Dict[str, Any], req.json())

    except HomeAssistantCliError as exception:
        raise HomeAssistantCliError("Error firing event: {}".format(exception))


def call_service(
    ctx: Configuration,
    domain: str,
    service: str,
    service_data: Optional[Dict] = None,
) -> List[Dict[str, Any]]:
    """Call a service."""
    try:
        req = restapi(
            ctx,
            METH_POST,
            hass.URL_API_SERVICES_SERVICE.format(domain, service),
            service_data,
        )
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError("Error calling service: {}".format(ex))

    if req.status_code != 200:
        raise HomeAssistantCliError(
            "Error calling service: {} - {}".format(req.status_code, req.text)
        )

    return cast(List[Dict[str, Any]], req.json())


def get_services(ctx: Configuration,) -> List[Dict[str, Any]]:
    """Get list of services."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_SERVICES)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting services: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(List[Dict[str, Any]], req.json())

    raise HomeAssistantCliError(
        "Error while getting all services: {}".format(req.text)
    )
