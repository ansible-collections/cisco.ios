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

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import Facts
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)


class Bgp_global(ResourceModule):
    """
    The cisco.ios_bgp_global config class
    """

    parsers = [
        "auto_summary",
        "bmp.buffer_size",
        "bmp.initial_refresh.delay",
        "bmp.initial_refresh.skip",
        "bmp.server",
        "bmp.server_options.activate",
        "bmp.server_options.address",
        "default_information",
        "default_metric",
        "distance.admin",
        "distance.bgp",
        "distance.mbgp",
        "maximum_paths.paths",
        "maximum_paths.eibgp",
        "maximum_paths.ibgp",
        "maximum_secondary_paths.paths",
        "maximum_secondary_paths.eibgp",
        "maximum_secondary_paths.ibgp",
        "route_server_context.name",
        "route_server_context.address_family",
        "route_server_context.description",
        "synchronization",
        "table_map",
        "timers",
        "bgp.additional_paths",
        "bgp.advertise_best_external",
        "bgp.aggregate_timer",
        "bgp.always_compare_med",
        "bgp.asnotation",
        "bgp.bestpath_options.aigp",
        "bgp.bestpath_options.compare_routerid",
        "bgp.bestpath_options.cost_community",
        "bgp.bestpath_options.igp_metric",
        "bgp.bestpath_options.med",
        "bgp.client_to_client",
        "bgp.cluster_id",
        "bgp.confederation.peer",
        "bgp.confederation.identifier",
        "bgp.consistency_checker.auto_repair",
        "bgp.consistency_checker.error_message",
        "bgp.dampening",
        "bgp.deterministic_med",
        "bgp.dmzlink_bw",
        "bgp.enforce_first_as",
        "bgp.enhanced_error",
        "bgp.fast_external_fallover",
        "bgp.graceful_restart.set",
        "bgp.graceful_restart.extended",
        "bgp.graceful_restart.restart_time",
        "bgp.graceful_restart.stalepath_time",
        "bgp.graceful_shutdown.neighbors",
        "bgp.graceful_shutdown.vrfs",
        "bgp.listen.limit",
        "bgp.listen.range",
        "bgp.log_neighbor_changes",
        "bgp.maxas_limit",
        "bgp.maxcommunity_limit",
        "bgp.maxextcommunity_limit",
        "bgp.nexthop.route_map",
        "bgp.nexthop.trigger.delay",
        "bgp.nexthop.trigger.enable",
        "bgp.nopeerup_delay_options.cold_boot",
        "bgp.nopeerup_delay_options.post_boot",
        "bgp.nopeerup_delay_options.nsf_switchover",
        "bgp.nopeerup_delay_options.user_initiated",
        "bgp.recursion",
        "bgp.redistribute_internal",
        "bgp.refresh.max_eor_time",
        "bgp.refresh.stalepath_time",
        "bgp.regexp",
        "bgp.router_id",
        "bgp.scan_time",
        "bgp.slow_peer.detection.set",
        "bgp.slow_peer.detection.threshold",
        "bgp.slow_peer.split_update_group",
        "bgp.snmp",
        "bgp.sso",
        "bgp.soft_reconfig_backup",
        "bgp.suppress_inactive",
        "bgp.transport",
        "bgp.update_delay",
        "bgp.update_group",
        "bgp.upgrade_cli.set",
        "bgp.upgrade_cli.af_mode",
    ]

    def __init__(self, module):
        super(Bgp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_global",
            tmplt=Bgp_globalTemplate(),
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
        if self.state in ["merged", "replaced"]:
            w_asn = self.want.get("as_number")
            h_asn = self.have.get("as_number")

            if h_asn and w_asn != h_asn:
                self._module.fail_json(
                    msg="BGP is already configured with ASN {0}. "
                    "Please remove it with state: purged before "
                    "configuring new ASN".format(h_asn),
                )

        if self.want:
            self.handle_deprecates(self.want)

        for each in self.want, self.have:
            self._bgp_global_list_to_dict(each)

        if self.state == "deleted":
            # deleted, clean up global params
            if not self.want or (self.have.get("as_number") == self.want.get("as_number")):
                self._compare(want={}, have=self.have)

        elif self.state == "purged":
            # delete as_number takes down whole bgp config
            if not self.want or (self.have.get("as_number") == self.want.get("as_number")):
                self.addcmd(self.have or {}, "as_number", True)

        else:
            wantd = self.want
            # if state is merged, merge want with have and then compare
            if self.state == "merged":
                wantd = dict_merge(self.have, self.want)

            self._compare(want=wantd, have=self.have)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Bgp_global network resource.
        """
        self.generic_list_parsers = ["distributes", "aggregate_addresses", "networks"]
        if self._has_bgp_inject_maps(want):
            self.generic_list_parsers.insert(0, "inject_maps")

        cmd_len = len(self.commands)  # holds command length to add as_number
        # for dict type attributes
        self.compare(parsers=self.parsers, want=want, have=have)

        # for list type attributes
        for _parse in self.generic_list_parsers:
            if _parse == "inject_maps":
                self._compare_generic_lists(
                    want.get("bgp", {}).get(_parse, {}),
                    have.get("bgp", {}).get(_parse, {}),
                    _parse,
                )
            else:
                self._compare_generic_lists(want.get(_parse, {}), have.get(_parse, {}), _parse)

        # for neighbors
        self._compare_neighbor_lists(want.get("neighbors", {}), have.get("neighbors", {}))

        # for redistribute
        self._compare_redistribute_lists(want.get("redistribute", {}), have.get("redistribute", {}))

        # add as_number in the begining fo command set if commands generated
        if len(self.commands) != cmd_len or (not have and want):
            self.commands.insert(0, self._tmplt.render(want or have, "as_number", False))

    def _has_bgp_inject_maps(self, want):
        if want.get("bgp", {}).get("inject_maps", {}):
            return True
        else:
            return False

    def _compare_redistribute_lists(self, want, have):
        """Compare redistribute list of dict"""
        redist_parses = [
            "application",
            "bgp",
            "connected",
            "eigrp",
            "isis",
            "iso_igrp",
            "lisp",
            "mobile",
            "odr",
            "ospf",
            "ospfv3",
            "rip",
            "static",
            "vrf",
        ]
        for name, w_redist in want.items():
            have_nbr = have.pop(name, {})
            self.compare(parsers=redist_parses, want=w_redist, have=have_nbr)

        # remove remaining items in have for replaced state
        for name, h_redist in have.items():
            self.compare(parsers=redist_parses, want={}, have=h_redist)

    def _compare_neighbor_lists(self, want, have):
        """Compare neighbor list of dict"""
        neig_parses = [
            "remote_as",
            "peer_group",
            "bmp_activate",
            "cluster_id",
            "description",
            "disable_connected_check",
            "ebgp_multihop",
            "fall_over.bfd",
            "fall_over.route_map",
            "ha_mode",
            "inherit",
            "local_as",
            "log_neighbor_changes",
            "password_options",
            "path_attribute.discard",
            "path_attribute.treat_as_withdraw",
            "shutdown",
            "soft_reconfiguration",
            "ntimers",
            "transport.connection_mode",
            "transport.multi_session",
            "transport.path_mtu_discovery",
            "ttl_security",
            "unsuppress_map",
            "update_source",
            "version",
            "weight",
            "activate",
            "additional_paths",
            "advertise.additional_paths",
            "advertise.best_external",
            "advertise.diverse_path",
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
            "default_originate",
            "default_originate.route_map",
            "distribute_list",
            "dmzlink_bw",
            "filter_list",
            "maximum_prefix",
            "next_hop_self.set",
            "next_hop_self.all",
            "next_hop_unchanged.set",
            "next_hop_unchanged.allpaths",
            "remove_private_as.set",
            "remove_private_as.all",
            "remove_private_as.replace_as",
            "route_reflector_client",
            "route_server_client.set",
            "route_server_client.context",
            "send_community.set",
            "send_community.both",
            "send_community.extended",
            "send_community.standard",
            "send_label.set",
            "send_label.explicit_null",
            "slow_peer.detection",
            "slow_peer.split_update_group",
            "translate_update.set",
            "translate_update.nlri",
        ]

        for name, w_neighbor in want.items():
            have_nbr = have.pop(name, {})
            want_route = w_neighbor.pop("route_maps", {})
            have_route = have_nbr.pop("route_maps", {})
            self.compare(parsers=neig_parses, want=w_neighbor, have=have_nbr)
            if want_route:
                for k_rmps, w_rmps in want_route.items():
                    have_rmps = have_route.pop(k_rmps, {})
                    w_rmps["neighbor_address"] = w_neighbor.get("neighbor_address")
                    if have_rmps:
                        have_rmps["neighbor_address"] = have_nbr.get("neighbor_address")
                        have_rmps = {"route_maps": have_rmps}
                    self.compare(
                        parsers=["route_maps"],
                        want={"route_maps": w_rmps},
                        have=have_rmps,
                    )
        for name, h_neighbor in have.items():
            self.compare(parsers="neighbor_address", want={}, have=h_neighbor)

    def _compare_generic_lists(self, w_attr, h_attr, parser):
        """Handling of gereric list options."""
        for wkey, wentry in iteritems(w_attr):
            if wentry != h_attr.pop(wkey, {}):
                self.addcmd(wentry, parser, False)

        # remove remaining items in have for replaced state
        for hkey, hentry in iteritems(h_attr):
            self.addcmd(hentry, parser, True)

    def _bgp_global_list_to_dict(self, tmp_data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "aggregate_addresses": "address",
            "inject_maps": "name",
            "distributes": ["acl", "gateway", "prefix"],
            "neighbors": "neighbor_address",
            "route_maps": "name",
            "networks": "address",
            "bgp": None,
            "redistribute": [
                "application",
                "bgp",
                "eigrp",
                "isis",
                "iso_igrp",
                "ospf",
                "ospfv3",
                "vrf",
            ],
        }
        for k, _v in p_key.items():
            if tmp_data.get(k) and k not in ["distributes", "redistribute", "bgp"]:
                if k == "neighbors":
                    for neb in tmp_data.get("neighbors"):
                        neb = self._bgp_global_list_to_dict(neb)
                        _ntimer = neb.pop("timers", {})
                        if _ntimer:
                            neb["ntimers"] = _ntimer
                tmp_data[k] = {str(i[p_key[k]]): i for i in tmp_data[k]}
            elif tmp_data.get("distributes") and k == "distributes":
                tmp_data[k] = {str("".join([i.get(j, "") for j in _v])): i for i in tmp_data[k]}
            elif tmp_data.get("redistribute") and k == "redistribute":
                tmp_data[k] = {
                    str(
                        [
                            ky + vl.get("name", "") + vl.get("process_id", "") if ky in _v else ky
                            for ky, vl in i.items()
                        ][0],
                    ): i
                    for i in tmp_data[k]
                }
            elif tmp_data.get("bgp") and k == "bgp":
                tmp_data[k] = self._bgp_global_list_to_dict(tmp_data.get(k))
        return tmp_data

    def handle_deprecates(self, want, is_nbr=False):
        """
        Handles deprecated values post rewrite
        aggregate_address [dict] - aggregate_addresses [list:dict]
        bgp.bestpath [list:dict] - bgp.bestpath_options [dict]
        bgp.inject_map [dict] - bgp.inject_map [list:dict]
        bgp.listen.(ipv4/v6_with_subnet) [multiple] - bgp.listen.host_with_subnet
        bgp.nopeerup_delay [list:dict] - bgp.nopeerup_delay_option [dict]
        distributed_list [dict] - distributes [list:dict]
        neighbor.address.(tag/ipv4/v6_address) [multiple] - neighbor.address.neighbor_address
        neighbor.password [str] - neighbor.password [dict]
        neighbor.route_map [dict] - neighbor.route_maps [list:dict]

        Args:
            want (_type_): Handle want attributes for deprecated values
            is_nbr (bool, optional): activates neighbor part on recursion. Defaults to False.
        """
        if not is_nbr:
            if want.get("aggregate_address"):
                if want.get("aggregate_addresses"):
                    want["aggregate_addresses"].append(want.pop("aggregate_address"))
                else:
                    want["aggregate_addresses"] = [want.pop("aggregate_address")]
            if want.get("bgp"):
                _want_bgp = want.get("bgp", {})
                if _want_bgp.get("bestpath"):
                    bpath = {}
                    for i in _want_bgp.pop("bestpath"):
                        bpath = dict_merge(bpath, i)
                    _want_bgp["bestpath_options"] = bpath
                if _want_bgp.get("nopeerup_delay"):
                    npdelay = {}
                    for i in _want_bgp.pop("nopeerup_delay"):
                        npdelay = dict_merge(npdelay, i)
                    _want_bgp["nopeerup_delay_options"] = npdelay
                if _want_bgp.get("inject_map"):
                    if _want_bgp.get("inject_maps"):
                        _want_bgp["inject_maps"].append(_want_bgp.pop("inject_map"))
                    else:
                        _want_bgp["inject_maps"] = [_want_bgp.pop("inject_map")]
                if _want_bgp.get("listen", {}).get("range"):
                    if _want_bgp.get("listen").get("range").get("ipv4_with_subnet"):
                        _want_bgp["listen"]["range"]["host_with_subnet"] = _want_bgp["listen"][
                            "range"
                        ].pop("ipv4_with_subnet")
                    elif _want_bgp.get("listen").get("range").get("ipv6_with_subnet"):
                        _want_bgp["listen"]["range"]["host_with_subnet"] = _want_bgp["listen"][
                            "range"
                        ].pop("ipv6_with_subnet")
            if want.get("distribute_list"):
                if want.get("distributes"):
                    want["distributes"].append(want.pop("distribute_list"))
                else:
                    want["distributes"] = [want.pop("distribute_list")]
            if want.get("neighbors"):
                _want_nbrs = want.get("neighbors", {})
                for nbr in _want_nbrs:
                    nbr = self.handle_deprecates(nbr, is_nbr=True)
        else:
            if want.get("address"):
                want["neighbor_address"] = want.pop("address")
            if want.get("tag"):
                want["neighbor_address"] = want.pop("tag")
            if want.get("ipv6_adddress"):
                want["neighbor_address"] = want.pop("ipv6_adddress")
            if want.get("route_map"):
                if want.get("route_maps"):
                    want["route_maps"].append(want.pop("route_map"))
                else:
                    want["route_maps"] = [want.pop("route_map")]
            if want.get("password"):
                want["password_options"] = {"pass_key": want.pop("password")}
