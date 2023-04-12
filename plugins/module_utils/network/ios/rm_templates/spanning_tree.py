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

def _tmplt_set_spanning_tree(data):
    cmd = []
    glob_data = data["spanning_tree"]

    if "backbonefast" in glob_data:
        cmd.append("spanning-tree backbonefast")
    if "bridge_assurance" in glob_data:
        cmd.append("spanning-tree bridge assurance")
    if "etherchannel_guard_misconfig" in glob_data:
        cmd.append("spanning-tree etherchannel guard misconfig")
    if "extend_system_id" in glob_data:
        cmd.append("spanning-tree extend system-id")
    if "logging" in glob_data:
        cmd.append("spanning-tree logging")
    if "loopguard_default" in glob_data:
        cmd.append("spanning-tree loopguard default")
    if "mode" in glob_data:
        cmd.append("spanning-tree mode {mode}".format(**glob_data))
    if "pathcost_method" in glob_data:
        cmd.append("spanning-tree pathcost method {pathcost_method}".format(**glob_data))
    if "transmit_hold_count" in glob_data:
        cmd.append("spanning-tree transmit hold-count {transmit_hold_count}".format(**glob_data))
    return cmd

def _tmplt_set_portfast(data):
    cmd = []
    glob_data = data["spanning_tree"]["portfast"]
    if "bpdufilter_default" in glob_data:
        cmd.append("spanning-tree portfast edge bpdufilter default")
    if "bpduguard_default" in glob_data:
        cmd.append("spanning-tree portfast edge bpduguard default")
    if "network_default" in glob_data:
        cmd.append("spanning-tree portfast network default")
    if "edge_default" in glob_data:
        cmd.append("spanning-tree portfast edge default")
    if "normal_default" in glob_data:
        cmd.append("spanning-tree portfast normal default")
    return cmd

def _tmplt_set_uplinkfast(data):
    cmd = []
    glob_data = data["spanning_tree"]["uplinkfast"]
    if "enabled" in glob_data:
        cmd.append("spanning-tree uplinkfast")
    if "max_update_rate" in glob_data:
        cmd.append("spanning-tree uplinkfast max-update-rate {max_update_rate}".format(**glob_data))
    return cmd

def vlan_list_to_str(vlan_list):
    seq = []
    final = []
    last = 0
    for index, val in enumerate(vlan_list):
        if last + 1 == val or index == 0:
            seq.append(val)
            last = val
        else:
            if len(seq) > 1:
               final.append(str(seq[0]) + '-' + str(seq[len(seq)-1]))
            else:
               final.append(str(seq[0]))
            seq = []
            seq.append(val)
            last = val
        if index == len(vlan_list) - 1:
            if len(seq) > 1:
                final.append(str(seq[0]) + '-' + str(seq[len(seq)-1]))
            else:
                final.append(str(seq[0]))
    final_str = ','.join(map(str, final))
    return final_str

def _tmplt_set_forward_time(data):
    glob_data = data["spanning_tree"]["forward_time"]
    cmd = "spanning-tree vlan " +  vlan_list_to_str(sorted(glob_data["vlan_list"]))
    cmd += " forward-time { value }".format(**glob_data)
    return cmd

def _tmplt_set_hello_time(data):
    glob_data = data["spanning_tree"]["hello_time"]
    cmd = "spanning-tree vlan " +  vlan_list_to_str(sorted(glob_data["vlan_list"]))
    cmd += " hello-time { value }".format(**glob_data)
    return cmd

def _tmplt_set_max_age(data):
    glob_data = data["spanning_tree"]["max_age"]
    cmd = "spanning-tree vlan " +  vlan_list_to_str(sorted(glob_data["vlan_list"]))
    cmd += " max-age { value }".format(**glob_data)
    return cmd

def _tmplt_set_priority(data):
    glob_data = data["spanning_tree"]["priority"]
    cmd = "spanning-tree vlan " +  vlan_list_to_str(sorted(glob_data["vlan_list"]))
    cmd += " priority { value }".format(**glob_data)
    return cmd

