# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Bgp_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_bgp_additional_paths(config_data):
    if "bgp" in config_data:
        if "additional_paths" in config_data["bgp"]:
            cmd = "bgp additional-paths"
            if "install" in config_data["bgp"]["additional_paths"]:
                cmd += " install"
            elif "select" in config_data["bgp"]["additional_paths"]:
                cmd += " select"
                if "all" in config_data["bgp"]["additional_paths"]["select"]:
                    cmd += " all"
                elif (
                    "best" in config_data["bgp"]["additional_paths"]["select"]
                ):
                    cmd += " best {best}".format(
                        **config_data["bgp"]["additional_paths"]["select"]
                    )
                elif (
                    "best_external"
                    in config_data["bgp"]["additional_paths"]["select"]
                ):
                    cmd += " best-external"
                elif (
                    "group_best"
                    in config_data["bgp"]["additional_paths"]["select"]
                ):
                    cmd += " group-best"
            if "receive" in config_data["bgp"]["additional_paths"]:
                cmd += " receive"
            if "send" in config_data["bgp"]["additional_paths"]:
                cmd += " send"
            return cmd


def _tmplt_bgp_bestpath(config_data):
    if "bgp" in config_data and "bestpath" in config_data["bgp"]:
        commands = []
        val = config_data["bgp"]["bestpath"]
        cmd = "bgp bestpath"
        if val.get("aigp"):
            commands.append("{0} aigp ignore".format(cmd))
        elif val.get("compare_routerid"):
            commands.append("{0} compare-routerid".format(cmd))
        elif val.get("cost_community"):
            commands.append("{0} cost-community ignore".format(cmd))
        elif val.get("igp_metric"):
            commands.append("{0} igp-metric ignore".format(cmd))
        elif "med" in val:
            self_cmd = "{0} med".format(cmd)
            if "confed" in val["med"]:
                self_cmd += " confed"
            elif "missing_as_worst" in val["med"]:
                self_cmd += " missing-as-worst"
            commands.append(self_cmd)
        return commands


def _tmplt_bgp_config(config_data):
    if "bgp" in config_data:
        cmd = []
        command = "bgp"
        if config_data["bgp"].get("advertise_best_external"):
            cmd.append("bgp advertise-best-external")
        if config_data["bgp"].get("aggregate_timer"):
            cmd.append(
                "bgp aggregate-timer {aggregate_timer}".format(
                    **config_data["bgp"]
                )
            )
        if config_data["bgp"].get("always_compare_med"):
            cmd.append("bgp always-compare-med")
        if config_data["bgp"].get("asnotation"):
            cmd.append("bgp asnotation dot")
        if "client_to_client" in config_data["bgp"]:
            command = "bgp client-to-client reflection"
            if "all" in config_data["bgp"]["client_to_client"]:
                command += " all"
            elif "intra_cluster" in config_data["bgp"]["client_to_client"]:
                command += " intra-cluster cluster-id {intra_cluster}".format(
                    **config_data["bgp"]["client_to_client"]
                )
            cmd.append(command)
        if config_data["bgp"].get("cluster_id"):
            cmd.append(
                "bgp cluster-id {cluster_id}".format(**config_data["bgp"])
            )
        if "confederation" in config_data["bgp"]:
            command = "bgp confederation"
            if "identifier" in config_data["bgp"]["confederation"]:
                command += "bgp identifier {identifier}".format(
                    **config_data["bgp"]["confederation"]
                )
            elif "peers" in config_data["bgp"]["confederation"]:
                command += "bgp peers {peers}".format(
                    **config_data["bgp"]["confederation"]
                )
            cmd.append(command)
        if "consistency_checker" in config_data["bgp"]:
            command = "bgp consistency-checker"
            if "auto_repair" in config_data["bgp"]["consistency_checker"]:
                command += " auto-repair"
                if (
                    "interval"
                    in config_data["bgp"]["consistency_checker"]["auto_repair"]
                ):
                    command += " interval {interval}".format(
                        **config_data["bgp"]["consistency_checker"][
                            "auto_repair"
                        ]
                    )
            elif "error-message" in config_data["bgp"]["consistency_checker"]:
                command += " error-message"
                if (
                    "interval"
                    in config_data["bgp"]["consistency_checker"][
                        "error_message"
                    ]
                ):
                    command += " interval {interval}".format(
                        **config_data["bgp"]["consistency_checker"][
                            "error_message"
                        ]
                    )
        if config_data["bgp"].get("deterministic_med"):
            cmd.append("bgp deterministic-med")
        if config_data["bgp"].get("dmzlink_bw"):
            cmd.append("bgp dmzlink-bw")
        if config_data["bgp"].get("enforce_first_as"):
            cmd.append("bgp enforce-first-as")
        if config_data["bgp"].get("enhanced_error"):
            cmd.append("bgp enhanced-error")
        if config_data["bgp"].get("fast_external_fallover"):
            cmd.append("bgp fast-external-fallover")
        if "graceful_restart" in config_data["bgp"]:
            command = "bgp graceful-restart"
            if config_data["bgp"]["graceful_restart"].get("extended"):
                command += " extended"
            elif config_data["bgp"]["graceful_restart"].get("restart_time"):
                command += " restart-time {restart_time}".format(
                    **config_data["bgp"]["graceful_restart"]
                )
            elif config_data["bgp"]["graceful_restart"].get("stalepath_time"):
                command += " stalepath-time {stalepath_time}".format(
                    **config_data["bgp"]["graceful_restart"]
                )
            cmd.append(command)
        if "inject_map" in config_data["bgp"]:
            command = "bgp inject-map {name} exist-map {exist_map_name}".format(
                **config_data["bgp"]["inject_map"]
            )
            if config_data["bgp"]["inject_map"].get("copy_attributes"):
                command += "copy-attributes"
            cmd.append(command)
        if "listen" in config_data["bgp"]:
            command = "bgp listen"
            if "limit" in config_data["bgp"]["listen"]:
                command += " limit {limit}".format(
                    **config_data["bgp"]["listen"]
                )
            elif "range" in config_data["bgp"]["listen"]:
                if config_data["bgp"]["listen"]["range"].get(
                    "ipv4_with_subnet"
                ):
                    command += " range {ipv4_with_subnet}".format(
                        **config_data["bgp"]["listen"]["range"]
                    )
                elif config_data["bgp"]["listen"]["range"].get(
                    "ipv6_with_subnet"
                ):
                    command += " range {ipv6_with_subnet}".format(
                        **config_data["bgp"]["listen"]["range"]
                    )
                if config_data["bgp"]["listen"]["range"].get("peer_group"):
                    command += " peer-group {peer_group}".format(
                        **config_data["bgp"]["listen"]["range"]
                    )
            cmd.append(command)
        if config_data["bgp"].get("log_neighbor_changes"):
            cmd.append("bgp log-neighbor-changes")
        if config_data["bgp"].get("maxas_limit"):
            cmd.append(
                "bgp maxas-limit {maxas_limit}".format(**config_data["bgp"])
            )
        if config_data["bgp"].get("maxextcommunity_limit"):
            cmd.append(
                "bgp maxextcommunity-limit {maxextcommunity_limit}".format(
                    **config_data["bgp"]
                )
            )
        if "nexthop" in config_data["bgp"]:
            command = "bgp nexthop"
            if "route_map" in config_data["bgp"]["nexthop"]:
                command += " route-map {route_map}".format(
                    **config_data["bgp"]["nexthop"]
                )
            elif "trigger" in config_data["bgp"]["nexthop"]:
                if config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger delay {delay}".format(
                        **config_data["bgp"]["nexthop"]["trigger"]
                    )
                elif config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger enable"
            cmd.append(command)
        if config_data["bgp"].get("recursion"):
            cmd.append("bgp recursion host")
        if config_data["bgp"].get("redistribute_internal"):
            cmd.append("bgp redistribute-internal")
        if "refresh" in config_data["bgp"]:
            command = "bgp refresh"
            if "max_eor_time" in config_data["bgp"]["refresh"]:
                command += " max-eor-time {max_eor_time}".format(
                    **config_data["bgp"]["refresh"]
                )
            elif "stalepath_time" in config_data["bgp"]["refresh"]:
                command += " stalepath-time {stalepath_time}".format(
                    **config_data["bgp"]["refresh"]
                )
            cmd.append(command)
        if config_data["bgp"].get("regexp"):
            cmd.append("bgp regexp deterministic")
        if config_data["bgp"].get("route_map"):
            cmd.append("bgp route-map priority")
        if "router_id" in config_data["bgp"]:
            command = "bgp router-id"
            if "address" in config_data["bgp"]["router_id"]:
                command += " {address}".format(
                    **config_data["bgp"]["router_id"]
                )
            elif "interface" in config_data["bgp"]["router_id"]:
                command += " interface {interface}".format(
                    **config_data["bgp"]["router_id"]
                )
            elif "vrf" in config_data["bgp"]["router_id"]:
                command += " vrf auto-assign"
            cmd.append(command)
        if config_data["bgp"].get("scan_time"):
            cmd.append(
                "bgp scan-time {scan_time}".format(**config_data["bgp"])
            )
        if "slow_peer" in config_data["bgp"]:
            command = "bgp slow-peer"
            if "detection" in config_data["bgp"]["slow_peer"]:
                command += " detection"
                if "threshold" in config_data["bgp"]["slow_peer"]["detection"]:
                    command += " threshold {threshold}".format(
                        **config_data["bgp"]["slow_peer"]["detection"]
                    )
            elif "split_update_group" in config_data["bgp"]["slow_peer"]:
                if (
                    "dynamic"
                    in config_data["bgp"]["slow_peer"]["split_update_group"]
                ):
                    command += " dynamic"
                    if (
                        "permanent"
                        in config_data["bgp"]["slow_peer"][
                            "split_update_group"
                        ]
                    ):
                        command += " permanent {permanent}".format(
                            **config_data["bgp"]["slow_peer"][
                                "split_update_group"
                            ]
                        )
            cmd.append(command)
        if config_data["bgp"].get("snmp"):
            cmd.append("bgp snmp traps add-type")
        if config_data["bgp"].get("sso"):
            cmd.append("bgp sso route-refresh-enable")
        if config_data["bgp"].get("soft_reconfig_backup"):
            cmd.append("bgp soft-reconfig-backup")
        if config_data["bgp"].get("suppress_inactive"):
            cmd.append("bgp suppress-inactive")
        if config_data["bgp"].get("transport"):
            cmd.append("bgp transport path-mtu-discovery")
        if config_data["bgp"].get("update_delay"):
            cmd.append(
                "bgp update-delay {update_delay}".format(**config_data["bgp"])
            )
        if config_data["bgp"].get("update_group"):
            cmd.append("bgp update-group split as-override")
        if config_data["bgp"].get("upgrade_cli"):
            command += "bgp upgrade-cli"
            if config_data["bgp"]["upgrade_cli"].get("af_mode"):
                command += " af-mode"
        return cmd


