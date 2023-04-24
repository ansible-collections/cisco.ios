# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Spanning_tree parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

def _tmplt_spanning_tree_mst_priority(data):
    cmd = []
    for each in data["spanning_tree"]["mst"]["priority"]:
        cmd.append("spanning-tree mst {instance} priority {value}".format(**each))
    return cmd

def _tmplt_spanning_tree_mst_config_instances(data):
    cmd = []
    for each in data["spanning_tree"]["mst"]["configuration"]["instances"]:
        cmd.append("instance {instance} vlan {vlan_list}".format(**each))
    return cmd

def _tmplt_spanning_tree_priority(data):
    cmd = []
    for each in data["spanning_tree"]["priority"]:
        cmd.append("spanning-tree vlan {vlan_list} priority {value}".format(**each))
    return cmd

def _tmplt_spanning_tree_max_age(data):
    cmd = []
    for each in data["spanning_tree"]["max_age"]:
        cmd.append("spanning-tree vlan {vlan_list} max-age {value}".format(**each))
    return cmd

def _tmplt_spanning_tree_hello_time(data):
    cmd = []
    for each in data["spanning_tree"]["hello_time"]:
        cmd.append("spanning-tree vlan {vlan_list} hello-time {value}".format(**each))
    return cmd

def _tmplt_spanning_tree_forward_time(data):
    cmd = []
    for each in data["spanning_tree"]["forward_time"]:
        cmd.append("spanning-tree vlan {vlan_list} forward-time {value}".format(**each))
    return cmd

