# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Bgp_address_family parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_af(config_data):
    if "address_family" in config_data:
        cmd = "address-family {{ afi }}".format(**config_data["address_family"])
        if config_data["address_family"].get("safi"):
            cmd += " {{ safi }}".format(**config_data["address_family"])
        if config_data["address_family"].get("vrf"):
            cmd += " vrf {{ vrf }}".format(**config_data["address_family"])
        return cmd


def _tmplt_af_aggregate_address(config_data):
    if "aggregate_address" in config_data:
        cmd = "aggregate-address {address} {netmask}".format(**config_data["aggregate_address"])
        if "advertise_map" in config_data["aggregate_address"]:
            cmd += " advertise-map {advertise_map}".format(**config_data["aggregate_address"])
        if "as_confed_set" in config_data["aggregate_address"]:
            cmd += " as-confed-set"
        if "as_set" in config_data["aggregate_address"]:
            cmd += " as-set"
        if "attribute_map" in config_data["aggregate_address"]:
            cmd += " attribute-map {attribute_map}".format(**config_data["aggregate_address"])
        if "summary_only" in config_data["aggregate_address"]:
            cmd += " summary-only"
        if "suppress_map" in config_data["aggregate_address"]:
            cmd += " suppress-map {suppress_map}".format(**config_data["aggregate_address"])

        return cmd


def _tmplt_bgp_af_additional_paths(config_data):
    if "bgp" in config_data:
        if "additional_paths" in config_data["bgp"]:
            cmd = "bgp additional-paths"
            if "install" in config_data["bgp"]["additional_paths"]:
                cmd += " install"
            elif "select" in config_data["bgp"]["additional_paths"]:
                cmd += " select"
                if "all" in config_data["bgp"]["additional_paths"]["select"]:
                    cmd += " all"
                elif "best" in config_data["bgp"]["additional_paths"]["select"]:
                    cmd += " best {best}".format(**config_data["bgp"]["additional_paths"]["select"])
                elif "best_external" in config_data["bgp"]["additional_paths"]["select"]:
                    cmd += " best-external"
                elif "group_best" in config_data["bgp"]["additional_paths"]["select"]:
                    cmd += " group-best"
            if "receive" in config_data["bgp"]["additional_paths"]:
                cmd += " receive"
            if "send" in config_data["bgp"]["additional_paths"]:
                cmd += " send"
            return cmd


def _tmplt_bgp_af_config(config_data):
    if "bgp" in config_data:
        cmd = []
        if config_data["bgp"].get("aggregate_timer"):
            cmd.append("bgp aggregate-timer {aggregate_timer}".format(**config_data["bgp"]))
        if config_data["bgp"].get("dmzlink_bw"):
            cmd.append("bgp dmzlink-bw")
        if "nexthop" in config_data["bgp"]:
            command = "bgp nexthop"
            if "route_map" in config_data["bgp"]["nexthop"]:
                command += " route-map {route_map}".format(**config_data["bgp"]["nexthop"])
            elif "trigger" in config_data["bgp"]["nexthop"]:
                if config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger delay {delay}".format(
                        **config_data["bgp"]["nexthop"]["trigger"]
                    )
                elif config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger enable"
            cmd.append(command)
        if config_data["bgp"].get("redistribute_internal"):
            cmd.append("bgp redistribute-internal")
        if config_data["bgp"].get("route_map"):
            cmd.append("bgp route-map priority")
        if config_data["bgp"].get("scan_time"):
            cmd.append("bgp scan-time {scan_time}".format(**config_data["bgp"]))
        if config_data["bgp"].get("soft_reconfig_backup"):
            cmd.append("bgp soft-reconfig-backup")
        if config_data["bgp"].get("update_group"):
            cmd.append("bgp update-group split as-override")
        return cmd


def _tmplt_bgp_af_dampening(config_data):
    if "bgp" in config_data and "dampening" in config_data["bgp"]:
        if config_data["bgp"]["dampening"].get("penalty_half_time"):
            command = "bgp dampening {penalty_half_time}".format(**config_data["bgp"]["dampening"])
            if config_data["bgp"]["dampening"].get("reuse_route_val"):
                command += " {reuse_route_val}".format(**config_data["bgp"]["dampening"])
            if config_data["bgp"]["dampening"].get("suppress_route_val"):
                command += " {suppress_route_val}".format(**config_data["bgp"]["dampening"])
            if config_data["bgp"]["dampening"].get("max_suppress"):
                command += " {max_suppress}".format(**config_data["bgp"]["dampening"])
        elif config_data["bgp"]["dampening"].get("route_map"):
            command = "bgp dampening {route_map}".format(**config_data["bgp"]["dampening"])
        return command


def _tmplt_bgp_af_slow_peer(config_data):
    if "bgp" in config_data and "slow_peer" in config_data["bgp"]:
        if "slow_peer" in config_data["bgp"]:
            cmd = "bgp slow-peer"
            if "detection" in config_data["bgp"]["slow_peer"]:
                cmd += " detection"
                if "threshold" in config_data["bgp"]["slow_peer"]["detection"]:
                    cmd += " threshold {threshold}".format(
                        **config_data["bgp"]["slow_peer"]["detection"]
                    )
            elif "split_update_group" in config_data["bgp"]["slow_peer"]:
                cmd += " split-update-group"
                if "dynamic" in config_data["bgp"]["slow_peer"]["split_update_group"]:
                    cmd += " dynamic"
                    if "permanent" in config_data["bgp"]["slow_peer"]["split_update_group"]:
                        cmd += " permanent {permanent}".format(
                            **config_data["bgp"]["slow_peer"]["split_update_group"]
                        )
        return cmd


def _tmplt_af_distance(config_data):
    if config_data.get("distance"):
        cmd = "distance bgp {external} {internal} {local}".format(**config_data["distance"])
        return cmd


