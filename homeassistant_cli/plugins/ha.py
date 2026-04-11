"""Home Assistant Operating System plugin for Home Assistant CLI (hass-cli)."""

import json as json_
import logging
from typing import Any, Dict, List, cast

import click
from packaging.version import Version
from requests.exceptions import HTTPError

import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.exceptions import HomeAssistantCliError
from homeassistant_cli.helper import format_output

_LOGGING = logging.getLogger(__name__)

# These commands loosely based on what can be found in
# https://developers.home-assistant.io/docs/api/supervisor/endpoints


@click.group("ha")
@pass_context
def cli(ctx: Configuration):
    """Home Assistant Operating System commands."""
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


def _handle(ctx, method, httpmethod="get", raw=False) -> None:
    """Handle the data."""
    method = f"/{method}"
    response = api.restapi_supervisor(ctx, httpmethod, method)

    _report(ctx, httpmethod, method, response)


def _handle_raw(ctx, method, httpmethod="get") -> dict:
    """Handle raw data."""
    method = f"/{method}"
    response = api.restapi_supervisor(ctx, httpmethod, method)
    return response.json()


# Addon/Apps endpoints
#########################################################################
@cli.group("addons")
@pass_context
def addons(ctx: Configuration):
    """Home Assistant addons commands."""
    ctx.auto_output("data")


@addons.command("all")
@pass_context
def addons_all(ctx: Configuration):
    """Home Assistant addons info."""
    _handle(ctx, "addons")


@addons.command("reload")
@pass_context
def addons_reload(ctx: Configuration):
    """Home Assistant addons reload."""
    _handle(ctx, "addons/reload", "post")


# Audio endpoints
#########################################################################
@cli.group("audio")
@pass_context
def audio(ctx: Configuration):
    """Home Assistant audio commands."""
    ctx.auto_output("data")


@audio.command("info")
@pass_context
def audio_info(ctx: Configuration):
    """Home Assistant audio info."""
    _handle(ctx, "audio/info")


@audio.command("stats")
@pass_context
def audio_stats(ctx: Configuration):
    """Home Assistant audio stats."""
    _handle(ctx, "audio/stats")


@audio.command("logs")
@pass_context
def audio_logs(ctx: Configuration):
    """Home Assistant audio logs."""
    _handle(ctx, "audio/logs")


@audio.command("reload")
@pass_context
def audio_reload(ctx: Configuration):
    """Home Assistant audio reload."""
    _handle(ctx, "audio/reload", "post")


@audio.command("restart")
@pass_context
def audio_restart(ctx: Configuration):
    """Home Assistant audio restart."""
    _handle(ctx, "audio/restart", "post")


# Auth endpoints
#########################################################################
@cli.group("auth")
@pass_context
def auth(ctx: Configuration):
    """Home Assistant auth commands."""
    ctx.auto_output("data")


@auth.command("list")
@pass_context
def auth_list(ctx: Configuration):
    """Home Assistant auth list."""
    _handle(ctx, "auth/list")


# Backup endpoints
#########################################################################
@cli.group("backup")
@pass_context
def backup(ctx: Configuration):
    """Home Assistant backup commands."""
    ctx.auto_output("data")


@backup.command("info")
@pass_context
def backup_info(ctx: Configuration):
    """Home Assistant backup info."""
    _handle(ctx, "backups/info")


@backup.command("reload")
@pass_context
def backup_reload(ctx: Configuration):
    """Home Assistant backups reload."""
    _handle(ctx, "backups/reload", "post")


# CLI endpoints
#########################################################################
@cli.group("ha-cli")
@pass_context
def ha_cli(ctx: Configuration):
    """Home Assistant ha-cli commands."""
    ctx.auto_output("data")


@ha_cli.command("info")
@pass_context
def ha_info(ctx: Configuration):
    """Home Assistant ha-cli info."""
    _handle(ctx, "cli/info")


