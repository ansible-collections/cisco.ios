#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The cisco.ios_bgp_address_family config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_address_family import (
    Bgp_address_familyTemplate,
)


class Bgp_address_family(ResourceModule):
    """
    The cisco.ios_bgp_address_family config class
    """

    parsers = [
        "as_number",  # generic
        "aggregate_addresses",
        "auto_summary",
        "default",
        "default_information",
        "default_metric",
        "distance",
        "table_map",
        "bgp.additional_paths.select",  # bgp
        "bgp.additional_paths.install",
        "bgp.additional_paths.receive",
        "bgp.additional_paths.send",
        "bgp.aggregate_timer",
        "bgp.dmzlink-bw",
        "bgp.nexthop.route_map",
        "bgp.nexthop.trigger.delay",
        "bgp.nexthop.trigger.enable",
        "bgp.redistribute_internal",
        "bgp.route_map",
        "bgp.scan_time",
        "bgp.soft_reconfig_backup",
        "bgp.update_group",
        "bgp.dampening",
        "bgp.slow_peer_options.detection.enable",
        "bgp.slow_peer_options.detection.threshold",
        "bgp.slow_peer_options.split_update_group.dynamic",
        "bgp.slow_peer.split_update_group.permanent",
        "snmp.context.user",  # snmp
        "snmp.context.community",
        "redistribute.application",  # redistribute
        "redistribute.bgp",
        "redistribute.connected",
        "redistribute.eigrp",
        "redistribute.isis",
        "redistribute.iso_igrp",
        "redistribute.lisp",
        "redistribute.mobile",
        "redistribute.odr",
        "redistribute.ospf",
        "redistribute.ospfv3",
        "redistribute.rip",
        "redistribute.static",
        "redistribute.vrf",  # redistribute
    ]

    def __init__(self, module):
        super(Bgp_address_family, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_address_family",
            tmplt=Bgp_address_familyTemplate(),
        )

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
        if self.state in ["merged", "replaced", "overridden"]:
            if self.have.get("as_number") and self.want.get("as_number") != self.have.get(
                "as_number",
            ):
                self._module.fail_json(
                    msg="BGP is already running. Only one BGP instance is allowed per device.",
                )

        for each in self.want, self.have:
            each["address_family"] = self._bgp_add_fam_list_to_dict(each.get("address_family", []))

        if self.state == "deleted":
            # deleted, clean up global params
            if not self.want or (self.have.get("as_number") == self.want.get("as_number")):
                self._compare(want={}, have=self.have)

        else:
            wantd = self.want
            # if state is merged, merge want with have and then compare
            if self.state == "merged":
                wantd = dict_merge(self.have, self.want)

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.get("address_family").items():
            self._compare(want=want, have=self.have["address_family"].pop(k, {}))

        # adds router bgp AS_NUMB command
        if len(self.commands) > 0:
            self.commands.insert(0, self._tmplt.render(self.want or self.have, "as_number", False))

    def _compare(self, want, have):
        begin = len(self.commands)
        # for everything else
        self.compare(parsers=self.parsers, want=want, have=have)
        # for neighbors
        self._compare_neighbor_lists(want.get("neighbors", {}), have.get("neighbors", {}))
        # for networks
        self._compare_network_lists(want.get("networks", {}), have.get("networks", {}))
        # add af command
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "afi", False))

    def _compare_neighbor_lists(self, want, have):
        """Compare neighbor list of dict"""
        neig_parses = [
            "activate",
            "additional_paths",
            "advertises.additional_paths",
            "advertises.best_external",
            "advertises.diverse_path",
            "advertise_map",
            "advertisement_interval",
            "aigp",
            "aigp.send.cost_community",
            "aigp.send.med",
            "allow_policy",
            "allowas_in",
            "as_override",
            "bmp_activate",
            "capability",
            "cluster_id",
            "default_originate",
            "default_originate.route_map",
            "description",
            "disable_connected_check",
            "ebgp_multihop",
            "distribute_list",
            "dmzlink_bw",
            "filter_list",
            "fall_over.bfd",
            "fall_over.route_map",
            "ha_mode",
            "inherit",
            "internal_vpn_client",
            "local_as",
            "remote_as",
            "log_neighbor_changes",
            "maximum_prefix",
            "nexthop_self.set",
            "nexthop_self.all",
            "next_hop_unchanged.set",
            "next_hop_unchanged.allpaths",
            "password_options",
            "path_attribute.discard",
            "path_attribute.treat_as_withdraw",
            "peer_group_name",
            "peer_group",
            "route_maps",
            "remove_private_as.set",
            "remove_private_as.all",
            "remove_private_as.replace_as",
            "route_reflector_client",
            "route_server_client",
            "send_community.set",
            "send_community.both",
            "send_community.extended",
            "send_community.standard",
            "shutdown",
            "slow_peer_options.detection",
            "slow_peer_options.split_update_group",
            "soft_reconfiguration",
            "soo",
            "timers",
            "transport.connection_mode",
            "transport.multi_session",
            "transport.path_mtu_discovery",
            "ttl_security",
            "unsuppress_map",
            "version",
            "weight",
        ]

        for name, w_neighbor in want.items():
            have_nbr = have.pop(name, {})
            self.compare(parsers=neig_parses, want=w_neighbor, have=have_nbr)
            for i in ["route_maps", "prefix_lists"]:  # handles route_maps, prefix_lists
                want_route_or_prefix = w_neighbor.pop(i, {})
                have_route_or_prefix = have_nbr.pop(i, {})
                if want_route_or_prefix:
                    for k_rmps, w_rmps in want_route_or_prefix.items():
                        have_rmps = have_route_or_prefix.pop(k_rmps, {})
                        w_rmps["neighbor_address"] = w_neighbor.get("neighbor_address")
                        if have_rmps:
                            have_rmps["neighbor_address"] = have_nbr.get("neighbor_address")
                            have_rmps = {i: have_rmps}
                        self.compare(parsers=[i], want={i: w_rmps}, have=have_rmps)
        for name, h_neighbor in have.items():
            self.compare(parsers="neighbor_address", want={}, have=h_neighbor)

    def _compare_network_lists(self, w_attr, h_attr):
        """Handling of gereric list options."""
        for wkey, wentry in w_attr.items():
            if wentry != h_attr.pop(wkey, {}):
                self.addcmd(wentry, "networks", False)

        # remove remaining items in have for replaced state
        for hkey, hentry in h_attr.items():
            self.addcmd(hentry, "networks", True)

    def _bgp_add_fam_list_to_dict(self, tmp_data):
        """Convert all list of dicts to dicts of dicts, also deals with deprecated attributes"""
        p_key = {
            "aggregate_address": "address",
            "neighbor": "neighbor_address",
            "neighbors": "neighbor_address",
            "route_maps": "name",
            "prefix_lists": "name",
            "networks": "address",
            "network": "address",
        }
        af_data = {}
        for af in tmp_data:
            for k, val in af.items():
                if k == "neighbor" or k == "neighbors":
                    tmp = {}
                    for neib in val:
                        # address/ tag/ ipv6_address to neighbor_address
                        if neib.get("address"):
                            neib["neighbor_address"] = neib.pop("address")
                        if neib.get("tag"):
                            neib["neighbor_address"] = neib.pop("tag")
                        if neib.get("ipv6_address"):
                            neib["neighbor_address"] = neib.pop("ipv6_address")
                        if neib.get("ipv6_adddress"):
                            neib["neighbor_address"] = neib.pop("ipv6_adddress")
                        # next_hop_self deprecated added nexthop_self
                        if neib.get("next_hop_self"):
                            neib["nexthop_self"] = {"set": neib.pop("next_hop_self")}
                        # prefix_list and prefix_lists
                        if neib.get("prefix_list"):  # deprecated made list
                            neib["prefix_lists"] = [neib.get("prefix_list")]
                        if neib.get("prefix_lists"):
                            neib["prefix_lists"] = {
                                str(i[p_key["prefix_lists"]]): i for i in neib.get("prefix_lists")
                            }
                        # route_map and route_maps
                        if neib.get("route_map"):  # deprecated made list
                            neib["route_maps"] = [neib.get("route_map")]
                        if neib.get("route_maps"):
                            neib["route_maps"] = {
                                str(i[p_key["route_maps"]]): i for i in neib.get("route_maps")
                            }
                        # slow_peer to slow_peer_options
                        if neib.get("slow_peer"):  # only one slow_peer is allowed
                            neib["slow_peer_options"] = neib.get("slow_peer")[0]
                        # make dict neighbors dict
                        tmp[neib[p_key[k]]] = neib
                    af["neighbors"] = tmp
                # make dict networks dict
                elif k == "network" or k == "networks":
                    af["networks"] = {str(i[p_key[k]]): i for i in val}
                # make dict aggregate_addresses dict
                elif k == "aggregate_address":
                    af["aggregate_address"] = {str(i[p_key[k]]): i for i in val}
                # slow_peer to slow_peer_options
                elif k == "bgp":
                    if val.get("slow_peer"):  # only one slow_peer is allowed
                        af["bgp"]["slow_peer_options"] = val.get("slow_peer")[0]
                # keep single dict to compare redistribute
                elif k == "redistribute":
                    for i in val:
                        af["redistribute"] = {m: v for m, v in i.items()}
            # make distinct address family entires
            af_data[af.get("afi", "") + "_" + af.get("safi", "") + "_" + af.get("vrf", "")] = af
        return af_data
