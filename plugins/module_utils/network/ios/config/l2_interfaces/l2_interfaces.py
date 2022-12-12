#
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_l2_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.l2_interfaces import (
    L2_interfacesTemplate,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.utils.utils import (
    normalize_interface,
    vlan_list_to_range,
    vlan_range_to_list,
)


class L2_interfaces(ResourceModule):
    """
    The ios_l2_interfaces config class
    """

    def __init__(self, module):
        super(L2_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l2_interfaces",
            tmplt=L2_interfacesTemplate(),
        )
        self.parsers = [
            "access.vlan",
            "access.vlan_name",
            "voice.vlan",
            "voice.vlan_tag",
            "voice.vlan_name",
            "mode",
            "trunk.encapsulation",
            "trunk.native_vlan",
        ]

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
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        for each in wantd, haved:
            self.process_list_attrs(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the L2_interfaces network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self.compare_list(want, have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def compare_list(self, want, have):
        for vlan in ["allowed_vlans", "pruning_vlans"]:
            cmd_always = list(
                set(want.get("trunk", {}).get(vlan, [])) - set(have.get("trunk", {}).get(vlan, [])),
            )  # find vlans to create wrt have
            if self.state != "merged":
                rem_vlan = []
                for vl_no in have.get("trunk", {}).get(vlan, []):
                    if vl_no not in cmd_always and vl_no not in want.get("trunk", {}).get(vlan, []):
                        rem_vlan.append(vl_no)
                if (
                    not want.get("trunk", {}).get(vlan, []) and rem_vlan
                ):  # remove vlan all as want blank
                    self.commands.append(
                        "no switchport trunk {0} vlan".format(vlan.split("_", maxsplit=1)[0]),
                    )
                elif rem_vlan:  # remove excess vlans for replaced overridden with vlan entries
                    self.commands.append(
                        "switchport trunk {0} vlan remove {1}".format(
                            vlan.split("_", maxsplit=1)[0],
                            vlan_list_to_range(sorted(rem_vlan)),
                        ),
                    )
            if self.state != "deleted" and cmd_always:  # add configuration needed
                add = "add " if have.get("trunk", {}).get(vlan, []) else ""
                self.commands.append(
                    "switchport trunk {0} vlan {1}{2}".format(
                        vlan.split("_", maxsplit=1)[0],
                        add,
                        vlan_list_to_range(sorted(cmd_always)),
                    ),
                )

    def process_list_attrs(self, param):
        if param:
            for _k, val in iteritems(param):
                val["name"] = normalize_interface(val["name"])
                if val.get("trunk"):
                    for vlan in ["allowed_vlans", "pruning_vlans"]:
                        if val.get("trunk").get(vlan):
                            val["trunk"][vlan] = vlan_range_to_list(val.get("trunk").get(vlan))
