# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios_vrf_global config file.
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
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.vrf_global import (
    Vrf_globalTemplate,
)


class Vrf_global(ResourceModule):
    """
    The ios_vrf_global config class
    """

    def __init__(self, module):
        super(Vrf_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vrf_global",
            tmplt=Vrf_globalTemplate(),
        )
        self.parsers = [
            "description",
            "ipv4.multicast.multitopology",
            "ipv6.multicast.multitopology",
            "rd",
            "route_target.export",
            "route_target.import_config",
            "route_target.both",
            "vnet.tag",
            "vpn.id",
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
        haved, wantd = dict(), dict()

        if self.want:
            for entry in self.want.get("vrfs", []):
                wantd.update({(entry["name"]): entry})

        if self.have:
            for entry in self.have.get("vrfs", []):
                haved.update({(entry["name"]): entry})

        # if state is merged, merge want onto have
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, limit the have to anything in want & set want to nothing
        if self.state == "deleted":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        if self.state == "purged":
            for k, have in iteritems(haved):
                self.purge(have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Vrf_global network resource.
        """
        if want != have:
            self.addcmd(want or have, "name", False)
            self.compare(self.parsers, want, have)

    def purge(self, have):
        """Purge the VRF configuration"""
        self.commands.append("no vrf definition {0}".format(have["name"]))
