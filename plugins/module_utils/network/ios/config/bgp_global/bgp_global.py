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
        if self.want:
            wantd = {self.want["as_number"]: self.want}
        else:
            wantd = {}
        if self.have:
            haved = {self.have["as_number"]: self.have}
        else:
            haved = {}

        wantd, haved = self.list_to_dict(wantd, haved)
        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted" and self.have:
            if (
                not self.want
                or self.have.get("as_number") == self.want.get("as_number")
                and len(self.have) > 1
            ):
                self.addcmd(
                    {"as_number": haved[list(haved)[0]].pop("as_number")},
                    "as_number",
                    False,
                )
                self.compare(parsers=self.parsers, want={}, have=haved[list(haved)[0]])
                self._compare(want={}, have=haved[list(haved)[0]])
                self._list_params_compare(want={}, have=haved[list(haved)[0]])
            wantd = {}

        if self.state == "purged" and self.have:
            if (
                not self.want
                or (self.have.get("as_number") == self.want.get("as_number"))
                and len(self.have) >= 1
            ):
                self.addcmd(
                    {"as_number": haved[list(haved)[0]].pop("as_number")},
                    "as_number",
                    True,
                )
                wantd = {}

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Ospf_interfaces network resource.
        """
        if want != have and self.state != "deleted":
            self.addcmd(have, "as_number", False)
            self.compare(parsers=self.parsers, want=want, have=have)
            self._bgp_config_compare(want.get("bgp"), have.get("bgp"))
            self._list_params_compare(want, have)
        elif self.state == "deleted":
            self._bgp_config_compare(dict(), have.get("bgp"))

    def _bgp_config_compare(self, want, have):
        if want and have and want != have and isinstance(want, dict):
            set_have = True
            for k, val in iteritems(want):
                if isinstance(val, dict):
                    if k in have:
                        self.compare(
                            parsers=["bgp.config"],
                            want={"bgp": {k: val}},
                            have={"bgp": {k: have[k]}},
                        )
                    if k in have and self.state == "replaced":
                        if set_have:
                            self.compare(
                                parsers=["bgp.config"],
                                want=dict(),
                                have={"bgp": {k: have[k]}},
                            )
                        self.compare(
                            parsers=["bgp.config"],
                            want={"bgp": {k: val}},
                            have={"bgp": {k: have[k]}},
                        )
                    else:
                        self.compare(
                            parsers=["bgp.config"], want={"bgp": {k: val}}, have=dict()
                        )
        elif want and not have:
            for k, val in iteritems(want):
                if not isinstance(val, list):
                    self.compare(
                        parsers=["bgp.config"], want={"bgp": {k: val}}, have=dict()
                    )
        elif not want and have:
            for k, val in iteritems(have):
                if not isinstance(val, list):
                    self.compare(
                        parsers=["bgp.config"], want=dict(), have={"bgp": {k: val}}
                    )

    def _list_params_compare(self, want, have):
        def multi_compare(parser, want, have):
            if want:
                dict_iter = want
            else:
                dict_iter = have
            for k, v in iteritems(dict_iter):
                if parser == "neighbor":
                    type = None
                    if want.get("address") or have.get("address"):
                        type = "address"
                        want_type_val = want.get("address")
                        have_type_val = have.get("address")
                    if want.get("tag") or have.get("tag"):
                        type = "tag"
                        want_type_val = want.get("tag")
                        have_type_val = have.get("tag")
                    if want.get("ipv6_adddress") or have.get("ipv6_address"):
                        type = "ipv6_adddress"
                        want_type_val = want.get("ipv6_adddress")
                        have_type_val = have.get("ipv6_adddress")
                    if want and have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v, type: want_type_val}},
                            have={parser: {k: have.get(k, {}), type: have_type_val}},
                        )
                    elif not have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v, type: want_type_val}},
                            have=dict(),
                        )
                    elif not want:
                        self.compare(
                            parsers=[parser],
                            want=dict(),
                            have={parser: {k: v, type: have_type_val}},
                        )
                if parser == "redistribute":
                    if want and have:
                        self.compare(
                            parsers=[parser],
                            want={parser: {k: v}},
                            have={parser: {k: have.get(k, {})}},
                        )
                    elif not have:
                        self.compare(
                            parsers=[parser], want={parser: {k: v}}, have=dict()
                        )
                    elif not want:
                        self.compare(
                            parsers=[parser], want=dict(), have={parser: {k: v}}
                        )

        for every in ["bgp", "neighbor", "redistribute"]:

            param_want = want.get(every)
            param_have = have.get(every)
            if param_want and param_want != param_have:
                set_have = True
                if every == "bgp":
                    for each in ["bestpath", "nopeerup_delay"]:
                        set_have = True
                        if param_want.get(each):
                            for k, v in iteritems(param_want.get(each)):
                                if (
                                    param_have
                                    and k in param_have.get(each)
                                    and self.state == "merged"
                                ):
                                    if k in param_have.get(each):
                                        self.compare(
                                            parsers=[every + "." + each],
                                            want={"bgp": {each: {k: v}}},
                                            have={
                                                "bgp": {
                                                    each: {
                                                        k: param_have.get(each, {})[k]
                                                    }
                                                }
                                            },
                                        )

                                elif param_have and self.state == "replaced":
                                    if set_have and param_have.get(each):
                                        if isinstance(each, dict):
                                            for (key_have, val_have) in iteritems(
                                                param_have.get(each)
                                            ):
                                                multi_compare(
                                                    parser=every,
                                                    want=dict(),
                                                    have=val_have,
                                                )
                                        else:
                                            temp = {}
                                            for i in list(param_have[each]):
                                                if i not in param_want[each]:
                                                    temp.update(
                                                        {each: {i: param_have[each][i]}}
                                                    )
                                            temp_have = temp
                                            temp = {}
                                            for i in list(param_want[each]):
                                                if i not in param_have[each]:
                                                    temp.update(
                                                        {each: {i: param_want[each][i]}}
                                                    )
                                            temp_want = temp
                                            if temp_have:
                                                self.compare(
                                                    parsers=[every + "." + each],
                                                    want=dict(),
                                                    have={"bgp": temp_have},
                                                )
                                            if temp_want:
                                                self.compare(
                                                    parsers=[every + "." + each],
                                                    want={"bgp": temp_want},
                                                    have=dict(),
                                                )
                                        set_have = False
                                else:
                                    self.compare(
                                        parsers=[every + "." + each],
                                        want={"bgp": {each: {k: v}}},
                                        have=dict(),
                                    )
                if every == "neighbor" or every == "redistribute":
                    for k, v in iteritems(param_want):
                        if every == "neighbor":
                            if param_have and self.state == "merged":
                                multi_compare(
                                    parser=every, want=v, have=param_have.pop(k, {})
                                )
                            elif param_have and self.state == "replaced":
                                if set_have:
                                    for key_have, val_have in iteritems(param_have):
                                        multi_compare(
                                            parser=every, want=dict(), have=val_have
                                        )
                                    set_have = False
                                multi_compare(parser=every, want=v, have=dict())
                            else:
                                multi_compare(parser=every, want=v, have=dict())
                            self.commands = (
                                [
                                    each
                                    for each in self.commands
                                    if "neighbor" not in each
                                ]
                                + [
                                    each
                                    for each in self.commands
                                    if "remote-as" in each and "neighbor" in each
                                ]
                                + [
                                    each
                                    for each in self.commands
                                    if "remote-as" not in each and "neighbor" in each
                                ]
                            )
                        elif every == "redistribute":
                            if param_have and self.state == "merged":
                                multi_compare(
                                    parser=every,
                                    want={k: v},
                                    have={k: param_have.pop(k, {})},
                                )
                            if param_have and self.state == "replaced":
                                if set_have:
                                    for key_have, val_have in iteritems(param_have):
                                        multi_compare(
                                            parser=every, want=dict(), have=val_have
                                        )
                                    set_have = False
                                multi_compare(parser=every, want={k: v}, have=dict())
                            else:
                                multi_compare(parser=every, want={k: v}, have=dict())
            elif param_have and self.state == "deleted":
                del_config_have = True
                if param_have:
                    for k, v in iteritems(param_have):
                        if every == "bgp" and del_config_have:
                            for each in ["bestpath", "nopeerup_delay"]:
                                if param_have.get(each):
                                    for k, v in iteritems(param_have.get(each)):
                                        self.compare(
                                            parsers=[every + "." + each],
                                            want=dict(),
                                            have={"bgp": {each: {k: v}}},
                                        )
                            del_config_have = False
                        elif every == "neighbor":
                            multi_compare(parser=every, want=dict(), have=v)
                        elif every == "redistribute":
                            if param_have:
                                multi_compare(parser=every, want=dict(), have={k: v})

    def list_to_dict(self, wantd, haved):
        for thing in wantd, haved:
            if thing:
                for key, val in iteritems(thing):
                    for every in ["bgp", "neighbor", "redistribute"]:
                        value = val.get(every)
                        if value:
                            if isinstance(value, dict):
                                for k, v in iteritems(val.get(every)):
                                    if isinstance(v, list):
                                        temp = dict()
                                        temp[k] = {}
                                        for each in v:
                                            temp[k].update(each)
                                        val[every][k] = temp[k]
                            elif isinstance(value, list):
                                temp = dict()
                                temp[every] = {}
                                for each in value:
                                    if every == "neighbor":
                                        if each.get("address"):
                                            temp[every].update(
                                                {each.get("address"): each}
                                            )
                                        elif each.get("tag"):
                                            temp[every].update({each.get("tag"): each})
                                        elif each.get("ipv6_adddress"):
                                            temp[every].update(
                                                {each.get("ipv6_adddress"): each}
                                            )
                                    elif every == "redistribute":
                                        temp[every].update(each)
                                val[every] = temp[every]
        return wantd, haved
