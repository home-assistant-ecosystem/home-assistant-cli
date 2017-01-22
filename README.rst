Home Assistant Command-line Interface (``hass-cli``)
====================================================

|Join the chat at https://gitter.im/home-assistant/home-assistant| |Join the dev chat at https://gitter.im/home-assistant/home-assistant/devs| |License| |PyPI|

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

.. |Join the chat at https://gitter.im/home-assistant/home-assistant| image:: https://img.shields.io/badge/gitter-general-blue.svg
   :target: https://gitter.im/home-assistant/home-assistant?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Join the dev chat at https://gitter.im/home-assistant/home-assistant/devs| image:: https://img.shields.io/badge/gitter-development-yellowgreen.svg
   :target: https://gitter.im/home-assistant/home-assistant/devs?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |License| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/home-assistant/home-assistant-cli/blob/master/LICENSE
   :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/home-assistant-cli.svg
   :target: https://pypi.python.org/pypi/phome-assistant-cli
   :alt: PyPI release

