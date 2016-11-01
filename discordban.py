#
# DiscordB3 (www.namelessnoobs.com)
# Copyright (C) 2016 st0rm
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#Credits 
#Fenix the orginal author of the irc b3 bot which this plugin is based on.
#Mordecaii from iG for his lovely discordPush fuction <3.

__author__ = 'Fenix, st0rm, Mordecaii'
__version__ = '1.0'

import b3
import b3.plugin
import b3.events
import urllib
import re
import datetime, time
import urllib2
import json

from b3.functions import getCmd
from b3.functions import minutesStr
from ConfigParser import NoSectionError
from threading import Thread


class DiscordbanPlugin(b3.plugin.Plugin):

    ####################################################################################################################
    #                                                                                                                  #
    #   PLUGIN INIT                                                                                                    #
    #                                                                                                                  #
    ####################################################################################################################

    def __init__(self, console, config=None):
        """
        Build the plugin object.
        :param console: The parser instance.
        :param config: The plugin configuration object instance.
        """
        b3.plugin.Plugin.__init__(self, console, config)
        self.adminPlugin = self.console.getPlugin('admin')
        if not self.adminPlugin:
            raise AttributeError('could not start without admin plugin')

    def onLoadConfig(self):
        """
        Load plugin configuration.
        """
        self._discordWebhookUrl = self.config.get('authentication','webhookUrl')
        self._serverName = self.config.get('authentication','hostname')

    def onStartup(self):
        """
        Initialize plugin settings.
        """

        # register necessary events
        self.registerEvent(self.console.getEventID('EVT_CLIENT_BAN'), self.onBan)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_BAN_TEMP'), self.onBan)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_KICK'), self.onKick)

        # notice plugin started
        self.debug('plugin started')

    ####################################################################################################################
    #                                                                                                                  #
    #   EVENTS                                                                                                         #
    #                                                                                                                  #
    ####################################################################################################################

    def onBan(self, event):
        """
        Perform operations when EVT_CLIENT_BAN or EVT_CLIENT_BAN_TEMP is received.
        :param event: An EVT_CLIENT_BAN or and EVT_CLIENT_BAN_TEMP event.
        """
        admin = event.data['admin']
        client = event.client
        reason = event.data['reason']
        message = '[B3 BAN] Server: `%s` Admin: `%s` Banned `%s`' % (self._serverName, admin.name, client.name)

        if reason:
            # if there is a reason attached to the ban, append it to the notice
            message += ' Reason : `%s`' % (self.console.stripColors(reason))

        duration = 'permanent'
        if 'duration' in event.data:
            # if there is a duration convert it
            duration = minutesStr(event.data['duration'])

        # append the duration to the ban notice
        message += ' [duration : `%s`]' % (duration)
        self.discordPush(message)

    def onKick(self, event):
        """
        Perform operations when EVT_CLIENT_KICK is received.
        :param event: An EVT_CLIENT_KICK event.
        """
        admin = event.data['admin']
        client = event.client
        reason = event.data['reason']
        message = '[B3 KICK] Server: `%s` Admin: `%s` Kicked `%s`' % (self._serverName, admin.name, client.name)

        if reason:
            message += ' Reason : `%s`' % (self.console.stripColors(reason))
        self.discordPush(message)

    def discordPush(self, message):
        """
        Send message to discord bot yay.
        """
	
        data = json.dumps({"content": message})
        req = urllib2.Request(self._discordWebhookUrl, data, {'Content-Type': 'application/json', "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"})
        try:
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
        except urllib2.HTTPError:
            print "Cannot push data to Discord. is your webhook url right?"
            pass
