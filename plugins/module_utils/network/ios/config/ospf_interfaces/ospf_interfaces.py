#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The cisco.ios_ospf_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospf_interfaces import (
    Ospf_interfacesTemplate,
)


class Ospf_interfaces(ResourceModule):
    """
    The cisco.ios_ospf_interfaces config class
    """

    def __init__(self, module):
        super(Ospf_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospf_interfaces",
            tmplt=Ospf_interfacesTemplate(),
        )
        self.parsers = []

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """

        # turn all lists of dicts into dicts prior to merge
        wantd = self._list_to_dict(self.want, "want")
        haved = self._list_to_dict(self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have, interface=k)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}), interface=k)

    def _compare(self, want, have, interface):
        begin = len(self.commands)
        self._compare_afis(want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render({"name": interface}, "name", False))

    def _compare_afis(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Ospf_interfaces network resource.
        """

        parsers = [
            "name",
            "process",
            "adjacency",
            "authentication",
            "bfd",
            "cost",
            "database_filter",
            "dead_interval",
            "demand_circuit",
            "flood_reduction",
            "hello_interval",
            "lls",
            "manet",
            "mtu_ignore",
            "multi_area",
            "neighbor",
            "network",
            "prefix_suppression",
            "priority",
            "resync_timeout",
            "retransmit_interval",
            "shutdown",
            "transmit_delay",
            "ttl_security",
        ]

        for afi in ("ipv4", "ipv6"):
            wacls = want.pop(afi, {})
            hacls = have.pop(afi, {})

            self.compare(parsers=parsers, want=wacls, have=hacls)

    def _list_to_dict(self, entry, attr_type=None):
        if self.state == "deleted" and attr_type == "want":
            del_list = {}
            for intf in entry:
                del_list[intf.get("name")] = {}
            return del_list

        list_to_dict = {}
        for intf in entry:
            if intf.get("address_family"):
                list_to_dict[intf.get("name")] = self.process_list_attr(intf)
        return list_to_dict

    def process_list_attr(self, add_fam):
        item = {}
        for ag in add_fam.get("address_family", []):
            item[ag.get("afi")] = ag
        return item
