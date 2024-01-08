#
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_vlans config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vlans import (
    VlansTemplate,
)


class Vlans(ResourceModule):
    """
    The ios_vlans config class
    """

    def __init__(self, module):
        super(Vlans, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vlans",
            tmplt=VlansTemplate(),
        )
        self.parsers = [
            "name",
            "state",
            "mtu",
            "remote_span",
            "private_vlan.type",
            "private_vlan.associated",
            "shutdown",
            "member",
        ]

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.segregate_resource()
            # self.generate_commands()
            self.run_commands()
        return self.result

    def segregate_resource(self):
        self.want_vlan_config = []
        self.have_vlan_config = []
        for vlan_data in self.want:
            if vlan_data.get("member"):
                self.want_vlan_config.append(
                    {
                        "vlan_id": vlan_data.get("vlan_id"),
                        "member": vlan_data.pop("member"),
                    },
                )
        for vlan_data in self.have:
            if vlan_data.get("member"):
                self.have_vlan_config.append(
                    {
                        "vlan_id": vlan_data.get("vlan_id"),
                        "member": vlan_data.pop("member"),
                    },
                )
        if self.want or self.have:
            self.generate_commands(self.want, self.have, "vlans")
        if self.want_vlan_config or self.have_vlan_config:
            self.generate_commands(
                self.want_vlan_config,
                self.have_vlan_config,
                "vlan_configuration",
            )

    def generate_commands(self, conf_want, conf_have, resource=None):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = {entry["vlan_id"]: entry for entry in conf_want}
        haved = {entry["vlan_id"]: entry for entry in conf_have}

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
                    self._compare(want={}, have=have, resource=resource)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}), resource=resource)

    def _compare(self, want, have, resource=None):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Vlans network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(
                begin,
                self._tmplt.render(want or have, resource, False),
            )
