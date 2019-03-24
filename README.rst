Home Assistant Command-line Interface (``hass-cli``)
====================================================

|Build Status| |Coverage| |Chat Status| |License| |PyPI|

The Home Assistant Command-line interface (``hass-cli``) allows one to
work with a local or a remote `Home Assistant <https://home-assistant.io>`_
instance directly from the command-line.

.. image:: https://asciinema.org/a/216235.png
      :alt: hass-cli screencast
      :target: https://asciinema.org/a/216235?autoplay=1&speed=1


**Note**: This is still in alpha and under heavy development. Name and
structure of commands are expected to still change.

Installation
============

To use latest release:

.. code:: bash

    $ pip install homeassistant-cli

To use latest pre-release from ``dev`` branch:

.. code:: bash

   $ pip install git+https://github.com/home-assistant/home-assistant-cli@dev

To use homebrew on Mac OSX:

.. code:: bash

   $ brew install homeassistant-cli

Docker
-------

If you do not have a Python setup you can try use ``hass-cli`` via a container using Docker.

.. code:: bash

   $ docker run homeassistant/home-assistant-cli


To make auto-completion and access environment work like other scripts you'll need to
create a script file to execute.

.. code:: bash

   $ curl https://raw.githubusercontent.com/home-assistant/home-assistant-cli/master/docker-hass-cli > hass-cli
   $ chmod +x hass-cli


Now put the ``hass-cli`` script into your path and you can use it like if you had installed it via
command line as long as you don't need file system access (like for ``hass-cli template``).

Setup
======

