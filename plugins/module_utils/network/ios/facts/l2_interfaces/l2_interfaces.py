# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios l2_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l2_interfaces import (
    L2_interfacesTemplate,
)


class L2_interfacesFacts(object):
    """The ios l2_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = L2_interfacesArgs.argument_spec

    def get_l2_interfaces_data(self, connection):
        return connection.get("show running-config | section ^interface")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for L2_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_l2_interfaces_data(connection)

        # parse native config using the L2_interfaces template
        l2_interfaces_parser = L2_interfacesTemplate(lines=data.splitlines(), module=self._module)
        objs = list(l2_interfaces_parser.parse().values())

        def process_mode(obj):
            mode = ""
            if obj == "dot1q-tunnel":
                mode = "dot1q_tunnel"
            elif obj == "dynamic auto":
                mode = "dynamic_auto"
            elif obj == "dynamic desirable":
                mode = "dynamic_desirable"
            elif obj == "private-vlan host":
                mode = "private_vlan_host"
            elif obj == "private-vlan promiscuous":
                mode = "private_vlan_promiscuous"
            elif obj == "private-vlan trunk secondary":
                mode = "private_vlan_trunk"
            return mode

        def process_vlans(obj, vlan_type):
            vlans = []
            _vlans = obj.get("trunk")
            if _vlans.get(vlan_type):
                vlans.extend(_vlans.get(vlan_type))
            if _vlans.get(vlan_type + "_add"):
                for vlan_grp in _vlans.get(vlan_type + "_add"):
                    vlans.extend(vlan_grp)
                del _vlans[vlan_type + "_add"]
            return vlans

        if objs:
            for obj in objs:
                if obj.get("mode") and obj.get("mode") not in ["trunk", "access", "dynamic"]:
                    obj["mode"] = process_mode(obj.get("mode"))
                if obj.get("trunk"):
                    for _vlan in ["allowed_vlans", "pruning_vlans"]:
                        if obj.get("trunk", {}).get(_vlan):
                            obj["trunk"][_vlan] = process_vlans(obj, _vlan)

            ansible_facts["ansible_network_resources"].pop("l2_interfaces", None)

        params = utils.remove_empties(
            l2_interfaces_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["l2_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
