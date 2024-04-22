#
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

from copy import deepcopy

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
            "name",
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
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        if self.state == "purged":
            haved = {k: v for k, v in iteritems(haved) if k in wantd or not wantd}
            wantd = {}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Vrf_global network resource.
        """
        self._compare_vrf(want=want, have=have)

    def _compare_vrf(self, want, have):
        """Custom handling of vrfs option
        :params want: the want VRF dictionary
        :params have: the have VRF dictionary
        """

        for name, entry in iteritems(want):
            begin = len(self.commands)
            vrf_have = have.pop(name, {})

            self.compare(parsers=self.parsers, want=entry, have=vrf_have)

        # for deleted and overridden state
        if self.state != "replaced":
            begin = len(self.commands)
            for name, entry in iteritems(have):
                self.commands.insert(begin, "no vrf definition {0}".format(name))

    def _get_config(self):
        return self._connection.get("show running-config vrf")
