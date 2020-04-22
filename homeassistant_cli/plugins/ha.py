"""Home Assistant (former Hass.io) plugin for Home Assistant CLI (hass-cli)."""
from distutils.version import StrictVersion
import json as json_
import logging
from typing import Any, Dict, List, cast  # noqa: F401

import click
from requests.exceptions import HTTPError

from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.exceptions import HomeAssistantCliError
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)

# These commands loosely based on what is found in
# https://github.com/home-assistant/supervisor/blob/master/API.md


@click.group('ha')
@pass_context
def cli(ctx: Configuration):
    """Home Assistant (former Hass.io) commands."""
    ctx.auto_output("data")


def _report(ctx, cmd, method, response) -> None:
    """Create a report."""
    response.raise_for_status()

    if response.ok:
        try:
            ctx.echo(format_output(ctx, response.json()))
        except json_.decoder.JSONDecodeError:
            _LOGGING.debug("Response could not be parsed as JSON")
            ctx.echo(response.text)
    else:
        _LOGGING.warning(
            "%s: <No output returned from %s %s>",
            response.status_code,
            cmd,
            method,
        )


def _handle(ctx, method, httpmethod='get', raw=False) -> None:
    """Handle the data."""
    method = "/api/hassio/" + method
    response = api.restapi(ctx, httpmethod, method)
    api.restapi(ctx, httpmethod, method)

    _report(ctx, httpmethod, method, response)


def _handle_raw(ctx, method, httpmethod='get') -> Dict:
    """Handle raw data."""
    method = "/api/hassio/" + method
    response = api.restapi(ctx, httpmethod, method)
    api.restapi(ctx, httpmethod, method)
    return response.json()


@cli.group('supervisor')
@pass_context
def supervisor(ctx: Configuration):
    """Home Assistant supervisor commands."""
    ctx.auto_output("data")


@supervisor.command('ping')
@pass_context
def supervisor_ping(ctx: Configuration):
    """Home Assistant supervisor ping."""
    _handle(ctx, 'supervisor/ping')


@supervisor.command('info')
@pass_context
def supervisor_info(ctx: Configuration):
    """Home Assistant supervisor info."""
    _handle(ctx, 'supervisor/info')


@supervisor.command('update')
@pass_context
def supervisor_update(ctx: Configuration):
    """Home Assistant supervisor update."""
    response = _handle_raw(ctx, 'supervisor/info')
    data = response['data']
    current_version = int(data['version'])
    latest_version = int(data['version_latest'])
    if current_version == latest_version:
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, 'supervisor/update', 'post')
        except (HomeAssistantCliError, HTTPError):
            pass


@supervisor.command('options')
@pass_context
def supervisor_options(ctx: Configuration):
    """Home Assistant supervisor options."""
    _handle(ctx, 'supervisor/options', 'post')


@supervisor.command('reload')
@pass_context
def supervisor_reload(ctx: Configuration):
    """Home Assistant supervisor reload."""
    _handle(ctx, 'supervisor/reload', 'post')


@supervisor.command('logs')
@pass_context
def supervisor_logs(ctx: Configuration):
    """Home Assistant supervisor logs."""
    _handle(ctx, 'supervisor/logs')


@supervisor.command('repair')
@pass_context
def supervisor_repair(ctx: Configuration):
    """Home Assistant supervisor repair."""
    _handle(ctx, 'supervisor/repair')


@supervisor.command('stats')
@pass_context
def supervisor_stats(ctx: Configuration):
    """Home Assistant supervisor stats."""
    _handle(ctx, 'supervisor/stats')


@cli.group('snapshot')
@pass_context
def snapshot(ctx: Configuration):
    """Home Assistant snapshot commands."""
    ctx.auto_output('data')


@snapshot.command('reload')
@pass_context
def snapshot_reload(ctx: Configuration):
    """Home Assistant snapshots reload."""
    _handle(ctx, 'snapshots/reload', 'post')


@snapshot.command('shutdown')
@pass_context
def snapshot_shutdown(ctx: Configuration):
    """Home Assistant host shutdown."""
    _handle(ctx, 'host/shutdown', 'post')


@cli.group('host')
@pass_context
def host(ctx: Configuration):
    """Home Assistant host commands."""
    ctx.auto_output('data')


@host.command('reboot')
@pass_context
def host_reboot(ctx: Configuration):
    """Home Assistant host reboot."""
    _handle(ctx, 'host/reboot', 'post')


