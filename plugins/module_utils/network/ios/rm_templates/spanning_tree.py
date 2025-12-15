# -*- coding: utf-8 -*-
# Copyright 2023 Timur Nizharadze (@tnizharadze)
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
    for each in data["mst"]["priority"]:
        cmd.append("spanning-tree mst {instance} priority {value}".format(**each))
    return cmd


def _tmplt_spanning_tree_mst_config_instances(data):
    cmd = []
    for each in data["mst"]["configuration"]["instances"]:
        cmd.append("instance {instance} vlan {vlan_list}".format(**each))
    return cmd


def _tmplt_spanning_tree_priority(data):
    cmd = []
    for each in data["priority"]:
        cmd.append("spanning-tree vlan {vlan_list} priority {value}".format(**each))
    return cmd


def _tmplt_spanning_tree_max_age(data):
    cmd = []
    for each in data["max_age"]:
        cmd.append("spanning-tree vlan {vlan_list} max-age {value}".format(**each))
    return cmd


def _tmplt_spanning_tree_hello_time(data):
    cmd = []
    for each in data["hello_time"]:
        cmd.append("spanning-tree vlan {vlan_list} hello-time {value}".format(**each))
    return cmd


def _tmplt_spanning_tree_forward_time(data):
    cmd = []
    for each in data["forward_time"]:
        cmd.append("spanning-tree vlan {vlan_list} forward-time {value}".format(**each))
    return cmd


