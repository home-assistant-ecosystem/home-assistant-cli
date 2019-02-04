"""conftest.py loads all fixtures found in fixtures/.

Each file are made available as follows:

Given a file named: `mydata.json`
it will be available as:

mydata_text - str with the raw text
mydata      - Dict with the content parsed from json
"""

import json
import os
import socket
import subprocess
import sys
import time
from typing import Tuple

import click_log.core as logcore
import pkg_resources
import pytest
from xprocess import ProcessStarter

FIXTURES_PATH = pkg_resources.resource_filename(__name__, 'fixtures/')


logcore.basic_config()

WIN = sys.platform == 'win32'


def wait_for_port(port: int, host='localhost', timeout=5.0):
    """Wait until a port starts accepting TCP connections.

    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time
                      specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    'Waited too long for the port {} on host {}\
                     to start accepting '
                    'connections.'.format(port, host)
                ) from ex


class VirtualEnvironment:
    """Virtual Environment to represent termpoary venv"""

    def __init__(self, path: str) -> None:
        """Init VirtualEnvironment."""
        self.path = path
        self.bin = os.path.join(
            self.path, 'bin' if sys.platform != 'win32' else 'Scripts'
        )
        self.python = os.path.join(self.bin, 'python')

    def create(self, system_packages=False) -> None:
        """Create venv."""
        cmd = [sys.executable, '-m', 'venv']
        # cmd += ['-p', python or sys.executable]
        if system_packages:
            cmd += ['--system-site-packages']
        cmd += [self.path]
        subprocess.check_call(cmd)

    def install(self, pkg_name: str, editable=False, upgrade=False) -> None:
        """Install package into venv."""
        cmd = [os.path.join(self.bin, "python"), '-m', 'pip', 'install']
        if upgrade:
            cmd += ['-U']
        if editable:
            cmd += ['-e']
        cmd += [pkg_name]
        print(cmd)
        subprocess.check_call(cmd, timeout=30)

    def get_version(self, pkg_name: str) -> Tuple[str, ...]:
        """Return version installed in venv."""
        script = (
            'import pkg_resources; '
            'print(pkg_resources.get_distribution("%(pkg_name)s").version)'
        ) % dict(pkg_name=pkg_name)
        version = subprocess.check_output([self.python, '-c', script]).strip()
        return pkg_resources.parse_version(version.decode('utf8'))


@pytest.fixture(scope="session")
def starthomeassistant(request, xprocess, tmpdir_factory):
    """Start Home Assistant for integration testing."""

    if xprocess.getinfo('homeassistant').isrunning():
        return

    tmpdir = tmpdir_factory.mktemp('venv-tmp')
    venv = VirtualEnvironment(tmpdir.strpath)
    print("Creating venv in " + str(tmpdir))
    venv.create()
    print("Install homeassistant in venv")
    venv.install('homeassistant')
    tmpdir = tmpdir_factory.mktemp('hass-tmp')
    print("Trying to luanch hass in " + str(tmpdir))

    from shutil import copyfile

    configfile = tmpdir.join('configuration.yaml')
    copyfile('hass-config/configuration.yaml', configfile)

    class Starter(ProcessStarter):
        """Start of hass"""

        args = [os.path.join(venv.bin, 'hass'), '-c', tmpdir]

        def wait(self, log_file):
            """Wait until the process is ready."""
            wait_for_port(8123, host='localhost', timeout=60.0)
            return True

    xprocess.ensure('homeassistant', Starter)


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


def generate_fixture(content: str):
    """Generate the individual fixtures."""
    pass  # pylint: disable=unnecessary-pass

    @pytest.fixture(scope='module')
    def my_fixture():
        return content

    return my_fixture


def _inject_fixture(name: str, someparam: str):
    globals()[name] = generate_fixture(someparam)


def _all_fixtures():
    for fname in os.listdir(FIXTURES_PATH):
        path = os.path.join(FIXTURES_PATH, fname)
        if os.path.isdir(path):
            continue

        name, ext = os.path.splitext(fname)

        with open(FIXTURES_PATH + fname) as file:
            content = file.read()

        _inject_fixture(name + "_text", content)
        if ext == '.json':
            _inject_fixture(name, json.loads(content))


_all_fixtures()  # type: ignore
