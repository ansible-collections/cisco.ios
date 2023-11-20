#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_evpn_global config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.evpn_global import (
    Evpn_globalTemplate,
)


EVPN_GLOBAL_PARENT = "l2vpn evpn"


class Evpn_global(ResourceModule):
    """
    The ios_evpn_global config class
    """

    def __init__(self, module):
        super(Evpn_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="evpn_global",
            tmplt=Evpn_globalTemplate(),
        )
        self.parsers = [
            "default_gateway.advertise",
            "flooding_suppression.address_resolution.disable",
            "ip.local_learning.disable",
            "replication_type",
            "route_target.auto.vni",
            "router_id",
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
        wantd = self.want
        haved = self.have

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # remove superfluous config for deleted
        if self.state == "deleted":
            if haved:
                self.commands.append("no " + EVPN_GLOBAL_PARENT)
            wantd, haved = {}, {}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Evpn_global network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        if len(self.commands) != begin:
            self.commands.insert(begin, EVPN_GLOBAL_PARENT)
