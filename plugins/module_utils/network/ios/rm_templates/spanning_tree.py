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
    if "loopguard_default" in glob_data:
        cmd.append("spanning-tree loopguard default")
    if "portfast_network_default" in glob_data:
        cmd.append("spanning-tree portfast network default")
    if "portfast_edge_default" in glob_data:
        cmd.append("spanning-tree portfast edge default")
    if "portfast_normal_default" in glob_data:
        cmd.append("spanning-tree portfast normal default")
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
    return cmd

def _tmplt_set_uplinkfast(data):
    cmd = []
    glob_data = data["spanning_tree"]["uplinkfast"]
    if "enabled" in glob_data:
        cmd.append("spanning-tree uplinkfast")
    if "max_update_rate" in glob_data:
        cmd.append("spanning-tree uplinkfast max-update-rate {max_update_rate}".format(**glob_data))
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
                (spanning-tree (?P<backbonefast>backbonefast))?
                (spanning-tree bridge (?P<bridge_assurance>assurance))?
                (spanning-tree etherchannel guard (?P<etherchannel_guard_misconfig>misconfig))?
                (spanning-tree extend (?P<extend_system_id>system-id))?
                (spanning-tree loopguard (?P<loopguard_default>default))?
                (spanning-tree portfast network (?P<portfast_network_default>default))?
                (spanning-tree portfast edge (?P<portfast_edge_default>default))?
                (spanning-tree portfast normal (?P<portfast_normal_default>default))?
                (spanning-tree mode (?P<mode>mst|pvst|rapid-pvst))?
                (spanning-tree pathcost method (?<pathcost_method>long|short))?
                (spanning-tree transmit hold-count (?<transmit_hold_count>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_spanning_tree,
            "result": {
                "backbonefast": "{{ not not backbonefast }}",
                "bridge_assurance": "{{ not not bridge_assurance }}",
                "etherchannel_guard_misconfig": "{{ not not etherchannel_guard_misconfig }}",
                "extend_system_id": "{{ not not extend_system_id }}",
                "loopguard_default": "{{ not not loopguard_default }}",
                "portfast_network_default": "{{ not not portfast_network_default }}",
                "portfast_edge_default": "{{ not not portfast_edge_default }}",
                "portfast_normal_default": "{{ not not portfast_normal_default }}",
                "mode": "{{ spanning_tree.mode }}",
                "pathcost_method": "{{ spanning_tree.pathcost_method }}",
                "transmit_hold_count": "{{ spanning_tree.transmit_hold_count }}"
            },
        },
        {
            "name": "spanning_tree.portfast",
            "getval": re.compile(
                r"""
                (spanning-tree portfast edge bpdufilter (?P<bpdufilter_default>default))?
                (spanning-tree portfast edge bpduguard (?P<bpduguard_default>default))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_portfast,
            "result": {
                "bpdufilter_default": "{{ not not bpdufilter_default }}",
                "bpduguard_default": "{{ not not bpduguard_default }}",
            },
        },
        {
            "name": "spanning_tree.uplinkfast",
            "getval": re.compile(
                r"""
                (spanning-tree (?P<enabled>uplinkfast)$)?
                (spanning-tree uplinkfast max-update-rate (?P<max_update_rate>\d+))?
                \s*
                $""", re.VERBOSE),
            "setval": _tmplt_set_uplinkfast,
            "result": {
                "enabled": "{{ not not enabled }}",
                "max_update_rate": "{{ spanning_tree.uplinkfast.max_update_rate }}",
            },
        },
    ]
    # fmt: on
