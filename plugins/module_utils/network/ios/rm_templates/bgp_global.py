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
    if "bgp" in config_data:
        commands = []
        if "bestpath" in config_data["bgp"]:
            cmd = "bgp bestpath"
            if "aigp" in config_data["bgp"]["bestpath"]:
                commands.append("{0} aigp".format(cmd))
            elif "compare_routerid" in config_data["bgp"]["bestpath"]:
                commands.append("{0} compare-routerid".format(cmd))
            elif "cost_community" in config_data["bgp"]["bestpath"]:
                commands.append("{0} cost-community ignore".format(cmd))
            elif "igp_metric" in config_data["bgp"]["bestpath"]:
                commands.append("{0} igp-metric ignore".format(cmd))
            elif "med" in config_data["bgp"]["bestpath"]:
                self_cmd = "{0} med".format(cmd)
                if "aigp" in config_data["bgp"]["bestpath"]:
                    self_cmd += " confed"
                elif "aigp" in config_data["bgp"]["bestpath"]:
                    self_cmd += " missing-as-worst"
                commands.append(self_cmd)
            return commands


def _tmplt_bgp_nopeerup_delay(config_data):
    if "bgp" in config_data:
        commands = []
        if "nopeerup_delay" in config_data["bgp"]:
            cmd = "bgp nopeerup-delay"
            if "cold_boot" in config_data["bgp"]["nopeerup_delay"]:
                commands.append(
                    "{0} cold-boot {cold_boot}".format(
                        cmd, **config_data["bgp"]["nopeerup_delay"]
                    )
                )
            elif "post_boot" in config_data["bgp"]["nopeerup_delay"]:
                commands.append(
                    "{0} post-boot {post_boot}".format(
                        cmd, **config_data["bgp"]["nopeerup_delay"]
                    )
                )
            elif "nsf_switchover" in config_data["bgp"]["nopeerup_delay"]:
                commands.append(
                    "{0} nsf-switchover {nsf_switchover}".format(
                        cmd, **config_data["bgp"]["nopeerup_delay"]
                    )
                )
            elif "user_initiated" in config_data["bgp"]["nopeerup_delay"]:
                commands.append(
                    "{0} user-initiated {user_initiated}".format(
                        cmd, **config_data["bgp"]["nopeerup_delay"]
                    )
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
        if "description" in config_data["neighbor"]:
            commands.append(
                "{0} description {description}".format(
                    cmd, **config_data["neighbor"]
                )
            )
        if "remote_as" in config_data["neighbor"]:
            commands.append(
                "{0} remote-as {remote_as}".format(
                    cmd, **config_data["neighbor"]
                )
            )
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
        return commands


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
            "name": "address_family",
            "getval": re.compile(
                r"""\s*(?P<address_family>address-family)""",
                re.VERBOSE,
            ),
            "compval": "address_family",
            "result": {
                "address_family": "{{ True if address_family is defined }}"
            },
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
            # "compval": "additional_paths",
            "result": {
                # "{{ asn }}": {
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
                },
                # },
            },
        },
        {
            "name": "bgp.advertise_best_external",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*(?P<advertise_best_external>advertise-best-external)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "bgp advertise-best-external",
            # "compval": "always_compare_med",
            "result": {
                "bgp": {
                    "advertise_best_external": "{{ True if advertise_best_external is defined }}"
                }
            },
        },
        {
            "name": "bgp.always_compare_med",
            "getval": re.compile(
                r"""\s*bgp*
                        \s*(?P<always_compare_med>always-compare-med)*
                        $""",
                re.VERBOSE,
            ),
            "setval": "bgp always-compare-med",
            # "compval": "always_compare_med",
            "result": {
                "bgp": {
                    "always_compare_med": "{{ True if always_compare_med is defined }}"
                }
            },
        },
        {
            "name": "bgp.log_neighbor_changes",
            "getval": re.compile(
                r"""\s*bgp*
                    \s*(?P<log_neighbor_changes>log-neighbor-changes)*
                    $""",
                re.VERBOSE,
            ),
            "setval": "bgp log-neighbor-changes",
            # "compval": "log_neighbor_changes",
            "result": {
                "bgp": {
                    "log_neighbor_changes": "{{ True if log_neighbor_changes is defined }}"
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
            # "compval": "bestpath",
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
            # "compval": "nopeerup_delay",
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
                    \s*(?P<remote_as>remote-as\s\d+)*
                    \s*(?P<description>description\s\S.+)*
                    \s*(?P<slow_peer>slow-peer\s(detection|split-update-group))*
                    \s*(?P<detection_disable>disable)*
                    \s*(?P<detection_threshold>threshold\s\d+)*
                    \s*(?P<split_dynamic>dynamic\s(disable|permanent))*
                    \s*(?P<split_static>static)*
                    \s*(?P<route_map>route-map\s\S+\s(in|out))*
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
                        "remote_as": "{{ remote_as.split('remote-as ')[1] if remote_as is defined }}",
                        "description": "{{ description.split('description ')[1] if description is defined }}",
                        "slow_peer": {
                            "detection": {
                                "enable": "{{ True if slow_peer is defined and 'detection' in slow_peer and detection_threshold is not defined }}",
                                "disable": "{{ True if detection_disable is defined }}",
                                "threshold": "{{ detection_threshold.split('threshold ')[1] if detection_threshold is defined }}",
                            },
                            "split_update_group": {
                                "dynamic": "{{ True if split_dynamic is defined and split_dynamic.split('dynamic ')[1] == 'disable' }}",
                                "static": "{{ True if split_static is defined }}",
                            },
                        },
                        "route_map": {
                            "name": "{{ route_map.split(' ')[1] if route_map is defined }}",
                            "in": "{{ True if route_map is defined and 'in' in route_map.split(' ') }}",
                            "out": "{{ True if route_map is defined and 'out' in route_map.split(' ') }}",
                        },
                    }
                ]
            },
        },
    ]