def _tmplt_bgp_dampening(config_data):
    if "bgp" in config_data and "dampening" in config_data["bgp"]:
        if config_data["bgp"]["dampening"].get("penalty_half_time"):
            command = "bgp dampening {penalty_half_time}".format(
                **config_data["bgp"]["dampening"]
            )
            if config_data["bgp"]["dampening"].get("reuse_route_val"):
                command += " {reuse_route_val}".format(
                    **config_data["bgp"]["dampening"]
                )
            if config_data["bgp"]["dampening"].get("suppress_route_val"):
                command += " {suppress_route_val}".format(
                    **config_data["bgp"]["dampening"]
                )
            if config_data["bgp"]["dampening"].get("max_suppress"):
                command += " {max_suppress}".format(
                    **config_data["bgp"]["dampening"]
                )
        elif config_data["bgp"]["dampening"].get("route_map"):
            command = "bgp dampening {route_map}".format(
                **config_data["bgp"]["dampening"]
            )
        return command


def _tmplt_bgp_graceful_shutdown(config_data):
    if "bgp" in config_data and "graceful_shutdown" in config_data["bgp"]:
        command = "bgp graceful-shutdown all"
        if config_data["bgp"]["graceful_shutdown"].get("neighbors"):
            command += " neighbors"
            if config_data["bgp"]["graceful_shutdown"]["neighbors"].get(
                "activate"
            ):
                command += " activate"
            elif config_data["bgp"]["graceful_shutdown"]["neighbors"].get(
                "time"
            ):
                command += " {time}".format(
                    **config_data["bgp"]["graceful_shutdown"]["neighbors"]
                )
        elif config_data["bgp"]["graceful_shutdown"].get("vrfs"):
            command += " vrfs"
            if config_data["bgp"]["graceful_shutdown"]["vrfs"].get("activate"):
                command += " activate"
            elif config_data["bgp"]["graceful_shutdown"]["neighbors"].get(
                "time"
            ):
                command += " {time}".format(
                    **config_data["bgp"]["graceful_shutdown"]["vrfs"]
                )
        if config_data["bgp"]["graceful_shutdown"].get("local_preference"):
            command += " local-preference {local_preference}".format(
                **config_data["bgp"]["graceful_shutdown"]
            )
        if config_data["bgp"]["graceful_shutdown"].get("community"):
            command += " community {community}".format(
                **config_data["bgp"]["graceful_shutdown"]
            )
        return command


def _tmplt_bgp_nopeerup_delay(config_data):
    if "bgp" in config_data and "nopeerup_delay" in config_data["bgp"]:
        commands = []
        val = config_data["bgp"]["nopeerup_delay"]
        cmd = "bgp nopeerup-delay"
        if val.get("cold_boot"):
            commands.append("{0} cold-boot {cold_boot}".format(cmd, **val))
        elif val.get("post_boot"):
            commands.append("{0} post-boot {post_boot}".format(cmd, **val))
        elif val.get("nsf_switchover"):
            commands.append(
                "{0} nsf-switchover {nsf_switchover}".format(cmd, **val)
            )
        elif val.get("user_initiated"):
            commands.append(
                "{0} user-initiated {user_initiated}".format(cmd, **val)
            )
        return commands


