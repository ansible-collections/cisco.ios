# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Ospf_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def _tmplt_ospf_interface_process(config_data):
    import q

    q(config_data)
    if "process" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf {id} area {area_id}".format(**config_data["process"])
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf {id} area {area_id}".format(**config_data["process"])
        if "secondaries" in config_data["process"]:
            command += " secondaries"
    return command


def _tmplt_ip_ospf_authentication(config_data):
    if "authentication" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf authentication"
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf authentication"
        if "key_chain" in config_data["authentication"]:
            command += " key-chain {key_chain}".format(**config_data["authentication"])
        elif "message_digest" in config_data["authentication"]:
            command += " message-digest"
        elif "null" in config_data["authentication"]:
            command += " null"
    return command


def _tmplt_ip_ospf_cost(config_data):
    if "cost" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf cost {interface_cost}".format(**config_data["cost"])
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf cost"
            if "interface_cost" in config_data["cost"]:
                command = "ipv6 ospf cost {interface_cost}".format(**config_data["cost"])
            if "dynamic_cost" in config_data["cost"]:
                if "default" in config_data["cost"]["dynamic_cost"]:
                    command += " dynamic default {default}".format(
                        **config_data["cost"]["dynamic_cost"]
                    )
                elif "hysteresis" in config_data["cost"]["dynamic_cost"]:
                    command += " dynamic hysteresis"
                    if "percent" in config_data["cost"]["dynamic_cost"]["hysteresis"]:
                        command += " percent {percent}".format(
                            **config_data["cost"]["dynamic_cost"]["hysteresis"]
                        )
                    elif "threshold" in config_data["cost"]["dynamic_cost"]["hysteresis"]:
                        command += " threshold {threshold}".format(
                            **config_data["cost"]["dynamic_cost"]["hysteresis"]
                        )
                elif "weight" in config_data["cost"]["dynamic_cost"]:
                    command += " dynamic weight"
                    if "l2_factor" in config_data["cost"]["dynamic_cost"]["weight"]:
                        command += " L2-factor {l2_factor}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
                    elif "latency" in config_data["cost"]["dynamic_cost"]["weight"]:
                        command += " latency {latency}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
                    elif (
                        "oc" in config_data["cost"]["dynamic_cost"]["weight"]
                        and config_data["cost"]["dynamic_cost"]["weight"]["oc"]
                    ):
                        command += " oc cdr"
                    elif "resources" in config_data["cost"]["dynamic_cost"]["weight"]:
                        command += " resources {resources}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
                    elif "throughput" in config_data["cost"]["dynamic_cost"]["weight"]:
                        command += " throughput {throughput}".format(
                            **config_data["cost"]["dynamic_cost"]["weight"]
                        )
    return command


def _tmplt_ip_ospf_dead_interval(config_data):
    if "dead_interval" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf dead-interval"
            if "time" in config_data["dead_interval"]:
                command += " {time}".format(**config_data["dead_interval"])
            elif "minimal" in config_data["dead_interval"]:
                command += " minimal hello-multiplier {minimal}".format(
                    **config_data["dead_interval"]
                )
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf dead-interval {time}".format(**config_data["dead_interval"])
    return command


def _tmplt_ip_ospf_demand_circuit(config_data):
    if "demand_circuit" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf demand-circuit"
            if config_data["demand_circuit"]["ignore"]:
                command += " ignore"
            elif config_data["demand_circuit"]["enable"]:
                return command
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf demand-circuit"
            if config_data["demand_circuit"]["enable"]:
                return command
            elif config_data["demand_circuit"]["ignore"]:
                command += " ignore"
            elif config_data["demand_circuit"]["disable"]:
                command += " disable"
    return command


def _tmplt_ip_ospf_manet(config_data):
    if "manet" in config_data:
        command = "ipv6 ospf manet peering"
        if "cost" in config_data["manet"]:
            command += " cost"
            if "percent" in config_data["manet"]["cost"]:
                command += " percent {percent}".format(**config_data["manet"]["cost"])
            elif "threshold" in config_data["manet"]["cost"]:
                command += " threshold {threshold}".format(**config_data["manet"]["cost"])
        elif "link_metrics" in config_data["manet"]:
            command += " link-metrics"
            if "cost_threshold" in config_data["manet"]["link_metrics"]:
                command += " {cost_threshold}".format(**config_data["manet"]["link_metrics"])
    return command


def _tmplt_ip_ospf_multi_area(config_data):
    if "multi_area" in config_data:
        command = "ip ospf multi-area {id}".format(**config_data["multi_area"])
        if "cost" in config_data["multi_area"]:
            command += " cost {cost}".format(**config_data["multi_area"])
    return command


def _tmplt_ip_ospf_neighbor(config_data):
    if "neighbor" in config_data:
        command = "ipv6 ospf neighbor {address}".format(**config_data["neighbor"])
    if "cost" in config_data["neighbor"]:
        command += " cost {cost}".format(**config_data["neighbor"])
    if "database_filter" in config_data["neighbor"] and config_data["neighbor"]["database_filter"]:
        command += " database-filter all out"
    if "poll_interval" in config_data["neighbor"]:
        command += " poll-interval {poll_interval}".format(
            **config_data["neighbor"]["poll_interval"]
        )
    if "priority" in config_data["neighbor"]:
        command += " priority {priority}".format(**config_data["neighbor"]["priority"])
    return command