def _tmplt_af_neighbor(config_data):
    if "neighbor" in config_data:
        commands = []
        cmd = "neighbor"
        if "address" in config_data["neighbor"]:
            cmd += " {address}".format(**config_data["neighbor"])
        elif "tag" in config_data["neighbor"]:
            cmd += " {tag}".format(**config_data["neighbor"])
        elif "ipv6_adddress" in config_data["neighbor"]:
            cmd += " {ipv6_adddress}".format(**config_data["neighbor"])
        if "peer_group" in config_data["neighbor"]:
            commands.append("{0} peer-group {peer_group}".format(cmd, **config_data["neighbor"]))
        if "remote_as" in config_data["neighbor"]:
            commands.append("{0} remote-as {remote_as}".format(cmd, **config_data["neighbor"]))
        if "activate" in config_data["neighbor"]:
            commands.append("{0} activate".format(cmd))
        if "additional_paths" in config_data["neighbor"]:
            self_cmd = "{0} additional-paths".format(cmd)
            if "disable" in config_data["neighbor"]["additional_paths"]:
                self_cmd += " disable"
            elif "receive" in config_data["neighbor"]["additional_paths"]:
                self_cmd += " receive"
            elif "send" in config_data["neighbor"]["additional_paths"]:
                self_cmd += " send"
            commands.append(self_cmd)
        if "advertise" in config_data["neighbor"]:
            self_cmd = "{0} advertise".format(cmd)
            if "additional_paths" in config_data["neighbor"]["advertise"]:
                self_cmd += " additional-paths"
                if "all" in config_data["neighbor"]["advertise"]["additional_paths"]:
                    self_cmd += " all"
                elif "best" in config_data["neighbor"]["advertise"]["additional_paths"]:
                    self_cmd += " best {best}".format(
                        **config_data["neighbor"]["advertise"]["additional_paths"]
                    )
                elif "group_best" in config_data["neighbor"]["advertise"]["additional_paths"]:
                    self_cmd += " group-best"
            elif "best_external" in config_data["neighbor"]["advertise"]:
                self_cmd += " best-external"
            elif "diverse_path" in config_data["neighbor"]["advertise"]:
                self_cmd += "diverse-path"
                if "backup" in config_data["neighbor"]["advertise"]["diverse_path"]:
                    self_cmd += " backup"
                elif "mpath" in config_data["neighbor"]["advertise"]["diverse_path"]:
                    self_cmd += " mpath"
            commands.append(self_cmd)
        if config_data["neighbor"].get("advertise_map"):
            self_cmd = "{0} advertise-map {name}".format(
                cmd, **config_data["neighbor"]["advertise_map"]
            )
            if "exist_map" in config_data["neighbor"]["advertise_map"]:
                self_cmd += " exist-map {exist_map}".format(
                    **config_data["neighbor"]["advertise_map"]
                )
            elif "non_exist_map" in config_data["neighbor"]["advertise_map"]:
                self_cmd += " exist-map {non_exist_map}".format(
                    **config_data["neighbor"]["advertise_map"]
                )
            commands.append(self_cmd)
        if config_data["neighbor"].get("advertisement_interval"):
            commands.append(
                "{0} advertisement-interval {advertisement_interval}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get("aigp"):
            self_cmd = "{0} aigp".format(cmd)
            if config_data["neighbor"]["aigp"].get("send"):
                self_cmd += " send"
                if config_data["neighbor"]["aigp"]["send"].get("cost_community"):
                    self_cmd += " cost-community {id}".format(
                        **config_data["neighbor"]["aigp"]["send"]["cost_community"]
                    )
                    if config_data["neighbor"]["aigp"]["send"]["cost_community"].get("poi"):
                        self_cmd += " poi"
                        if config_data["neighbor"]["aigp"]["send"]["cost_community"]["poi"].get(
                            "igp_cost"
                        ):
                            self_cmd += " igp-cost"
                        if config_data["neighbor"]["aigp"]["send"]["cost_community"]["poi"].get(
                            "pre_bestpath"
                        ):
                            self_cmd += " pre-bestpath"
                        if config_data["neighbor"]["aigp"]["send"]["cost_community"]["poi"].get(
                            "transitive"
                        ):
                            self_cmd += " transitive"
                if config_data["neighbor"]["aigp"]["send"].get("med"):
                    self_cmd += " med"
            commands.append(self_cmd)
        if config_data["neighbor"].get("allow_policy"):
            commands.append("{0} allow-policy".format(cmd))
        if config_data["neighbor"].get("allowas_in"):
            commands.append("{0} allowas-in {allowas_in}".format(cmd, **config_data["neighbor"]))
        if config_data["neighbor"].get("as_override"):
            commands.append("{0} as-override".format(cmd))
        if "bmp_activate" in config_data["neighbor"]:
            self_cmd = "{0} bmp-activate".format(cmd)
            if config_data["neighbor"]["bmp_activate"].get("all"):
                self_cmd += " all"
            if "server" in config_data["neighbor"]["bmp_activate"]:
                self_cmd += " server {server}".format(**config_data["neighbor"]["bmp_activate"])
            commands.append(self_cmd)
        if "capability" in config_data["neighbor"]:
            self_cmd = "{0} capability".format(cmd)
            if config_data["neighbor"]["capability"].get("both"):
                self_cmd += " both"
            elif config_data["neighbor"]["capability"].get("receive"):
                self_cmd += " receive"
            elif config_data["neighbor"]["capability"].get("send"):
                self_cmd += " send"
            commands.append(self_cmd)
        if config_data["neighbor"].get("cluster_id"):
            commands.append("{0} cluster-id {cluster_id}".format(cmd, **config_data["neighbor"]))
        if "default_originate" in config_data["neighbor"]:
            self_cmd = "{0} default-originate".format(cmd)
            if config_data["neighbor"]["default_originate"].get("route_map"):
                self_cmd += " route-map {route_map}".format(
                    **config_data["neighbor"]["default_originate"]
                )
            commands.append(self_cmd)
        if "description" in config_data["neighbor"]:
            commands.append("{0} description {description}".format(cmd, **config_data["neighbor"]))
        if config_data["neighbor"].get("disable_connected_check"):
            commands.append("{0} disable-connected-check".format(cmd))
        if "distribute_list" in config_data["neighbor"]:
            self_cmd = "{0} distribute-list".format(cmd)
            if "acl" in config_data["neighbor"]["distribute_list"]:
                self_cmd += " {acl}".format(**config_data["neighbor"]["distribute_list"])
            if config_data["neighbor"]["distribute_list"].get("in"):
                self_cmd += " in"
            elif config_data["neighbor"]["distribute_list"].get("out"):
                self_cmd += " out"
            commands.append(self_cmd)
        if config_data["neighbor"].get("dmzlink_bw"):
            commands.append("{0} dmzlink-bw".format(cmd))
        if "ebgp_multihop" in config_data["neighbor"]:
            self_cmd = "{0} ebgp-multihop".format(cmd)
            if "hop_count" in config_data["neighbor"]["ebgp_multihop"]:
                self_cmd += " {hop_count}".format(**config_data["neighbor"]["ebgp_multihop"])
            commands.append(self_cmd)
        if "fall_over" in config_data["neighbor"]:
            self_cmd = "{0} fall-over".format(cmd)
            if "bfd" in config_data["neighbor"]["fall_over"]:
                self_cmd += " bfd"
                if config_data["neighbor"]["fall_over"]["bfd"].get("multi_hop"):
                    self_cmd += " multi-hop"
                elif config_data["neighbor"]["fall_over"]["bfd"].get("single_hop"):
                    self_cmd += " single-hop"
            elif "route_map" in config_data["neighbor"]["fall_over"]:
                self_cmd += " {route_map}".format(**config_data["neighbor"]["route_map"])
            commands.append(self_cmd)
        if "filter_list" in config_data["neighbor"]:
            self_cmd = "{0} filter-list".format(cmd)
            if "path_acl" in config_data["neighbor"]["filter_list"]:
                self_cmd += " {path_acl}".format(**config_data["neighbor"]["filter_list"])
            if config_data["neighbor"]["filter_list"].get("in"):
                self_cmd += " in"
            elif config_data["neighbor"]["filter_list"].get("out"):
                self_cmd += " out"
            commands.append(self_cmd)
        if "ha_mode" in config_data["neighbor"]:
            self_cmd = "{0} ha-mode".format(cmd)
            if config_data["neighbor"]["ha_mode"].get("disable"):
                self_cmd += " disable"
            commands.append(self_cmd)
        if "inherit" in config_data["neighbor"]:
            self_cmd = "{0} inherit {inherit}".format(cmd, **config_data["neighbor"])
            commands.append(self_cmd)
        if config_data["neighbor"].get("local_as"):
            self_cmd = "{0} local-as".format(cmd)
            if "number" in config_data["neighbor"]["local_as"]:
                self_cmd += " {number}".format(**config_data["neighbor"]["local_as"])
            if config_data["neighbor"]["local_as"].get("dual_as"):
                self_cmd += " dual-as"
            elif config_data["neighbor"]["local_as"].get("no_prepend"):
                self_cmd += " no-prepend"
                if config_data["neighbor"]["local_as"]["no_prepend"]:
                    self_cmd += " replace-as"
            commands.append(self_cmd)
        if "log_neighbor_changes" in config_data["neighbor"]:
            self_cmd = "{0} log-neighbor-changes".format(cmd)
            if config_data["neighbor"]["log_neighbor_changes"].get("disable"):
                self_cmd += " disable"
            commands.append(self_cmd)
        if "maximum_prefix" in config_data["neighbor"]:
            self_cmd = "{0} maximum-prefix".format(cmd)
            if "number" in config_data["neighbor"]["maximum_prefix"]:
                self_cmd += " {number}".format(**config_data["neighbor"]["maximum_prefix"])
            if "threshold_value" in config_data["neighbor"]["maximum_prefix"]:
                self_cmd += " {threshold_value}".format(**config_data["neighbor"]["maximum_prefix"])
            if config_data["neighbor"]["maximum_prefix"].get("restart"):
                self_cmd += " restart {restart}".format(**config_data["neighbor"]["maximum_prefix"])
            elif config_data["neighbor"]["filter_list"].get("warning_only"):
                self_cmd += " warning-only"
            commands.append(self_cmd)
        if "nexthop_self" in config_data["neighbor"]:
            self_cmd = "{0} next-hop-self".format(cmd)
            if config_data["neighbor"]["nexthop_self"].get("all"):
                self_cmd += " all"
            commands.append(self_cmd)
        if "next_hop_unchanged" in config_data["neighbor"]:
            self_cmd = "{0} next-hop-unchanged".format(cmd)
            if config_data["neighbor"]["next_hop_unchanged"].get("allpaths"):
                self_cmd += " allpaths"
            commands.append(self_cmd)
        if (
            "prefix_list" in config_data["neighbor"]
            and "prefix_lists" not in config_data["neighbor"]
        ):
            self_cmd = "{0} prefix-list {name}".format(
                cmd, **config_data["neighbor"]["prefix_list"]
            )
            if config_data["neighbor"]["prefix_list"].get("in"):
                self_cmd += " in"
            elif config_data["neighbor"]["prefix_list"].get("out"):
                self_cmd += " out"
            commands.append(self_cmd)
        if "peer_group" in config_data["neighbor"]:
            commands.append("{0} peer-group {peer_group}".format(cmd, **config_data["neighbor"]))
        if "remove_private_as" in config_data["neighbor"]:
            self_cmd = "{0} remove-private-as".format(cmd)
            if config_data["neighbor"]["remove_private_as"].get("all"):
                self_cmd += " all"
            elif config_data["neighbor"]["remove_private_as"].get("replace_as"):
                self_cmd += " replace_as"
            commands.append(self_cmd)
        if "route_map" in config_data["neighbor"] and "route_maps" not in config_data["neighbor"]:
            self_cmd = "{0} route-map".format(cmd)
            if "name" in config_data["neighbor"]["route_map"]:
                self_cmd += " {name}".format(**config_data["neighbor"]["route_map"])
            if "in" in config_data["neighbor"]["route_map"]:
                self_cmd += " in"
            elif "out" in config_data["neighbor"]["route_map"]:
                self_cmd += " out"
            commands.append(self_cmd)
        if "route_reflector_client" in config_data["neighbor"]:
            commands.append("{0} route-reflector-client".format(cmd))
        if "route_server_client" in config_data["neighbor"]:
            self_cmd = "{0} route-server-client".format(cmd)
            commands.append(self_cmd)
        if "send_community" in config_data["neighbor"]:
            self_cmd = "{0} send-community".format(cmd)
            if config_data["neighbor"]["send_community"].get("both"):
                self_cmd += " both"
            elif config_data["neighbor"]["send_community"].get("extended"):
                self_cmd += " extended"
            elif config_data["neighbor"]["send_community"].get("standard"):
                self_cmd += " standard"
            commands.append(self_cmd)
        if "soft_reconfiguration" in config_data["neighbor"]:
            commands.append("{0} soft-reconfiguration inbound".format(cmd))
        if "soo" in config_data["neighbor"]:
            commands.append("{0} soo {soo}".format(cmd, **config_data["neighbor"]))
        if "unsuppress_map" in config_data["neighbor"]:
            commands.append(
                "{0} unsuppress-map {unsuppress_map}".format(cmd, **config_data["neighbor"])
            )
        if "version" in config_data["neighbor"]:
            commands.append("{0} version {version}".format(cmd, **config_data["neighbor"]))
        if "weight" in config_data["neighbor"]:
            commands.append("{0} weight {weight}".format(cmd, **config_data["neighbor"]))
        return commands


def _tmplt_neighbor_af_prefix_lists(config_data):
    if "prefix_lists" in config_data["neighbor"]:
        cmd = "neighbor"
        if "address" in config_data["neighbor"]:
            cmd += " {address}".format(**config_data["neighbor"])
        elif "tag" in config_data["neighbor"]:
            cmd += " {tag}".format(**config_data["neighbor"])
        elif "ipv6_adddress" in config_data["neighbor"]:
            cmd += " {ipv6_adddress}".format(**config_data["neighbor"])
        cmd = "{0} prefix-list {name}".format(cmd, **config_data["neighbor"]["prefix_lists"])
        if config_data["neighbor"]["prefix_lists"].get("in"):
            cmd += " in"
        elif config_data["neighbor"]["prefix_lists"].get("out"):
            cmd += " out"
        return cmd


def _tmplt_neighbor_af_route_maps(config_data):
    if (
        "neighbor" in config_data
        and "route_maps" in config_data["neighbor"]
        and len(config_data["neighbor"]) == 2
    ):
        cmd = "neighbor"
        if "address" in config_data["neighbor"]:
            cmd += " {address}".format(**config_data["neighbor"])
        elif "tag" in config_data["neighbor"]:
            cmd += " {tag}".format(**config_data["neighbor"])
        elif "ipv6_adddress" in config_data["neighbor"]:
            cmd += " {ipv6_adddress}".format(**config_data["neighbor"])
        cmd = "{0} route-map".format(cmd)
        if "name" in config_data["neighbor"]["route_maps"]:
            cmd += " {name}".format(**config_data["neighbor"]["route_maps"])
        if "in" in config_data["neighbor"]["route_maps"]:
            cmd += " in"
        elif "out" in config_data["neighbor"]["route_maps"]:
            cmd += " out"
        return cmd


def _tmplt_neighbor_af_slow_peer(config_data):
    if "neighbor" in config_data and "slow_peer" in config_data["neighbor"]:
        cmd = "neighbor"
        if "address" in config_data["neighbor"]:
            cmd += " {address}".format(**config_data["neighbor"])
        elif "tag" in config_data["neighbor"]:
            cmd += " {tag}".format(**config_data["neighbor"])
        elif "ipv6_adddress" in config_data["neighbor"]:
            cmd += " {ipv6_adddress}".format(**config_data["neighbor"])
        cmd = "{0} slow-peer".format(cmd)
        if "detection" in config_data["neighbor"]["slow_peer"]:
            cmd += " detection"
            if "disable" in config_data["neighbor"]["slow_peer"]["detection"]:
                cmd += " disable"
            elif "threshold" in config_data["neighbor"]["slow_peer"]["detection"]:
                cmd += " threshold {threshold}".format(
                    **config_data["neighbor"]["slow_peer"]["detection"]
                )
        elif "split_update_group" in config_data["neighbor"]["slow_peer"]:
            cmd += " split-update-group"
            if "dynamic" in config_data["neighbor"]["slow_peer"]["split_update_group"]:
                cmd += " dynamic"
                if (
                    "disable"
                    in config_data["neighbor"]["slow_peer"]["split_update_group"]["dynamic"]
                ):
                    cmd += " disable"
                elif (
                    "permanent"
                    in config_data["neighbor"]["slow_peer"]["split_update_group"]["dynamic"]
                ):
                    cmd += " permanent"
            elif "static" in config_data["neighbor"]["slow_peer"]["split_update_group"]:
                cmd += " static"
        return cmd


def _tmplt_af_network(config_data):
    if "network" in config_data:
        cmd = "network {address}".format(**config_data["network"])
        if "mask" in config_data["network"]:
            cmd += " mask {mask}".format(**config_data["network"])
        if "backdoor" in config_data["network"]:
            cmd += " backdoor"
        if "route_map" in config_data["network"]:
            cmd += " route-map {route_map}".format(**config_data["network"])
        return cmd


def _tmplt_af_snmp(config_data):
    if "snmp" in config_data:
        cmd = "snmp context {name}".format(**config_data["snmp"])
        if config_data["snmp"].get("community"):
            cmd += " community {snmp_community}".format(**config_data["snmp"]["community"])
            if config_data["snmp"]["community"].get("ro"):
                cmd += " ro"
            elif config_data["snmp"]["community"].get("rw"):
                cmd += " rw"
            if config_data["snmp"]["community"].get("acl"):
                cmd += " {acl}".format(**config_data["snmp"]["community"])
            elif config_data["snmp"]["community"].get("ipv6"):
                cmd += " ipv6 {ipv6}".format(**config_data["snmp"]["community"])
        if config_data["snmp"].get("user"):
            cmd += " user {name}".format(**config_data["snmp"]["user"])
            if config_data["snmp"]["user"].get("credential"):
                cmd += " credential"
            elif config_data["snmp"]["user"].get("encrypted"):
                cmd += " encrypted"
            if config_data["snmp"]["user"].get("auth"):
                cmd += " auth"
                if config_data["snmp"]["user"]["auth"].get("md5"):
                    cmd += " md5 {md5}".format(**config_data["snmp"]["user"]["auth"])
                elif config_data["snmp"]["user"]["auth"].get("sha"):
                    cmd += " sha {sha}".format(**config_data["snmp"]["user"]["auth"])
            if config_data["snmp"]["user"].get("access"):
                cmd += " access"
                if config_data["snmp"]["user"]["access"].get("acl"):
                    cmd += " {acl}".format(**config_data["snmp"]["user"]["access"])
                elif config_data["snmp"]["user"]["access"].get("ipv6"):
                    cmd += " ipv6 {ipv6}".format(**config_data["snmp"]["user"]["access"])
            if config_data["snmp"]["user"].get("priv"):
                cmd += " priv"
                if config_data["snmp"]["user"]["priv"].get("3des"):
                    cmd += " 3des {3des}".format(**config_data["snmp"]["user"]["priv"])
                elif config_data["snmp"]["user"]["priv"].get("des"):
                    cmd += " des {des}".format(**config_data["snmp"]["user"]["priv"])
                elif config_data["snmp"]["user"]["priv"].get("aes"):
                    cmd += " aes"
                    if config_data["snmp"]["user"]["priv"]["aes"].get("128"):
                        cmd += " 128 {128}".format(**config_data["snmp"]["user"]["priv"]["aes"])
                    if config_data["snmp"]["user"]["priv"]["aes"].get("192"):
                        cmd += " 192 {192}".format(**config_data["snmp"]["user"]["priv"]["aes"])
                    if config_data["snmp"]["user"]["priv"]["aes"].get("256"):
                        cmd += " 256 {256}".format(**config_data["snmp"]["user"]["priv"]["aes"])
        return cmd


def _tmplt_af_table_map(config_data):
    if "table_map" in config_data:
        cmd = "table-map {name}".format(**config_data["table_map"])
        if config_data["table_map"].get("filter"):
            cmd += " filter"
        return cmd


def _tmplt_af_redistribute(config_data):
    if "redistribute" in config_data:
        commands = []

        def common_config(command, param):
            if config_data["redistribute"][param].get("metric"):
                command += " metric {metric}".format(**config_data["redistribute"][param])
            if config_data["redistribute"][param].get("route_map"):
                command += " route-map {route_map}".format(**config_data["redistribute"][param])
            commands.append(command)

        command = "redistribute"
        if config_data["redistribute"].get("application"):
            cmd = "{0} application {name}".format(
                command, **config_data["redistribute"]["application"]
            )
            common_config(cmd, "application")
        if config_data["redistribute"].get("bgp"):
            cmd = "{0} bgp {as_number}".format(command, **config_data["redistribute"]["bgp"])
            common_config(cmd, "bgp")
        if config_data["redistribute"].get("connected"):
            cmd = "{0} connected".format(command)
            common_config(cmd, "connected")
        if config_data["redistribute"].get("eigrp"):
            cmd = "{0} eigrp {as_number}".format(command, **config_data["redistribute"]["eigrp"])
            common_config(cmd, "eigrp")
        if config_data["redistribute"].get("isis"):
            cmd = "{0} isis {area_tag}".format(command, **config_data["redistribute"]["isis"])
            if config_data["redistribute"]["isis"].get("clns"):
                cmd += " clns"
            elif config_data["redistribute"]["isis"].get("ip"):
                cmd += " ip"
            common_config(cmd, "isis")
        if config_data["redistribute"].get("iso_igrp"):
            cmd = "{0} iso-igrp {area_tag}".format(
                command, **config_data["redistribute"]["iso_igrp"]
            )
            if config_data["redistribute"]["iso_igrp"].get("route_map"):
                cmd += " route-map {route_map}".format(**config_data["redistribute"]["iso_igrp"])
            common_config(cmd, "iso_igrp")
        if config_data["redistribute"].get("lisp"):
            cmd = "{0} lisp".format(command)
            common_config(cmd, "lisp")
        if config_data["redistribute"].get("mobile"):
            cmd = "{0} mobile".format(command)
            common_config(cmd, "mobile")
        if config_data["redistribute"].get("odr"):
            cmd = "{0} odr".format(command)
            common_config(cmd, "odr")
        if config_data["redistribute"].get("rip"):
            cmd = "{0} rip".format(command)
            common_config(cmd, "rip")
        if config_data["redistribute"].get("ospf"):
            cmd = "{0} ospf {process_id}".format(command, **config_data["redistribute"]["ospf"])
            common_config(cmd, "ospf")
            if config_data["redistribute"]["ospf"].get("match"):
                external_type = None
                commands[-1] += " match"
                if config_data["redistribute"]["ospf"]["match"].get("internal"):
                    commands[-1] += " internal"
                if config_data["redistribute"]["ospf"]["match"].get("external"):
                    external_type = " external"
                if config_data["redistribute"]["ospf"]["match"].get("nssa_external"):
                    external_type = " nssa-external"
                if config_data["redistribute"]["ospf"]["match"].get("type_1") and external_type:
                    commands[-1] += "{0} 1".format(external_type)
                if config_data["redistribute"]["ospf"]["match"].get("type_2") and external_type:
                    commands[-1] += "{0} 2".format(external_type)
            if config_data["redistribute"]["ospf"].get("vrf"):
                commands[-1] += " vrf"
        if config_data["redistribute"].get("ospfv3"):
            cmd = "{0} ospfv3 {process_id}".format(command, **config_data["redistribute"]["ospfv3"])
            if config_data["redistribute"]["ospfv3"].get("match"):
                cmd += " match"
                if config_data["redistribute"]["ospfv3"]["match"].get("external"):
                    cmd += " external"
                if config_data["redistribute"]["ospfv3"]["match"].get("internal"):
                    cmd += " internal"
                if config_data["redistribute"]["ospfv3"]["match"].get("nssa_external"):
                    cmd += " nssa-external"
                if config_data["redistribute"]["ospfv3"]["match"].get("type_1"):
                    cmd += " 1"
                elif config_data["redistribute"]["ospfv3"]["match"].get("type_2"):
                    cmd += " 2"
            common_config(cmd, "ospf")
        if config_data["redistribute"].get("static"):
            cmd += "{0} static".format(command)
            common_config(cmd, "static")
        if config_data["redistribute"].get("vrf"):
            if config_data["redistribute"]["vrf"].get("name"):
                cmd = "{0} vrf {name}".format(command, **config_data["redistribute"]["vrf"])
            elif config_data["redistribute"]["vrf"].get("global"):
                cmd = "{0} vrf global".format(command)
            common_config(cmd, "vrf")

        return commands


UNIQUE_AFI = "{{ afi|d() + '_' + safi|d() + '_' + vrf|d() }}"
UNIQUE_NEIB_ADD = "{{ neighbor_address }}"


class Bgp_address_familyTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bgp_address_familyTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    PARSERS = [
        {
            "name": "as_number",
            "getval": re.compile(
                r"""
                ^router\sbgp
                (\s(?P<as_number>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "router bgp {{ as_number }}",
            "result": {"as_number": "{{ as_number }}"},
            "shared": True,
        },
        {
            "name": "afi",
            "getval": re.compile(
                r"""
                \s+address-family
                (\s(?P<afi>ipv4|ipv6|l2vpn|nsap|rtfilter|vpnv4|vpnv6))?
                (\s(?P<safi>flowspec|mdt|multicast|mvpn|unicast|evpn|vpls))?
                (\svrf\s(?P<vrf>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "afi": "{{ afi }}",
                        "safi": "{{ safi }}",
                        "vrf": "{{ vrf }}",
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "aggregate_addresses",
            "getval": re.compile(
                r"""
                \s+aggregate-address
                (\s(?P<address>\S+))?
                (\s(?P<netmask>\S+))?
                (\s(?P<as_set>as-set))?
                (\s(?P<summary_only>summary-only))?
                (\s(?P<as_confed_set>as-confed-set))?
                (\sadvertise-map\s(?P<advertise_map>\S+))?
                (\sattribute-map\s(?P<attribute_map>\S+))?
                (\ssuppress-map\s(?P<suppress_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "aggregate-address "
            "{{ address }} {{ netmask }}"
            "{{ ' as-set' if as_set|d(False) else ''}}"
            "{{ ' summary-only' if summary_only|d(False) else ''}}"
            "{{ ' as-confed-set' if as_confed_set|d(False) else ''}}"
            "{{ (' advertise-map ' + advertise_map) if advertise_map is defined else '' }}"
            "{{ (' attribute-map ' + attribute_map) if attribute_map is defined else '' }}"
            "{{ (' suppress-map ' + suppress_map) if suppress_map is defined else '' }}",
            "result": {
                "aggregate_addresses": [
                    {
                        "address": "{{ address }}",
                        "netmask": "{{ netmask }}",
                        "advertise_map": "{{ advertise_map }}",
                        "as_confed_set": "{{ not not as_confed_set }}",
                        "as_set": "{{ not not as_set }}",
                        "attribute_map": "{{ attribute_map }}",
                        "suppress_map": "{{ suppress_map }}",
                        "summary_only": "{{ not not summary_only }}",
                    }
                ]
            },
        },
        {
            "name": "auto_summary",
            "getval": re.compile(
                r"""
                ((\sauto-summary))?
                $""",
                re.VERBOSE,
            ),
            "setval": "auto-summary",
            "result": {"auto_summary": True},
        },
        # bgp starts
        {
            "name": "bgp.additional_paths.select",
            "getval": re.compile(
                r"""
                \s+bgp\sadditional-paths\sselect
                (\s(?P<select_all>all))?
                (\s(?P<select_backup>backup))?
                (\s(?P<select_best_ext>best-external))?
                (\s(?P<select_group_best>group-best))?
                (\sbest\s(?P<select_best>\d))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select"
            "{{ (' all' ) if bgp.additional_paths.select.all|d(False) else '' }}"
            "{{ (' backup' ) if bgp.additional_paths.select.backup|d(False) else '' }}"
            "{{ (' best-external' ) if bgp.additional_paths.select.best_external|d(False) else '' }}"
            "{{ (' group-best' ) if bgp.additional_paths.select.group_best|d(False) else '' }}"
            "{{ (' best ' + bgp.additional_paths.select.best ) if bgp.additional_paths.select.best else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {
                            "additional_paths": {
                                "select": {
                                    "all": "{{ not not select_all }}",
                                    "backup": "{{ not not select_backup }}",
                                    "best": "{{ select_best }}",
                                    "group_best": "{{ not not select_group_best }}",
                                    "best_external": "{{ not not select_best_ext }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.additional_paths.install",
            "getval": re.compile(
                r"""
                \s+bgp\sadditional-paths\sinstall$""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select install",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {
                            "additional_paths": {
                                "install": True,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.additional_paths.receive",
            "getval": re.compile(
                r"""
                \s+bgp\sadditional-paths\sreceive$""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select receive",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {
                            "additional_paths": {
                                "receive": True,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.additional_paths.send",
            "getval": re.compile(
                r"""
                \s+bgp\sadditional-paths\ssend$""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select send",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {
                            "additional_paths": {
                                "send": True,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.aggregate_timer",
            "getval": re.compile(
                r"""
                \s+bgp\saggregate-timer
                (\s(?P<aggregate_timer>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"aggregate_timer": "{{ aggregate_timer }}"}}
                }
            },
        },
        {
            "name": "bgp.dmzlink-bw",
            "getval": re.compile(
                r"""
                \s+bgp\sdmzlink-bw
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af,
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"dmzlink_bw": True}}}},
        },
        {
            "name": "bgp.nexthop.route_map",
            "getval": re.compile(
                r"""
                \s+bgp\snexthop\sroute-map
                (\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"nexthop": {"route_map": "{{ route_map }}"}}}
                }
            },
        },
        {
            "name": "bgp.nexthop.trigger.delay",
            "getval": re.compile(
                r"""
                \s+bgp\snexthop\strigger\sdelay
                (\s(?P<delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"nexthop": {"trigger": {"delay": "{{ delay }}"}}}}
                }
            },
        },
        {
            "name": "bgp.nexthop.trigger.enable",
            "getval": re.compile(
                r"""
                \s+bgp\snexthop\strigger\sdelay\senable
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger delay enable",
            "result": {
                "address_family": {UNIQUE_AFI: {"bgp": {"nexthop": {"trigger": {"enable": True}}}}}
            },
        },
        {
            "name": "bgp.redistribute_internal",
            "getval": re.compile(
                r"""
                \s+bgp\sredistribute-internal
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp redistribute-internal",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"redistribute_internal": True}}}},
        },
        {
            "name": "bgp.route_map",
            "getval": re.compile(
                r"""
                \s+bgp\sroute-map\spriority
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp route-map priority",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"route_map": True}}}},
        },
        {
            "name": "bgp.scan_time",
            "getval": re.compile(
                r"""
                \s+bgp\sscan-time
                (\s(?P<scan_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp scan-time {{ scan_time }}",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"scan_time": "{{ scan_time }}"}}}},
        },
        {
            "name": "bgp.soft_reconfig_backup",
            "getval": re.compile(
                r"""
                \s+bgp\ssoft-reconfig-backup
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp soft-reconfig-backup",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"soft_reconfig_backup": True}}}},
        },
        {
            "name": "bgp.update_group",
            "getval": re.compile(
                r"""
                \s+bgp\supdate-group\ssplit\sas-override
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp update-group split as-override",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"update_group": True}}}},
        },
        {
            "name": "bgp.dampening",
            "getval": re.compile(
                r"""\s+bgp\sdampening
                    (\s(?P<penalty_half_time>\d+))?
                    (\s(?P<reuse_route_val>\d+))?
                    (\s(?P<suppress_route_val>\d+))?
                    (\s(?P<max_suppress>\d+))?
                    (\sroute-map\s(?P<route_map>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_af_dampening,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {
                            "dampening": {
                                "penalty_half_time": "{{ penalty_half_time  }}",
                                "reuse_route_val": "{{ reuse_route_val  }}",
                                "suppress_route_val": "{{ suppress_route_val  }}",
                                "max_suppress": "{{ max_suppress  }}",
                                "route_map": "{{ route_map }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "bgp.slow_peer.detection.enable",
            "getval": re.compile(r"""\s+bgp\sslow-peer\sdetection$""", re.VERBOSE),
            "setval": "bgp slow-peer detection",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"slow_peer": {"detection": {"enable": True}}}}
                }
            },
        },
        {
            "name": "bgp.slow_peer.detection.threshold",
            "getval": re.compile(
                r"""
                \s+bgp\sslow-peer\sdetection\sthreshold
                (\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer detection threshold {{ threshold }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {"slow_peer": {"detection": {"threshold": "{{ threshold }}"}}}
                    }
                }
            },
        },
        {
            "name": "bgp.slow_peer.split_update_group.dynamic",
            "getval": re.compile(
                r"""
                \s+bgp\sslow-peer\ssplit-update-group\sdynamic$""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer split-update-group dynamic",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"slow_peer": {"split_update_group": {"dynamic": True}}}}
                }
            },
        },
        {
            "name": "bgp.slow_peer.split_update_group.permanent",
            "getval": re.compile(
                r"""
                \s+bgp\sslow-peer\ssplit-update-group\sdynamic\spermanent$""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer split-update-group dynamic permanent",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"slow_peer": {"split_update_group": {"permanent": True}}}}
                }
            },
        },
        # bgp ends
        {
            "name": "default",
            "getval": re.compile(r"""\s+default$""", re.VERBOSE),
            "setval": "default",
            "result": {"address_family": {UNIQUE_AFI: {"default": True}}},
        },
        {
            "name": "default_information",
            "getval": re.compile(r"""\s+default-information\soriginate$""", re.VERBOSE),
            "setval": "default-information originate",
            "result": {"address_family": {UNIQUE_AFI: {"default_information": True}}},
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""\s+default-metric
                    (\s(?P<default_metric>\d+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric|string }}",
            "result": {"address_family": {UNIQUE_AFI: {"default_metric": "{{ default_metric }}"}}},
        },
        {
            "name": "distance",
            "getval": re.compile(
                r"""\s+distance\sbgp
                    (\s(?P<external>\d+))
                    (\s(?P<internal>\d+))
                    (\s(?P<local>\d+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "distance bgp {{ external|string }} {{ internal|string }} {{ local|string }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "distance": {
                            "external": "{{ external }}",
                            "internal": "{{ internal }}",
                            "local": "{{ local }}",
                        }
                    }
                }
            },
        },
        # neighbor starts
        {
            "name": "activate",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)\sactivate$""", re.VERBOSE
            ),
            "setval": "neighbor {{ neighbor_address }} activate",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "activate": True,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "additional_paths",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sadditional-paths
                (\s(?P<disable>disable))?
                (\s(?P<receive>receive))?
                (\s(?P<send>send))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} additional-paths"
            "{{ (' disable') if  additional_paths.disable|d(False) else '' }}"
            "{{ (' receive') if additional_paths.receive|d(False) else '' }}"
            "{{ (' send') if additional_paths.send|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "additional_paths": {
                                    "disable": "{{ not not disable }}",
                                    "receive": "{{ not not receive }}",
                                    "send": "{{ not not send }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "advertises.additional_paths",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sadvertise\sadditional-paths
                (\s(?P<all>all))?
                (\sbest\s(?P<receive>\d+))?
                (\s(?P<group_best>group-best))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertise additional-paths"
            "{{ (' all') if  advertise.additional_paths.all|d(False) else '' }}"
            "{{ (' best '+ best|string) if advertise.additional_paths.best|d(False) else '' }}"
            "{{ (' group-best') if advertise.additional_paths.group_best|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "advertises": {
                                    "additional_paths": {
                                        "all": "{{ not not all }}",
                                        "best": "{{ receive }}",
                                        "group_best": "{{ not not group_best }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "advertises.best_external",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sadvertise\sbest-external
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' advertise best-external') if  advertise.best_external|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"advertises": {"best-external": True}}}
                    }
                }
            },
        },
        {
            "name": "advertises.diverse_path",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sadvertise\sdiverse-path
                (\s(?P<backup>backup))?
                (\s(?P<mpath>mpath))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertise diverse-path"
            "{{ (' backup') if  advertise.diverse_path.backup|d(False) else '' }}"
            "{{ (' mpath') if advertise.diverse_path.mpath|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "advertises": {
                                    "diverse_path": {
                                        "backup": "{{ not not backup }}",
                                        "mpath": "{{ not not mpath }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "advertise_map",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sadvertise-map
                (\s(?P<name>\S+))?
                (\sexist-map\s(?P<exist_map>\S+))?
                (\snon-exist-map\s(?P<non_exist_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertise-map"
            "{{ (' ' + name) if  advertise_map.name is defined else '' }}"
            "{{ (' exist-map ' + exist_map) if  advertise_map.exist_map is defined else '' }}"
            "{{ (' non-exist-map ' + non_exist_map) if advertise_map.non_exist_map is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "advertise_map": {
                                    "name": "{{ name }}",
                                    "exist_map": "{{ exist_map }}",
                                    "non_exist_map": "{{ non_exist_map }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "advertisement_interval",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\sadvertisement-interval
                (\s(?P<advertisement_interval>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} advertisement-interval"
            "{{ (' ' + advertisement_interval|string) if advertisement_interval is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "advertisement_interval": "{{ advertisement_interval }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "aigp",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\saigp
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' aigp') if aigp.enable|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"aigp": {"enable": True}}}}
                }
            },
        },
        {
            "name": "aigp.send.cost_community",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\saigp\ssend\scost-community
                (\s(?P<id>\d+))\spoi
                (\s(?P<igp_cost>igp-cost))?
                (\s(?P<pre_bestpath>pre-bestpath))?
                (\s(?P<transitive>transitive))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} aigp send cost-community"
            "{{ (' ' + aigp.send.cost_community.id|string + ' poi') if  aigp.send.cost_community.id is defined else '' }}"
            "{{ (' igp-cost') if  aigp.send.cost_community.poi.igp_cost|d(False) else '' }}"
            "{{ (' pre-bestpath') if  aigp.send.cost_community.poi.pre_bestpath|d(False) else '' }}"
            "{{ (' transitive') if  aigp.send.cost_community.poi.transitive|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "aigp": {
                                    "send": {
                                        "cost_community": {
                                            "id": "{{ id }}",
                                            "poi": {
                                                "igp_cost": "{{ not not igp_cost }}",
                                                "pre_bestpath": "{{ not not pre_bestpath }}",
                                                "transitive": "{{ not not transitive }}",
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "aigp.send.med",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\saigp\ssend\smed
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' aigp send med') if aigp.send.med|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"aigp": {"send": {"med": True}}}}}
                }
            },
        },
        {
            "name": "allow_policy",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sallow-policy
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' allow-policy') if allow_policy|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"allow_policy": True}}}
                }
            },
        },
        {
            "name": "allowas_in",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sallowas-in
                (\s(?P<allowas_in>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' allowas-in ' + allowas_in|string) if allowas_in is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"allowas_in": "{{ allowas_in }}"}}}
                }
            },
        },
        {
            "name": "as_override",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sas-override
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' as-override') if as_override|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"as_override": True}}}
                }
            },
        },
        {
            "name": "bmp_activate",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sbmp-activate
                (\sserver\s(?P<server>\d+))?
                (\s(?P<all>all))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} bmp-activate"
            "{{ (' server '+ bmp_activate.server|string) if bmp_activate.server is defined else '' }}"
            "{{ (' all') if bmp_activate.all|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "bmp_activate": {
                                    "server": "{{ server }}",
                                    "all": "{{ not not  all }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "capability",
            "getval": re.compile(
                r"""
                \sneighbor\s(?P<neighbor_address>\S+)\scapability\sorf\sprefix-list
                (\s(?P<both>both))?
                (\s(?P<receive>receive))?
                (\s(?P<send>send))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} capability orf prefix-list"
            "{{ (' both') if capability.both|d(False) else '' }}"
            "{{ (' receive') if capability.receive|d(False) else '' }}"
            "{{ (' send') if capability.send|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "capability": {
                                    "both": "{{ not not both }}",
                                    "receive": "{{ not not receive }}",
                                    "send": "{{ not not  send }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "cluster_id",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\scluster-id(\s(?P<cluster_id>\s\d+))$""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} cluster-id {{ cluster_id }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"cluster_id": "{{ cluster_id }}"}}}
                }
            },
        },
        {
            "name": "default_originate",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sdefault-originate$""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' default-originate') if default_originate.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"default_originate": {"set": True}}}
                    }
                }
            },
        },
        {
            "name": "default_originate.route_map",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sdefault-originate
                (\sroute-map\s(?P<route_map>\S+))
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} default-originate"
            "{{ (' route-map' + default_originate.route_map) if default_originate.route_map is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {"default-originate": {"route_map": "{{ route_map }}"}}
                        }
                    }
                }
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sdescription\s(?P<description>\S.+)$""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} description {{ description }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "description": "{{ description }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "disable_connected_check",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<disable_connected_check>disable-connected-check)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} disable-connected-check",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "disable_connected_check": "{{ not not disable_connected_check }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "ebgp_multihop",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<enable>ebgp_multihop)
                (\s(?P<hop_count>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ebgp-multihop"
            "{{ (' ' + hop_count|string) if hop_count is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "ebgp_multihop": {
                                    "enable": "{{ not not enable }}",
                                    "hop_count": "{{ hop_count }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "distribute_list",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sdistribute-list
                (\s(?P<acl>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} distribute-list"
            "{{ (' ' + distribute_list.acl) if distribute_list.acl is defined else '' }}"
            "{{ (' in') if distribute_list.in|d(False) else '' }}"
            "{{ (' out') if distribute_list.out|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "distribute_list": {
                                    "acl": "{{ acl }}",
                                    "in": "{{ not not in }}",
                                    "out": "{{ not not out }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "dmzlink_bw",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sdmzlink-bw
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' dmzlink-bw') if dmzlink_bw|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"dmzlink_bw": True}}}
                }
            },
        },
        {
            "name": "filter_list",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sfilter-list
                (\s(?P<acl>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} filter-list"
            "{{ (' ' + filter_list.path_acl) if filter_list.path_acl is defined else '' }}"
            "{{ (' in') if filter_list.in|d(False) else '' }}"
            "{{ (' out') if filter_list.out|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "filter_list": {
                                    "path_acl": "{{ acl }}",
                                    "in": "{{ not not in }}",
                                    "out": "{{ not not out }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "fall_over.bfd",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sfall-over
                \s(?P<set>bfd)
                (\s(?P<multi_hop>multi-hop))?
                (\s(?P<single_hop>single-hop))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} fall-over"
            "{{ (' bfd') if fall_over.bfd.set is defined else '' }}"
            "{{ (' multi-hop') if fall_over.bfd.multi_hop is defined else '' }}"
            "{{ (' single-hop') if fall_over.bfd.single_hop is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "fall_over": {
                                    "bfd": {
                                        "set": "{{ not not set }}",
                                        "multi_hop": "{{ not not multi_hop }}",
                                        "single_hop": "{{ not not single_hop }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "fall_over.route_map",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sroute-map
                \s(?P<route_map>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} route-map {{ fall_over.route_map }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {"fall_over": {"route_map": "{{ not not route_map }}"}}
                        }
                    }
                }
            },
        },
        {
            "name": "ha_mode",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sha-mode
                \s(?P<set>graceful-restart)
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ha-mode"
            "{{ (' graceful-restart') if ha_mode.set is defined else '' }}"
            "{{ (' disable') if ha_mode.disable is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "ha_mode": {
                                    "set": "{{ not not set }}",
                                    "disable": "{{ not not disable }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "inherit",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sinherit\speer-session
                \s(?P<inherit>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} inherit peer-session"
            "{{ (' ' + inherit) if inherit is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"inherit": "{{ inherit }}"}}}
                }
            },
        },
        {
            "name": "internal_vpn_client",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sinternal-vpn-client
                \s(?P<inherit>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} internal-vpn-client",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"internal_vpn_client": True}}}
                }
            },
        },
        {
            "name": "local_as",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\s(?P<local_as>local-as)
                (\s(?P<number>\S+))?
                (\s(?P<dual_as>dual-as))?
                (\s(?P<no_prepend>no-prepend))?
                (\s(?P<replace_as>replace-as))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} local-as"
            "{{ (' ' + local_as.number|string) if local_as.number is defined else '' }}"
            "{{ (' dual-as') if local_as.dual_as is defined else '' }}"
            "{{ (' no-prepend') if local_as.no_prepend.set is defined else '' }}"
            "{{ (' replace-as') if local_as.no_prepend.replace_as is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "local_as": {
                                    "set": "{{ not not local_as }}",
                                    "number": "{{ number }}",
                                    "dual_as": "{{ not not dual_as }}",
                                    "no_prepend": {
                                        "set": "{{ not not no_prepend }}",
                                        "replace_as": "{{ not not replace_as }}",
                                    },
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "remote_as",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\s(?P<remote_as>remote-as)
                (\s(?P<number>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} remote-as"
            "{{ (' ' + remote_as|string) if remote_as is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"remote_as": "{{ number }}"}}}
                }
            },
        },
        {
            "name": "log_neighbor_changes",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \s(?P<set>log-neighbor-changes)
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' log-neighbor-changes') if log_neighbor_changes.set is defined else '' }}"
            "{{ (' disable') if log_neighbor_changes.disable is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "log_neighbor_changes": {
                                    "set": "{{ not not set }}",
                                    "disable": "{{ not not disable }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "maximum_prefix",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\smaximum-prefix
                (\s(?P<max_no>\d+))
                (\s(?P<threshold_val>\d+))?
                (\srestart(?P<restart>\d+))?
                (\s(?P<warning_only>warning-only))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} maximum-prefix"
            "{{ (' ' + maximum_prefix.max_no|string) if maximum_prefix.max_no is defined else '' }}"
            "{{ (' ' + maximum_prefix.threshold_val|string) if maximum_prefix.threshold_val is defined else '' }}"
            "{{ (' restart ' + maximum_prefix.restart|string) if maximum_prefix.restart is defined else '' }}"
            "{{ (' warning-only') if maximum_prefix.warning_only|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "maximum_prefix": {
                                    "number": "{{ max_no }}",
                                    "threshold_value": "{{ threshold_val }}",
                                    "restart": "{{ restart }}",
                                    "warning_only": "{{ not not warning_only }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "nexthop_self.set",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\snext-hop-self
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' next-hop-self') if nexthop_self.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"nexthop_self": {"set": True}}}}
                }
            },
        },
        {
            "name": "nexthop_self.all",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\snext-hop-self\sall
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' next-hop-self all') if nexthop_self.all|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"nexthop_self": {"all": True}}}}
                }
            },
        },
        {
            "name": "next_hop_unchanged.set",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\snext-hop-unchanged
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' next-hop-unchanged') if next_hop_unchanged.set|d(False) else ''}}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"next_hop_unchanged": {"set": True}}}
                    }
                }
            },
        },
        {
            "name": "next_hop_unchanged.allpaths",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\snext-hop-unchanged\sallpaths
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' next-hop-unchanged allpaths') if next_hop_unchanged.allpaths|d(False) else ''}}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"next_hop_unchanged": {"allpaths": True}}}
                    }
                }
            },
        },
        {
            "name": "password_options",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\spassword
                \s(?P<encryption>\d+)
                (\s(?P<pass_key>.$))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} password"
            "{{ (' '+ password_options.encryption|string) if password_options.encryption is defined else '' }}"
            "{{ (' '+ password_options.pass_key) if password_options.pass_key is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "password_options": {
                                    "encryption": "{{ encryption }}",
                                    "pass_key": "{{ pass_key }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "path_attribute.discard",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\spath-attribute\sdiscard
                (\s(?P<type>\d+))?
                (\srange\s(?P<start>\d+)\s(?P<end>\d+))?
                (\s(?P<in>in))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} path-attribute discard"
            "{{ (' ' + type) if path_attribute.discard.type is defined else '' }}"
            "{{ (' range '+ path_attribute.discard.range.start|string) if spath_attribute.discard.range.start is defined else '' }}"
            "{{ (' '+ path_attribute.discard.range.end|string) if spath_attribute.discard.range.end is defined else '' }}"
            "{{ (' in') if path_attribute.discard.in|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "path_attribute": {
                                    "discard": {
                                        "type": "{{ type }}",
                                        "range": {"start": "{{ start }}", "end": "{{ end }}"},
                                        "in": "{{ not not in }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "path_attribute.treat_as_withdraw",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)\spath-attribute\streat-as-withdraw
                (\s(?P<type>\d+))?
                (\srange\s(?P<start>\d+)\s(?P<end>\d+))?
                (\s(?P<in>in))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} path-attribute treat-as-withdraw"
            "{{ (' ' + type) if path_attribute.treat_as_withdraw.type is defined else '' }}"
            "{{ (' range '+ path_attribute.treat_as_withdraw.range.start|string) if spath_attribute.treat_as_withdraw.range.start is defined else '' }}"
            "{{ (' '+ path_attribute.treat_as_withdraw.range.end|string) if spath_attribute.treat_as_withdraw.range.end is defined else '' }}"
            "{{ (' in') if path_attribute.treat_as_withdraw.in|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "path_attribute": {
                                    "treat_as_withdraw": {
                                        "type": "{{ type }}",
                                        "range": {"start": "{{ start }}", "end": "{{ end }}"},
                                        "in": "{{ not not in }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "route_maps",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)\sroute-map
                (\s(?P<route_map>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor_af_route_maps,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "route_maps": [
                                    {
                                        "name": "{{ route_map }}",
                                        "in": "{{ not not in }}",
                                        "out": "{{ not not out }}",
                                    }
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "prefix_lists",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)\sprefix-list
                (\s(?P<prefix_list>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor_af_prefix_lists,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "prefix_lists": [
                                    {
                                        "name": "{{ prefix_list }}",
                                        "in": "{{ not not in }}",
                                        "out": "{{ not not out }}",
                                    }
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "peer_group_name",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)
                \speer-group\s(?P<peer_group>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' peer-group ' + peer_group_name) if peer_group_name|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "peer_group_name": "{{ peer_group_name }}",
                                "neighbor_address": UNIQUE_NEIB_ADD,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "peer_group",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)\speer-group$""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} peer-group",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "peer_group": True,
                                "neighbor_address": UNIQUE_NEIB_ADD,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "route_maps",
            "getval": re.compile(
                r"""\s+neighbor\s(?P<neighbor_address>\S+)\sroute-map
                (\s(?P<route_map>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor_af_route_maps,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "route_maps": [
                                    {
                                        "name": "{{ route_map }}",
                                        "in": "{{ not not in }}",
                                        "out": "{{ not not out }}",
                                    }
                                ],
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "remove_private_as.set",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sremove-private-as
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as') if remove_private_as.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"remove_private_as": {"set": True}}}
                    }
                }
            },
        },
        {
            "name": "remove_private_as.all",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sremove-private-as\sall
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as all') if remove_private_as.all|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"remove_private_as": {"all": True}}}
                    }
                }
            },
        },
        {
            "name": "remove_private_as.replace_as",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sremove-private-as\sreplace-as
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as replace-as') if remove_private_as.replace_as|d(False) else ''}}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"remove_private_as": {"replace_as": True}}}
                    }
                }
            },
        },
        {
            "name": "route_reflector_client",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sroute-reflector-client
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' route-reflector-client') if route_reflector_client|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "route_reflector_client": True,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "route_server_client",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sroute-server-client
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' route-server-client') if route_server_client|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "route_server_client": True,
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "send_community.set",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssend-community
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' send-community') if send_community.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"set": True}}}}
                }
            },
        },
        {
            "name": "send_community.both",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssend-community\sboth
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' both') if send_community.both|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"both": True}}}}
                }
            },
        },
        {
            "name": "send_community.extended",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssend-community\sextended
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' extended') if send_community.extended|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"extended": True}}}
                    }
                }
            },
        },
        {
            "name": "send_community.standard",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssend-community\sstandard
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' standard') if send_community.standard|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"standard": True}}}
                    }
                }
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sshutdown
                (\sgraceful(?P<graceful>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' shutdown') if shutdown.set is defined else '' }}"
            "{{ (' graceful '+ shutdown.graceful|string) if shutdown.graceful is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "shutdown": {"set": True, "graceful": "{{ graceful }}"}
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "slow_peer.detection",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sslow-peer\sdetection
                (\s(?P<enable>enable))?
                (\s(?P<disable>disable))?
                (\sthreshold\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} slow-peer detection"
            "{{ (' enable') if slow_peer.detection.enable|d(False) else '' }}"
            "{{ (' disable') if slow_peer.detection.disable|d(False) else '' }}"
            "{{ (' threshold ' + slow_peer.detection.threshold|string) if slow_peer.detection.threshold is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "slow_peer": {
                                    "detection": {
                                        "enable": "{{ not not enable }}",
                                        "disable": "{{ not not disable }}",
                                        "threshold": "{{ threshold }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "slow_peer.split_update_group",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sslow-peer\ssplit-update-group
                (\s(?P<static>static))?
                (\s(?P<dynamic>dynamic))?
                (\s(?P<disable>disable))?
                (\s(?P<permanent>permanent))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} slow-peer split-update-group"
            "{{ (' static') if slow_peer.split_update_group.static|d(False) else '' }}"
            "{{ (' dynamic') if slow_peer.split_update_group.dynamic.enable|d(False) else '' }}"
            "{{ (' disable') if slow_peer.split_update_group.dynamic.disable|d(False) else '' }}"
            "{{ (' permanent') if slow_peer.split_update_group.dynamic.permanent|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "slow_peer": {
                                    "split_update_group": {
                                        "static": "{{ not not static }}",
                                        "dynamic": {
                                            "enable": "{{ not not dynamic }}",
                                            "disable": "{{ not not disable }}",
                                            "permanent": "{{ not not permanent }}",
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "soft_reconfiguration",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssoft-reconfiguration\sinbound
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' soft-reconfiguration inbound') if soft_reconfiguration|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"soft_reconfiguration": True}}}
                }
            },
        },
        {
            "name": "soo",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\ssoo
                (\s(?P<soo>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} soo {{ soo }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"soo": "{{ soo }}"}}}
                }
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stimers
                (\s(?P<keepalive>\d+))?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} timers"
            "{{ (' ' + timers.keepalive|string) if timers.keepalive is defined else '' }}"
            "{{ (' ' + timers.holdtime|string) if timers.holdtime is defined else '' }}"
            "{{ (' ' + timers.min_holdtime|string) if timers.min_holdtime is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "timers": {
                                    "keepalive": "{{ keepalive }}",
                                    "holdtime": "{{ holdtime }}",
                                    "min_holdtime": "{{ min_holdtime }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "transport.connection_mode",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stransport\sconnection-mode
                (\s(?P<active>active))?
                (\s(?P<passive>passive))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} transport connection-mode"
            "{{ (' active') if transport.connection_mode.active|d(False) else '' }}"
            "{{ (' passive') if transport.connection_mode.passive|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "transport": {
                                    "connection_mode": {
                                        "active": "{{ not not active }}",
                                        "passive": "{{ not not passive }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "transport.multi_session",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stransport\smulti-session
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} transport multi-session",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "transport": {"multi_session": True},
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "transport.path_mtu_discovery",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\stransport\spath-mtu-discovery
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} transport"
            "{{ (' path-mtu-discovery') if transport.path_mtu_discovery.set|d(False) else '' }}"
            "{{ (' disable') if transport.path_mtu_discovery.disable|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "transport": {
                                    "path_mtu_discovery": {
                                        "set": True,
                                        "disable": "{{ not not disable }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sttl-security
                (\shops(?P<ttl_security>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ttl-security"
            "{{ (' hops '+ ttl_security|string) if ttl_security is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"ttl_security": "{{ ttl_security }}"}}
                    }
                }
            },
        },
        {
            "name": "unsuppress_map",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sunsuppress-map
                (\s(?P<unsuppress_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} unsuppress-map"
            "{{ (' ' + unsuppress_map) if unsuppress_map is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"unsuppress_map": "{{ unsuppress_map }}"}}
                    }
                }
            },
        },
        {
            "name": "version",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sversion
                (\s(?P<version>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} version"
            "{{ (' ' + version|string) if version is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "version": "{{ version }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "weight",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)\sweight
                (\s(?P<weight>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} weight"
            "{{ (' ' + weight|string) if weight is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"weight": "{{ weight }}"}}}
                }
            },
        },
        # neighbors end
        {
            "name": "networks",
            "getval": re.compile(
                r"""
                \s+network
                (\s(?P<address>\S+))?
                (\smask\s(?P<netmask>\S+))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\s(?P<backdoor>backdoor))?
                (\s(?P<evpn>evpn))?
                $""",
                re.VERBOSE,
            ),
            "setval": "network"
            "{{ (' ' + address) if address is defined else '' }}"
            "{{ (' mask ' + netmask) if netmask is defined else '' }}"
            "{{ (' route-map ' + route_map) if route_map is defined else '' }}"
            "{{ (' backdoor' ) if backdoor|d(False) else '' }}"
            "{{ (' evpn' ) if evpn|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "networks": [
                            {
                                "address": "{{ address }}",
                                "netmask": "{{ netmask }}",
                                "route_map": "{{ route_map }}",
                                "evpn": "{{ not not evpn }}",
                                "backdoor": "{{ not not backdoor }}",
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""
                \stable-map
                (\s(?P<name>\S+))?
                (\s(?P<filter>filter))?
                $""",
                re.VERBOSE,
            ),
            "setval": "table-map"
            "{{ (' ' + name) if name is defined else '' }}"
            "{{ (' filter' ) if filter|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "table_map": {"name": "{{ name }}", "filter": "{{ not not filter }}"}
                    }
                }
            },
        },
        {  # TODO
            "name": "snmp",
            "getval": re.compile(
                r"""\s+snmp
                    (\s(?P<context>\S+))?
                    (\scontext\s(?P<community>community\s\S+))?
                    (\suser\s(?P<user>\S+))?
                    (\s(?P<ro>ro|RO))?
                    (\s(?P<rw>rw|RW))?
                    (\scredential\s(?P<credential>\S+))?
                    (\s(?P<encrypted>encrypted))?
                    (\s(?P<auth>auth))?
                    (\smd5\s(?P<md5>\S+))?
                    (\ssha\s(?P<sha>\S+))?
                    (\spriv\s(?P<priv>(3des\s\S+|aes\s128\s\S+|aes\s192\s\S+|aes\s256\s\S+|des\s\S+)))?
                    (\saccess\s(?P<access>(ipv6\s\S+|\S+)))?
                    (\sipv6\s(?P<acl>\S+|\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_af_snmp,
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "snmp": {
                            "context": {
                                "name": "{{ context.split('context ')[1] if context is defined }}",
                                "community": {
                                    "snmp_community": "{{ community.split('community ')[1] if community is defined }}",
                                    "acl": "{{ acl if acl is defined and 'ipv6' not in acl }}",
                                    "ro": "{{ True if ro is defined }}",
                                    "rw": "{{ True if rw is defined }}",
                                    "ipv6": "{{ acl.split('ipv6 ')[1] if acl is defined and 'ipv6' in acl }}",
                                },
                                "user": {
                                    "name": "{{ user.split('user ')[1] if user is defined }}",
                                    "access": {
                                        "acl": "{{ access.split('access ')[1] if access is defined and 'ipv6' not in access }}",
                                        "ipv6": "{{ access.split('access ipv6 ')[1] if access is defined and 'ipv6' in access }}",
                                    },
                                    "auth": {
                                        "md5": "{{ md5.split('md5 ')[1] if md5 is defined }}",
                                        "sha": "{{ sha.split('sha ')[1] if sha is defined }}",
                                    },
                                    "priv": {
                                        "3des": "{{ priv.split('priv 3des ')[1] if priv is defined and '3des' in priv }}",
                                        "aes": {
                                            "128": "{{ priv.split('priv aes 128 ')[1] if priv is defined and 'aes 128' in priv }}",
                                            "192": "{{ priv.split('priv aes 192 ')[1] if priv is defined and 'aes 192' in priv }}",
                                            "256": "{{ priv.split('priv aes 256 ')[1] if priv is defined and 'aes 256' in priv }}",
                                        },
                                        "des": "{{ priv.split('priv des ')[1] if priv is defined and 'des' in priv }}",
                                    },
                                    "credential": "{{ True if credential is defined }}",
                                    "encrypted": "{{ True if encrypted is defined }}",
                                },
                            }
                        }
                    }
                }
            },
        },
        # redistribute starts
        {
            "name": "application",
            "getval": re.compile(
                r"""
                \sredistribute\sapplication\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute application {{ application.name }}"
            "{{ (' metric ' + application.metric|string) if application.metric is defined else '' }}"
            "{{ (' route-map ' + application.route_map) if application.route_map is defined else '' }}",
            "remval": "redistribute application {{ application.name }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "application": {
                                    "name": "{{ name }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "bgp",
            "getval": re.compile(
                r"""
                \sredistribute\sbgp\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute bgp {{ bgp.as_number }}"
            "{{ (' metric ' + bgp.metric|string) if bgp.metric is defined else '' }}"
            "{{ (' route-map ' + bgp.route_map) if bgp.route_map is defined else '' }}",
            "remval": "redistribute bgp {{ bgp.as_number }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "bgp": {
                                    "as_number": "{{ name }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "connected",
            "getval": re.compile(
                r"""
                \sredistribute\sconnected
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute connected"
            "{{ (' metric ' + connected.metric|string) if connected.metric is defined else '' }}"
            "{{ (' route-map ' + connected.route_map) if connected.route_map is defined else '' }}",
            "remval": "redistribute connected",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "connected": {
                                    "set": True,
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "eigrp",
            "getval": re.compile(
                r"""
                \sredistribute\seigrp\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute eigrp {{ eigrp.name|string }}"
            "{{ (' metric ' + eigrp.metric|string) if eigrp.metric is defined else '' }}"
            "{{ (' route-map ' + eigrp.route_map) if eigrp.route_map is defined else '' }}",
            "remval": "redistribute eigrp {{ eigrp.name|string }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "eigrp": {
                                    "as_number": "{{ name }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "isis",
            "getval": re.compile(
                r"""
                \sredistribute\sisis\s(?P<name>\S+)
                (\s(?P<clns>clns))?
                (\s(?P<ip>ip))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute isis {{ isis.area_tag }}"
            "{{ (' clns') if isis.clns|d(False) else '' }}"
            "{{ (' ip') if isis.ip|d(False) else '' }}"
            "{{ (' metric ' + isis.metric|string) if isis.metric is defined else '' }}"
            "{{ (' route-map ' + isis.route_map) if isis.route_map is defined else '' }}",
            "remval": "redistribute isis {{ isis.area_tag }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "isis": {
                                    "area_tag": "{{ name }}",
                                    "clns": "{{ not not clns }}",
                                    "ip": "{{ not not ip }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "iso_igrp",
            "getval": re.compile(
                r"""
                \sredistribute\siso-igrp\s(?P<name>\S+)
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute iso-igrp {{ iso_igrp.area_tag }}"
            "{{ (' route-map ' + iso_igrp.route_map) if iso_igrp.route_map is defined else '' }}",
            "remval": "redistribute iso-igrp {{ iso_igrp.area_tag }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {"iso_igrp": {"area_tag": "{{ name }}", "route_map": "{{ route_map }}"}}
                        ]
                    }
                }
            },
        },
        {
            "name": "lisp",
            "getval": re.compile(
                r"""
                \sredistribute\slisp
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute lisp"
            "{{ (' metric ' + lisp.metric|string) if lisp.metric is defined else '' }}"
            "{{ (' route-map ' + lisp.route_map) if lisp.route_map is defined else '' }}",
            "remval": "redistribute lisp",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "lisp": {
                                    "set": True,
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "mobile",
            "getval": re.compile(
                r"""
                \sredistribute\smobile
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute mobile"
            "{{ (' metric ' + mobile.metric|string) if mobile.metric is defined else '' }}"
            "{{ (' route-map ' + mobile.route_map) if mobile.route_map is defined else '' }}",
            "remval": "redistribute mobile",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "mobile": {
                                    "set": True,
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "odr",
            "getval": re.compile(
                r"""
                \sredistribute\sodr
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute odr"
            "{{ (' metric ' + odr.metric|string) if odr.metric is defined else '' }}"
            "{{ (' route-map ' + odr.route_map) if odr.route_map is defined else '' }}",
            "remval": "redistribute odr",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "odr": {
                                    "set": True,
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "ospf",
            "getval": re.compile(
                r"""
                \sredistribute\sospf\s(?P<process_id>\S+)
                (\s(?P<type_1>1))?
                (\s(?P<type_2>2))?
                (\s(?P<external>external))?
                (\s(?P<internal>internal))?
                (\s(?P<nssa_external>nssa-external))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute ospf {{ ospf.process_id }}"
            "{{ (' 1') if ospf.match.type_1|d(False) else '' }}"
            "{{ (' 2') if ospf.match.type_2|d(False) else '' }}"
            "{{ (' external') if ospf.match.external|d(False) else '' }}"
            "{{ (' internal') if ospf.match.internal|d(False) else '' }}"
            "{{ (' nssa-external') if ospf.match.nssa_external|d(False) else '' }}"
            "{{ (' metric ' + ospf.metric|string) if ospf.metric is defined else '' }}"
            "{{ (' route-map ' + ospf.route_map) if ospf.route_map is defined else '' }}"
            "{{ (' vrf ' + ospf.vrf) if ospf.vrf is defined else '' }}",
            "remval": "redistribute ospf {{ ospf.process_id }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "ospf": {
                                    "process_id": "{{ process_id }}",
                                    "match": {
                                        "type_1": "{{ not not type_1 }}",
                                        "type_2": "{{ not not type_2 }}",
                                        "external": "{{ not not external }}",
                                        "internal": "{{ not not internal }}",
                                        "nssa_external": "{{ not not nssa_external }}",
                                    },
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                    "vrf": "{{ vrf }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "ospfv3",
            "getval": re.compile(
                r"""
                \sredistribute\sospfv3\s(?P<process_id>\S+)
                (\s(?P<type_1>1))?
                (\s(?P<type_2>2))?
                (\s(?P<external>external))?
                (\s(?P<internal>internal))?
                (\s(?P<nssa_external>nssa-external))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute ospfv3 {{ ospfv3.process_id }}"
            "{{ (' 1') if ospfv3.match.type_1|d(False) else '' }}"
            "{{ (' 2') if ospfv3.match.type_2|d(False) else '' }}"
            "{{ (' external') if ospfv3.match.external|d(False)  else '' }}"
            "{{ (' internal') if ospfv3.match.internal|d(False)  else '' }}"
            "{{ (' nssa-external') if ospfv3.match.nssa_external|d(False) else '' }}"
            "{{ (' metric ' + ospfv3.metric|string) if ospfv3.metric is defined else '' }}"
            "{{ (' route-map ' + ospfv3.route_map) if ospfv3.route_map is defined else '' }}",
            "remval": "redistribute ospfv3 {{ ospfv3.process_id }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "ospfv3": {
                                    "process_id": "{{ process_id }}",
                                    "match": {
                                        "type_1": "{{ not not type_2 }}",
                                        "type_2": "{{ not not type_2 }}",
                                        "external": "{{ not not external }}",
                                        "internal": "{{ not not internal }}",
                                        "nssa_external": "{{ not not nssa_external }}",
                                    },
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "rip",
            "getval": re.compile(
                r"""
                \sredistribute\srip
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute rip"
            "{{ (' metric ' + rip.metric|string) if rip.metric is defined else '' }}"
            "{{ (' route-map ' + rip.route_map) if rip.route_map is defined else '' }}",
            "remval": "redistribute rip",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "rip": {
                                    "set": True,
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "static",
            "getval": re.compile(
                r"""
                \sredistribute\sstatic
                (\s(?P<clns>clns))?
                (\s(?P<ip>ip))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute static"
            "{{ (' clns') if static.clns|d(False) else '' }}"
            "{{ (' ip') if static.ip|d(False) else '' }}"
            "{{ (' metric ' + static.metric|string) if static.metric is defined else '' }}"
            "{{ (' route-map ' + static.route_map) if static.route_map is defined else '' }}",
            "remval": "redistribute static",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "static": {
                                    "set": True,
                                    "clns": "{{ not not clns }}",
                                    "ip": "{{ not not ip }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                }
                            }
                        ]
                    }
                }
            },
        },
        {
            "name": "vrf",
            "getval": re.compile(
                r"""
                \sredistribute\svrf
                (\s(?P<name>\S+))?
                (\s(?P<global>global))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute vrf {{ vrf.name }}"
            "{{ (' global') if vrf.global|d(False) else '' }}",
            "remval": "redistribute vrf {{ vrf.name }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {"vrf": {"name": "{{ name }}", "global": "{{ not not global }}"}}
                        ]
                    }
                }
            },
        },
        # redistribute ends
    ]
