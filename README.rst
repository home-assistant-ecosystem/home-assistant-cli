Home Assistant Command-line Interface (``hass-cli``)
====================================================

|Coverage| |License| |PyPI|

The Home Assistant Command-line interface (``hass-cli``) allows one to
work with a local or a remote `Home Assistant <https://home-assistant.io>`_
Core or Home Assistant (former Hass.io) instance directly from the command-line.

.. image:: https://asciinema.org/a/216235.png
      :alt: hass-cli screencast
      :target: https://asciinema.org/a/216235?autoplay=1&speed=1


Installation
============

To use latest release:

.. code:: bash

    $ pip install homeassistant-cli

To use latest pre-release from ``dev`` branch:

.. code:: bash

   $ pip install git+https://github.com/home-assistant/home-assistant-cli@dev

The developers of `hass-cli` usually provide up-to-date `packages <https://src.fedoraproject.org/rpms/home-assistant-cli>`_ for recent Fedora and EPEL releases. Use ``dnf`` for the installation:

.. code:: bash

   $ sudo  dnf -y install home-assistant-cli

The community is providing support for macOS through `homebew <https://formulae.brew.sh/formula/homeassistant-cli#default>`_.

.. code:: bash

   $ brew install homeassistant-cli

Keep in mind that the available releases in the distribution could be out-dated.

``home-assistant-cli`` is also available for NixOS.

To use the tool on NixOS. Keep in mind that the latest release could only
be available in the ``unstable`` channel.

.. code:: bash

   $ nix-env -iA nixos.home-assistant-cli

Docker
-------

If you do not have a Python setup you can try use ``hass-cli`` via a container
using Docker.

.. code:: bash

   $ docker run homeassistant/home-assistant-cli


To make auto-completion and access environment work like other scripts you'll
need to create a script file to execute.

.. code:: bash

   $ curl https://raw.githubusercontent.com/home-assistant/home-assistant-cli/master/docker-hass-cli > hass-cli
   $ chmod +x hass-cli


Now put the ``hass-cli`` script into your path and you can use it like if you
had installed it via command line as long as you don't need file system access
(like for ``hass-cli template``).

Setup
======

To get started you'll need to have or generate a long lasting token format
on your Home Assistant profile page (i.e. https://localhost:8123/profile
then scroll down to "Long-Lived Access Tokens").

Then you can use ``--server`` and ``--token`` parameter on each call or as is
recommended setup ``HASS_SERVER`` and ``HASS_TOKEN`` environment variables.

.. code:: bash

    $ export HASS_SERVER=https://homeassistant.local:8123
    $ export HASS_TOKEN=<secret>

Once that is enabled and you are using either ``zsh`` or ``bash`` run
the following to enable autocompletion for ``hass-cli`` commands.

.. code:: bash

  $  source <(hass-cli completion zsh)


Usage
=======

Note: Below is listed **some** of the features, make sure to use ``--help`` and
autocompletion to learn more of the features as they become available.

Most commands returns a table version of what the Home Assistant API returns.
For example to get basic info about your Home Assistant server you use ``info``:

.. code:: bash

   $ hass-cli info
     BASE_URL                           LOCATION         REQUIRES_API_PASWORD  VERSION
     https://home-assistant.local:8123  Fort of Solitude False                 0.86.2

If you prefer yaml you can use ``--output=yaml``:

.. code:: bash

    $ hass-cli --output yaml info
      base_url: https://home-assistant.local:8123
      location_name: Wayne Manor
      requires_api_password: false
      version: 0.86.2

To get list of states you use `state list`:

.. code:: bash

    $ hass-cli state list
    ENTITY                                                     DESCRIPTION                                     STATE
    zone.school                                                School                                          zoning
    zone.home                                                  Andersens                                       zoning
    sun.sun                                                    Sun                                             below_horizon
    camera.babymonitor                                         babymonitor                                     idle
    timer.timer_office_lights                                                                                  idle
    timer.timer_small_bathroom                                                                                 idle
    [...]


You can use ``--no-headers`` to suppress the header.

``--table-format`` let you select which table format you want. Default is
``simple`` but you can use any of the formats supported by https://pypi.org/project/tabulate/:
``plain``, ``simple``, ``github``, ``grid``, ``fancy_grid``, ``pipe``,
``orgtbl``, ``rst``, ``mediawiki``, ``html``, ``latex``, ``latex_raw``,
``latex_booktabs`` or ``tsv``

