# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_ospfv2 class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospfv2 import (
    Ospfv2Template,
)


class Ospfv2(ResourceModule):
    """
    The ios_ospfv2 class
    """

    def __init__(self, module):
        super(Ospfv2, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ospfv2",
            tmplt=Ospfv2Template(),
        )

        self.parsers = [
            "adjacency",
            "address_family",
            "auto_cost",
            "bfd",
            "capability.lls",
            "capability.opaque",
            "capability.transit",
            "capability.vrf_lite",
            "compatible",
            "default_information",
            "default_metric",
            "discard_route",
            "distance.admin_distance",
            "distance.ospf",
            "distribute_list.prefix",
            "distribute_list.route_map",
            "domain_id",
            "domain_tag",
            "event_log",
            "help",
            "ignore",
            "interface_id",
            "ispf",
            "limit",
            "local_rib_criteria",
            "log_adjacency_changes",
            "max_lsa",
            "max_metric",
            "maximum_paths",
            "mpls.ldp.autoconfig",
            "mpls.ldp.sync",
            "mpls.traffic_eng",
            "neighbor",
            "nsf.cisco",
            "nsf.ietf.disable",
            "nsf.ietf.strict_lsa_checking",
            "prefix_suppression",
            "priority",
            "queue_depth.hello.max_packets",
            "queue_depth.hello.unlimited",
            "queue_depth.update.max_packets",
            "queue_depth.update.unlimited",
            "router_id",
            "shutdown",
            "summary_address.not_advertise",
            "summary_address.nssa_only",
            "timers.throttle.lsa",
            "timers.pacing.flood",
            "timers.pacing.lsa_group",
            "timers.pacing.retransmission",
            "timers.throttle.spf",
            "traffic_share",
            "ttl_security",
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
        """Select the appropriate function based on the state provided

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """
        haved, wantd = dict(), dict()

        if self.want:
            for entry in self.want.get("processes", []):
                entry = self._handle_deprecated(entry)
                wantd.update({(entry["process_id"], entry.get("vrf")): entry})

        if self.have:
            for entry in self.have.get("processes", []):
                # entry = self._handle_deprecated(entry)
                haved.update({(entry["process_id"], entry.get("vrf")): entry})

        # turn all lists of dicts into dicts prior to merge
        for each in wantd, haved:
            if each:
                self._list_to_dict(each)

        # if state is merged, merge want onto have
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, limit the have to anything in want
        # set want to nothing
        if self.state == "deleted":
            temp = {}
            for k, v in iteritems(haved):
                if k in wantd or not wantd:
                    temp.update({k: v})
            haved = temp
            wantd = {}

        # delete processes first so we do run into "more than one" errors
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self.addcmd(have, "pid", True)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        if want != have:
            self.addcmd(want or have, "pid", False)
            self.compare(self.parsers, want, have)
            self._areas_compare(want, have)
            self._complex_compare(want, have)
            if want.get("passive_interfaces"):
                self._passive_interfaces_compare(want, have)

    def _complex_compare(self, want, have):
        complex_parsers = ["distribute_list.acls", "network"]
        for _parser in complex_parsers:
            if _parser == "distribute_list.acls":
                wdist = want.get("distribute_list", {}).get("acls", {})
                hdist = have.get("distribute_list", {}).get("acls", {})
            else:
                wdist = want.get(_parser, {})
                hdist = have.get(_parser, {})
            for key, wanting in iteritems(wdist):
                haveing = hdist.pop(key, {})
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser, False)
            for key, haveing in iteritems(hdist):
                self.addcmd(haveing, _parser, negate=True)

    def _areas_compare(self, want, have):
        wareas = want.get("areas", {})
        hareas = have.get("areas", {})
        for name, entry in iteritems(wareas):
            self._area_compare(want=entry, have=hareas.pop(name, {}))
        for name, entry in iteritems(hareas):
            self._area_compare(want={}, have=entry)

    def _area_compare(self, want, have):
        parsers = [
            "authentication",
            "capability",
            "default_cost",
            "nssa",
            "nssa.translate",
            "sham_link",
            "stub",
        ]
        self.compare(parsers=parsers, want=want, have=have)
        self._area_complex_compare(want, have, want.get("area_id"))

    def _area_complex_compare(self, want, have, area_id):
        area_complex_parsers = ["filter_list", "ranges"]
        for _parser in area_complex_parsers:
            wantr = want.get(_parser, {})
            haver = have.get(_parser, {})
            for key, wanting in iteritems(wantr):
                haveing = have.pop(key, {})
                haveing["area_id"] = area_id
                wanting["area_id"] = area_id
                if wanting != haveing:
                    if haveing and self.state in ["overridden", "replaced"]:
                        self.addcmd(haveing, _parser, negate=True)
                    self.addcmd(wanting, _parser, False)
            for key, haveing in iteritems(haver):
                haveing["area_id"] = area_id
                self.addcmd(haveing, _parser, negate=True)

    def _passive_interfaces_compare(self, want, have):
        parsers = ["passive_interfaces.default", "passive_interfaces.interface"]
        h_pi = None
        for k, v in iteritems(want["passive_interfaces"]):
            h_pi = have.get("passive_interfaces", {})
            if h_pi.get(k) and h_pi.get(k) != v:
                for each in v["name"]:
                    h_interface_name = h_pi[k].get("name", [])
                    if each not in h_interface_name:
                        temp = {"interface": {each: each}, "set_interface": v["set_interface"]}
                        self.compare(
                            parsers=parsers,
                            want={"passive_interfaces": temp},
                            have=dict(),
                        )
                    else:
                        h_interface_name.pop(each)
            elif not h_pi:
                if k == "interface":
                    for each in v["name"]:
                        temp = {"interface": {each: each}, "set_interface": v["set_interface"]}
                        self.compare(
                            parsers=parsers,
                            want={"passive_interfaces": temp},
                            have=dict(),
                        )
                elif k == "default":
                    self.compare(
                        parsers=parsers,
                        want={"passive_interfaces": {"default": True}},
                        have=dict(),
                    )
            else:
                h_pi.pop(k)
        if (self.state == "replaced" or self.state == "overridden") and h_pi:
            if h_pi.get("default") or h_pi.get("interface"):
                for k, v in iteritems(h_pi):
                    if k == "interface":
                        for each in v["name"]:
                            temp = {
                                "interface": {each: each},
                                "set_interface": not (v["set_interface"]),
                            }
                            self.compare(
                                parsers=parsers,
                                want={"passive_interfaces": temp},
                                have=dict(),
                            )
                    elif k == "default":
                        self.compare(
                            parsers=parsers,
                            want=dict(),
                            have={"passive_interfaces": {"default": True}},
                        )

    def _list_to_dict(self, param):
        for _pid, proc in param.items():
            # convert list to dict for areas
            for area in proc.get("areas", []):
                area["ranges"] = {entry["address"]: entry for entry in area.get("ranges", [])}
                area["filter_list"] = {
                    entry["direction"]: entry for entry in area.get("filter_list", [])
                }

            proc["areas"] = {entry["area_id"]: entry for entry in proc.get("areas", [])}

            # list to dict for distribute_list
            distribute_list = proc.get("distribute_list", {})
            if "acls" in distribute_list:
                distribute_list["acls"] = {
                    entry["name"]: entry for entry in distribute_list["acls"]
                }

            # list to dict for passive_interfaces
            passive_interfaces = proc.get("passive_interfaces", {}).get("interface", {})
            if passive_interfaces.get("name"):
                passive_interfaces["name"] = {entry: entry for entry in passive_interfaces["name"]}

            # list to dict for network
            if proc.get("network"):
                proc["network"] = {entry["address"]: entry for entry in proc["network"]}

    def _handle_deprecated(self, config):
        if config.get("passive_interface"):
            passive_interfaces = config.get("passive_interfaces", {})
            interface = passive_interfaces.get("interface", {})
            name_list = interface.get("name", [])
            if not name_list:
                name_list.append(config["passive_interface"])
            else:
                name_list.extend(config["passive_interface"])
            del config["passive_interface"]
        return config
