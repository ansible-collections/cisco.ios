# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios evpn_ethernet fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.evpn_ethernet.evpn_ethernet import (
    Evpn_ethernetArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.evpn_ethernet import (
    Evpn_ethernetTemplate,
)


class Evpn_ethernetFacts(object):
    """The ios evpn_ethernet facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Evpn_ethernetArgs.argument_spec

    def get_evpn_ethernet_segment_data(self, connection):
        return connection.get("show running-config | section ^l2vpn evpn ethernet-segment")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Evpn_ethernet network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_evpn_ethernet_segment_data(connection)

        # parse native config using the Evpn_ethernet template
        evpn_ethernet_parser = Evpn_ethernetTemplate(lines=data.splitlines(), module=self._module)
        objs = list(evpn_ethernet_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("evpn_ethernet", None)

        params = utils.remove_empties(
            evpn_ethernet_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["evpn_ethernet"] = params.get("config")
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