Finally, you can also via ``--columns`` control which data you want shown.
Each column has a name and a jsonpath. The default setup for entities are:

``--columns=ENTITY=entity_id,DESCRIPTION=attributes.friendly_name,STATE=state,CHANGED=last_changed``

If you for example just wanted the name and all attributes you could do:

.. code:: bash

   $ hass-cli --columns=ENTITY="entity_id,ATTRIBUTES=attributes[*]" state list zone
   ENTITY             ATTRIBUTES
   zone.school        {'friendly_name': 'School', 'hidden': True, 'icon': 'mdi:school', 'latitude': 7.011023, 'longitude': 16.858151, 'radius': 50.0}
   zone.unnamed_zone  {'friendly_name': 'Unnamed zone', 'hidden': True, 'icon': 'mdi:home', 'latitude': 37.006476, 'longitude': 2.861699, 'radius': 50.0}
   zone.home          {'friendly_name': 'Andersens', 'hidden': True, 'icon': 'mdi:home', 'latitude': 27.006476, 'longitude': 7.861699, 'radius': 100}

You can get more details about a state by using ``yaml`` or ``json`` output
format. In this example we use the shorthand of output: ``-o``:

.. code:: bash

    $ hass-cli -o yaml state get light.guestroom_light                                                                                                                                                                       ◼
    attributes:
      friendly_name: Guestroom Light
      supported_features: 61
    context:
      id: 84d52fe306ec4895948b546b492702a4
      user_id: null
    entity_id: light.guestroom_light
    last_changed: '2018-12-10T18:33:51.883238+00:00'
    last_updated: '2018-12-10T18:33:51.883238+00:00'
    state: 'off'

You can edit state via an editor:

.. code:: bash

    $ hass-cli state edit light.guestroom_light

This will open the current state in your favorite editor and any changes you
save will be used for an update.

You can also explicitly create/edit via the ``--json`` flag:

.. code:: bash

  $ hass-cli state edit sensor.test --json='{ "state":"off"}'

List possible services with or without a regular expression filter:

.. code:: bash

    $ hass-cli service list 'home.*toggle'
      DOMAIN         SERVICE    DESCRIPTION
      homeassistant  toggle     Generic service to toggle devices on/off...

For more details the YAML format is useful:

.. code:: bash

    $ hass-cli -o yaml service list homeassistant.toggle
    homeassistant:
      services:
        toggle:
          description: Generic service to toggle devices on/off under any domain. Same
            usage as the light.turn_on, switch.turn_on, etc. services.
          fields:
            entity_id:
              description: The entity_id of the device to toggle on/off.
              example: light.living_room

You can get history about one or more entities, here getting state changes for the last
50 minutes:

.. code:: bash

   $ hass-cli state history --since 50m light.kitchen_light_1 binary_sensor.presence_kitchen
     ENTITY                          DESCRIPTION      STATE    CHANGED
     binary_sensor.presence_kitchen  Kitchen Motion   off      2019-01-27T23:19:55.322474+00:00
     binary_sensor.presence_kitchen  Kitchen Motion   on       2019-01-27T23:21:44.015071+00:00
     binary_sensor.presence_kitchen  Kitchen Motion   off      2019-01-27T23:22:02.330566+00:00
     light.kitchen_light_1           Kitchen Light 1  on       2019-01-27T23:19:55.322474+00:00
     light.kitchen_light_1           Kitchen Light 1  off      2019-01-27T23:36:45.254266+00:00

The data is sorted by default as Home Assistant returns it, thus for history it is useful
to sort by a property:

.. code:: bash

   $ hass-cli --sort-by last_changed state history --since 50m  light.kitchen_light_1 binary_sensor.presence_kitchen
   ENTITY                          DESCRIPTION      STATE    CHANGED
   binary_sensor.presence_kitchen  Kitchen Motion   off      2019-01-27T23:18:00.717611+00:00
   light.kitchen_light_1           Kitchen Light 1  on       2019-01-27T23:18:00.717611+00:00
   binary_sensor.presence_kitchen  Kitchen Motion   on       2019-01-27T23:18:12.135015+00:00
   binary_sensor.presence_kitchen  Kitchen Motion   off      2019-01-27T23:18:30.417064+00:00
   light.kitchen_light_1           Kitchen Light 1  off      2019-01-27T23:36:45.254266+00:00

Note: the `--sort-by` argument is referring to the attribute in the underlying
``json``/``yaml`` NOT the column name. The advantage for this is that it can
be used for sorting on any property even if not included in the default output.