def _tmplt_ip_ospf_network(config_data):
    if "network" in config_data:
        if config_data.get("afi") == "ipv4":
            command = "ip ospf network"
        elif config_data.get("afi") == "ipv6":
            command = "ipv6 ospf network"
        if "broadcast" in config_data["network"]:
            command += " broadcast"
        if "manet" in config_data["network"]:
            command += " manet"
        if "non_broadcast" in config_data["network"]:
            command += " non-broadcast"
        if "point_to_multipoint" in config_data["network"]:
            command += " point-to-multipoint"
        if "point_to_point" in config_data["network"]:
            command += " point-to-point"
    return command


def _tmplt_ip_ospf_ttl_security(config_data):
    if "ttl_security" in config_data:
        command = "ip ospf ttl-security"
        if "hops" in config_data["ttl_security"]:
            command += " hops {hops}".format(**config_data["ttl_security"])
    return command


class Ospf_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Ospf_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^interface\s(?P<name>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}", "address_family": {}}},
            "shared": True,
        },
        {
            "name": "process",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf
                (\s(?P<id>\d+))
                (\sarea\s(?P<area>\d+))?
                (\sarea\s(?P<area_ip>\s+))?
                (\s(?P<secondaries>secondaries))?
                (\sinstance\s(?P<instance>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ospf_interface_process,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "process": {
                                "id": "{{ id }}",
                                "area_id": "{{ area }}",
                                "secondaries": "{{ not not secondaries }}",
                                "instance_id": "{{ instance }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "adjacency",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf
                \s(?P<adjacency>adjacency\sstagger\sdisable)
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} adjacency stagger disable",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "adjacency": "{{ not not adjacency }}",
                        },
                    },
                },
            },
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \s+ip\sospf\sauthentication
                (\skey-chain\s(?P<key_chain>\S+))?
                (\s(?P<message_digest>message-digest))?
                (\s(?P<isnull>null))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_authentication,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ip": {
                            "afi": "ipv4",
                            "authentication": {
                                "key_chain": "{{ key_chain }}",
                                "message_digest": "{{ not not message_digest }}",
                                "null": "{{ not not isnull }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sbfd
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} bfd",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "bfd": True,
                        },
                    },
                },
            },
        },
        {
            "name": "cost",
            "getval": re.compile(
                r"""
                \s+ip\sospf
                (\scost\s(?P<cost>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_cost,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ip": {
                            "afi": "ipv4",
                            "cost": {"interface_cost": "{{ cost }}"},
                        },
                    },
                },
            },
        },
        {
            "name": "cost_ipv6_dynamic_cost",
            "getval": re.compile(
                r"""
                \s+ipv6\sospf\scost\s(?P<interface_cost>\d+)
                (\sdynamic)?
                (\sdefault\s(?P<default>\d+))?
                (\shysteresis)?
                (\spercent\s(?P<h_params_p>\d+))?
                (\sthreshold\s(?P<h_params_t>\d+))?
                (\sweight)?
                (\sL2-factor\s(?P<l2_factor>\d+))?
                (\slatency\s(?P<latency>\d+))?
                (\sresources\s(?P<resources>\d+))?
                (\sthroughput\s(?P<throughput>\d+))?
                (\s(?P<weight_oc>oc))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_cost,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ipv6": {
                            "afi": "ipv6",
                            "cost": {
                                "interface_cost": "{{ interface_cost }}",
                                "dynamic_cost": {
                                    "default": "{{ default }}",
                                    "hysteresis": {
                                        "percent": "{{ h_params_p }}",
                                        "threshold": "{{ h_params_t  }}",
                                    },
                                    "weight": {
                                        "l2_factor": "{{ l2_factor  }}",
                                        "latency": "{{ latency  }}",
                                        "oc": "{{ not not weight_oc }}",
                                        "resources": "{{ resources  }}",
                                        "throughput": "{{ throughput }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "database_filter",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sdatabase-filter\sall\sout
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} database-filter all out",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "database_filter": True,
                        },
                    },
                },
            },
        },
        {
            "name": "dead_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sdead-interval
                (\s(?P<seconds>\d+))?
                (\sminimal\shello-multiplier\s(?P<minimal>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_dead_interval,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "dead_interval": {"time": "{{ seconds }}", "minimal": "{{ minimal }}"},
                        },
                    },
                },
            },
        },
        {
            "name": "demand_circuit",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sdemand-circuit
                (\s(?P<ignore>ignore))?
                (\s(?P<disable>disable))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_demand_circuit,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "demand_circuit": {
                                "enable": True,
                                "ignore": "{{ not not ignore }}",
                                "disable": "{{ not not disable }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "flood_reduction",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sflood-reduction
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} flood-reduction",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "flood_reduction": True,
                        },
                    },
                },
            },
        },
        {
            "name": "hello_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf(\shello-interval\s(?P<hello_interval>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} hello-interval {{ hello_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "hello_interval": "{{ hello_interval }}",
                        },
                    },
                },
            },
        },
        {
            "name": "lls",
            "getval": re.compile(
                r"""\s+ip\sospf\slls$""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} lls",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ip": {
                            "afi": "ipv4",
                            "lls": True,
                        },
                    },
                },
            },
        },
        {
            "name": "manet",
            "getval": re.compile(
                r"""
                \s+ipv6\sospf\smanet\speering
                (\scost\spercent\s(?P<cost_p>\d+))?
                (\scost\sthreshold\s(?P<cost_t>\d+))?
                (\slink-metrics\s(?P<link_metrics>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_manet,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ipv6": {
                            "afi": "ipv6",
                            "manet": {
                                "cost": {
                                    "percent": "{{ cost_p }}",
                                    "threshold": "{{ cost_t }}",
                                },
                                "link_metrics": {
                                    "set": "{{ True if link_metrics is not defined and link_metrics is defined  }}",
                                    "cost_threshold": "{{ link_metrics }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "mtu_ignore",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\smtu-ignore
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} mtu-ignore",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "mtu_ignore": True,
                        },
                    },
                },
            },
        },
        {
            "name": "multi_area",
            "getval": re.compile(
                r"""
                \s+ip\sospf\smulti-area\s(?P<multi_area>\d+)
                (\scost\s(?P<cost>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_multi_area,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ip": {
                            "afi": "ipv4",
                            "multi_area": {
                                "id": "{{ multi_area }}",
                                "cost": "{{ cost }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "neighbor",
            "getval": re.compile(
                r"""
                \s+ipv6\sospf\sneighbor\s(?P<address>\S+)
                (\scost\s(?P<cost>\d+))?
                (\s(?P<database_filter>database-filter\sall\sout))?
                (\spoll-interval\s(?P<poll_interval>\d+))?
                (\spriority\s(?P<priority>\d+))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_neighbor,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ipv6": {
                            "afi": "ipv6",
                            "neighbor": {
                                "address": "{{ address }}",
                                "cost": "{{ cost }}",
                                "database_filter": "{{ not not database_filter }}",
                                "poll_interval": "{{ poll_interval }}",
                                "priority": "{{ priority }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "network",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\snetwork
                (\s(?P<broadcast>broadcast))?
                (\s(?P<manet>manet))?
                (\s(?P<non_broadcast>non-broadcast))?
                (\s(?P<point_to_multipoint>point-to-multipoint))?
                (\s(?P<point_to_point>point-to-point))?
                $""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_network,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "network": {
                                "broadcast": "{{ not not broadcast }}",
                                "manet": "{{ not not manet }}",
                                "non_broadcast": "{{ not not non_broadcast }}",
                                "point_to_multipoint": "{{ not not point_to_multipoint }}",
                                "point_to_point": "{{ not not point_to_point }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "prefix_suppression",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sprefix-suppression
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} prefix-suppression",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "prefix_suppression": True,
                        },
                    },
                },
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf
                (\spriority\s(?P<priority>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} priority {{ priority }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "priority": "{{ priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "resync_timeout",
            "getval": re.compile(
                r"""
                \s+ip\sospf
                (\sresync-timeout\s(?P<resync_timeout>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "ip ospf resync-timeout {{ resync_timeout }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ip": {
                            "afi": "ipv4",
                            "resync_timeout": "{{ resync_timeout }}",
                        },
                    },
                },
            },
        },
        {
            "name": "retransmit_interval",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf
                (\sretransmit-interval\s(?P<retransmit_interval>\d+))
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} retransmit-interval {{ retransmit_interval }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "retransmit_interval": "{{ retransmit_interval }}",
                        },
                    },
                },
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                \s+(?P<afi>ip|ipv6)\sospf\sshutdown
                $""",
                re.VERBOSE,
            ),
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} shutdown",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "{{ afi }}": {
                            "afi": "{{ 'ipv4' if afi == 'ip' else 'ipv6' }}",
                            "shutdown": True,
                        },
                    },
                },
            },
        },
        {
            "name": "transmit_delay",
            "getval": re.compile(
                r"""
                \s+ipv6\sospf\stransmit-delay\s(?P<transmit_delay>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "ipv6 ospf transmit-delay {{ transmit_delay }}",
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ipv6": {
                            "afi": "ipv6",
                            "transmit_delay": "{{ transmit_delay }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                \s+ip\sospf\sttl-security\shops\s(?P<hops>\d+)
                *$""",
                re.VERBOSE,
            ),
            "setval": _tmplt_ip_ospf_ttl_security,
            "result": {
                "{{ name }}": {
                    "address_family": {
                        "ip": {
                            "afi": "ipv4",
                            "ttl_security": {
                                "set": True,
                                "hops": "{{ hops }}",
                            },
                        },
                    },
                },
            },
        },
    ]