@ha_cli.command("update")
@pass_context
def ha_update(ctx: Configuration):
    """Home Assistant ha-cli update."""
    response = _handle_raw(ctx, "cli/info")
    data = response["data"]
    current_version = int(data["version"])
    latest_version = int(data["version_latest"])
    if current_version == latest_version:
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, "cli/update", "post")
        except (HomeAssistantCliError, HTTPError):
            pass


@ha_cli.command("stats")
@pass_context
def ha_stats(ctx: Configuration):
    """Home Assistant ha-cli stats."""
    _handle(ctx, "cli/stats")


# Core endpoints
#########################################################################
@cli.group("core")
@pass_context
def core(ctx: Configuration):
    """Home Assistant core commands."""
    ctx.auto_output("data")


@core.command("info")
@pass_context
def core_info(ctx: Configuration):
    """Home Assistant core info."""
    _handle(ctx, "core/info")


@core.command("update")
@pass_context
def core_update(ctx: Configuration):
    """Home Assistant core update."""
    response = _handle_raw(ctx, "core/info")
    data = response["data"]
    current_version = data["version"]
    latest_version = data["version_latest"]
    if Version(current_version) == Version(latest_version):
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, "core/update", "post")
        except (HomeAssistantCliError, HTTPError):
            pass


@core.command("logs")
@pass_context
def core_logs(ctx: Configuration):
    """Home Assistant core logs."""
    _handle(ctx, "core/logs")


@core.command("restart")
@pass_context
def core_restart(ctx: Configuration):
    """Home Assistant core restart."""
    try:
        _handle(ctx, "core/restart", "post")
    except HomeAssistantCliError:
        pass


@core.command("check")
@pass_context
def core_check(ctx: Configuration):
    """Home Assistant core check."""
    try:
        _handle(ctx, "core/check", "post")
    except (HomeAssistantCliError, HTTPError):
        _handle(ctx, "core/logs")


@core.command("start")
@pass_context
def core_start(ctx: Configuration):
    """Home Assistant core start."""
    try:
        _handle(ctx, "core/start", "post")
    except HomeAssistantCliError:
        pass


@core.command("stop")
@pass_context
def core_stop(ctx: Configuration):
    """Home Assistant core stop."""
    try:
        _handle(ctx, "core/stop", "post")
    except HomeAssistantCliError:
        pass


@core.command("rebuild")
@pass_context
def core_rebuild(ctx: Configuration):
    """Home Assistant core rebuild."""
    try:
        _handle(ctx, "core/rebuild", "post")
    except HomeAssistantCliError:
        pass


@core.command("options")
@pass_context
def core_options(ctx: Configuration):
    """Home Assistant core options."""
    _handle(ctx, "core/options", "post")


@core.command("websocket")
@pass_context
def core_websocket(ctx: Configuration):
    """Home Assistant core websocket."""
    try:
        _handle(ctx, "core/websocket")
    except (HomeAssistantCliError, HTTPError):
        pass


@core.command("stats")
@pass_context
def core_stats(ctx: Configuration):
    """Home Assistant core stats."""
    _handle(ctx, "core/stats")


# Discovery endpoints
#########################################################################
# Not implemented
# @cli.group("discovery")
# @pass_context
# def discovery(ctx: Configuration):
#     """Home Assistant discovery commands."""
#     ctx.auto_output("data")


# DNS endpoints
#########################################################################
@cli.group("dns")
@pass_context
def dns(ctx: Configuration):
    """Home Assistant DNS commands."""
    ctx.auto_output("data")


@dns.command("info")
@pass_context
def dns_info(ctx: Configuration):
    """Home Assistant DNS info."""
    _handle(ctx, "dns/info")


@dns.command("options")
@pass_context
def dns_options(ctx: Configuration):
    """Home Assistant DNS options."""
    _handle(ctx, "dns/options", "post")


@dns.command("restart")
@pass_context
def dns_restart(ctx: Configuration):
    """Home Assistant DNS restart."""
    try:
        _handle(ctx, "dns/restart", "post")
    except HomeAssistantCliError:
        pass


@dns.command("logs")
@pass_context
def dns_logs(ctx: Configuration):
    """Home Assistant DNS logs."""
    _handle(ctx, "dns/logs")