Areas and Device Registry
-------------------------

Since v0.87 of Home Assistant there is a notion of Areas in the Device registry. ``hass-cli`` lets
you list devices and areas and assign areas to devices.

Listing devices and areas works similar to list Entities.

.. code:: bash

   $ hass-cli device list
   ID                                NAME                           MODEL                            MANUFACTURER        AREA
   a3852c3c3ebd47d3acac195478ca6f8b  Basement stairs motion         SML001                           Philips             c6c962b892064a218e968fcaee7950c8
   880a944e74db4bb48ea3db6dd24af357  Basement Light 2               TRADFRI bulb GU10 WS 400lm       IKEA of Sweden      c6c962b892064a218e968fcaee7950c8
   657c3cc908594479aab819ff80d0c710  Office                         Hue white lamp                   Philips             None
   [...]

   $ hass-cli area list
   ID                                NAME
   295afc88012341ecb897cd12d3fbc6b4  Bathroom
   9e08d89203804d5db995c3d0d5dbd91b  Winter Garden
   8816ee92b7b84f54bbb30a68b877e739  Office
   [...]


You can create and delete areas:

.. code:: bash

   $ hass-cli area delete "Old Shed"
   -  id: 1
      type: result
      success: true
      result: success

   $ hass-cli area create "New Shed"
   -  id: 1
      type: result
      success: true
      result:
          area_id: cdd09a80f03a4cc59d2943053c0414c0
          name: New Shed

You can assign area to a specific device. Here the Kitchen
area gets assigned to device named "Cupboard Light".

.. code:: bash

   $ hass-cli device assign Kitchen "Cupboard Light"

Besides assigning individual devices you can assign in bulk:

.. code:: bash

   $ hass-cli device assign Kitchen --match "Kitchen Light"

The above line will assign Kitchen area to all devices with substring "Kitchen Light".

You can also combine individual and matched devices in one line:

.. code:: bash

   $ hass-cli device assign Kitchen --match "Kitchen Light" eab9930f8652408882cc8cb604651c60 Cupboard

Above will assign area named "Kitchen" to all devices having substring "Kitchen Light" and to
specific area with id "eab9930..." or named "Cupboard".

Events
------

You can subscribe and watch all or a specific event type using ``event watch``.

.. code:: bash

   $ hass-cli event watch

This will watch for all event types, you can limit to a specific event type
by specifying it as an argument:

.. code:: bash

   $ hass-cli event watch deconz_event


Home Assistant (former Hass.io)
-------------------------------

If you are using Home Assistant (former Hass.io) there are commands available
for you to interact with Home Assistant services/systems. This includes the
underlying services like the supervisor.

Check the Supervisor release you are running:

.. code:: bash

   $ hass-cli ha supervisor info
   result: ok
   data:
    version: '217'
    version_latest: '217'
    channel: stable
    [...]

Check the Core release you are using at the moment:

.. code:: bash

   $ hass-cli ha core info
   result: ok
   data:
       version: 0.108.2
       version_latest: 0.108.3
       [...]

Update Core to the latest available release:

.. code:: bash

   $ hass-cli ha core update


Other
-----

You can call services:

.. code:: bash

    $ hass-cli service call deconz.device_refresh

With arguments:

.. code:: bash

    $ hass-cli service call homeassistant.toggle --arguments entity_id=light.office_light


Open a map for your Home Assistant location:

.. code:: bash

    $ hass-cli map

Render templates server side:

.. code:: bash

    $ hass-cli template motionlight.yaml.j2 motiondata.yaml

Render templates client (local) side:

.. code:: bash

    $ hass-cli template --local lovelace-template.yaml


Auto-completion
###############

As described above you can use ``source <(hass-cli completion zsh)`` to
quickly and easy enable auto completion. If you do it from your ``.bashrc``
or ``.zshrc`` it's recommend to use the form below as that does not trigger
a run of ``hass-cli`` itself.

For zsh:

.. code:: bash

  eval "$(_HASS_CLI_COMPLETE=source_zsh hass-cli)"


For bash:

.. code:: bash

  eval "$(_HASS_CLI_COMPLETE=source hass-cli)"


Once enabled there is autocompletion for commands and for certain attributes like entities:

.. code:: bash

  $ hass-cli state get light.<TAB>                                                                                                                                                                    ⏎ ✱ ◼
  light.kitchen_light_5          light.office_light             light.basement_light_4         light.basement_light_9         light.dinner_table_light_4     light.winter_garden_light_2    light.kitchen_light_2
  light.kitchen_table_light_1    light.hallroom_light_2         light.basement_light_5         light.basement_light_10        light.dinner_table_wall_light  light.winter_garden_light_4    light.kitchen_table_light_2
  light.kitchen_light_1          light.hallroom_light_1         light.basement_light_6         light.small_bathroom_light     light.dinner_table_light_5     light.winter_garden_light_3    light.kitchen_light_4
  [...]


Note: For this to work you'll need to have setup the following environment
variables if your Home Assistant installation is secured and not running on
localhost:8123:

.. code:: bash

   export HASS_SERVER=http://homeassistant.local:8123
   export HASS_TOKEN=eyJ0eXAiO-----------------------ed8mj0NP8


Help
####

.. code:: bash

    $ hass-cli
    Usage: hass-cli [OPTIONS] COMMAND [ARGS]...

      Command line interface for Home Assistant.

    Options:
      -l, --loglevel LVL              Either CRITICAL, ERROR, WARNING, INFO or
                                      DEBUG
      --version                       Show the version and exit.
      -s, --server TEXT               The server URL or `auto` for automatic
                                      detection. Can also be set with the
                                      environment variable HASS_SERVER.  [default:
                                      auto]
      --token TEXT                    The Bearer token for Home Assistant
                                      instance. Can also be set with the
                                      environment variable HASS_TOKEN.
      --password TEXT                 The API password for Home Assistant
                                      instance. Can also be set with the
                                      environment variable HASS_PASSWORD.
      --timeout INTEGER               Timeout for network operations.  [default:
                                      5]
      -o, --output [json|yaml|table|ndjson|auto]
                                      Output format.  [default: auto]
      -v, --verbose                   Enables verbose mode.
      -x                              Print backtraces when exception occurs.
      --cert TEXT                     Path to client certificate file (.pem) to
                                      use when connecting.
      --insecure                      Ignore SSL Certificates. Allow to connect to
                                      servers with self-signed certificates. Be
                                      careful!
      --debug                         Enables debug mode.
      --columns TEXT                  Custom columns key=value list. Example:
                                      ENTITY=entity_id,
                                      NAME=attributes.friendly_name
      --no-headers                    When printing tables don't use headers
                                      (default: print headers)
      --table-format TEXT             Which table format to use.
      --sort-by TEXT                  Sort table by the jsonpath expression.
                                      Example: last_changed
      --version                       Show the version and exit.
      --help                          Show this message and exit.

    Commands:
      area        Get info and operate on areas from Home Assistant...
      completion  Output shell completion code for the specified shell (bash or...
      config      Get configuration from a Home Assistant instance.
      device      Get info and operate on devices from Home Assistant...
      discover    Discovery for the local network.
      entity      Get info on entities from Home Assistant.
      event       Interact with events.
      ha          Home Assistant (former Hass.io) commands.
      info        Get basic info from Home Assistant.
      map         Show the location of the config or an entity on a map.
      raw         Call the raw API (advanced).
      service     Call and work with services.
      state       Get info on entity state from Home Assistant.
      system      System details and operations for Home Assistant.
      template    Render templates on server or locally.


Clone the git repository and

.. code:: bash

    $ pip3 install --editable .



Development
###########

Developing is (re)using as much as possible from
[Home Assistant development setup](https://developers.home-assistant.io/docs/en/development_environment.html).

Recommended way to develop is to use virtual environment to ensure isolation
from rest of your system using the following steps:

Clone the git repository and do the following:

.. code:: bash

    $ python3 -m venv .
    $ source bin/activate
    $ script/setup


after this you should be able to edit the source code and running ``hass-cli``
directly:

.. code:: bash

    $ hass-cli

.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/home-assistant/home-assistant-cli/blob/master/LICENSE
   :alt: License
.. |PyPI| image:: https://img.shields.io/pypi/v/homeassistant_cli.svg
   :target: https://pypi.org/project/homeassistant_cli/
   :alt: PyPI release
.. |Coverage| image:: https://coveralls.io/repos/github/home-assistant/home-assistant-cli/badge.svg?branch=dev
    :target: https://coveralls.io/github/home-assistant/home-assistant-cli?branch=dev
    :alt: Coveralls
.. |Docker| image:: https://img.shields.io/docker/pulls/homeassistant/home-assistant-cli.svg?style=flat
    :target: https://hub.docker.com/r/homeassistant/home-assistant-cli
    :alt: Docker
