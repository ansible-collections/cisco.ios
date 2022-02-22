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


class Bgp_global(ResourceModule):
    """
    The cisco.ios_bgp_global config class
    """

    parsers = [
        "as_number",
        "aggregate_addresses",
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
        "distribute_lists",
        "maximum_paths.paths",
        "maximum_paths.eibgp",
        "maximum_paths.ibgp",
        "maximum_secondary_paths.paths",
        "maximum_secondary_paths.eibgp",
        "maximum_secondary_paths.ibgp",
        "networks",
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
        "bgp.bestpath.aigp",
        "bgp.bestpath.compare_routerid",
        "bgp.bestpath.cost_community",
        "bgp.bestpath.igp_metric",
        "bgp.bestpath.med",
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
        "bgp.graceful_shutdown",
        "bgp.inject_maps",
        "bgp.listen.limit",
        "bgp.listen.range",
        "bgp.log_neighbor_changes",
        "bgp.maxas_limit",
        "bgp.maxcommunity_limit",
        "bgp.maxextcommunity_limit",
        "bgp.nexthop.route_map",
        "bgp.nexthop.trigger.delay",
        "bgp.nexthop.trigger.enable",
        "bgp.nopeerup_delay.cold_boot",
        "bgp.nopeerup_delay.post_boot",
        "bgp.nopeerup_delay.nsf_switchover",
        "bgp.nopeerup_delay.user_initiated",
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
        "neighbors.remote_as",
        "neighbors.peer_group",
        "neighbors.bmp_activate",
        "neighbors.cluster_id",
        "neighbors.description",
        "neighbors.disable_connected_check",
        "neighbors.ebgp_multihop",
        "neighbors.fall_over.bfd",
        "neighbors.fall_over.route_map",
        "neighbors.ha_mode",
        "neighbors.inherit",
        "neighbors.local_as",
        "neighbors.log_neighbor_changes",
        "neighbors.password",
        "neighbors.path_attribute",
        "neighbors.shutdown",
        "neighbors.soft_reconfiguration",
        "neighbors.timers",
        "neighbors.transport.connection_mode",
        "neighbors.transport.multi_session",
        "neighbors.transport.path_mtu_discovery",
        "neighbors.ttl_security",
        "neighbors.unsuppress_map",
        "neighbors.update_source",
        "neighbors.version",
        "neighbors.weight",
        "neighbors.activate",
        "neighbors.additional_paths",
        "neighbors.advertise.additional_paths",
        "neighbors.advertise.best_external",
        "neighbors.advertise.diverse_path",
        "neighbors.advertise_map",
        "neighbors.advertisement_interval",
        "neighbors.aigp",
        "neighbors.aigp.send.cost_community",
        "neighbors.aigp.send.med",
        "neighbors.allow_policy",
        "neighbors.allowas_in",
        "neighbors.as_override",
        "neighbors.bmp_activate",
        "neighbors.capability",
        "neighbors.default_originate",
        "neighbors.default_originate.route_map",
        "neighbors.distribute_list",
        "neighbors.dmzlink_bw",
        "neighbors.filter_list",
        "neighbors.maximum_prefix",
        "neighbors.next_hop_self.set",
        "neighbors.next_hop_self.all",
        "neighbors.next_hop_unchanged.set",
        "neighbors.next_hop_unchanged.allpaths",
        "neighbors.remove_private_as.set",
        "neighbors.remove_private_as.all",
        "neighbors.remove_private_as.replace_as",
        "neighbors.route_maps",
        "neighbors.route_reflector_client",
        "neighbors.route_server_client.set",
        "neighbors.route_server_client.context",
        "neighbors.send_community.set",
        "neighbors.send_community.both",
        "neighbors.send_community.extended",
        "neighbors.send_community.standard",
        "neighbors.send_label.set",
        "neighbors.send_label.explicit_null",
        "neighbors.slow_peer.detection",
        "neighbors.slow_peer.split_update_group",
        "neighbors.translate_update.set",
        "neighbors.translate_update.nlri",
        "redistribute.application",
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
        "redistribute.vrf",
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
        if self.state in ["merged", "replaced"]:
            w_asn = self.want.get("as_number")
            h_asn = self.have.get("as_number")

            if h_asn and w_asn != h_asn:
                self._module.fail_json(
                    msg="BGP is already configured with ASN {0}. "
                    "Please remove it with state: purged before "
                    "configuring new ASN".format(h_asn)
                )

        if self.state in ["deleted", "replaced"]:
            self._build_af_data()

        for each in self.want, self.have:
            self._bgp_global_list_to_dict(each)

        # if state is deleted, clean up global params
        if self.state == "deleted":
            if not self.want or (
                self.have.get("as_number") == self.want.get("as_number")
            ):
                self._compare(want={}, have=self.have)

        elif self.state == "purged":
            if not self.want or (
                self.have.get("as_number") == self.want.get("as_number")
            ):
                self.addcmd(self.have or {}, "as_number", True)

        else:
            wantd = self.want
            # if state is merged, merge want onto have and then compare
            if self.state == "merged":
                wantd = dict_merge(self.have, self.want)

            self._compare(want=wantd, have=self.have)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_global network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)

    def _bgp_global_list_to_dict(self, tmp_data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "aggregate_addresses": "address",
            "inject_maps": "name",
            "distribute_lists": ["acl", "gateway", "prefix"],
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
            if tmp_data.get(k) and k not in [
                "distribute_lists",
                "redistribute",
                "bgp",
            ]:
                if k == "neighbors":
                    pass
                    # for neb in tmp_data.get("neighbors"):  # work here
                    #     tmp_data[k] = self._bgp_global_list_to_dict(neb)
                tmp_data[k] = {str(i[p_key[k]]): i for i in tmp_data[k]}
            elif tmp_data.get("distribute_lists") and k == "distribute_lists":
                tmp_data[k] = {
                    str("".join([i.get(j, "") for j in _v])): i
                    for i in tmp_data[k]
                }
            elif tmp_data.get("redistribute") and k == "redistribute":
                tmp_data[k] = {
                    str(
                        [
                            ky + vl.get("name", "") + vl.get("process_id", "")
                            if ky in _v
                            else ky
                            for ky, vl in i.items()
                        ][0]
                    ): i
                    for i in tmp_data[k]
                }
            elif tmp_data.get("bgp") and k == "bgp":
                tmp_data[k] = self._bgp_global_list_to_dict(tmp_data.get(k))
        return tmp_data