@dns.command("stats")
@pass_context
def dns_stats(ctx: Configuration):
    """Home Assistant DNS stats."""
    _handle(ctx, "dns/stats")


@dns.command("update")
@pass_context
def dns_update(ctx: Configuration):
    """Home Assistant DNS update."""
    try:
        _handle(ctx, "dns/update", "post")
    except (HomeAssistantCliError, HTTPError):
        pass


@dns.command("reset")
@pass_context
def dns_reset(ctx: Configuration):
    """Home Assistant DNS reset."""
    try:
        _handle(ctx, "dns/reset", "post")
    except (HomeAssistantCliError, HTTPError):
        pass


# Docker endpoints
#########################################################################
@cli.group("docker")
@pass_context
def docker(ctx: Configuration):
    """Home Assistant Docker commands."""
    ctx.auto_output("data")


@docker.command("info")
@pass_context
def docker_info(ctx: Configuration):
    """Home Assistant Docker info."""
    _handle(ctx, "docker/info")


@docker.command("registries")
@pass_context
def docker_registries(ctx: Configuration):
    """Home Assistant Docker registries."""
    _handle(ctx, "docker/registries")


# Hardware endpoints
#########################################################################
@cli.group("hardware")
@pass_context
def hardware(ctx: Configuration):
    """Home Assistant hardware info."""
    ctx.auto_output("data")


@hardware.command("info")
@pass_context
def hardware_info(ctx: Configuration):
    """Home Assistant hardware info."""
    _handle(ctx, "hardware/info")


@hardware.command("audio")
@pass_context
def hardware_audio(ctx: Configuration):
    """Home Assistant hardware audio."""
    _handle(ctx, "hardware/audio")


# Host endpoints
#########################################################################
@cli.group("host")
@pass_context
def host(ctx: Configuration):
    """Home Assistant host commands."""
    ctx.auto_output("data")


@host.command("reboot")
@pass_context
def host_reboot(ctx: Configuration):
    """Home Assistant host reboot."""
    _handle(ctx, "host/reboot", "post")


@host.command("reload")
@pass_context
def host_reload(ctx: Configuration):
    """Home Assistant host reload."""
    _handle(ctx, "host/reload", "post")


@host.command("shutdown")
@pass_context
def host_shutdown(ctx: Configuration):
    """Home Assistant host shutdown."""
    _handle(ctx, "host/shutdown", "post")


@host.command("info")
@pass_context
def host_info(ctx: Configuration):
    """Home Assistant host info."""
    _handle(ctx, "host/info")


@host.command("options")
@pass_context
def host_options(ctx: Configuration):
    """Home Assistant options shutdown."""
    _handle(ctx, "host/options", "post")


@host.command("services")
@pass_context
def host_services(ctx: Configuration):
    """Home Assistant host reboot."""
    _handle(ctx, "host/services")


# Ingress endpoints
#########################################################################
@cli.group("ingress")
@pass_context
def ingress(ctx: Configuration):
    """Home Assistant ingress info."""
    ctx.auto_output("data")


@ingress.command("info")
@pass_context
def ingress_info(ctx: Configuration):
    """Home Assistant ingress info."""
    _handle(ctx, "ingress/panels")


# Jobs endpoints
#########################################################################
@cli.group("jobs")
@pass_context
def jobs(ctx: Configuration):
    """Home Assistant jobs info."""
    ctx.auto_output("data")


@jobs.command("info")
@pass_context
def jobs_info(ctx: Configuration):
    """Home Assistant jobs info."""
    _handle(ctx, "jobs/info")


# Root endpoints
#########################################################################
@cli.group("root")
@pass_context
def root(ctx: Configuration):
    """Home Assistant root info."""
    ctx.auto_output("data")


@root.command("info")
@pass_context
def root_info(ctx: Configuration):
    """Home Assistant root info."""
    _handle(ctx, "info")


@root.command("info")
@pass_context
def root_available_updates(ctx: Configuration):
    """Home Assistant root available updates."""
    _handle(ctx, "available_updates")


