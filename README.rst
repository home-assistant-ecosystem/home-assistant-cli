Home Assistant Command-line Interface (``hass-cli``)
====================================================

|Chat Status| |License| |PyPI|

The Home Assistant Command-line interface (``hass-cli``) allows one to
work with a local or a remote `Home Assistant <https://home-assistant.io>`_
instance directly from the command-line.

.. code:: bash

   $ hass-cli
    Usage: hass-cli [OPTIONS] COMMAND [ARGS]...

      A command line interface for Home Assistant.

    Options:
      --version            Show the version and exit.
      -h, --host TEXT      The IP address of Home Assistant instance.
      -p, --password TEXT  The API password of Home Assistant instance.
      -v, --verbose        Enables verbose mode.
      --help               Show this message and exit.

    Commands:
      discovery  Discovery for the local network.
      info       Get configuration details.
      list       List various entries of an instance.
      notify     Send a notification with a given service.
      state      Get, set or remove the state of entity.
      status     Show the status of an instance.

Documentation will be available at `Home Assistant <https://home-assistant.io>`_.

This tool is in ALPHA stage or a so-called prototype.

Clone the git repository and 

.. code:: bash

    $ pip3 install --editable .


A hard requirement is that ``hass-cli`` needs to support Python 3.4 because
Home Assistant is able to run with Python 3.4.2.

.. |Chat Status| image:: https://img.shields.io/discord/330944238910963714.svg
   :target: https://discord.gg/c5DvZ4e
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/home-assistant/home-assistant-cli/blob/master/LICENSE
   :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/home-assistant-cli.svg
   :target: https://pypi.python.org/pypi/home-assistant-cli
   :alt: PyPI release

