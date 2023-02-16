# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The cisco.ios bgp_address_family fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_address_family.bgp_address_family import (
    Bgp_address_familyArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_address_family import (
    Bgp_address_familyTemplate,
)


class Bgp_address_familyFacts(object):
    """The cisco.ios_bgp_address_family facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bgp_address_familyArgs.argument_spec

    def get_bgp_address_family_data(self, connection):
        return connection.get("show running-config | section ^router bgp")

    def _process_facts(self, objs):
        """makes data as per the facts after data obtained from parsers"""
        addr_fam_facts = {}
        temp_af = []

        addr_fam_facts["as_number"] = objs["as_number"]
        if objs.get("address_family"):
            for kaf, afs in (objs["address_family"]).items():  # remove unique value from add_fam
                af = {}
                for af_key, afs_val in afs.items():
                    if af_key == "neighbors":
                        temp_neighbor = []
                        for tag, neighbor in afs_val.items():  # remove unique value from neighbor
                            if not neighbor.get("neighbor_address"):
                                neighbor["neighbor_address"] = tag
                            temp_neighbor.append(neighbor)
                        af[af_key] = temp_neighbor
                    else:
                        af[af_key] = afs_val
                temp_af.append(af)

        if temp_af:
            addr_fam_facts["address_family"] = temp_af
        return addr_fam_facts

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bgp_address_family network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = {}

        if not data:
            data = self.get_bgp_address_family_data(connection)

        # parse native config using the Bgp_address_family template
        bgp_af_parser = Bgp_address_familyTemplate(lines=data.splitlines(), module=self._module)
        objs = bgp_af_parser.parse()
        if objs:
            objs = self._process_facts(utils.remove_empties(objs))
        ansible_facts["ansible_network_resources"].pop("bgp_address_family", None)
        params = utils.remove_empties(
            bgp_af_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )
        facts["bgp_address_family"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
