# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The ios ntp_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ntp_global import (
    Ntp_globalTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ntp_global.ntp_global import (
    Ntp_globalArgs,
)


class Ntp_globalFacts(object):
    """ The ios ntp_global facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ntp_globalArgs.argument_spec

    def get_ntp_data(self, connection):
        return connection.get("show running-config | section ^ntp")
        # return "ntp server 10.0.2.10 version 2\nntp server ipv6 ceeck.com\nntp source GigabitEthernet0/1\nntp server 10.0.2.15 source GigabitEthernet0/1\nntp access-group ipv4 peer DHCP-Server kod\nntp access-group ipv6 peer preauth_ipv6_acl kod\nntp access-group peer 2 kod\nntp access-group query-only 10\nntp allow mode control 4\nntp allow mode private\nntp authenticate\nntp authentication-key 2 md5 wew 22\nntp broadcastdelay 22\nntp clock-period 5\nntp logging\nntp master 4\nntp max-associations 34\nntp maxdistance 3\nntp mindistance 10\nntp orphan 4\nntp panic update\nntp trusted-key 3 - 3\nntp trusted-key 21 - 41\nntp peer 10.0.2.10 version 2\nntp peer 10.0.2.11 key 2 minpoll 5 prefer version 2\nntp peer ip abc.com prefer\nntp peer ipv6 ipv6abc.com\nntp peer ipv6 avipv6.com prefer"

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Ntp_global network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_ntp_data(connection)

        # parse native config using the Ntp_global template
        ntp_global_parser = Ntp_globalTemplate(
            lines=data.splitlines(), module=self._module
        )
        objs = ntp_global_parser.parse()

        ansible_facts["ansible_network_resources"].pop("ntp_global", None)

        params = utils.remove_empties(
            ntp_global_parser.validate_config(
                self.argument_spec, {"config": objs}, redact=True
            )
        )

        facts["ntp_global"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
