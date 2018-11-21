Home Assistant Command-line Interface (``hass-cli``)
====================================================

|Chat Status| |License| |PyPI|

The Home Assistant Command-line interface (``hass-cli``) allows one to
work with a local or a remote `Home Assistant <https://home-assistant.io>`_
instance directly from the command-line.

Examples:

Get state of a entity:

.. code:: bash

    $ hass-cli get state sensor
    hass-cli  get state light.guestroom_light                                                                                                                                                                       ◼
    {
      "attributes": {
        "friendly_name": "Guestroom Light",
        "is_deconz_group": false,
        "supported_features": 61
      },
      "context": {
      "id": "e257a0f15fe74579b4a693de65ed618b",
      "user_id": "4c7c32b2934f4deeb346bf8017e2bf28"
      },
    "entity_id": "light.guestroom_light",
    "last_changed": "2018-11-18T21:48:20.279802+00:00",
    "last_updated": "2018-11-18T21:48:20.279802+00:00",
    "state": "off"
    }


If you prefer yaml you can do:

.. code:: bash
  
  $ hass-cli -o yaml get state light.guestroom_light
  attributes:
    friendly_name: Guestroom Light
    is_deconz_group: false
    supported_features: 61
  context:
    id: e257a0f15fe74579b4a693de65ed618b
    user_id: 4c7c32b2934f4deeb346bf8017e2bf28
  entity_id: light.guestroom_light
  last_changed: '2018-11-18T21:48:20.279802+00:00'
  last_updated: '2018-11-18T21:48:20.279802+00:00'
  state: 'off'
..

You can edit state via an editor:

.. code:: bash
  
    $ hass-cli edit state light.guestroom_light
..

This will open the current state in your favorite editor and any changes you save will
be used for an update. 

You can also explicitly create/edit via the `--json` flag:

.. code:: bash

  $ hass-cli edit state sensor.test --json='{ "state":"off"}'
..

Auto-completion
###############

For zsh:

.. code:: bash

  eval "$(_HASS_CLI_COMPLETE=source_zsh hass-cli)"
..

For bash:

.. code:: bash

  eval "$(_FOO_BAR_COMPLETE=source foo-bar)"
..

Once enable there is autocompletion for commands and for certain attributes like entities:

.. code:: bash

  $ hass-cli get state light.<TAB>                                                                                                                                                                    ⏎ ✱ ◼
  light.kitchen_light_5          light.office_light             light.basement_light_4         light.basement_light_9         light.dinner_table_light_4     light.winter_garden_light_2    light.kitchen_light_2
  light.kitchen_table_light_1    light.hallroom_light_2         light.basement_light_5         light.basement_light_10        light.dinner_table_wall_light  light.winter_garden_light_4    light.kitchen_table_light_2
  light.kitchen_light_1          light.hallroom_light_1         light.basement_light_6         light.small_bathroom_light     light.dinner_table_light_5     light.winter_garden_light_3    light.kitchen_light_4
  light.kitchen_light_6          light.basement_light_1         light.basement_light_7         light.dinner_table_light_1     light.dinner_table_light_6     light.hallroom_light_4
  light.guestroom_light          light.basement_light_stairs    light.basement_light_2         light.hallroom_light_5         light.dinner_table_light_3     light.winter_garden_light_5
  light.hallroom_light_3         light.basement_light_3         light.basement_light_8         light.dinner_table_light_2     light.winter_garden_light_1    light.kitchen_light_3

..

Note: For this to work you'll need to have setup the following environment variables if your home-assistant
is secured and not running on localhost:8123:

.. code:: bash
 
   export HASS_SERVER=https://hassio.local:8123
   export HASS_TOKEN=<Bearer token from HASS_SERVER/profile>

..

help
####

.. code:: bash

  Usage: hass-cli [OPTIONS] COMMAND [ARGS]...

    A command line interface for Home Assistant.

  Options:
    --version                 Show the version and exit.
    -s, --server TEXT         The server URL of Home Assistant instance.
                              [default: http://localhost:8123]
    --token TEXT              The Bearer token for Home Assistant instance.
    --timeout INTEGER         Timeout for network operations.
    -o, --output [json|yaml]  Output format  [default: json]
    -v, --verbose             Enables verbose mode.
    --help                    Show this message and exit.

  Commands:
    discover  Discovery for the local network.
    edit      list info from Home Assistant
    get       list info from Home Assistant
    info      Get basic info from Home Assistant using /api/discovery_info.
    raw       call raw api (advanced)
    toggle    toggle data from Home Assistant

Clone the git repository and 

.. code:: bash

    $ pip3 install --editable .



Development
###########

Developing is (re)using as much as possible from `homeassistant development setup <https://developers.home-assistant.io/docs/en/development_environment.html>`.

Recommended way to develop is to use virtual environment to ensure isolation from rest of your system using the following steps:

.. code:: bash

    $ python3 -m venv .
    $ source bin/activate
    $ script/setup


after this you should be able to edit the source code and running `hass-cli` directly:

.. code:: bash

    $ hass-cli 


.. |Chat Status| image:: https://img.shields.io/discord/330944238910963714.svg
   :target: https://discord.gg/c5DvZ4e
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/home-assistant/home-assistant-cli/blob/master/LICENSE
   :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/home-assistant-cli.svg
   :target: https://pypi.python.org/pypi/home-assistant-cli
   :alt: PyPI release
