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

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


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
                \saddress-family
                (\s(?P<afi>ipv4|ipv6|l2vpn|nsap|rtfilter|vpnv4|vpnv6))?
                (\s(?P<safi>flowspec|mdt|multicast|mvpn|unicast|evpn|vpls))?
                (\svrf\s(?P<vrf>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "address-family"
            "{{ (' ' + afi) if afi is defined else '' }}"
            "{{ (' ' + safi) if safi is defined else '' }}"
            "{{ (' vrf ' + vrf) if vrf is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"afi": "{{ afi }}", "safi": "{{ safi }}", "vrf": "{{ vrf }}"},
                },
            },
            "shared": True,
        },
        {
            "name": "aggregate_addresses",
            "getval": re.compile(
                r"""
                \s\saggregate-address
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
                "address_family": {
                    UNIQUE_AFI: {
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
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "auto_summary",
            "getval": re.compile(
                r"""
                ((\s\sauto-summary))?
                $""",
                re.VERBOSE,
            ),
            "setval": "auto-summary",
            "result": {"address_family": {UNIQUE_AFI: {"auto_summary": True}}},
        },
        {
            "name": "table_map",
            "getval": re.compile(
                r"""
                \s\stable-map
                (\s(?P<name>\S+))?
                (\s(?P<filter>filter))?
                $""",
                re.VERBOSE,
            ),
            "setval": "table-map"
            "{{ (' ' + table_map.name) if table_map.name is defined else '' }}"
            "{{ (' filter' ) if table_map.filter|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "table_map": {"name": "{{ name }}", "filter": "{{ not not filter }}"},
                    },
                },
            },
        },
        {
            "name": "default",
            "getval": re.compile(r"""\s\sdefault$""", re.VERBOSE),
            "setval": "default",
            "result": {"address_family": {UNIQUE_AFI: {"default": True}}},
        },
        {
            "name": "default_information",
            "getval": re.compile(r"""\s\sdefault-information\soriginate$""", re.VERBOSE),
            "setval": "default-information originate",
            "result": {"address_family": {UNIQUE_AFI: {"default_information": True}}},
        },
        {
            "name": "default_metric",
            "getval": re.compile(
                r"""\s\sdefault-metric
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
                r"""\s\sdistance\sbgp
                    (\s(?P<external>\d+))
                    (\s(?P<internal>\d+))
                    (\s(?P<local>\d+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "distance bgp {{ distance.external|string }} {{ distance.internal|string }} {{ distance.local|string }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "distance": {
                            "external": "{{ external }}",
                            "internal": "{{ internal }}",
                            "local": "{{ local }}",
                        },
                    },
                },
            },
        },
        # bgp starts
        {
            "name": "bgp.additional_paths.select",
            "getval": re.compile(
                r"""
                \s\sbgp\sadditional-paths\sselect
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
            "{{ (' best ' + bgp.additional_paths.select.best|string ) if bgp.additional_paths.select.best is defined else '' }}",
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.additional_paths.install",
            "getval": re.compile(
                r"""
                \s\sbgp\sadditional-paths\sinstall$""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select install",
            "result": {
                "address_family": {UNIQUE_AFI: {"bgp": {"additional_paths": {"install": True}}}},
            },
        },
        {
            "name": "bgp.additional_paths.receive",
            "getval": re.compile(
                r"""
                \s\sbgp\sadditional-paths\sreceive$""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select receive",
            "result": {
                "address_family": {UNIQUE_AFI: {"bgp": {"additional_paths": {"receive": True}}}},
            },
        },
        {
            "name": "bgp.additional_paths.send",
            "getval": re.compile(
                r"""
                \s\sbgp\sadditional-paths\ssend$""",
                re.VERBOSE,
            ),
            "setval": "bgp additional-paths select send",
            "result": {
                "address_family": {UNIQUE_AFI: {"bgp": {"additional_paths": {"send": True}}}},
            },
        },
        {
            "name": "bgp.aggregate_timer",
            "getval": re.compile(
                r"""
                \s\sbgp\saggregate-timer
                (\s(?P<aggregate_timer>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp aggregate-timer {{ bgp.aggregate_timer }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"aggregate_timer": "{{ aggregate_timer }}"}},
                },
            },
        },
        {
            "name": "bgp.dmzlink_bw",
            "getval": re.compile(
                r"""
                \s\sbgp\sdmzlink-bw
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp dmzlink-bw",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"dmzlink_bw": True}}}},
        },
        {
            "name": "bgp.nexthop.route_map",
            "getval": re.compile(
                r"""
                \s\sbgp\snexthop\sroute-map
                (\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop route-map {{ bgp.nexthop.route_map }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"nexthop": {"route_map": "{{ route_map }}"}}},
                },
            },
        },
        {
            "name": "bgp.nexthop.trigger.delay",
            "getval": re.compile(
                r"""
                \s\sbgp\snexthop\strigger\sdelay
                (\s(?P<delay>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger delay {{ bgp.nexthop.trigger.delay|string }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"nexthop": {"trigger": {"delay": "{{ delay }}"}}}},
                },
            },
        },
        {
            "name": "bgp.nexthop.trigger.enable",
            "getval": re.compile(
                r"""
                \s\sbgp\snexthop\strigger\sdelay\senable
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp nexthop trigger delay enable",
            "result": {
                "address_family": {UNIQUE_AFI: {"bgp": {"nexthop": {"trigger": {"enable": True}}}}},
            },
        },
        {
            "name": "bgp.redistribute_internal",
            "getval": re.compile(
                r"""
                \s\sbgp\sredistribute-internal
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
                \s\sbgp\sroute-map\spriority
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
                \s\sbgp\sscan-time
                (\s(?P<scan_time>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp scan-time {{ bgp.scan_time }}",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"scan_time": "{{ scan_time }}"}}}},
        },
        {
            "name": "bgp.soft_reconfig_backup",
            "getval": re.compile(
                r"""
                \s\sbgp\ssoft-reconfig-backup
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
                \s\sbgp\supdate-group\ssplit\sas-override
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp update-group split as-override",
            "result": {"address_family": {UNIQUE_AFI: {"bgp": {"update_group": True}}}},
        },
        {
            "name": "bgp.dampening",
            "getval": re.compile(
                r"""\s\sbgp\sdampening
                    (\s(?P<penalty_half_time>\d+))?
                    (\s(?P<reuse_route_val>\d+))?
                    (\s(?P<suppress_route_val>\d+))?
                    (\s(?P<max_suppress>\d+))?
                    (\sroute-map\s(?P<route_map>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "bgp dampening"
            "{{ (' ' + bgp.dampening.penalty_half_time|string ) if bgp.dampening.penalty_half_time is defined else '' }}"
            "{{ (' ' + bgp.dampening.reuse_route_val|string ) if bgp.dampening.reuse_route_val is defined else '' }}"
            "{{ (' ' + bgp.dampening.suppress_route_val|string ) if bgp.dampening.suppress_route_val is defined else '' }}"
            "{{ (' ' + bgp.dampening.max_suppress|string ) if bgp.dampening.max_suppress is defined else '' }}"
            "{{ (' route-map ' + bgp.dampening.route_map ) if bgp.dampening.route_map is defined else '' }}",
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.slow_peer_options.detection.enable",
            "getval": re.compile(r"""\s\sbgp\sslow-peer\sdetection$""", re.VERBOSE),
            "setval": "bgp slow-peer detection",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"bgp": {"slow_peer_options": {"detection": {"enable": True}}}},
                },
            },
        },
        {
            "name": "bgp.slow_peer_options.detection.threshold",
            "getval": re.compile(
                r"""
                \s\sbgp\sslow-peer\sdetection\sthreshold
                (\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer detection threshold {{ bgp.slow_peer_options.detection.threshold }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {
                            "slow_peer_options": {"detection": {"threshold": "{{ threshold }}"}},
                        },
                    },
                },
            },
        },
        {
            "name": "bgp.slow_peer_options.split_update_group.dynamic",
            "getval": re.compile(
                r"""
                \s\sbgp\sslow-peer\ssplit-update-group\sdynamic$""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer split-update-group dynamic",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {"slow_peer_options": {"split_update_group": {"dynamic": True}}},
                    },
                },
            },
        },
        {
            "name": "bgp.slow_peer.split_update_group.permanent",
            "getval": re.compile(
                r"""
                \s\sbgp\sslow-peer\ssplit-update-group\sdynamic\spermanent$""",
                re.VERBOSE,
            ),
            "setval": "bgp slow-peer split-update-group dynamic permanent",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "bgp": {"slow_peer_options": {"split_update_group": {"permanent": True}}},
                    },
                },
            },
        },
        # bgp ends
        # neighbor starts
        {
            "name": "peer_group_name",
            "getval": re.compile(
                r"""\s\sneighbor\s(?P<neighbor_address>\S+)
                \speer-group\s(?P<peer_group_name>\S+)
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "peer_group",
            "getval": re.compile(
                r"""\s\sneighbor\s(?P<neighbor_address>\S+)\speer-group$""",
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "remote_as",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\s(?P<remote_as>remote-as)
                (\s(?P<number>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} remote-as"
            "{{ (' ' + remote_as|string) if remote_as is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"remote_as": "{{ number }}"}}},
                },
            },
        },
        {
            "name": "local_as",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\s(?P<local_as>local-as)
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "neighbor_address",
            "getval": re.compile(
                r"""
                \sneighbordelDummy(?P<neighbor_address>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}",
            "result": {"dummy_neighbor": True},
        },
        {
            "name": "activate",
            "getval": re.compile(
                r"""\s\sneighbor\s(?P<neighbor_address>\S+)\sactivate$""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} activate",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "neighbor_address": UNIQUE_NEIB_ADD,
                                "activate": True,
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "additional_paths",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sadditional-paths
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "advertises.additional_paths",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sadvertise\sadditional-paths
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "advertises.best_external",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sadvertise\sbest-external
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' advertise best-external') if  advertise.best_external|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"advertises": {"best-external": True}}},
                    },
                },
            },
        },
        {
            "name": "advertises.diverse_path",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sadvertise\sdiverse-path
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "advertise_map",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sadvertise-map
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "advertisement_interval",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sadvertisement-interval
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
                                "advertisement_interval": "{{ advertisement_interval }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "aigp",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\saigp
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' aigp') if aigp.enable|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"aigp": {"enable": True}}}},
                },
            },
        },
        {
            "name": "aigp.send.cost_community",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\saigp\ssend\scost-community
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
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "aigp.send.med",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\saigp\ssend\smed
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' aigp send med') if aigp.send.med|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"aigp": {"send": {"med": True}}}}},
                },
            },
        },
        {
            "name": "allow_policy",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sallow-policy
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' allow-policy') if allow_policy|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"allow_policy": True}}},
                },
            },
        },
        {
            "name": "allowas_in",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sallowas-in
                (\s(?P<allowas_in>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' allowas-in ' + allowas_in|string) if allowas_in is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"allowas_in": "{{ allowas_in }}"}},
                    },
                },
            },
        },
        {
            "name": "as_override",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sas-override
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' as-override') if as_override|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"as_override": True}}},
                },
            },
        },
        {
            "name": "bmp_activate",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sbmp-activate
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "capability",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\scapability\sorf\sprefix-list
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "cluster_id",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\scluster-id(\s(?P<cluster_id>\s\d+))$""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} cluster-id {{ cluster_id }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"cluster_id": "{{ cluster_id }}"}},
                    },
                },
            },
        },
        {
            "name": "default_originate",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sdefault-originate$""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' default-originate') if default_originate.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"default_originate": {"set": True}}},
                    },
                },
            },
        },
        {
            "name": "default_originate.route_map",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sdefault-originate
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
                            UNIQUE_NEIB_ADD: {
                                "default_originate": {"route_map": "{{ route_map }}"},
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sdescription\s(?P<description>\S.+)$""",
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "disable_connected_check",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)
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
                                "disable_connected_check": "{{ not not disable_connected_check }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ebgp_multihop",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "distribute_list",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sdistribute-list
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "dmzlink_bw",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sdmzlink-bw
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' dmzlink-bw') if dmzlink_bw|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"dmzlink_bw": True}}},
                },
            },
        },
        {
            "name": "filter_list",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sfilter-list
                (\s(?P<acl>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} filter-list"
            "{{ (' ' + filter_list.as_path_acl) if filter_list.as_path_acl is defined else '' }}"
            "{{ (' in') if filter_list.in|d(False) else '' }}"
            "{{ (' out') if filter_list.out|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "filter_list": {
                                    "as_path_acl": "{{ acl }}",
                                    "in": "{{ not not in }}",
                                    "out": "{{ not not out }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "fall_over.bfd",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sfall-over
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "fall_over.route_map",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sroute-map
                \s(?P<route_map>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} route-map {{ fall_over.route_map }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "fall_over": {"route_map": "{{ not not route_map }}"},
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ha_mode",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sha-mode
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "inherit",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sinherit\speer-session
                \s(?P<inherit>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} inherit peer-session"
            "{{ (' ' + inherit) if inherit is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"inherit": "{{ inherit }}"}}},
                },
            },
        },
        {
            "name": "internal_vpn_client",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sinternal-vpn-client
                \s(?P<inherit>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} internal-vpn-client",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"internal_vpn_client": True}}},
                },
            },
        },
        {
            "name": "log_neighbor_changes",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "maximum_prefix",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\smaximum-prefix
                (\s(?P<max_no>\d+))
                (\s(?P<threshold_val>\d+))?
                (\srestart\s(?P<restart>\d+))?
                (\s(?P<warning_only>warning-only))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} maximum-prefix"
            "{{ (' ' + maximum_prefix.number|string) if maximum_prefix.number is defined else '' }}"
            "{{ (' ' + maximum_prefix.threshold_value|string) if maximum_prefix.threshold_value is defined else '' }}"
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
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "nexthop_self.set",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\snext-hop-self
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' next-hop-self') if nexthop_self.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"nexthop_self": {"set": True}}}},
                },
            },
        },
        {
            "name": "nexthop_self.all",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\snext-hop-self\sall
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' next-hop-self all') if nexthop_self.all|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"nexthop_self": {"all": True}}}},
                },
            },
        },
        {
            "name": "next_hop_unchanged.set",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\snext-hop-unchanged
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' next-hop-unchanged') if next_hop_unchanged.set|d(False) else ''}}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"next_hop_unchanged": {"set": True}}},
                    },
                },
            },
        },
        {
            "name": "next_hop_unchanged.allpaths",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\snext-hop-unchanged\sallpaths
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' next-hop-unchanged allpaths') if next_hop_unchanged.allpaths|d(False) else ''}}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"next_hop_unchanged": {"allpaths": True}}},
                    },
                },
            },
        },
        {
            "name": "password_options",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\spassword
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "path_attribute.discard",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\spath-attribute\sdiscard
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "path_attribute.treat_as_withdraw",
            "getval": re.compile(
                r"""\s\sneighbor\s(?P<neighbor_address>\S+)\spath-attribute\streat-as-withdraw
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "route_maps",
            "getval": re.compile(
                r"""\s\sneighbor\s(?P<neighbor_address>\S+)\sroute-map
                (\s(?P<route_map>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ route_maps.neighbor_address }} route-map"
            "{{ (' ' + route_maps.name) if route_maps.name is defined else '' }}"
            "{{ (' in') if route_maps.in|d(False) else '' }}"
            "{{ (' out') if route_maps.out|d(False) else '' }}",
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
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "prefix_lists",
            "getval": re.compile(
                r"""\s\sneighbor\s(?P<neighbor_address>\S+)\sprefix-list
                (\s(?P<prefix_list>\S+))
                (\s(?P<in>in))?
                (\s(?P<out>out))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ prefix_lists.neighbor_address }} prefix-list"
            "{{ (' ' + prefix_lists.name) if prefix_lists.name is defined else '' }}"
            "{{ (' in') if prefix_lists.in|d(False) else '' }}"
            "{{ (' out') if prefix_lists.out|d(False) else '' }}",
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
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "remove_private_as.set",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sremove-private-as
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as') if remove_private_as.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"remove_private_as": {"set": True}}},
                    },
                },
            },
        },
        {
            "name": "remove_private_as.all",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sremove-private-as\sall
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as all') if remove_private_as.all|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"remove_private_as": {"all": True}}},
                    },
                },
            },
        },
        {
            "name": "remove_private_as.replace_as",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sremove-private-as\sreplace-as
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address + ' remove-private-as replace-as') if remove_private_as.replace_as|d(False) else ''}}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"remove_private_as": {"replace_as": True}}},
                    },
                },
            },
        },
        {
            "name": "route_reflector_client",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sroute-reflector-client
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "route_server_client",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sroute-server-client
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "send_community.set",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\ssend-community
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ ('neighbor ' + neighbor_address  + ' send-community') if send_community.set|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"set": True}}}},
                },
            },
        },
        {
            "name": "send_community.both",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\ssend-community\sboth
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' both') if send_community.both|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"both": True}}},
                    },
                },
            },
        },
        {
            "name": "send_community.extended",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\ssend-community\sextended
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' extended') if send_community.extended|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"extended": True}}},
                    },
                },
            },
        },
        {
            "name": "send_community.standard",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\ssend-community\sstandard
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} send-community"
            "{{ (' standard') if send_community.standard|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"send_community": {"standard": True}}},
                    },
                },
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sshutdown
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
                                "shutdown": {"set": True, "graceful": "{{ graceful }}"},
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "slow_peer_options.detection",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sslow-peer\sdetection
                (\s(?P<enable>enable))?
                (\s(?P<disable>disable))?
                (\sthreshold\s(?P<threshold>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} slow-peer detection"
            "{{ (' enable') if slow_peer_options.detection.enable|d(False) else '' }}"
            "{{ (' disable') if slow_peer_options.detection.disable|d(False) else '' }}"
            "{{ (' threshold ' + slow_peer_options.detection.threshold|string) if slow_peer_options.detection.threshold is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "slow_peer_options": {
                                    "detection": {
                                        "enable": "{{ not not enable }}",
                                        "disable": "{{ not not disable }}",
                                        "threshold": "{{ threshold }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "slow_peer_options.split_update_group",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sslow-peer\ssplit-update-group
                (\s(?P<static>static))?
                (\s(?P<dynamic>dynamic))?
                (\s(?P<disable>disable))?
                (\s(?P<permanent>permanent))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} slow-peer split-update-group"
            "{{ (' static') if slow_peer_options.split_update_group.static|d(False) else '' }}"
            "{{ (' dynamic') if slow_peer_options.split_update_group.dynamic.enable|d(False) else '' }}"
            "{{ (' disable') if slow_peer_options.split_update_group.dynamic.disable|d(False) else '' }}"
            "{{ (' permanent') if slow_peer_options.split_update_group.dynamic.permanent|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "slow_peer_options": {
                                    "split_update_group": {
                                        "static": "{{ not not static }}",
                                        "dynamic": {
                                            "enable": "{{ not not dynamic }}",
                                            "disable": "{{ not not disable }}",
                                            "permanent": "{{ not not permanent }}",
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "soft_reconfiguration",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\ssoft-reconfiguration\sinbound
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }}"
            "{{ (' soft-reconfiguration inbound') if soft_reconfiguration|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"soft_reconfiguration": True}}},
                },
            },
        },
        {
            "name": "soo",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\ssoo
                (\s(?P<soo>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} soo {{ soo }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"soo": "{{ soo }}"}}},
                },
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\stimers
                (\s(?P<keepalive>\d+))?
                (\s(?P<holdtime>\d+))?
                (\s(?P<min_holdtime>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} timers"
            "{{ (' ' + timers.interval|string) if timers.interval is defined else '' }}"
            "{{ (' ' + timers.holdtime|string) if timers.holdtime is defined else '' }}"
            "{{ (' ' + timers.min_holdtime|string) if timers.min_holdtime is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {
                            UNIQUE_NEIB_ADD: {
                                "timers": {
                                    "interval": "{{ keepalive }}",
                                    "holdtime": "{{ holdtime }}",
                                    "min_holdtime": "{{ min_holdtime }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "transport.connection_mode",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\stransport\sconnection-mode
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "transport.multi_session",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\stransport\smulti-session
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "transport.path_mtu_discovery",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\stransport\spath-mtu-discovery
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
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sttl-security
                (\shops(?P<ttl_security>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} ttl-security"
            "{{ (' hops '+ ttl_security|string) if ttl_security is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"ttl_security": "{{ ttl_security }}"}},
                    },
                },
            },
        },
        {
            "name": "unsuppress_map",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sunsuppress-map
                (\s(?P<unsuppress_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} unsuppress-map"
            "{{ (' ' + unsuppress_map) if unsuppress_map is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "neighbors": {UNIQUE_NEIB_ADD: {"unsuppress_map": "{{ unsuppress_map }}"}},
                    },
                },
            },
        },
        {
            "name": "version",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sversion
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
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "weight",
            "getval": re.compile(
                r"""
                \s\sneighbor\s(?P<neighbor_address>\S+)\sweight
                (\s(?P<weight>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "neighbor {{ neighbor_address }} weight"
            "{{ (' ' + weight|string) if weight is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {"neighbors": {UNIQUE_NEIB_ADD: {"weight": "{{ weight }}"}}},
                },
            },
        },
        # neighbors end
        {
            "name": "networks",
            "getval": re.compile(
                r"""
                \s\snetwork
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
            "{{ (' mask ' + mask) if mask is defined else '' }}"
            "{{ (' route-map ' + route_map) if route_map is defined else '' }}"
            "{{ (' backdoor' ) if backdoor|d(False) else '' }}"
            "{{ (' evpn' ) if evpn|d(False) else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "networks": [
                            {
                                "address": "{{ address }}",
                                "mask": "{{ netmask }}",
                                "route_map": "{{ route_map }}",
                                "evpn": "{{ not not evpn }}",
                                "backdoor": "{{ not not backdoor }}",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "snmp.context.user",
            "getval": re.compile(
                r"""\s\ssnmp
                    (\scontext\s(?P<context>\S+))
                    (\suser\s(?P<user>\S+))
                    (\s(?P<credential>credential))?
                    (\s(?P<encrypted>encrypted))?
                    (\sauth\smd5\s(?P<md5>\S+))?
                    (\sauth\ssha\s(?P<sha>\S+))?
                    (\spriv\saes\s128\s(?P<a>\S+))?
                    (\spriv\saes\s192\s(?P<b>\S+))?
                    (\spriv\saes\s256\s(?P<c>\S+))?
                    (\spriv\sdes\s(?P<des>\S+))?
                    (\spriv\sdes56\s(?P<des56>\S+))?
                    (\saccess\sipv6\s(?P<aclv6>\S+))?
                    (\saccess\s(?P<acl>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "snmp context {{ snmp.context.name }} user"
            "{{ (' ' + snmp.context.user.name) if snmp.context.user.name is defined else '' }}"
            "{{ (' credential' ) if snmp.context.user.credential|d(False) else '' }}"
            "{{ (' encrypted' ) if snmp.context.user.encrypted|d(False) else '' }}"
            "{{ (' auth md5 ' + snmp.context.user.auth.md5 ) if snmp.context.user.auth is defined and snmp.context.user.auth.acl is defined else '' }}"
            "{{ (' auth sha ' + snmp.context.user.auth.sha ) if snmp.context.user.auth is defined and snmp.context.user.auth.sha is defined else '' }}"
            "{{ (' priv md5 ' + snmp.context.user.priv.aes128 ) if snmp.context.user.priv is defined and snmp.context.user.priv.aes128 is defined else '' }}"
            "{{ (' priv sha ' + snmp.context.user.priv.aes192 ) if snmp.context.user.priv is defined and snmp.context.user.priv.aes192 is defined else '' }}"
            "{{ (' priv sha ' + snmp.context.user.priv.aes256 ) if snmp.context.user.priv is defined and snmp.context.user.priv.aes256 is defined else '' }}"
            "{{ (' priv sha ' + snmp.context.user.priv.des56 ) if snmp.context.user.priv is defined and snmp.context.user.priv.des56 is defined else '' }}"
            "{{ (' priv sha ' + snmp.context.user.priv.des ) if snmp.context.user.priv is defined and snmp.context.user.priv.des is defined else '' }}"
            "{{ (' access ' + snmp.context.user.access.acl|string ) if snmp.context.user.access is defined"
            " and snmp.context.user.access.acl is defined else '' }}"
            "{{ (' access ipv6 ' + snmp.context.user.access.ipv6|string ) if snmp.context.user.access is defined"
            " and snmp.context.user.access.ipv6 is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "snmp": {
                            "context": {
                                "name": "{{ context }}",
                                "user": {
                                    "name": "{{ user }}",
                                    "access": {"acl": "{{ acl }}", "ipv6": "{{ aclv6 }}"},
                                    "auth": {"md5": "{{ md5 }}", "sha": "{{ sha }}"},
                                    "priv": {
                                        "des56": "{{ des56 }}",
                                        "aes128": "{{ a }}",
                                        "aes192": "{{ b }}",
                                        "aes256": "{{ c }}",
                                        "des": "{{ des }}",
                                    },
                                    "credential": "{{ not not credential }}",
                                    "encrypted": "{{ not not encrypted }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "snmp.context.community",
            "getval": re.compile(
                r"""\s\ssnmp
                    (\scontext\s(?P<context>\S+))
                    (\scommunity\s(?P<community>\S+))
                    (\s(?P<ro>RO))?
                    (\s(?P<rw>RW))?
                    (\sipv6\s(?P<ip6acl>\S+))?
                    (\s(?P<acl>\S+))?
                    $""",
                re.VERBOSE,
            ),
            "setval": "snmp context {{ snmp.context.name }} community"
            "{{ (' ' + snmp.context.community.snmp_community) if snmp.context.community.snmp_community is defined else '' }}"
            "{{ (' ro' ) if snmp.context.community.ro|d(False) else '' }}"
            "{{ (' rw' ) if snmp.context.community.rw|d(False) else '' }}"
            "{{ (' ' + snmp.context.community.acl) if snmp.context.community.acl is defined else '' }}"
            "{{ (' ipv6 ' + snmp.context.community.ipv6) if snmp.context.community.ipv6 is defined else '' }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "snmp": {
                            "context": {
                                "name": "{{ context }}",
                                "community": {
                                    "snmp_community": "{{ community }}",
                                    "acl": "{{ acl }}",
                                    "ro": "{{ not not ro }}",
                                    "rw": "{{ not not rw }}",
                                    "ipv6": "{{ ip6acl }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        # redistribute starts
        {
            "name": "redistribute.application",
            "getval": re.compile(
                r"""
                \s\sredistribute\sapplication\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute application {{ redistribute.application.name }}"
            "{{ (' metric ' + redistribute.application.metric|string) if redistribute.application.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.application.route_map) if redistribute.application.route_map is defined else '' }}",
            "remval": "redistribute application {{ redistribute.application.name }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "application": {
                                    "name": "{{ name }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.bgp",
            "getval": re.compile(
                r"""
                \s\sredistribute\sbgp\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute bgp {{ redistribute.bgp.as_number }}"
            "{{ (' metric ' + redistribute.bgp.metric|string) if redistribute.bgp.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.bgp.route_map) if redistribute.bgp.route_map is defined else '' }}",
            "remval": "redistribute bgp {{ redistribute.bgp.as_number }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "bgp": {
                                    "as_number": "{{ name }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.connected",
            "getval": re.compile(
                r"""
                \s\sredistribute\sconnected
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute connected"
            "{{ (' metric ' + redistribute.connected.metric|string) if redistribute.connected.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.connected.route_map) if redistribute.connected.route_map is defined else '' }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.eigrp",
            "getval": re.compile(
                r"""
                \s\sredistribute\seigrp\s(?P<name>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute eigrp {{ redistribute.eigrp.name|string }}"
            "{{ (' metric ' + redistribute.eigrp.metric|string) if redistribute.eigrp.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.eigrp.route_map) if redistribute.eigrp.route_map is defined else '' }}",
            "remval": "redistribute eigrp {{ redistribute.eigrp.name|string }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "eigrp": {
                                    "as_number": "{{ name }}",
                                    "metric": "{{ metric }}",
                                    "route_map": "{{ route_map }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.isis",
            "getval": re.compile(
                r"""
                \s\sredistribute\sisis\s(?P<name>\S+)
                (\s(?P<clns>clns))?
                (\s(?P<ip>ip))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute isis {{ redistribute.isis.area_tag }}"
            "{{ (' clns') if redistribute.isis.clns|d(False) else '' }}"
            "{{ (' ip') if redistribute.isis.ip|d(False) else '' }}"
            "{{ (' metric ' + redistribute.isis.metric|string) if redistribute.isis.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.isis.route_map) if redistribute.isis.route_map is defined else '' }}",
            "remval": "redistribute isis {{ redistribute.isis.area_tag }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.iso_igrp",
            "getval": re.compile(
                r"""
                \s\sredistribute\siso-igrp\s(?P<name>\S+)
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute iso-igrp {{ redistribute.iso_igrp.area_tag }}"
            "{{ (' route-map ' + redistribute.iso_igrp.route_map) if redistribute.iso_igrp.route_map is defined else '' }}",
            "remval": "redistribute iso-igrp {{ redistribute.iso_igrp.area_tag }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "iso_igrp": {
                                    "area_tag": "{{ name }}",
                                    "route_map": "{{ route_map }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.lisp",
            "getval": re.compile(
                r"""
                \s\sredistribute\slisp
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute lisp"
            "{{ (' metric ' + redistribute.lisp.metric|string) if redistribute.lisp.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.lisp.route_map) if redistribute.lisp.route_map is defined else '' }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.mobile",
            "getval": re.compile(
                r"""
                \s\sredistribute\smobile
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute mobile"
            "{{ (' metric ' + redistribute.mobile.metric|string) if redistribute.mobile.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.mobile.route_map) if redistribute.mobile.route_map is defined else '' }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.odr",
            "getval": re.compile(
                r"""
                \s\sredistribute\sodr
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute odr"
            "{{ (' metric ' + redistribute.odr.metric|string) if redistribute.odr.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.odr.route_map) if redistribute.odr.route_map is defined else '' }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.ospf",
            "getval": re.compile(
                r"""
                \s+redistribute\sospf\s(?P<process_id>\S+)
                (\svrf(?P<vrf>\s\S+))?
                (\smetric\s(?P<metric>\d+))?
                (\smatch)?
                (\s(?P<internal>internal))?
                (\s(?P<ext_type_1>external\s1))?
                (\s(?P<ext_type_2>external\s2))?
                (\s(?P<nssa_type_1>nssa-external\s1))?
                (\s(?P<nssa_type_2>nssa-external\s2))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\s(?P<include_connected>include-connected))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute ospf {{ process_id }}"
            "{{ (' metric ' + metric|string) if metric is defined }}"
            "{{ (' vrf ' + vrf) if vrf is defined }}"
            "{{ (' match') if match is defined }}"
            "{{ (' internal') if match is defined and match.internal is defined and match.internal }}"
            "{{ (' external 1') if match is defined and match.externals is defined and "
            "match.externals.type_1 is defined and match.externals.type_1 }}"
            "{{ (' external 2') if match is defined and match.externals is defined and "
            "match.externals.type_2 is defined and match.externals.type_2 }}"
            "{{ (' nssa-external 1') if match is defined and match.nssa_externals is defined and "
            "match.nssa_externals.type_1 is defined and match.nssa_externals.type_1 }}"
            "{{ (' nssa-external 2') if match is defined and match.nssa_externals is defined and "
            "match.nssa_externals.type_2 is defined and match.nssa_externals.type_2}}"
            "{{ (' route-map ' + route_map) if route_map is defined }}"
            "{{ (' include-connected') if include_connected is defined and include_connected }}",
            "remval": "redistribute ospf {{ process_id }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "ospf": {
                                    "process_id": "{{ process_id }}",
                                    "vrf": "{{ vrf }}",
                                    "metric": "{{ metric }}",
                                    "match": {
                                        "internal": "{{ not not internal }}",
                                        "externals": {
                                            "type_1": "{{ not not ext_type_1 }}",
                                            "type_2": "{{ not not ext_type_2 }}",
                                        },
                                        "nssa_externals": {
                                            "type_1": "{{ not not nssa_type_1 }}",
                                            "type_2": "{{ not not nssa_type_2 }}",
                                        },
                                    },
                                    "route_map": "{{ route_map }}",
                                    "include_connected": "{{ not not include_connected }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.ospfv3",
            "getval": re.compile(
                r"""
                \s+redistribute\sospfv3\s(?P<process_id>\S+)
                (\smetric\s(?P<metric>\d+))?
                (\smatch)?
                (\s(?P<internal>internal))?
                (\s(?P<ext_type_1>external\s1))?
                (\s(?P<ext_type_2>external\s2))?
                (\s(?P<nssa_type_1>nssa-external\s1))?
                (\s(?P<nssa_type_2>nssa-external\s2))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute ospfv3 {{ process_id }}"
            "{{ (' metric ' + metric|string) if metric is defined }}"
            "{{ (' match') if match is defined }}"
            "{{ (' internal') if match is defined and match.internal is defined and match.internal }}"
            "{{ (' external 1') if match is defined and match.externals is defined and "
            "match.externals.type_1 is defined and match.externals.type_1 }}"
            "{{ (' external 2') if match is defined and match.externals is defined and "
            "match.externals.type_2 is defined and match.externals.type_2 }}"
            "{{ (' nssa-external 1') if match is defined and match.nssa_externals is defined and "
            "match.nssa_externals.type_1 is defined and match.nssa_externals.type_1 }}"
            "{{ (' nssa-external 2') if match is defined and match.nssa_externals is defined and "
            "match.nssa_externals.type_2 is defined and match.nssa_externals.type_2}}"
            "{{ (' route-map ' + route_map) if route_map is defined }}",
            "remval": "redistribute ospfv3 {{ process_id }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {
                                "ospfv3": {
                                    "process_id": "{{ process_id }}",
                                    "metric": "{{ metric }}",
                                    "match": {
                                        "internal": "{{ not not internal }}",
                                        "externals": {
                                            "type_1": "{{ not not ext_type_1 }}",
                                            "type_2": "{{ not not ext_type_2 }}",
                                        },
                                        "nssa_externals": {
                                            "type_1": "{{ not not nssa_type_1 }}",
                                            "type_2": "{{ not not nssa_type_2 }}",
                                        },
                                    },
                                    "route_map": "{{ route_map }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.rip",
            "getval": re.compile(
                r"""
                \s\sredistribute\srip
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute rip"
            "{{ (' metric ' + redistribute.rip.metric|string) if redistribute.rip.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.rip.route_map) if redistribute.rip.route_map is defined else '' }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.static",
            "getval": re.compile(
                r"""
                \s\sredistribute\sstatic
                (\s(?P<clns>clns))?
                (\s(?P<ip>ip))?
                (\smetric\s(?P<metric>\d+))?
                (\sroute-map\s(?P<route_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute static"
            "{{ (' clns') if redistribute.static.clns|d(False) else '' }}"
            "{{ (' ip') if redistribute.static.ip|d(False) else '' }}"
            "{{ (' metric ' + redistribute.static.metric|string) if redistribute.static.metric is defined else '' }}"
            "{{ (' route-map ' + redistribute.static.route_map) if redistribute.static.route_map is defined else '' }}",
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
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "redistribute.vrf",
            "getval": re.compile(
                r"""
                \s\sredistribute\svrf
                (\s(?P<name>\S+))?
                (\s(?P<global>global))?
                $""",
                re.VERBOSE,
            ),
            "setval": "redistribute vrf {{ redistribute.vrf.name }}"
            "{{ (' global') if redistribute.vrf.global|d(False) else '' }}",
            "remval": "redistribute vrf {{ redistribute.vrf.name }}",
            "result": {
                "address_family": {
                    UNIQUE_AFI: {
                        "redistribute": [
                            {"vrf": {"name": "{{ name }}", "global": "{{ not not global }}"}},
                        ],
                    },
                },
            },
        },
        # redistribute ends
    ]
