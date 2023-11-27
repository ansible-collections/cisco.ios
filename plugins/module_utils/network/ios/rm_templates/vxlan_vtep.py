# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vxlan_vtep parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Vxlan_vtepTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vxlan_vtepTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "interface",
            "getval": re.compile(
                r"""^interface\s(?P<interface>\S+)$""",
                re.VERBOSE,
            ),
            "setval": "interface {{ interface }}",
            "result": {"{{ interface }}": {"interface": "{{ interface }}"}},
            "shared": True,
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""\s+source-interface
                    \s(?P<source_interface>\S+)
                    $""",
                re.VERBOSE,
            ),
            "setval": "source-interface {{ source_interface }}",
            "result": {"{{ interface }}": {"source_interface": "{{ source_interface }}"}},
        },
        {
            "name": "host_reachability_bgp",
            "getval": re.compile(
                r"""\s+host-reachability\sprotocol\sbgp$""",
                re.VERBOSE,
            ),
            "setval": "host-reachability protocol bgp",
            "result": {
                "{{ interface }}": {
                    "host_reachability_bgp": True,
                },
            },
        },
        # member vni starts
        {
            "name": "replication",
            "getval": re.compile(
                r"""
                \s+member\svni\s(?P<vni>\d+)\s(?P<type>mcast-group|ingress-replication)
                (\s(?P<ipv4_mcast_group>[\d.]+))?
                (\s(?P<ipv6_mcast_group>[\da-fA-F:]+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "member vni {{ vni }}"
            "{{ (' ' + 'ingress-replication') if replication.type == 'ingress' else (' ' + 'mcast-group') }}"
            "{{ (' ' + replication.mcast_group.ipv4) if replication.mcast_group is defined and "
            "replication.mcast_group.ipv4 is defined and replication.type == 'static' else '' }}"
            "{{ (' ' + replication.mcast_group.ipv6) if replication.mcast_group is defined and "
            "replication.mcast_group.ipv6 is defined and replication.type == 'static' else '' }}",
            "result": {
                "{{ interface }}": {
                    "member": {
                        "vni": {
                            "l2vni": [
                                {
                                    "vni": "{{ vni }}",
                                    "replication": {
                                        "type": "{{ 'ingress' if type == 'ingress-replication' else 'static' }}",
                                        "mcast_group": {
                                            "ipv4": "{{ ipv4_mcast_group }}",
                                            "ipv6": "{{ ipv6_mcast_group }}",
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "vrf",
            "getval": re.compile(
                r"""
                \s+member\svni
                \s(?P<vni>\d+)
                \svrf\s(?P<vrf>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "member vni {{ vni }} vrf {{ vrf }}",
            "result": {
                "{{ interface }}": {
                    "member": {
                        "vni": {
                            "l3vni": [
                                {
                                    "vni": "{{ vni }}",
                                    "vrf": "{{ vrf }}",
                                },
                            ],
                        },
                    },
                },
            },
        },
        # member vni ends
    ]
    # fmt: on
