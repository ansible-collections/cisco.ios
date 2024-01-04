# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios vlan_configurations fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlan_configurations.vlan_configurations import (
    Vlan_configurationsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vlan_configurations import (
    Vlan_configurationsTemplate,
)
<<<<<<< Updated upstream:plugins/module_utils/network/ios/facts/vlan_configuration/vlan_configuration.py
=======
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.vlan_configurations.vlan_configurations import (
    Vlan_configurationsArgs,
)
from textwrap import dedent
>>>>>>> Stashed changes:plugins/module_utils/network/ios/facts/vlan_configurations/vlan_configurations.py


class Vlan_configurationsFacts(object):
    """The ios vlan_configurations facts class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = Vlan_configurationsArgs.argument_spec

    def get_vlan_conf_data(self, connection):
        return dedent(
            """\
            vlan configuration 101
             member evpn-instance 101 vni 10101
            vlan configuration 102
             member evpn-instance 102 vni 10102
            vlan configuration 201
             member evpn-instance 201 vni 10201
            vlan configuration 202
             member evpn-instance 202 vni 10202
            vlan configuration 901
             member vni 50901
            vlan configuration 902
             member vni 50902
            """,
        )
        return connection.get("show running-config | sec ^vlan configuration .+")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vlan_configurations network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_vlan_conf_data(connection)

        # parse native config using the Vlan_configurations template
        vlan_configurations_parser = Vlan_configurationsTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = list(vlan_configurations_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("vlan_configurations", None)

        params = utils.remove_empties(
            vlan_configurations_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["vlan_configurations"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