@host.command('reload')
@pass_context
def host_reload(ctx: Configuration):
    """Home Assistant host reload."""
    _handle(ctx, 'host/reload', 'post')


@host.command('shutdown')
@pass_context
def host_shutdown(ctx: Configuration):
    """Home Assistant host shutdown."""
    _handle(ctx, 'host/shutdown', 'post')


@host.command('info')
@pass_context
def host_info(ctx: Configuration):
    """Home Assistant host info."""
    _handle(ctx, 'host/info')


@host.command('options')
@pass_context
def host_options(ctx: Configuration):
    """Home Assistant options shutdown."""
    _handle(ctx, 'host/options', 'post')


@host.command('services')
@pass_context
def host_services(ctx: Configuration):
    """Home Assistant host reboot."""
    _handle(ctx, 'host/services')


@cli.group('os')
@pass_context
def os(ctx: Configuration):
    """Home Assistant os commands."""
    ctx.auto_output('data')


@os.command('info')
@pass_context
def os_info(ctx: Configuration):
    """Home Assistant os info."""
    _handle(ctx, 'os/info')


@os.command('update')
@pass_context
def os_update(ctx: Configuration):
    """Home Assistant os update."""
    response = _handle_raw(ctx, 'os/info')
    data = response['data']
    current_version = data['version']
    latest_version = data['version_latest']
    if StrictVersion(current_version) == StrictVersion(latest_version):
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, 'os/update', 'post')
        except (HomeAssistantCliError, HTTPError):
            pass


@cli.group('hardware')
@pass_context
def hardware(ctx: Configuration):
    """Home Assistant hardware info."""
    ctx.auto_output('data')


@hardware.command('info')
@pass_context
def hardware_info(ctx: Configuration):
    """Home Assistant hardware audio."""
    _handle(ctx, 'hardware/info')


@hardware.command('audio')
@pass_context
def hardware_audio(ctx: Configuration):
    """Home Assistant hardware audio."""
    _handle(ctx, 'hardware/audio')


@hardware.command('trigger')
@pass_context
def hardware_trigger(ctx: Configuration):
    """Home Assistant hardware trigger."""
    try:
        _handle(ctx, 'hardware/trigger', 'post')
    except (HomeAssistantCliError, HTTPError):
        pass


@cli.group('addons')
@pass_context
def addons(ctx: Configuration):
    """Home Assistant addons commands."""
    ctx.auto_output('data')


@addons.command('all')
@pass_context
def addons_all(ctx: Configuration):
    """Home Assistant addons info."""
    _handle(ctx, 'addons')


@addons.command('reload')
@pass_context
def addons_reload(ctx: Configuration):
    """Home Assistant addons reload."""
    _handle(ctx, 'addons/reload', 'post')


@cli.group('core')
@pass_context
def core(ctx: Configuration):
    """Home Assistant core commands."""
    ctx.auto_output('data')


@core.command('info')
@pass_context
def core_info(ctx: Configuration):
    """Home Assistant core info."""
    _handle(ctx, 'core/info')


@core.command('update')
@pass_context
def core_update(ctx: Configuration):
    """Home Assistant core update."""
    response = _handle_raw(ctx, 'core/info')
    data = response['data']
    current_version = data['version']
    latest_version = data['version_latest']
    if StrictVersion(current_version) == StrictVersion(latest_version):
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, 'core/update', 'post')
        except (HomeAssistantCliError, HTTPError):
            pass


@core.command('logs')
@pass_context
def core_logs(ctx: Configuration):
    """Home Assistant core logs."""
    _handle(ctx, 'core/logs')


@core.command('restart')
@pass_context
def core_restart(ctx: Configuration):
    """Home Assistant core restart."""
    try:
        _handle(ctx, 'core/restart', 'post')
    except HomeAssistantCliError:
        pass


@core.command('check')
@pass_context
def core_check(ctx: Configuration):
    """Home Assistant core check."""
    try:
        _handle(ctx, 'core/check', 'post')
    except (HomeAssistantCliError, HTTPError):
        _handle(ctx, 'core/logs')


@core.command('start')
@pass_context
def core_start(ctx: Configuration):
    """Home Assistant core start."""
    try:
        _handle(ctx, 'core/start', 'post')
    except HomeAssistantCliError:
        pass


@core.command('stop')
@pass_context
def core_stop(ctx: Configuration):
    """Home Assistant core stop."""
    try:
        _handle(ctx, 'core/stop', 'post')
    except HomeAssistantCliError:
        pass


