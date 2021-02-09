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
            commands.append("{0} aigp".format(cmd))
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
    if 'bgp' in config_data:
        cmd = []
        command = "bgp"
        if config_data["bgp"].get("advertise_best_external"):
            cmd.append("bgp advertise-best-external")
        if config_data["bgp"].get("aggregate_timer"):
            cmd.append("bgp aggregate-timer {aggregate_timer}".format(**config_data["bgp"]))
        if config_data["bgp"].get("always_compare_med"):
            cmd.append("bgp always-compare-med")
        if config_data["bgp"].get("asnotation"):
            cmd.append("bgp asnotation dot")
        if "client_to_client" in config_data["bgp"]:
            command = "bgp client-to-client reflection"
            if "all" in config_data["bgp"]["client_to_client"]:
                command += " all"
            elif "intra_cluster" in config_data["bgp"]["client_to_client"]:
                command += " intra-cluster cluster-id {intra_cluster}".format(**config_data["bgp"]["client_to_client"])
            cmd.append(command)
        if config_data["bgp"].get("cluster_id"):
            cmd.append("bgp cluster-id {cluster_id}".format(**config_data["bgp"]))
        if "confederation" in config_data["bgp"]:
            command = "bgp confederation"
            if "identifier" in config_data["bgp"]["confederation"]:
                command += "bgp identifier {identifier}".format(**config_data["bgp"]["confederation"])
            elif "peers" in config_data["bgp"]["confederation"]:
                command += "bgp peers {peers}".format(**config_data["bgp"]["confederation"])
            cmd.append(command)
        if "consistency_checker" in config_data["bgp"]:
            command = "bgp consistency-checker"
            if "auto_repair" in config_data["bgp"]["consistency_checker"]:
                command += " auto-repair"
                if "interval" in config_data["bgp"]["consistency_checker"]["auto_repair"]:
                    command += " interval {interval}".format(**config_data["bgp"]["consistency_checker"]["auto_repair"])
            elif "error-message" in config_data["bgp"]["consistency_checker"]:
                command += " error-message"
                if "interval" in config_data["bgp"]["consistency_checker"]["error_message"]:
                    command += " interval {interval}".format(**config_data["bgp"]["consistency_checker"]["error_message"])
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
                command += " restart-time {restart_time}".format(**config_data["bgp"]["graceful_restart"])
            elif config_data["bgp"]["graceful_restart"].get("stalepath_time"):
                command += " stalepath-time {stalepath_time}".format(**config_data["bgp"]["graceful_restart"])
            cmd.append(command)
        if "inject_map" in config_data["bgp"]:
            command = "bgp inject-map {name} exist-map {exist_map_name}".format(**config_data["bgp"]["inject_map"])
            if config_data["bgp"]["inject_map"].get("copy_attributes"):
                command += "copy-attributes"
            cmd.append(command)
        if "listen" in config_data["bgp"]:
            command = "bgp listen"
            if "limit" in config_data["bgp"]["listen"]:
                command += " limit {limit}".format(**config_data["bgp"]["listen"])
            elif "range" in config_data["bgp"]["listen"]:
                if config_data["bgp"]["listen"]["range"].get("ipv4_with_subnet"):
                    command += " range {ipv4_with_subnet}".format(**config_data["bgp"]["listen"]["range"])
                elif config_data["bgp"]["listen"]["range"].get("ipv6_with_subnet"):
                    command += " range {ipv6_with_subnet}".format(**config_data["bgp"]["listen"]["range"])
                if config_data["bgp"]["listen"]["range"].get("peer_group"):
                    command += " peer-group {peer_group}".format(**config_data["bgp"]["listen"]["range"])
            cmd.append(command)
        if config_data["bgp"].get("log_neighbor_changes"):
            cmd.append("bgp log-neighbor-changes")
        if config_data["bgp"].get("maxas_limit"):
            cmd.append("bgp maxas-limit {maxas_limit}".format(**config_data["bgp"]))
        if config_data["bgp"].get("maxextcommunity_limit"):
            cmd.append("bgp maxextcommunity-limit {maxextcommunity_limit}".format(**config_data["bgp"]))
        if "nexthop" in config_data["bgp"]:
            command = "bgp nexthop"
            if "route_map" in config_data["bgp"]["nexthop"]:
                command += " route-map {route_map}".format(**config_data["bgp"]["nexthop"])
            elif "trigger" in config_data["bgp"]["nexthop"]:
                if config_data["bgp"]["nexthop"]["trigger"].get("delay"):
                    command += " trigger delay {delay}".format(**config_data["bgp"]["nexthop"]["trigger"])
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
                command += " max-eor-time {max_eor_time}".format(**config_data["bgp"]["refresh"])
            elif "stalepath_time" in config_data["bgp"]["refresh"]:
                command += " stalepath-time {stalepath_time}".format(**config_data["bgp"]["refresh"])
            cmd.append(command)
        if config_data["bgp"].get("regexp"):
            cmd.append("bgp regexp deterministic")
        if config_data["bgp"].get("route_map"):
            cmd.append("bgp route-map priority")
        if "router_id" in config_data["bgp"]:
            command = "bgp router-id"
            if "address" in config_data["bgp"]["router_id"]:
                command += " {address}".format(**config_data["bgp"]["router_id"])
            elif "interface" in config_data["bgp"]["router_id"]:
                command += " interface {interface}".format(**config_data["bgp"]["router_id"])
            elif "vrf" in config_data["bgp"]["router_id"]:
                command += " vrf auto-assign"
            cmd.append(command)
        if config_data["bgp"].get("scan_time"):
            cmd.append("bgp scan-time {scan_time}".format(**config_data["bgp"]))
        if "slow_peer" in config_data["bgp"]:
            command = "bgp slow-peer"
            if "detection" in config_data["bgp"]["slow_peer"]:
                command += " detection"
                if "threshold" in config_data["bgp"]["slow_peer"]["detection"]:
                    command += " threshold {threshold}".format(**config_data["bgp"]["slow_peer"]["detection"])
            elif "split_update_group" in config_data["bgp"]["slow_peer"]:
                if "dynamic" in config_data["bgp"]["slow_peer"]["split_update_group"]:
                    command += " dynamic"
                    if "permanent" in config_data["bgp"]["slow_peer"]["split_update_group"]:
                        command += " permanent {permanent}".format(**config_data["bgp"]["slow_peer"]["split_update_group"])
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
            cmd.append("bgp update-delay {update_delay}".format(**config_data["bgp"]))
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
            command = "bgp dampening {penalty_half_time}".format(**config_data["bgp"]["dampening"])
            if config_data["bgp"]["dampening"].get("reuse_route_val"):
                command += " {reuse_route_val}".format(**config_data["bgp"]["dampening"])
            if config_data["bgp"]["dampening"].get("suppress_route_val"):
                command += " {suppress_route_val}".format(**config_data["bgp"]["dampening"])
        elif config_data["bgp"]["dampening"].get("route_map"):
            command = "bgp dampening {route_map}".format(**config_data["bgp"]["dampening"])
        return command

