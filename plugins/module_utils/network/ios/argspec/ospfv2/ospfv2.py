# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""The arg spec for the ios_ospfv2 module."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class Ospfv2Args:
    """The arg spec for the ios_ospfv2 module."""

    argument_spec = {
        "config": {
            "options": {
                "processes": {
                    "mutually_exclusive": [("passive_interface", "passive_interfaces")],
                    "elements": "dict",
                    "options": {
                        "address_family": {
                            "options": {
                                "default": {"type": "bool"},
                                "snmp_context": {"type": "str"},
                                "topology": {
                                    "options": {
                                        "base": {"type": "bool"},
                                        "name": {"type": "str"},
                                        "tid": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "adjacency": {
                            "options": {
                                "max_adjacency": {"type": "int"},
                                "min_adjacency": {"type": "int"},
                                "none": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "areas": {
                            "elements": "dict",
                            "options": {
                                "area_id": {"type": "str"},
                                "authentication": {
                                    "options": {
                                        "enable": {"type": "bool"},
                                        "message_digest": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "capability": {"type": "bool"},
                                "default_cost": {"type": "int"},
                                "filter_list": {
                                    "elements": "dict",
                                    "options": {
                                        "direction": {
                                            "choices": ["in", "out"],
                                            "required": True,
                                            "type": "str",
                                        },
                                        "name": {"type": "str"},
                                    },
                                    "type": "list",
                                },
                                "nssa": {
                                    "options": {
                                        "default_information_originate": {
                                            "options": {
                                                "metric": {"type": "int"},
                                                "metric_type": {"choices": [1, 2], "type": "int"},
                                                "nssa_only": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                        "no_ext_capability": {"type": "bool"},
                                        "no_redistribution": {"type": "bool"},
                                        "no_summary": {"type": "bool"},
                                        "set": {"type": "bool"},
                                        "translate": {
                                            "choices": ["always", "suppress-fa"],
                                            "type": "str",
                                        },
                                    },
                                    "type": "dict",
                                },
                                "ranges": {
                                    "options": {
                                        "address": {"type": "str"},
                                        "advertise": {"type": "bool"},
                                        "cost": {"type": "int"},
                                        "netmask": {"type": "str"},
                                        "not_advertise": {"type": "bool"},
                                    },
                                    "type": "list",
                                    "elements": "dict",
                                },
                                "sham_link": {
                                    "options": {
                                        "cost": {"type": "int"},
                                        "destination": {"type": "str"},
                                        "source": {"type": "str"},
                                        "ttl_security": {"type": "int"},
                                    },
                                    "type": "dict",
                                },
                                "stub": {
                                    "options": {
                                        "no_ext_capability": {"type": "bool"},
                                        "no_summary": {"type": "bool"},
                                        "set": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "list",
                        },
                        "auto_cost": {
                            "options": {
                                "reference_bandwidth": {"type": "int"},
                                "set": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "bfd": {"type": "bool"},
                        "capability": {
                            "options": {
                                "lls": {"type": "bool"},
                                "opaque": {"type": "bool"},
                                "transit": {"type": "bool"},
                                "vrf_lite": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "compatible": {
                            "options": {
                                "rfc1583": {"type": "bool"},
                                "rfc1587": {"type": "bool"},
                                "rfc5243": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "default_information": {
                            "options": {
                                "always": {"type": "bool"},
                                "metric": {"type": "int"},
                                "metric_type": {"type": "int"},
                                "originate": {"type": "bool"},
                                "route_map": {"type": "str"},
                            },
                            "type": "dict",
                        },
                        "default_metric": {"type": "int"},
                        "discard_route": {
                            "options": {
                                "external": {"type": "int"},
                                "internal": {"type": "int"},
                                "set": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "distance": {
                            "options": {
                                "admin_distance": {
                                    "options": {
                                        "acl": {"type": "str"},
                                        "address": {"type": "str"},
                                        "distance": {"type": "int"},
                                        "wildcard_bits": {"type": "str"},
                                    },
                                    "type": "dict",
                                },
                                "ospf": {
                                    "options": {
                                        "external": {"type": "int"},
                                        "inter_area": {"type": "int"},
                                        "intra_area": {"type": "int"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "distribute_list": {
                            "options": {
                                "acls": {
                                    "elements": "dict",
                                    "options": {
                                        "direction": {
                                            "choices": ["in", "out"],
                                            "required": True,
                                            "type": "str",
                                        },
                                        "interface": {"type": "str"},
                                        "name": {"required": True, "type": "str"},
                                        "protocol": {"type": "str"},
                                    },
                                    "type": "list",
                                },
                                "prefix": {
                                    "options": {
                                        "direction": {
                                            "choices": ["in", "out"],
                                            "required": True,
                                            "type": "str",
                                        },
                                        "gateway_name": {"type": "str"},
                                        "interface": {"type": "str"},
                                        "name": {"required": True, "type": "str"},
                                        "protocol": {"type": "str"},
                                    },
                                    "type": "dict",
                                },
                                "route_map": {
                                    "options": {"name": {"required": True, "type": "str"}},
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "domain_id": {
                            "options": {
                                "ip_address": {
                                    "options": {
                                        "address": {"type": "str"},
                                        "secondary": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "null": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "domain_tag": {"type": "int"},
                        "event_log": {
                            "options": {
                                "enable": {"type": "bool"},
                                "one_shot": {"type": "bool"},
                                "pause": {"type": "bool"},
                                "size": {"type": "int"},
                            },
                            "type": "dict",
                        },
                        "help": {"type": "bool"},
                        "ignore": {"type": "bool"},
                        "interface_id": {"type": "bool"},
                        "ispf": {"type": "bool"},
                        "limit": {
                            "options": {
                                "dc": {
                                    "options": {
                                        "disable": {"type": "bool"},
                                        "number": {"type": "int"},
                                    },
                                    "type": "dict",
                                },
                                "non_dc": {
                                    "options": {
                                        "disable": {"type": "bool"},
                                        "number": {"type": "int"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "local_rib_criteria": {
                            "options": {
                                "enable": {"type": "bool"},
                                "forwarding_address": {"type": "bool"},
                                "inter_area_summary": {"type": "bool"},
                                "nssa_translation": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "log_adjacency_changes": {
                            "options": {"detail": {"type": "bool"}, "set": {"type": "bool"}},
                            "type": "dict",
                        },
                        "max_lsa": {
                            "options": {
                                "ignore_count": {"type": "int"},
                                "ignore_time": {"type": "int"},
                                "number": {"type": "int"},
                                "reset_time": {"type": "int"},
                                "threshold_value": {"type": "int"},
                                "warning_only": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "max_metric": {
                            "options": {
                                "external_lsa": {"type": "int"},
                                "include_stub": {"type": "bool"},
                                "on_startup": {
                                    "options": {
                                        "time": {"type": "int"},
                                        "wait_for_bgp": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "router_lsa": {"required": True, "type": "bool"},
                                "summary_lsa": {"type": "int"},
                            },
                            "type": "dict",
                        },
                        "maximum_paths": {"type": "int"},
                        "mpls": {
                            "options": {
                                "ldp": {
                                    "options": {
                                        "autoconfig": {
                                            "options": {
                                                "area": {"type": "str"},
                                                "set": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                        "sync": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "traffic_eng": {
                                    "options": {
                                        "area": {"type": "str"},
                                        "autoroute_exclude": {"type": "str"},
                                        "interface": {
                                            "options": {
                                                "area": {"type": "int"},
                                                "interface_type": {"type": "str"},
                                            },
                                            "type": "dict",
                                        },
                                        "mesh_group": {
                                            "options": {
                                                "area": {"type": "str"},
                                                "id": {"type": "int"},
                                                "interface": {"type": "str"},
                                            },
                                            "type": "dict",
                                        },
                                        "multicast_intact": {"type": "bool"},
                                        "router_id_interface": {"type": "str"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "neighbor": {
                            "options": {
                                "address": {"type": "str"},
                                "cost": {"type": "int"},
                                "database_filter": {"type": "bool"},
                                "poll_interval": {"type": "int"},
                                "priority": {"type": "int"},
                            },
                            "type": "dict",
                        },
                        "network": {
                            "options": {
                                "address": {"type": "str"},
                                "area": {"type": "str"},
                                "wildcard_bits": {"type": "str"},
                            },
                            "type": "list",
                            "elements": "dict",
                        },
                        "nsf": {
                            "options": {
                                "cisco": {
                                    "options": {
                                        "disable": {"type": "bool"},
                                        "helper": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "ietf": {
                                    "options": {
                                        "disable": {"type": "bool"},
                                        "helper": {"type": "bool"},
                                        "strict_lsa_checking": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "passive_interface": {"type": "str"},
                        "passive_interfaces": {
                            "options": {
                                "default": {"type": "bool"},
                                "interface": {
                                    "options": {
                                        "set_interface": {"type": "bool"},
                                        "name": {"type": "list", "elements": "str"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "prefix_suppression": {"type": "bool"},
                        "priority": {"type": "int"},
                        "process_id": {"required": True, "type": "int"},
                        "queue_depth": {
                            "options": {
                                "hello": {
                                    "options": {
                                        "max_packets": {"type": "int"},
                                        "unlimited": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "update": {
                                    "options": {
                                        "max_packets": {"type": "int"},
                                        "unlimited": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "router_id": {"type": "str"},
                        "shutdown": {"type": "bool"},
                        "summary_address": {
                            "options": {
                                "address": {"type": "str"},
                                "mask": {"type": "str"},
                                "not_advertise": {"type": "bool"},
                                "nssa_only": {"type": "bool"},
                                "tag": {"type": "int"},
                            },
                            "type": "dict",
                        },
                        "timers": {
                            "options": {
                                "lsa": {"type": "int"},
                                "pacing": {
                                    "options": {
                                        "flood": {"type": "int"},
                                        "lsa_group": {"type": "int"},
                                        "retransmission": {"type": "int"},
                                    },
                                    "type": "dict",
                                },
                                "throttle": {
                                    "options": {
                                        "lsa": {
                                            "options": {
                                                "first_delay": {"type": "int"},
                                                "max_delay": {"type": "int"},
                                                "min_delay": {"type": "int"},
                                            },
                                            "type": "dict",
                                        },
                                        "spf": {
                                            "options": {
                                                "between_delay": {"type": "int"},
                                                "max_delay": {"type": "int"},
                                                "receive_delay": {"type": "int"},
                                            },
                                            "type": "dict",
                                        },
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "dict",
                        },
                        "traffic_share": {"type": "bool"},
                        "ttl_security": {
                            "options": {"hops": {"type": "int"}, "set": {"type": "bool"}},
                            "type": "dict",
                        },
                        "vrf": {"type": "str"},
                    },
                    "type": "list",
                },
            },
            "type": "dict",
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
    }
