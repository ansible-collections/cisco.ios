# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vlans parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def vlan_associated_config(config):
    """Generate private-vlan association command with proper error handling"""
    associated = config.get("private_vlan", {}).get("associated", [])
    if not associated:
        return ""
    vlan_ids = [str(vlan) for vlan in associated]
    cmd = ",".join(vlan_ids)
    return "private-vlan association " + cmd


class VlansTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(VlansTemplate, self).__init__(
            lines=lines,
            tmplt=self,
            module=module,
        )

    # fmt: off
    PARSERS = [
        {
            "name": "vlan_configuration",
            "getval": re.compile(
                r"""
                ^vlan\sconfiguration\s(?P<vlan_id>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "vlan configuration {{ vlan_id|string }}",
            "result": {
                "{{ vlan_id }}": {
                    "vlan_id": "{{ vlan_id }}",
                },
            },
            "shared": True,
        },
        {
            "name": "member",
            "getval": re.compile(
                r"""
                \s*member
                (\sevpn-instance\s(?P<inst_vlan_id>\d+))?
                (\svni\s(?P<vni>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "member"
            "{{ (' evpn-instance ' + member.evi|string) if member.evi is defined else '' }}"
            "{{ (' vni ' + member.vni|string) if member.vni is defined else '' }}",
            "result": {
                "{{ vlan_id }}": {
                    "member": {
                        "evi": "{{ inst_vlan_id }}",
                        "vni": "{{ vni }}",
                    },
                },
            },
        },
        {
            "name": "vlans",
            "getval": "",
            "setval": "vlan {{ vlan_id|string }}",
            "result": {},
        },
        {
            "name": "name",
            "getval": "",
            "setval": "name {{ name|string }}",
            "result": {},
        },
        {
            "name": "state",
            "getval": "",
            "setval": "state {{ state }}",
            "result": {},
        },
        {
            "name": "mtu",
            "getval": "",
            "setval": "mtu {{ mtu|string }}",
            "result": {},
        },
        {
            "name": "remote_span",
            "getval": "",
            "setval": "remote-span",
            "result": {},
        },
        {
            "name": "private_vlan.type",
            "getval": "",
            "setval": "private-vlan {{ private_vlan.type if private_vlan.type is defined }}",
            "result": {},
        },
        {
            "name": "private_vlan.associated",
            "getval": "",
            "setval": vlan_associated_config,
            "result": {},
        },
        {
            "name": "shutdown",
            "getval": "",
            "setval": "shutdown",
            "result": {},
        },
    ]
    # fmt: on