class Spanning_treeTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Spanning_treeTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "backbonefast",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<backbonefast>backbonefast))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree backbonefast",
            "result": {
                "backbonefast": "{{ not not backbonefast }}",
            },
        },
        {
            "name": "bridge_assurance",
            "getval": re.compile(
                r"""
                ((?P<negated>no\s)?spanning-tree\sbridge\s(?P<bridge_assurance>assurance))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bridge assurance",
            "result": {
                "bridge_assurance": "{{ False if negated is defined else (not not bridge_assurance) }}",
            },
        },
        {
            "name": "etherchannel_guard_misconfig",
            "getval": re.compile(
                r"""
                ((?P<negated>no\s)?spanning-tree\setherchannel\sguard\s(?P<etherchannel_guard_misconfig>misconfig))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree etherchannel guard misconfig",
            "result": {
                "etherchannel_guard_misconfig": "{{ False if negated is defined else (not not etherchannel_guard_misconfig) }}",
            },
        },
        {
            "name": "logging",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<logging>logging))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree logging",
            "result": {
                "logging": "{{ not not logging }}",
            },
        },
        {
            "name": "loopguard_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sloopguard\s(?P<loopguard_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree loopguard default",
            "result": {
                "loopguard_default": "{{ not not loopguard_default }}",
            },
        },
        {
            "name": "mode",
            "getval": re.compile(
                r"""
                (spanning-tree\smode\s(?P<mode>mst|pvst|rapid-pvst))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mode {{ mode }}",
            "result": {
                "mode": "{{ mode }}",
            },
        },
        {
            "name": "pathcost_method",
            "getval": re.compile(
                r"""
                (spanning-tree\spathcost\smethod\s(?P<pathcost_method>long|short))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree pathcost method {{ pathcost_method }}",
            "result": {
                "pathcost_method": "{{ pathcost_method }}",
            },
        },
        {
            "name": "transmit_hold_count",
            "getval": re.compile(
                r"""
                (spanning-tree\stransmit\shold-count\s(?P<transmit_hold_count>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree transmit hold-count {{ transmit_hold_count }}",
            "result": {
                "transmit_hold_count": "{{ transmit_hold_count }}",
            },
        },
        {
            "name": "portfast.default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\s(?P<default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast default",
            "result": {
                "portfast": {
                    "default": "{{ not not default }}",
                },
            },
        },
        {
            "name": "portfast.network_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\snetwork\s(?P<network_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast network default",
            "result": {
                "portfast": {
                    "network_default": "{{ not not network_default }}",
                },
            },
        },
        {
            "name": "portfast.edge_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\s(?P<edge_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast edge default",
            "result": {
                "portfast": {
                    "edge_default": "{{ not not edge_default }}",
                },
            },
        },
        {
            "name": "portfast.edge_bpdufilter_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\sbpdufilter\s(?P<edge_bpdufilter_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast edge bpdufilter default",
            "result": {
                "portfast": {
                    "edge_bpdufilter_default": "{{ not not edge_bpdufilter_default }}",
                },
            },
        },
        {
            "name": "portfast.bpdufilter_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sbpdufilter\s(?P<bpdufilter_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast bpdufilter default",
            "result": {
                "portfast": {
                    "bpdufilter_default": "{{ not not bpdufilter_default }}",
                },
            },
        },
        {
            "name": "portfast.edge_bpduguard_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\sbpduguard\s(?P<edge_bpduguard_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast edge bpduguard default",
            "result": {
                "portfast": {
                    "edge_bpduguard_default": "{{ not not edge_bpduguard_default }}",
                },
            },
        },
        {
            "name": "portfast.bpduguard_default",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sbpduguard\s(?P<bpduguard_default>default))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree portfast bpduguard default",
            "result": {
                "portfast": {
                    "bpduguard_default": "{{ not not bpduguard_default }}",
                },
            },
        },
        {
            "name": "uplinkfast.enabled",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<enabled>uplinkfast)$)?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree uplinkfast",
            "result": {
                "uplinkfast": {
                    "enabled": "{{ not not enabled }}",
                },
            },
        },
        {
            "name": "uplinkfast.max_update_rate",
            "getval": re.compile(
                r"""
                (spanning-tree\suplinkfast\smax-update-rate\s(?P<max_update_rate>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree uplinkfast max-update-rate {{ uplinkfast.max_update_rate }}",
            "result": {
                "uplinkfast": {
                    "max_update_rate": "{{ max_update_rate }}",
                },
            },
        },
        {
            "name": "forward_time",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\sforward-time\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": _tmplt_spanning_tree_forward_time,
            "result": {
                "forward_time": [{
                    "vlan_list": "'{{ vlan_list }}'",
                    "value": "{{ value }}",
                }],
            },
        },
        {
            "name": "hello_time",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\shello-time\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": _tmplt_spanning_tree_hello_time,
            "result": {
                "hello_time": [{
                    "vlan_list": "'{{ vlan_list }}'",
                    "value": "{{ value }}",
                }],
            },
        },
        {
            "name": "max_age",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\smax-age\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": _tmplt_spanning_tree_max_age,
            "result": {
                "max_age": [{
                    "vlan_list": "'{{ vlan_list }}'",
                    "value": "{{ value }}",
                }],
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\spriority\s(?P<value>\d+)
                \s*
                $""", re.VERBOSE,
            ),
            "setval": _tmplt_spanning_tree_priority,
            "result": {
                "priority": [{
                    "vlan_list": "'{{ vlan_list }}'",
                    "value": "{{ value }}",
                }],
            },
        },
        {
            "name": "mst.simulate_pvst_global",
            "getval": re.compile(
                r"""
                ((?P<negated>no\s)?spanning-tree\smst\ssimulate\spvst\s(?P<simulate_pvst_global>global))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst simulate pvst global",
            "result": {
                "mst": {
                    "simulate_pvst_global": "{{ False if negated is defined else (not not simulate_pvst_global) }}",
                },
            },
        },
        {
            "name": "mst.hello_time",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\shello-time\s(?P<hello_time>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst hello-time {{ mst.hello_time }}",
            "result": {
                "mst": {
                    "hello_time": "{{ hello_time }}",
                },
            },
        },
        {
            "name": "mst.forward_time",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\sforward-time\s(?P<forward_time>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst forward-time {{ mst.forward_time }}",
            "result": {
                "mst": {
                    "forward_time": "{{ forward_time }}",
                },
            },
        },
        {
            "name": "mst.max_age",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\smax-age\s(?P<max_age>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst max-age {{ mst.max_age }}",
            "result": {
                "mst": {
                    "max_age": "{{ max_age }}",
                },
            },
        },
        {
            "name": "mst.max_hops",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\smax-hops\s(?P<max_hops>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst max-hops {{ mst.max_hops }}",
            "result": {
                "mst": {
                    "max_hops": "{{ max_hops }}",
                },
            },
        },
        {
            "name": "mst.priority",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\s(?P<instance>[0-9,\,\-]+)\spriority\s(?P<value>\d+))?
                \s*
                $""", re.VERBOSE,
            ),
            "setval": _tmplt_spanning_tree_mst_priority,
            "result": {
                "mst": {
                    "priority": [{
                        "instance": "'{{ instance }}'",
                        "value": "{{ value }}",
                    }],
                },
            },
        },
        {
            "name": "mst.configuration",
            "getval": re.compile(
                r"""
                (spanning-tree\smst\s(?P<enabled>configuration)$)?
                $""", re.VERBOSE,
            ),
            "setval": "{{ 'spanning-tree mst configuration' if mst.configuration is defined else '' }}",
            "result": {
                "mst": {
                    "{{ enabled }}": {},
                },
            },
        },
        {
            "name": "mst.configuration.name",
            "getval": re.compile(
                r"""
                (\sname\s(?P<name>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "name {{ mst.configuration.name }}",
            "result": {
                "mst": {
                    "configuration": {
                        "name": "{{ name }}",
                    },
                },
            },
        },
        {
            "name": "mst.configuration.revision",
            "getval": re.compile(
                r"""
                (\srevision\s(?P<revision>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "revision {{ mst.configuration.revision }}",
            "result": {
                "mst": {
                    "configuration": {
                        "revision": "{{ revision }}",
                    },
                },
            },
        },
        {
            "name": "mst.configuration.instances",
            "getval": re.compile(
                r"""
                (\sinstance\s(?P<instance>\d+)\svlan\s(?P<vlan_list>[0-9,\,\-]+))?
                $""", re.VERBOSE,
            ),
            "setval": _tmplt_spanning_tree_mst_config_instances,
            "result": {
                "mst": {
                    "configuration": {
                        "instances": [{
                            "instance": "{{ instance }}",
                            "vlan_list": "'{{ vlan_list }}'",
                        }],
                    },
                },
            },
        },
    ]
    # fmt: on