def _tmplt_bgp_graceful_shutdown(config_data):
    if "bgp" in config_data and "graceful_shutdown" in config_data["bgp"]:
        command = "bgp graceful-shutdown all"
        if config_data["bgp"]["graceful_shutdown"].get("neighbors"):
            command += " neighbors"
            if config_data["bgp"]["graceful_shutdown"]["neighbors"].get("activate"):
                command += " activate"
            elif config_data["bgp"]["graceful_shutdown"]["neighbors"].get("time"):
                command += " {time}".format(**config_data["bgp"]["graceful_shutdown"]["neighbors"])
        elif config_data["bgp"]["graceful_shutdown"].get("vrfs"):
            command += " vrfs"
            if config_data["bgp"]["graceful_shutdown"]["vrfs"].get("activate"):
                command += " activate"
            elif config_data["bgp"]["graceful_shutdown"]["neighbors"].get("time"):
                command += " {time}".format(**config_data["bgp"]["graceful_shutdown"]["vrfs"])
        if config_data["bgp"]["graceful_shutdown"].get("community"):
            command += " community {community}".format(**config_data["bgp"]["graceful_shutdown"])
        if config_data["bgp"]["graceful_shutdown"].get("local_preference"):
            command += " local-preference {local_preference}".format(**config_data["bgp"]["graceful_shutdown"])
        return command

def _tmplt_bgp_nopeerup_delay(config_data):
    if "bgp" in config_data and "nopeerup_delay" in config_data["bgp"]:
        print(config_data)
        commands = []
        val = config_data["bgp"]["nopeerup_delay"]
        cmd = "bgp nopeerup-delay"
        if val.get("cold_boot"):
            commands.append(
                "{0} cold-boot {cold_boot}".format(
                    cmd, **val
                )
            )
        elif val.get("post_boot"):
            commands.append(
                "{0} post-boot {post_boot}".format(
                    cmd, **val
                )
            )
        elif val.get("nsf_switchover"):
            commands.append(
                "{0} nsf-switchover {nsf_switchover}".format(
                    cmd, **val
                )
            )
        elif val.get("user_initiated"):
            commands.append(
                "{0} user-initiated {user_initiated}".format(
                    cmd, **val
                )
            )
        print(commands)
        return commands

