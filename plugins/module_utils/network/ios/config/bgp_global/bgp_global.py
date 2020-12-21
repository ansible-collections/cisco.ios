#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_bgp_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)
import q


class Bgp_global(ResourceModule):
    """
    The cisco.ios_bgp_global config class
    """

    def __init__(self, module):
        super(Bgp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_global",
            tmplt=Bgp_globalTemplate(),
        )
        self.parsers = [
            "asn",
            "bgp.additional_paths",
            "bgp.advertise_best_external",
            "bgp.always_compare_med",
            "bgp.log_neighbor_changes",
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        if self.want:
            wantd = {self.want["asn"]: self.want}
        else:
            wantd = {}
        if self.have:
            haved = {self.have["asn"]: self.have}
        else:
            haved = {}
        q(self.state, wantd, haved)
        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: {"asn": v["asn"]}
                for k, v in iteritems(haved)
                if k in wantd or not wantd
            }
            wantd = {}

        # remove superfluous config for and deleted
        if self.state in ["deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd and "asn" in have:
                    self.compare(parsers=self.parsers, want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

        q(self.commands)
        self.commands = []

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_global network resource.
        """

        if want != have and self.state != "deleted":
            self.addcmd(have, "asn", False)
            self.compare(parsers=self.parsers, want=want, have=have)
            self._bgp_list_param_compare(want, have)
            self._neighbor_compare(want, have)

    def _bgp_list_param_compare(self, wantd, haved):
        for name, entry in iteritems(wantd):
            h_item = haved.pop(name, {})
            if entry != h_item and name == "filter_list":
                filter_list_entry = {}
                filter_list_entry["area_id"] = wantd["area_id"]
                if h_item:
                    li_diff = [
                        item
                        for item in entry + h_item
                        if item not in entry or item not in h_item
                    ]
                else:
                    li_diff = entry
                filter_list_entry["filter_list"] = li_diff
                self.addcmd(filter_list_entry, "area.filter_list", False)
        for name, entry in iteritems(haved):
            if name == "filter_list":
                self.addcmd(entry, "area.filter_list", True)

    def _neighbor_compare(self, wantd, haved):
        for name, entry in iteritems(wantd):
            h_item = haved.pop(name, {})
            if entry != h_item and name == "filter_list":
                filter_list_entry = {}
                filter_list_entry["area_id"] = wantd["area_id"]
                if h_item:
                    li_diff = [
                        item
                        for item in entry + h_item
                        if item not in entry or item not in h_item
                    ]
                else:
                    li_diff = entry
                filter_list_entry["filter_list"] = li_diff
                self.addcmd(filter_list_entry, "area.filter_list", False)
        for name, entry in iteritems(haved):
            if name == "filter_list":
                self.addcmd(entry, "area.filter_list", True)