def _tmplt_neighbor(config_data):
    if "neighbor" in config_data:
        commands = []
        cmd = "neighbor"
        if "address" in config_data["neighbor"]:
            cmd += " {address}".format(**config_data["neighbor"])
        elif "tag" in config_data["neighbor"]:
            cmd += " {tag}".format(**config_data["neighbor"])
        elif "ipv6_adddress" in config_data["neighbor"]:
            cmd += " {ipv6_adddress}".format(**config_data["neighbor"])
        if "remote_as" in config_data["neighbor"]:
            commands.append(
                "{0} remote-as {remote_as}".format(
                    cmd, **config_data["neighbor"]
                )
            )
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
                if (
                    "all"
                    in config_data["neighbor"]["advertise"]["additional_paths"]
                ):
                    self_cmd += " all"
                elif (
                    "best"
                    in config_data["neighbor"]["advertise"]["additional_paths"]
                ):
                    self_cmd += " best {best}".format(
                        **config_data["neighbor"]["advertise"][
                            "additional_paths"
                        ]
                    )
                elif (
                    "group_best"
                    in config_data["neighbor"]["advertise"]["additional_paths"]
                ):
                    self_cmd += " group-best"
            elif "best_external" in config_data["neighbor"]["advertise"]:
                self_cmd += " best-external"
            elif "diverse_path" in config_data["neighbor"]["advertise"]:
                self_cmd += "diverse-path"
                if (
                    "backup"
                    in config_data["neighbor"]["advertise"]["diverse_path"]
                ):
                    self_cmd += " backup"
                elif (
                    "mpath"
                    in config_data["neighbor"]["advertise"]["diverse_path"]
                ):
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
                if config_data["neighbor"]["aigp"]["send"].get(
                    "cost_community"
                ):
                    self_cmd += " cost-community {id}".format(
                        **config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]
                    )
                    if config_data["neighbor"]["aigp"]["send"][
                        "cost_community"
                    ].get("poi"):
                        self_cmd += " poi"
                        if config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]["poi"].get("igp_cost"):
                            self_cmd += " igp-cost"
                        if config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]["poi"].get("pre_bestpath"):
                            self_cmd += " pre-bestpath"
                        if config_data["neighbor"]["aigp"]["send"][
                            "cost_community"
                        ]["poi"].get("transitive"):
                            self_cmd += " transitive"
                if config_data["neighbor"]["aigp"]["send"].get("med"):
                    self_cmd += " med"
            commands.append(self_cmd)
        if config_data["neighbor"].get("allow_policy"):
            commands.append("{0} allow-policy".format(cmd))
        if config_data["neighbor"].get("allowas_in"):
            commands.append(
                "{0} allowas-in {allowas_in}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get("as_override"):
            commands.append("{0} as-override".format(cmd))
        if "bmp_activate" in config_data["neighbor"]:
            self_cmd = "{0} bmp-activate".format(cmd)
            if config_data["neighbor"]["bmp_activate"].get("all"):
                self_cmd += " all"
            if "server" in config_data["neighbor"]["bmp_activate"]:
                self_cmd += " server {server}".format(
                    **config_data["neighbor"]["bmp_activate"]
                )
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
            commands.append(
                "{0} cluster-id {cluster_id}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "default_originate" in config_data["neighbor"]:
            self_cmd = "{0} default-originate".format(cmd)
            if config_data["neighbor"]["default_originate"].get("route_map"):
                self_cmd += " route-map {route_map}".format(
                    **config_data["neighbor"]["default_originate"]
                )
            commands.append(self_cmd)
        if "description" in config_data["neighbor"]:
            commands.append(
                "{0} description {description}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get("disable_connected_check"):
            commands.append("{0} disable-connected-check".format(cmd))
        if "distribute_list" in config_data["neighbor"]:
            self_cmd = "{0} distribute-list".format(cmd)
            if "acl" in config_data["neighbor"]["distribute_list"]:
                self_cmd += " {acl}".format(
                    **config_data["neighbor"]["distribute_list"]
                )
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
                self_cmd += " {hop_count}".format(
                    **config_data["neighbor"]["ebgp_multihop"]
                )
            commands.append(self_cmd)
        if "fall_over" in config_data["neighbor"]:
            self_cmd = "{0} fall-over".format(cmd)
            if "bfd" in config_data["neighbor"]["fall_over"]:
                self_cmd += " bfd"
                if config_data["neighbor"]["fall_over"]["bfd"].get(
                    "multi_hop"
                ):
                    self_cmd += " multi-hop"
                elif config_data["neighbor"]["fall_over"]["bfd"].get(
                    "single_hop"
                ):
                    self_cmd += " single-hop"
            elif "route_map" in config_data["neighbor"]["fall_over"]:
                self_cmd += " {route_map}".format(
                    **config_data["neighbor"]["route_map"]
                )
            commands.append(self_cmd)
        if "filter_list" in config_data["neighbor"]:
            self_cmd = "{0} filter-list".format(cmd)
            if "path_acl" in config_data["neighbor"]["filter_list"]:
                self_cmd += " {path_acl}".format(
                    **config_data["neighbor"]["filter_list"]
                )
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
            self_cmd = "{0} inherit {inherit}".format(
                cmd, **config_data["neighbor"]
            )
            commands.append(self_cmd)
        if "local_as" in config_data["neighbor"]:
            self_cmd = "{0} local-as".format(cmd)
            if "number" in config_data["neighbor"]["local_as"]:
                self_cmd += " {number}".format(
                    **config_data["neighbor"]["local_as"]
                )
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
            if "max_no" in config_data["neighbor"]["maximum_prefix"]:
                self_cmd += " {max_no}".format(
                    **config_data["neighbor"]["maximum_prefix"]
                )
            if "threshold_val" in config_data["neighbor"]["maximum_prefix"]:
                self_cmd += " {threshold_val}".format(
                    **config_data["neighbor"]["maximum_prefix"]
                )
            if config_data["neighbor"]["maximum_prefix"].get("restart"):
                self_cmd += " restart {restart}".format(
                    **config_data["neighbor"]["maximum_prefix"]
                )
            elif config_data["neighbor"]["filter_list"].get("warning_only"):
                self_cmd += " warning-only"
            commands.append(self_cmd)
        if "next_hop_self" in config_data["neighbor"]:
            self_cmd = "{0} next-hop-self".format(cmd)
            if config_data["neighbor"]["next_hop_self"].get("all"):
                self_cmd += " all"
            commands.append(self_cmd)
        if "next_hop_unchanged" in config_data["neighbor"]:
            self_cmd = "{0} next-hop-unchanged".format(cmd)
            if config_data["neighbor"]["next_hop_unchanged"].get("allpaths"):
                self_cmd += " allpaths"
            commands.append(self_cmd)
        if "password" in config_data["neighbor"]:
            commands.append(
                "{0} password {password}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "path_attribute" in config_data["neighbor"]:
            self_cmd = "{0} path-attribute".format(cmd)
            if "discard" in config_data["neighbor"]["path_attribute"]:
                self_cmd += " discard"
                if (
                    "type"
                    in config_data["neighbor"]["path_attribute"]["discard"]
                ):
                    self_cmd += " {type}".format(
                        **config_data["neighbor"]["path_attribute"]["discard"]
                    )
                elif (
                    "range"
                    in config_data["neighbor"]["path_attribute"]["discard"]
                ):
                    self_cmd += " range"
                    if (
                        "start"
                        in config_data["neighbor"]["path_attribute"][
                            "discard"
                        ]["range"]
                    ):
                        self_cmd += " {start}".format(
                            **config_data["neighbor"]["path_attribute"][
                                "discard"
                            ]["range"]
                        )
                    elif (
                        "end"
                        in config_data["neighbor"]["path_attribute"][
                            "discard"
                        ]["range"]
                    ):
                        self_cmd += " {start}".format(
                            **config_data["neighbor"]["path_attribute"][
                                "discard"
                            ]["range"]
                        )
                if (
                    "in"
                    in config_data["neighbor"]["path_attribute"]["discard"]
                ):
                    self_cmd += " in"
            if (
                "treat_as_withdraw"
                in config_data["neighbor"]["path_attribute"]
            ):
                self_cmd += " treat-as-withdraw"
                if (
                    "type"
                    in config_data["neighbor"]["path_attribute"][
                        "treat_as_withdraw"
                    ]
                ):
                    self_cmd += " {type}".format(
                        **config_data["neighbor"]["path_attribute"][
                            "treat_as_withdraw"
                        ]
                    )
                elif (
                    "range"
                    in config_data["neighbor"]["path_attribute"][
                        "treat_as_withdraw"
                    ]
                ):
                    self_cmd += " range"
                    if (
                        "start"
                        in config_data["neighbor"]["path_attribute"][
                            "treat_as_withdraw"
                        ]["range"]
                    ):
                        self_cmd += " {start}".format(
                            **config_data["neighbor"]["path_attribute"][
                                "treat_as_withdraw"
                            ]["range"]
                        )
                    elif (
                        "end"
                        in config_data["neighbor"]["path_attribute"][
                            "treat_as_withdraw"
                        ]["range"]
                    ):
                        self_cmd += " {start}".format(
                            **config_data["neighbor"]["path_attribute"][
                                "treat_as_withdraw"
                            ]["range"]
                        )
                if (
                    "in"
                    in config_data["neighbor"]["path_attribute"][
                        "treat_as_withdraw"
                    ]
                ):
                    self_cmd += " in"
            commands.append(self_cmd)
        if "peer_group" in config_data["neighbor"]:
            commands.append(
                "{0} peer-group {peer_group}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "remove_private_as" in config_data["neighbor"]:
            self_cmd = "{0} remove-private-as".format(cmd)
            if config_data["neighbor"]["remove_private_as"].get("all"):
                self_cmd += " all"
            elif config_data["neighbor"]["remove_private_as"].get(
                "replace_as"
            ):
                self_cmd += " replace_as"
            commands.append(self_cmd)
        if "route_map" in config_data["neighbor"]:
            self_cmd = "{0} route-map".format(cmd)
            if "name" in config_data["neighbor"]["route_map"]:
                self_cmd += " {name}".format(
                    **config_data["neighbor"]["route_map"]
                )
            if "in" in config_data["neighbor"]["route_map"]:
                self_cmd += " in"
            elif "out" in config_data["neighbor"]["route_map"]:
                self_cmd += " out"
            commands.append(self_cmd)
        if "route_reflector_client" in config_data["neighbor"]:
            commands.append("{0} route-reflector-client".format(cmd))
        if "route_server_client" in config_data["neighbor"]:
            self_cmd = "{0} route-server-client".format(cmd)
            if "context" in config_data["neighbor"]["route_map"]:
                self_cmd += " context {context}".format(
                    **config_data["neighbor"]["route_server_client"]
                )
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
        if "send_label" in config_data["neighbor"]:
            self_cmd = "{0} send-label".format(cmd)
            if config_data["neighbor"]["send_label"].get("explicit_null"):
                self_cmd += " explicit-null"
            commands.append(self_cmd)
        if "shutdown" in config_data["neighbor"]:
            self_cmd = "{0} shutdown".format(cmd)
            if "graceful" in config_data["neighbor"]["route_map"]:
                self_cmd += " graceful {graceful}".format(
                    **config_data["neighbor"]["shutdown"]
                )
            commands.append(self_cmd)
        if "slow_peer" in config_data["neighbor"]:
            self_cmd = "{0} slow-peer".format(cmd)
            if "detection" in config_data["neighbor"]["slow_peer"]:
                self_cmd += " detection"
                if (
                    "disable"
                    in config_data["neighbor"]["slow_peer"]["detection"]
                ):
                    self_cmd += " disable"
                elif (
                    "threshold"
                    in config_data["neighbor"]["slow_peer"]["detection"]
                ):
                    self_cmd += " threshold {threshold}".format(
                        **config_data["neighbor"]["slow_peer"]["detection"]
                    )
            elif "split_update_group" in config_data["neighbor"]["slow_peer"]:
                self_cmd += " split-update-group"
                if (
                    "dynamic"
                    in config_data["neighbor"]["slow_peer"][
                        "split_update_group"
                    ]
                ):
                    self_cmd += " dynamic"
                    if (
                        "disable"
                        in config_data["neighbor"]["slow_peer"][
                            "split_update_group"
                        ]["dynamic"]
                    ):
                        self_cmd += " disable"
                    elif (
                        "permanent"
                        in config_data["neighbor"]["slow_peer"][
                            "split_update_group"
                        ]["dynamic"]
                    ):
                        self_cmd += " permanent"
                elif (
                    "static"
                    in config_data["neighbor"]["slow_peer"][
                        "split_update_group"
                    ]
                ):
                    self_cmd += " static"
            commands.append(self_cmd)
        if "soft_reconfiguration" in config_data["neighbor"]:
            commands.append("{0} soft-reconfiguration".format(cmd))
        if "timers" in config_data["neighbor"]:
            self_cmd = "{0} timers {interval} {holdtime}".format(
                cmd, **config_data["neighbor"]["timers"]
            )
            if "min_holdtime" in config_data["neighbor"]["timers"]:
                self_cmd += " {min_holdtime}".format(
                    **config_data["neighbor"]["timers"]
                )
            commands.append(self_cmd)
        if "translate_update" in config_data["neighbor"]:
            self_cmd = "{0} translate-update".format(cmd)
            if config_data["neighbor"]["send_community"].get("nlri"):
                self_cmd += " nlri"
                if config_data["neighbor"]["nlri"].get("multicast"):
                    self_cmd += "multicast"
                if config_data["neighbor"]["nlri"].get("unicast"):
                    self_cmd += "unicast"
            commands.append(self_cmd)
        if "transport" in config_data["neighbor"]:
            self_cmd = "{0} transport".format(cmd)
            if config_data["neighbor"]["transport"].get("connection_mode"):
                self_cmd += " connection-mode"
                if config_data["neighbor"]["transport"]["connection_mode"].get(
                    "active"
                ):
                    self_cmd += " active"
                elif config_data["neighbor"]["transport"][
                    "connection_mode"
                ].get("passive"):
                    self_cmd += " passive"
            elif config_data["neighbor"]["transport"].get("multi_session"):
                self_cmd += " multi-session"
            elif config_data["neighbor"]["transport"].get(
                "path_mtu_discovery"
            ):
                self_cmd += " path-mtu-discovery"
                if config_data["neighbor"]["transport"][
                    "path_mtu_discovery"
                ].get("disable"):
                    self_cmd += " disable"
            commands.append(self_cmd)
        if "ttl_security" in config_data["neighbor"]:
            commands.append(
                "{0} ttl-security {ttl_security}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "unsuppress_map" in config_data["neighbor"]:
            commands.append(
                "{0} unsuppress-map {unsuppress_map}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "version" in config_data["neighbor"]:
            commands.append(
                "{0} version {version}".format(cmd, **config_data["neighbor"])
            )
        if "weight" in config_data["neighbor"]:
            commands.append(
                "{0} weight {weight}".format(cmd, **config_data["neighbor"])
            )
        return commands


def _tmplt_redistribute(config_data):
    if "redistribute" in config_data:

        def common_config(command, param):
            if config_data["redistribute"][param].get("metric"):
                command += " metric {metric}".format(
                    **config_data["redistribute"][param]
                )
            if config_data["redistribute"][param].get("route_map"):
                command += " route-map {route_map}".format(
                    **config_data["redistribute"][param]
                )
            return command

        command = "redistribute"
        if config_data["redistribute"].get("application"):
            command += " application {name}".format(
                **config_data["redistribute"]["application"]
            )
            command = common_config(command, "application")
        elif config_data["redistribute"].get("bgp"):
            command += " bgp {as_number}".format(
                **config_data["redistribute"]["bgp"]
            )
            command = common_config(command, "bgp")
        elif config_data["redistribute"].get("connected"):
            command += " connected"
            command = common_config(command, "connected")
        elif config_data["redistribute"].get("eigrp"):
            command += " eigrp {as_number}".format(
                **config_data["redistribute"]["eigrp"]
            )
            command = common_config(command, "eigrp")
        elif config_data["redistribute"].get("isis"):
            command += " isis {area_tag}".format(
                **config_data["redistribute"]["isis"]
            )
            if config_data["redistribute"]["isis"].get("clns"):
                command += " clns"
            elif config_data["redistribute"]["isis"].get("ip"):
                command += " ip"
            command = common_config(command, "isis")
        elif config_data["redistribute"].get("iso_igrp"):
            command += " iso-igrp {area_tag}".format(
                **config_data["redistribute"]["iso_igrp"]
            )
            if config_data["redistribute"]["iso_igrp"].get("route_map"):
                command += " route-map {route_map}".format(
                    **config_data["redistribute"]["iso_igrp"]
                )
        elif config_data["redistribute"].get("lisp"):
            command += " lisp"
            command = common_config(command, "lisp")
        elif config_data["redistribute"].get("mobile"):
            command += " mobile"
            command = common_config(command, "mobile")
        elif config_data["redistribute"].get("odr"):
            command += " odr"
            command = common_config(command, "odr")
        elif config_data["redistribute"].get("rip"):
            command += " rip"
            command = common_config(command, "rip")
        elif config_data["redistribute"].get("ospf"):
            command += " ospf {process_id}".format(
                **config_data["redistribute"]["ospf"]
            )
            if config_data["redistribute"]["ospf"].get("match"):
                command += " match"
                if config_data["redistribute"]["ospf"]["match"].get(
                    "external"
                ):
                    command += " external"
                if config_data["redistribute"]["ospf"]["match"].get(
                    "internal"
                ):
                    command += " internal"
                if config_data["redistribute"]["ospf"]["match"].get(
                    "nssa_external"
                ):
                    command += " nssa-external"
                if config_data["redistribute"]["ospf"]["match"].get("type_1"):
                    command += " 1"
                elif config_data["redistribute"]["ospf"]["match"].get(
                    "type_2"
                ):
                    command += " 2"
            if config_data["redistribute"]["ospf"].get("vrf"):
                command += " vrf"
            command = common_config(command, "ospf")
        elif config_data["redistribute"].get("ospfv3"):
            command += " ospfv3 {process_id}".format(
                **config_data["redistribute"]["ospfv3"]
            )
            if config_data["redistribute"]["ospfv3"].get("match"):
                command += " match"
                if config_data["redistribute"]["ospfv3"]["match"].get(
                    "external"
                ):
                    command += " external"
                if config_data["redistribute"]["ospfv3"]["match"].get(
                    "internal"
                ):
                    command += " internal"
                if config_data["redistribute"]["ospfv3"]["match"].get(
                    "nssa_external"
                ):
                    command += " nssa-external"
                if config_data["redistribute"]["ospfv3"]["match"].get(
                    "type_1"
                ):
                    command += " 1"
                elif config_data["redistribute"]["ospfv3"]["match"].get(
                    "type_2"
                ):
                    command += " 2"
            command = common_config(command, "ospf")
        elif config_data["redistribute"].get("static"):
            command += " static"
            command = common_config(command, "static")
        elif config_data["redistribute"].get("vrf"):
            if config_data["redistribute"]["vrf"].get("name"):
                command += " vrf {name}".format(
                    **config_data["redistribute"]["vrf"]
                )
            elif config_data["redistribute"]["vrf"].get("global"):
                command += " vrf global"

        return command


def _tmplt_bgp_timers(config_data):
    if "timers" in config_data:
        command = "timers bgp"
        if config_data["timers"].get("keepalive"):
            command += " {keepalive}".format(**config_data["timers"])
        if config_data["timers"].get("holdtime"):
            command += " {holdtime}".format(**config_data["timers"])
        if config_data["timers"].get("min_holdtime"):
            command += " {min_holdtime}".format(**config_data["timers"])
    return command


class Bgp_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Bgp_globalTemplate, self).__init__(lines=lines, tmplt=self)

    PARSERS = [
        {
            "name": "as_number",
            "getval": re.compile(
                r"""^router*
                    \s*bgp*
                    \s*(?P<as_number>\d+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "as_number",
            "setval": "router bgp {{ as_number }}",
            "result": {"as_number": "{{ as_number }}"},
            "shared": True,
        },
        {
            "name": "bgp.additional_paths",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*additional-paths*
                    \s*(?P<install>install)*
                    \s*(?P<receive>receive)*
                    \s*(?P<select>select)*
                    \s*(?P<select_all>all)*
                    \s*(?P<select_backup>backup)*
                    \s*(?P<select_best>best\s\d)*
                    \s*(?P<select_best_external>best-external)*
                    \s*(?P<select_group_best>group-best)*
                    \s*(?P<send>send)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_additional_paths,
            "result": {
                "bgp": {
                    "additional_paths": {
                        "install": "{{ True if install is defined }}",
                        "receive": "{{ True if receive is defined }}",
                        "select": {
                            "all": "{{ True if select_all is defined }}",
                            "backup": "{{ True if select_backup is defined }}",
                            "best": "{{ select_best.split('best ')[1] if select_best is defined }}",
                            "best_external": "{{ True if select_best_external is defined }}",
                            "group_best": "{{ True if select_group_best is defined }}",
                        },
                        "send": "{{ True if send is defined }}",
                    }
                }
            },
        },
        {
            "name": "bgp.bestpath",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*bestpath*
                    \s*(?P<aigp>aigp\signore)*
                    \s*(?P<compare_routerid>compare-routerid)*
                    \s*(?P<cost_community>cost-community\signore)*
                    \s*(?P<med>med\s(confed|missing-as-worst|confed\smissing-as-worst))*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_bestpath,
            "result": {
                "bgp": {
                    "bestpath": [
                        {
                            "aigp": "{{ True if aigp is defined }}",
                            "compare_routerid": "{{ True if compare_routerid is defined }}",
                            "cost_community": "{{ True if cost_community is defined }}",
                            "med": {
                                "confed": "{{ True if med is defined and 'confed' in med }}",
                                "missing_as_worst": "{{ True if med is defined and 'missing-as-worst' in med }}",
                            },
                        }
                    ]
                }
            },
        },
        {
            "name": "bgp.config",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*(?P<advertise_best_external>advertise-best-external)*
                    \s*(?P<aggregate_timer>aggregate-timer\s\d+)*
                    \s*(?P<always_compare_med>always-compare-med)*
                    \s*(?P<asnotation>asnotation\sdot)*
                    \s*(?P<client_to_client>client-to-client\sreflection\s(all|intra-cluster))*
                    \s*(?P<cluster_id>cluster-id\s.*)*
                    \s*(?P<confederation>confederation\s(identifier\s\d+|peers\s\d+))*
                    \s*(?P<consistency_checker>consistency-checker\s((auto-repair\sinterval\s\d+|auto-repair)|(error-message\sinterval\s\d+|error-message)))*
                    \s*(?P<deterministic_med>deterministic-med)*
                    \s*(?P<dmzlink_bw>dmzlink-bw)*
                    \s*(?P<enforce_first_as>enforce-first-as)*
                    \s*(?P<enhanced_error>enhanced-error)*
                    \s*(?P<fast_external_fallover>fast-external-fallover)*
                    \s*(?P<graceful_restart>graceful-restart(\sextended|\srestart-time\s\d+|\sstalepath-time\s\d+))*
                    \s*(?P<inject_map>inject-map\s\S+\sexist-map\s\S+\scopy-attributes|inject-map\s\S+\sexist-map\s\S+)*
                    \s*(?P<listen>listen\s(limit\s\d+|(range\s.*peer-group\s\S+|range\s.*)))*
                    \s*(?P<log_neighbor_changes>log-neighbor-changes)*
                    \s*(?P<maxas_limit>maxas-limit\s\d+)*
                    \s*(?P<maxcommunity_limit>maxas-limit\s\d+)*
                    \s*(?P<maxextcommunity_limit>maxextcommunity-limit\s\d+)*
                    \s*(?P<nexthop>nexthop\s(route-map\s\S+|trigger\s(delay\s\d+|enable)))*
                    \s*(?P<recursion>recursion\shost)*
                    \s*(?P<redistribute_internal>redistribute-internal)*
                    \s*(?P<refresh>refresh\s(max-eor-time\s\d+|stalepath-time\s\d+))*
                    \s*(?P<regexp>regexp\sdeterministic)*
                    \s*(?P<router_id>router-id\s((?:[0-9]{1,3}\.){3}[0-9]{1,3}|interface\s\S+\s\S+|vrf\sauto-assign))*
                    \s*(?P<route_map>route-map\spriority)*
                    \s*(?P<scan_time>scan-time\s\d+)*
                    \s*(?P<slow_peer>slow-peer((\sdetection\sthreshold\d+|\sdetection)|(\ssplit-update-group\sdynamic\spermanent|\ssplit-update-group\sdynamic)))*
                    \s*(?P<snmp>snmp\straps\sadd-type)*
                    \s*(?P<sso>sso\sroute-refresh-enable)*
                    \s*(?P<soft_reconfig_backup>soft-reconfig-backup)*
                    \s*(?P<suppress_inactive>suppress-inactive)*
                    \s*(?P<transport>transport\spath-mtu-discovery)*
                    \s*(?P<update_delay>update-delay\s\d+)*
                    \s*(?P<update_group>update-group\ssplit\sas-override)*
                    \s*(?P<upgrade_cli>upgrade-cli\saf-mode|upgrade-cli)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_config,
            "compval": "bgp",
            "result": {
                "bgp": {
                    "advertise_best_external": "{{ True if advertise_best_external is defined }}",
                    "aggregate_timer": "{{ aggregate_timer.split('aggregate-timer ')[1] if aggregate_timer is defined }}",
                    "always_compare_med": "{{ True if always_compare_med is defined }}",
                    "asnotation": "{{ True if asnotation is defined }}",
                    "client_to_client": {
                        "set": "{{ True if client_to_client is defined and client_to_client.split(' ')|length == 2 }}",
                        "all": "{{ True if client_to_client is defined and 'all' in client_to_client }}",
                        "intra_cluster": "{{\
                            client_to_client.split('cluster-id ')[1]\
                                if client_to_client is defined and 'intra-cluster' in client_to_client }}",
                    },
                    "cluster_id": "{{ cluster_id.split('cluster-id ')[1] if cluster_id is defined }}",
                    "confederation": {
                        "identifier": "{{ confederation.split('confederation identifier ')[1] if confederation is defined }}",
                        "peers": "{{ confederation.split('confederation peers ')[1] if confederation is defined }}",
                    },
                    "consistency_checker": {
                        "auto_repair": {
                            "set": "{{\
                                True if consistency_checker is defined and\
                                    'auto-repair' in consistency_checker and\
                                        consistency_checker.split(' ')|length == 2 }}",
                            "interval": "{{\
                                consistency_checker.split('interval ')[1] if consistency_checker is defined and\
                                    consistency_checker.split(' ')|length > 2 }}",
                        },
                        "error_message": {
                            "set": "{{\
                                True if consistency_checker is defined and\
                                    'error-message' in consistency_checker and consistency_checker.split(' ')|length == 2 }}",
                            "interval": "{{\
                                consistency_checker.split('interval ')[1] if consistency_checker is defined and\
                                    consistency_checker.split(' ')|length > 2 }}",
                        },
                    },
                    "deterministic_med": "{{ True if deterministic_med is defined }}",
                    "dmzlink_bw": "{{ True if dmzlink_bw is defined }}",
                    "enforce_first_as": "{{ True if enforce_first_as is defined }}",
                    "enhanced_error": "{{ True if enhanced_error is defined }}",
                    "fast_external_fallover": "{{ True if fast_external_fallover is defined }}",
                    "graceful_restart": {
                        "set": "{{ True if graceful_restart is defined and graceful_restart.split(' ')|length == 2 }}",
                        "extended": "{{ True if graceful_restart is defined and 'extended' in graceful_restart }}",
                        "restart_time": "{{\
                            graceful_restart.split('graceful-restart restart-time ')[1] if graceful_restart is defined and\
                                'restart-time' in graceful_restart }}",
                        "stalepath_time": "{{\
                            graceful_restart.split('graceful-restart stalepath-time ')[1] if graceful_restart is defined and\
                                'stalepath-time' in graceful_restart }}",
                    },
                    "inject_map": {
                        "name": "{{ inject_map.split(' ')[1] if inject_map is defined }}",
                        "exist_map_name": "{{ inject_map.split('exist-map ')[1].split(' ')[0] if inject_map is defined and 'exist-map' in inject_map }}",
                        "copy_attributes": "{{ True if inject_map is defined and 'copy-attributes' in inject_map }}",
                    },
                    "listen": {
                        "limit": "{{ listen.split('limit ')[1] if listen is defined and 'limit' in listen }}",
                        "range": {
                            "ipv4_with_subnet": "{{ listen.split('range ')[1].split(' ')[0] if listen is defined and ':' not in listen and '.' in listen }}",
                            "ipv6_with_subnet": "{{ listen.split('range ')[1].split(' ')[0] if listen is defined and ':' in listen and '.' in listen }}",
                            "peer_group": "{{ listen.split('peer-group ')[1] if listen is defined and 'peer-group' in listen }}",
                        },
                    },
                    "log_neighbor_changes": "{{ True if log_neighbor_changes is defined }}",
                    "maxas_limit": "{{ maxas_limit.split('maxas-limit ')[1] if maxas_limit is defined }}",
                    "maxcommunity_limit": "{{ maxcommunity_limit.split('maxcommunity-limit ')[1] if maxcommunity_limit is defined }}",
                    "maxextcommunity_limit": "{{ maxextcommunity_limit.split('maxextcommunity-limit ')[1] if maxextcommunity_limit is defined }}",
                    "nexthop": {
                        "route_map": "{{ nexthop.split('route-map ')[1] if nexthop is defined and 'route-map' in nexthop }}",
                        "trigger": {
                            "delay": "{{ nexthop.split('delay ')[1] if nexthop is defined and 'delay' in nexthop }}",
                            "enable": "{{ True if nexthop is defined and 'enable' in nexthop }}",
                        },
                    },
                    "recursion": "{{ True if recursion is defined }}",
                    "redistribute_internal": "{{ True if redistribute_internal is defined }}",
                    "refresh": {
                        "max_eor_time": "{{ refresh.split('max-eor-time ')[1] if refresh is defined }}",
                        "stalepath_time": "{{ refresh.split('stalepath-time ')[1] if refresh is defined }}",
                    },
                    "regexp": "{{ True if regexp is defined }}",
                    "router_id": {
                        "address": "{{ router_id.split(' ')[1] if router_id is defined and '.' in router_id }}",
                        "interface": "{{ router_id.split('interface ')[1] if router_id is defined and 'interface' in router_id }}",
                        "vrf": "{{ True if router_id is defined and 'vrf auto-assign' in router_id }}",
                    },
                    "route_map": "{{ True if route_map is defined }}",
                    "scan_time": "{{ scan_time.split('scan-time ')[1] if scan_time is defined }}",
                    "slow_peer": {
                        "detection": {
                            "set": "{{ True if slow_peer is defined and 'detection' in slow_peer and 'threshold' not in slow_peer }}",
                            "threshold": "{{ slow_peer.split('threshold ')[1] if slow_peer is defined and 'threshold' in slow_peer }}",
                        },
                        "split_update_group": {
                            "dynamic": "{{ True if split_dynamic is defined and split_dynamic.split('dynamic ')[1] == 'disable' }}",
                            "static": "{{ True if split_static is defined }}",
                        },
                    },
                    "snmp": "{{ True if snmp is defined }}",
                    "sso": "{{ True if sso is defined }}",
                    "soft_reconfig_backup": "{{ True if soft_reconfig_backup is defined }}",
                    "suppress_inactive": "{{ True if suppress_inactive is defined }}",
                    "transport": "{{ True if transport is defined }}",
                    "update_delay": "{{ update_delay.split('update-delay ')[1] if update_delay is defined }}",
                    "update_group": "{{ True if update_group is defined }}",
                    "upgrade_cli": {
                        "set": "{{ True if graceful_restart is defined and graceful_restart.split(' ')|length == 2 }}",
                        "af_mode": "{{ True if upgrade_cli is defined and 'af-mode' in upgrade_cli }}",
                    },
                }
            },
        },
        {
            "name": "bgp.dampening",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*dampening*
                    \s*(?P<penalty_half_time>\d+)*
                    \s*(?P<reuse_route_val>\d+)*
                    \s*(?P<suppress_route_val>\d+)*
                    \s*(?P<max_suppress>\d+)*
                    \s*(?P<route_map>\S+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_dampening,
            "result": {
                "bgp": {
                    "dampening": {
                        "penalty_half_time": "{{ penalty_half_time if penalty_half_time is defined }}",
                        "reuse_route_val": "{{ reuse_route_val if penalty_half_time is defined }}",
                        "suppress_route_val": "{{ suppress_route_val if penalty_half_time is defined }}",
                        "max_suppress": "{{ max_suppress if penalty_half_time is defined }}",
                        "route_map": "{{ dampening.split('route-map ')[1] if dampening is defined and 'route-map' in dampening }}",
                    }
                }
            },
        },
        {
            "name": "bgp.graceful_shutdown",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*graceful-shutdown\sall*
                    \s*(?P<neighbors>neighbors\s(\d+|activate))*
                    \s*(?P<vrfs>vrfs\s(\d+|activate))*
                    \s*(?P<local_preference>local-preference\s\d+)*
                    \s*(?P<community>community\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_graceful_shutdown,
            "result": {
                "bgp": {
                    "graceful_shutdown": {
                        "neighbors": {
                            "time": "{{ neighbors.split('neighbors ')[1] if neighbors is defined and 'activate' not in neighbors }}",
                            "activate": "{{ True if neighbors is defined and 'activate' in neighbors }}",
                        },
                        "vrfs": {
                            "time": "{{ vrfs.split('vrfs ')[1] if vrfs is defined and 'activate' not in vrfs }}",
                            "activate": "{{ True if vrfs is defined and 'activate' in vrfs }}",
                        },
                        "community": "{{ community.split('community ')[1] if community is defined }}",
                        "local_preference": "{{ local_preference.split('local-preference ')[1] if local_preference is defined }}",
                    }
                }
            },
        },
        {
            "name": "bgp.nopeerup_delay",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*nopeerup-delay*
                    \s*(?P<cold_boot>cold-boot\s\d+)*
                    \s*(?P<nsf_switchover>nsf-switchover\s\d+)*
                    \s*(?P<post_boot>post-boot\s\d+)*
                    \s*(?P<user_initiated>user-initiated\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_nopeerup_delay,
            "result": {
                "bgp": {
                    "nopeerup_delay": [
                        {
                            "cold_boot": "{{ cold_boot.split('cold-boot ')[1] if cold_boot is defined }}",
                            "nsf_switchover": "{{ nsf_switchover.split('nsf-switchover ')[1] if nsf_switchover is defined }}",
                            "post_boot": "{{ post_boot.split('post-boot ')[1] if post_boot is defined }}",
                            "user_initiated": "{{ user_initiated.split('user-initiated ')[1] if user_initiated is defined }}",
                        }
                    ]
                }
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""\s*neighbor*
                    \s*(?P<neighbor>(?:[0-9]{1,3}\.){3}[0-9]{1,3}|host\s(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\S+|\S+)*
                    \s*(?P<activate>activate)*
                    \s*(?P<additional_paths>additional-paths\s(disable|receive|send))*
                    \s*(?P<advertise>advertise\sadditional-paths\sall\sbest\s\d+\sgroup-best|advertise\sadditional-paths\sbest\s\d+\sgroup-best|advertise\sadditional-paths\sall\sgroup-best|advertise\sbest-external|advertise\sdiverse-path\sbackup\smpath|advertise\sdiverse-path\sbackup|advertise\sdiverse-path\smpath)*
                    \s*(?P<advertisement_interval>advertisement-interval\s\d+)*
                    \s*(?P<aigp>aigp\ssend\scost-community\s\d+\spoi\sigp-cost\stransitive|aigp\ssend\scost-community\s\d+\spoi\spre-bestpath\stransitive|aigp\ssend\smed|aigp)*
                    \s*(?P<allow_policy>allow-policy)*
                    \s*(?P<allowas_in>allowas-in\s\d+)*
                    \s*(?P<as_override>as-override)*
                    \s*(?P<bmp_activate>bmp-activate\s(all|server\s\d+))*
                    \s*(?P<capability>capability\s(both|receive|send))*
                    \s*(?P<cluster_id>cluster-id\s\S+)*
                    \s*(?P<default_originate>default-originate\sroute-map|default-originate)*
                    \s*(?P<description>description\s\S.+)*
                    \s*(?P<disable_connected_check>disable-connected-check)*
                    \s*(?P<distribute_list>distribute-list\s\d+\s(in|out))*
                    \s*(?P<dmzlink_bw>dmzlink-bw)*
                    \s*(?P<ebgp_multihop>(ebgp-multihop\s\d+|ebgp-multihop))*
                    \s*(?P<fall_over>fall-over\s((bfd\s(single-hop|multi-hop)|bfd)|route-map\s\S+))*
                    \s*(?P<filter_list>filter-list\s\d+\s(in|out))*
                    \s*(?P<ha_mode>ha-mode\s(graceful-restart\sdisable|graceful-restart))*
                    \s*(?P<inherit>inherit\speer-session\s\S+)*
                    \s*(?P<local_as>(local-as\s\d+\s(dual-as|(no-prepend\sreplace-as|no-prepend))|local-as))*
                    \s*(?P<log_neighbor_changes>log-neighbor-changes\sdisable|log-neighbor-changes)*
                    \s*(?P<maximum_prefix>maximum-prefix\s(\d+\s\d+\s(restart\s\d+|warning-only)|\d+\s(restart\s\d+|warning-only)))*
                    \s*(?P<next_hop_self>next-hop-self\sall|next-hop-self)*
                    \s*(?P<next_hop_unchanged>next-hop-unchanged\sallpaths|next-hop-unchanged)*
                    \s*(?P<password>password\s\S+)*
                    \s*(?P<path_attribute>path-attribute\s(discard\srange\s\d+\s\d+\sin|discard\s\d+\sin)|path-attribute\s(treat-as-withdraw\srange\s\d+\s\d+\sin|treat-as-withdraw\s\d+\sin))*
                    \s*(?P<peer_group>peer-group\s\S+)*
                    \s*(?P<remote_as>remote-as\s\d+)*
                    \s*(?P<remove_private_as>remove-private-as\sall\sreplace-as|remove-private-as\sall|remove-private-as)*
                    \s*(?P<route_map>route-map\s\S+\s(in|out))*
                    \s*(?P<route_reflector_client>route-reflector-client)*
                    \s*(?P<route_server_client>route-server-client\scontext\s\S+|route-server-client)*
                    \s*(?P<send_community>send-community\s(both|extended|standard)|send-community)*
                    #\s*(?P<send_label>send-label\sexplicit-null|send-label)*
                    \s*(?P<soft_reconfiguration>soft-reconfiguration\sinbound)*
                    \s*(?P<slow_peer>slow-peer\s(detection.*|split-update-group.*))*
                    \s*(?P<timers>(timers\s\d+\s\d+\s\d+|timers\s\d+\s\d+))*
                    \s*(?P<transport>(transport\s(connection-mode\sactive|connection-mode\spassive)|transport\smulti-session|transport\s(path-mtu-discovery\sdisable|path-mtu-discovery)))*
                    \s*(?P<ttl_security>ttl-security\shops\s\d+)*
                    \s*(?P<unsuppress_map>unsuppress-map\s\S+)*
                    \s*(?P<version>version\s\d+)*
                    \s*(?P<weight>weight\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor,
            "compval": "neighbor",
            "result": {
                "neighbor": [
                    {
                        "address": "{{ neighbor if ':' not in neighbor and '.' in neighbor }}",
                        "ipv6_address": "{{ neighbor if ':' in neighbor and '.' in neighbor }}",
                        "tag": "{{ neighbor if ':' not in neighbor and '.' not in neighbor }}",
                        "activate": "{{ True if activate is defined }}",
                        "additional_paths": {
                            "disable": "{{ True if additional_paths is defined and 'disable' in additional_paths }}",
                            "receive": "{{ True if additional_paths is defined and 'receive' in additional_paths }}",
                            "send": "{{ True if additional_paths is defined and 'send' in additional_paths }}",
                        },
                        "advertise": {
                            "additional_paths": {
                                "all": "{{ True if advertise is defined and 'additional-paths' in advertise and 'all' in advertise }}",
                                "best": "{{\
                                    advertise.split('best ')[1].split(' ')[0] if advertise is defined and\
                                        'additional-paths' in advertise and 'best' in advertise }}",
                                "group_best": "{{ True if advertise is defined and 'additional-paths' in advertise and 'group-best' in advertise }}",
                            },
                            "best_external": "{{ True if advertise is defined and 'best-external' in advertise }}",
                            "diverse_path": {
                                "backup": "{{ True if advertise is defined and 'diverse-path' in advertise and 'backup' in advertise }}",
                                "mpath": "{{ True if advertise is defined and 'diverse-path' in advertise and 'mpath' in advertise }}",
                            },
                        },
                        "advertisement_interval": "{{ advertisement_interval.split('advertisement-interval ')[1] if advertisement_interval is defined }}",
                        "aigp": {
                            "enable": "{{ True if aigp is defined and aigp.split(' ')|length == 1 }}",
                            "send": {
                                "cost_community": {
                                    "id": "{{ aigp.split('send cost-community ')[1].split(' ')[0] if aigp is defined and 'send cost-community' in aigp }}",
                                    "poi": {
                                        "igp_cost": "{{ True if aigp is defined and 'poi igp-cost' in aigp }}",
                                        "pre_bestpath": "{{ True if aigp is defined and 'poi pre-bestpath' in aigp }}",
                                        "transitive": "{{ True if aigp is defined and 'transitive' in aigp }}",
                                    },
                                },
                                "med": "{{ True if aigp is defined and 'send med' in aigp }}",
                            },
                        },
                        "allow_policy": "{{ True if allow_policy is defined }}",
                        "allowas_in": "{{ allowas_in.split('allowas-in ')[1] if allowas_in is defined }}",
                        "as_override": "{{ True if as_override is defined }}",
                        "bmp_activate": {
                            "all": "{{ True if bmp_activate is defined and 'all' in bmp_activate }}",
                            "server": "{{ bmp_activate.split('server ')[1] if bmp_activate is defined and 'server' in bmp_activate }}",
                        },
                        "capability": {
                            "both": "{{ True if capability is defined and 'both' in capability }}",
                            "receive": "{{ True if capability is defined and 'receive' in capability }}",
                            "send": "{{ True if capability is defined and 'send' in capability }}",
                        },
                        "cluster_id": "{{ cluster_id.split('cluster-id ')[1] if bmp_activate is defined }}",
                        "default_originate": {
                            "set": "{{ True if default_originate is defined and default_originate.split(' ')|length == 1 }}",
                            "route_map": "{{ default_originate.split(' ')[1] if default_originate is defined and default_originate.split(' ')|length > 1 }}",
                        },
                        "description": "{{ description.split('description ')[1] if description is defined }}",
                        "disable_connected_check": "{{ True if disable_connected_check is defined }}",
                        "distribute_list": {
                            "acl": "{{ distribute_list.split(' ')[1] if distribute_list is defined }}",
                            "in": "{{ True if distribute_list is defined and 'in' in distribute_list }}",
                            "out": "{{ True if distribute_list is defined and 'out' in distribute_list }}",
                        },
                        "dmzlink_bw": "{{ True if dmzlink_bw is defined }}",
                        "ebgp_multihop": {
                            "enable": "{{ True if ebgp_multihop is defined and ebgp_multihop.split(' ')|length == 1 }}",
                            "hop_count": "{{ ebgp_multihop.split(' ')[1] if ebgp_multihop is defined and len(ebgp_multihop.split(' ')) > 1 }}",
                        },
                        "fall_over": {
                            "bfd": {
                                "set": "{{ True if fall_over is defined and\
                                    'bfd' in fall_over and 'single-hop' not in fall_over and 'multi-hop' not in fall_over }}",
                                "multi_hop": "{{ True if fall_over is defined and 'bfd' in fall_over and 'multi-hop' in fall_over }}",
                                "single_hop": "{{ True if fall_over is defined and 'bfd' in fall_over and 'single-hop' in fall_over }}",
                            },
                            "route_map": "{{ fall_over.split('fall-over route-map ')[1] if fall_over is defined and 'route-map' in fall_over }}",
                        },
                        "filter_list": {
                            "acl": "{{ filter_list.split(' ')[1] if filter_list is defined }}",
                            "in": "{{ True if filter_list is defined and 'in' in filter_list }}",
                            "out": "{{ True if filter_list is defined and 'out' in filter_list }}",
                        },
                        "ha_mode": {
                            "set": "{{ True if ha_mode is defined and 'disable' not in ha_mode }}",
                            "disable": "{{ True if ha_mode is defined and 'disable' in ha_mode }}",
                        },
                        "inherit": "{{ inherit.split('inherit peer-session ')[1] if inherit is defined }}",
                        "local_as": {
                            "set": "{{ True if local_as is defined and local_as.split(' ')|length == 1 }}",
                            "number": "{{ local_as.split(' ')[1] if local_as is defined and local_as.split(' ')|length > 1 }}",
                            "dual_as": "{{ True if local_as is defined and local_as.split(' ')|length > 2 and 'dual-as' in local_as }}",
                            "no_prepend": {
                                "set": "{{\
                                    True if local_as is defined and\
                                        local_as.split(' ')|length > 2 and 'no-prepend' in local_as and\
                                            'replace-as' not in local_as }}",
                                "replace_as": "{{ True if local_as is defined and\
                                    local_as.split(' ')|length > 2 and 'no-prepend' in local_as and 'replace-as' in local_as }}",
                            },
                        },
                        "log_neighbor_changes": {
                            "set": "{{ True if log_neighbor_changes is defined and 'disable' not in log_neighbor_changes }}",
                            "disable": "{{ True if log_neighbor_changes is defined and 'disable' in log_neighbor_changes }}",
                        },
                        "maximum_prefix": {
                            "max_no": "{{ maximum_prefix.split(' ')[1] if maximum_prefix is defined }}",
                            "threshold_val": "{{ maximum_prefix.split(' ')[2] if maximum_prefix is defined and\
                                maximum_prefix.split(' ')|length > 3 and maximum_prefix.split(' ')[1] != 'restart' }}",
                            "restart": "{{ maximum_prefix.split('restart ')[1] if maximum_prefix is defined and 'restart' in maximum_prefix }}",
                            "warning_only": "{{ True if maximum_prefix is defined and 'warning-only' in maximum_prefix }}",
                        },
                        "next_hop_self": {
                            "set": "{{ True if next_hop_self is defined and next_hop_self.split(' ')|length == 1 }}",
                            "all": "{{ True if next_hop_self is defined and next_hop_self.split(' ')|length > 1 }}",
                        },
                        "next_hop_unchanged": {
                            "set": "{{ True if next_hop_unchanged is defined and next_hop_unchanged.split(' ')|length == 1 }}",
                            "allpaths": "{{ True if next_hop_unchanged is defined and next_hop_unchanged.split(' ')|length > 1 }}",
                        },
                        "password": "{{ password.split(' ')[1] if password is defined }}",
                        "path_attribute": {
                            "discard": {
                                "type": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                    path_attribute.split(' ')|length <= 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                "range": {
                                    "start": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                        path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                    "end": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                        path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[4] }}{% endif %}",
                                },
                                "in": "{% if path_attribute is defined and 'discard range' in path_attribute and\
                                    'in' in path_attribute %}{{ True }}{% endif %}",
                            },
                            "treat_as_withdraw": {
                                "type": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                    path_attribute.split(' ')|length <= 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                "range": {
                                    "start": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                        path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                    "end": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                        path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[4] }}{% endif %}",
                                },
                                "in": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and\
                                    'in' in path_attribute %}{{ True }}{% endif %}",
                            },
                        },
                        "peer_group": "{{ listen.split('peer-group ')[1] if listen is defined and 'peer-group' in listen }}",
                        "remote_as": "{{ remote_as.split('remote-as ')[1] if remote_as is defined }}",
                        "remove_private_as": {
                            "set": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length == 1 }}",
                            "all": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length > 1 and 'all' in remove_private_as }}",
                            "replace_as": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length > 1 and\
                                'replace-as' in remove_private_as }}",
                        },
                        "route_map": {
                            "name": "{{ route_map.split(' ')[1] if route_map is defined }}",
                            "in": "{{ True if route_map is defined and 'in' in route_map.split(' ') }}",
                            "out": "{{ True if route_map is defined and 'out' in route_map.split(' ') }}",
                        },
                        "route_reflector_client": "{{ True if route_reflector_client is defined }}",
                        "route_server_client": {
                            "set": "{{ True if route_server_client is defined and route_server_client.split(' ')|length == 1 }}",
                            "context": "{{ route_server_client.split('route-server-client context ')[1] if route_server_client is defined }}",
                        },
                        "send_community": {
                            "set": "{{ True if send_community is defined and send_community.split(' ')|length == 1 }}",
                            "both": "{{ True if send_community is defined and 'both' in send_community }}",
                            "extended": "{{ True if send_community is defined and 'extended' in send_community }}",
                            "standard": "{{ True if send_community is defined and 'standard' in send_community }}",
                        },
                        "send_label": {
                            "set": "{{ True if send_label is defined and send_label.split(' ')|length == 1 }}",
                            "explicit_null": "{{ True if send_label is defined and 'explicit-null' in send_label }}",
                        },
                        "slow_peer": {
                            "detection": {
                                "enable": "{{ True if slow_peer is defined and 'disable' not in slow_peer and 'threshold' not in slow_peer }}",
                                "disable": "{{ True if slow_peer is defined and 'disable' in slow_peer }}",
                                "threshold": "{{ slow_peer.split('threshold ')[1] if slow_peer is defined and 'threshold' in slow_peer }}",
                            },
                            "split_update_group": {
                                "dynamic": {
                                    "enable": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and\
                                        'disable' not in slow_peer and 'threshold' not in slow_peer }}",
                                    "disable": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and 'disable' in slow_peer }}",
                                    "permanent": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and 'permanent' in slow_peer }}",
                                },
                                "static": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and 'static' in slow_peer }}",
                            },
                        },
                        "soft_reconfiguration": "{{ True if soft_reconfiguration is defined }}",
                        "timers": {
                            "interval": "{{ timers.split(' ')[1] if timers is defined }}",
                            "holdtime": "{{ timers.split(' ')[2] if timers is defined }}",
                            "min_holdtime": "{{ timers.split(' ')[3] if timers is defined and timers.split(' ')|length > 3 }}",
                        },
                        "translate_update": {
                            "set": "{{ True if translate_update is defined and translate_update.split(' ')|length == 1 }}",
                            "nlri": {
                                "multicast": "{{ True if translate_update is defined and 'nlri multicast' in translate_update }}",
                                "unicast": "{{ True if translate_update is defined and 'nlri unicast' in translate_update }}",
                            },
                        },
                        "transport": {
                            "connection_mode": {
                                "active": "{{ True if transport is defined and 'connection-mode active' in transport }}",
                                "passive": "{{ True if transport is defined and 'connection-mode passive' in transport }}",
                            },
                            "multi_session": "{{ True if transport is defined and 'multi-session' in transport }}",
                            "path_mtu_discovery": {
                                "set": "{{ True if transport is defined and 'path-mtu-discovery' in transport and 'disable' not in transport }}",
                                "disable": "{{ True if transport is defined and 'path-mtu-discovery' in transport and 'disable' in transport }}",
                            },
                        },
                        "ttl_security": "{{ ttl_security.split('ttl-security hops ')[1] if ttl_security is defined }}",
                        "unsuppress_map": "{{ unsuppress_map.split('unsuppress-map ')[1] if unsuppress_map is defined }}",
                        "version": "{{ version.split('version ')[1] if version is defined }}",
                        "weight": "{{ weight.split('weight ')[1] if weight is defined }}",
                    }
                ]
            },
        },
        {
            "name": "redistribute",
            "getval": re.compile(
                r"""\s*redistribute*
                        \s*(?P<application>application\s\S+\smetric\s\d+\sroute-map\s\S+|application\s\S+\s(metric\s\d+|route-map\s\S+))*
                        \s*(?P<bgp>bgp\s\d+\smetric\s\d+\sroute-map\s\S+|bgp\s\d+\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<connected>connected\s(metric\s\d+\sroute-map\s\S+|metric\s\d+))*
                        \s*(?P<eigrp>eigrp\s\d+\smetric\s\d+\sroute-map\s\S+|eigrp\s\d+\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<isis>isis\s\S+\sclns\smetric\s\d+\sroute-map\s\S+|isis\s\S+\sip\smetric\s\d+\sroute-map\s\S+|isis\s\S+\s(clns|ip)\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<iso_igrp>iso-igrp\s\S+\sroute-map\s\S+|iso-igrp\s\S+)*
                        \s*(?P<lisp>lisp\smetric\s\d+\sroute-map\s\S+|lisp\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<mobile>mobile\smetric\s\d+\sroute-map\s\S+|mobile\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<odr>odr\smetric\s\d+\sroute-map\s\S+|odr\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<ospf>ospf\s\d+(\s.*))*
                        \s*(?P<ospfv3>ospfv3\s\d+(\s.*))*
                        \s*(?P<rip>rip\smetric\s\d+\sroute-map\s\S+|rip\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<static>static\sclns\smetric\s\d+\sroute-map\s\S+|static\sip\smetric\s\d+\sroute-map\s\S+|static\s(clns|ip)\s(metric\s\d+\sroute-map\s\S+))*
                        \s*(?P<vrf>vrf\s\S+|vrf\sglobal)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "redistribute",
            "setval": _tmplt_redistribute,
            "result": {
                "redistribute": [
                    {
                        "application": {
                            "name": "{{ application.split(' ')[1] if application is defined }}",
                            "metric": "{{ application.split('metric ')[1].split(' ')[0] if application is defined and 'metric' in application }}",
                            "route_map": "{{ application.split('route-map ')[1].split(' ')[0] if application is defined and 'route-map' in application }}",
                        },
                        "bgp": {
                            "as_number": "{{ bgp.split(' ')[1] if bgp is defined }}",
                            "metric": "{{ bgp.split('metric ')[1].split(' ')[0] if bgp is defined and 'metric' in bgp }}",
                            "route_map": "{{ bgp.split('route-map ')[1].split(' ')[0] if bgp is defined and 'route-map' in bgp }}",
                        },
                        "connected": {
                            "metric": "{{ connected.split('metric ')[1].split(' ')[0] if connected is defined and 'metric' in connected }}",
                            "route_map": "{{ connected.split('route-map ')[1].split(' ')[0] if connected is defined and 'route-map' in connected }}",
                        },
                        "eigrp": {
                            "as_number": "{{ eigrp.split(' ')[1] if eigrp is defined }}",
                            "metric": "{{ eigrp.split('metric ')[1].split(' ')[0] if eigrp is defined and 'metric' in eigrp }}",
                            "route_map": "{{ eigrp.split('route-map ')[1].split(' ')[0] if eigrp is defined and 'route-map' in eigrp }}",
                        },
                        "isis": {
                            "area_tag": "{{ isis.split(' ')[1] if isis is defined }}",
                            "clns": "{{ True if isis is defined and 'clns' in isis }}",
                            "ip": "{{ True if isis is defined and 'ip' in isis }}",
                            "metric": "{{ isis.split('metric ')[1].split(' ')[0] if isis is defined and 'metric' in isis }}",
                            "route_map": "{{ isis.split('route-map ')[1].split(' ')[0] if isis is defined and 'route-map' in isis }}",
                        },
                        "iso_igrp": {
                            "area_tag": "{{ iso_igrp.split(' ')[1] if iso_igrp is defined }}",
                            "route_map": "{{ iso_igrp.split('route-map ')[1].split(' ')[0] if iso_igrp is defined and 'route-map' in iso_igrp }}",
                        },
                        "lisp": {
                            "metric": "{{ lisp.split('metric ')[1].split(' ')[0] if lisp is defined and 'metric' in lisp }}",
                            "route_map": "{{ lisp.split('route-map ')[1].split(' ')[0] if lisp is defined and 'route-map' in lisp }}",
                        },
                        "mobile": {
                            "metric": "{{ mobile.split('metric ')[1].split(' ')[0] if mobile is defined and 'metric' in mobile }}",
                            "route_map": "{{ mobile.split('route-map ')[1].split(' ')[0] if mobile is defined and 'route-map' in mobile }}",
                        },
                        "odr": {
                            "metric": "{{ odr.split('metric ')[1].split(' ')[0] if odr is defined and 'metric' in odr }}",
                            "route_map": "{{ odr.split('route-map ')[1].split(' ')[0] if odr is defined and 'route-map' in odr }}",
                        },
                        "ospf": {
                            "process_id": "{{ ospf.split(' ')[1] if ospf is defined }}",
                            "match": {
                                "external": "{{ True if ospf is defined and 'external' in ospf }}",
                                "internal": "{{ True if ospf is defined and 'internal' in ospf }}",
                                "nssa_external": "{{ True if ospf is defined and 'nssa-external' in ospf }}",
                                "type_1": "{{ True if ospf is defined and '1' in ospf }}",
                                "type_2": "{{ True if ospf is defined and '2' in ospf }}",
                            },
                            "metric": "{{ ospf.split('metric ')[1].split(' ')[0] if ospf is defined and 'metric' in ospf }}",
                            "route_map": "{{ ospf.split('route-map ')[1].split(' ')[0] if ospf is defined and 'route-map' in ospf }}",
                            "vrf": "{{ ospf.split('vrf ')[1].split(' ')[0] if ospf is defined and 'vrf' in ospf }}",
                        },
                        "ospfv3": {
                            "process_id": "{{ ospfv3.split(' ')[1] if ospf is defined }}",
                            "match": {
                                "external": "{{ True if ospfv3 is defined and 'external' in ospfv3 }}",
                                "internal": "{{ True if ospfv3 is defined and 'internal' in ospfv3 }}",
                                "nssa_external": "{{ True if ospfv3 is defined and 'nssa-external' in ospfv3 }}",
                                "type_1": "{{ True if ospfv3 is defined and '1' in ospfv3 }}",
                                "type_2": "{{ True if ospfv3 is defined and '2' in ospfv3 }}",
                            },
                            "metric": "{{ ospfv3.split('metric ')[1].split(' ')[0] if ospfv3 is defined and 'metric' in ospfv3 }}",
                            "route_map": "{{ ospfv3.split('route-map ')[1].split(' ')[0] if ospfv3 is defined and 'route-map' in ospfv3 }}",
                            "vrf": "{{ ospfv3.split('vrf ')[1].split(' ')[0] if ospfv3 is defined and 'vrf' in ospfv3 }}",
                        },
                        "rip": {
                            "metric": "{{ rip.split('metric ')[1].split(' ')[0] if rip is defined and 'metric' in rip }}",
                            "route_map": "{{ rip.split('route-map ')[1].split(' ')[0] if rip is defined and 'route-map' in rip }}",
                        },
                        "static": {
                            "clns": "{{ True if static is defined and 'clns' in static }}",
                            "ip": "{{ True if static is defined and 'ip' in static }}",
                            "metric": "{{ static.split('metric ')[1].split(' ')[0] if static is defined and 'metric' in static }}",
                            "route_map": "{{ static.split('route-map ')[1].split(' ')[0] if static is defined and 'route-map' in static }}",
                        },
                        "vrf": {
                            "name": "{{ vrf.split('vrf ')[1].split(' ')[0] if vrf is defined and 'vrf' in vrf and 'global' not in vrf }}",
                            "global": "{{ True if vrf is defined and 'vrf' in vrf and 'global' in vrf }}",
                        },
                    }
                ]
            },
        },
        {
            "name": "route_server_context",
            "getval": re.compile(
                r"""\s*(?P<route_server_context>route-server-context\s\S+)""",
                re.VERBOSE,
            ),
            "compval": "route_server_context",
            "setval": "",
            "result": {
                "route_server_context": "{{ route_server_context.split('route-server-context ')[1] if route_server_context is defined }}"
            },
        },
        {
            "name": "synchronization",
            "getval": re.compile(
                r"""\s*(?P<synchronization>synchronization)""", re.VERBOSE
            ),
            "compval": "synchronization",
            "setval": "synchronization",
            "result": {
                "synchronization": "{{ Trues if synchronization is defined }}"
            },
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""\s*(?P<table_map>route-server-context\s\S+)""", re.VERBOSE
            ),
            "compval": "table_map",
            "setval": "",
            "result": {
                "table_map": "{{ table_map.split('route-server-context ')[1] if table_map is defined }}"
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""\s*(?P<timers>timers\sbgp\s\d+\s\d+\s\d+)""", re.VERBOSE
            ),
            "compval": "timers",
            "setval": _tmplt_bgp_timers,
            "result": {
                "timers": {
                    "keepalive": "{{ timers.split(' ')[2] if timers is defined }}",
                    "holdtime": "{{ timers.split(' ')[3] if timers is defined }}",
                    "min_holdtime": "{{ timers.split(' ')[4] if timers is defined and timers.split(' ')|length > 4 }}",
                }
            },
        },
    ]