To get started you'll need to have or generate a long lasting token format
on your Home Assistant profile page (i.e. https://localhost:8123/profile).

Then you can use ``--server`` and ``--token`` paremeter on each call or as is
recommended setup ``HASS_SERVER`` and ``HASS_TOKEN`` environment variables.

.. code:: bash

    $ export HASS_SERVER=https://hassio.local:8123
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

   $ hass-cli  info
     BASE_URL                   LOCATION         REQUIRES_API_PASWORD  VERSION
     https://hassio.local:8123  Fort of Solitude False                 0.86.2

If you prefer yaml you can use ``--output=yaml``:

.. code:: bash

    $ hass-cli --output yaml info
      base_url: https://hassio.local:8123
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
    group.kitchen_lights                                       Kitchen Lights                                  off
    binary_sensor.presence_basement_combined                   Basement Motion Anywhere                        off
    sensor.yr_symbol                                           yr Symbol                                       4
    group.basement_lights                                      Basement Lights                                 unknown
    sensor.packages_delivered                                  Packages Delivered                              1
    sensor.packages_in_transit                                 Packages In Transit                             1
    sensor.ring_front_door_last_ding                           Front Door Last Ding                            14:08
    sensor.ring_front_door_battery                             Front Door Battery                              52
    ...


You can use ``--no-headers`` to suppress the header.

``--table-format`` let you select which table format you want. Default is ``simple`` but
you can use any of the formats supported by https://pypi.org/project/tabulate/:
``plain``, ``simple``, ``github``, ``grid``, ``fancy_grid``, ``pipe``, ``orgtbl``, ``rst``, ``mediawiki``, ``html``, ``latex``, ``latex_raw``, ``latex_booktabs`` or ``tsv``

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

This will open the current state in your favorite editor and any changes you save will
be used for an update.

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

Note: the `--sort-by` argument is referring to the attribute in the underlying ``json``/``yaml``
NOT the column name. The advantage for this is that it can be used for sorting on any property
even if not included in the default output.

Areas and Device Registry
-------------------------

Since v0.87 of Home Assistant there is a notion of Areas in the Device registry. hass-cli lets
you list devices and areas and assign areas to devices.

Listing devices and areas works similar to list Entities.

.. code:: bash

   $ hass-cli device list
   ID                                NAME                           MODEL                            MANUFACTURER        AREA
   a3852c3c3ebd47d3acac195478ca6f8b  Basement stairs motion         SML001                           Philips             c6c962b892064a218e968fcaee7950c8
   880a944e74db4bb48ea3db6dd24af357  Basement Light 2               TRADFRI bulb GU10 WS 400lm       IKEA of Sweden      c6c962b892064a218e968fcaee7950c8
   657c3cc908594479aab819ff80d0c710  Office                         Hue white lamp                   Philips             None
   ee62c3af815f4ec89994977a730782a0  Kids room main                 Hue color lamp                   Philips             69fdd00e91614957980a8dc1a7f0f68a
   4637186392b84c1a843f64c810f04bbe  Dinner table 4                 Hue ambiance candle              Philips             81c28de473dd41a7846fc97fdcd3027b
   90f8944476e544348e6691bc0d3cc855  Bedroom                        Play:1                           Sonos               None
   e20132e0f90942298bdae2340e61c079  Kitchen Light 6                LCT003                           Philips             e6ebd3e6f6e04b63a0e4a109b4748584
   9ea61cecaf8d4de08aa20306ec6bdd07  Winter Garden Light 3          LCT012                           Philips             9e08d89203804d5db995c3d0d5dbd91b
   93cc3e42be224ef6b192ce203f6bf7fe  Dinner table 3                 Hue ambiance candle              Philips             81c28de473dd41a7846fc97fdcd3027b
   ae8b84e99dbf4a9e94072a1588f29298  Kitchen Motion                 SML001                           Philips             e6ebd3e6f6e04b63a0e4a109b4748584

   $ hass-cli area list
   ID                                NAME
   295afc88012341ecb897cd12d3fbc6b4  Bathroom
   9e08d89203804d5db995c3d0d5dbd91b  Winter Garden
   8816ee92b7b84f54bbb30a68b877e739  Office
   e6ebd3e6f6e04b63a0e4a109b4748584  Kitchen
   f7f5412a9f47436da669a537e0c0c10f  Livingroom
   bc98c209249f452f8d074e8384780e15  Hallway
   5f8de5b8cf264c17b10d21e741573713  Small Bathroom
   c6c962b892064a218e968fcaee7950c8  Basement
   efaa42ae0b7645aebfa51d8303c361c5  Loft
   ea63e86747104abdb26f6d6ea9d2ddef  Old Shed
   16bd0505030a430b91fcf331340090f8  Entrance
   81c28de473dd41a7846fc97fdcd3027b  Dinner Table
   69fdd00e91614957980a8dc1a7f0f68a  Kids room  


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
  light.kitchen_light_6          light.basement_light_1         light.basement_light_7         light.dinner_table_light_1     light.dinner_table_light_6     light.hallroom_light_4
  light.guestroom_light          light.basement_light_stairs    light.basement_light_2         light.hallroom_light_5         light.dinner_table_light_3     light.winter_garden_light_5
  light.hallroom_light_3         light.basement_light_3         light.basement_light_8         light.dinner_table_light_2     light.winter_garden_light_1    light.kitchen_light_3


Note: For this to work you'll need to have setup the following environment variables if your home-assistant
is secured and not running on localhost:8123:

.. code:: bash

   export HASS_SERVER=https://hassio.local:8123
   export HASS_TOKEN=<Bearer token from HASS_SERVER/profile>


Help
####

.. code:: bash

   Usage: hass-cli [OPTIONS] COMMAND [ARGS]...

     Command line interface for Home Assistant.

   Options:
     -l, --loglevel LVL              Either CRITICAL, ERROR, WARNING, INFO or
                                     DEBUG
     --version                       Show the version and exit.
     -s, --server TEXT               The server URL or `auto` for automatic
                                     detection  [default: auto]
     --token TEXT                    The Bearer token for Home Assistant
                                     instance.
     --password TEXT                 The API password for Home Assistant
                                     instance.
     --timeout INTEGER               Timeout for network operations.  [default:
                                     5]
     -o, --output [json|yaml|table|auto]
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
                                     ENTITY=entity_name,
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
     state       Get info and operate on entities from Home Assistant.
     event       Interact with events.
     info        Get basic info from Home Assistant.
     map         Print the current location on a map.
     raw         Call the raw API (advanced).
     service     Call and work with services.
     system      System details and operations for Home Assistant.
     template    Render templates on server or locally.


Clone the git repository and

.. code:: bash

    $ pip3 install --editable .



Development
###########

Developing is (re)using as much as possible from [Home Assistant development setup](https://developers.home-assistant.io/docs/en/development_environment.html).

Recommended way to develop is to use virtual environment to ensure isolation from rest of your system using the following steps:

Clone the git repository and do the following:

.. code:: bash

    $ python3 -m venv .
    $ source bin/activate
    $ script/setup


after this you should be able to edit the source code and running `hass-cli` directly:

.. code:: bash

    $ hass-cli


.. |Build Status| image:: https://travis-ci.com/home-assistant/home-assistant-cli.svg?branch=dev
    :target: https://travis-ci.com/home-assistant/home-assistant-cli

.. |Chat Status| image:: https://img.shields.io/discord/330944238910963714.svg
   :target: https://discord.gg/c5DvZ4e
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