# Mount endpoints
#########################################################################
@cli.group("mount")
@pass_context
def mount(ctx: Configuration):
    """Home Assistant mount info."""
    ctx.auto_output("data")


@mount.command("info")
@pass_context
def mount_info(ctx: Configuration):
    """Home Assistant mount info."""
    _handle(ctx, "mounts")


# Multicast endpoints
#########################################################################
@cli.group("multicast")
@pass_context
def multicast(ctx: Configuration):
    """Home Assistant Multicast commands."""
    ctx.auto_output("data")


@multicast.command("info")
@pass_context
def multicast_info(ctx: Configuration):
    """Home Assistant Multicast info."""
    _handle(ctx, "multicast/info")


@multicast.command("update")
@pass_context
def multicast_update(ctx: Configuration):
    """Home Assistant Multicast update."""
    response = _handle_raw(ctx, "multicast/info")
    data = response["data"]
    current_version = int(data["version"])
    latest_version = int(data["version_latest"])
    if current_version == latest_version:
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, "multicast/update", "post")
        except (HomeAssistantCliError, HTTPError):
            pass


@multicast.command("restart")
@pass_context
def multicast_restart(ctx: Configuration):
    """Home Assistant Multicast restart."""
    try:
        _handle(ctx, "multicast/restart", "post")
    except HomeAssistantCliError:
        pass


@multicast.command("logs")
@pass_context
def multicast_logs(ctx: Configuration):
    """Home Assistant DNS logs."""
    _handle(ctx, "multicast/logs")


@multicast.command("stats")
@pass_context
def multicast_stats(ctx: Configuration):
    """Home Assistant Multicast stats."""
    _handle(ctx, "multicast/stats")


# Network endpoints
#########################################################################
@cli.group("network")
@pass_context
def network(ctx: Configuration):
    """Home Assistant Network commands."""
    ctx.auto_output("data")


@network.command("info")
@pass_context
def network_info(ctx: Configuration):
    """Home Assistant network info."""
    _handle(ctx, "network/info")


@network.command("reload")
@pass_context
def network_reload(ctx: Configuration):
    """Home Assistant Network reload."""
    try:
        _handle(ctx, "network/reload", "post")
    except HomeAssistantCliError:
        pass


# Observer endpoints
#########################################################################
@cli.group("observer")
@pass_context
def observer(ctx: Configuration):
    """Home Assistant Observer commands."""
    ctx.auto_output("data")


@observer.command("info")
@pass_context
def observer_info(ctx: Configuration):
    """Home Assistant observer info."""
    _handle(ctx, "observer/info")


@observer.command("stats")
@pass_context
def observer_stats(ctx: Configuration):
    """Home Assistant observer stats."""
    _handle(ctx, "observer/stats")


# OS endpoints
#########################################################################
@cli.group("os")
@pass_context
def os(ctx: Configuration):
    """Home Assistant Operating System commands."""
    ctx.auto_output("data")


@os.command("info")
@pass_context
def os_info(ctx: Configuration):
    """Home Assistant os info."""
    _handle(ctx, "os/info")


@os.command("swap")
@pass_context
def os_swap(ctx: Configuration):
    """Home Assistant os swap."""
    _handle(ctx, "os/config/swap")


@os.command("datadisk")
@pass_context
def os_datadisk(ctx: Configuration):
    """Home Assistant os datadisk."""
    _handle(ctx, "os/datadisk/list")


@os.command("update")
@pass_context
def os_update(ctx: Configuration):
    """Home Assistant Operating System update."""
    response = _handle_raw(ctx, "os/info")
    data = response["data"]
    current_version = data["version"]
    latest_version = data["version_latest"]
    if Version(current_version) == Version(latest_version):
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, "os/update", "post")
        except (HomeAssistantCliError, HTTPError):
            pass


# Resolution endpoints
#########################################################################
@cli.group("resolution")
@pass_context
def resolution(ctx: Configuration):
    """Home Assistant Resolution commands."""
    ctx.auto_output("data")


@resolution.command("info")
@pass_context
def resolution_info(ctx: Configuration):
    """Home Assistant resolution info."""
    _handle(ctx, "resolution/info")