class Spanning_treeTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Spanning_treeTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "spanning_tree",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<backbonefast>backbonefast))?
                (spanning-tree\sbridge\s(?P<bridge_assurance>assurance))?
                (spanning-tree\setherchannel\sguard\s(?P<etherchannel_guard_misconfig>misconfig))?
                (spanning-tree\sextend\s(?P<extend_system_id>system-id))?
                (spanning-tree\s(?P<logging>logging))?
                (spanning-tree\sloopguard\s(?P<loopguard_default>default))?
                (spanning-tree\spathcost\smethod\s(?P<pathcost_method>long|short))?
                (spanning-tree\stransmit\shold-count\s(?P<transmit_hold_count>\d+))?
                (spanning-tree\smode\s(?P<mode>mst|pvst|rapid-pvst))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_spanning_tree,
            "result": {
                "spanning_tree": {
                    "backbonefast": "{{ not not backbonefast }}",
                    "bridge_assurance": "{{ not not bridge_assurance }}",
                    "etherchannel_guard_misconfig": "{{ not not etherchannel_guard_misconfig }}",
                    "extend_system_id": "{{ not not extend_system_id }}",
                    "logging": "{{ not not logging }}",
                    "loopguard_default": "{{ not not loopguard_default }}",
                    "mode": "{{ mode }}",
                    "pathcost_method": "{{ pathcost_method }}",
                    "transmit_hold_count": "{{ transmit_hold_count }}"
                },
            },
        },
        {
            "name": "spanning_tree.portfast",
            "getval": re.compile(
                r"""
                (spanning-tree\sportfast\sedge\sbpdufilter\s(?P<bpdufilter_default>default))?
                (spanning-tree\sportfast\sedge\sbpduguard\s(?P<bpduguard_default>default))?
                (spanning-tree\sportfast\sedge\s(?P<edge_default>default))?
                (spanning-tree\sportfast\snetwork\s(?P<network_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_portfast,
            "result": {
                "spanning_tree": {
                    "portfast": {
                        "network_default": "{{ not not network_default }}",
                        "edge_default": "{{ not not edge_default }}",
                        "bpdufilter_default": "{{ not not bpdufilter_default }}",
                        "bpduguard_default": "{{ not not bpduguard_default }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.uplinkfast",
            "getval": re.compile(
                r"""
                (spanning-tree\s(?P<enabled>uplinkfast)$)?
                (spanning-tree\suplinkfast\smax-update-rate\s(?P<max_update_rate>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_uplinkfast,
            "result": {
                "spanning_tree": {
                    "uplinkfast": {
                        "enabled": "{{ not not enabled }}",
                        "max_update_rate": "{{ max_update_rate }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.forward_time",
            "getval": re.compile(
                r"""
                (spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\sforward-time\s(?P<forward_time>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_forward_time,
            "result": {
                "spanning_tree": {
                    "forward_time": {
                        "vlan_list": "{% set comma_list = vlan_list.split(',') %}"
                                     "{% for comma in comma_list %}"
                                     "{% if '-' in comma %}"
                                     "{% set first,last = comma.split('-') %}"
                                     "{% else %}"
                                     "{% set first,last = comma,comma %}"
                                     "{% endif %}"
                                     "{% for each in range(first|int, last|int + 1) %}"
                                     "{{ each }},"
                                     "{% endfor %}"
                                     "{% endfor %}",
                        "value": "{{ forward_time }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.hello_time",
            "getval": re.compile(
                r"""
                (spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\shello-time\s(?P<hello_time>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_hello_time,
            "result": {
                "spanning_tree": {
                    "hello_time": {
                        "vlan_list": "{% set comma_list = vlan_list.split(',') %}"
                                     "{% for comma in comma_list %}"
                                     "{% if '-' in comma %}"
                                     "{% set first,last = comma.split('-') %}"
                                     "{% else %}"
                                     "{% set first,last = comma,comma %}"
                                     "{% endif %}"
                                     "{% for each in range(first|int, last|int + 1) %}"
                                     "{{ each }},"
                                     "{% endfor %}"
                                     "{% endfor %}",
                        "value": "{{ hello_time }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.max_age",
            "getval": re.compile(
                r"""
                (spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\smax-age\s(?P<max_age>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_max_age,
            "result": {
                "spanning_tree": {
                    "max_age": {
                        "vlan_list": "{% set comma_list = vlan_list.split(',') %}"
                                     "{% for comma in comma_list %}"
                                     "{% if '-' in comma %}"
                                     "{% set first,last = comma.split('-') %}"
                                     "{% else %}"
                                     "{% set first,last = comma,comma %}"
                                     "{% endif %}"
                                     "{% for each in range(first|int, last|int + 1) %}"
                                     "{{ each }},"
                                     "{% endfor %}"
                                     "{% endfor %}",
                        "value": "{{ max_age }}",
                    },
                },
            },
        },
        {
            "name": "spanning_tree.priority",
            "getval": re.compile(
                r"""
                (spanning-tree\svlan\s(?P<vlan_list>[0-9,\,\-]+)\spriority\s(?P<priority>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_priority,
            "result": {
                "spanning_tree": {
                    "priority": {
                        "vlan_list": "{% set comma_list = vlan_list.split(',') %}"
                                     "{% for comma in comma_list %}"
                                     "{% if '-' in comma %}"
                                     "{% set first,last = comma.split('-') %}"
                                     "{% else %}"
                                     "{% set first,last = comma,comma %}"
                                     "{% endif %}"
                                     "{% for each in range(first|int, last|int + 1) %}"
                                     "{{ each }},"
                                     "{% endfor %}"
                                     "{% endfor %}",
                        "value": "{{ priority }}",
                    },
                },
            },
        },
    ]
    # fmt: on
