#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The cisco.ios_route_maps config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.route_maps import (
    Route_mapsTemplate,
)


class Route_maps(ResourceModule):
    """
    The cisco.ios_route_maps config class
    """

    def __init__(self, module):
        super(Route_maps, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="route_maps",
            tmplt=Route_mapsTemplate(),
        )
        self.parsers = []

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
            wantd = {(entry["route_map"]): entry for entry in self.want}
        else:
            wantd = {}
        if self.have:
            haved = {(entry["route_map"]): entry for entry in self.have}
        else:
            haved = {}

        # Convert each of config list to dict
        for each in wantd, haved:
            self.list_to_dict(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
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
           for the Route_maps network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)

    def list_to_dict(self, param):
        if param:

            def convert_to_dict(inner_match, key):
                temp = dict()
                for each in inner_match:
                    temp.update({key + "_" + str(each): each})
                return temp

            for key, val in iteritems(param):
                temp_entries = dict()
                for every in val["entries"]:
                    match = every.get("match")
                    if match:
                        if match.get("as_path") and match.get("as_path").get(
                            "acl"
                        ):
                            match["as_path"]["acl"] = convert_to_dict(
                                match["as_path"]["acl"], "acl"
                            )
                        if match.get("ip"):
                            for each_ip_param in [
                                "address",
                                "flowspec",
                                "next_hop",
                                "redistribution_source",
                                "route_source",
                            ]:
                                if match["ip"].get(each_ip_param):
                                    if match["ip"][each_ip_param].get("acl"):
                                        match["ip"][each_ip_param][
                                            "acl"
                                        ] = convert_to_dict(
                                            match["ip"][each_ip_param]["acl"],
                                            "acl",
                                        )
                                    elif match["ip"][each_ip_param].get(
                                        "prefix_list"
                                    ):
                                        match["ip"][each_ip_param][
                                            "prefix_list"
                                        ] = convert_to_dict(
                                            match["ip"][each_ip_param][
                                                "prefix_list"
                                            ],
                                            "prefix_list",
                                        )
                        if match.get("local_preference") and match.get(
                            "local_preference"
                        ).get("value"):
                            match["local_preference"][
                                "value"
                            ] = convert_to_dict(
                                match["local_preference"]["value"], "value"
                            )
                        if match.get("security_group"):
                            for each_sg_param in ["source", "destination"]:
                                if match.get("security_group").get(
                                    each_sg_param
                                ):
                                    match["security_group"][
                                        each_sg_param
                                    ] = convert_to_dict(
                                        match["security_group"][each_sg_param],
                                        each_sg_param,
                                    )
                    action = every.get("action")
                    sequence = every.get("sequence")
                    temp_entries.update({action + "_" + str(sequence): every})
                val["entries"] = temp_entries
