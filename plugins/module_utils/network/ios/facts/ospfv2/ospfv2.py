# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios ospfv2 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type


from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.ospfv2.ospfv2 import (
    Ospfv2Args,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospfv2 import (
    Ospfv2Template,
)


class Ospfv2Facts(object):
    """The ios ospfv2 fact class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ospfv2Args.argument_spec

    def get_ospfv2_data(self, connection):
        return connection.get("show running-config | section ^router ospf")

    def dict_to_list(self, ospf_data):
        """Converts areas, interfaces in each process to list
        :param ospf_data: ospf data
        :rtype: dictionary
        :returns: facts_output
        """

        facts_output = {"processes": []}

        for process in ospf_data.get("processes", []):
            if "passive_interfaces" in process and process["passive_interfaces"].get("default"):
                if process.get("passive_interfaces", {}).get("interface"):
                    process["passive_interfaces"]["interface"]["name"] = [
                        each for each in process["passive_interfaces"]["interface"]["name"] if each
                    ]
            if "areas" in process:
                process["areas"] = list(process["areas"].values())
            facts_output["processes"].append(process)

        return facts_output

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for ospfv2
        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf
        :rtype: dictionary
        :returns: facts
        """

        facts = {}

        if not data:
            data = self.get_ospfv2_data(connection)

        ospf_temp_obj = NetworkTemplate(lines=data.splitlines(), tmplt=Ospfv2Template())
        ospf_parsed = ospf_temp_obj.parse()

        # Convert dict to list
        ospf_parsed["processes"] = (
            ospf_parsed["processes"].values() if "processes" in ospf_parsed else []
        )

        # converts areas, interfaces in each process to list
        facts_output = self.dict_to_list(ospf_parsed)

        ansible_facts["ansible_network_resources"].pop("ospfv2", None)

        if ospf_parsed["processes"]:
            params = utils.validate_config(self.argument_spec, {"config": facts_output})
            params = utils.remove_empties(params)
            facts["ospfv2"] = params["config"]
            ansible_facts["ansible_network_resources"].update(facts)
        return ansible_facts
