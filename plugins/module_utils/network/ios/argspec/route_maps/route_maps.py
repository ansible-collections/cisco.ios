# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
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
The arg spec for the cisco.ios_route_maps module
"""


class Route_mapsArgs(object):  # pylint: disable=R0903
    """The arg spec for the cisco.ios_route_maps module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "route_map": {"type": "str"},
                "entries": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "sequence": {"type": "int"},
                        "action": {
                            "type": "str",
                            "choices": ["deny", "permit"],
                        },
                        "continue_entry": {
                            "type": "dict",
                            "options": {
                                "set": {"type": "bool"},
                                "entry_sequence": {"type": "int"},
                            },
                        },
                        "description": {"type": "str"},
                        "match": {
                            "type": "dict",
                            "options": {
                                "additional_paths": {
                                    "type": "dict",
                                    "options": {
                                        "all": {"type": "bool"},
                                        "best": {"type": "int"},
                                        "best_range": {
                                            "type": "dict",
                                            "options": {
                                                "lower_limit": {"type": "int"},
                                                "upper_limit": {"type": "int"},
                                            },
                                        },
                                        "group_best": {"type": "bool"},
                                    },
                                },
                                "as_path": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "acls": {
                                            "type": "list",
                                            "elements": "int",
                                        },
                                    },
                                },
                                "clns": {
                                    "type": "dict",
                                    "options": {
                                        "address": {"type": "str"},
                                        "next_hop": {"type": "str"},
                                        "route_source": {"type": "str"},
                                    },
                                },
                                "community": {
                                    "type": "dict",
                                    "options": {
                                        "name": {
                                            "type": "list",
                                            "elements": "str",
                                        },
                                        "exact_match": {"type": "bool"},
                                    },
                                },
                                "extcommunity": {
                                    "type": "list",
                                    "elements": "str",
                                },
                                "interfaces": {
                                    "type": "list",
                                    "elements": "str",
                                },
                                "ip": {
                                    "type": "dict",
                                    "options": {
                                        "address": {
                                            "type": "dict",
                                            "options": {
                                                "acls": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                                "prefix_lists": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                            },
                                        },
                                        "flowspec": {
                                            "type": "dict",
                                            "options": {
                                                "dest_pfx": {"type": "bool"},
                                                "src_pfx": {"type": "bool"},
                                                "acls": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                                "prefix_lists": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                            },
                                        },
                                        "next_hop": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "acls": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                                "prefix_lists": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                            },
                                        },
                                        "redistribution_source": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "acls": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                                "prefix_lists": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                            },
                                        },
                                        "route_source": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "redistribution_source": {
                                                    "type": "bool"
                                                },
                                                "acls": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                                "prefix_lists": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                            },
                                        },
                                    },
                                },
                                "ipv6": {
                                    "type": "dict",
                                    "options": {
                                        "address": {
                                            "type": "dict",
                                            "options": {
                                                "acl": {"type": "str"},
                                                "prefix_list": {"type": "str"},
                                            },
                                        },
                                        "flowspec": {
                                            "type": "dict",
                                            "options": {
                                                "dest_pfx": {"type": "bool"},
                                                "src_pfx": {"type": "bool"},
                                                "acl": {"type": "str"},
                                                "prefix_list": {"type": "str"},
                                            },
                                        },
                                        "next_hop": {
                                            "type": "dict",
                                            "options": {
                                                "acl": {"type": "str"},
                                                "prefix_list": {"type": "str"},
                                            },
                                        },
                                        "route_source": {
                                            "type": "dict",
                                            "options": {
                                                "acl": {"type": "str"},
                                                "prefix_list": {"type": "str"},
                                            },
                                        },
                                    },
                                },
                                "length": {
                                    "type": "dict",
                                    "options": {
                                        "minimum": {"type": "int"},
                                        "maximum": {"type": "int"},
                                    },
                                },
                                "local_preference": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "value": {
                                            "type": "list",
                                            "elements": "str",
                                        },
                                    },
                                },
                                "mdt_group": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "acls": {
                                            "type": "list",
                                            "elements": "str",
                                        },
                                    },
                                },
                                "metric": {
                                    "type": "dict",
                                    "options": {
                                        "value": {"type": "int"},
                                        "external": {"type": "bool"},
                                        "deviation": {"type": "bool"},
                                        "deviation_value": {"type": "int"},
                                    },
                                },
                                "mpls_label": {"type": "bool"},
                                "policy_lists": {
                                    "type": "list",
                                    "elements": "str",
                                },
                                "route_type": {
                                    "type": "dict",
                                    "options": {
                                        "external": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "type_1": {"type": "bool"},
                                                "type_2": {"type": "bool"},
                                            },
                                        },
                                        "internal": {"type": "bool"},
                                        "level_1": {"type": "bool"},
                                        "level_2": {"type": "bool"},
                                        "local": {"type": "bool"},
                                        "nssa_external": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "type_1": {"type": "bool"},
                                                "type_2": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "rpki": {
                                    "type": "dict",
                                    "options": {
                                        "invalid": {"type": "bool"},
                                        "not_found": {"type": "bool"},
                                        "valid": {"type": "bool"},
                                    },
                                },
                                "security_group": {
                                    "type": "dict",
                                    "options": {
                                        "source": {
                                            "type": "list",
                                            "elements": "int",
                                        },
                                        "destination": {
                                            "type": "list",
                                            "elements": "int",
                                        },
                                    },
                                },
                                "source_protocol": {
                                    "type": "dict",
                                    "options": {
                                        "bgp": {"type": "str"},
                                        "connected": {"type": "bool"},
                                        "eigrp": {"type": "int"},
                                        "isis": {"type": "bool"},
                                        "lisp": {"type": "bool"},
                                        "mobile": {"type": "bool"},
                                        "ospf": {"type": "int"},
                                        "ospfv3": {"type": "int"},
                                        "rip": {"type": "bool"},
                                        "static": {"type": "bool"},
                                    },
                                },
                                "tag": {
                                    "type": "dict",
                                    "options": {
                                        "value": {
                                            "type": "list",
                                            "elements": "str",
                                        },
                                        "tag_list": {
                                            "type": "list",
                                            "elements": "str",
                                        },
                                    },
                                },
                                "track": {"type": "int"},
                            },
                        },
                        "set": {
                            "type": "dict",
                            "options": {
                                "aigp_metric": {
                                    "type": "dict",
                                    "options": {
                                        "value": {"type": "int"},
                                        "igp_metric": {"type": "bool"},
                                    },
                                },
                                "as_path": {
                                    "type": "dict",
                                    "options": {
                                        "prepend": {
                                            "type": "dict",
                                            "options": {
                                                "as_number": {
                                                    "type": "list",
                                                    "elements": "str",
                                                },
                                                "last_as": {"type": "int"},
                                            },
                                        },
                                        "tag": {"type": "bool"},
                                    },
                                },
                                "automatic_tag": {"type": "bool"},
                                "clns": {"type": "str"},
                                "comm_list": {"type": "str"},
                                "community": {
                                    "type": "dict",
                                    "options": {
                                        "number": {"type": "str"},
                                        "additive": {"type": "bool"},
                                        "gshut": {"type": "bool"},
                                        "internet": {"type": "bool"},
                                        "local_as": {"type": "bool"},
                                        "no_advertise": {"type": "bool"},
                                        "no_export": {"type": "bool"},
                                        "none": {"type": "bool"},
                                    },
                                },
                                "dampening": {
                                    "type": "dict",
                                    "options": {
                                        "penalty_half_time": {"type": "int"},
                                        "reuse_route_val": {"type": "int"},
                                        "suppress_route_val": {"type": "int"},
                                        "max_suppress": {"type": "int"},
                                    },
                                },
                                "default": {"type": "str"},
                                "extcomm_list": {"type": "str"},
                                "extcommunity": {
                                    "type": "dict",
                                    "options": {
                                        "cost": {
                                            "type": "dict",
                                            "options": {
                                                "id": {"type": "str"},
                                                "cost_value": {"type": "int"},
                                                "igp": {"type": "bool"},
                                                "pre_bestpath": {
                                                    "type": "bool"
                                                },
                                            },
                                        },
                                        "rt": {
                                            "type": "dict",
                                            "options": {
                                                "address": {"type": "str"},
                                                "range": {
                                                    "type": "dict",
                                                    "options": {
                                                        "lower_limit": {
                                                            "type": "str"
                                                        },
                                                        "upper_limit": {
                                                            "type": "str"
                                                        },
                                                    },
                                                },
                                                "additive": {"type": "bool"},
                                            },
                                        },
                                        "soo": {"type": "str"},
                                        "vpn_distinguisher": {
                                            "type": "dict",
                                            "options": {
                                                "address": {"type": "str"},
                                                "range": {
                                                    "type": "dict",
                                                    "options": {
                                                        "lower_limit": {
                                                            "type": "str"
                                                        },
                                                        "upper_limit": {
                                                            "type": "str"
                                                        },
                                                    },
                                                },
                                                "additive": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                                "global_route": {"type": "bool"},
                                "interfaces": {
                                    "type": "list",
                                    "elements": "str",
                                },
                                "ip": {
                                    "type": "dict",
                                    "options": {
                                        "address": {"type": "str"},
                                        "df": {
                                            "choices": [0, 1],
                                            "type": "int",
                                        },
                                        "global_route": {
                                            "type": "dict",
                                            "options": {
                                                "address": {"type": "str"},
                                                "verify_availability": {
                                                    "type": "dict",
                                                    "options": {
                                                        "address": {
                                                            "type": "str"
                                                        },
                                                        "sequence": {
                                                            "type": "int"
                                                        },
                                                        "track": {
                                                            "type": "int"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "next_hop": {
                                            "type": "dict",
                                            "options": {
                                                "address": {"type": "str"},
                                                "dynamic": {"type": "bool"},
                                                "encapsulate": {"type": "str"},
                                                "peer_address": {
                                                    "type": "bool"
                                                },
                                                "recursive": {
                                                    "type": "dict",
                                                    "options": {
                                                        "address": {
                                                            "type": "str"
                                                        },
                                                        "global_route": {
                                                            "type": "bool"
                                                        },
                                                        "vrf": {"type": "str"},
                                                    },
                                                },
                                                "self": {"type": "bool"},
                                                "verify_availability": {
                                                    "type": "dict",
                                                    "options": {
                                                        "set": {
                                                            "type": "bool"
                                                        },
                                                        "address": {},
                                                        "sequence": {
                                                            "type": "int"
                                                        },
                                                        "track": {
                                                            "type": "int"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "precedence": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "critical": {"type": "bool"},
                                                "flash": {"type": "bool"},
                                                "flash_override": {
                                                    "type": "bool"
                                                },
                                                "immediate": {"type": "bool"},
                                                "internet": {"type": "bool"},
                                                "network": {"type": "bool"},
                                                "priority": {"type": "bool"},
                                                "routine": {"type": "bool"},
                                            },
                                        },
                                        "qos_group": {"type": "int"},
                                        "tos": {
                                            "type": "dict",
                                            "options": {
                                                "set": {"type": "bool"},
                                                "max_reliability": {
                                                    "type": "bool"
                                                },
                                                "max_throughput": {
                                                    "type": "bool"
                                                },
                                                "min_delay": {"type": "bool"},
                                                "min_monetary_cost": {
                                                    "type": "bool"
                                                },
                                                "normal": {"type": "bool"},
                                            },
                                        },
                                        "vrf": {
                                            "type": "dict",
                                            "options": {
                                                "name": {"type": "str"},
                                                "address": {"type": "str"},
                                                "verify_availability": {
                                                    "type": "dict",
                                                    "options": {
                                                        "set": {
                                                            "type": "bool"
                                                        },
                                                        "address": {},
                                                        "sequence": {
                                                            "type": "int"
                                                        },
                                                        "track": {
                                                            "type": "int"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "ipv6": {
                                    "type": "dict",
                                    "options": {
                                        "address": {"type": "str"},
                                        "default": {"type": "bool"},
                                        "global_route": {
                                            "type": "dict",
                                            "options": {
                                                "address": {"type": "str"},
                                                "verify_availability": {
                                                    "type": "dict",
                                                    "options": {
                                                        "address": {
                                                            "type": "str"
                                                        },
                                                        "sequence": {
                                                            "type": "int"
                                                        },
                                                        "track": {
                                                            "type": "int"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "next_hop": {
                                            "type": "dict",
                                            "options": {
                                                "address": {"type": "str"},
                                                "encapsulate": {"type": "str"},
                                                "peer_address": {
                                                    "type": "bool"
                                                },
                                                "recursive": {"type": "str"},
                                            },
                                        },
                                        "precedence": {"type": "int"},
                                        "vrf": {
                                            "type": "dict",
                                            "options": {
                                                "name": {"type": "str"},
                                                "verify_availability": {
                                                    "type": "dict",
                                                    "options": {
                                                        "address": {},
                                                        "sequence": {
                                                            "type": "int"
                                                        },
                                                        "track": {
                                                            "type": "int"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "level": {
                                    "type": "dict",
                                    "options": {
                                        "level_1": {"type": "bool"},
                                        "level_1_2": {"type": "bool"},
                                        "level_2": {"type": "bool"},
                                        "nssa_only": {"type": "bool"},
                                    },
                                },
                                "lisp": {"type": "str"},
                                "local_preference": {"type": "int"},
                                "metric": {
                                    "type": "dict",
                                    "options": {
                                        "deviation": {
                                            "choices": ["plus", "minus"],
                                            "type": "str",
                                        },
                                        "metric_value": {"type": "int"},
                                        "eigrp_delay": {"type": "int"},
                                        "metric_reliability": {"type": "int"},
                                        "metric_bandwidth": {"type": "int"},
                                        "mtu": {"type": "int"},
                                    },
                                },
                                "metric_type": {
                                    "type": "dict",
                                    "options": {
                                        "external": {"type": "bool"},
                                        "internal": {"type": "bool"},
                                        "type_1": {"type": "bool"},
                                        "type_2": {"type": "bool"},
                                    },
                                },
                                "mpls_label": {"type": "bool"},
                                "origin": {
                                    "type": "dict",
                                    "options": {
                                        "igp": {"type": "bool"},
                                        "incomplete": {"type": "bool"},
                                    },
                                },
                                "tag": {"type": "str"},
                                "traffic_index": {"type": "int"},
                                "vrf": {"type": "str"},
                                "weight": {"type": "int"},
                            },
                        },
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "parsed",
                "rendered",
            ],
            "default": "merged",
        },
    }