class Spanning_treeTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Spanning_treeTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "spanning_tree.backbonefast",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<backbonefast>backbonefast))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree backbonefast",
            "result": {
                "spanning_tree": {
                    "backbonefast": "{{ not not backbonefast }}",
                },
            },
        },
        {
            "name": "spanning_tree.bridge_assurance",
            "getval": re.compile(
                r"""
                ((?P<negated>no\s)?spanning-tree\sbridge\s(?P<bridge_assurance>assurance))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree bridge assurance",
            "result": {
                "spanning_tree": {
                    "bridge_assurance": "{{ False if negated is defined else (not not bridge_assurance) }}",
                },
            },
        },
        {
            "name": "spanning_tree.etherchannel_guard_misconfig",
            "getval": re.compile(
                r"""
                ((?P<negated>no\s)?spanning-tree\setherchannel\sguard\s(?P<etherchannel_guard_misconfig>misconfig))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree etherchannel guard misconfig",
            "result": {
                "spanning_tree": {
                    "etherchannel_guard_misconfig": "{{ False if negated is defined else (not not etherchannel_guard_misconfig) }}",
                },
            },
        },
        {
            "name": "spanning_tree.extend_system_id",
            "getval": re.compile(
                r"""
                (spanning-tree\sextend\s(?P<extend_system_id>system-id))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree extend system-id",
            "result": {
                "spanning_tree": {
                    "extend_system_id": "{{ not not extend_system_id }}",
                },
            },
        },
        {
            "name": "spanning_tree.logging",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<logging>logging))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree logging",
            "result": {
                "spanning_tree": {
                    "logging": "{{ not not logging }}",
                },
            },
        },
        {
            "name": "spanning_tree.loopguard_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sloopguard\s(?P<loopguard_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree loopguard default",
            "result": {
                "spanning_tree": {
                    "loopguard_default": "{{ not not loopguard_default }}",
                },
            },
        },
        {
            "name": "spanning_tree.mode",
            "getval": re.compile(
                r"""
                (spanning-tree\smode\s(?P<mode>mst|pvst|rapid-pvst))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree mode {{ spanning_tree.mode }}",
            "result": {
                "spanning_tree": {
                    "mode": "{{ mode }}",
                },
            },
        },
        {
            "name": "spanning_tree.pathcost_method",
            "getval": re.compile(
                r"""
                (spanning-tree\spathcost\smethod\s(?P<pathcost_method>long|short))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree pathcost method {{ spanning_tree.pathcost_method }}",
            "result": {
                "spanning_tree": {
                    "pathcost_method": "{{ pathcost_method }}",
                },
            },
        },
        {
            "name": "spanning_tree.transmit_hold_count",
            "getval": re.compile(
                r"""
                (spanning-tree\stransmit\shold-count\s(?P<transmit_hold_count>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree transmit hold-count {{ spanning_tree.transmit_hold_count }}",
            "result": {
                "spanning_tree": {
                    "transmit_hold_count": "{{ transmit_hold_count }}"
                },
            },
        },
        {
            "name": "spanning_tree.portfast.network_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\snetwork\s(?P<network_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree portfast network default",
            "result": {
                "spanning_tree": {
                    "portfast": {
                        "network_default": "{{ not not network_default }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.portfast.edge_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\s(?P<edge_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree portfast edge default",
            "result": {
                "spanning_tree": {
                    "portfast": {
                        "edge_default": "{{ not not edge_default }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.portfast.bpdufilter_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\sbpdufilter\s(?P<bpdufilter_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree portfast edge bpdufilter default",
            "result": {
                "spanning_tree": {
                    "portfast": {
                        "bpdufilter_default": "{{ not not bpdufilter_default }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.portfast.bpduguard_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\sbpduguard\s(?P<bpduguard_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree portfast edge bpduguard default",
            "result": {
                "spanning_tree": {
                    "portfast": {
                        "bpduguard_default": "{{ not not bpduguard_default }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.uplinkfast.enabled",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<enabled>uplinkfast)$)?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree uplinkfast",
            "result": {
                "spanning_tree": {
                    "uplinkfast": {
                        "enabled": "{{ not not enabled }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.uplinkfast.max_update_rate",
            "getval": re.compile(
                r"""
                (spanning-tree\suplinkfast\smax-update-rate\s(?P<max_update_rate>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree uplinkfast max-update-rate {{ spanning_tree.uplinkfast.max_update_rate }}",
            "result": {
                "spanning_tree": {
                    "uplinkfast": {
                        "max_update_rate": "{{ max_update_rate }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.forward_time",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\sforward-time\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_spanning_tree_forward_time,
            "result": {
                "spanning_tree": {
                    "forward_time": [ {
                        "vlan_list": "'{{ vlan_list }}'",
                        "value": "{{ value }}",
                    } ],
                },
            },
        },
        {
            "name": "spanning_tree.hello_time",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\shello-time\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_spanning_tree_hello_time,
            "result": {
                "spanning_tree": {
                    "hello_time": [ {
                        "vlan_list": "'{{ vlan_list }}'",
                        "value": "{{ value }}",
                    } ],
                },
            },
        },
        {
            "name": "spanning_tree.max_age",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\smax-age\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_spanning_tree_max_age,
            "result": {
                "spanning_tree": {
                    "max_age": [ {
                        "vlan_list": "'{{ vlan_list }}'",
                        "value": "{{ value }}",
                    } ],
                },
            },
        },
        {
            "name": "spanning_tree.priority",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\spriority\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_spanning_tree_priority,
            "result": {
                "spanning_tree": {
                    "priority": [ {
                        "vlan_list": "'{{ vlan_list }}'",
                        "value": "{{ value }}",
                    } ],
                },
            },
        },
        {
            "name": "spanning_tree.mst.simulate_pvst_global",
            "getval": re.compile(
                r"""
                ((?P<negated>no\s)?spanning-tree\smst\ssimulate\spvst\s(?P<simulate_pvst_global>global))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree mst simulate pvst global",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "simulate_pvst_global": "{{ False if negated is defined else (not not simulate_pvst_global) }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.hello_time",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\shello-time\s(?P<hello_time>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree mst hello-time {{ spanning_tree.mst.hello_time }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "hello_time": "{{ hello_time }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.forward_time",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\sforward-time\s(?P<forward_time>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree mst forward-time {{ spanning_tree.mst.forward_time }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "forward_time": "{{ forward_time }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.max_age",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\smax-age\s(?P<max_age>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree mst max-age {{ spanning_tree.mst.max_age }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "max_age": "{{ max_age }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.max_hops",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\smax-hops\s(?P<max_hops>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": "spanning-tree mst max-hops {{ spanning_tree.mst.max_hops }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "max_hops": "{{ max_hops }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.priority",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\s(?P<instance>[0-9,\,\-]+)\spriority\s(?P<value>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_spanning_tree_mst_priority,
            "result": {
                "spanning_tree": {
                    "mst": {
                        "priority": [ {
                            "instance": "'{{ instance }}'",
                            "value": "{{ value }}"
                        } ],
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.configuration",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\s(?P<enabled>configuration)$)?
                $""", re.VERBOSE),
            "setval": "{{ 'spanning-tree mst configuration' if spanning_tree.mst.configuration is defined else '' }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "{{ enabled }}": {},
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.configuration.name",
            "getval": re.compile(
                r"""
                (\sname\s(?P<name>\S+))?
                $""", re.VERBOSE),
            "setval": "name {{ spanning_tree.mst.configuration.name }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "configuration": {
                            "name": "{{ name }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.configuration.revision",
            "getval": re.compile(
                r"""
                (\srevision\s(?P<revision>\d+))?
                $""", re.VERBOSE),
            "setval": "revision {{ spanning_tree.mst.configuration.revision }}",
            "result": {
                "spanning_tree": {
                    "mst": {
                        "configuration": {
                            "revision": "{{ revision }}",
                        },
                    },
                },
            },
        },
        {
            "name": "spanning_tree.mst.configuration.instances",
            "getval": re.compile(
                r"""
                (\sinstance\s(?P<instance>\d+)\svlan\s(?P<vlan_list>[0-9,\,\-]+))?
                $""", re.VERBOSE),
            "setval": _tmplt_spanning_tree_mst_config_instances,
            "result": {
                "spanning_tree": {
                    "mst": {
                        "configuration": {
                            "instances": [ {
                                "instance": "{{ instance }}",
                                "vlan_list": "'{{ vlan_list }}'",
                            } ],
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
