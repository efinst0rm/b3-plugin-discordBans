Discord BOT Plugin for BigBrotherBot [![BigBrotherBot](http://i.imgur.com/7sljo4G.png)][B3]
================================

Description
-----------

A [BigBrotherBot][B3] plugin which allows you to see kicks, bans and temp bans in your discord server.

Download
--------

Latest version available [here](https://github.com/efinst0rm/B3DiscordPlugin/archive/master.zip).

Requirements
------------

In order for this plugin to work you need to have B3 *v1.10.11 * installed (or greater).

Installation
------------

* copy the `discord.py` folder into `b3/extplugins`
* add to the `plugins` section of your `b3.xml` config file:

  ```xml
  <plugin name="discord" config="@b3/extplugins/conf/plugin_discord.xml" />
  ```
* you will need a discord web hook url [info](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

B3 events
---------

The plugin make use of the folowing events to display notices in the dicord channel:

* `EVT_CLIENT_BAN` and `EVT_CLIENT_BAN_TEMP` : send a notice upon admin bans
* `EVT_CLIENT_KICK` : send a notice upon admin kicks

Support
-------

If you have found a bug, please report it on [Discord].

[Discord]: https://discordapp.com/invite/AwPd37D