# Services endpoints
#########################################################################
@cli.group("service")
@pass_context
def service(ctx: Configuration):
    """Home Assistant Service commands."""
    ctx.auto_output("data")


@service.command("info")
@pass_context
def service_info(ctx: Configuration):
    """Home Assistant service info."""
    _handle(ctx, "services")


@service.command("mqtt")
@pass_context
def service_mqtt(ctx: Configuration):
    """Home Assistant MQTT service info."""
    _handle(ctx, "services/mqtt")


@service.command("mysql")
@pass_context
def service_mysql(ctx: Configuration):
    """Home Assistant MySQL service info."""
    _handle(ctx, "services/mysql")


# Store endpoints
#########################################################################
@cli.group("store")
@pass_context
def store(ctx: Configuration):
    """Home Assistant Store commands."""
    ctx.auto_output("data")


@store.command("info")
@pass_context
def store_info(ctx: Configuration):
    """Home Assistant store info."""
    _handle(ctx, "store/info")


@store.command("addon")
@pass_context
def store_addon(ctx: Configuration):
    """Home Assistant addon store info."""
    _handle(ctx, "store/addons")


@store.command("repositories")
@pass_context
def store_repositories(ctx: Configuration):
    """Home Assistant store repositories info."""
    _handle(ctx, "store/repositories")


@store.command("reload")
@pass_context
def store_reload(ctx: Configuration):
    """Home Assistant Store reload."""
    try:
        _handle(ctx, "store/reload", "post")
    except HomeAssistantCliError:
        pass


# Security endpoints
#########################################################################
@cli.group("security")
@pass_context
def security(ctx: Configuration):
    """Home Assistant Security commands."""
    ctx.auto_output("data")


@security.command("info")
@pass_context
def security_info(ctx: Configuration):
    """Home Assistant security info."""
    _handle(ctx, "security/info")


# Supervisor endpoints
#########################################################################
@cli.group("supervisor")
@pass_context
def supervisor(ctx: Configuration):
    """Home Assistant supervisor commands."""
    ctx.auto_output("data")


@supervisor.command("ping")
@pass_context
def supervisor_ping(ctx: Configuration):
    """Home Assistant supervisor ping."""
    _handle(ctx, "supervisor/ping")


@supervisor.command("info")
@pass_context
def supervisor_info(ctx: Configuration):
    """Home Assistant supervisor info."""
    _handle(ctx, "supervisor/info")


@supervisor.command("update")
@pass_context
def supervisor_update(ctx: Configuration):
    """Home Assistant supervisor update."""
    response = _handle_raw(ctx, "supervisor/info")
    data = response["data"]
    current_version = int(data["version"])
    latest_version = int(data["version_latest"])
    if current_version == latest_version:
        ctx.echo("Already running the latest release")
    else:
        try:
            _handle(ctx, "supervisor/update", "post")
        except (HomeAssistantCliError, HTTPError):
            pass


@supervisor.command("options")
@pass_context
def supervisor_options(ctx: Configuration):
    """Home Assistant supervisor options."""
    _handle(ctx, "supervisor/options", "post")


@supervisor.command("reload")
@pass_context
def supervisor_reload(ctx: Configuration):
    """Home Assistant supervisor reload."""
    _handle(ctx, "supervisor/reload", "post")


@supervisor.command("logs")
@pass_context
def supervisor_logs(ctx: Configuration):
    """Home Assistant supervisor logs."""
    _handle(ctx, "supervisor/logs")


@supervisor.command("repair")
@pass_context
def supervisor_repair(ctx: Configuration):
    """Home Assistant supervisor repair."""
    _handle(ctx, "supervisor/repair", "post")


@supervisor.command("restart")
@pass_context
def supervisor_restart(ctx: Configuration):
    """Home Assistant supervisor restart."""
    try:
        _handle(ctx, "supervisor/restart", "post")
    except HomeAssistantCliError:
        pass


@supervisor.command("stats")
@pass_context
def supervisor_stats(ctx: Configuration):
    """Home Assistant supervisor stats."""
    _handle(ctx, "supervisor/stats")
