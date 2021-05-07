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

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_address_family import (
    Bgp_AddressFamilyTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.bgp_address_family.bgp_address_family import (
    Bgp_AddressFamilyArgs,
)


class Bgp_AddressFamilyFacts(object):
    """ The cisco.ios_bgp_address_family facts class
    """

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bgp_AddressFamilyArgs.argument_spec

    def get_bgp_address_family_data(self, connection):
        return connection.get("sh running-config | section ^router bgp")

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Bgp_address_family network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_bgp_address_family_data(connection)

        # parse native config using the Bgp_address_family template
        bgp_af_parser = Bgp_AddressFamilyTemplate(
            lines=data.splitlines(), module=self._module
        )
        objs = bgp_af_parser.parse()
        objs = utils.remove_empties(objs)
        temp_af = []
        if objs.get("address_family"):
            for k, v in iteritems(objs["address_family"]):
                if k == "__":
                    continue
                temp_dict = {}
                temp = [every for every in k.split("_") if every != ""]
                temp_dict["afi"] = temp.pop(0)
                if len(temp) > 1:
                    temp_dict["vrf"] = [
                        each.split(" ")[1] for each in temp if "vrf" in each
                    ][0]
                    temp_dict["safi"] = [
                        each for each in temp if "vrf" not in each
                    ][0]
                elif len(temp) == 1:
                    if "vrf" in temp[0]:
                        temp_dict["vrf"] = temp[0].split("vrf ")[1]
                    else:
                        temp_dict["safi"] = temp[0]
                neighbor = v.get("neighbor")
                if neighbor:
                    neighbor_list = []
                    temp_slow_peer = []
                    temp = {}
                    neighbor_identifier = None
                    for each in neighbor:
                        if (
                            each.get("address")
                            or each.get("ipv6_address")
                            or each.get("tag")
                        ) != neighbor_identifier:
                            if temp:
                                if temp_slow_peer:
                                    temp.update({"slow_peer": temp_slow_peer})
                                neighbor_list.append(temp)
                                temp = {}
                            neighbor_identifier = (
                                each.get("address")
                                or each.get("ipv6_address")
                                or each.get("tag")
                            )
                            if "address" in each:
                                temp["address"] = neighbor_identifier
                            elif "ipv6_address" in each:
                                temp["ipv6_address"] = neighbor_identifier
                            else:
                                temp["tag"] = neighbor_identifier
                        for every in ["address", "ipv6_address", "tag"]:
                            if every in each:
                                each.pop(every)
                        temp.update(each)
                        slow_peer_val = each.get("slow_peer")
                        if slow_peer_val:
                            temp_slow_peer.append(slow_peer_val[0])
                    if temp:
                        temp.update({"slow_peer": temp_slow_peer})
                        neighbor_list.append(temp)
                        temp = {}
                    v["neighbor"] = neighbor_list
                v.update(temp_dict)
                temp_af.append(v)

            objs["address_family"] = temp_af
            objs["address_family"] = sorted(
                objs["address_family"], key=lambda k, sk="afi": k[sk]
            )
        if objs:
            ansible_facts["ansible_network_resources"].pop(
                "bgp_address_family", None
            )

            params = utils.remove_empties(
                bgp_af_parser.validate_config(
                    self.argument_spec, {"config": objs}, redact=True
                )
            )

            facts["bgp_address_family"] = params["config"]
            ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
