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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} {{ process.id|string }}"
            "{{ (' area ' + process.area_id|string ) if process.area_id is defined else '' }}"
            "{{ (' ' + secondaries) if process.secondaries is defined else '' }}"
            "{{ (' instance ' + process.instance) if process.instance is defined else '' }}",
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
            "setval": "ip ospf authentication"
            "{{ (' key-chain ' + authentication.key_chain) if authentication.key_chain is defined else '' }}"
            "{{ (' ' + message-digest) if authentication.message_digest is defined else '' }}"
            "{{ (' ' + null) if authentication.null is defined else '' }}",
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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} cost"
            " {{ cost.interface_cost|string }}",
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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} cost"
            " {{ cost.interface_cost|string }}",
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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} dead-interval {{ dead_interval.time|string }}"
            "{{ (' minimal hello-multiplier ' + dead_interval.minimal|string) if dead_interval.minimal is defined else '' }}",
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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} demand-circuit"
            "{{ ' ignore' if demand_circuit.ignore is defined else '' }}"
            "{{ ' disable' if demand_circuit.disable is defined else '' }}",
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
            "setval": "ipv6 ospf manet peering"
            "{{ ' cost' if manet.cost is defined else '' }}"
            "{{ (' percent ' + manet.cost.percent|string ) if manet.cost.percent is defined else '' }}"
            "{{ (' threshold ' + manet.cost.threshold|string ) if manet.cost.threshold is defined else '' }}"
            "{{ ' link-metrics' if manet.link_metrics is defined else '' }}"
            "{{ (' ' + manet.link_metrics.cost_threshold) if manet.link_metrics is defined and manet.link_metrics.cost_threshold is defined  else '' }}",
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
            "setval": "ip ospf multi-area {{ multi_area.id|string }}"
            "{{ (' cost ' + multi_area.cost|string ) if multi_area.cost is defined else '' }}",
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
            "setval": "ipv6 ospf neighbor {{ neighbor.address }}"
            "{{ (' cost ' + neighbor.cost|string ) if neighbor.cost is defined else '' }}"
            "{{ ' database-filter all out' if neighbor.database_filter is defined else '' }}"
            "{{ (' poll-interval ' + neighbor.poll_interval|string ) if neighbor.poll_interval is defined else '' }}"
            "{{ (' priority ' + neighbor.priority|string ) if neighbor.priority is defined else '' }}",
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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} network"
            "{{ ' broadcast' if network.broadcast is defined else '' }}"
            "{{ ' manet' if network.manet is defined else '' }}"
            "{{ ' non-broadcast' if network.non_broadcast is defined else '' }}"
            "{{ ' point-to-multipoint' if network.point_to_multipoint is defined else '' }}"
            "{{ ' point-to-point' if network.point_to_point is defined else '' }}",
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
            "setval": "ip ospf resync-timeout {{ resync_timeout|string }}",
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
            "setval": "{{ 'ip ospf' if afi == 'ipv4' else 'ipv6 ospf' }} retransmit-interval {{ retransmit_interval|string }}",
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
            "setval": "ipv6 ospf transmit-delay {{ transmit_delay|string }}",
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
            "setval": "ip ospf ttl-security"
            "{{ (' hops ' + ttl_security.hops|string) if ttl_security.hops is defined else '' }}",
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
