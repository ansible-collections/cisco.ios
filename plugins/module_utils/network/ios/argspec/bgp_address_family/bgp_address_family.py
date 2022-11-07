# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# cli_rm_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################

"""
The arg spec for the ios_bgp_address_family module
"""


class Bgp_address_familyArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_bgp_address_family module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "as_number": {"type": "str"},
                "address_family": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "afi": {
                            "type": "str",
                            "choices": [
                                "ipv4",
                                "ipv6",
                                "l2vpn",
                                "nsap",
                                "rtfilter",
                                "vpnv4",
                                "vpnv6",
                            ],
                        },
                        "safi": {
                            "type": "str",
                            "choices": ["flowspec", "mdt", "multicast", "mvpn", "evpn", "unicast"],
                        },
                        "vrf": {"type": "str"},
                        "aggregate_address": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "address": {"type": "str"},
                                "netmask": {"type": "str"},
                                "advertise_map": {"type": "str"},
                                "as_confed_set": {"type": "bool"},
                                "as_set": {"type": "bool"},
                                "attribute_map": {"type": "str"},
                                "summary_only": {"type": "bool"},
                                "suppress_map": {"type": "str"},
                            },
                        },
                        "auto_summary": {"type": "bool"},
                        "bgp": {
                            "type": "dict",
                            "options": {
                                "additional_paths": {
                                    "type": "dict",
                                    "options": {
                                        "receive": {"type": "bool"},
                                        "select": {
                                            "type": "dict",
                                            "options": {
                                                "all": {"type": "bool"},
                                                "best": {"type": "int"},
                                                "group_best": {"type": "bool"},
                                            },
                                        },
                                        "send": {"type": "bool"},
                                    },
                                },
                                "aggregate_timer": {"type": "int"},
                                "dampening": {
                                    "type": "dict",
                                    "options": {
                                        "penalty_half_time": {"type": "int"},
                                        "reuse_route_val": {"type": "int"},
                                        "suppress_route_val": {"type": "int"},
                                        "max_suppress": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "dmzlink_bw": {"type": "bool"},
                                "nexthop": {
                                    "type": "dict",
                                    "options": {
                                        "route_map": {"type": "str"},
                                        "trigger": {
                                            "type": "dict",
                                            "options": {
                                                "delay": {"type": "int"},
                                                "enable": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "redistribute_internal": {"type": "bool"},
                                "route_map": {"type": "bool"},
                                "scan_time": {"type": "int"},
                                "slow_peer": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "detection": {
                                            "type": "dict",
                                            "options": {
                                                "enable": {"type": "bool"},
                                                "threshold": {"type": "int"},
                                            },
                                        },
                                        "split_update_group": {
                                            "type": "dict",
                                            "options": {
                                                "dynamic": {"type": "bool"},
                                                "permanent": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "soft_reconfig_backup": {"type": "bool"},
                                "update_group": {"type": "bool"},
                            },
                        },
                        "default": {"type": "bool"},
                        "default_information": {"type": "bool"},
                        "default_metric": {"type": "int"},
                        "distance": {
                            "type": "dict",
                            "options": {
                                "external": {"type": "int"},
                                "internal": {"type": "int"},
                                "local": {"type": "int"},
                            },
                        },
                        "neighbors": {
                            "type": "list",
                            "elements": "dict",
                            "aliases": ["neighbor"],
                            "options": {
                                "neighbor_address": {"type": "str"},
                                "address": {"type": "str"},
                                "tag": {"type": "str"},
                                "ipv6_adddress": {"type": "str", "aliases": ["ipv6_address"]},
                                "activate": {"type": "bool"},
                                "additional_paths": {
                                    "type": "dict",
                                    "options": {
                                        "disable": {"type": "bool"},
                                        "receive": {"type": "bool"},
                                        "send": {"type": "bool"},
                                    },
                                },
                                "advertise": {
                                    "type": "dict",
                                    "options": {
                                        "all": {"type": "bool"},
                                        "best": {"type": "int"},
                                        "group_best": {"type": "bool"},
                                    },
                                },
                                "advertise_map": {
                                    "type": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "exist_map": {"type": "str"},
                                        "non_exist_map": {"type": "str"},
                                    },
                                },
                                "advertisement_interval": {"type": "int"},
                                "aigp": {
                                    "type": "dict",
                                    "options": {
                                        "enable": {"type": "str"},
                                        "send": {
                                            "type": "dict",
                                            "options": {
                                                "cost_community": {
                                                    "type": "dict",
                                                    "options": {
                                                        "id": {"type": "int"},
                                                        "poi": {
                                                            "type": "dict",
                                                            "options": {
                                                                "igp_cost": {"type": "bool"},
                                                                "pre_bestpath": {"type": "bool"},
                                                                "transitive": {"type": "bool"},
                                                            },
                                                        },
                                                    },
                                                },
                                                "med": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "allow_policy": {"type": "bool"},
                                "allowas_in": {"type": "int"},
                                "as_override": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "split_horizon": {"type": "bool"},
                                    },
                                },
                                "bmp_activate": {
                                    "type": "dict",
                                    "options": {"all": {"type": "bool"}, "server": {"type": "int"}},
                                },
                                "capability": {
                                    "type": "dict",
                                    "options": {
                                        "both": {"type": "bool"},
                                        "receive": {"type": "bool"},
                                        "send": {"type": "bool"},
                                    },
                                },
                                "cluster_id": {"type": "str"},
                                "default_originate": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "description": {"type": "str"},
                                "disable_connected_check": {"type": "bool"},
                                "distribute_list": {
                                    "type": "dict",
                                    "options": {
                                        "acl": {"type": "str"},
                                        "in": {"type": "bool"},
                                        "out": {"type": "bool"},
                                    },
                                },
                                "dmzlink_bw": {"type": "bool"},
                                "ebgp_multihop": {
                                    "type": "dict",
                                    "options": {
                                        "enable": {"type": "bool"},
                                        "hop_count": {"type": "int"},
                                    },
                                },
                                "fall_over": {
                                    "type": "dict",
                                    "options": {
                                        "bfd": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "multi_hop": {"type": "bool"},
                                                "single_hop": {"type": "bool"},
                                            },
                                        },
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "filter_list": {
                                    "type": "dict",
                                    "options": {
                                        "as_path_acl": {"type": "int"},
                                        "in": {"type": "bool"},
                                        "out": {"type": "bool"},
                                    },
                                },
                                "ha_mode": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "disable": {"type": "bool"},
                                    },
                                },
                                "inherit": {"type": "str"},
                                "internal_vpn_client": {"type": "bool"},
                                "local_as": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "number": {"type": "int"},
                                        "dual_as": {"type": "bool"},
                                        "no_prepend": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "replace_as": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "log_neighbor_changes": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "disable": {"type": "bool"},
                                    },
                                },
                                "maximum_prefix": {
                                    "type": "dict",
                                    "options": {
                                        "number": {"type": "int"},
                                        "threshold_value": {"type": "int"},
                                        "restart": {"type": "int"},
                                        "warning_only": {"type": "bool"},
                                    },
                                },
                                "next_hop_self": {"type": "bool"},
                                "nexthop_self": {
                                    "type": "dict",
                                    "options": {"set": {"type": "bool"}, "all": {"type": "bool"}},
                                },
                                "next_hop_unchanged": {"type": "bool"},
                                "password": {"type": "str", "no_log": True},
                                "path_attribute": {
                                    "type": "dict",
                                    "options": {
                                        "discard": {
                                            "type": "dict",
                                            "options": {
                                                "type": {"type": "int"},
                                                "range": {
                                                    "type": "dict",
                                                    "options": {
                                                        "start": {"type": "int"},
                                                        "end": {"type": "int"},
                                                    },
                                                },
                                                "in": {"type": "bool"},
                                            },
                                        },
                                        "treat_as_withdraw": {
                                            "type": "dict",
                                            "options": {
                                                "type": {"type": "int"},
                                                "range": {
                                                    "type": "dict",
                                                    "options": {
                                                        "start": {"type": "int"},
                                                        "end": {"type": "int"},
                                                    },
                                                },
                                                "in": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "peer_group": {"type": "bool"},
                                "prefix_list": {
                                    "type": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "in": {"type": "bool"},
                                        "out": {"type": "bool"},
                                    },
                                },
                                "prefix_lists": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "in": {"type": "bool"},
                                        "out": {"type": "bool"},
                                    },
                                },
                                "remote_as": {"type": "int"},
                                "remove_private_as": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "all": {"type": "bool"},
                                        "replace_as": {"type": "bool"},
                                    },
                                },
                                "route_map": {
                                    "type": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "in": {"type": "bool"},
                                        "out": {"type": "bool"},
                                    },
                                },
                                "route_maps": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "in": {"type": "bool"},
                                        "out": {"type": "bool"},
                                    },
                                },
                                "route_reflector_client": {"type": "bool"},
                                "route_server_client": {"type": "bool"},
                                "send_community": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "both": {"type": "bool"},
                                        "extended": {"type": "bool"},
                                        "standard": {"type": "bool"},
                                    },
                                },
                                "shutdown": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "graceful": {"type": "int"},
                                    },
                                },
                                "slow_peer": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "detection": {
                                            "type": "dict",
                                            "options": {
                                                "enable": {"type": "bool"},
                                                "disable": {"type": "bool"},
                                                "threshold": {"type": "int"},
                                            },
                                        },
                                        "split_update_group": {
                                            "type": "dict",
                                            "options": {
                                                "dynamic": {
                                                    "type": "dict",
                                                    "options": {
                                                        "enable": {"type": "bool"},
                                                        "disable": {"type": "bool"},
                                                        "permanent": {"type": "bool"},
                                                    },
                                                },
                                                "static": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "soft_reconfiguration": {"type": "bool"},
                                "soo": {"type": "str"},
                                "timers": {
                                    "type": "dict",
                                    "options": {
                                        "interval": {"type": "int"},
                                        "holdtime": {"type": "int"},
                                        "min_holdtime": {"type": "int"},
                                    },
                                },
                                "transport": {
                                    "type": "dict",
                                    "options": {
                                        "connection_mode": {
                                            "type": "dict",
                                            "options": {
                                                "active": {"type": "bool"},
                                                "passive": {"type": "bool"},
                                            },
                                        },
                                        "multi_session": {"type": "bool"},
                                        "path_mtu_discovery": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "disable": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "ttl_security": {"type": "int"},
                                "unsuppress_map": {"type": "str"},
                                "version": {"type": "int"},
                                "weight": {"type": "int"},
                            },
                        },
                        "network": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "address": {"type": "str"},
                                "mask": {"type": "str"},
                                "backdoor": {"type": "bool"},
                                "route_map": {"type": "str"},
                            },
                        },
                        "redistribute": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "application": {
                                    "type": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "bgp": {
                                    "type": "dict",
                                    "options": {
                                        "as_number": {"type": "str"},
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "connected": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "eigrp": {
                                    "type": "dict",
                                    "options": {
                                        "as_number": {"type": "str"},
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "isis": {
                                    "type": "dict",
                                    "options": {
                                        "area_tag": {"type": "str"},
                                        "clns": {"type": "bool"},
                                        "ip": {"type": "bool"},
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "iso_igrp": {
                                    "type": "dict",
                                    "options": {
                                        "area_tag": {"type": "str"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "lisp": {
                                    "type": "dict",
                                    "options": {
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "mobile": {
                                    "type": "dict",
                                    "options": {
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "odr": {
                                    "type": "dict",
                                    "options": {
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "ospf": {
                                    "type": "dict",
                                    "options": {
                                        "process_id": {"type": "int"},
                                        "match": {
                                            "type": "dict",
                                            "options": {
                                                "external": {"type": "bool"},
                                                "internal": {"type": "bool"},
                                                "nssa_external": {"type": "bool"},
                                                "type_1": {"type": "bool"},
                                                "type_2": {"type": "bool"},
                                            },
                                        },
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                        "vrf": {"type": "str"},
                                    },
                                },
                                "ospfv3": {
                                    "type": "dict",
                                    "options": {
                                        "process_id": {"type": "int"},
                                        "match": {
                                            "type": "dict",
                                            "options": {
                                                "external": {"type": "bool"},
                                                "internal": {"type": "bool"},
                                                "nssa_external": {"type": "bool"},
                                                "type_1": {"type": "bool"},
                                                "type_2": {"type": "bool"},
                                            },
                                        },
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "rip": {
                                    "type": "dict",
                                    "options": {
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "static": {
                                    "type": "dict",
                                    "options": {
                                        "clns": {"type": "bool"},
                                        "ip": {"type": "bool"},
                                        "metric": {"type": "int"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "vrf": {
                                    "type": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "global": {"type": "bool"},
                                    },
                                },
                            },
                        },
                        "snmp": {
                            "type": "dict",
                            "options": {
                                "context": {
                                    "type": "dict",
                                    "options": {
                                        "name": {"type": "str"},
                                        "community": {
                                            "type": "dict",
                                            "options": {
                                                "snmp_community": {"type": "str"},
                                                "acl": {"type": "str"},
                                                "ipv6": {"type": "str"},
                                                "ro": {"type": "bool"},
                                                "rw": {"type": "bool"},
                                            },
                                        },
                                        "user": {
                                            "type": "dict",
                                            "options": {
                                                "name": {"type": "str"},
                                                "access": {
                                                    "type": "dict",
                                                    "options": {
                                                        "acl": {"type": "str"},
                                                        "ipv6": {"type": "str"},
                                                    },
                                                },
                                                "auth": {
                                                    "type": "dict",
                                                    "options": {
                                                        "md5": {"type": "str"},
                                                        "sha": {"type": "str"},
                                                    },
                                                },
                                                "priv": {
                                                    "type": "dict",
                                                    "options": {"des": {"type": "str"}},
                                                },
                                                "credential": {"type": "bool"},
                                                "encrypted": {"type": "bool"},
                                            },
                                        },
                                    },
                                }
                            },
                        },
                        "table_map": {
                            "type": "dict",
                            "options": {"name": {"type": "str"}, "filter": {"type": "bool"}},
                        },
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