def _tmplt_neighbor(config_data):
    if "neighbor" in config_data:
        commands = []
        cmd = "neighbor"
        #for each in list(config_data["neighbor"]):
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
        if config_data["neighbor"].get('advertise_map'):
            self_cmd = "{0} advertise-map {name}".format(cmd, **config_data["neighbor"]["advertise_map"])
            if 'exist_map' in config_data["neighbor"]["advertise_map"]:
                self_cmd += " exist-map {exist_map}".format(**config_data["neighbor"]["advertise_map"])
            elif 'non_exist_map' in config_data["neighbor"]["advertise_map"]:
                self_cmd += " exist-map {non_exist_map}".format(**config_data["neighbor"]["advertise_map"])
            commands.append(self_cmd)
        if config_data["neighbor"].get('advertisement_interval'):
            commands.append(
                "{0} advertisement-interval {advertisement_interval}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get('aigp'):
            self_cmd = "{0} aigp".format(cmd)
            if config_data["neighbor"]["aigp"].get('send'):
                self_cmd += " send"
                if config_data["neighbor"]["aigp"]['send'].get('cost_community'):
                    self_cmd += " cost-community {id}".format(**config_data["neighbor"]["aigp"]["send"]["cost_community"])
                    if config_data["neighbor"]["aigp"]["send"]["cost_community"].get("poi"):
                        self_cmd += " poi"
                        if config_data["neighbor"]["aigp"]["send"]["cost_community"]["poi"].get("igp_cost"):
                            self_cmd += " igp-cost"
                        if config_data["neighbor"]["aigp"]["send"]["cost_community"]["poi"].get("pre_bestpath"):
                            self_cmd += " pre-bestpath"
                        if config_data["neighbor"]["aigp"]["send"]["cost_community"]["poi"].get("transitive"):
                            self_cmd += " transitive"
                if config_data["neighbor"]["aigp"]['send'].get('med'):
                    self_cmd += " med"
            commands.append(self_cmd)
        if config_data["neighbor"].get('allow_policy'):
            commands.append("{0} allow-policy".format(cmd))
        if config_data["neighbor"].get('allowas_in'):
            commands.append("{0} allowas-in {allowas_in}".format(cmd, **config_data["neighbor"]))
        if config_data["neighbor"].get('as_override'):
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
        if config_data["neighbor"].get('cluster_id'):
            commands.append("{0} cluster-id {cluster_id}".format(cmd, **config_data["neighbor"]))
        if "default_originate" in config_data["neighbor"]:
            self_cmd = "{0} default-originate".format(cmd)
            if config_data["neighbor"]["default_originate"].get("route_map"):
                self_cmd += " route-map {route_map}".format(**config_data["neighbor"]["default_originate"])
            commands.append(self_cmd)
        if "description" in config_data["neighbor"]:
            commands.append(
                "{0} description {description}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if config_data["neighbor"].get('disable_connected_check'):
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
        if config_data["neighbor"].get('dmzlink_bw'):
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
                if config_data["neighbor"]["fall_over"]["bfd"].get("multi_hop"):
                    self_cmd += " multi-hop"
                elif config_data["neighbor"]["fall_over"]["bfd"].get("single_hop"):
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
                cmd,
                **config_data["neighbor"]
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
                self_cmd += " restart {restart}".format(**config_data["neighbor"]["maximum_prefix"])
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
                if "type" in config_data["neighbor"]["path_attribute"]["discard"]:
                    self_cmd += " {type}".format(**config_data["neighbor"]["path_attribute"]["discard"])
                elif "range" in config_data["neighbor"]["path_attribute"]["discard"]:
                    self_cmd += " range"
                    if "start" in config_data["neighbor"]["path_attribute"]["discard"]["range"]:
                        self_cmd += " {start}".format(**config_data["neighbor"]["path_attribute"]["discard"]["range"])
                    elif "end" in config_data["neighbor"]["path_attribute"]["discard"]["range"]:
                        self_cmd += " {start}".format(**config_data["neighbor"]["path_attribute"]["discard"]["range"])
                if "in" in config_data["neighbor"]["path_attribute"]["discard"]:
                    self_cmd += " in"
            if "treat_as_withdraw" in config_data["neighbor"]["path_attribute"]:
                self_cmd += " treat-as-withdraw"
                if "type" in config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]:
                    self_cmd += " {type}".format(**config_data["neighbor"]["path_attribute"]["treat_as_withdraw"])
                elif "range" in config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]:
                    self_cmd += " range"
                    if "start" in config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]["range"]:
                        self_cmd += " {start}".format(**config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]["range"])
                    elif "end" in config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]["range"]:
                        self_cmd += " {start}".format(**config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]["range"])
                if "in" in config_data["neighbor"]["path_attribute"]["treat_as_withdraw"]:
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
            elif config_data["neighbor"]["remove_private_as"].get("replace_as"):
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
            self_cmd = "{0} timers {interval} {holdtime}".format(cmd, **config_data["neighbor"]["timers"])
            if "min_holdtime" in config_data["neighbor"]["timers"]:
                self_cmd += " {min_holdtime}".format(
                    **config_data["neighbor"]["timers"]
                )
            commands.append(self_cmd)
        if "translate_update" in config_data["neighbor"]:
            self_cmd = "{0} translate-update".format(cmd)
            if config_data["neighbor"]["send_community"].get("nlri"):
                self_cmd += " nlri"
                if config_data["neighbor"]['nlri'].get('multicast'):
                    self_cmd += "multicast"
                if config_data["neighbor"]['nlri'].get('unicast'):
                    self_cmd += "unicast"
            commands.append(self_cmd)
        if "transport" in config_data["neighbor"]:
            self_cmd = "{0} transport".format(cmd)
            if config_data["neighbor"]["transport"].get("connection_mode"):
                self_cmd += " connection-mode"
                if config_data["neighbor"]['transport']['connection_mode'].get('active'):
                    self_cmd += " active"
                elif config_data["neighbor"]['transport']['connection_mode'].get('passive'):
                    self_cmd += " passive"
            elif config_data["neighbor"]["transport"].get("multi_session"):
                self_cmd += " multi-session"
            elif config_data["neighbor"]["transport"].get("path_mtu_discovery"):
                self_cmd += " path-mtu-discovery"
                if config_data["neighbor"]['transport']['path_mtu_discovery'].get('disable'):
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
                "{0} version {version}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "weight" in config_data["neighbor"]:
            commands.append(
                "{0} weight {weight}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        return commands

def _tmplt_redistribute(config_data):
    if 'redistribute' in config_data:
        def common_config(command, param):
            if config_data['redistribute'][param].get('metric'):
                command += " metric {metric}".format(**config_data['redistribute'][param])
            if config_data['redistribute'][param].get('route_map'):
                command += " route-map {route_map}".format(**config_data['redistribute'][param])
            return command

        command = "redistribute"
        if config_data['redistribute'].get('application'):
            command += " application {name}".format(**config_data['redistribute']['application'])
            command = common_config(command, 'application')
        elif config_data['redistribute'].get('bgp'):
            command += " bgp {as_number}".format(**config_data['redistribute']['bgp'])
            command = common_config(command, 'bgp')
        elif config_data['redistribute'].get('connected'):
            command += " connected"
            command = common_config(command, 'connected')
        elif config_data['redistribute'].get('eigrp'):
            command += " eigrp {as_number}".format(**config_data['redistribute']['eigrp'])
            command = common_config(command, 'eigrp')
        elif config_data['redistribute'].get('isis'):
            command += " isis {area_tag}".format(**config_data['redistribute']['isis'])
            if config_data['redistribute']['isis'].get('clns'):
                command += " clns"
            elif config_data['redistribute']['isis'].get('ip'):
                command += " ip"
            command = common_config(command, 'isis')
        elif config_data['redistribute'].get('iso_igrp'):
            command += " iso-igrp {area_tag}".format(**config_data['redistribute']['iso_igrp'])
            if config_data['redistribute']['iso_igrp'].get('route_map'):
                command += " route-map {route_map}".format(**config_data['redistribute']['iso_igrp'])
        elif config_data['redistribute'].get('lisp'):
            command += " lisp"
            command = common_config(command, 'lisp')
        elif config_data['redistribute'].get('mobile'):
            command += " mobile"
            command = common_config(command, 'mobile')
        elif config_data['redistribute'].get('odr'):
            command += " odr"
            command = common_config(command, 'odr')
        elif config_data['redistribute'].get('rip'):
            command += " rip"
            command = common_config(command, 'rip')
        elif config_data['redistribute'].get('ospf'):
            command += " ospf {process_id}".format(**config_data['redistribute']['ospf'])
            if config_data['redistribute']['ospf'].get("match"):
                command += " match"
                if config_data['redistribute']['ospf']['match'].get('external'):
                    command += " external"
                if config_data['redistribute']['ospf']['match'].get('internal'):
                    command += " internal"
                if config_data['redistribute']['ospf']['match'].get('nssa_external'):
                    command += " nssa-external"
                if config_data['redistribute']['ospf']['match'].get('type_1'):
                    command += " 1"
                elif config_data['redistribute']['ospf']['match'].get('type_2'):
                    command += " 2"
            if config_data['redistribute']['ospf'].get("vrf"):
                command += " vrf"
            command = common_config(command, 'ospf')
        elif config_data['redistribute'].get('ospfv3'):
            command += " ospfv3 {process_id}".format(**config_data['redistribute']['ospfv3'])
            if config_data['redistribute']['ospfv3'].get("match"):
                command += " match"
                if config_data['redistribute']['ospfv3']['match'].get('external'):
                    command += " external"
                if config_data['redistribute']['ospfv3']['match'].get('internal'):
                    command += " internal"
                if config_data['redistribute']['ospfv3']['match'].get('nssa_external'):
                    command += " nssa-external"
                if config_data['redistribute']['ospfv3']['match'].get('type_1'):
                    command += " 1"
                elif config_data['redistribute']['ospfv3']['match'].get('type_2'):
                    command += " 2"
            command = common_config(command, 'ospf')
        elif config_data['redistribute'].get('static'):
            command += " static"
            command = common_config(command, 'static')
        elif config_data['redistribute'].get('vrf'):
            if config_data['redistribute']['vrf'].get('name'):
                command += " vrf {name}".format(**config_data['redistribute']['vrf'])
            elif config_data['redistribute']['vrf'].get('global'):
                command += " vrf global"

        return command

def _tmplt_bgp_timers(config_data):
    if 'timers' in config_data:
        command = "timers bgp"
        if config_data['timers'].get('keepalive'):
            command += ' {keepalive}'.format(**config_data['timers'])
        if config_data['timers'].get('holdtime'):
            command += ' {holdtime}'.format(**config_data['timers'])
        if config_data['timers'].get('min_holdtime'):
            command += ' {min_holdtime}'.format(**config_data['timers'])
    return command


class Bgp_AddressFamilyTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Bgp_AddressFamilyTemplate, self).__init__(lines=lines, tmplt=self)

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
            "name": "afi",
            "getval": re.compile(
                r"""\s*address-family*
                    \s*(?P<afi>ipv4|ipv6|l2vpn|nsap|rtfilter|vpnv4|vpnv6)*
                    \s*(?P<af_modifier>flowspec|mdt|multicast|mvpn|unicast|evpn|vpls)*
                    \s*(?P<vrf>vrf\s\S+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "afi",
            "setval": "address-family {{ afi }} {{ af_modifier }} {{ vrf vrf.split('vrf ')[1] }}",
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "afi": "{{ afi }}",
                        "af_modifier": "{{ af_modifier }}",
                        "vrf": "{{ vrf.split('vrf ')[1] if vrf is defined }}"
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "aggregate_address",
            "getval": re.compile(
                r"""\s*aggregate-address*
                    \s*(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3}\s(?:[0-9]{1,3}\.){3}[0-9]{1,3})*
                    \s*(?P<advertise_map>advertise-map\s\S+)*
                    \s*(?P<as_confed_set>as-confed-set)*
                    \s*(?P<as_set>as-set)*
                    \s*(?P<attribute_map>attribute-map\s\S+)*
                    \s*(?P<route_map>route-map\s\S+)*
                    \s*(?P<summary_only>summary-only)*
                    \s*(?P<suppress_map>suppress-map\s\S+)*
                    $""",
                re.VERBOSE,
            ),
            "compval": "afi",
            "setval": "address-family {{ afi }} {{ af_modifier }} {{ vrf vrf.split('vrf ')[1] }}",
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "aggregate_address": {
                            "address": "{{ address.split(' ')[0] }}",
                            "netmask": "{{ address.split(' ')[1] }}",
                            "advertise_map": "{{ advertise_map.split('advertise-map ')[1] if advertise_map is defined }}",
                            "as_confed_set": "{{ True if as_confed_set is defined }}",
                            "as_set": "{{ True if as_set is defined }}",
                            "attribute_map": "{{ attribute_map.split('attribute-map ')[1] if attribute_map is defined }}",
                            "summary_only": "{{ True if summary_only is defined }}",
                            "suppress_map": "{{ suppress_map.split('suppress-map ')[1] if suppress_map is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.additional_paths",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*additional-paths*
                    \s*(?P<receive>receive)*
                    \s*(?P<select>select)*
                    \s*(?P<select_all>all)*
                    \s*(?P<select_backup>backup)*
                    \s*(?P<select_best>best\s\d)*
                    \s*(?P<select_group_best>group-best)*
                    \s*(?P<send>send)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_additional_paths,
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "additional_paths": {
                                "receive": "{{ True if receive is defined }}",
                                "select": {
                                    "all": "{{ True if select_all is defined }}",
                                    "backup": "{{ True if select_backup is defined }}",
                                    "best": "{{ select_best.split('best ')[1] if select_best is defined }}",
                                    "group_best": "{{ True if select_group_best is defined }}",
                                },
                                "send": "{{ True if send is defined }}",
                            }
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.config",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*(?P<aggregate_timer>aggregate-timer\s\d+)*
                    \s*(?P<dmzlink_bw>dmzlink-bw)*
                    \s*(?P<nexthop>nexthop\s(route-map\s\S+|trigger\s(delay\s\d+|enable)))*
                    \s*(?P<redistribute_internal>redistribute-internal)*
                    \s*(?P<route_map>route-map\spriority)*
                    \s*(?P<scan_time>scan-time\s\d+)*
                    \s*(?P<slow_peer>slow-peer((\sdetection\sthreshold\d+|\sdetection)|(\ssplit-update-group\sdynamic\spermanent|\ssplit-update-group\sdynamic)))*
                    \s*(?P<update_group>update-group\ssplit\sas-override)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_config,
            "compval": "bgp",
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "aggregate_timer": "{{ aggregate_timer.split('aggregate-timer ')[1] if aggregate_timer is defined }}",
                            "dmzlink_bw": "{{ True if dmzlink_bw is defined }}",
                            "nexthop": {
                                "route_map": "{{ nexthop.split('route-map ')[1] if nexthop is defined and 'route-map' in nexthop }}",
                                "trigger": {
                                    "delay": "{{ nexthop.split('delay ')[1] if nexthop is defined and 'delay' in nexthop }}",
                                    "enable": "{{ True if nexthop is defined and 'enable' in nexthop }}",
                                },
                            },
                            "redistribute_internal": "{{ True if redistribute_internal is defined }}",
                            "route_map": "{{ True if route_map is defined }}",
                            "scan_time": "{{ scan_time.split('scan-time ')[1] if scan_time is defined }}",
                            "slow_peer": {
                                "detection": {
                                    "set": "{{ True if slow_peer is defined and 'detection' in slow_peer and 'threshold' not in slow_peer }}",
                                    "threshold": "{{ slow_peer.split('threshold ')[1] if slow_peer is defined and 'threshold' in slow_peer }}",
                                },
                                "split_update_group": {
                                    "dynamic": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and 'dynamic' in slow_peer }}",
                                    "permanent": "{{ True if slow_peer is defined and 'split-update-group' in slow_peer and 'permanent' in slow_peer }}",
                                },
                            },
                            "soft_reconfig_backup": "{{ True if soft_reconfig_backup is defined }}",
                            "update_group": "{{ True if update_group is defined }}",
                        },
                    },
                },
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
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "bgp": {
                            "dampening": {
                                "penalty_half_time": "{{ penalty_half_time if penalty_half_time is defined }}",
                                "reuse_route_val": "{{ reuse_route_val if penalty_half_time is defined }}",
                                "suppress_route_val": "{{ suppress_route_val if penalty_half_time is defined }}",
                                "max_suppress": "{{ max_suppress if penalty_half_time is defined }}",
                                "route_map": "{{ dampening.split('route-map ')[1] if dampening is defined and 'route-map' in dampening }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "default",
            "getval": re.compile(
                r"""\s*(?P<default>default)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "default",
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "default": "{{ True if default is defined }}"
                    },
                },
            },
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""\s*(?P<default_metric>default-metric\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "default-metric {{ default_metric }}",
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "default_metric": "{{ default_metric.split('default-metric ')[1] if default_metric is defined }}"
                    },
                },
            },
        },
        {
            "name": "distance",
            "getval": re.compile(
                r"""\s*distance\sbgp(?P<distance>\s\d+\s\d+\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_dampening,
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "distance": {
                            "external": "{{ distance.split(' ')[0] }}",
                            "internal": "{{ distance.split(' ')[1] }}",
                            "local": "{{ distance.split(' ')[2] }}",
                        }
                    },
                },
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
                    \s*(?P<capability>capability\s(both|receive|send))*
                    \s*(?P<default_originate>default-originate\sroute-map|default-originate)*
                    \s*(?P<distribute_list>distribute-list\s\d+\s(in|out))*
                    \s*(?P<dmzlink_bw>dmzlink-bw)*
                    \s*(?P<filter_list>filter-list\s\d+\s(in|out))*
                    \s*(?P<inherit>inherit\speer-session\s\S+)*
                    \s*(?P<maximum_prefix>maximum-prefix\s(\d+\s\d+\s(restart\s\d+|warning-only)|\d+\s(restart\s\d+|warning-only)))*
                    \s*(?P<next_hop_self>next-hop-self\sall|next-hop-self)*
                    \s*(?P<next_hop_unchanged>next-hop-unchanged\sallpaths|next-hop-unchanged)*
                    \s*(?P<prefix_list>prefix-list\s\S+\s(in|out))*
                    \s*(?P<remove_private_as>remove-private-as\sall\sreplace-as|remove-private-as\sall|remove-private-as)*
                    \s*(?P<route_map>route-map\s\S+\s(in|out))*
                    \s*(?P<route_reflector_client>route-reflector-client)*
                    \s*(?P<route_server_client>route-server-client\scontext\s\S+|route-server-client)*
                    \s*(?P<send_community>send-community\s(both|extended|standard)|send-community)*
                    \s*(?P<soft_reconfiguration>soft-reconfiguration\sinbound)*
                    \s*(?P<slow_peer>slow-peer\s(detection.*|split-update-group.*))*
                    \s*(?P<unsuppress_map>unsuppress-map\s\S+)*
                    \s*(?P<weight>weight\s\d+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_neighbor,
            "compval": "neighbor",
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
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
                                        "best": "{{ advertise.split('best ')[1].split(' ')[0] if advertise is defined and 'additional-paths' in advertise and 'best' in advertise }}",
                                        "group_best": "{{ True if advertise is defined and 'additional-paths' in advertise and 'group-best' in advertise }}",
                                    },
                                    "best_external": "{{ True if advertise is defined and 'best-external' in advertise }}",
                                    "diverse_path": {
                                        "backup": "{{ True if advertise is defined and 'diverse-path' in advertise and 'backup' in advertise }}",
                                        "mpath": "{{ True if advertise is defined and 'diverse-path' in advertise and 'mpath' in advertise }}"
                                    }
                                },
                                "advertisement_interval": "{{ advertisement_interval.split('advertisement-interval ')[1] if advertisement_interval is defined }}",
                                "aigp": {
                                    "enable": "{{ True if aigp is defined and aigp.split(' ')|length == 1 }}",
                                    "send": {
                                        "cost_community": {
                                            "id": "{{ aigp.split('send cost-community')[1].split(' ')[0] if aigp is defined and 'send cost-community' in aigp }}",
                                            "poi": {
                                                "igp_cost": "{{ True if aigp is defined and 'poi igp-cost' in aigp }}",
                                                "pre_bestpath": "{{ True if aigp is defined and 'poi pre-bestpath' in aigp }}",
                                                "transitive": "{{ True if aigp is defined and 'transitive' in aigp }}",
                                            }
                                        },
                                        "med": "{{ True if aigp is defined and 'send med' in aigp }}"
                                    },
                                },
                                "allow_policy": "{{ True if allow_policy is defined }}",
                                "allowas_in": "{{ allowas_in.split('allowas-in ')[1] if allowas_in is defined }}",
                                "as_override": "{{ True if as_override is defined }}",
                                "capability": {
                                    "both": "{{ True if capability is defined and 'both' in capability }}",
                                    "receive": "{{ True if capability is defined and 'receive' in capability }}",
                                    "send": "{{ True if capability is defined and 'send' in capability }}",
                                },
                                "default_originate": {
                                    "set": "{{ True if default_originate is defined and default_originate.split(' ')|length == 1 }}",
                                    "route_map": "{{ default_originate.split(' ')[1] if default_originate is defined and default_originate.split(' ')|length > 1 }}"
                                },
                                "distribute_list": {
                                    "acl": "{{ distribute_list.split(' ')[1] if distribute_list is defined }}",
                                    "in": "{{ True if distribute_list is defined and 'in' in distribute_list }}",
                                    "out": "{{ True if distribute_list is defined and 'out' in distribute_list }}",
                                },
                                "dmzlink_bw": "{{ True if dmzlink_bw is defined }}",
                                "filter_list": {
                                    "acl": "{{ filter_list.split(' ')[1] if filter_list is defined }}",
                                    "in": "{{ True if filter_list is defined and 'in' in filter_list }}",
                                    "out": "{{ True if filter_list is defined and 'out' in filter_list }}",
                                },
                                "inherit": "{{ inherit.split('inherit peer-session ')[1] if inherit is defined }}",
                                "maximum_prefix": {
                                    "max_no": "{{ maximum_prefix.split(' ')[1] if maximum_prefix is defined }}",
                                    "threshold_val": "{{ maximum_prefix.split(' ')[2] if maximum_prefix is defined and maximum_prefix.split(' ')|length > 3 and maximum_prefix.split(' ')[1] != 'restart' }}",
                                    "restart": "{{ maximum_prefix.split('restart ')[1] if maximum_prefix is defined and 'restart' in maximum_prefix }}",
                                    "warning_only": "{{ True if maximum_prefix is defined and 'warning-only' in maximum_prefix }}"
                                },
                                "next_hop_self": {
                                    "set": "{{ True if next_hop_self is defined and next_hop_self.split(' ')|length == 1 }}",
                                    "all": "{{ True if next_hop_self is defined and next_hop_self.split(' ')|length > 1 }}",
                                },
                                "next_hop_unchanged": {
                                    "set": "{{ True if next_hop_unchanged is defined and next_hop_unchanged.split(' ')|length == 1 }}",
                                    "allpaths": "{{ True if next_hop_unchanged is defined and next_hop_unchanged.split(' ')|length > 1 }}",
                                },
                                "prefix_list": {
                                    "name": "{{ prefix_list.split(' ')[1] if prefix_list is defined }}",
                                    "in": "{{ True if prefix_list is defined and 'in' in prefix_list }}",
                                    "out": "{{ True if prefix_list is defined and 'out' in prefix_list }}",
                                },
                                "password": "{{ password.split(' ')[1] if password is defined }}",
                                "path_attribute": {
                                    "discard": {
                                        "type": "{% if path_attribute is defined and 'discard range' in path_attribute and path_attribute.split(' ')|length <= 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                        "range": {
                                            "start": "{% if path_attribute is defined and 'discard range' in path_attribute and path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                            "end": "{% if path_attribute is defined and 'discard range' in path_attribute and path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[4] }}{% endif %}",
                                        },
                                        "in": "{% if path_attribute is defined and 'discard range' in path_attribute and 'in' in path_attribute %}{{ True }}{% endif %}"
                                    },
                                    "treat_as_withdraw": {
                                        "type": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and path_attribute.split(' ')|length <= 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                        "range": {
                                            "start": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[3] }}{% endif %}",
                                            "end": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and path_attribute.split(' ')|length > 5 %}{{ path_attribute.split(' ')[4] }}{% endif %}",
                                        },
                                        "in": "{% if path_attribute is defined and 'discard treat-as-withdraw' in path_attribute and 'in' in path_attribute %}{{ True }}{% endif %}"
                                    },
                                },
                                "remove_private_as": {
                                    "set": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length == 1 }}",
                                    "all": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length > 1 and 'all' in remove_private_as }}",
                                    "replace_as": "{{ True if remove_private_as is defined and remove_private_as.split(' ')|length > 1 and 'replace-as' in remove_private_as }}",
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
                                "unsuppress_map": "{{ unsuppress_map.split('unsuppress-map ')[1] if unsuppress_map is defined }}",
                                "weight": "{{ weight.split('weight ')[1] if weight is defined }}",
                            }
                        ]
                    },
                },
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""\s*network*
                    \s*(?P<address>(?:[0-9]{1,3}\.){3}[0-9]{1,3})*
                    \s*(?P<mask>mask\s(?:[0-9]{1,3}\.){3}[0-9]{1,3})*
                    \s*(?P<backdoor>backdoor)*
                    \s*(?P<route_map>route-map\s\S+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_dampening,
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "network": [{
                            "address": "{{ address if address is defined }}",
                            "mask": "{{ mask.split('mask ')[1] if mask is defined }}",
                            "backdoor": "{{ True if backdoor is defined }}",
                            "route_map": "{{ route_map.split('route-map ')[1] if route_map is defined }}",
                        }],
                    },
                },
            },
        },
        {
            "name": "snmp",
            "getval": re.compile(
                r"""\s*snmp*
                    \s*(?P<context>context\s\S+)*
                    \s*(?P<community>community\s\S+)*
                    \s*(?P<user>user\s\S+)*
                    \s*(?P<ro>ro|RO)*
                    \s*(?P<rw>rw|RW)*
                    \s*(?P<credential>credential\s\S+)*
                    \s*(?P<encrypted>encrypted)*
                    \s*(?P<auth>auth)*
                    \s*(?P<md5>md5\s\S+)*
                    \s*(?P<sha>sha\s\S+)*
                    \s*(?P<priv>priv\s(3des\s\S+|aes\s128\s\S+|aes\s192\s\S+|aes\s256\s\S+|des\s\S+))*
                    \s*(?P<access>access\s(ipv6\s\S+|\S+))*
                    \s*(?P<acl>ipv6\s\S+|\S+)*
                    $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_bgp_dampening,
            "result": {
                "address_family": {
                    "{{ afi + '_' + af_modifier|d() + '_' + vrf|d() }}": {
                        "snmp": {
                            "context": "{{ context.split('context ')[1] if context is defined }}",
                            "community": {
                                "snmp_community": "{{ community.split('community ')[1] if community is defined }}",
                                "acl": "{{ acl if acl is defined and 'ipv6' not in acl }}",
                                "ro": "{{ True if ro is defined }}",
                                "rw": "{{ True if ro is defined }}",
                                "ipv6": "{{ acl.split('ipv6 ')[1] if acl is defined and 'ipv6' in acl }}",
                            },
                            "user": {
                                "name": "{{ user.split('user ')[1] if user is defined }}",
                                "credential": "{{ credential.split('credential ')[1] if credential is defined }}",
                                "encrypted": "{{ True if encrypted is defined }}",
                                "access": {
                                    "acl": "{{ access.split('access ')[1] if access is defined and 'ipv6' not in access }}",
                                    "ipv6": "{{ access.split('access ipv6 ')[1] if access is defined and 'ipv6' in access }}",
                                },
                                "auth": {
                                    "md5": "{{ md5.split('md5 ')[1] if md5 is defined }}",
                                    "sha": "{{ sha.split('sha ')[1] if sha is defined }}",
                                    "access": {
                                        "acl": "{{ access.split('access ')[1] if md5 is defined or sha is defined and access is defined and 'ipv6' not in access }}",
                                        "ipv6": "{{ access.split('access ipv6 ')[1] if md5 is defined or sha is defined and access is defined and 'ipv6' in access }}",
                                    },
                                    "priv": {
                                        "3des": "{{ priv.split('priv 3des ')[1] if priv is defined and '3des' in priv }}",
                                        "aes": {
                                            "128": "{{ priv.split('priv aes 128 ')[1] if priv is defined and 'aes 128' in priv }}",
                                            "192": "{{ priv.split('priv aes 192 ')[1] if priv is defined and 'aes 192' in priv }}",
                                            "256": "{{ priv.split('priv aes 256 ')[1] if priv is defined and 'aes 256' in priv }}",
                                        },
                                        "des": "{{ priv.split('priv des ')[1] if priv is defined and 'des' in priv }}"
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    ]