@core.command('rebuild')
@pass_context
def core_rebuild(ctx: Configuration):
    """Home Assistant core rebuild."""
    try:
        _handle(ctx, 'core/rebuild', 'post')
    except HomeAssistantCliError:
        pass


@core.command('options')
@pass_context
def core_options(ctx: Configuration):
    """Home Assistant core options."""
    _handle(ctx, 'core/options', 'post')


@core.command('websocket')
@pass_context
def core_websocket(ctx: Configuration):
    """Home Assistant core websocket."""
    try:
        _handle(ctx, 'core/websocket')
    except (HomeAssistantCliError, HTTPError):
        pass


@core.command('stats')
@pass_context
def core_stats(ctx: Configuration):
    """Home Assistant core stats."""
    _handle(ctx, 'core/stats')


@cli.group('dns')
@pass_context
def dns(ctx: Configuration):
    """Home Assistant DNS commands."""
    ctx.auto_output('data')


@dns.command('info')
@pass_context
def dns_info(ctx: Configuration):
    """Home Assistant DNS info."""
    _handle(ctx, 'dns/info')


@dns.command('options')
@pass_context
def dns_options(ctx: Configuration):
    """Home Assistant DNS options."""
    _handle(ctx, 'dns/options', 'post')


@dns.command('restart')
@pass_context
def dns_restart(ctx: Configuration):
    """Home Assistant DNS restart."""
    try:
        _handle(ctx, 'dns/restart', 'post')
    except HomeAssistantCliError:
        pass


@dns.command('logs')
@pass_context
def dns_logs(ctx: Configuration):
    """Home Assistant DNS logs."""
    _handle(ctx, 'dns/logs')


@dns.command('stats')
@pass_context
def dns_stats(ctx: Configuration):
    """Home Assistant DNS stats."""
    _handle(ctx, 'dns/stats')


@cli.group('multicast')
@pass_context
def multicast(ctx: Configuration):
    """Home Assistant Multicast commands."""
    ctx.auto_output('data')


@multicast.command('info')
@pass_context
def multicast_info(ctx: Configuration):
    """Home Assistant Multicast info."""
    _handle(ctx, 'multicast/info')


@multicast.command('update')
@pass_context
def multicast_update(ctx: Configuration):
    """Home Assistant Multicast update."""
    response = _handle_raw(ctx, 'multicast/info')
    data = response['data']
    current_version = int(data['version'])
    latest_version = int(data['version_latest'])
    if current_version == latest_version:
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, 'multicast/update', 'post')
        except (HomeAssistantCliError, HTTPError):
            pass


@multicast.command('restart')
@pass_context
def multicast_restart(ctx: Configuration):
    """Home Assistant Multicast restart."""
    try:
        _handle(ctx, 'multicast/restart', 'post')
    except HomeAssistantCliError:
        pass


@multicast.command('logs')
@pass_context
def multicast_logs(ctx: Configuration):
    """Home Assistant DNS logs."""
    _handle(ctx, 'multicast/logs')


@multicast.command('stats')
@pass_context
def multicast_stats(ctx: Configuration):
    """Home Assistant Multicast stats."""
    _handle(ctx, 'multicast/stats')


@cli.group('ha-cli')
@pass_context
def ha_cli(ctx: Configuration):
    """Home Assistant ha-cli commands."""
    ctx.auto_output('data')


@ha_cli.command('info')
@pass_context
def ha_info(ctx: Configuration):
    """Home Assistant ha-cli info."""
    _handle(ctx, 'cli/info')


@ha_cli.command('update')
@pass_context
def ha_update(ctx: Configuration):
    """Home Assistant ha-cli update."""
    response = _handle_raw(ctx, 'cli/info')
    data = response['data']
    current_version = int(data['version'])
    latest_version = int(data['version_latest'])
    if current_version == latest_version:
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, 'cli/update', 'post')
        except (HomeAssistantCliError, HTTPError):
            pass


@ha_cli.command('restart')
@pass_context
def ha_restart(ctx: Configuration):
    """Home Assistant ha-cli restart."""
    try:
        _handle(ctx, 'cli/restart', 'post')
    except HomeAssistantCliError:
        pass


@ha_cli.command('logs')
@pass_context
def ha_logs(ctx: Configuration):
    """Home Assistant ha-cli logs."""
    _handle(ctx, 'cli/logs')


@ha_cli.command('stats')
@pass_context
def ha_stats(ctx: Configuration):
    """Home Assistant ha-cli stats."""
    _handle(ctx, 'cli/stats')
